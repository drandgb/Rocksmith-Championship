#!/usr/bin/env bash
# Rebuild index.html from the scoreboard Google Sheet.
#   ./build.sh                 download the sheet and build
#   ./build.sh path/to.xlsx    build from a downloaded copy
# MODE=full  (default) re-reads every WeekNNN tab
# MODE=quick re-reads only the newest week tabs and reuses build/data/cache for older weeks
set -euo pipefail
cd "$(dirname "$0")"
SHEET_ID="${SHEET_ID:-1WN-m8wF0lVkQ4cLWHBa009SkqDoPk0xN-C4-llcrXXs}"
export MODE="${MODE:-full}"
rm -rf work && mkdir -p work data/cache
cp *.py *.js template.html data/*.json work/
cp -r data/cache work/cache
if [ "${1:-}" != "" ]; then
  cp "$1" work/board.xlsx
else
  echo "Downloading the scoreboard sheet..."
  curl -sSfL -o work/board.xlsx "https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=xlsx"
fi
cd work
python3 build_weeks.py
python3 build_songsel.py
python3 parse_weeks.py
python3 build_sb.py
python3 build_links.py
python3 build_players.py
python3 build_rankings.py
python3 build_yearend.py || echo "yearend: skipped"
python3 build_level.py || echo "level: skipped"
# when the sheet was last edited: sent by the sheet's updateWebsite script; kept in the cache between runs
if [[ "${SHEET_EDITED:-}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z$ ]]; then printf '"%s"' "$SHEET_EDITED" > cache/sheet_edited.json; fi
OUT="${OUT:-../../index.html}" python3 render.py
# medal leaders: count them once in headless Chrome from the page just built, then build the page again with them
rm -f ml_pre.json
python3 ml_pre.py "${OUT:-../../index.html}" && if [ -f ml_pre.json ]; then OUT="${OUT:-../../index.html}" python3 render.py; fi
# scoreboard fix log: what the scoreboard checks found fixed since the previous update (fixlog.js)
node fixlog.js "${OUT:-../../index.html}" cache || echo "fixlog: skipped"
# Your week: first and best scores this week, and who passed whom (weeklog.js)
node weeklog.js "${OUT:-../../index.html}" cache || echo "weeklog: skipped"
# original host ratings: frozen the first time each challenge is seen (hostorig.js)
node hostorig.js "${OUT:-../../index.html}" cache || echo "hostorig: skipped"
# the website's rating for each recent challenge, for drandTools (ratings_pre.py writes ratings.json next to the page)
python3 ratings_pre.py "${OUT:-../../index.html}" || echo "ratings: skipped"
# each week's forum post from the NewWeekPost sheet, for drandTools (weekposts.py writes weekposts.json next to the page)
python3 weekposts.py "${OUT:-../../index.html}" || echo "weekposts: skipped"
cp cache/*.json ../data/cache/
