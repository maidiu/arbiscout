#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x '.venv/bin/python' ]; then
  echo 'Creating isolated Python environment...'
  python3 -m venv .venv
fi
.venv/bin/python -m pip -q install -r requirements.txt
URL="${1:-}"
if [ -z "$URL" ]; then
  printf 'Best Buy deals page URL [https://www.bestbuy.com/black-friday]: '
  IFS= read -r URL
fi
URL="${URL:-https://www.bestbuy.com/black-friday}"
EBAY_DIR="${2:-}"
if [ -z "$EBAY_DIR" ]; then
  printf 'Folder of saved eBay sold pages (01.html..20.html), or Return to skip: '
  IFS= read -r EBAY_DIR
fi
CMD=(.venv/bin/python run_test.py
  --url "$URL"
  --mode browser --browser-visible
  --timeout 60 --delay 2
  --output bestbuy_live)
if [ -n "$EBAY_DIR" ]; then
  CMD+=(--ebay-pages "$EBAY_DIR" --ebay-auto-match)
  if [ -f 'bestbuy_live/retailer/products.json' ]; then
    CMD+=(--reuse-retailer)
  fi
  printf 'Delete the saved eBay HTML files after processing? [y/N]: '
  IFS= read -r DELETE_EBAY
  case "$DELETE_EBAY" in
    y|Y|yes|YES) CMD+=(--delete-ebay-pages) ;;
  esac
fi
"${CMD[@]}"
open bestbuy_live/index.html
