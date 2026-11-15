#!/usr/bin/env bash
# Read-only hidden-home-folder inventory. Python's -B prevents bytecode writes.
set -u
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'pc-clean: python3 is required for the read-only scanner' >&2
  exit 127
fi
exec python3 -B "$(dirname -- "${BASH_SOURCE[0]}")/scan.py" "$@"
