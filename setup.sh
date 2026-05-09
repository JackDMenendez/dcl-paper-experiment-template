#!/usr/bin/env bash
# Create the Python virtual environment and install dependencies.
set -euo pipefail
cd "$(dirname "$0")"
exec make env
