#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -f 'bestbuy_live/comparisons/comparisons.json' ]; then
  echo 'Run ./run_live.command first so the Best Buy candidates exist.'
  exit 1
fi
.venv/bin/python - <<'PY'
import json, subprocess, sys
from pathlib import Path
try:
    tty=open('/dev/tty')
except OSError:
    tty=sys.stdin
def ask(prompt):
    print(prompt,end='',flush=True)
    line=tty.readline()
    if not line:raise SystemExit
    return line.strip()
rows=sorted(json.loads(Path('bestbuy_live/comparisons/comparisons.json').read_text()),
            key=lambda r:r.get('fixture_index',999))
folder=ask('Folder to save eBay pages into [ebay_saved]: ') or 'ebay_saved'
Path(folder).mkdir(parents=True,exist_ok=True)
print('For each candidate: open its eBay sold page in your browser, then use')
print('File > Save Page As and save it into', folder)
print('Any filename works; matching is by the eBay search query.')
for r in rows:
    name=r.get('fixture_file','??.html')
    print('\n'+name+'  '+r['retailer']['title'][:90])
    print('   '+r['ebay_search_url'])
    answer=ask('Open this page now? [Y/n/q] ').lower()
    if answer=='q':break
    if answer!='n':
        subprocess.run(['open',r['ebay_search_url']],check=False)
        ask('   Press Return after saving it as '+name+' (Return alone skips)... ')
print('\nDone. Rerun ./run_live.command and give it the folder:',folder)
PY
