# LAUNCH — ARB-RETAIL-54 — Source-specific retailer acquisition and treatment ledger

**Repository:** `maidiu/arbiscout` (public). **Research/workroom branch:** `agent/arb-retailer-treatment-workspace-20261117-r1` (verify actual commit SHA before writes). **Application source:** `work/arbiscout-local-build` at current verified HEAD; this commission workroom began from `65529f5c5d23820d679f8d003157a1dd25d4f994`. Do not overwrite later app changes; reconcile exact upstream heads before coding.

**Role:** OpenCode implementation engineer working a source-specific 54-retailer acquisition program. Not the independent reviewer, not HQ accreditation, not autonomous merge authority. Read `CONTROL_ROOM/RETAILER_EXPANSION/20261117_R1/README.md`, `RESEARCH/OPEN_CODE_BUILD_DOSSIER.md`, `RESEARCH/MECHANISM_SPECIFICATIONS.json`, `TREATMENT_PROTOCOL.md`, and current `ENGINEERING/arbiscout_app/` before implementing.

**Goal:** Maximize *actually accessible, correctly extracted and legally usable* current retailer purchase offers across the entire inventory. Find **how each retailer works**, not whether it superficially resembles Best Buy. Source-specific handlers may use current Chrome browser collection, pagination/listing HTML, embedded JSON, official API, approved merchant feed, consented WooCommerce Store API, or manual saved-page ingestion as evidence supports. Use shared primitives where useful without forcing a universal page template.

## Required ledger discipline
- All 54 `RET-001…RET-054` exist. **Take explicit custody of every source**, keeping `TREATMENTS/RET-xxx.json` and `TREATMENTS/RET-xxx.md` current. The registry is `MANIFEST.json`; JSON per-case is the source of truth; dashboard is generated, never fabricated.
- Do work in controlled batches by mechanism family; do not silently drop difficult sites. Use `ACCESS_HOLD`/documentary adapter if rights prohibit automatic collection, and record exact rationale/source/date.
- Capture **source, pagination, price, identity, rights, tests, catalog, review** receipts per `TREATMENT_PROTOCOL.md`, with path and commit hash. No production-ready claim from a README, HTTP 200, first-dollar regex, screenshot, synthetic fixture or successful browser navigation alone.
- Use a source-neutral `retailer/products.json` offer adapter; protect SKU, GTIN, variant, condition, seller, unit, local stock and payable price semantics. No range minimum, MSRP, in-cart hidden price, reward value or coupon contingency silently turned into an unconditional purchase price.
- Determine target/deal pages, link discovery, pagination (including `page`, `start`, `sz`, `firstResult`, load-more and infinite scroll), price hydration readiness, embedded product objects, canonical dedupe, category source, location/currency and stock *per source*.
- Preserve **Control Room / Deals / Results / Settings** and the existing Results mechanism: browser opens eBay Sold/Completed; user saves HTML; watcher parses real completed-sale observations and 30-day distributions. This is not a mandate to integrate CompsAPI or to rebuild eBay. No future resale, fees, ROI or net-margin application model.
- Keep raw captures from prohibited/private feeds out of Git; never commit API keys/session cookies. Do not evade CAPTCHAs or access controls or run prohibited bulk scraping.

## Sequence
1. Verify source branch and app HEAD, run baseline tests and validator. Create a child `agent/arb-retail54-implementation-*` branch from the live workroom head; don't commit to the user's actively developed working branch.
2. Run a bounded **per-source mechanism discovery** pass; write the precise observed recipe or what evidence is still missing into all 54 treatment files. Separate old research from newly seen DOM, response JSON, API or authorized feed evidence.
3. Implement fastest useful source families, including existing Best Buy/Woot/Meh/Kroger regression protection, then permitted paginated sale pages/embedded data and approved feeds; choose engineering order by actual yield, rights and evidence rather than fixed list order. Expand categories/filters in existing Deals only.
4. For each implemented adapter, add real-source sample evidence (when allowed), stored-source fixtures or hashed private snapshots, positive + hostile negative parsing tests, field-precision estimates and normalized `retailer/products.json` output.
5. Run app and root tests plus `python3 CONTROL_ROOM/RETAILER_EXPANSION/20261117_R1/scripts/validate_and_render.py --check`. Update currentness only after exact evidence, maintain causal work history.
6. Submit a comprehensive exact-SHA return: 54 statuses, implemented set, usable live rows vs source-free fixtures, denied/HOLD set, coverage/yield, rights/expiry/retention unresolved, test output, files and SHA, next unblocked actions. Request independent reviewer; do not merge.

## Stop/GO law
One source may proceed without all 54 being integrated, but all 54 must be **accounted for** with reasoned status. Inaccessible vendor, disallowed collection, unproved current prices or variant mismatch → HOLD / zero qualified rows, never guessed deals. Price gap against eBay is only qualified when the existing comparator has enough actual matching completed-sale evidence.

**Success:** working treatment ledger + demonstrably permitted, tested additional retailer data producers integrated into existing Deals. **Not success:** an impressive count of merchant names, unsupported scraped prices, or a separate UI that bypasses existing eBay Results.
