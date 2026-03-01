#!/usr/bin/env bash
# -------------------------------------------------------
# run_daily.sh — Daily cron wrapper.
#
# Intended to be called from crontab. Handles:
#   - virtualenv activation
#   - date-partitioned logging
#   - exit code propagation
#
# Crontab example (every day at 06:00 JST):
#   0 6 * * * /absolute/path/to/scripts/run_daily.sh >> /tmp/scraper-cron.log 2>&1
# -------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY="$(date +%Y-%m-%d)"

cd "$PROJECT_DIR"

# Activate virtualenv if present
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

echo "[$TODAY] Starting daily scrape..."

if python -m scraper --date "$TODAY"; then
    echo "[$TODAY] Success"
    exit 0
else
    echo "[$TODAY] FAILED (exit $?)" >&2
    exit 1
fi
