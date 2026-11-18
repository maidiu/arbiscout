import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import llm_refine


class LLMRefineTests(unittest.TestCase):
    def test_parse_and_normalize_strict_verdicts(self):
        content = '''```json
        {"listings":[
          {"item_id":"1","verdict":"exact_match","confidence":1.4,"reason":"same"},
          {"item_id":"2","verdict":"NOT_A_VERDICT","confidence":"bad"},
          {"item_id":"999","verdict":"EXACT_MATCH","confidence":0.9}
        ]}
        ```'''
        payload = llm_refine.parse_llm_content(content)
        verdicts = llm_refine.normalize_verdicts(payload, {"1", "2"})
        self.assertEqual(verdicts["1"]["verdict"], "EXACT_MATCH")
        self.assertEqual(verdicts["1"]["confidence"], 1.0)
        self.assertEqual(verdicts["2"]["verdict"], "UNKNOWN")
        self.assertNotIn("999", verdicts)

    def test_refine_filters_wrong_config_and_used(self):
        now = datetime.now(timezone.utc).isoformat()
        product = {
            "key": "dell:dc16255", "title": "Dell 16 Laptop", "model": "DC16255",
            "brand": "Dell", "condition": "New", "category": "Laptops",
            "current_price": 649.99, "regular_price": 1099.99,
            "ebay_query": "Dell DC16255",
            "url": "https://www.dell.com/en-us/shop/laptop-computers/spd/xps/dc16255",
        }
        observations = [
            {"item_id": "1", "retailer_key": "dell:dc16255",
             "title": "Dell 16 DC16255 16GB 512GB Laptop", "sold_at": now,
             "displayed_price": 600.0, "paid_price": 600.0,
             "price_status": "DISPLAYED_SOLD", "item_url": "https://www.ebay.com/itm/1"},
            {"item_id": "2", "retailer_key": "dell:dc16255",
             "title": "Dell 16 DC16255 32GB 2TB Laptop", "sold_at": now,
             "displayed_price": 900.0, "paid_price": 900.0,
             "price_status": "DISPLAYED_SOLD", "item_url": "https://www.ebay.com/itm/2"},
            {"item_id": "3", "retailer_key": "dell:dc16255",
             "title": "Dell 16 DC16255 16GB 512GB Used", "sold_at": now,
             "displayed_price": 500.0, "paid_price": 500.0,
             "price_status": "DISPLAYED_SOLD", "item_url": "https://www.ebay.com/itm/3"},
        ]
        receipt = {
            "as_of_utc": now, "synthetic_demo": False, "selected_retail_offers": 1,
            "positive_provisional_count": 0, "top_ten_count": 0,
            "actual_paid_verified_count": 0, "source_mode": "SAVED_EBAY_HTML",
        }
        fake = {"listings": [
            {"item_id": "1", "verdict": "EXACT_MATCH", "confidence": 0.95},
            {"item_id": "2", "verdict": "WRONG_CONFIG", "confidence": 0.95},
            {"item_id": "3", "verdict": "EXACT_MATCH", "confidence": 0.95},
        ]}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "comparisons").mkdir()
            (root / "selection.json").write_text(json.dumps({"products": [product]}))
            (root / "run_receipt.json").write_text(json.dumps(receipt))
            (root / "comparisons" / "sold_observations.json").write_text(json.dumps(observations))
            (root / "comparisons" / "comparisons.json").write_text(json.dumps([
                {"retailer": product, "ebay_search_url": "https://www.ebay.com/sch/i.html",
                 "ebay_status": "PARSED", "fixture_index": 1, "fixture_file": "01.html",
                 "comparison": {"status": "INSUFFICIENT_VERIFIED_SALES", "diagnostics": {}}}
            ]))
            with patch("llm_refine.call_llm", return_value=fake):
                summary = llm_refine.refine(root, "test-model", "http://test", "key",
                                            min_confidence=0.8)
            self.assertEqual(summary["listings"], 3)
            self.assertEqual(summary["exact"], 1)
            self.assertEqual(summary["removed"], 2)
            refined = json.loads((root / "comparisons" / "comparisons.json").read_text())
            self.assertEqual(refined[0]["comparison"]["diagnostics"]["llm_exact"], 1)
            self.assertEqual(refined[0]["comparison"]["diagnostics"]["llm_removed"], 2)
            self.assertTrue((root / "comparisons" / "llm_verdicts.json").is_file())
            self.assertTrue((root / "comparisons" / "comparisons_raw.json").is_file())


if __name__ == "__main__":
    unittest.main()
