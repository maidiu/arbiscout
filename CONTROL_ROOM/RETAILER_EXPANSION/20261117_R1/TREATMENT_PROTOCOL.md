# Treatment and evidence protocol

## Per-retailer procedure (repeat for all 54)
1. **Discover:** Identify actual sale/clearance entry point, product enumeration method, pagination/cursor/limit behavior, JavaScript hydration, data transport. A public search snippet is NOT a confirmed API endpoint.
2. **Access and rights:** Check current terms, robots policy where relevant, whether a publisher/feed relationship was actually granted, allowed extraction, storage, pricing comparisons, retention and attribution. Save a dated quote/URL and disposition. If unresolved, use manually supplied/saved permitted HTML or source-free fixtures; no blocked network collection.
3. **Source receipt:** At a stated capture time, include page/feed URL, response status, locale/store/ZIP, mode (manual saved HTML / consented browser / permitted API / feed), page/cursor, actual visible count, content hash, source owner and capture limitation.
4. **Paging receipt:** Record expected and actual number of pages/products; follow/stop rules; duplicates; missing lazy-loaded rows; pagination boundaries; whether all apparent results are enumerable.
5. **Price extraction receipt:** Record paired current and reference price at same SKU/variant/seller/time, tax/shipping/coupon/member/trade-in ambiguities; forbid first-$ parsing or range min impersonating a buyable price.
6. **Identity receipt:** GTIN/UPC/MPN, model revision, size, color, kit/pack, condition, marketplace seller, stock and location, with explicit refusal cases.
7. **Fixture and tests:** Preserve permitted sanitized fixture or local hash; positive and negative extraction tests; compare extracted items/prices to independently counted visible offers and expected paging.
8. **Catalog integration:** Confirm rows appear in existing Deals and can be saved, selected and enter existing Results without modifying the eBay acquisition workflow.
9. **Review:** Commit/branch SHA, paths, test commands/results, source rights decision and reviewer decision. An adapter with fixture tests is FIXTURE_VALIDATED, not LIVE_VALIDATED. A live run without suitable rights is not accepted.

## Receipt categories
- `SOURCE_RECEIPT` — original provenance, capture time, raw file SHA-256 (or documented absence), access method
- `PAGING_RECEIPT` — discovery coverage, pages/units/duplicates
- `PRICE_EXTRACTION_RECEIPT` — correct current price, reference semantics, explicit exclusions
- `IDENTITY_RECEIPT` — exact model/variant/pack/condition and mismatch tests
- `RIGHTS_RECEIPT` — terms, permission, permitted purpose/retention, unresolved constraints
- `CATALOG_RECEIPT` — normalized records, source filter, selected handoff
- `TEST_RECEIPT` — tests, pass/skip/fail and fixture type
- `REVIEW_RECEIPT` — independent receiving and exact SHA

Each record's JSON `receipts` list contains objects with `type`, `path`, `sha256` (nullable), `commit_sha`, `captured_at`, `verdict` and `notes`. A receipt may point to an evidence document under `RECEIPTS/RET-xxx/`. Never commit credentials, user-saved private HTML, cookies, tokens, paid feed dumps or third-party content without retention rights. Keep exact source facts and claims separate.

## Stage law
`UNSTARTED` = no expansion work; `EXISTING_SOURCE_RECHECK` = older adapter exists, not accepted here; `RESEARCHING` = investigating; `ACCESS_HOLD` = rights/availability obstacle; `MECHANISM_DOCUMENTED` = capture/pagination/extraction mechanism established with evidence; `FIXTURE_VALIDATED` = source-free parser tests run; `LIVE_VALIDATED` = legitimate live data with matching price/stock/identity confirmed; `CATALOG_INTEGRATED` = verified live rows into current Deals and existing selection→Results; `REVIEWED_ACCEPTED` = independent review of exact head and source rights. Movement is not monotonic: regress when source or permission changes.

Treat `mechanism_state`, `rights_state`, `quality_state`, `integration_state` and `review_state` separately—one passing gate cannot be substituted for another.
