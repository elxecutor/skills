---
name: pc-clean
description: Inspect hidden home files and folders, attribute storage to likely applications or exact package owners, and report cautious cleanup candidates without making changes. Use for hidden application data, caches, installed tools, or reclaiming home-directory space.
---

# PC Clean — hidden home files and folders (report-only)

> ## Primary directive
> This skill **only investigates and reports**. Never run a destructive or
> state-changing command, including `rm`, `pacman -R`, `pacman -D`, `pkexec`,
> cache-cleaning commands, or venv migration commands—even if the user asks it
> to execute a recommendation. The user runs any chosen command in their own
> terminal. Every report ends with: **“No changes were made.”**

The goal is to explain what takes space in the user's hidden home files and folders,
what software or project it may belong to, and what deserves review. Size alone
never proves something is unwanted or safe to remove.

## Scope and safety

1. Scan hidden **files and directories directly under the current user's
   home**, such as `~/.bashrc`, `~/.cache`, `~/.config`, `~/.local`, `~/.npm`,
   and other `~/.*` entries, plus readable descendants of actual directories.
   Report hidden symlinks and special files without following or opening them.
   Normal home entries, other users, system trees and package-wide inventories
   are outside scope.
2. Do not follow symlinks, cross a different-device filesystem boundary, inspect protected
   system paths, elevate privileges, read file contents or configuration
   values, or create files. Hidden home symlinks are listed as not followed.
   A home directory resolving to a protected path is refused.
3. The report shows all discovered top-level hidden directories and regular
   dotfiles, followed by the largest
   application/data folders and largest files, followed by coverage gaps.
   Default output is compact; only request the potentially enormous complete
   directory listing when specifically useful. Inaccessible or timed-out
   folders have partial sizes, not zero-size or clean status. Treat shell
   histories, credentials and other dotfiles as sensitive data, never cache.
4. Attribution from a path is a **possible** owner or purpose, not proof that
   software is installed or unused. `pacman -Qqo` checks the exact displayed
   file against the local package database; failure is not evidence that the
   file is unwanted. Never imply that a package owns a whole folder because it
   owns one file.
5. Preserve configuration, browser profiles, credentials, SSH/GPG keys,
   application data, games, saves and virtual environments. Treat caches as
   review candidates only: identify the specific app, explain rebuilding or
   redownload costs, and close the app before any user-directed browser-cache
   maintenance. Never target a browser profile in `~/.config` as cache.
6. Never consolidate, copy or symlink virtual environments between projects.
   Treat each environment as project/interpreter-specific and report its size
   only. If package advice is explicitly requested, never suggest bulk
   `pacman -Rns`; check `Required By`, `Optional For`, installed kernels and
   headers, and the package-removal preview before any user decision.
7. Journals, coredumps and package caches are diagnostic/recoverability data,
   not junk. This skill does not scan their system locations.

## Running the scanner

The scanner needs Python 3 and uses only its standard library. It reads
filesystem metadata, not file contents, and queries the local pacman database
only for exact ownership of displayed large files. No data is deleted or
modified by the scanner.

```bash
# All hidden files and actual hidden directories under the user's home.
bash ~/.agents/skills/pc-clean/scripts/scan.sh

# Investigate one hidden directory without scanning the others.
bash ~/.agents/skills/pc-clean/scripts/scan.sh --folder .cache

# Inspect home-root dotfiles without traversing hidden directories.
bash ~/.agents/skills/pc-clean/scripts/scan.sh --dotfiles-only

# Optional exhaustive directory listing; can be very large.
bash ~/.agents/skills/pc-clean/scripts/scan.sh --all-folders
```

`--limit N` controls the number of application/data folders in the summary
(default 20), `--files N` controls largest files (default 10), and `--timeout N`
sets the per-hidden-root deadline in seconds (default 120). `--help` and
`--version` are available. `--dotfiles-only` cannot be combined with `--folder`
or `--all-folders`. An inaccessible directory, skipped different-device
subtree, or timeout is reported as an incomplete result. Same-device bind mounts
cannot be reliably identified by a device boundary alone. Directory sizes
are allocated bytes; largest files are ranked by logical bytes with allocated
bytes also shown. Hardlinks are counted once per hidden root. Folder sizes
overlap and should not be added together; compression, reflinks and concurrent
changes can also make estimates differ from actual unique disk use.

The user has specifically asked not to flood the conversation with scan output.
Do not paste a full tree into chat. Summarize the largest useful attributed
items and access gaps; use `--folder` for a focused follow-up. The full listing
is opt-in and can contain sensitive path names.

## Presenting findings

Present a concise table with item/path, size, likely owner and evidence,
classification or risk, and what to verify. Distinguish a pacman-confirmed
**file** owner from a path-based guess. Say clearly that results only cover
hidden home entries and can be partial. If a user independently chooses
maintenance, provide a narrowly scoped informational reference only after
explaining its trade-off; never perform it on their behalf.

Read-only references for the user:

```bash
du -sh -- "$HOME/.cache/<specific-app>"
pacman -Qqo -- "$HOME/<specific-hidden-path>/<file>"
```

End every report with: **No changes were made.**
