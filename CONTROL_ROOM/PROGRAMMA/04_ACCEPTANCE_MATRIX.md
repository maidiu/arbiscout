# Acceptance matrix — purchase-price-gap index only

| ID | Evidence needed for PASS | False-positive / rejection test | State |
|---|---|---|---|
| A01 | Relevant retailer offer feed/source and compatible use rights | Unapproved source, expired cache, unsupported retention | OPEN |
| A02 | Exact current total RETAIL PURCHASE price, link, timestamp, seller, region and actual availability | Expired coupon, local-only, wrong seller, no stock | OPEN |
| A03 | Product identity proves exact same GTIN/model/bundle/condition/quantity for retailer and eBay history | Similar model, wrong size, refurbished vs new, bundle mismatch | DRAFT IDENTITY UTILITY ONLY |
| A04 | eBay historical regular completed-sale price data with valid actual-sales window, sample, exclusions and rights | Asking price, zero sales, incomparable offer, outlier-dominated sample | BLOCKED LIVE DATA |
| A05 | Robust regular historical price estimate, dispersion and conservative quantile with enough valid observations | Median of 1 item, unknown accepted-offer, stale window | NOT_STARTED |
| A06 | Accurate absolute and relative RETAIL PURCHASE PRICE GAP below eBay historical regular completed-sale reference | Negative gap, arithmetic mistakes, unsupported tax/shipping assumption | NOT_STARTED |
| A07 | Purchase condition scoring ranks MAXIMUM RELIABLE gap with source strength and refusal behavior; returns 0–10 | Invented sale evidence, price gap justified by wrong variant, padding top 10 | NOT_STARTED |
| A08 | For imports when supported: actual delivered acquisition price, MOQ, freight, currency, lead-time evidence | Misstated delivered price or noncomparable product | OPTIONAL |
| A09 | Daily scheduling, idempotence, error state and freshness of permitted sources | No data, quota failure, duplicate, outdated result | NOT_STARTED |
| A10 | First real retailer price + same-item historical eBay reference → quantified purchase gap → human index report | Independent recheck of offer and original sales observations | BLOCKED LIVE |
| A11 | Repeated accuracy measurement: observed offer still current, historical baseline credible, false alerts counted | Stale prices, unverifiable stock, repeated false discount | NOT_STARTED |
| A12 | Security and exact code SHA, tests, source permissions and independently reviewable receipts | Secret leak, fixture presented as live, unmerged PR advertised as accepted | IN_PROGRESS |

A successful mock does not establish live market evidence. Different statuses for source documented / permitted / executable / tested / independently accepted / deployed must be preserved. No subsequent transaction belongs to acceptance.
