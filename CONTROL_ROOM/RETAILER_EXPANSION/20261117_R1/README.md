# ArbiScout — retailer mechanism implementation workroom

**Established:** 2026-11-17. **Custody:** isolated GitHub branch `agent/arb-retailer-treatment-workspace-20261117-r1`, based on `65529f5c5d23820d679f8d003157a1dd25d4f994`. **Scope:** 54 named retailer/source cases (RET-001…RET-054) from the 2026-11-17 OpenCode handoff; do not confuse research with verified live access, permitted use, or integrated implementation.

## Read in this order
1. [OpenCode execution commission](OPENCODE_EXECUTION_COMMISSION.md) — operational instructions and return contract.
2. [Research dossier](RESEARCH/OPEN_CODE_BUILD_DOSSIER.md) — how each source exposes deals, navigation, pagination, price and identity hazards.
3. [Mechanism specifications](RESEARCH/MECHANISM_SPECIFICATIONS.json) — exact 54 canonical research source records; source research is a snapshot, **not** certified selectors or authorized access.
4. [Inventory](MANIFEST.json) and [Dashboard](DASHBOARD.md) — complete cross-source accountability.
5. [Treatment and receipt protocol](TREATMENT_PROTOCOL.md), then individual [TREATMENTS](TREATMENTS/) files.

## Work product and truth
Every RET-xxx has two files: `TREATMENTS/RET-xxx.json` is its **mutable machine-readable state and receipt index**, and `TREATMENTS/RET-xxx.md` is its dated explanatory engineering journal. They must be updated together whenever work is performed. The immutable research snapshot must not be overwritten with claimed code results. Source receipts should be committed under `RECEIPTS/RET-xxx/` when permission and privacy permit; large/private raw HTML, user credentials and prohibited vendor content remain local, with hashes and sanitized metadata in Git.

States: `UNSTARTED`, `EXISTING_SOURCE_RECHECK`, `RESEARCHING`, `ACCESS_HOLD`, `MECHANISM_DOCUMENTED`, `FIXTURE_VALIDATED`, `LIVE_VALIDATED`, `CATALOG_INTEGRATED`, `REVIEWED_ACCEPTED`. **Do not skip evidence gates.** Existing Best Buy/Woot/Meh/Kroger integrations start at RECHECK; this does not upgrade source permission or accuracy.

Every new producer must feed the existing `ENGINEERING/arbiscout_app` normalized retailer source contract and the Control Room → Deals → saved/Top N selection workflow. **Leave Results' eBay Sold/Completed open → user-saved HTML watcher → 30-day comparison unchanged.** No resale/profit features.

## Commands
```bash
python3 CONTROL_ROOM/RETAILER_EXPANSION/20261117_R1/scripts/validate_and_render.py --check
python3 CONTROL_ROOM/RETAILER_EXPANSION/20261117_R1/scripts/validate_and_render.py --write
python3 -m unittest discover -s ENGINEERING/arbiscout_app/tests -v
python3 -m unittest discover -s tests -v
```
Run at a checkout root, with app requirements installed. The workroom validator checks 54 records, status vocabulary, minimal proof requirements and generated dashboard currentness; it is not by itself a test that remote retailers work.

## Source and governance
Based on original ARB-020, F1 and F2 independent research and the Nov 17 handoff. Earlier research branches are **not independently adopted live source licences**. The current app baseline remains the user's active local-build branch. All implementation changes need exact-SHA branch-level evidence, repeatable negative tests and separate independent receiving. **Do not merge to main autonomously.**
