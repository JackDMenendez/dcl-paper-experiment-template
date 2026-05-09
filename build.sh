#!/usr/bin/env bash
# Build the paper from the repository root.
#
# Usage:
#   ./build.sh            # build the paper (default)
#   ./build.sh all        # full build: env, tests, paper, promote
#   ./build.sh tests      # run pytest
#   ./build.sh clean      # remove build artifacts
#
# Requires GNU Make >= 4.3, a TeX distribution (MiKTeX or TeX Live),
# and Python 3.  On Windows, run from an MSYS2 UCRT64 shell.

set -euo pipefail

cd "$(dirname "$0")"

target="${1:-paper}"

if ! command -v make >/dev/null 2>&1; then
    echo "build.sh: GNU Make is required but not found in PATH." >&2
    exit 1
fi

exec make "$target"
