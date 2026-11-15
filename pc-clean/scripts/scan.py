#!/usr/bin/env python3
"""Read-only inventory of the current user's hidden home entries."""

from __future__ import annotations

import argparse
import heapq
import os
import shutil
import signal
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

VERSION = "3.1.0"
MAX_ISSUES = 20


def positive_int(value: str) -> int:
    try:
        number = int(value)
        if 1 <= number <= 3600:
            return number
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("must be an integer between 1 and 3600")


def hidden_name(value: str) -> str:
    if value in (".", "..") or not value.startswith(".") or "/" in value:
        raise argparse.ArgumentTypeError("use a hidden directory name such as .cache")
    return value


def display(path: str) -> str:
    """Keep unusual filenames from splitting or spoofing report lines."""
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in path):
        return repr(path)
    return path


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB"):
        if value < 1024 or unit == "PiB":
            return f"{int(value)} B" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    raise AssertionError("unreachable")


def allocated(info: os.stat_result) -> int:
    return info.st_blocks * 512


def describe(relative: str) -> str:
    """Classify from the path only; never assert that the app still exists."""
    parts = relative.split(os.sep)
    root = parts[0]
    root_files = {
        ".bashrc": "Bash startup settings; preserve",
        ".bash_profile": "Bash login settings; preserve",
        ".bash_logout": "Bash logout settings; preserve",
        ".bash_history": "Bash command history; may contain sensitive data",
        ".zshrc": "Zsh startup settings; preserve",
        ".zprofile": "Zsh login settings; preserve",
        ".zsh_history": "Zsh command history; may contain sensitive data",
        ".profile": "Shell login settings; preserve",
        ".gitconfig": "Git settings; may contain sensitive data, preserve",
        ".git-credentials": "Git credentials; sensitive, preserve",
        ".netrc": "Network credentials/settings; sensitive, preserve",
        ".npmrc": "npm settings; may contain tokens, preserve",
        ".pypirc": "Python package settings; may contain credentials, preserve",
        ".python_history": "Python command history; may contain sensitive data",
        ".Xauthority": "X11 authentication data; sensitive, preserve",
    }
    if len(parts) == 1 and root in root_files:
        return root_files[root] + " (path-based)"
    known = {
        (".agents", "skills"): "Agent skill instructions and scripts; verify usage",
        (".local", "share", "baloo"): "Probable KDE Baloo search index; rebuild affects search",
        (".local", "share", "Steam"): "Probable Steam library/data; may contain games or saves",
        (".local", "share", "flatpak"): "Probable per-user Flatpak applications and runtimes",
        (".cache", "thumbnails"): "Probable desktop thumbnail cache; verify before cleaning",
        (".cache", "pip"): "Probable pip cache; use the tool's own cache controls",
        (".cache", "uv"): "Probable uv cache; use the tool's own cache controls",
        (".cache", "opencode-skills"): "Probable OpenCode skill runtimes/cache; verify usage",
        (".npm", "_cacache"): "Probable npm cache; use npm's cache controls",
        (".bun", "install", "cache"): "Probable Bun package cache; verify tool usage",
    }
    for prefix, label in known.items():
        if tuple(parts[: len(prefix)]) == prefix:
            return label + " (path-based)"
    sensitive = {
        ".ssh": "SSH keys/settings; sensitive, preserve",
        ".gnupg": "GnuPG keys/settings; sensitive, preserve",
        ".pki": "Certificates/keys; sensitive, preserve",
        ".kube": "Kubernetes config/credentials; sensitive, preserve",
        ".mozilla": "Mozilla profiles/data; preserve",
        ".docker": "Docker client settings/credentials; verify before changes",
        ".rustup": "Rust toolchains/settings; verify project dependencies",
        ".cargo": "Cargo packages/toolchains/tools; verify project dependencies",
        ".npm": "npm data; may contain cache or tools, verify",
        ".bun": "Bun data; may contain cache or tools, verify",
        ".cache": "Application caches; verify the specific app before cleanup",
        ".config": "Application configuration/profiles; preserve",
        ".local": "User application data, state, executables or environments",
        ".var": "Possible sandboxed application data; preserve until verified",
    }
    if len(parts) >= 2 and root == ".cache":
        return f"Possible {display(parts[1])} cache (path clue only); verify and close app"
    if len(parts) >= 2 and root == ".config":
        return f"Possible {display(parts[1])} configuration/profile (path clue only); preserve"
    if len(parts) >= 3 and parts[:2] == [".local", "share"]:
        return f"Possible {display(parts[2])} application data (path clue only); verify"
    if len(parts) >= 3 and parts[:2] == [".local", "state"]:
        return f"Possible {display(parts[2])} application state (path clue only); verify"
    if len(parts) >= 3 and parts[:2] == [".local", "venvs"]:
        return f"Possible {display(parts[2])} Python environment; project/tool-specific"
    if len(parts) >= 3 and parts[:2] == [".var", "app"]:
        return f"Possible Flatpak app {display(parts[2])} data (path clue only); preserve"
    return sensitive.get(root, f"Possible {display(root[1:])} data (name clue only); verify")


def is_app_folder(relative: str) -> bool:
    parts = relative.split(os.sep)
    return len(parts) == 2 or (
        len(parts) == 3
        and parts[:2] in ([".local", "share"], [".local", "state"],
                          [".local", "venvs"], [".var", "app"])
    )


def pacman_owner(path: str) -> str:
    """Return a confirmed owner for this exact file, never its directory tree."""
    if not shutil.which("pacman"):
        return "pacman unavailable"
    try:
        result = subprocess.run(
            ["pacman", "-Qqo", "--", path],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, errors="replace", timeout=3, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "pacman lookup unavailable"
    packages = ", ".join(line for line in result.stdout.splitlines() if line)
    return f"pacman: {packages}" if result.returncode == 0 and packages else "no pacman owner established"


@dataclass
class Directory:
    path: str
    size: int
    complete: bool


@dataclass
class Frame:
    path: str
    iterator: Iterator[os.DirEntry[str]]
    size: int
    complete: bool = True


class ScanTimeout(Exception):
    pass


class Inventory:
    def __init__(self, home: str, limit: int, file_limit: int, all_folders: bool):
        self.home = home
        self.limit = limit
        self.file_limit = file_limit
        self.all_folders = all_folders
        self.roots: list[Directory] = []
        self.home_files: list[tuple[int, str, int]] = []
        self.app_folders: list[tuple[int, str, bool]] = []
        self.directories: list[Directory] = []
        self.files: list[tuple[int, str, int]] = []
        self.issues: list[tuple[str, str]] = []
        self.issue_count = 0
        self.skipped_links: list[str] = []
        self.special_entries: list[tuple[str, str]] = []
        self.directory_count = 0

    def issue(self, path: str, reason: str) -> None:
        self.issue_count += 1
        if len(self.issues) < MAX_ISSUES:
            self.issues.append((path, reason))

    def relative(self, path: str) -> str:
        return os.path.relpath(path, self.home)

    def record_directory(self, frame: Frame, root: str) -> None:
        directory = Directory(frame.path, frame.size, frame.complete)
        self.directory_count += 1
        if frame.path == root:
            self.roots.append(directory)
        elif is_app_folder(self.relative(frame.path)):
            item = (frame.size, frame.path, frame.complete)
            if len(self.app_folders) < self.limit:
                heapq.heappush(self.app_folders, item)
            else:
                heapq.heappushpop(self.app_folders, item)
        if self.all_folders:
            self.directories.append(directory)

    def record_file(self, path: str, info: os.stat_result) -> None:
        item = (info.st_size, path, allocated(info))
        if len(self.files) < self.file_limit:
            heapq.heappush(self.files, item)
        else:
            heapq.heappushpop(self.files, item)

    def record_home_file(self, path: str, info: os.stat_result) -> None:
        self.home_files.append((allocated(info), path, info.st_size))
        self.record_file(path, info)

    def scan(self, root: str, root_info: os.stat_result, timeout: int) -> None:
        """One traversal per root; skip symlinks and different-device subtrees."""
        stack: list[Frame] = []
        hardlinks: set[tuple[int, int]] = set()
        root_device = root_info.st_dev

        def enter(path: str, info: os.stat_result) -> None:
            try:
                iterator = os.scandir(path)
            except OSError as exc:
                self.issue(path, f"cannot read directory: {exc.strerror or exc}")
                stack.append(Frame(path, iter(()), allocated(info), False))
                return
            stack.append(Frame(path, iterator, allocated(info)))

        def finish() -> None:
            frame = stack.pop()
            close = getattr(frame.iterator, "close", None)
            if close:
                close()
            self.record_directory(frame, root)
            if stack:
                stack[-1].size += frame.size
                stack[-1].complete = stack[-1].complete and frame.complete

        def alarm_handler(_signum: int, _frame: object) -> None:
            raise ScanTimeout()

        previous_handler = signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout)
        try:
            enter(root, root_info)
            while stack:
                frame = stack[-1]
                try:
                    entry = next(frame.iterator)
                except StopIteration:
                    finish()
                    continue
                except OSError as exc:
                    self.issue(frame.path, f"directory listing interrupted: {exc.strerror or exc}")
                    frame.complete = False
                    finish()
                    continue
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    self.issue(entry.path, f"cannot inspect entry: {exc.strerror or exc}")
                    frame.complete = False
                    continue
                if stat.S_ISLNK(info.st_mode):
                    frame.size += allocated(info)
                elif stat.S_ISDIR(info.st_mode):
                    if info.st_dev != root_device:
                        self.issue(entry.path, "nested filesystem skipped")
                        frame.complete = False
                    else:
                        enter(entry.path, info)
                else:
                    key = (info.st_dev, info.st_ino)
                    if stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
                        if key in hardlinks:
                            continue
                        hardlinks.add(key)
                    frame.size += allocated(info)
                    if stat.S_ISREG(info.st_mode):
                        self.record_file(entry.path, info)
        except ScanTimeout:
            self.issue(root, f"scan timed out after {timeout}s")
            while stack:
                stack[-1].complete = False
                finish()
            if not any(directory.path == root for directory in self.roots):
                self.record_directory(Frame(root, iter(()), allocated(root_info), False), root)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)

    def print_report(self, selected_folder: str | None = None, dotfiles_only: bool = False) -> None:
        print(f"PC-CLEAN HIDDEN HOME REPORT — {datetime.now().astimezone().isoformat(timespec='seconds')}")
        if selected_folder:
            print(f"Scope: selected hidden directory {display(os.path.join(self.home, selected_folder))} only")
        elif dotfiles_only:
            print(f"Scope: hidden files and other non-directory entries directly under {display(self.home)} only")
        else:
            print(f"Scope: hidden files and directories directly under {display(self.home)}, plus directory descendants")
        print("Symlinks are not followed; special files are not opened; different-device subtrees are skipped.")
        print("Directory sizes are allocated disk usage, may overlap, and can be partial; size alone is not cleanup advice.")
        print("Attribution is a path-based clue unless an exact file has a confirmed pacman owner.")
        if not dotfiles_only:
            print("\n## Hidden home directories (selected root)" if selected_folder else
                  "\n## Hidden home directories (all discovered roots)")
            if not self.roots:
                print("  (none scanned)")
            for record in sorted(self.roots, key=lambda item: (-item.size, item.path)):
                status = " [partial]" if not record.complete else ""
                print(f"  {human_size(record.size):>10}  {display(record.path)}{status} — {describe(self.relative(record.path))}")
        if not selected_folder:
            print("\n## Hidden home files (all discovered regular dotfiles; allocated size)")
            if not self.home_files:
                print("  (none found)")
            for size, path, logical in sorted(self.home_files, key=lambda item: (-item[0], item[1])):
                print(f"  {human_size(size):>10}  {display(path)} (logical {human_size(logical)}) — {describe(self.relative(path))}")
        if not dotfiles_only:
            print(f"\n## Largest application/data folders (up to {self.limit}; nested sizes overlap)")
            if not self.app_folders:
                print("  (none found)")
            for size, path, complete in sorted(self.app_folders, key=lambda item: (-item[0], item[1])):
                status = " [partial]" if not complete else ""
                print(f"  {human_size(size):>10}  {display(path)}{status} — {describe(self.relative(path))}")
        print(f"\n## Largest observed files (up to {self.file_limit}; logical size, then allocated)")
        if not self.files:
            print("  (none found)")
        for logical, path, disk in sorted(self.files, key=lambda item: (-item[0], item[1])):
            print(f"  {human_size(logical):>10}  {display(path)} (disk {human_size(disk)})")
            print(f"             {describe(self.relative(path))}; {pacman_owner(path)}")
        if self.all_folders:
            print("\n## Every observed directory (nested sizes overlap)")
            for record in sorted(self.directories, key=lambda item: (-item.size, item.path)):
                status = " [partial]" if not record.complete else ""
                print(f"  {human_size(record.size):>10}  {display(record.path)}{status} — {describe(self.relative(record.path))}")
        print("\n## Coverage and limitations")
        print(f"  {len(self.roots)} hidden root(s), {len(self.home_files)} home dotfile(s), {self.directory_count} directories observed; {self.issue_count} access/coverage issue(s).")
        for path in sorted(self.skipped_links):
            print(f"  NOT FOLLOWED (hidden home symlink): {display(path)}")
        for path, kind in sorted(self.special_entries):
            print(f"  NOT OPENED (hidden home {kind}): {display(path)}")
        for path, reason in self.issues:
            print(f"  INCOMPLETE: {display(path)} — {reason}")
        if self.issue_count > len(self.issues):
            print(f"  ... {self.issue_count - len(self.issues)} further issue(s) omitted from this summary.")
        if dotfiles_only:
            print("  Hidden directories and their contents were not scanned in dotfiles-only mode.")
        elif not self.all_folders:
            print("  Use --all-folders for every observed directory; that output can be very large.")
        print("  Sizes may differ on compressed, deduplicated, reflinked, or changing filesystems.")
        print("\nFindings require review. No changes were made.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only inventory of hidden files and folders in the current user's home.",
        epilog="Entries are not cleanup recommendations. Symlinks and different-device subtrees are not followed.",
    )
    parser.add_argument("--version", action="version", version=f"pc-clean scan {VERSION}")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--folder", type=hidden_name, help="scan only this hidden home directory, e.g. .cache")
    scope.add_argument("--dotfiles-only", action="store_true", help="report hidden home files only, without scanning directories")
    parser.add_argument("--all-folders", action="store_true", help="list every observed subdirectory (potentially very large)")
    parser.add_argument("--limit", type=positive_int, default=20, help="maximum application folders in summary (default: 20)")
    parser.add_argument("--files", type=positive_int, default=10, help="maximum largest files in summary (default: 10)")
    parser.add_argument("--timeout", type=positive_int, default=120, help="per-hidden-folder timeout in seconds (default: 120)")
    args = parser.parse_args(argv)
    if args.dotfiles_only and args.all_folders:
        parser.error("--dotfiles-only cannot be combined with --all-folders")

    home = os.path.abspath(os.path.expanduser("~"))
    resolved_home = os.path.realpath(home)
    protected = ("/root", "/boot", "/efi", "/proc", "/sys", "/dev", "/run", "/tmp", "/usr/lib/modules", "/usr/src/linux")
    if resolved_home == "/" or any(resolved_home == path or resolved_home.startswith(path + os.sep) for path in protected):
        print("pc-clean: refusing to scan a protected home directory", file=sys.stderr)
        return 2
    inventory = Inventory(home, args.limit, args.files, args.all_folders)
    try:
        with os.scandir(home) as entries:
            for entry in entries:
                if not entry.name.startswith(".") or (args.folder and entry.name != args.folder):
                    continue
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    inventory.issue(entry.path, f"cannot inspect hidden entry: {exc.strerror or exc}")
                    continue
                if stat.S_ISLNK(info.st_mode):
                    inventory.skipped_links.append(entry.path)
                elif stat.S_ISDIR(info.st_mode):
                    if not args.dotfiles_only:
                        inventory.scan(entry.path, info, args.timeout)
                elif not args.folder and stat.S_ISREG(info.st_mode):
                    inventory.record_home_file(entry.path, info)
                elif not args.folder:
                    kind = ("socket" if stat.S_ISSOCK(info.st_mode) else
                            "FIFO" if stat.S_ISFIFO(info.st_mode) else
                            "device" if stat.S_ISCHR(info.st_mode) or stat.S_ISBLK(info.st_mode) else
                            "special file")
                    inventory.special_entries.append((entry.path, kind))
    except OSError as exc:
        print(f"pc-clean: cannot read home {display(home)}: {exc.strerror or exc}", file=sys.stderr)
        return 1
    if args.folder and not inventory.roots and not inventory.skipped_links and not inventory.issue_count:
        print(f"pc-clean: hidden directory not found: {display(args.folder)}", file=sys.stderr)
        return 2
    inventory.print_report(args.folder, args.dotfiles_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
