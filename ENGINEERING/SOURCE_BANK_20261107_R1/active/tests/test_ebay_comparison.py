import json
from datetime import datetime,timezone
from pathlib import Path
import sys,tempfile,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import ebay_comparison as e

RETAIL={'key':'bestbuy:123','title':'Sony WH-1000XM5 Wireless Noise Canceling Headphones - Black',
        'url':'https://www.bestbuy.com/product/x/123','current_price':199.99,'regular_price':399.99,
        'discount_percent':50.0,'savings':200.0,'price_conflict':False,'variant_conflict':False}

def sold_card(id,title,dt,price,extra=''):
    return f'<li class="s-item"><a class="s-item__link" href="https://www.ebay.com/itm/{id}"><h3 class="s-item__title">{title}</h3></a><span class="s-item__price">${price}</span><span class="s-item__ended-date">Sold {dt}</span><span>{extra}</span></li>'

class EBayEvidenceTests(unittest.TestCase):
    def test_filters_dates_price_and_best_offer(self):
        page=''.join([sold_card('111111111111',RETAIL['title'],'Nov 06, 2026','310.00'),
                      sold_card('222222222222',RETAIL['title'],'Nov 03, 2026','315.00'),
                      sold_card('333333333333',RETAIL['title'],'Oct 31, 2026','320.00'),
                      sold_card('444444444444',RETAIL['title'],'Oct 01, 2026','999.00'),
                      sold_card('555555555555',RETAIL['title'],'Nov 02, 2026','450.00','Best offer accepted'),
                      sold_card('666666666666','Sony WH-1000XM4 headphones','Nov 01, 2026','100.00')])
        obs,status=e.parse_ebay_sold_html(page,e.search_url('Sony'))
        self.assertEqual((len(obs),status),(6,'PARSED'))
        r=e.qualify(RETAIL,obs,datetime(2026,11,7,tzinfo=timezone.utc))
        self.assertEqual(r['historical_median'],315.0)
        self.assertEqual(r['sample_count'],3)
        self.assertAlmostEqual(r['gap'],115.01)
        self.assertEqual(r['diagnostics']['unknown_best_offer'],1)
    def test_no_dates_is_not_thirty_day_evidence(self):
        obs,status=e.parse_ebay_sold_html(sold_card('111111111111',RETAIL['title'],'','350.00'),'https://www.ebay.com/sch/i.html')
        self.assertEqual(e.qualify(RETAIL,obs,datetime(2026,11,7,tzinfo=timezone.utc))['status'],'INSUFFICIENT_VERIFIED_SALES')
    def test_no_model_token_is_hold(self):
        bad={**RETAIL,'title':'Generic Headphones with No Model'}
        self.assertFalse(e.model_match(bad,RETAIL['title'])[0])
    def test_only_retail_complete_top20(self):
        goods=[{**RETAIL,'current_price':None,'discount_percent':99},RETAIL]
        self.assertEqual(len(e.choose_deals(goods)),1)
    def test_end_to_end_fixture_ranking(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);(p/'retail.json').write_text(json.dumps([RETAIL]));(p/'fixtures').mkdir()
            (p/'fixtures'/'01.html').write_text(''.join(sold_card(str(100000000000+i),RETAIL['title'],'Nov 06, 2026','300.00') for i in range(3)))
            rows=e.compare_top20(p/'retail.json',p/'out',top=1,fixture_dir=p/'fixtures',as_of=datetime(2026,11,7,tzinfo=timezone.utc))
            self.assertEqual(rows[0]['comparison']['sample_count'],3)
            self.assertTrue((p/'out'/'index.html').exists())
            self.assertEqual(rows[0]['comparison']['gap'],100.01)
            self.assertIn('eBay sold',(p/'out'/'index.html').read_text())
    def test_no_fixture_produces_unranked_not_faked(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);(p/'retail.json').write_text(json.dumps([RETAIL]));(p/'empty').mkdir()
            rows=e.compare_top20(p/'retail.json',p/'out',fixture_dir=p/'empty')
            self.assertIsNone(rows[0]['comparison']['gap'])
            self.assertEqual(rows[0]['ebay_status'],'NO_FIXTURE_FOR_PRODUCT')
if __name__=='__main__':unittest.main()
