#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x '.venv/bin/python' ]; then python3 -m venv .venv; fi
.venv/bin/python -m pip -q install -r requirements.txt
printf 'Path to an HTML page you already saved: '
IFS= read -r FILE
# Finder drag-and-drop in Terminal may escape spaces as \\ .
FILE="${FILE//\\ / }"
printf 'Original full URL of that page: '
IFS= read -r URL
if [ ! -f "$FILE" ]; then echo "File not found: $FILE"; exit 1; fi
.venv/bin/python arbiscout.py --snapshot "$FILE" --snapshot-url "$URL" --offline --outdir arbiscout_output
open arbiscout_output/index.html
