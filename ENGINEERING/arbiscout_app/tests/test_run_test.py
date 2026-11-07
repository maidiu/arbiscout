import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_test


class FullTwentyToTenTests(unittest.TestCase):
    def test_rank_refuses_unknown_and_negative(self):
        def row(name, gap, status="PROVISIONAL_SOLD_DISPLAY_COMPARISON"):
            return {
                "retailer": {"key": name, "title": name,
                             "url": "https://shop.example.com/" + name,
                             "current_price": 50, "regular_price": 100},
                "ebay_search_url": "https://www.ebay.com/sch/i.html",
                "comparison": {"status": status, "gap": gap, "historical_median": 110,
                               "gap_percent": 40, "sample_count": 3},
            }
        data = [row("better", 70), row("worse", 60), row("negative", -5),
                row("unknown", None, "INSUFFICIENT_VERIFIED_SALES")]
        out = run_test.rank_provisional(data)
        self.assertEqual([r["retailer_key"] for r in out], ["better", "worse"])
        self.assertTrue(all("NOT_ACTUAL_PAID" in r["evidence_status"] for r in out))

    def test_twenty_product_fictional_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = run_test.execute(
                demo=True, output=root,
                as_of=datetime(2026, 11, 7, 12, tzinfo=timezone.utc))
            self.assertEqual(result["selected_retail_offers"], 20)
            self.assertEqual(result["positive_provisional_count"], 20)
            self.assertEqual(result["top_ten_count"], 10)
            self.assertEqual(result["actual_paid_verified_count"], 0)
            self.assertEqual(result["source_status_counts"], {"PARSED": 20})
            top = json.loads((root / "top10.json").read_text())
            self.assertEqual(len(top), 10)
            self.assertGreater(top[0]["indicative_gap_dollars"],
                               top[-1]["indicative_gap_dollars"])
            self.assertTrue((root / "top10.csv").exists())
            self.assertTrue((root / "comparisons" / "sold_observations.json").exists())
            self.assertIn("SYNTHETIC", (root / "index.html").read_text())
            self.assertTrue((root / "synthetic_input" / "NOTICE.txt").exists())

    def test_real_saved_retailer_without_ebay_returns_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture = Path(__file__).resolve().parents[1] / "sample" / "sample_deals.html"
            result = run_test.execute(
                snapshot=fixture, url="https://shop.example.com/sale", output=root,
                as_of=datetime(2026, 11, 7, 12, tzinfo=timezone.utc))
            self.assertEqual(result["top_ten_count"], 0)
            self.assertEqual(result["positive_provisional_count"], 0)
            self.assertEqual(json.loads((root / "top10.json").read_text()), [])

    def test_live_and_saved_ebay_are_mutually_exclusive(self):
        with self.assertRaises(ValueError):
            run_test.execute(snapshot="absent.html", ebay_pages="x", ebay_live=True)


if __name__ == "__main__":
    unittest.main()
