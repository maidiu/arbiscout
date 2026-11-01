# ARB-020-F1 — $0 provider fees, candidate capacity and real maintenance budget
**2026-10-31; modeled, not measured.** 'No subscription' is distinct from free operator labor, a Mac, network/electricity, a public website demanded by an affiliate, or upstream eBay history. No free source has passed a 100-/500-/1000-unique-sale-offer/day live capacity test in this worker.

## Count correctly
Let `U` = **unique currently obtainable discounted merchant+GTIN+condition+quantity+region offers per day**. Let `s` = observed eligible-discount-and-stock fraction among retrieved catalog rows (unknown), `d` = fraction of repeated/duplicate rows (unknown), `p` = page size, `k` = product-detail or ZIP verification calls per candidate. **Required raw rows = ceiling(U / (s*(1-d)))**, and base pages `ceil(raw_rows/p)`; add country/store variants, retries and checkout verification. These are **hypotheses** unless sampled.

For illustration, assume *only to show sensitivity* page size 100 and 10% of catalog rows yield unique sale candidates after dedup/availability; this is **NOT an observed retailer discount rate**.

| Unique current sale offers/day | Raw catalog rows/day at 10% | Feed/API 100-item pages | Detail/stock calls if 1 each | Interpretation |
|---:|---:|---:|---:|---|
| 100 | 1,000 | 10 | 100 | Plausible **if** approved source has enough real sale/available rows |
| 500 | 5,000 | 50 | 500 | Requires broad retailer sale coverage and strong dedupe |
| 1,000 | 10,000 | 100 | 1,000 | No present source has passed this yield or permission test |

At only 1% eligible, all page counts inflate **10×**: 100/500/1000 pages respectively; local inventory and quantity requirements add calls. For the WooCommerce documented 100/page this arithmetic can be applied once merchant approved; an `on_sale=true` server filter may be more efficient than broad catalog scan, but many such products may be stale, out of stock or nonexistent at checkout. **Best Buy** 50k calls/day quota would not in itself block the scenario, but 5/sec, timeouts, actual query pagination, 72h cache and licence must be respected. **Kroger** product API prices require locationId, and multiple stores multiply calls; no verified 1k sale candidates/day.

A licensed bulk feed can deliver perhaps thousands of catalog rows in one scheduled file transfer: request count low, CSV bytes/storage larger; its real sale yield is still unknown. A full 100k-row CSV at 0.5–2 KB/row is illustratively **50–200 MB** per snapshot; retain only allowed fields and TTL. 30-day 1k unique offers/day = 30k offers, easy for local SQLite, with exact SKU indexes. No production storage benchmark performed.

## Mac-local cost accounting
| Resource | Explicit recurring third-party fee | Real condition |
|---|---|---|
| Python requests/BeautifulSoup/lxml, standard CSV/JSON/SQLite | $0 licence/subscription | Developer labor, version/update effort |
| Scrapy open-source | $0 licence | Need approved site + spider maintenance, not an authorization waiver |
| Playwright | $0 licence | Browser binaries, higher CPU/RAM, avoid unless truly necessary and allowed |
| SQLite/DuckDB local | $0 licence | Mac disk/backups and data retention policies |
| macOS launchd | $0 licence | Mac awake, powered and connected at schedule; home connectivity/electricity external |
| Best Buy public developer API | No published paid tier in documented developer material | Exact app key and purpose approval needed; pricing not contract-confirmed |
| Kroger self-service Public API | Advertised self-service without a published per-call price | OAuth app, API use restrictions, SKU/price location |
| Approved Awin/CJ/Impact/Home Depot merchant feeds | Usually no named per-API subscription if admitted | Website/affiliate approval, true permissions, availability and potentially partner fees |
| Arbitrary HTML scraper | $0 code library | Not legal/operational when terms prohibit, even if technically possible |
| eBay completed sale actual-paid data | **UNRESOLVED, separate ARB-010** | Free API entitlement not proven, likely external spend/limited manual use |

## Developer and maintenance sensitivity — assumptions, not telemetry
| Path type | Initial implementation estimate (engineering hours; judgement only) | Routine maintenance illustration | Failure response |
|---|---|---|---|
| One official structured API | 4–12 hours once credentials/rights are granted | 0.5–2 hr/month after stable launch | API version/schema, auth renewal, quota, price drift |
| One approved standard CSV/FTP feed | 3–10 hours after advertiser approval | 0.5–2 hr/month, additional corrections if feed changes | Missing columns/currency/category, staleness |
| One permissioned WooCommerce store | 3–8 hours per store if standard API compatible | 1–3 hr/month per source illustrative | Plugin version changes, SKU/GTIN missing, page counts |
| One permissioned simple HTML + JSON-LD | 6–20 hours each | 1–4 hr per **selector break** (not every month); higher possible | Seller changes markup, membership price, pagination |
| One permitted JS/Playwright site | 12–40 hours each | 2–8 hr per meaningful break, plus CPU | Login, JS, locale, dynamic stock, 429; STOP rather than bypass |
| Explicitly restrictive site | No acceptable $0 scraper implementation | Not applicable | SEEK PERMISSION/FEED, not build stealth |

Example **not measured:** if two permitted HTML sites each break twice monthly and each repair takes 3h, that is **12 engineer-hours/month**. At an illustrative $40/hr opportunity cost = $480/month in labor, even with $0 provider API charges. Ten sites suffering two similar changes each could require **60 hours/month**. These hypotheticals are meant to falsify 'free scraper = cheap system', not report observed failure rates.

## Anti-bot and geography
- Blocked by retailer contractual prohibition: Walmart/Target/Newegg/GameStop/B&H defaults; no request budget allowed.
- 403, 429, CAPTCHA, bot challenge or need for IP rotation → mark **NOT FEASIBLE_AT_$0 UNDER CURRENT AUTHORIZATION**. Do not hide identity, rotate IPs, solve CAPTCHA, or harvest cookies.
- Store-specific pickup prices require explicit store/ZIP and pickup possibility; collect none without permitted path. This can render a nationwide clearance feed misleading.
- Manufacturer outlet/configurable refurbished SKU values and club membership prices need extra exact-match gating.
- Browser rendering per product inflates costs: **1,000 browser navigations/day** can be substantially more expensive than ten 100-product JSON pages even though both are free in dollars. Actual runtime/CPU is **NOT MEASURED**.

## Budget separate from eBay
Retailer discovery may be conditionally $0 in recurring data-provider charges, but 100/500/1000 true candidates/day could require 100/500/1000 additional eBay exact-item price lookups (or fewer after permitted cache/longer 90d reuse). That paid-data question is separately unqualified by ARB-010. Any DeepSeek cost, if used for ambiguous identity only, is outside this retailer API-fee objective and should be separately budgeted; deterministic UPC/price/median calculations cost no inference tokens.

**Viability:** 100/day POSSIBLE_CONDITIONAL; 500/day UNTESTED_AND_SOURCE_DEPENDENT; 1k/day UNPROVEN. Do not convert any hypothetical page count into a guarantee or a source permission.
