#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -x '.venv/bin/python' ]; then
  echo 'Creating isolated Python environment...'
  python3 -m venv .venv
fi
.venv/bin/python -m pip -q install -r requirements.txt
.venv/bin/python build_catalog.py --output catalog
exec .venv/bin/python catalog_server.py --catalog catalog --output catalog
