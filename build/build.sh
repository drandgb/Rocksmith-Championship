#!/usr/bin/env bash
# Rebuild index.html from the scoreboard Google Sheet.
#   ./build.sh                 download the sheet and build
#   ./build.sh path/to.xlsx    build from a downloaded copy
set -euo pipefail
cd "$(dirname "$0")"
SHEET_ID="${SHEET_ID:-1WN-m8wF0lVkQ4cLWHBa009SkqDoPk0xN-C4-llcrXXs}"
rm -rf work && mkdir work
cp *.py template.html data/*.json work/
if [ "${1:-}" != "" ]; then
  cp "$1" work/board.xlsx
else
  echo "Downloading the scoreboard sheet..."
  curl -sSfL -o work/board.xlsx "https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=xlsx"
fi
cd work
python3 build_weeks.py
python3 parse_board.py
python3 fonts.py
python3 build_sb.py
python3 build_players.py
OUT="${OUT:-../../index.html}" python3 render.py
