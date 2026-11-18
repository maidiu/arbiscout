# RET-046 receipt index — 2026-11-17

- **Retailer:** Woot
- **Treatment status:** EXISTING_SOURCE_RECHECK
- **Local adapter:** `ENGINEERING/arbiscout_app/providers.py`
- **Prior local run:** 500 rows in the local app run (not independently verified).
- **Source/paging/price/rights receipt:** [../../../ENGINEERING/arbiscout_app/sources/receipts/RET-046.json](../../../ENGINEERING/arbiscout_app/sources/receipts/RET-046.json)
- **Identity:** dedupe and variant rules are documented in the receipt JSON; variant conflicts are not merged into one buyable price.
- **Catalog:** local catalog tests confirm normalized rows can enter Deals; no fresh live catalog acceptance is claimed.
- **Tests:**
- `ENGINEERING/arbiscout_app/tests/test_providers.py`
- `ENGINEERING/arbiscout_app/tests/test_catalog.py`
- `ENGINEERING/arbiscout_app/tests/test_source_registry.py`
- **Rights:** not authorized for live/production use; terms review remains open.
- **Review:** NOT_REVIEWED.
- **Next action:** obtain independent rights/terms review and a fresh authorized source capture before any LIVE_VALIDATED or CATALOG_INTEGRATED claim.
