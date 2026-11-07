import unittest
from pathlib import Path
from unittest.mock import patch
from discovery import parse_rss,parse_cards,money,crawl,assert_robots_allowed
D=Path(__file__).parent
C=__import__('json').loads((D/'site_example.json').read_text())
class Tests(unittest.TestCase):
    def test_rss_count_and_link(self):
        rows=parse_rss((D/'example_feed.xml').read_bytes(),'https://example.com/feed')
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[0]['original_link'],'https://example.com/deal/1?ref=original')
        self.assertIsNone(rows[0]['merchant_verified_price_usd'])
    def test_feed_price_only_hint(self):
        rows=parse_rss((D/'example_feed.xml').read_bytes(),'https://example.com/feed')
        self.assertEqual(rows[0]['price_hint_from_title_usd'],79.99)
        self.assertIsNone(rows[1]['price_hint_from_title_usd'])
    def test_html_markup(self):
        rows,nxt=parse_cards((D/'example_sale_page.html').read_text(),'https://example.com/clearance',C)
        self.assertEqual(len(rows),2);self.assertEqual(nxt,'https://example.com/clearance?page=2')
        self.assertEqual(rows[0]['mpn'],'DRILL-111')
        self.assertEqual(rows[0]['price_hint_from_page_usd'],119.95)
        self.assertTrue(rows[0]['verified_markdown_on_page'])
    def test_missing_regular_not_markdown(self):
        rows,_=parse_cards((D/'example_sale_page.html').read_text(),'https://example.com/clearance',C)
        self.assertFalse(rows[1]['verified_markdown_on_page'])
    def test_no_checkout_or_ebay_claim(self):
        rows,_=parse_cards((D/'example_sale_page.html').read_text(),'https://example.com/clearance',C)
        self.assertFalse(rows[0]['suitable_for_ebay_match']);self.assertIsNone(rows[0]['merchant_verified_price_usd'])
    def test_untrusted_script_or_external_link(self):
        html='<article class="product"><h3>X</h3><a class="product-link" href="javascript:alert(1)"></a><b class="sale-price">$50</b></article>'
        rows,_=parse_cards(html,'https://example.com/',C)
        self.assertEqual(rows,[])
    def test_price(self):
        self.assertEqual(money('From $1,299.00 shipped'),1299.0)
        self.assertIsNone(money('Save 30%'))
    def test_robots_refusal(self):
        with patch('discovery.fetch', return_value=b'User-agent: *\nDisallow: /clearance'):
            with self.assertRaises(RuntimeError):
                assert_robots_allowed('https://example.com/clearance')
    def test_robots_missing_refusal(self):
        with patch('discovery.fetch',side_effect=Exception('network')):
            with self.assertRaises(RuntimeError):
                assert_robots_allowed('https://example.com/clearance')
    def test_max_page_bound(self):
        with patch('discovery.assert_robots_allowed',return_value=None), patch('discovery.fetch',return_value=(D/'example_sale_page.html').read_bytes()):
            out=crawl('https://example.com/clearance',C,1,1.5)
            self.assertEqual(len(out),2)
if __name__=='__main__':unittest.main()
