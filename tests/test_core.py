"""Boundary tests: false positives should fail closed."""

import copy
import json
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arbiscout.core import adjudicate, dec, rank  # noqa: E402

DATA = json.loads((Path(__file__).resolve().parents[1] / "examples" / "synthetic_candidates.json").read_text())
AS_OF = date(2026, 10, 21)


class CoreTests(unittest.TestCase):
    def candidate(self):
        return copy.deepcopy(DATA["candidates"][0])

    def assess(self, candidate):
        return adjudicate(candidate, DATA["assumptions"], AS_OF)

    def test_exact_synthetic_fixture_passes(self):
        out = self.assess(self.candidate())
        self.assertEqual(out["status"], "ELIGIBLE_VERIFY_BEFORE_BUYING")
        self.assertEqual(out["estimates"]["profit"], "15.38")
        self.assertEqual(out["estimates"]["roi_pct"], "71.86")

    def test_zero_sales_is_not_a_deal(self):
        out = self.assess(DATA["candidates"][1])
        self.assertEqual(out["status"], "REVIEW")
        self.assertIn("insufficient completed-sales count", out["reasons"])

    def test_variant_mismatch_is_not_a_deal(self):
        out = self.assess(DATA["candidates"][2])
        self.assertTrue(any("model mismatch" in s for s in out["reasons"]))

    def test_gtin_mismatch_rejects_even_when_names_match(self):
        data = self.candidate()
        data["market"]["identity"]["gtin"] = "9999999999999"
        self.assertIn("product gtin mismatch", self.assess(data)["reasons"])

    def test_stale_observation_fails(self):
        data = self.candidate()
        data["market"]["observed_on"] = "2026-09-01"
        self.assertTrue(any("stale" in r for r in self.assess(data)["reasons"]))

    def test_future_observation_fails(self):
        data = self.candidate()
        data["retail"]["observed_on"] = "2026-10-22"
        self.assertTrue(any("future" in r for r in self.assess(data)["reasons"]))

    def test_active_only_does_not_fake_sales(self):
        data = self.candidate()
        data["market"]["source_type"] = "active_listings"
        self.assertIn("no verified completed-sales data source", self.assess(data)["reasons"])

    def test_unavailable_stock_fails(self):
        data = self.candidate()
        data["retail"]["in_stock"] = False
        self.assertIn("retail availability unconfirmed", self.assess(data)["reasons"])

    def test_missing_price_fails_closed(self):
        data = self.candidate()
        del data["market"]["sold_price_estimate"]
        self.assertEqual(self.assess(data)["status"], "REVIEW")

    def test_negative_and_nan_not_allowed(self):
        for value in ("-1", "NaN", "Infinity", None, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    dec(value, "price")

    def test_tax_and_shipping_reduce_profit(self):
        baseline = self.assess(self.candidate())
        data = self.candidate()
        data["retail"]["shipping_cost"] = "4.00"
        actual = self.assess(data)
        self.assertLess(float(actual["estimates"]["profit"]), float(baseline["estimates"]["profit"]))

    def test_price_below_profit_threshold_does_not_pass(self):
        data = self.candidate()
        data["market"]["sold_price_estimate"] = "28"
        self.assertIn("below minimum estimated profit", self.assess(data)["reasons"])

    def test_output_has_all_three_and_only_one_eligible(self):
        results = rank(DATA["candidates"], DATA["assumptions"], AS_OF)
        self.assertEqual(len(results), 3)
        self.assertEqual(sum(r["status"].startswith("ELIGIBLE") for r in results), 1)
        self.assertEqual(results[0]["id"], "fixture-clear-001")


if __name__ == "__main__":
    unittest.main()
