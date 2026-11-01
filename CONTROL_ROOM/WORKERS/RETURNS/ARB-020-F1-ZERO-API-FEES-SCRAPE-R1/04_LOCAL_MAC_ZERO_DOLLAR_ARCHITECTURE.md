# ARB-020-F1 — Minimal $0 Mac-local scanner architecture

**Status 2026-10-31: design only.** No scanner installed on user's Mac and no external API calls/paid services. Must never enable a source without specific permitted-use and storage/retention scope.

## Source-neutral daily pipeline
```
ONLY APPROVED sources:
  Best Buy official Products/Categories API with key and scoped permission
  OR accepted Home Depot/Awin/CJ/Impact advertiser full feed
  OR named consenting WooCommerce merchant on_sale=true Store API
  OR individual merchant permitted HTML/JSON-LD
    → rate/expiry-checked fetch (no anti-bot evasion)
    → feed JSON/CSV/HTML parser
    → GTIN/MPN/model+revision+condition+bundle match
    → dedupe by merchant/SKU/condition/region/quantity/offer time
    → price, shipping, tax, stock, expiry and source URL validation
    → local SQLite staging with provider retention clock
    → separate ARB-010 permissioned eBay actual completed-sales price reference
    → ARB-051 median/p25/n and uncertainty
    → compare current obtainable purchaser total, refuse missing values
    → ARB-071 report of 0–10 truthful candidates or zero
```

## Mac-specific pieces
- Python 3.12+ venv, `urllib`/requests, built-in CSV/JSON, Decimal, SQLite. BeautifulSoup/lxml and Scrapy optional for **permissioned** HTML; Playwright only where a named merchant expressly permits automated browser access and standard HTML is insufficient.
- `launchd` User LaunchAgent schedule once daily; no external server. Assumes Mac awake/online. Log run timestamp, source rights status, item and refusal counts; do not invent a running scheduler.
- API keys in local Keychain/environment not public GitHub; source permit file holds source origin, method, exact grant scope, robots user-agent/path for HTML, rate/day, retention TTL, allowed derived display. Default disabled.
- Refuse 401/403/429/CAPTCHA instead of rotating identity/proxy or using hidden endpoints. No authorized retry beyond provider documented limits. Do not use source data after rights expiry.
- SQLite `offers` table stores allowed source URL, timestamp, SKU/GTIN, model, price/condition/stock/region, provenance and status; source raw content expires by contract. Network calls only through source adapter with explicit allowlisted path.
- Currency arithmetic via Decimal, unknown shipping/tax = null. Neither MSRP, loyalty rewards nor retailer offer history can become actual eBay sale prices. DeepSeek optional for ambiguous naming only, never upgrade unverifiable identity.

## Fixture-only normalized source record
```json
{
  "retailer_id": "EXAMPLE_APPROVED_SOURCE",
  "observed_at": "2026-10-31T16:00:00-04:00",
  "source_url": "https://example.invalid/product",
  "sku": "SYNTHETIC-001", "gtin": null,
  "model": "X-1", "condition": "NEW", "quantity": 1,
  "currency": "USD", "item_price": "59.99",
  "shipping": null, "tax": null, "purchase_total": null,
  "stock": "REPORTED_ONLY", "region": null,
  "is_sale": "PROVIDER_REPORTED",
  "merchant_confirmed": false, "identity_verified": false,
  "license_verified": false
}
```

## Non-running implementation pseudocode
```python
for s in configured_sources:
    if not s.grant_is_current() or s.monthly_fee > 0:
        continue
    for page in s.allowed_pages(max_pages=s.source_cap):
        # On any denied/challenged response: STOP, don't evade.
        response = s.fetch_permitted_path(page, min_interval=s.allowed_interval)
        if response.status in (401, 403, 429) or response.challenge:
            quarantine(s, response.status)
            break
        for r in s.parse(response):
            store_if_licensed(normalize_preserving_nulls(r))
for offer in deduplicate_and_filter():
    if not offer.identity_exact or not offer.current_total_verified:
        mark_hold(offer); continue
    if not qualified_actual_paid_ebay_reference(offer):
        mark_hold(offer); continue
    compute_and_report_observed_purchase_gap(offer)
```

## Three acquisition adapters, not installed
1. **Best Buy** official API's catalog enumeration, sale/regular price fields and UPC, never blocked internal website `/api/` paths. Publisher key and price-index authorization still HOLD; API cache ≤72h as documented.
2. **Merchant full CSV feed**: download only if advertiser-approved, preferably on source update manifest, parse mapped columns and avoid repeated browser page retrieval.
3. **WooCommerce named consenting store**: GET `/wp-json/wc/store/v1/products?on_sale=true&page=1&per_page=100`, stop at `X-WP-TotalPages`; minor-unit price conversion, GTIN may be missing. Site permission and robots still first.
4. **HTML JSON-LD** only on separately approved merchant: parse Product/Offer but do not infer sale/list price/available checkout where absent.

The source-free script ran 8/8 parser tests in a verified isolated container; this does not prove live retail access, Mac launchd operation, source permission, eBay transaction evidence, or price-gap output. The next bounded two-source 20–50-product canary is the deployment gate.
