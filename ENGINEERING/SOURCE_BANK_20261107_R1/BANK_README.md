# ARBISCOUT EXPLICIT SOURCE BANK — 2026-11-07

`active/` is the current full local prototype and eBay 30-day comparison extension; it is SOURCEFREE_TESTED only, NOT a legally enabled live production scraper or verified eBay sold-data tool.

`legacy/` preserves original independently developed pilot, saved Best Buy extractor, and listing-first crawl planner sources without treating them as approved separate current implementations.

No user-uploaded Best Buy HTML, credentials, private communications, or third-party copyrighted pages are distributed here. Test fixtures are synthetic. This is a provenance/custody archive, not a proof of production readiness, external authorization, accepted economic evidence or protected main-branch merge.

Extract this tarball with `tar -xzf ENGINEERING/SOURCE_BANK_20261107_R1.tar.gz`; run `cd active && python3 -m pip install -r requirements.txt && python3 -m unittest discover -s tests -v`.
