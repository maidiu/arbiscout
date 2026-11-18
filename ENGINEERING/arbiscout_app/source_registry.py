#!/usr/bin/env python3
"""Source-neutral retailer registry and 54-case coverage ledger.

The research dossier documents 54 merchant/source mechanisms. This module keeps
the coverage honest: four adapters are implemented locally; the rest are HOLD
with their exact rights/evidence blockers. No selectors or endpoints are
invented for sources without a capture.
"""
from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
SPECS_PATH = APP_DIR / "sources" / "mechanism_specifications.json"

IMPLEMENTED = {
    "RET-001": {"adapter": "arbiscout.py (browser listing + extractors)",
                 "receipt": "sources/receipts/RET-001.json"},
    "RET-046": {"adapter": "providers.py (Woot API feed + /getoffers)",
                 "receipt": "sources/receipts/RET-046.json"},
    "RET-047": {"adapter": "providers.py (Meh current-deal API)",
                 "receipt": "sources/receipts/RET-047.json"},
    "RET-048": {"adapter": "providers.py (Kroger OAuth products/locations)",
                 "receipt": "sources/receipts/RET-048.json"},
}

STATUS_ORDER = [
    "IMPLEMENTED_LOCAL",
    "HOLD_RIGHTS",
    "HOLD_APPROVED_FEED",
    "HOLD_TERMS",
    "HOLD_NEEDS_CAPTURE",
    "HOLD_EVIDENCE",
]


def load_rows():
    if not SPECS_PATH.is_file():
        return []
    return json.loads(SPECS_PATH.read_text(encoding="utf-8")).get("rows", [])


def _status(row):
    if row.get("id") in IMPLEMENTED:
        return "IMPLEMENTED_LOCAL"
    gate = row.get("access_gate", "") or ""
    if gate in ("EXPLICIT_SITE_RESTRICTION", "PUBLISHED_AFFILIATE_CONFLICT"):
        return "HOLD_RIGHTS"
    if any(part in gate for part in ("APPROVED_FEED", "CJ_", "BRAND_APPROVAL",
                                     "PARTNER_APPROVAL", "ACTIVE_FEED")):
        return "HOLD_APPROVED_FEED"
    if "TERMS" in gate or "API" in gate or "PERMISSION" in gate or "RIGHTS" in gate:
        return "HOLD_TERMS"
    if "UNKNOWN_NEEDS_SAVED_HTML" in (row.get("selector_status") or ""):
        return "HOLD_NEEDS_CAPTURE"
    return "HOLD_EVIDENCE"


def _blocker(row, status):
    if status == "IMPLEMENTED_LOCAL":
        return "Local adapter works; live rights/terms review and independent acceptance remain open."
    if status == "HOLD_RIGHTS":
        return "Documented site restriction or affiliate/terms conflict; do not automate without permission."
    if status == "HOLD_APPROVED_FEED":
        return "Approved feed/partner brand access is required."
    if status == "HOLD_TERMS":
        return "Terms/API permission review is required before collection."
    if status == "HOLD_NEEDS_CAPTURE":
        return "No saved HTML capture; selectors, pagination and price roles are unverified."
    return "Mechanism or evidence is not proven."


def _next_action(row, status):
    action = (row.get("recommended_action") or "").strip()
    if action:
        return action
    if status == "IMPLEMENTED_LOCAL":
        return "Obtain independent rights review and re-run the live canary."
    return "Obtain authorized page 1/page 2 captures and record selectors, price roles, pagination and variants."


def coverage_rows():
    rows = []
    for row in load_rows():
        status = _status(row)
        rows.append({
            "id": row.get("id"),
            "name": row.get("name"),
            "category": row.get("category"),
            "family": row.get("family") or row.get("mechanism_family"),
            "evidence_status": row.get("confidence") or row.get("evidence_status"),
            "access_gate": row.get("access_gate"),
            "selector_status": row.get("selector_status"),
            "status": status,
            "blocker": _blocker(row, status),
            "next_action": _next_action(row, status),
            "adapter": IMPLEMENTED.get(row.get("id"), {}).get("adapter"),
            "receipt": IMPLEMENTED.get(row.get("id"), {}).get("receipt"),
            "production_ready": False,
        })
    return rows


def summary():
    rows = coverage_rows()
    counts = {key: 0 for key in STATUS_ORDER}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {"total": len(rows), "counts": counts,
            "implemented": [row["name"] for row in rows if row["status"] == "IMPLEMENTED_LOCAL"],
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def coverage_markdown():
    rows = coverage_rows()
    info = summary()
    lines = [
        "# ArbiScout retailer source coverage — 54 cases",
        "",
        f"Generated: {info['generated_at']}",
        "",
        f"**{info['counts'].get('IMPLEMENTED_LOCAL', 0)} implemented locally; "
        f"{info['total'] - info['counts'].get('IMPLEMENTED_LOCAL', 0)} HOLD.**",
        "",
        "HOLD is deliberate: no saved capture, rights review or approved feed means no live adapter and no fabricated products.",
        "",
        "| ID | Source | Mechanism | Evidence | Access gate | Status | Blocker | Next action |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        values = [row["id"], row["name"], row["family"], row["evidence_status"],
                  row["access_gate"], row["status"], row["blocker"], row["next_action"]]
        lines.append("| " + " | ".join(str(v or "").replace("|", "\\|") for v in values) + " |")
    return "\n".join(lines) + "\n"


def main():
    output = APP_DIR / "sources"
    output.mkdir(parents=True, exist_ok=True)
    (output / "coverage_ledger.json").write_text(
        json.dumps({"summary": summary(), "rows": coverage_rows()}, indent=2,
                   ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "coverage_ledger.md").write_text(coverage_markdown(), encoding="utf-8")
    info = summary()
    print(f"Coverage: {info['total']} sources; "
          f"{info['counts'].get('IMPLEMENTED_LOCAL', 0)} implemented locally; "
          f"{info['total'] - info['counts'].get('IMPLEMENTED_LOCAL', 0)} HOLD")
    print("Ledger:", (output / "coverage_ledger.md").resolve())


if __name__ == "__main__":
    main()
