# ArbiScout

**Evidence-first retail arbitrage and import sourcing scout.**

The product goal is a daily automated 0–10-item shortlist of potentially profitable buy-low/sell-high inventory opportunities. It requires exact product matching, verified completed-sales evidence, full landed costs, availability, and a final human purchase decision. No deal or historic sale is invented to fill the report.

## Control room and full PROGRAMMA

**[HQ start here](CONTROL_ROOM/00_READ_ME_FIRST.md)** → [Programma whole project](CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_ARBISCOUT.md) → [39-task dependency ledger](CONTROL_ROOM/PROGRAMMA/01_WORK_REGISTRY.json) → [16-source evidence ledger](CONTROL_ROOM/PROGRAMMA/02_SOURCE_REGISTRY.json) → [Current status](CONTROL_ROOM/STATUS/CURRENT_PROGRESS.md).

Read those before commissioning, editing or claiming production readiness. Programma is a living project map (recognize/recover/reconcile; organize/adjudicate; implement/prove/integrate/learn), not an automated worker or new permission grant.

## Current development reality

- The first source-free matching/finance prototype is on [draft PR #1](https://github.com/maidiu/arbiscout/pull/1), **not canonical main**.
- This control room itself is also a separately reviewed proposal until merged.
- No live provider contract, active eBay sold-data API, deployed daily crawler, real verified shortlist, or profitable backtest is established by these docs.
- Vendor terms and independent source rights must be verified before using live feeds or retaining source content.

## Tests

```bash
python scripts/validate_programma.py
python -m unittest discover -s tests -v
```

These are **structural** tests only; green tests do not demonstrate access rights or actual market intelligence.

**Security:** this repository is currently public. Never commit credentials, private sales data, user/customer information, or login cookies. Only authorized live access belongs in protected runtime integrations.
