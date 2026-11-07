# Best Buy saved-HTML extractor — ArbiScout diagnostic

This is an **offline parser for a page you manually saved in Chrome**. It makes **no network requests** and does not scan Best Buy for new offers.

## Requirements

```bash
python3 -m pip install beautifulsoup4 lxml
```

## Run it

Put `bestbuy_saved_html.py` and the saved `.html` file in the same directory:

```bash
python3 bestbuy_saved_html.py \
  --file 'Best Buy Black Friday 2026 is Nov. 26–27.html' \
  --output bestbuy_deals.jsonl
```

Each JSONL line represents one distinct Best Buy **product ID** with the fields `title`, `url`, `sku` (if present), `price_usd`, `previous_price_usd`, `advertised_discount_percent`, `price_complete`, and `card_occurrences`.

## Test result on the uploaded page

- 152 product cards in the local HTML
- 131 unique products after 21 duplicate cards
- 37 unique products have both current price and previous price
- 94 unique products have missing current/previous price; they are retained with null fields
- 8 extraction sanity assertions passed

Important: Best Buy's previous-price figure is **not eBay's actual historical sold price**, and prices in a saved snapshot are **not a current checkout quote**. Stock, exact model/UPC, bundles, shipping and taxes require separate verification. The output should be treated as candidate discovery only.

For the 94 missing prices, inspect browser rendering/data hydration or pursue a permitted official data source. Don't infer price from percentage-off labels or claim a live, unattended scraper has been tested.
