# Retailer expansion implementation return — 2026-11-17 R1

**Branch:** `agent/arb-retail54-implementation-20261117-r1`
**Workroom seed / CI head:** `16a194d4aa5d98b6262c1ad956211f2f9d345a37` / `8517aba3a9420e8558f3285608dd25e92c8b68f5`
**Reconciled app head:** `8bdf2111593b6d2e0ea5ab3d7819abcc0153b112`
**Treatment ledger commit:** `a745e7e`
**Dell implementation commit:** `0e144bced6ae130ae3464ba6002c3af218dbc84f`
**Model-code fix commit:** `216febf7bad514cfd6fd6ebd4eae920a2804ce10`
**LEGO implementation commit:** `0432d2f368345b8f86218caf018830806448d0fc`
**Scope:** all 54 RET cases accounted for. No autonomous merge to `main`.

## Status totals

- `EXISTING_SOURCE_RECHECK`: 4 — RET-001 Best Buy, RET-046 Woot, RET-047 Meh, RET-048 Kroger.
- `FIXTURE_VALIDATED`: 2 — RET-054 Dell new-product deals (36 offers) and RET-029 LEGO Store (18 sets).
- `ACCESS_HOLD`: 48 — 5 rights, 9 approved-feed and 34 terms blockers.

Every treatment JSON now carries `implementation_status`, separate rights/mechanism/quality/integration/review states, exact blocker, next action, receipt index, decision and dated history. Every treatment journal has a matching 2026-11-17 coverage entry. The generated dashboard reports the same 4/50 split.

## Implemented local adapters (not accepted live)

| ID | Source | Adapter | Prior local rows | Status |
|---|---|---|---|---|
| RET-001 | Best Buy | `ENGINEERING/arbiscout_app/arbiscout.py` | 137 products / 74 complete pairs / 12 listing pages | EXISTING_SOURCE_RECHECK |
| RET-046 | Woot | `ENGINEERING/arbiscout_app/providers.py` | 500 capped offers / 354 catalog families | EXISTING_SOURCE_RECHECK |
| RET-047 | Meh | `ENGINEERING/arbiscout_app/providers.py` | 1 current deal | EXISTING_SOURCE_RECHECK |
| RET-048 | Kroger | `ENGINEERING/arbiscout_app/providers.py` | 36 promoted products at ZIP 29072 | EXISTING_SOURCE_RECHECK |
| RET-054 | Dell new-product deals | `ENGINEERING/arbiscout_app/providers.py` (embedded JSON) | 36 offers / 34 paired / 2 current-only | FIXTURE_VALIDATED |
| RET-029 | LEGO Store | `ENGINEERING/arbiscout_app/providers.py` (JSON-LD + __NEXT_DATA__) | 18 sets / 18 paired | FIXTURE_VALIDATED |

These are local-run and test receipts, not authorized production acceptance. `correct_current_prices_verified` is `false` for all six; `rights_status` is `TERMS_REVIEW_REQUIRED`; `review_status` is `NOT_REVIEWED`. Dell has one local capture (raw HTML hash recorded, not committed) and a synthetic parser fixture; it is not `LIVE_VALIDATED` or `CATALOG_INTEGRATED`.

## HOLD discipline

The 48 HOLD sources emit no products and have no invented selectors, endpoints or prices. Dell emits only parser-validated rows from a captured embedded JSON object; its rights and exact configuration/GTIN accuracy remain open. Each has a per-source `RECEIPTS/RET-xxx/rights.md` recording the access gate, blocker, next action and evidence limitation. No raw HTML, credentials, cookies, paid feeds or private respondent data were committed.

## Verification

- Root tests: `python3 -m unittest discover -s tests` — **5 passed**.
- App tests: `python3 -m unittest discover -s ENGINEERING/arbiscout_app/tests` — **55 executed, 54 passed, 1 skipped**.
- Workroom validator: `python3 CONTROL_ROOM/RETAILER_EXPANSION/20261117_R1/scripts/validate_and_render.py --check` — **PASS, 54 treatment files**.
- `git diff --check` — clean at the treatment commit.

## Unresolved and next actions

- Rights/terms, permitted purpose, retention and redistribution remain unresolved for all 54; the six local adapters are not production-authorized.
- The 48 HOLD cases need authorized page-1/page-2 captures or approved feeds before selectors, pagination and price semantics can be established. Do not guess them.
- Dell model-code fix: `Dell16LaptopDC16255` now maps to `DC16255`; the existing saved Dell 16 page yields **3 usable sold observations**, provisional median **$599.99** vs retail **$649.99**. This is still displayed-price evidence, not verified actual paid.
- Results watcher now stages already-saved eBay HTML before its first comparison and reuses a single running instance; the saved Dell 16 page shows 3 usable sold observations. Saved-page matching now uses sold-item titles/model codes, so a user-improved search query no longer breaks the match. Save HTML, not Safari `.webarchive` files.
- Optional LLM identity refinement added: Results supports per-candidate arm/disarm plus **Run selected** and **Run all new**. Selected candidates are combined into one compact identity-only job when safe, split only by a configurable input-size limit. Strict JSON verdicts remove wrong-config/used/unknown rows; cache, raw backup and deterministic calculations remain local. Checked rows display the post-LLM exact/removed counts, usable sample, median and gap, and a persistent `llm_checked` flag prevents Run all new from processing them again. Results also has a per-candidate HTML Match selector; manual mappings override auto-match and are persisted in `manual_matches.json`. When a candidate is LLM-checked, identity adjudication runs first and `qualify(identity_verified=True)` bypasses the regex model veto; deterministic condition/parts/price guards still apply. The regex remains the default when no LLM check exists. Rows are explicitly labeled PRE-LLM or POST-LLM; checked rows show pre-LLM n/median and post-LLM n/median/gap. The LLM is now inclusive: same brand/model/family is enough; absent optional specs or condition are not contradictions, and only explicit different models/configurations/used/parts are removed. A Reset control restores the raw comparison so a checked row can be re-run. Deals and Results default to Last 30 days so observations do not disappear at midnight. No live provider call was made; provider terms and false-positive rates remain open.
- Fresh identity, stock, payable-price and independent reviewer acceptance remain open.
- Next productive move: resolve Dell/LEGO rights and completeness, then choose the next highest-yield HOLD family with a viable permission path. Promote only cases with exact evidence.
