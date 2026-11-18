from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import source_registry


class SourceRegistryTests(unittest.TestCase):
    def test_all_54_cases_present_and_unique(self):
        rows = source_registry.coverage_rows()
        self.assertEqual(len(rows), 54)
        self.assertEqual(len({r["id"] for r in rows}), 54)
        self.assertEqual(len({r["name"] for r in rows}), 54)

    def test_implemented_adapters(self):
        rows = source_registry.coverage_rows()
        implemented = {r["name"] for r in rows if r["status"] == "IMPLEMENTED_LOCAL"}
        self.assertEqual(implemented, {"Best Buy", "Woot", "Meh", "Kroger", "Dell new-product deals"})
        for row in rows:
            if row["status"] == "IMPLEMENTED_LOCAL":
                self.assertTrue(row["adapter"])
                self.assertTrue(row["receipt"])

    def test_holds_have_explicit_blockers(self):
        for row in source_registry.coverage_rows():
            self.assertFalse(row["production_ready"])
            if row["status"] != "IMPLEMENTED_LOCAL":
                self.assertTrue(row["blocker"])
                self.assertTrue(row["next_action"])
                self.assertIn(row["status"], source_registry.STATUS_ORDER)

    def test_no_unverified_selectors_on_holds(self):
        implemented = set(source_registry.IMPLEMENTED)
        for row in source_registry.load_rows():
            if row.get("id") not in implemented:
                self.assertFalse(row.get("concrete_css_selectors_verified", False))

    def test_coverage_ledger_and_receipts_exist(self):
        base = Path(__file__).resolve().parents[1] / "sources"
        ledger = base / "coverage_ledger.md"
        self.assertTrue(ledger.is_file())
        text = ledger.read_text(encoding="utf-8")
        for row in source_registry.coverage_rows():
            self.assertIn(row["id"], text)
        for source_id in source_registry.IMPLEMENTED:
            receipt = base / "receipts" / f"{source_id}.json"
            self.assertTrue(receipt.is_file())
            data = json.loads(receipt.read_text(encoding="utf-8"))
            for key in ("SOURCE_RECEIPT", "PAGING_RECEIPT",
                        "PRICE_EXTRACTION_RECEIPT", "RIGHTS_RECEIPT"):
                self.assertIn(key, data)

    def test_summary_counts(self):
        info = source_registry.summary()
        self.assertEqual(info["total"], 54)
        self.assertEqual(info["counts"].get("IMPLEMENTED_LOCAL"), 5)


if __name__ == "__main__":
    unittest.main()
