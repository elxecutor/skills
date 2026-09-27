---
name: pc-clean
description: Investigates and reports system bloat on Arch Linux — ghost files (dead .desktop launchers, broken symlinks, unowned config), orphaned/bloated packages, wasteful caches, and redundant Python venvs / node_modules. ADVISORY ONLY — it never executes removals; it reports findings and outputs the exact commands for the user to run. Use when the user says "clean my pc", "find bloat", "remove ghost files", "free up disk space", or wants a repeatable cleanup routine.
---

# PC Clean — Arch Linux bloat investigation (ADVISORY ONLY)

> ## ⛔ PRIMARY DIRECTIVE
> **This skill NEVER executes destructive commands.** It investigates, reports,
> and prints the exact commands the user can run. The agent presents the report
> and **stops**. The user issues the execute order (e.g. "run 3b and 3f").
> The agent must not run `pacman -R`, `rm`, `pkexec`, cache clears, or venv
> merges on its own initiative.

A repeatable, safety-first workflow to reclaim disk space on Arch Linux (any DE).
Built from hard-won lessons: a careless `pacman -Rns` once removed the display
manager and X server. This skill is **recon-first, user-decides-everything**.

All paths use `$HOME` / environment variables — nothing is hardcoded to a user.

## When to use

- "clean my pc" / "free up space" / "find bloat"
- "remove ghost files" / "there are dead launchers"
- Periodic maintenance pass

## HARD SAFETY RULES (do not violate)

1. **Recon is read-only. Never delete in Phase 1.**
2. **`pacman -R` (not `-Rns`) for explicit removals.** `-s` (remove deps no longer
   needed) cascades and can rip out the display manager, X server, network applet,
   polkit agent, etc. If you remove orphans, do it ONE package at a time with `-R`
   and read the dependency preview pacman prints.
3. **Never remove `linux-headers` for the CURRENT kernel.** Check
   `pacman -Q linux linux-headers` — if versions match, it's the current kernel's
   headers. Keep it. (Old kernels' headers are safe to drop; most boxes have one kernel.)
4. **Before removing any package, verify nothing needs it:**
   `pacman -Qi <pkg> | grep -E "^Required By\s*:\s*\S"` — if this prints any
   package names, do NOT remove. Also check `Optional For:`.
5. **Browser cache ≠ credentials.** `~/.cache/<browser>/` is safe to clear.
   Cookies, passwords, bookmarks live in `~/.config/<browser>/` — never touch that.
6. **Keep backups.** When migrating/replacing, rename to `.old`; don't delete outright
   until the user confirms the new setup works.
7. **Use `pkexec`, never `sudo`, for elevated commands.**
8. **Confirm every destructive action with the user before running it.**

## Phase 1 — Recon (read-only, no changes)

Run `bash ~/.agents/skills/pc-clean/scripts/scan.sh` for an automated report.
The output covers all sections below in one pass. The output sections map to:

| scan.sh section | What it finds |
|---|---|
| `## 1. GHOST .desktop LAUNCHERS` | `~/.local/share/applications/` launchers pointing to missing binaries |
| `## 2. BROKEN SYMLINKS` | Broken symlinks under `/opt` and `$HOME/.local` |
| `## 4. ORPHAN PACKAGES` | Packages installed as deps, no longer needed by anything |
| `## 5. CURRENT KERNEL HEADERS` | `linux` vs `linux-headers` version match |
| `## 6. TOP PACKAGES BY SIZE` | Installed packages sorted by size (MiB) |
| `## 7. CACHE SIZES` | per-tool cache sizes (npm, bun, pip, AUR, Go, Cargo, etc.) |
| `## 8. SYSTEM /var BLOAT` | coredumps, pacman cache, journal, libvirt images |
| `## 9. TOP-LEVEL $HOME ENTRIES` | hidden dir sizes under `$HOME` |
| `## 10. LARGE FILES IN HIDDEN DIRS` | files >500M inside hidden dirs |
| `## 11. REDUNDANT PYTHON VENVS` | per-project `.venv`/`venv` sizes (if `$PROJECTS` set) |
| `## 12. node_modules DIRS` | node_modules sizes (if `$PROJECTS` set) |
| `## 13. UNMANAGED /opt INSTALLS` | directories in `/opt` not owned by any package |

XDG user dirs (Desktop, Documents, Downloads, Music, Pictures, Public, Templates,
Videos), `/boot`, `/etc`, `/usr`, and `/lib/modules` are never scanned.

### Notes on specific sections

**1a. Ghost files — false positives to ignore:**
user-local `.desktop` files in `~/.local/share/applications/` that reference
binaries in non-PATH libexec dirs (e.g. pipx-installed apps). Verify with
`command -v <binary>`.

**1b. Orphans:**
A package showing as orphan may still be wanted (e.g. a screenshot tool you use
daily). Mark it explicit: `pacman -D --asexplicit <pkg>` (no root).

**1c. Bloated packages — typical candidates:**
| Package class | Usually safe? | Check first |
|---|---|---|
| `*-wallpapers` / `plasma-workspace-wallpapers` | yes | n/a |
| `noto-fonts-cjk` | if no CJK content | grep your docs for CJK |
| `clang` | if you only use gcc | confirm no clang/compile_commands.json usage |
| `deno` | if unused | no Deno projects/cache |
| `gradle` | if no Java builds | Android/Java builds often use their own wrapper |
| `guile` / scheme interpreters | rarely | `pacman -Qi guile \| grep Required` |
| `opencv` | if unused | no `cv2`/`cv::` in your code |
| `exploitdb` | if you host your own | you may keep a local exploit repo |
| GNOME cruft on KDE (`cheese clutter* cogl`) | yes | GNOME apps on a KDE box |
| `linux-headers` | **KEEP if matches current kernel** | see rule 3 |

**1d. System-level /var (biggest safe wins):**
`/var/lib/systemd/coredump`, `/var/cache/pacman/pkg`, `/var/log/journal` are
pure junk / cache — safe to clear. `/var/lib/libvirt/images` is user VM data —
report only, never auto-delete.

**1e. Caches:**
Browser cache in `~/.cache/<browser>/` is safe to clear — cookies, passwords,
bookmarks live in `~/.config/<browser>/` and are never touched.

**1f. Tool-install / dev-toolchain dirs (LIVE installs — report only):**
| Dir | What it is |
|---|---|
| `~/.local/share/opencode/opencode.db` | opencode session history DB (can be huge) |
| `~/.bun/install/global` | bun global packages |
| `~/.apio` | FPGA toolchain (oss-cad-suite / Yosys) |
| `~/.platformio` | embedded/Arduino toolchains |
| `~/.gradle/caches` | Gradle build cache (regenerates) |
| `~/.cache/dotslash` | dotslash-fetched tool binaries (regenerates) |
| a plugin dir's `node_modules` | plugin deps (regenerate on rebuild) |

**1g. Venvs & node_modules scope:**
Set `$PROJECTS` to your code directory (outside XDG dirs) to have scan.sh scan
for redundant Python venvs and node_modules. Default: not set (skipped).

## Phase 2 — Produce the report (STOP here)

Present a table: item, size, why it's safe/unsafe, and the **exact command**
the user would run. Do NOT run anything. Ask the user which items they want
executed. Specifically flag anything `pacman -R` would cascade into (show the
dependency preview) so they can decide.

## Phase 3 — Recommended commands (FOR THE USER TO RUN)

These are reference commands. The agent prints them; it does **not** execute them.
The user copies/runs them, or tells the agent "run 3b and 3f".

### 3a. Mark wanted orphans explicit (no root)
```bash
pacman -D --asexplicit <pkg>
```

### 3b. Remove explicit packages — SAFE FORM (no `-s`)
```bash
pkexec pacman -R --noconfirm <pkg1> <pkg2> ...
# If pacman errors "breaks dependency 'X' required by Y" -> that package is NEEDED. Stop, keep it.
```

### 3c. Remove orphans — ONE AT A TIME, watch the preview
```bash
# Safer than -Rns: removes just the named orphan, leaves its deps.
pkexec pacman -R --noconfirm <orphan>
# If the dependency preview lists the display manager / X server / network applet /
# polkit agent, CANCEL and reinstall those instead (they got swept in as deps).
```

### 3d. Ghost files (user-local only)
```bash
rm -f ~/.local/share/applications/DEAD.desktop   # user-local launcher
rm -f ~/.config/STALE.rc                         # user-owned config
```

### 3e. Manual/unmanaged installs
```bash
for d in /opt/*/; do pacman -Qo "$d" 2>&1 | grep -q error && echo "UNMANAGED: $d"; done
```
Remove only if the package-manager equivalent is what you actually use (e.g. the
distro package vs a manual `/opt/<app>-launcher-*`). Verify which one runs with
`which <app>` before deleting the manual copy.

### 3f. Caches (no root unless noted)
```bash
npm cache clean --force
rm -rf ~/.npm/_npx
uv cache clean
rm -rf ~/.cache/go-build
rm -rf ~/.cache/dotslash/*
rm -rf ~/.cache/<browser>/*     # SAFE — cookies/keys in ~/.config untouched
pip cache purge
```

> **Root-owned files inside user caches:** some tools (e.g. things launched via a
> root-run helper) leave root-owned files under `~/.cache`. A plain `rm` then fails
> with "Permission denied" for those paths. Re-run just the failed removals with
> `pkexec rm -rf <path>`. Per the user's rule, use `pkexec`, never `sudo`.

> **In-progress cache dirs:** before clearing `~/.bun/install/cache`, check nothing
> is actively installing (`pgrep -a bun`). A live `bun install` uses a `.tmp/`
> subdir that can be multiple GB; if the install already exited it may leave that
> `.tmp` orphaned — safe to `rm -rf` once no bun process is running.

### 3g. System-level /var cleanup (needs pkexec)
```bash
# systemd coredumps
pkexec coredumpctl delete
# pacman cache: keep latest 3 of installed + drop all of uninstalled
pkexec sh -c 'paccache -rk3; paccache -ruk0'
# journal: cap to a size (or use --vacuum-time=2weeks)
pkexec journalctl --vacuum-size=200M
```
Do NOT touch `/var/lib/libvirt/images/` — those are VM disks (user data). Only the
user decides; offer `virt-sparsify`/`qemu-img convert` to *compact* rather than delete.

### 3h. Consolidate Python venvs into ONE shared venv (prevents future bloat)
Auto-detect the largest existing venv as a seed, merge the rest by **local copy**
(never re-download). Set `PROJECTS` to your code directory first (must be outside
XDG dirs — e.g. `$HOME/.projects`).

```bash
set -e
PROJECTS="${PROJECTS:-$HOME/.projects}"
if [ ! -d "$PROJECTS" ]; then echo "PROJECTS dir '$PROJECTS' not found — set it to your code dir."; exit 1; fi
SEED=$(find "$PROJECTS" -maxdepth 4 \( -name .venv -o -name venv \) -type d -exec du -s {} + 2>/dev/null | sort -rn | head -1 | awk '{print $2}')
if [ -z "$SEED" ]; then echo "No venvs found under $PROJECTS — nothing to merge."; exit 0; fi
SHARED="$PROJECTS/.venv"
cleanup() { echo "ERROR: merge failed"; rm -rf "$SHARED"; exit 1; }
trap cleanup ERR
cp -a "$SEED" "$SHARED"

# Merge missing packages from the other venvs into the shared one
python3 - <<'PY'
import os, shutil, glob as _g
projects = os.environ["PROJECTS"]
shared_path = os.path.join(projects, ".venv")
sp_shared = _g.glob(os.path.join(shared_path, "lib", "python3.*", "site-packages"))[0]
skip = {"pip","setuptools","_virtualenv.py","_virtualenv.pth","pkg_resources",
        "distlib","_distutils_hack","easy_install.py"}
venvs = set()
for pat in ("**/.venv", "**/venv"):
    venvs |= set(_g.glob(os.path.join(projects, pat), recursive=True))
for v in venvs:
    if os.path.abspath(v) == os.path.abspath(shared_path): continue
    sp = _g.glob(os.path.join(v, "lib", "python3.*", "site-packages"))
    if not sp: continue
    sp = sp[0]
    for n in os.listdir(sp):
        if n in skip or n.startswith("__pycache__") or n.endswith(".pyc"): continue
        dp = os.path.join(sp_shared, n)
        if os.path.exists(dp): continue
        s = os.path.join(sp, n)
        if os.path.isdir(s): shutil.copytree(s, dp)
        else: shutil.copy2(s, dp)
print("merged packages into shared venv")
PY

# Remove stale setuptools .pth shims that error on import
find "$SHARED/lib" -name 'distutils-precedence.pth' -delete

# Verify
"$SHARED/bin/python" -c "import importlib.util as u; mods=['fastapi','pandas','numpy','flask','sqlalchemy']; missing=[m for m in mods if not u.find_spec(m)]; print('shared venv OK' if not missing else 'MISSING: '+str(missing))"

# Symlink each project's venv to the shared one (keep originals as .old backup)
for v in $(find "$PROJECTS" -maxdepth 4 \( -name .venv -o -name venv \) -type d); do
  [ -L "$v" ] && continue
  [ -d "$v" ] && mv "$v" "$v.old" && ln -s "$SHARED" "$v" && echo "linked $v"
done
```

### 3i. Stop npm bloat from returning — use pnpm
```bash
npm install -g pnpm          # pnpm stores each package version ONCE globally
# Future projects: `pnpm init && pnpm add ...` instead of npm
# Existing npm projects can stay; just clear the redundant npm cache (3f)
# Bun projects already dedupe via their own global cache — leave them.
```

## Post-cleanup (report only)

- Report `df -h /` before/after.
- Note that `.old` venv backups should stay until projects are confirmed working.
- If a package was missing from the source venv to begin with, note it — it's not a
  merge loss, just pre-existing.

## Quick reference

| Goal | Command |
|---|---|
| Run full recon | `bash ~/.agents/skills/pc-clean/scripts/scan.sh` |
| List orphans | `pacman -Qtd` |
| Safe remove (no cascade) | `pkexec pacman -R --noconfirm pkg` |
| Keep wanted orphan | `pacman -D --asexplicit pkg` |
| Current kernel headers? | `pacman -Q linux linux-headers` |
| Who needs a pkg? | `pacman -Qi pkg \| grep -E "^Required By\s*:\s*\S"` |
| Clear npm cache | `npm cache clean --force` |
| Dedup node deps | `npm i -g pnpm` |
| Browser cache (safe) | `rm -rf ~/.cache/<browser>/*` |
| systemd coredumps | `pkexec coredumpctl delete` |
| Prune pacman cache | `pkexec sh -c 'paccache -rk3; paccache -ruk0'` |
| Vacuum journal | `pkexec journalctl --vacuum-size=200M` |
| Big files in hidden dirs | `find ~/.[!.]* -xdev -type f -size +500M -exec du -h {} + \| sort -rh` |
| \$HOME hidden dirs | `du -sh ~/.[!.]* \| sort -rh` |
