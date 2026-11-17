"""In-memory tests: no temporary files or real system traversal."""

import argparse
import contextlib
import importlib.util
import io
import os
import stat
import types
import unittest
from unittest import mock


SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "scan.py")
SPEC = importlib.util.spec_from_file_location("pc_clean_scan", SCRIPT)
scan = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = scan
SPEC.loader.exec_module(scan)


def info(kind, *, size=0, blocks=1, dev=1, inode=1, links=1):
    return types.SimpleNamespace(st_mode=kind, st_size=size, st_blocks=blocks,
                                 st_dev=dev, st_ino=inode, st_nlink=links)


class Entry:
    def __init__(self, path, data):
        self.path = path
        self.name = os.path.basename(path)
        self.data = data

    def stat(self, *, follow_symlinks):
        assert not follow_symlinks
        if isinstance(self.data, OSError):
            raise self.data
        return self.data


class Entries:
    def __init__(self, entries):
        self.entries = iter(entries)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.entries)

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()

    def close(self):
        pass


class ScannerTests(unittest.TestCase):
    def test_attribution_and_filename_safety(self):
        self.assertIn("KDE Baloo", scan.describe(os.path.join(".local", "share", "baloo", "index")))
        self.assertIn("Firefox", scan.describe(os.path.join(".config", "Firefox", "profiles")))
        self.assertIn("preserve", scan.describe(os.path.join(".ssh", "id_ed25519")))
        self.assertIn("name clue only", scan.describe(os.path.join(".unknown", "file")))
        self.assertIn("Bash startup", scan.describe(".bashrc"))
        self.assertIn("sensitive", scan.describe(".bash_history"))
        self.assertNotIn("\n", scan.display("/home/me/.config/line\nname"))

    def test_validation_and_exact_package_owner(self):
        for name in ("..", ".", ".cache/../../etc", ".cache\\..\\..\\etc"):
            with self.assertRaises(argparse.ArgumentTypeError):
                scan.hidden_name(name)
        for name in (".cache", "AppData"):
            self.assertEqual(scan.hidden_name(name), name)
        if scan.IS_WINDOWS:
            with mock.patch.object(scan, "windows_installed_programs",
                                   return_value=[("Example App", r"C:\Apps\Example")]):
                self.assertEqual(scan.package_owner(r"C:\Apps\Example\bin\app.exe"),
                                 "registry install location: Example App")
            self.assertEqual(scan.package_owner(r"C:\Elsewhere\file.txt"),
                             "no per-file owner available on Windows")
        with mock.patch.object(scan.shutil, "which", return_value="/usr/bin/pacman"), \
             mock.patch.object(scan.subprocess, "run", return_value=types.SimpleNamespace(returncode=0, stdout="example\n")) as run:
            self.assertEqual(scan.pacman_owner("/home/me/.local/a"), "pacman: example")
            self.assertEqual(run.call_args.args[0], ["pacman", "-Qqo", "--", "/home/me/.local/a"])
        with mock.patch.object(scan.shutil, "which", return_value=None):
            self.assertEqual(scan.pacman_owner("/home/me/.local/a"), "pacman unavailable")

    def test_allocated_prefers_reported_blocks(self):
        sparse = info(stat.S_IFREG, size=10_000, blocks=0)
        self.assertEqual(scan.allocated(sparse), 0)
        normal = info(stat.S_IFREG, size=10_000, blocks=8)
        self.assertEqual(scan.allocated(normal), 4096)
        no_blocks = types.SimpleNamespace(st_mode=stat.S_IFREG, st_size=10_000)
        self.assertEqual(scan.allocated(no_blocks), 10_000)

    def test_hidden_detection(self):
        self.assertTrue(scan.is_hidden(".cache", info(stat.S_IFDIR)))
        self.assertFalse(scan.is_hidden("projects", info(stat.S_IFDIR)))
        hidden_dir = info(stat.S_IFDIR)
        hidden_dir.st_file_attributes = getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 2)
        self.assertTrue(scan.is_hidden("IntelGraphicsProfiles", hidden_dir))
        if scan.IS_WINDOWS:
            self.assertTrue(scan.is_hidden("AppData", info(stat.S_IFDIR)))
        else:
            self.assertFalse(scan.is_hidden("AppData", info(stat.S_IFDIR)))
        self.assertFalse(scan.is_link_like(info(stat.S_IFDIR)))
        self.assertTrue(scan.is_link_like(info(stat.S_IFLNK)))

    def test_walk_skips_symlinks_mounts_and_deduplicates_hardlinks(self):
        home = "/home/me"
        root = home + "/.cache"
        app = root + "/app"
        denied = root + "/denied"
        mount = root + "/mount"
        link = root + "/outside-link"
        file_info = info(stat.S_IFREG, size=9000, blocks=8, inode=44, links=2)
        tree = {
            root: [Entry(app, info(stat.S_IFDIR, inode=2)),
                   Entry(denied, info(stat.S_IFDIR, inode=3)),
                   Entry(mount, info(stat.S_IFDIR, dev=2, inode=4)),
                   Entry(link, info(stat.S_IFLNK, blocks=0, inode=5))],
            app: [Entry(app + "/file", file_info), Entry(app + "/hardlink", file_info)],
        }
        visited = []

        def fake_scandir(path):
            visited.append(path)
            if path == denied:
                raise PermissionError(13, "Permission denied", path)
            return Entries(tree[path])

        inventory = scan.Inventory(home, limit=20, file_limit=10, all_folders=True)
        with mock.patch.object(scan.os, "scandir", side_effect=fake_scandir):
            inventory.scan(root, info(stat.S_IFDIR, inode=1), 5)
        self.assertEqual(visited, [root, app, denied])
        self.assertEqual(len(inventory.files), 1)
        self.assertEqual(inventory.issue_count, 2)
        self.assertFalse(inventory.roots[0].complete)
        self.assertEqual(inventory.directory_count, 3)
        self.assertEqual(inventory.roots[0].size, (1 + 1 + 8 + 1) * 512)
        self.assertTrue(any(path == denied for path, _ in inventory.issues))
        self.assertTrue(any(path == mount for path, _ in inventory.issues))

    def test_timeout_marks_partial(self):
        class TimeoutEntries(Entries):
            def __next__(self):
                raise scan.ScanTimeout()

        inventory = scan.Inventory("/home/me", 20, 10, True)
        with mock.patch.object(scan.os, "scandir", return_value=TimeoutEntries([])):
            inventory.scan("/home/me/.cache", info(stat.S_IFDIR), 5)
        self.assertFalse(inventory.roots[0].complete)
        self.assertIn("timed out", inventory.issues[0][1])

    def test_timeout_before_open_still_lists_partial_root(self):
        inventory = scan.Inventory("/home/me", 20, 10, True)
        with mock.patch.object(scan.os, "scandir", side_effect=scan.ScanTimeout):
            inventory.scan("/home/me/.cache", info(stat.S_IFDIR), 5)
        self.assertEqual(inventory.directory_count, 1)
        self.assertFalse(inventory.roots[0].complete)
        self.assertIn("timed out", inventory.issues[0][1])

    def test_main_includes_dotfiles_and_hidden_directories(self):
        home = "/home/me"
        entries = [Entry(home + "/.cache", info(stat.S_IFDIR)),
                   Entry(home + "/.config", info(stat.S_IFDIR)),
                   Entry(home + "/.bashrc", info(stat.S_IFREG, size=42)),
                   Entry(home + "/.linked", info(stat.S_IFLNK)),
                   Entry(home + "/.socket", info(stat.S_IFSOCK)),
                   Entry(home + "/projects", info(stat.S_IFDIR))]
        seen = []

        def fake_scan(instance, root, _info, _timeout):
            seen.append(root)
            instance.roots.append(scan.Directory(root, 512, True))

        output = io.StringIO()
        with mock.patch.object(scan.os.path, "expanduser", return_value=home), \
             mock.patch.object(scan.os.path, "realpath", return_value=home), \
             mock.patch.object(scan.os, "scandir", side_effect=lambda _: Entries(entries)), \
             mock.patch.object(scan.Inventory, "scan", new=fake_scan), \
             mock.patch.object(scan, "package_owner", return_value="no package owner established"), \
             contextlib.redirect_stdout(output):
            self.assertEqual(scan.main([]), 0)
        self.assertEqual(seen, [home + "/.cache", home + "/.config"])
        self.assertIn("NOT FOLLOWED (hidden home link/reparse point): /home/me/.linked", output.getvalue())
        self.assertIn("NOT OPENED (hidden home socket): /home/me/.socket", output.getvalue())
        self.assertNotIn(home + "/projects", output.getvalue())
        self.assertIn(home + "/.bashrc", output.getvalue())
        self.assertIn("Bash startup settings", output.getvalue())
        self.assertIn("1 home hidden file(s)", output.getvalue())
        self.assertIn("No changes were made.", output.getvalue())

    def test_dotfiles_are_included_in_largest_files(self):
        inventory = scan.Inventory("/home/me", 20, 1, False)
        inventory.record_file("/home/me/.cache/small", info(stat.S_IFREG, size=1))
        inventory.record_home_file("/home/me/.bash_history", info(stat.S_IFREG, size=9999))
        self.assertEqual(inventory.files[0][1], "/home/me/.bash_history")
        self.assertEqual(inventory.home_files[0][1], "/home/me/.bash_history")

    def test_dotfiles_only_does_not_scan_any_directory(self):
        home = "/home/me"
        entries = [Entry(home + "/.cache", info(stat.S_IFDIR)),
                   Entry(home + "/.bashrc", info(stat.S_IFREG, size=42)),
                   Entry(home + "/.linked", info(stat.S_IFLNK)),
                   Entry(home + "/notes", info(stat.S_IFREG, size=100))]
        output = io.StringIO()
        with mock.patch.object(scan.os.path, "expanduser", return_value=home), \
             mock.patch.object(scan.os.path, "realpath", return_value=home), \
             mock.patch.object(scan.os, "scandir", side_effect=lambda _: Entries(entries)), \
             mock.patch.object(scan.Inventory, "scan") as scan_directory, \
             mock.patch.object(scan, "package_owner", return_value="no package owner established"), \
             contextlib.redirect_stdout(output):
            self.assertEqual(scan.main(["--dotfiles-only"]), 0)
        scan_directory.assert_not_called()
        self.assertIn(home + "/.bashrc", output.getvalue())
        self.assertIn(home + "/.linked", output.getvalue())
        self.assertNotIn(home + "/.cache", output.getvalue())
        self.assertNotIn(home + "/notes", output.getvalue())
        self.assertIn("Hidden directories and their contents were not scanned", output.getvalue())

    def test_dotfiles_only_rejects_incompatible_options(self):
        for args in (["--dotfiles-only", "--all-folders"],
                     ["--dotfiles-only", "--folder", ".cache"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as result:
                scan.main(args)
            self.assertEqual(result.exception.code, 2)

    def test_main_folder_option_is_focused_and_labeled(self):
        home = "/home/me"
        entries = [Entry(home + "/.cache", info(stat.S_IFDIR)),
                   Entry(home + "/.config", info(stat.S_IFDIR)),
                   Entry(home + "/.bashrc", info(stat.S_IFREG))]
        seen = []

        def fake_scan(instance, root, _info, _timeout):
            seen.append(root)
            instance.roots.append(scan.Directory(root, 512, True))

        output = io.StringIO()
        with mock.patch.object(scan.os.path, "expanduser", return_value=home), \
             mock.patch.object(scan.os.path, "realpath", return_value=home), \
             mock.patch.object(scan.os, "scandir", side_effect=lambda _: Entries(entries)), \
             mock.patch.object(scan.Inventory, "scan", new=fake_scan), \
             contextlib.redirect_stdout(output):
            self.assertEqual(scan.main(["--folder", ".cache"]), 0)
        self.assertEqual(seen, [home + "/.cache"])
        self.assertIn("selected hidden directory", output.getvalue())
        self.assertIn(".cache only", output.getvalue())
        self.assertNotIn(home + "/.config", output.getvalue())
        self.assertNotIn(home + "/.bashrc", output.getvalue())

    def test_visible_folder_is_reported_as_not_hidden(self):
        home = "/home/me"
        entries = [Entry(home + "/Documents", info(stat.S_IFDIR)),
                   Entry(home + "/.cache", info(stat.S_IFDIR))]
        error = io.StringIO()
        with mock.patch.object(scan.os.path, "expanduser", return_value=home), \
             mock.patch.object(scan.os.path, "realpath", return_value=home), \
             mock.patch.object(scan.os, "scandir", side_effect=lambda _: Entries(entries)), \
             mock.patch.object(scan.Inventory, "scan") as scan_directory, \
             contextlib.redirect_stderr(error):
            self.assertEqual(scan.main(["--folder", "Documents"]), 2)
        scan_directory.assert_not_called()
        self.assertIn("exists but is not a hidden entry", error.getvalue())

    def test_protected_home_is_refused(self):
        protected_home = os.environ.get("SystemRoot") or r"C:\Windows" if scan.IS_WINDOWS else "/root"
        with mock.patch.object(scan.os.path, "expanduser", return_value=protected_home), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(scan.main([]), 2)


if __name__ == "__main__":
    unittest.main()
