#!/bin/bash
set -e
cd "$(dirname "$0")"
FILE="${1:-selected.json}"
if [ ! -f "$FILE" ]; then
  echo "Usage: ./run_selected.command selected.json"
  exit 1
fi
.venv/bin/python - "$FILE" <<'PY'
import json
from pathlib import Path
import sys
data=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
products=data.get("products") if isinstance(data,dict) else data
out=Path("catalog/selected/retailer")
out.mkdir(parents=True,exist_ok=True)
(out/"products.json").write_text(json.dumps(products,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
Path("catalog/selected/selection.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(len(products),"products selected")
PY
.venv/bin/python run_test.py --reuse-retailer --keep-selection --output catalog/selected
open catalog/selected/index.html
