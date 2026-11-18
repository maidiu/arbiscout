# OPENCODE COMMISSION — ARBISCOUT FULL RETAILER ACQUISITION EXPANSION

**Read FIRST:** `OPEN_CODE_BUILD_DOSSIER.md` (54 site-level mechanisms and detailed build instructions), then `MECHANISM_SPECIFICATIONS.json`, and the actual latest `maidiu/arbiscout` repo at `work/arbiscout-local-build`. Research anchor as of 2026-11-17: `65529f5c5d23820d679f8d003157a1dd25d4f994`; verify HEAD yourself and work from the current one.

## Role and target

You are ArbiScout's implementation engineer, not an assistant researching which stores look promising. **Implement differentiated acquisition mechanisms for the full 54-case merchant/source inventory**, not just the six original canaries and not a universal Best Buy selector over every domain. Organize by shared crawler/adapter primitives where helpful, but treat each merchant's pagination, page hydration, embedded JSON/JSON-LD, campaign-to-category navigation, SKU/variant, shipping, stock, coupon, membership, feed/API, and store context independently. Investigate each unresolved site with actual evidence as authorized.

**Terminal product:** Aggregate real currently obtainable discounted products from as many qualified retailers as possible, present them in the existing ArbiScout Deals catalog, permit manual/top-N selections, and feed those selections to the **existing** eBay Sold/Completed page open → user-saved HTML watcher → 30-day comparison → Results pipeline. Do NOT replace the eBay pipeline or add resale/profit calculations. Retailer advertised savings is not the historical eBay gap.

## Work rules

1. Create an isolated work branch from the observed current local-build head; preserve existing source and tests and do not merge independently into protected `main`.
2. Build a source-neutral adapter registry and keep the normalized `retailer/products.json`/unified catalog contracts compatible. Existing Best Buy browser parsing and Woot/Meh/Kroger API adapters are valid baselines; do not rewrite them gratuitously.
3. For each merchant inspect actual page/documentation and record **where its discounted product list originates, how products paginate or lazy-load, where price and model fields reside, and how item-specific variants/stock/locale are represented**. Public indexed snippets do not prove CSS selectors or private XHR endpoints. Freeze provenance-safe source fixtures before treating selectors as fact. Work with actual page captures, permitted APIs, approved feeds and local supplied HTML. Do not use unauthorized scraping or evade access controls.
4. Supply distinct treatments for documented public URL pagination (`page`, `start`, `sz`, `firstResult`), structured offer JSON (Dell), variant grids (REI/Backcountry/Macy's/PUMA), campaign pages (Costco/Kohl's/CVS/Samsung), store-specific sources (Micro Center/Kroger), dual-price sources (Chewy), approved network feeds (Impact/CJ/Awin), Keepa/Amazon and WooCommerce (only consented stores). Don't guess missing mechanisms: investigate or record exact evidence required.
5. Make price roles explicit: exact unconditional current buyer price; seller; shipping/store; regular/was; MSRP/compare-at; price range; member/trade-in/coupon/subscription; availability; variant. No range minimum as a buyable price; no credits counted as immediate cash discount; do not combine unrelated variants/sellers.
6. Produce per-source `SOURCE_RECEIPT`, `PAGING_RECEIPT`, `PRICE_EXTRACTION_RECEIPT`, `RIGHTS_RECEIPT` and fixture-backed tests. For blocked/unapproved sites, write non-network parsers or integration plans only where justified, with HOLD not fabricated success. Avoid credentials in repo.
7. Keep the existing Control Room / Deals / Results / Settings UI and saved-list/selection controls operational, expanding source filters and status observability where needed. Do not spin up another front end.
8. Cross-check genuine captures against browser-visible products, run all application and control-room tests, and maintain a clear table: site, mechanism proven, records extracted, current-price precision, variant identity precision, rights status, completeness, remaining blocker, exact source/commit/test.

## Final acceptance

- Coverage ledger for **all 54 cases**; no silent omissions.
- As many genuinely working, permitted, test-backed sources as possible; strict HOLD for unverified mechanisms/rights rather than simulated products.
- Concrete page/parser fixtures and positive/negative tests for each implemented adapter, including pagination, page counts, SKU identity and prices; source-free fixtures distinguished from live source checks.
- All new source rows appear correctly in existing Deals and selected product routes to existing eBay Results unchanged.
- A complete exact-SHA return and explicit independent review requirements. No claim of universal coverage or an unauthorized live crawler.

For all documentary background, follow the links and evidence qualifiers in `OPEN_CODE_BUILD_DOSSIER.md`. **Prioritize actual differentiated mechanisms over compatibility scores and generic speculation.**
