# Acceptance matrix — purchase-price-gap index only

| ID | Evidence needed for PASS | False-positive / rejection test | State |
|---|---|---|---|
| A01 | Relevant retailer offer feed/source and compatible use rights | Unapproved source, expired cache, unsupported retention | OPEN |
| A02 | Exact current total RETAIL PURCHASE price, link, timestamp, seller, region and actual availability | Expired coupon, local-only, wrong seller, no stock | OPEN |
| A03 | Product identity proves exact same GTIN/model/bundle/condition/quantity for retailer and eBay history | Similar model, wrong size, refurbished vs new, bundle mismatch | DRAFT IDENTITY + SIZE/CAPACITY GATES (fixture-tested) |
| A04 | eBay historical regular completed-sale price data with valid actual-sales window, sample, exclusions and rights | Asking price, zero sales, incomparable offer, outlier-dominated sample | BLOCKED LIVE DATA; USER-SAVED PAGES PROVISIONAL |
| A05 | Robust regular historical price estimate, dispersion and conservative quantile with enough valid observations | Median of 1 item, unknown accepted-offer, stale window | PROTOTYPE_DRAFT (low/high/mean/median/IQR; fixture + saved-page tested) |
| A06 | Accurate absolute and relative RETAIL PURCHASE PRICE GAP below eBay historical regular completed-sale reference | Negative gap, arithmetic mistakes, unsupported tax/shipping assumption | PROTOTYPE_DRAFT (gross gap only; fees/shipping excluded) |
| A07 | Purchase condition scoring ranks MAXIMUM RELIABLE gap with source strength and refusal behavior; returns 0–10 | Invented sale evidence, price gap justified by wrong variant, padding top 10 | PROTOTYPE_DRAFT (provisional top-10; no actual-paid verification) |
| A08 | For imports when supported: actual delivered acquisition price, MOQ, freight, currency, lead-time evidence | Misstated delivered price or noncomparable product | OPTIONAL |
| A09 | Daily scheduling, idempotence, error state and freshness of permitted sources | No data, quota failure, duplicate, outdated result | NOT_STARTED |
| A10 | First real retailer price + same-item historical eBay reference → quantified purchase gap → human index report | Independent recheck of offer and original sales observations | BLOCKED LIVE |
| A11 | Repeated accuracy measurement: observed offer still current, historical baseline credible, false alerts counted | Stale prices, unverifiable stock, repeated false discount | NOT_STARTED |
| A12 | Security and exact code SHA, tests, source permissions and independently reviewable receipts | Secret leak, fixture presented as live, unmerged PR advertised as accepted | IN_PROGRESS (no-secret `.env` guard; 21 tests; no independent review) |
| A13 | Provider API credentials scoped, local-only and absent from tracked files | Key leak, committed `.env`, broad OAuth scope | PROTOTYPE_DRAFT (local ignored `.env`; names-only example; no independent security review) |
| A14 | Category and source capacity assessed beyond food, with gross versus net distinction | Food-only assumption, gross gap presented as margin | PROTOTYPE_DRAFT (non-food probe; gross gap only; fees/shipping excluded) |
| A15 | Unified catalog filters by source/category and selects a reproducible top-N set | Source filter ignored, category mismatch, selection not preserved | PROTOTYPE_DRAFT (local merge test; no independent review) |

A successful mock does not establish live market evidence. Different statuses for source documented / permitted / executable / tested / independently accepted / deployed must be preserved. No subsequent transaction belongs to acceptance.
