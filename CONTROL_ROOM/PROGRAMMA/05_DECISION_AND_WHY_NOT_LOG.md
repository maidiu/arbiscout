# Decisions and WHY-NOT — purchase-index constitution

**D01 — historical source-free PR #1:** A prior draft implemented product matching and an incompatible financial scoring design. This is **NOT the current application**; only generic exact-product functions may be independently reviewed for reuse. PR #1 is unmerged. Do not import nonconforming scoring.

**D02 — actual eBay history:** Use regular patterns of same-item **completed eBay sales** where genuinely observed and comparable. Active asking prices, anomalous one-off transactions and unreliable inferred prices do not prove ordinary historical sale levels.

**D03 — 0–10 truthful results:** Never pad daily output. A day with zero statistically defensible purchase-price gaps is a successful refusal, not failure.

**D04 — retailer API applicability:** Evaluate the actual retailer **purchase-research/indexing** use; do not assume the software exists for a competing retailer or a later transaction. Best Buy's purchase-offer API may fit its positive sales-related use language; relevant real API contract provisions still require exact examination. Walmart affiliate terms are narrower than ordinary Walmart checkout availability, but no generic affiliate-feed rights may be presumed.

**D05 — Google Shopping:** Google Merchant API is merchant-specific; external Google Shopping search-result feeds are separate providers. The unsolved practical question is whether broad bargain discovery is achievable without known-product queries.

**D06 — imports:** AliExpress/Alibaba can become additional offered acquisition-price sources. Relevant quantities, delivery costs and time belong to purchase comparison; no later outcome constitutes the application.

**D07 — Rawlsing:** Borrow HQ method, source custody, dependency discipline, honest negative/unknown, independent review and return reconciliation. Rawlsing PRE-MAIN/Pyat/Sorok authority does not transfer.

**D08 — separate drafts:** Draft PR #1 and this PROGRAMMA control-room draft PR #2 are independent. Neither is merged. Do not advertise code from PR #1 as current gap ranking.

**D09 — controlling product revision:** ArbiScout is exclusively **purchase research indexed on retailer prices maximally below regular comparable eBay actual completed-sale history**. All earlier specifications defining a future commercial transaction are superseded; preserve history without restoring those as active work.

**D10 — priority and records (2026-10-31):** Maintain 39 structured task nodes and all 95 reviewed research questions. Canonical records are JSON; Markdown/CSV are generated views. Hard ALL-OF tasks, ANY-OF alternative sources, live acceptance gates and nonblocking related work are separate. Each question carries its prerequisites, related work, operational proof needs, status, findings, references and P0–P3 urgency.

**How to amend:** Record dated new source/term/code/test evidence and exact scope, compare with previous decision, update the governing JSON task/questions/source record and next action, regenerate views and require GitHub CI. Never call a source URL alone a substantive research answer.
