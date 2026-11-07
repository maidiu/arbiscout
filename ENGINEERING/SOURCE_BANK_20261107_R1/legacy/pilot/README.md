# ArbiScout: scraper/feed acquisition pilot

**Purpose**: Proof-of-concept that extracts deal leads from RSS and permitted sale-category HTML. No accounts, API keys, eBay requests, anti-bot evasion, checkout automation, or purchases. No paid dependencies. Every extracted row is **unverified** until exact identity, availability and purchaser price have been established.

## Requirements
Python 3.10+; for HTML mode install free `beautifulsoup4`:

```sh
python3 -m pip install beautifulsoup4
```

## Run the fully offline fixtures first

```sh
python3 -m unittest -v test_discovery
python3 discovery.py --output sample_html.jsonl html-file --file example_sale_page.html --url https://example.com/clearance --config site_example.json
```

This sample HTML is invented purely for parser tests. No real retailer was contacted.

## Read one actual official deal feed (network, requires normal connectivity)

DealNews officially links its most-recent feed at `https://www.dealnews.com/?rss=1&sort=time` (source: https://www.dealnews.com/pages/rss.html). Ben's Bargains lists merchant/category feeds at https://bensbargains.com/rss-feeds/. Preserve original headlines/links and respect feed-use restrictions; RSS is *curated leads*, not a retailer clearance census.

```sh
python3 discovery.py --output dealnews.jsonl rss --url 'https://www.dealnews.com/?rss=1&sort=time'
```

For comparison, Slickdeals publishes a public frontpage RSS URL, but review its current feed use terms before scheduling a robot:

```sh
python3 discovery.py --output slickdeals.jsonl rss --url 'https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1'
```

Slickdeals' RSS is published and consumed by readers but its own terms and permitted automation scope should be reviewed before unattended scheduled collection. This example is an *ad hoc test*, not permission to republish its data.

## Scrape ONE *authorized* real sale-category site

Inspect the relevant site's terms, robots and applicable rights, then inspect its HTML source and edit `site_example.json` CSS selectors to the actual visible HTML. Run a 1-page trial:

```sh
python3 discovery.py --output retailer_sample.jsonl crawl --url 'https://approved-retailer.example/sale' --config site_example.json --max-pages 1 --delay 2 --i-verified-permission
```

This command will refuse on inaccessible/disallowing robots.txt, 403/429 HTTP errors, cross-site redirects, oversized responses and disallowed page paths. It does not solve CAPTCHAs or conceal its identity. The script performs only one category URL/pagination path, up to five pages, with a >=1.5s inter-page delay; it is **not** a universal merchant scraper. Page-specific consent/terms must be checked *in addition to robots.txt*.

## What the pilot deliberately does not do

- Decide from a title string that an item matches a historical eBay sold product.
- Claim that an RSS headline price is a direct retailer purchase price.
- Treat page MSRP as actual discounted purchaser total.
- Infer stock or taxes/shipping when not observed.
- Automatically bypass page challenges, logins or rate limits.
- Enumerate hidden clearance products, perform checkout, use LLM calls or produce resale ROI.

## Next engineering milestones

Integrate approved Woot API source, Meh JSON source and Kroger Products/Locations source **without committing secrets**; expand permitted per-retailer HTML discovery adapters; run one 20–50-real-offer source-specific pilot; then add a provider-verified eBay sold-price adapter and conservative exact-item matching.
