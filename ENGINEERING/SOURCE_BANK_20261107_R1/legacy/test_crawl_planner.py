import tempfile
import unittest
from pathlib import Path
from arbiscout_crawl_planner import Snapshot,read_snapshot,merge,link_type,priority

class SnapshotPlannerTest(unittest.TestCase):
  def setUp(self):
    self.html='''<html><main><h2>Deals</h2><a href="https://www.bestbuy.com/site/top-deals/top-100-deals-this-season/abc">Top 100</a>
      <div data-testid="product-card"><div data-testid="product-card-percent-off">40% off</div>
      <a data-testid="product-card-title-link" href="https://www.bestbuy.com/product/foobar/JJJ123/sku/12345">Gadget A</a>
      </div></main></html>'''
    self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)
    (self.p/'a.html').write_text(self.html)
    self.snapshot=Snapshot(self.p/'a.html','https://www.bestbuy.com/black-friday')
  def tearDown(self):self.tmp.cleanup()
  def test_missing_price_and_nav_found(self):
    prods,links=read_snapshot(self.snapshot)
    self.assertEqual(len(prods),1);self.assertEqual(prods[0]['current_price_usd'],None)
    self.assertEqual(prods[0]['sku'],'12345')
    self.assertEqual(len(links),1);self.assertEqual(links[0]['type'],'top_deals')
  def test_second_saved_listing_completes_price(self):
    path=self.p/'b.html'
    path.write_text('''<html><main><div data-testid="product-card"><a data-testid="product-card-title-link"
      href="https://www.bestbuy.com/product/foobar/JJJ123/sku/12345">Gadget A</a>
      <div data-testid="price-block-customer-price">$60.00</div><div data-testid="price-block-regular-price">$100.00</div></div></main></html>''')
    a,_=read_snapshot(self.snapshot)
    b,_=read_snapshot(Snapshot(path,'https://www.bestbuy.com/site/top-deals/top-100-deals-this-season/abc'))
    joined=merge(a+b)
    self.assertEqual(len(joined),1);self.assertEqual(joined[0]['current_price_usd'],'60.00');self.assertEqual(len(joined[0]['seen_on_pages']),2)
  def test_conflicting_skus_are_not_merged_into_price_truth(self):
    a,_=read_snapshot(self.snapshot)
    bad={**a[0], 'sku':'98765','current_price_usd':'20.00','previous_price_usd':'70.00'}
    j=merge(a+[bad])[0]
    self.assertTrue(j['variant_conflict']);self.assertIsNone(j['current_price_usd'])
  def test_link_type_rejects_external(self):
    self.assertIsNone(link_type('https://notbestbuy.example.com/site/top-deals/x'))
    self.assertEqual(link_type('https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=abc'),'filtered_deals')
  def test_price_priority(self):
    self.assertGreater(priority('https://www.bestbuy.com/site/top-deals/a','top_deals'),priority('https://www.bestbuy.com/site/promo/a','promotion'))

if __name__=='__main__':unittest.main()
