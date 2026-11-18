# Retailer source coverage

This folder imports the 2026-11-17 retailer expansion research and keeps the
54-case coverage honest.

- `mechanism_specifications.json` — machine-readable 54-source profiles.
- `OPEN_CODE_BUILD_DOSSIER.md` — the full implementation-grade research dossier.
- `SOURCE_LEDGER.csv` — audited evidence pointers.
- `coverage_ledger.json` / `coverage_ledger.md` — generated status for all 54.
- `receipts/` — source, paging, price-extraction and rights receipts for the
  adapters that are actually implemented locally.

## Statuses

- **IMPLEMENTED_LOCAL** — a local adapter exists and has been exercised. This
  does not certify live rights or production readiness.
- **HOLD_RIGHTS** — a documented site restriction or affiliate/terms conflict
  must be resolved before collection.
- **HOLD_APPROVED_FEED** — an approved partner/brand feed is required.
- **HOLD_TERMS** — terms/API permission review is required.
- **HOLD_NEEDS_CAPTURE** — no saved page capture; selectors, pagination and
  price roles are unverified.
- **HOLD_EVIDENCE** — the mechanism itself is not proven.

A HOLD is not a failed test. It means the app deliberately emits no products
for that source rather than inventing selectors, endpoints or prices.

## Adding a source

1. Obtain an authorized/local page-1 and page-2 capture (or an approved feed).
2. Record the canonical URL, locale/currency, selected ZIP/store, membership
   state and capture timestamp.
3. Inspect the settled HTML, JSON-LD or embedded offer state and write down the
   exact card, title, current-price, regular-price, variant, stock and
   pagination pointers.
4. Add a source adapter that emits the existing normalized `retailer/products.json`
   records; preserve `current_price`, `regular_price`, `condition`, `variant`,
   `source`, `category`, `observed_at` and ZIP/location where relevant.
5. Add fixtures and negative tests: price range without a variant, trade-in or
   member price not treated as unconditional, duplicate/cross-seller products,
   page 2, missing prices and zero-result behavior.
6. Write `SOURCE_RECEIPT`, `PAGING_RECEIPT`, `PRICE_EXTRACTION_RECEIPT` and
   `RIGHTS_RECEIPT`, then register the adapter in `source_registry.py`.
7. Run all app/control-room tests and re-check the coverage ledger.

Do not guess a private XHR endpoint, a CSS selector or an API path. A source
without a capture stays HOLD.
