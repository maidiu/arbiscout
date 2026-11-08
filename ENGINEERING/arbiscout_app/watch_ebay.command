#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x '.venv/bin/python' ]; then
  echo 'Creating isolated Python environment...'
  python3 -m venv .venv
fi
.venv/bin/python -m pip -q install -r requirements.txt
FOLDER=ebay_saved
OUTPUT=bestbuy_live
DELETE=0
KEEP=0
while [ $# -gt 0 ]; do
  case "$1" in
    --output) OUTPUT="$2"; shift 2 ;;
    --delete-on-exit) DELETE=1; shift ;;
    --keep-selection) KEEP=1; shift ;;
    *) FOLDER="$1"; shift ;;
  esac
done
if [ ! -f "$OUTPUT/retailer/products.json" ]; then
  echo "No retailer products in $OUTPUT. Run ./run_live.command or ./run_api.command first."
  exit 1
fi
ARGS=(--folder "$FOLDER" --output "$OUTPUT")
if [ "$DELETE" -eq 1 ]; then ARGS+=(--delete-on-exit); fi
if [ "$KEEP" -eq 1 ]; then ARGS+=(--keep-selection); fi
exec .venv/bin/python ebay_watcher.py "${ARGS[@]}"
