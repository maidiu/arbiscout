from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import providers


class ProviderHelperTests(unittest.TestCase):
    def test_woot_price_shapes(self):
        self.assertEqual(providers.woot_price({"Minimum": 10, "Maximum": 20}), 10)
        self.assertEqual(providers.woot_price(15.5), 15.5)
        self.assertIsNone(providers.woot_price(None))

    def test_woot_category_mapping(self):
        self.assertEqual(providers.woot_category(["PC"]), "Computers & Tablets")
        self.assertEqual(providers.woot_category(["SHIRT"]), "Apparel")
        self.assertIsNone(providers.woot_category(["WOOT"]))


if __name__ == "__main__":
    unittest.main()
