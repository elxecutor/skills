---
name: pc-clean
description: Inspect hidden home files and folders, attribute storage to likely applications or exact package owners, and report cautious cleanup candidates without making changes. Use for hidden application data, caches, installed tools, or reclaiming home-directory space on Windows, Linux, or macOS.
---

# PC Clean — hidden home files and folders (report-only)

> ## Primary directive
> This skill **only investigates and reports**. Never run a destructive or
> state-changing command, including `rm`, `pacman -R`, `pacman -D`, `pkexec`,
> `Remove-Item`, `del`, `rd`, `rmdir`, `Clear-RecycleBin`, `winget uninstall`,
> disk-cleanup or cache-cleaning commands, or venv migration commands—even if
> the user asks it to execute a recommendation. The user runs any chosen
> command in their own terminal. Every report ends with:
> **“No changes were made.”**

The goal is to explain what takes space in the user's hidden home files and folders,
what software or project it may belong to, and what deserves review. Size alone
never proves something is unwanted or safe to remove.

## Scope and safety

1. Scan hidden **files and directories directly under the current user's
   home**, plus readable descendants of actual directories. What counts as
   hidden depends on the OS:
   - Everywhere: names that start with a dot, such as `.cache`, `.config`,
     `.ssh`, `.npm`, `.bashrc`, `.gitconfig`.
   - Windows also: entries carrying the hidden file attribute (`NTUSER.DAT`,
     `IntelGraphicsProfiles`, and normally `AppData`) and the shell-hidden
     user folders Explorer suppresses regardless of the attribute (`AppData`,
     `Application Data`, `Local Settings`, `Cookies`, `NetHood`, `PrintHood`,
     `Recent`, `SendTo`, `Start Menu`, `Templates`, `My Documents`).
   - Normal visible home entries (`Documents`, `Downloads`, `projects`), other
     users, system trees and package-wide inventories are outside scope.
2. Do not follow symlinks, junctions or other reparse points, cross a
   different-device filesystem boundary, inspect protected system paths,
   elevate privileges, read file contents or configuration values, or create
   files. Hidden home links are listed as not followed. A home directory
   resolving to a protected path (a drive root, `C:\Windows`, `Program Files`,
   `ProgramData`, `/root`, `/proc`, ...) is refused.
3. The report shows all discovered top-level hidden directories and hidden
   home files, followed by the largest application/data folders and largest
   files, followed by coverage gaps. Default output is compact; only request
   the potentially enormous complete directory listing when specifically
   useful. Inaccessible or timed-out folders have partial sizes, not zero-size
   or clean status. Treat shell histories, credentials and other hidden
   dotfiles as sensitive data, never cache.
4. Attribution from a path is a **possible** owner or purpose, not proof that
   software is installed or unused.
   - On Arch Linux, `pacman -Qqo` checks the exact displayed file against the
     local package database; failure is not evidence that the file is
     unwanted.
   - On Windows there is no per-file package database. The scanner matches the
     file against registry uninstall entries that publish an `InstallLocation`
     and labels the result as a registry install-location match, not an exact
     owner. Files outside every known install location report **no per-file
     owner available on Windows**.
   - Never imply that a package owns a whole folder because it owns one file.
5. Preserve configuration, browser profiles, credentials, SSH/GPG keys,
   application data, games, saves and virtual environments. Treat caches as
   review candidates only: identify the specific app, explain rebuilding or
   redownload costs, and close the app before any user-directed browser-cache
   maintenance. Never target a browser profile (`Chrome\User Data`,
   `AppData\Roaming\Mozilla`, `.config/<browser>`) as cache.
6. Never consolidate, copy or symlink virtual environments between projects.
   Treat each environment as project/interpreter-specific and report its size
   only. If package advice is explicitly requested, never suggest bulk removal
   (`pacman -Rns`, `winget uninstall --all`); check `Required By`,
   `Optional For`, installed kernels and headers, or the app's dependencies
   before any user decision.
7. Journals, coredumps, crash dumps, shadow copies, Recycle Bin contents and
   package caches are diagnostic/recoverability data, not junk. This skill does
   not scan their system locations.

## Running the scanner

The scanner needs Python 3.9+ and uses only its standard library. It reads
filesystem metadata, not file contents, and queries only local ownership data
(the pacman database on Arch, uninstall registry keys on Windows) for the exact
displayed large files. No data is deleted or modified by the scanner.

Windows (PowerShell):

```powershell
# All hidden files and hidden directories under the user's home.
powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME\.agents\skills\pc-clean\scripts\scan.ps1"

# Investigate one hidden directory without scanning the others.
powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME\.agents\skills\pc-clean\scripts\scan.ps1" --folder AppData

# Inspect home-root hidden files without traversing hidden directories.
powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME\.agents\skills\pc-clean\scripts\scan.ps1" --dotfiles-only

# Optional exhaustive directory listing; can be very large.
powershell -NoProfile -ExecutionPolicy Bypass -File "$HOME\.agents\skills\pc-clean\scripts\scan.ps1" --all-folders
```

Linux and macOS:

```bash
# All hidden files and actual hidden directories under the user's home.
bash ~/.agents/skills/pc-clean/scripts/scan.sh

# Investigate one hidden directory without scanning the others.
bash ~/.agents/skills/pc-clean/scripts/scan.sh --folder .cache

# Inspect home-root hidden files without traversing hidden directories.
bash ~/.agents/skills/pc-clean/scripts/scan.sh --dotfiles-only

# Optional exhaustive directory listing; can be very large.
bash ~/.agents/skills/pc-clean/scripts/scan.sh --all-folders
```

`scan.py` is the single implementation for both operating systems and branches
on the current platform internally; the `.ps1` and `.sh` files only locate
Python and forward arguments.

`--limit N` controls the number of application/data folders in the summary
(default 20), `--files N` controls largest files (default 10), and `--timeout N`
sets the per-hidden-root deadline in seconds (default 120). `--help` and
`--version` are available. `--dotfiles-only` cannot be combined with `--folder`
or `--all-folders`. An inaccessible directory, skipped different-device
subtree, or timeout is reported as an incomplete result. Directory sizes
are allocated bytes where the OS reports them (Windows falls back to logical
size); largest files are ranked by logical bytes with allocated bytes also
shown. Hardlinks are counted once per hidden root. Folder sizes overlap and
should not be added together; compression, reflinks and concurrent changes can
also make estimates differ from actual unique disk use.

The user has specifically asked not to flood the conversation with scan output.
Do not paste a full tree into chat. Summarize the largest useful attributed
items and access gaps; use `--folder` for a focused follow-up. The full listing
is opt-in and can contain sensitive path names.

## Presenting findings

Present a concise table with item/path, size, likely owner and evidence,
classification or risk, and what to verify. Distinguish a confirmed package
**file** owner (pacman on Arch, registry install location on Windows) from a
path-based guess. Say clearly that results only cover hidden home entries and
can be partial. If a user independently chooses maintenance, provide a narrowly
scoped informational reference only after explaining its trade-off; never
perform it on their behalf.

Read-only references for the user:

```bash
# Linux/macOS
du -sh -- "$HOME/.cache/<specific-app>"
pacman -Qqo -- "$HOME/<specific-hidden-path>/<file>"
```

```powershell
# Windows (read-only size lookup)
Get-ChildItem -LiteralPath "$HOME\AppData\Local\<specific-app>" -Recurse -Force -File |
  Measure-Object -Property Length -Sum
```

End every report with: **No changes were made.**
