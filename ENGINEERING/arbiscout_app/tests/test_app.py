import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import arbiscout as a

ROOT='https://shop.example.com'

def card(name,url,current=None,regular=None):
    curr=f'<span class="sale-price">${current}</span>' if current else ''
    prev=f'<s class="regular-price">${regular}</s>' if regular else ''
    return f'<div class="product-item"><h3>{name}</h3><a href="{url}">Shop</a>{curr}{prev}</div>'

class AppTests(unittest.TestCase):
    def test_sold_query_filters_and_user_edit(self):
        s=a.ebay_sold_url('Lenovo ThinkPad X1 Carbon 16GB')
        self.assertIn('LH_Sold=1',s);self.assertIn('LH_Complete=1',s)
        self.assertIn('ThinkPad',s)
        self.assertNotIn('days=30',s)
    def test_scope_and_private_host(self):
        self.assertFalse(a.is_safe_http('http://localhost:8080/'))
        self.assertFalse(a.is_safe_http('http://127.0.0.1/'))
        self.assertFalse(a.is_safe_http('file:///etc/passwd'))
        self.assertTrue(a.is_safe_http(ROOT+'/sale'))
        self.assertFalse(a.same_site('https://shop.example.com.evil.org/sale',ROOT))
    def test_link_scoring(self):
        self.assertGreater(a.score_link(ROOT+'/sale/cameras','Camera clearance'),0)
        self.assertEqual(a.score_link(ROOT+'/account','Account'),0)
        self.assertEqual(a.score_link(ROOT+'/product/gizmo','Gizmo'),0)
    def test_product_price_merge_no_invented_mix(self):
        st=a.Store()
        p1=a._make_record(ROOT+'/product/z1','Gizmo',ROOT+'/sale',0,'card',current=20,regular=None)
        p2=a._make_record(ROOT+'/product/z1','Gizmo',ROOT+'/sale/cameras',1,'card',current=20,regular=50)
        st.add([p1]);st.add([p2]);p=st.records()[0]
        self.assertEqual(p['savings'],30)
        self.assertEqual(p['discount_percent'],60)
    def test_price_variant_conflict(self):
        st=a.Store()
        u='https://www.bestbuy.com/product/brand-gadget/QJ1'
        st.add([a._make_record(u,'Gadget',ROOT+'/sale',0,'card',current=50,regular=80,sku='111')])
        st.add([a._make_record(u,'Gadget',ROOT+'/sale',1,'card',current=60,regular=80,sku='222')])
        p=st.records()[0]
        self.assertTrue(p['variant_conflict']);self.assertIsNone(p['current_price'])
    def test_html_escaping(self):
        st=a.Store()
        st.add([a._make_record(ROOT+'/product/test','<script>alert("hi")</script>',ROOT+'/sale',0,'card')])
        d=a.render_dashboard(st.records(),[],{},{});
        self.assertNotIn('<script>alert',d)
        self.assertIn('\\u003cscript',d)
    def test_generic_listing_price(self):
        h=f'<main>{card("Branded Gizmo Model K55","/product/gizmo-k55","45.00","90.00")}</main>'
        rows=a.extract(a.BeautifulSoup(h,'html.parser'),ROOT+'/sale',0)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['current_price'],45)
        self.assertEqual(rows[0]['regular_price'],90)
    def test_json_ld(self):
        h='<script type="application/ld+json">'+json.dumps({'@type':'Product','name':'Brand Widget 700','url':ROOT+'/product/widget-700','model':'700','brand':{'name':'Brand'},'offers':{'price':'19.95'}})+'</script>'
        rows=a.extract(a.BeautifulSoup(h,'html.parser'),ROOT+'/product/widget-700',1)
        self.assertTrue(any(x['current_price']==19.95 and x['model']=='700' for x in rows))
    def test_crawl_links_and_product_fallback_without_network(self):
        first='<main><h1>Holiday sale</h1>'+card('Gizmo Model Z1','/product/gizmo-z1')+'<a href="/sale/cameras">Camera sale deals</a></main>'
        second='<main>'+card('Gizmo Model Z1','/product/gizmo-z1','40.00','100.00')+card('Widget Model K2','/product/widget-k2')+'</main>'
        product='<html><h1>Widget Model K2</h1><div data-testid="price-block-customer-price">$27.00</div><div data-testid="price-block-regular-price">$54.00</div></html>'
        responses={ROOT+'/sale':first,ROOT+'/sale/cameras':second,ROOT+'/product/widget-k2':product}
        class Args: pass
        args=Args();args.url=ROOT+'/sale';args.snapshot=None;args.snapshot_url=None;args.offline=False;args.outdir=tempfile.mkdtemp();args.save_html=False
        args.depth=2;args.max_listings=5;args.max_products=5;args.enrich_models=False;args.delay=.7;args.mode='http';args.timeout=10
        with patch.object(a.Fetcher,'get',lambda self,url:responses[url]):
            store,log,nav=a.crawl(args)
        products=store.records()
        self.assertEqual(len(products),2)
        self.assertEqual(sum(x['price_complete'] for x in products),2)
        self.assertEqual(sum(x['type']=='product' for x in log),1)
        self.assertEqual(len(log),3)
    def test_saved_bestbuy_real_file_if_available(self):
        fixture=Path(__file__).resolve().parents[2]/'Best Buy Black Friday 2026 is Nov. 26–27.html'
        if not fixture.exists():self.skipTest('user-provided snapshot not bundled')
        s=a.Store();o,l=a.analyze_snapshot(fixture.read_text(encoding='utf-8'), 'https://www.bestbuy.com/black-friday',0,s)
        self.assertEqual(len(s.records()),131)
        self.assertEqual(sum(x['price_complete'] for x in s.records()),37)
        self.assertGreater(len(l),10)

if __name__=='__main__':unittest.main()
