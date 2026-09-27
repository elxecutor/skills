#!/usr/bin/env bash
# pc-clean scan — read-only bloat recon for Arch Linux (any DE).
# Prints a report. Modifies nothing. Run: bash ~/.agents/skills/pc-clean/scripts/scan.sh
#
# Optional env var: PROJECTS (default $HOME/Documents/projects) — where source
# code / venvs / node_modules live. Set it to scope the venv/node_modules scan.
set -u

PROJECTS="${PROJECTS:-$HOME/Documents/projects}"

hr() { printf '%s\n' "────────────────────────────────────────────"; }

echo "PC-CLEAN RECON REPORT — $(date)"
echo "PROJECTS dir: $PROJECTS"
hr

echo; echo "## 1. GHOST .desktop LAUNCHERS (Exec= -> missing binary)"
echo "  (NOTE: ignore KDE daemon / TeX binaries in non-PATH libexec dirs — false positives)"
found=0
for f in /usr/share/applications/*.desktop; do
  exec_line=$(grep -m1 '^Exec=' "$f" 2>/dev/null | sed 's/^Exec=//')
  [ -n "$exec_line" ] || continue
  binary=$(echo "$exec_line" | awk '{print $1}')
  if ! [ -e "$binary" ] && ! command -v "$binary" >/dev/null 2>&1; then
    name=$(grep -m1 '^Name=' "$f" 2>/dev/null | cut -d= -f2)
    echo "  GHOST: ${name:-?} ($binary)  <-  $f"; found=1
  fi
done
[ "$found" = 0 ] && echo "  (none)"

echo; echo "## 2. BROKEN SYMLINKS under /usr/local /opt /$HOME/.local"
for p in /usr/local /opt "$HOME/.local"; do
  find "$p" -type l ! -exec test -e {} \; -print 2>/dev/null
done
echo "  (end)"

echo; echo "## 3. UNOWNED /etc CONFIG DIRS"
echo "  (NOTE: mostly false positives — a package often owns files INSIDE the dir,"
echo "   not the dir itself. Verify with: pacman -Qo /etc/<dir>/<a-file>)"
for d in /etc/*/; do pacman -Qo "$d" >/dev/null 2>&1 || echo "  UNOWNED: $(basename "$d")"; done

echo; echo "## 4. ORPHAN PACKAGES (pacman -Qtd)"
orphans=$(pacman -Qtdq 2>/dev/null)
if [ -n "$orphans" ]; then
  echo "$orphans" | sed 's/^/  /'
  echo "  Count: $(echo "$orphans" | wc -l)"
else
  echo "  (none)"
fi

echo; echo "## 5. CURRENT KERNEL HEADERS (KEEP if versions match)"
pacman -Q linux linux-headers 2>/dev/null | sed 's/^/  /'

echo; echo "## 6. TOP PACKAGES BY SIZE (MiB)"
pacman -Qi 2>/dev/null | awk '/^Name/{n=$3} /^Installed Size/{s=$4; u=$5; if(u=="MiB") printf "%8.1f  %s\n", s, n; else if(u=="KiB") printf "%8.1f  %s\n", s/1024, n}' | sort -rn | head -25 | sed 's/^/  /'

echo; echo "## 7. CACHE SIZES"
for c in ~/.cache/pip ~/.cache/uv ~/.cache/go-build ~/.cache/dotslash ~/.npm/_cacache ~/.npm/_npx ~/.bun/install/cache; do
  [ -e "$c" ] && printf "  %8s  %s\n" "$(du -sh "$c" 2>/dev/null | cut -f1)" "$c"
done
# browser caches (any dir under ~/.cache that looks like a browser)
for b in ~/.cache/*/; do
  case "$(basename "$b")" in
    BraveSoftware|google-chrome|chromium|firefox|mozilla|Microsoft|Edge|Vivaldi*) printf "  %8s  %s\n" "$(du -sh "$b" 2>/dev/null | cut -f1)" "$b";;
  esac
done

echo; echo "## 8. SYSTEM /var BLOAT (usually the biggest safe wins)"
[ -d /var/lib/systemd/coredump ] && printf "  %8s  coredumps (%s files)\n" \
  "$(du -sh /var/lib/systemd/coredump 2>/dev/null | cut -f1)" \
  "$(ls /var/lib/systemd/coredump 2>/dev/null | wc -l)"
[ -d /var/cache/pacman/pkg ] && printf "  %8s  pacman pkg cache (%s files)\n" \
  "$(du -sh /var/cache/pacman/pkg 2>/dev/null | cut -f1)" \
  "$(ls /var/cache/pacman/pkg 2>/dev/null | wc -l)"
[ -d /var/log/journal ] && printf "  %8s  journal logs\n" \
  "$(du -sh /var/log/journal 2>/dev/null | cut -f1)"
if [ -d /var/lib/libvirt/images ]; then
  echo "  libvirt VM images (USER DATA — report only, never auto-delete):"
  du -sh /var/lib/libvirt/images/* 2>/dev/null | sort -rh | sed 's/^/    /'
fi

echo; echo "## 9. TOP-LEVEL \$HOME ENTRIES (hidden dirs included)"
du -sh ~/.[!.]* ~/* 2>/dev/null | sort -rh | head -20 | sed 's/^/  /'

echo; echo "## 10. LARGE FILES IN \$HOME (>500M — dbs/logs du -sh */ misses)"
find "$HOME" -type f -size +500M -exec du -h {} + 2>/dev/null | sort -rh | head -15 | sed 's/^/  /'

echo; echo "## 11. REDUNDANT PYTHON VENVS (under $PROJECTS)"
find "$PROJECTS" -maxdepth 4 \( -name '.venv' -o -name 'venv' \) -type d 2>/dev/null | while read -r v; do
  sz=$(du -sh "$v" 2>/dev/null | cut -f1)
  py=$(grep -m1 version_info "$v/pyvenv.cfg" 2>/dev/null | grep -o '[0-9.]*')
  printf "  %8s  py%s  %s\n" "$sz" "${py:-?}" "$v"
done

echo; echo "## 12. node_modules DIRS (under $PROJECTS)"
find "$PROJECTS" -maxdepth 4 -name node_modules -type d -prune 2>/dev/null | while read -r n; do
  printf "  %8s  %s\n" "$(du -sh "$n" 2>/dev/null | cut -f1)" "$n"
done

echo; echo "## 13. UNMANAGED /opt INSTALLS"
for d in /opt/*/; do pacman -Qo "$d" 2>&1 | grep -q error && echo "  UNMANAGED: $d"; done

hr
echo "Recon complete. Review items above, then remove with explicit confirmation."
echo "See SKILL.md for safe removal commands (use 'pacman -R', never 'pacman -Rns')."
