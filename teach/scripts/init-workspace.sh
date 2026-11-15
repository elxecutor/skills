#!/usr/bin/env bash
# Initialise or inspect a teach workspace.
#
# Optional teaching state lives inside a dedicated workspace directory, by default
# ./teaching/ relative to the current directory. The parent directory is never
# written to, so invoking the skill from a project root cannot litter it.
#
#   bash init-workspace.sh              # create ./teaching/ if absent
#   bash init-workspace.sh --check      # report only, write nothing
#   bash init-workspace.sh ./notes/rf   # use an explicit workspace directory
#
# Creates only NOTES.md and PROGRESS.md. Extra files/directories are on demand.
# Never overwrites an existing file, deletes anything, or writes outside the workspace.

set -euo pipefail

DEFAULT_WORKSPACE="teaching"

usage() {
  echo "usage: $(basename "$0") [--check] [workspace-dir]" >&2
  echo "  workspace-dir defaults to ./$DEFAULT_WORKSPACE" >&2
}

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
mode="create"
workspace=""

while (( $# )); do
  case "$1" in
    --check) mode="check" ;;
    -h|--help) usage; exit 0 ;;
    "") echo "error: workspace directory must not be empty" >&2; exit 2 ;;
    -*) echo "error: unknown option $1" >&2; usage; exit 2 ;;
    *)
      if [[ -n "$workspace" ]]; then
        echo "error: only one workspace directory may be given" >&2
        usage; exit 2
      fi
      workspace="$1"
      ;;
  esac
  shift
done

# ---------------------------------------------------------------------------
# Resolve the workspace directory.
#
# If no directory was given, adopt the current one only when it already looks
# like a teaching workspace — otherwise always nest under ./teaching/.
# ---------------------------------------------------------------------------
looks_like_workspace() {
  local d="$1"
  [[ -f "$d/NOTES.md" || -f "$d/MISSION.md" || -f "$d/TEACHING-STRATEGY.md" || -f "$d/PROGRESS.md" ]]
}

if [[ -z "$workspace" ]]; then
  if looks_like_workspace "."; then
    workspace="."
  else
    workspace="$DEFAULT_WORKSPACE"
  fi
fi

# Strip a trailing slash so printed paths read cleanly.
workspace="${workspace%/}"
[[ -n "$workspace" ]] || workspace="."

# Refuse anything that would escape upwards into the parent directory.
case "$workspace" in
  ..|../*|/*)
    echo "error: workspace must be a path inside the current directory" >&2
    exit 2
    ;;
esac

# The case pattern above only catches paths that BEGIN with "..". A path with
# ".." inside it ("./notes/../notes/rf", "./..") would pass and write outside.
# Canonicalise, then require the result to be at or under the cwd.
cwd="$(pwd -P)"
resolved="$(realpath -m -- "$workspace" 2>/dev/null || true)"
if [[ -z "$resolved" || ( "$resolved" != "$cwd" && "$resolved" != "$cwd"/* ) ]]; then
  echo "error: workspace resolves outside the current directory: ${resolved:-<unresolvable>}" >&2
  exit 2
fi
if [[ "$resolved" == "$cwd" ]]; then
  workspace="."
else
  workspace="${resolved#"$cwd"/}"
fi

# `-L` is checked on its own, not gated on `! -d`: a symlink to a directory
# still tests true for -d, and writing through it would place the whole
# workspace at an arbitrary target outside this project.
if [[ -L "$workspace" ]]; then
  echo "error: $workspace is a symlink; refusing to write the workspace through it." >&2
  echo "       cd into the real directory and re-run, or pass a real path." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# --check: report and exit
# ---------------------------------------------------------------------------
if [[ "$mode" == "check" ]]; then
  echo "Workspace: ${workspace}/"
  echo
  if [[ ! -d "$workspace" ]]; then
    echo "  [MISS] workspace directory does not exist"
    exit 0
  fi
  for d in lessons reference assets learning-records playground; do
    if [[ -d "$workspace/$d" ]]; then
      # 2>/dev/null || true so an unreadable directory degrades to a report
      # instead of killing --check under `set -euo pipefail`.
      count=$( { find "$workspace/$d" -maxdepth 1 -type f ! -name '.gitkeep' 2>/dev/null || true; } | wc -l )
      printf '  [dir ] %-22s %s file(s)\n' "$d/" "$count"
    fi
  done
  for f in NOTES.md PROGRESS.md; do
    if [[ -s "$workspace/$f" ]]; then
      printf '  [ok  ] %-22s %s line(s)\n' "$f" "$(wc -l < "$workspace/$f" | tr -d ' ')"
    elif [[ -f "$workspace/$f" ]]; then
      printf '  [    ] %-22s empty placeholder\n' "$f"
    else
      printf '  [MISS] %-22s\n' "$f"
    fi
  done
  echo
  echo "Only NOTES.md and PROGRESS.md are scaffolded; all other material is optional."
  exit 0
fi

# ---------------------------------------------------------------------------
# create: workspace directory and two minimal notes, no support directories.
# Existing paths are left alone.
# ---------------------------------------------------------------------------
created=0
kept=()

if [[ ! -d "$workspace" ]]; then
  mkdir -p "$workspace" || { echo "error: cannot create $workspace/" >&2; exit 1; }
  echo "created  $workspace/"
  created=$((created + 1))
fi

placeholder() {
  # $1 = filename within the workspace, $2 = content
  local path="$workspace/$1"
  # `-e` follows symlinks, so a DANGLING symlink would test false and `>` would
  # then write through it to an arbitrary path outside the workspace. `-L`
  # catches that case and keeps whatever is already there.
  if [[ -e "$path" || -L "$path" ]]; then
    kept+=("kept     $workspace/$1")
    return
  fi
  printf '%s\n' "$2" > "$path"
  echo "created  $workspace/$1"
  created=$((created + 1))
}

placeholder NOTES.md "# Teaching contract and source map
<!-- Persist only agreed purpose, source/order, execution environment, interaction preferences, and source resume point. Reuse existing answers. -->"

placeholder PROGRESS.md "# Progress
<!-- When useful, note the current source anchor, one task, learner evidence/help, blocker, and next action. No assessment ledger required. -->"

echo
# Print what was inspected and left alone. The `${#kept[@]}` guard matters:
# under `set -u`, expanding an empty array errors on bash < 4.4.
if (( ${#kept[@]} )); then
  printf '%s\n' "${kept[@]}"
  echo
fi

if (( created == 0 )); then
  echo "Workspace already initialised at ${workspace}/ — nothing changed."
else
  echo "Initialised ($created created, ${#kept[@]} kept) in ${workspace}/"
fi
