#!/usr/bin/env bash
# Lae Google Sheet → genereeri data.json → kui muutus, commit + push (GitHub Pages deploy).
# Jookseb cronist (õhtuti/öösiti iga 15 min). Push toimub AINULT kui data.json muutub.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
LOG="logs/update.log"
ts() { date '+%Y-%m-%d %H:%M:%S'; }

{
  if ! python3 build_data.py; then
    echo "$(ts) BUILD FAIL (Sheet ligipääs?)"
    exit 1
  fi
  if git diff --quiet -- data.json; then
    echo "$(ts) muutusi pole"
    exit 0
  fi
  git add data.json
  git -c user.name="Aimar Raid" -c user.email="aimarraid@gmail.com" \
      commit -q -m "data: auto-uuendus $(ts)"
  if ! git push -q origin main; then
    git pull -q --rebase --autostash origin main && git push -q origin main
  fi
  echo "$(ts) PUSHED → GitHub Pages deploy"
} >> "$LOG" 2>&1
