import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ebay_watcher
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
        payload["listings"][0]["retailer_id"] = "r"
        payload["listings"][1]["retailer_id"] = "r"
        verdicts = llm_refine.normalize_verdicts(payload, {("r", "1"), ("r", "2")})
        self.assertEqual(verdicts[("r", "1")]["verdict"], "EXACT_MATCH")
        self.assertEqual(verdicts[("r", "1")]["confidence"], 1.0)
        self.assertEqual(verdicts[("r", "2")]["verdict"], "UNKNOWN")
        self.assertNotIn(("r", "999"), verdicts)

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
            {"retailer_id": "dell:dc16255", "item_id": "1", "verdict": "EXACT_MATCH", "confidence": 0.95},
            {"retailer_id": "dell:dc16255", "item_id": "2", "verdict": "WRONG_CONFIG", "confidence": 0.95},
            {"retailer_id": "dell:dc16255", "item_id": "3", "verdict": "EXACT_MATCH", "confidence": 0.95},
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
            self.assertTrue(refined[0]["llm_checked"])
            self.assertTrue((root / "comparisons" / "llm_verdicts.json").is_file())
            self.assertTrue((root / "comparisons" / "comparisons_raw.json").is_file())

    def test_results_state_exposes_llm_checked_and_post_llm_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "comparisons").mkdir()
            product = {"key": "dell:dc16255", "title": "Dell 16 Laptop",
                       "url": "https://www.dell.com/en-us/shop/laptop-computers/spd/xps/dc16255",
                       "current_price": 649.99, "regular_price": 1099.99}
            record = {
                "retailer": product, "ebay_search_url": "https://www.ebay.com/sch/i.html",
                "ebay_status": "LLM_REFINED", "fixture_index": 1, "fixture_file": "01.html",
                "llm_checked": True,
                "llm_refinement": {"exact": 2, "removed": 1, "unknown": 0},
                "comparison": {"status": "INSUFFICIENT_VERIFIED_SALES",
                               "sample_count": 2, "historical_median": 100.0,
                               "gap": 10.0, "diagnostics": {}},
            }
            (root / "comparisons" / "comparisons.json").write_text(json.dumps([record]))
            state = ebay_watcher.load_state(root)
            candidate = state["candidates"][0]
            self.assertTrue(candidate["llm_checked"])
            self.assertIn("2 exact", candidate["llm_summary"])
            self.assertIn("1 removed", candidate["llm_summary"])
            self.assertIn("median $100.00", candidate["llm_summary"])
            self.assertIn("gap $10.00", candidate["llm_summary"])

    def test_multiple_retailers_are_sent_in_one_compact_job(self):
        now = datetime.now(timezone.utc).isoformat()
        products = [
            {"key": "dell:dc16255", "title": "Dell 16 Laptop", "model": "DC16255",
             "brand": "Dell", "condition": "New", "current_price": 649.99,
             "regular_price": 1099.99, "ebay_query": "Dell DC16255",
             "url": "https://www.dell.com/en-us/shop/laptop-computers/spd/dell16/dc16255"},
            {"key": "lego:76470", "title": "Enchanted Flying Ford Anglia", "model": "76470",
             "brand": "LEGO", "condition": "New", "current_price": 63.99,
             "regular_price": 79.99, "ebay_query": "LEGO 76470",
             "url": "https://www.lego.com/en-us/product/enchanted-flying-ford-anglia-76470"},
        ]
        observations = [
            {"item_id": "d1", "retailer_key": "dell:dc16255",
             "title": "Dell 16 DC16255 16GB 512GB", "sold_at": now,
             "displayed_price": 600.0, "paid_price": 600.0,
             "price_status": "DISPLAYED_SOLD", "item_url": "https://www.ebay.com/itm/d1"},
            {"item_id": "l1", "retailer_key": "lego:76470",
             "title": "LEGO 76470 Enchanted Flying Ford Anglia New", "sold_at": now,
             "displayed_price": 70.0, "paid_price": 70.0,
             "price_status": "DISPLAYED_SOLD", "item_url": "https://www.ebay.com/itm/l1"},
        ]
        receipt = {"as_of_utc": now, "synthetic_demo": False, "selected_retail_offers": 2,
                   "positive_provisional_count": 0, "top_ten_count": 0,
                   "actual_paid_verified_count": 0, "source_mode": "SAVED_EBAY_HTML"}
        calls = []
        def fake_call(base_url, api_key, model, retailers):
            calls.append(retailers)
            return {"listings": [
                {"retailer_id": "dell:dc16255", "item_id": "d1",
                 "verdict": "EXACT_MATCH", "confidence": 0.95},
                {"retailer_id": "lego:76470", "item_id": "l1",
                 "verdict": "EXACT_MATCH", "confidence": 0.95},
            ]}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "comparisons").mkdir()
            (root / "selection.json").write_text(json.dumps({"products": products}))
            (root / "run_receipt.json").write_text(json.dumps(receipt))
            (root / "comparisons" / "sold_observations.json").write_text(json.dumps(observations))
            (root / "comparisons" / "comparisons.json").write_text(json.dumps([]))
            with patch("llm_refine.call_llm", side_effect=fake_call):
                summary = llm_refine.refine(root, "test-model", "http://test", "key",
                                            min_confidence=0.8)
            self.assertEqual(summary["jobs"], 1)
            self.assertEqual(len(calls), 1)
            self.assertEqual(len(calls[0]), 2)
            sent = json.dumps(calls[0])
            self.assertNotIn("displayed_price", sent)
            self.assertNotIn("sold_at", sent)
            self.assertNotIn("item_url", sent)
            self.assertIn("retailer_id", sent)
            self.assertEqual(summary["exact"], 2)


if __name__ == "__main__":
    unittest.main()
