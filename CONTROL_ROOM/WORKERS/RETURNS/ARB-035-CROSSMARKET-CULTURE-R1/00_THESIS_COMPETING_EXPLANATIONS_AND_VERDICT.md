# ARB-035 / 00 — Scientific thesis, rivals, and evidence verdict
**Research date:** 2026-10-31 (US market). **Status:** S0/S1 DOCUMENTARY RETURN, NOT independently reviewed; all SKU-level completed-sale and cross-retailer price-gap tests NOT EXECUTED.

## Jurisdiction and decision
ArbiScout is a **purchase-research index**, not a resale simulator. Its positive datum is a verified *current retailer total purchase price* below the robust **historical price actually paid in comparable completed eBay sales** for the identical item. A future sale, seller fee, return or expected profit is neither needed nor modeled.

**Observed sector winner: NONE.** No accepted live dataset in this task supplies joint SKU-level eBay paid-price histories, matched retailer purchaser prices and time-series stock, hence actual gap-yield rankings are **UNMEASURED**, not zero. eBay's 2025 Form 10-K reports focus categories (Motors P&A, collectibles, refurbished, apparel/luxury/sneakers), and 2025 category-relative growth, but not the requisite SKU-level paid-price distribution or retail markdown overlap [E01]. eBay Product Research documents a potential official human sales oracle for up to three years and actual accepted Best Offer consideration, not a verified bulk API [E02]. ARB-010 PR #4 and ARB-020 isolated branch are **UNADJUDICATED**, not production data [R01, R02].

## Mechanism: different attention budgets, not naive buyers
A **temporal, geographic, product-specific mismatch in search attention** is more plausible than a blanket difference in consumer intelligence. A buyer requiring a replacement OEM module may search by exact part number in an established eBay category while a merchant's liquidation promotion is indexed under store-specific inventory; a product specialist may know the part better than the retailer customer, yet not watch that merchant's clearance. Local pickup constraints and temporary inventory partitions can preserve an observed *purchase-price* difference even if both communities know the prices. By contrast, a LEGO or electronics enthusiast may subscribe to retailer drop alerts and diffuse a promotion before any software can use it. Price comparison may also be costly because SKU aliases, kits, condition, shipping or trust differ.

Economic foundations are conditional, not proof of this marketplace: Brynjolfsson & Smith (2000) identify persistent online price dispersion and retailer branding/trust effects; Brynjolfsson, Dick & Smith (2004) find search intensity does not imply uniformly greater price sensitivity; Ellison & Ellison (2009) examine price-search obfuscation, and Brown & Goolsbee (2002) show comparison tools can compress prices. None directly measures *2026 eBay buyer × clearance alert overlap* [E10–E13].

## Rival explanations and discriminating tests
| ID | Causal account | What would support it | What would falsify it |
|---|---|---|---|
| H1 | **Channel attention separation**: exact-item eBay search habitual; store clearance unseen | Representative linked shopping panel finds lower clearance monitoring among eBay buyers than matched nonbuyers; retailer sale-to-eBay adjustment lags | Overlapping cross-platform visits/alerts are high, adjustment quick |
| H2 | **Product/fitment urgency** drives eBay searches without price ignorance | Urgent replacement cohort searches part numbers despite known competing offers | Choice does not differ with urgency / buyers readily choose clearance source |
| H3 | **Geographic inventory segmentation** keeps store-only discount outside broader buyer market | Verified price/stock differences across ZIPs; gap lasts geographically | All regions buy online at same cheap shipped price and rapidly adjust |
| H4 | **Marketing/price-obfuscation**: manufacturer/retailer bundles hide comparisons | Alias / bundle normalization shrinks apparent gap systematically | Strict GTIN + contents + condition still produces similar positive gaps |
| H5 | **Vintage/obsolete model inelastic need** | Adequate same-model paid transactions remain at steady prices when outlet discounts appear | No sold volume, old sample is stale, revision/compatibility mismatches |
| H6 | **Enthusiast arbitrage attention** corrects differences *faster* than mainstream market | Retail alert posts and fast depletion or normal eBay price adjustment coincide | Promotions remain independently observable and stable for multi-day windows |
| H7 | **Historical-data artifact**: asking upper bounds, used/new mixing, survivor bias | Paid Best Offer truth, condition and shipping correction kills gaps | Official paid-price verified full-condition subset preserves gaps |
| H8 | **Trust/service non-price differentiation** | New authorized retailer vs eBay item has different return/warranty/bundle terms; price difference persists for service reasons | Controlled product and purchase terms remain equivalent |
| H9 | **Ordinary sale-cycle inventory clearing** | Manufacturer model change/quarter close precedes repeated price dips | No actual repeat dips after price time-series observation |
| H10 | **Broad commodity efficiency** | Well-known gaming/phones show high sales but rapid retail/eBay convergence | Comparable large positive differences survive equally often in highly tracked goods |

**Causal identification:** A recorded deal-thread post is evidence the sale entered a community, not the joint probability that an eBay buyer saw it. eBay's self-selected recommerce survey discusses value-seeking and trust, not exact-new-SKU price overlap [E03]. A contemporaneous specialist Reddit deal thread is a selected example and can *disconfirm absolute unawareness*, never establish population-level penetration [E15–E17].

## Executive decision (two different columns)
| Question | Demonstrated winner | Highest-priority experiments (NOT results) |
|---|---|---|
| Regular completed eBay demand by exact SKU | **NONE VERIFIED** | OEM auto replacement components; genuine tool batteries/handheld kits; sealed LEGO set numbers; camera lenses; branded networking; mainstream game systems as control |
| High-ticket absolute purchase gaps | **NONE VERIFIED** | Camera bodies/lenses, pro audio/interfaces, industrial/network devices, pro tool kits; condition and sparse history serious |
| Recurrent deep retailer markdowns | **No cadence measured** | Home Depot daily deals/partner feeds; Best Buy onSale; Adorama closeout; LEGO sale; Harbor Freight coupon cycles — *documented sale surfaces*, not longitudinal rate |
| Channel separation | **NO representative linked sample** | Local SKU clearance vs national eBay; obsolete repair parts; regional warehouse stock, with well-monitored collectibles as negative control |
| Source feasibility / exact matching | **Documentation only** | Best Buy official catalog; licensed ShopSavvy enumerated deals; approved merchant full feed; LEGO set number; OEM MPN; confirm contracts |
| Balanced purchase-gap yield | **NONE VERIFIED** | Automotive OEM modules × authorized parts supplier; tools × Home Depot; photography × Adorama/B&H; branded IT × Newegg/Best Buy; LEGO × Target/LEGO |
| Poor candidates/control cohorts | **No measured failure rates** | Giant furniture, white-label fashion, one-off watches, untraceable clearance, hyper-tracked Pokémon drops, accessories under $20 |

These research candidates are ranked by **expected diagnostic value and feasible tests**, not odds or likelihood of a positive gap. The priority order cannot be read as a sector sales-volume league table.

## Three verdicts
- **Empirical current paid-price / gap court: HOLD / NO VALID COMPARABLE SKU DATA.** There are real documentary *category* and *retailer page* observations, but zero matched completed-sale samples in this return.
- **Mechanism / cultural court: HYPOTHESES WITH COMPETING EXPLANATIONS.** Counterexamples undermine any claim that specialist buyers are oblivious to markdowns; linked-cohort evidence not available.
- **Purchase-research feasibility: DOCUMENTARY CONDITIONAL.** Public tools/feeds exist, actual use/permission and precision are unverified. No source paid call, live retailer checkout, eBay login or automated scraping executed.

## Evidence keys and dependencies
E01 eBay FY2025 10-K https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm
E02 eBay Product Research https://www.ebay.com/help/selling/selling-tools/research?id=4853
E03 eBay 2026 Recommerce https://www.ebayinc.com/recommerce-report/
E10–E17 academic and community records in 08 docket.
R01 https://github.com/maidiu/arbiscout/pull/4
R02 https://github.com/maidiu/arbiscout/tree/agent/arb020-retailer-source-universe-r1/CONTROL_ROOM/WORKERS/RETURNS/ARB-020-RETAILER-SOURCE-UNIVERSE-R1
**No claim here independently adopts R01/R02.**
