import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_catalog
import catalog_ui


class CatalogTests(unittest.TestCase):
    def test_category_inference(self):
        self.assertEqual(catalog_ui.infer_category({"title": 'Samsung 65" OLED 4K Smart TV'}), "TV & Home Theater")
        self.assertEqual(catalog_ui.infer_category({"title": "ASUS Vivobook Laptop"}), "Computers & Tablets")
        self.assertEqual(catalog_ui.infer_category({"title": "Kroger 2% Reduced Fat Milk"}), "Grocery & Household")

    def test_filter_source_category_sort_top(self):
        products = [
            {"source": "Woot", "category": "Home & Outdoor", "title": "A",
             "discount_percent": 50, "savings": 10, "current_price": 10, "regular_price": 20},
            {"source": "Best Buy", "category": "TV & Home Theater", "title": "B",
             "discount_percent": 20, "savings": 100, "current_price": 400, "regular_price": 500},
            {"source": "Woot", "category": "Computers & Tablets", "title": "C",
             "discount_percent": 70, "savings": 5, "current_price": 3, "regular_price": 10},
        ]
        rows = catalog_ui.filter_sort(products, sources=["Woot"], sort="discount", top=1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "C")
        rows = catalog_ui.filter_sort(products, sources=["Best Buy", "Woot"],
                                      categories=["Home & Outdoor"], sort="discount")
        self.assertEqual([r["title"] for r in rows], ["A"])

    def test_build_catalog_merges_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sources = {
                "Best_Buy": {"key": "bb1", "title": "TV",
                             "url": "https://www.bestbuy.com/product/x/1",
                             "current_price": 100, "regular_price": 200,
                             "discount_percent": 50, "savings": 100},
                "Woot": {"key": "w1", "title": "Laptop",
                         "url": "https://www.woot.com/offers/x",
                         "current_price": 50, "regular_price": 100,
                         "discount_percent": 50, "savings": 50},
            }
            for folder_name, product in sources.items():
                folder = root / folder_name / "retailer"
                folder.mkdir(parents=True)
                (folder / "products.json").write_text(json.dumps([product]), encoding="utf-8")
            payload = build_catalog.build(
                [("Best Buy", str(root / "Best_Buy")), ("Woot", str(root / "Woot"))],
                root / "catalog", 100)
            self.assertEqual(len(payload["products"]), 2)
            self.assertEqual(set(payload["sources"]), {"Best Buy", "Woot"})
            self.assertTrue((root / "catalog" / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
