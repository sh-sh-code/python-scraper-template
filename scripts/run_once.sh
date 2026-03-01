#!/usr/bin/env bash
# -------------------------------------------------------
# run_once.sh — Run the scraper once and exit.
#
# Usage:
#   ./scripts/run_once.sh
#   ./scripts/run_once.sh --limit 10
#
# Exit codes:
#   0  success
#   1  scraper error (parse failure, network error, etc.)
# -------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Activate virtualenv if present
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

python -m scraper "$@"
