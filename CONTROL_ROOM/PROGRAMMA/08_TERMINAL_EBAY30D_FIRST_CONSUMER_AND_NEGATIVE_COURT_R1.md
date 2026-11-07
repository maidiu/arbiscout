# ArbiScout — 30-day eBay reference and first-consumer proof court

**Jurisdiction:** Single purchase-research product, no future-sale model. **Current grade:** sourcefree candidate; `S2_REAL_WORLD_NOT_PROVED`.

## Implementation entry

- `ENGINEERING/arbiscout_app/arbiscout.py`: bounded retailer crawl, listing discovery, deduplication, source extraction and retailer-only dashboard.
- `ENGINEERING/arbiscout_app/ebay_comparison.py`: top-N filtering, eBay sold query links, optional saved-HTML parsing, 30-day date/identity/price filters, exploratory median and source-linked gap dashboard.
- `ENGINEERING/arbiscout_app/run_compare.py`: source-to-source local operator.
- `ENGINEERING/arbiscout_app/tests/`: 16 synthetic and offline checks. Install dependencies first using `pip install -r requirements.txt`; run from that app directory with `python3 -m unittest discover -s tests -v`.
- `--ebay-live` is an **explicit opt-in** direct request mode subject to robots.txt and possible sign-in or access refusal; it has **not been live proven** here.

## Complete terminal chain

```
permitted retailer sale URL / permitted feed
    -> visited listing and relevant department pages (bounded depth/cost)
    -> product pages only where listing evidence is incomplete
    -> dedupe by stable identifier; keep provenance of current sale price and condition
    -> shortlist 20 only from verified retail discount amounts
    -> exact GTIN/model/variant/condition/quantity sale query
    -> permitted eBay historical producer, dated completed SALE observations
    -> filter to 30 elapsed days; remove missing dates, unproven best offers and mismatches
    -> adequate comparable sample and conservative regular historical reference
    -> true total retailer purchase price vs eBay reference arithmetic
    -> source-linked zero-to-ten actual observed gaps, with refusal and uncertainty
```

## Hard product/falsifier gates

1. **Acquisition:** source actually obtainable in the intended usage; no assumption that public pages grant automated extraction or caching. No bypass of access controls, CAPTCHAs or anti-bot systems.
2. **Retailer truth:** *current total purchase cost*, locale, seller, quantity, condition, availability and observation time; advertised MSRP is NOT a sufficient value reference.
3. **Identity:** GTIN/model family is insufficient alone if exact variant, bundle, region, condition or quantity differ. Reject broad title-only matches; current model-token matching is **provisional**.
4. **Historical eBay truth:** only genuine sold transactions in `(as_of - 30 days, as_of]`; real paid amount must be provable. Marketplace displayed sold price may be the former ask after a Best Offer; unknown is excluded, not silently equal to paid.
5. **Sample quality:** document searched/extracted count, exclusions, date coverage, missing pages/Best Offers, shipping amounts and sample dispersion; three matching displayed records in local test do **not** prove a robust historical normal price.
6. **Comparison:** use documented total retailer purchase price and historical same-product paid amount. The current code's basic median is a development baseline, not final robust estimator.
7. **Refusal:** no reliable source, unknown sale date, missing product price, insufficient sample, mismatched variant or access challenge -> no numeric historical ranking. Never fabricate a top ten.
8. **Performance:** count listing pages, product page fallbacks, HTTP errors and eBay query costs per usable match; fee/provider choice must compare **dollars per trustworthy completed comparison**, not advertised per-request price.

## Evidence grades; do not conflate

- `DOCUMENTED`: provider claims and public webpage descriptions.
- `SOURCEFREE_TESTED`: fixtures and saved HTML prove local extraction/calculation only.
- `LIVE_RETRIEVED`: actual external request successfully returned at a named time.
- `SOURCE_AUTHORIZED`: user-approved provider contract/use scope with exact entitlement.
- `FIRST_CONSUMER_PROVED`: one reproducible real retailer-to-eBay comparison with independently checked provenance.
- `INDEPENDENTLY_REVIEWED`: nonauthor challenge with exact source SHA, negative tests and bounded verdict.
- `PROTECTED_RECEIVED`: authorized integrator merges only the scope actually accepted.

No evidence grade entails another automatically. No account approval, paid source contract, reviewer independence, verified sale data or protected merge has occurred merely by issuing this document.

## Work priority

**P0** validate source access for Woot/Meh/Kroger as user-reported accounts (never expose secrets); select CompsAPI/SoldComps candidate for a benchmark against official eBay Product Research; compare 20–30 actual precise models including accepted Best Offers. Parallel engineering: improve matching, source records and 30-day reference quality. Then go from 20 retail candidates to real zero–ten report, and only thereafter optimize scale.
