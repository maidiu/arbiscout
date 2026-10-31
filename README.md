# ArbiScout

**Retailer purchase research conditioned on historical eBay sale-price patterns.** Discover current major-retailer purchase offers whose prices are **maximally below the regular price for the exact same product in completed eBay sales**. Quantify the gap and supporting evidence; show a daily 0–10 item purchase-research index. No future selling activity or account-specific financial analysis.

## PROGRAMMA — command and project state

**[At-a-glance PROGRAMMA dashboard](CONTROL_ROOM/PROGRAMMA/DASHBOARD.md)**

- [Governing product constitution](CONTROL_ROOM/PRODUCT_CONSTITUTION.md)
- [HQ Read First](CONTROL_ROOM/00_READ_ME_FIRST.md) and [standalone HQ bootstrap](CONTROL_ROOM/HQ_BOOTSTRAP_COPY_PASTE.md)
- [Complete 39-task table with hard dependencies, alternative source gates, priority and status](CONTROL_ROOM/PROGRAMMA/TASKS_TABLE.md)
- [All 95 question/substantiation items with question prerequisites and operational task dependencies](CONTROL_ROOM/PROGRAMMA/QUESTIONS_TABLE.md)
- [Work JSON](CONTROL_ROOM/PROGRAMMA/01_WORK_REGISTRY.json), [seven question JSON registries](CONTROL_ROOM/PROGRAMMA/QUESTIONS/), [source evidence JSON](CONTROL_ROOM/PROGRAMMA/02_SOURCE_REGISTRY.json)
- [CSV task view](CONTROL_ROOM/PROGRAMMA/TASKS_TABLE.csv) and [CSV question view](CONTROL_ROOM/PROGRAMMA/QUESTIONS_TABLE.csv)
- [End-to-end architecture](CONTROL_ROOM/PROGRAMMA/03_ARCHITECTURE_AND_CRITICAL_PATH.md), [acceptance](CONTROL_ROOM/PROGRAMMA/04_ACCEPTANCE_MATRIX.md), [current HQ checkpoint](CONTROL_ROOM/STATUS/CURRENT_PROGRESS.md)

**Canonical editing format:** JSON registers. **Readable views:** generated Markdown and CSV; don't manually diverge the tables. In a source checkout:

```bash
python scripts/validate_programma.py
python scripts/render_programma.py --write
python scripts/render_programma.py --check
python -m unittest discover -s tests -v
```

## Current factual status

Control room/PROGRAMMA is on **draft [PR #2](https://github.com/maidiu/arbiscout/pull/2)** until accepted and merged. **Draft [PR #1](https://github.com/maidiu/arbiscout/pull/1)** is an *older, incompatible proposal*: do not merge its earlier scoring scheme into the active index; inspect only potentially reusable exact-product identity utilities.

There is **no verified live retailer + eBay historical-comparables pair, running daily index, or current real bargain recommendation**. The real critical path is source access → retailer offer/identity and eBay regular completed-sale baseline → defensible purchase-price gap → index report. Provider rights, data quality and actual tests must be evidenced separately.

The repository is public: do not commit any passwords, account tokens, buyer information, or restricted datasets.
