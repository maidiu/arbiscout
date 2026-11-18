import json
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

    @staticmethod
    def dell_snapshot(products):
        payload = json.dumps(products).replace('"', r'\u0022')
        return f'<script>ProductsDetailInfo = JSON.parse("{payload}");</script>'

    def test_dell_embedded_json_prices_and_identity(self):
        products = {
            "a": {"productId": "a", "title": "XPS 13 Laptop",
                  "pdUrl": "https://www.dell.com/en-us/shop/laptop-computers/spd/xps/a",
                  "dellPrice": "$749.99", "marketPrice": "$999.99",
                  "variantCode": "XPS13", "snpStockStatus": 0},
            "b": {"productId": "b", "title": "New Dell 14S Laptop",
                  "pdUrl": "https://www.dell.com/en-us/shop/laptop-computers/spd/dell14s/b",
                  "dellPrice": "$749.99", "marketPrice": None,
                  "variantCode": "DELL14S", "snpStockStatus": 0},
            "c": {"productId": "c", "title": "Dell 16 Laptop",
                  "pdUrl": "https://www.dell.com/en-us/shop/laptop-computers/spd/dell16/c",
                  "dellPrice": "$649.99", "marketPrice": "$599.99",
                  "variantCode": "DELL16", "snpStockStatus": 1},
            "missing": {"title": "No URL", "dellPrice": "$10.00"},
        }
        raw, url, message = providers.dell_products_from_html(self.dell_snapshot(products))
        self.assertEqual(len(raw), 3)
        self.assertIn("3 embedded offer", message)
        by_sku = {row["sku"]: row for row in raw}
        self.assertEqual(by_sku["a"]["current"], 749.99)
        self.assertEqual(by_sku["a"]["regular"], 999.99)
        self.assertEqual(by_sku["a"]["category"], "Laptops")
        self.assertIsNone(by_sku["b"]["regular"])
        self.assertIsNone(by_sku["c"]["regular"])
        self.assertEqual(by_sku["c"]["stock_status"], 1)
        self.assertTrue(by_sku["a"]["market_price_reference"])

    def test_dell_model_code_extraction(self):
        self.assertEqual(providers.dell_model("Dell16LaptopDC16255"), "DC16255")
        self.assertEqual(providers.dell_model("XPS13DX13260"), "DX13260")
        self.assertEqual(providers.dell_model("Dell14SDS14270"), "DS14270")
        self.assertEqual(providers.dell_model("XPS13"), "XPS13")

    @staticmethod
    def lego_snapshot(apollo):
        payload = json.dumps({"props": {"pageProps": {"__APOLLO_STATE__": apollo}}})
        return f'<script id="__NEXT_DATA__" type="application/json">{payload}</script>'

    def test_lego_embedded_json_prices_and_set_identity(self):
        apollo = {
            "SingleVariantProduct:76470": {
                "productCode": "76470", "name": "Enchanted Flying Ford Anglia",
                "pdpPath": "/en-us/product/enchanted-flying-ford-anglia-76470",
                "variant": {"__ref": "ProductVariant:1"},
            },
            "ProductVariant:1": {
                "sku": "6588716", "salePercentage": 20,
                "price": {"formattedValue": 63.99},
                "listPrice": {"formattedValue": 79.99},
                "attributes": {"availabilityStatus": "E_AVAILABLE", "onSale": True},
            },
            "SingleVariantProduct:42209": {
                "productCode": "42209", "name": "Volvo L120 Electric Wheel Loader",
                "pdpPath": "/en-us/product/volvo-l120-electric-wheel-loader-42209",
                "variant": {"__ref": "ProductVariant:2"},
            },
            "ProductVariant:2": {
                "sku": "6526825", "salePercentage": 30,
                "price": {"centAmount": 8399},
                "listPrice": {"centAmount": 8399},
                "attributes": {"availabilityStatus": "E_AVAILABLE", "onSale": True},
            },
        }
        raw, _, message = providers.lego_products_from_html(self.lego_snapshot(apollo))
        self.assertEqual(len(raw), 2)
        self.assertIn("2 set", message)
        by_set = {row["set_number"]: row for row in raw}
        self.assertEqual(by_set["76470"]["current"], 63.99)
        self.assertEqual(by_set["76470"]["regular"], 79.99)
        self.assertEqual(by_set["76470"]["model"], "76470")
        self.assertEqual(by_set["76470"]["variant_sku"], "6588716")
        self.assertEqual(by_set["76470"]["category"], "Toys & Games")
        self.assertEqual(by_set["42209"]["current"], 83.99)
        self.assertIsNone(by_set["42209"]["regular"])

    def test_lego_parser_rejects_missing_payload(self):
        with self.assertRaises(RuntimeError):
            providers.lego_products_from_html("<html>no data</html>")

    def test_dell_parser_rejects_missing_payload(self):
        with self.assertRaises(RuntimeError):
            providers.dell_products_from_html("<html>no offers</html>")

    def test_dell_records_keep_current_only_rows(self):
        raw, _, _ = providers.dell_products_from_html(self.dell_snapshot({
            "a": {"productId": "a", "title": "Dell 16 Laptop",
                  "pdUrl": "https://www.dell.com/en-us/shop/laptop-computers/spd/dell16/a",
                  "dellPrice": "$649.99", "marketPrice": None},
        }))
        records = providers.build_records(raw)
        self.assertEqual(len(records), 1)
        self.assertFalse(records[0]["price_complete"])
        self.assertEqual(records[0]["current_price"], 649.99)
        self.assertIsNone(records[0]["regular_price"])


if __name__ == "__main__":
    unittest.main()
