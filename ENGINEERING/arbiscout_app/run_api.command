#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x '.venv/bin/python' ]; then
  echo 'Creating isolated Python environment...'
  python3 -m venv .venv
fi
.venv/bin/python -m pip -q install -r requirements.txt
SOURCE="${1:-}"
if [ -z "$SOURCE" ]; then
  printf 'Source (meh/woot/kroger): '
  IFS= read -r SOURCE
fi
case "$SOURCE" in
  meh|woot|kroger) ;;
  *) echo 'Choose meh, woot, or kroger.'; exit 1 ;;
esac
OUTPUT="${2:-${SOURCE}_live}"
ARGS=(--source "$SOURCE" --output "$OUTPUT" --max-products 500)
if [ "$SOURCE" = 'woot' ]; then
  printf 'Woot feed [Featured]: '
  IFS= read -r FEED
  ARGS+=(--feed "${FEED:-Featured}")
fi
if [ "$SOURCE" = 'kroger' ]; then
  printf 'Kroger search terms (comma-separated) [milk,eggs,bread]: '
  IFS= read -r TERMS
  ARGS+=(--terms "${TERMS:-milk,eggs,bread}")
  printf 'Kroger ZIP code (blank uses KROGER_ZIP from .env): '
  IFS= read -r ZIP
  if [ -n "$ZIP" ]; then ARGS+=(--zip "$ZIP"); fi
fi
.venv/bin/python providers.py "${ARGS[@]}"
.venv/bin/python run_test.py --reuse-retailer --output "$OUTPUT"
open "$OUTPUT/retailer/index.html"
echo
echo "To capture eBay sold pages: ./watch_ebay.command ebay_saved --output $OUTPUT"
