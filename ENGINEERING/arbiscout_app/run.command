#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x '.venv/bin/python' ]; then
  echo 'Creating isolated Python environment...'
  python3 -m venv .venv
fi
.venv/bin/python -m pip -q install -r requirements.txt
printf 'Retailer deals page URL: '
IFS= read -r URL
if [ -z "$URL" ]; then echo 'No URL provided'; exit 1; fi
.venv/bin/python arbiscout.py "$URL" --depth 2 --max-listings 12 --max-products 12 --outdir arbiscout_output
open arbiscout_output/index.html
