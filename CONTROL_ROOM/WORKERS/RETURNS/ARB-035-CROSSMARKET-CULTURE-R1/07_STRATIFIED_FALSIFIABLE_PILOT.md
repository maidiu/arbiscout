# ARB-035 / 07 — Preregistered, hostile, stratified 100-observation pilot
**Design frozen conceptually 2026-10-31; NOT EXECUTED.** No paid source, eBay Seller Hub session, buyer identity data, automated extraction, time series, true price match, programmatic retailer stock check or authorized survey ran.

## Primary estimands (before looking at outcomes)
(A) **Eligible evidence-qualified retailer purchase-gap yield** per 1000 unique observed offers, by sector × source × checkout locale; (B) same-condition, actual-paid eBay historical demand regularity, not annual category volume; (C) SKU/retailer discount-event frequency and duration; (D) distribution and lower CI of conservative absolute gap `G25`; (E) consented buyer deal-monitoring overlap if separately authorized.

## Sampling frame and exactly 100 *prospective* observations
**10 sector panels × 10 distinct prospective product offers each = 100**, not 100 alleged known SKUs:
1. OEM vehicle electronics/parts
2. Branded professional power tools / genuine batteries
3. Camera bodies / lenses
4. Professional IT / networking components
5. Industrial technical modules (sparse/high-ticket stress)
6. LEGO sealed sets
7. Mainstream game consoles/electronics **price-transparency control**
8. Genuine OEM toner / business consumables
9. Pokémon / hyper-monitored sealed cards **fast-attention negative control**
10. White-label furniture / oversized clearance **identity/logistics negative control**

Per panel, draw 10 without replacement from sources in `02`: **4** random time-stamped offers from a *permitted* enumerated deals feed, **2** random catalog products irrespective of sale badge from a different permitted source, **2** SKU candidates identified from actual paid eBay high-regularity data with **no known retailer promotion** (reverse control), **2** retail deeply marked-down SKU candidates selected *without eBay demand conditioning* (discount/no-demand control). Total 40 + 20 + 20 + 20 = 100. A cohort that cannot be sourced under permissions is recorded as `FRAME_INACCESSIBLE`; **do not backfill with favorable examples**. Retain a complete nonqualifier ledger and raw source-published sampling-frame count. Consult `01` for 38 prespecified candidate *strata*, **not invented SKU identifiers**.

**Source family balancing:** at least two independently permitted retailers/feeds per panel if technically available; catalogue enumeration, curated deals, manufacturer/authorized outlet and explicit local in-store clearance are distinct frames and cannot be treated as a probability sample of all US clearance. Each candidate must be a known physical unit with verifiable GTIN/MPN from a first-party merchant/manufacturer document. Before any outcome check, freeze chosen SKU list, merchant, source event timestamp and immutable sample random seed. No after-the-fact product substitution.

**Ticket bands:** <$50, $50–149, $150–299, $300–749, $750+ based on observed retailer price, recorded not preassigned to impossible bands. Sample a mix where available and report frame scarcity, rather than forcing industrial modules into $25 and LEGO into $2500. Quota condition: new unopened first, open-box/refurb separate and explicitly excluded unless exact condition equivalence proved.

## Historical eBay measurement
For all 100 when data permit, observe identical SKU actual-paid sale history at **7, 30, 90, 365 days**; actual local time and marketplace, total sold, weekly activity, median/p25/p75, shipping price basis, accepted-offer fidelity and omissions. Product Research may serve as a human-permitted audit oracle, not an automated feed; API row access is **HOLD** under ARB-010. If vendor returns only aggregates, do not pretend weekly sequence exists. Prespec conservative qualifying-study gate `n90 >= 12`, `>= 6/13 weeks with sales`, `last sale <= 21 days`, `exact condition+bundle`, and `G25 lower resampled interval > 0`. These numbers are provisional *study thresholds* deliberately strict; report exclusion counts and sensitivity to gates (`n=6/12/20`, `weeks=4/6/8`) without moving thresholds to manufacture a win.

## Merchant longitudinal protocol
Without unauthorized crawling: use permitted provider feed snapshots with fixed daily checks for minimum **12 weeks** to estimate recurrence; prospectively supplement sampled items at t0, +6h, +24h, +72h, +7d where source quotas and explicit terms allow. Observe actual price, seller-of-record, member/coupon entitlement, stock, pickup ZIP, final mandatory purchaser charges and link. A retailer's general daily-deals schedule is **not** 12 observations of a SKU's repeat markdown. For 12-week pilot, initial 100 offers and their repeat checks constitute separate longitudinal measures, not extra baseline sampled SKUs. Record source rate limits, credits, TTL and gaps in observation.

## Independent adversarial controls
- Retail 40%-off sticker with **0 exact eBay paid sales** (NO_BASELINE).
- Genuine active eBay demand but no retail sale (NO_GAP).
- Large high-ticket deal with **1 sold in 90d** (SPARSE).
- Kit vs bare tool; camera body vs bundled lens; SSD revision; LEGO set number vs damaged sealed box; genuine vs third-party toner (MISMATCH).
- Hyperinformed collectable alert feed; retailer promotion reaches Discord within minutes (ATTENTION_COUNTEREXAMPLE).
- Checkout price differs from feed, store-only ZIP inaccessible, coupon expired, tax or freight missing (NOT_OBTAINABLE).
- eBay sold-page price is *Best Offer asking upper bound* not accepted consideration (PRICE_TYPE_UNPROVEN).
- Same exact SKU promotion ends before next permitted check (SHORT_LIVED; censored appropriately).

## Power, uncertainty and verdict limits
At n=10 per category, individual-category opportunity rates have wide binomial intervals. Even 0 successes in 10 has an approximate **95% upper one-sided rate bound of 26%** under independent Bernoulli sampling (`1-0.05^(1/10)`); thus **no-zero-success category can be pronounced intrinsically barren**. Design is a **feasibility/falsification pilot**, not powered to prove modest between-sector yield differences. Report Wilson intervals and frame/cluster effects, yield per 1000 with defensible extrapolation of the *same sampled frame only*, and a predeclared holdout 2nd month/retailer with larger n based on measured rates. For a sector win: separate evidence in 2+ independent time periods and suppliers, no dependence on a single exceptional SKU, nonoverlapping uncertainty intervals for leading outcomes or a preregistered inferential comparison robust to multiple sectors. No invented p-values or confidence percentages.

### Attention sub-study is separate
Recruit a consented, non-deal-forum-only sample of category eBay buyers, *if authorized*; collect self-reported vs opt-in panel observed retailer monitoring within seven days of actual searches/purchases, approved privacy protocol, confidence bands and recruitment biases. Compare regional/repair niche against electronic and TCG fast-alert controls. Public Reddit time stamps or Similarweb traffic alone **never** satisfy this test.

## Quality check / stopping and rejection
A pilot can produce **zero qualified gaps** and still be completed faithfully. Stop on missing contract permission; identify missing fields and preserve record-level nulls without substitutes. Stop a cell with 0 exact matches instead of title fuzzing; preserve the failure denominator. No seller account, buyer behavior surveillance or checkout automation without actual separate grant.

## Operational handoffs
- **ARB-010/040/051:** actual paid eBay historical observations or manual oracle, vetted for rights and accepted-offer fidelity.
- **ARB-020/029/031/033:** permitted deal enumeration, retailer all-in purchase price/availability, source denominator.
- **ARB-030:** strict identity/condition/bundle match.
- **ARB-050/060/071:** conservative observed below-eBay gap, Pareto-relevant summaries and 0–10 actual linked daily index.
- **ARB-035/Q096–Q112:** no canonical statuses advance until hostile independent review and valid live pilot. Source-free design is complete but **NOT TESTED**.
