#!/usr/bin/env python3
"""End-to-end local operator: retailer discovery then date-filtered eBay comparison."""
import argparse
from pathlib import Path
import subprocess
import sys
import webbrowser

def main():
    p=argparse.ArgumentParser(description='ArbiScout source → discovery → eBay reference')
    p.add_argument('url',help='Initial retailer sale page')
    p.add_argument('--snapshot',help='Optional previously saved retailer HTML page')
    p.add_argument('--offline',action='store_true')
    p.add_argument('--mode',choices=('http','browser'),default='http')
    p.add_argument('--depth',type=int,default=2)
    p.add_argument('--max-listings',type=int,default=12)
    p.add_argument('--max-products',type=int,default=12)
    p.add_argument('--top',type=int,default=20)
    p.add_argument('--retail-order',choices=('percent','dollars'),default='percent')
    p.add_argument('--ebay-live',action='store_true')
    p.add_argument('--ebay-fixtures')
    p.add_argument('--outdir',default='arbiscout_output')
    a=p.parse_args()
    root=Path(a.outdir)
    cmd=[sys.executable,str(Path(__file__).with_name('arbiscout.py')),a.url,'--outdir',str(root/'retail'),'--depth',str(a.depth),'--max-listings',str(a.max_listings),'--max-products',str(a.max_products),'--mode',a.mode]
    if a.snapshot:cmd+=['--snapshot',a.snapshot]
    if a.offline:cmd+=['--offline']
    result=subprocess.run(cmd)
    if result.returncode:raise SystemExit(result.returncode)
    cmd=[sys.executable,str(Path(__file__).with_name('ebay_comparison.py')),'--retail-json',str(root/'retail'/'products.json'),'--outdir',str(root/'comparisons'),'--top',str(a.top),'--sort-retailer',a.retail_order]
    if a.ebay_live:cmd+=['--ebay-live']
    if a.ebay_fixtures:cmd+=['--ebay-fixtures',a.ebay_fixtures]
    result=subprocess.run(cmd)
    if result.returncode:raise SystemExit(result.returncode)
    final=(root/'comparisons'/'index.html').resolve()
    print('Dashboard:',final)
    webbrowser.open(final.as_uri())

if __name__=='__main__':main()
