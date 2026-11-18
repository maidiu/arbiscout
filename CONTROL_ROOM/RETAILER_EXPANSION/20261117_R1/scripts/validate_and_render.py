#!/usr/bin/env python3
"""Validate the 54-source retailer workroom and optionally refresh generated dashboard."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = {"UNSTARTED", "EXISTING_SOURCE_RECHECK", "RESEARCHING", "ACCESS_HOLD",
          "MECHANISM_DOCUMENTED", "FIXTURE_VALIDATED", "LIVE_VALIDATED",
          "CATALOG_INTEGRATED", "REVIEWED_ACCEPTED"}
RECEIPT_TYPES = {"SOURCE_RECEIPT", "PAGING_RECEIPT", "PRICE_EXTRACTION_RECEIPT",
                 "IDENTITY_RECEIPT", "RIGHTS_RECEIPT", "CATALOG_RECEIPT",
                 "TEST_RECEIPT", "REVIEW_RECEIPT"}

def main():
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = p.parse_args()
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    research = json.loads((ROOT / "RESEARCH/MECHANISM_SPECIFICATIONS.json").read_text(encoding="utf-8"))
    assert len(manifest["cases"]) == len(research["rows"]) == 54, "Expected 54 source records"
    ids = [x["id"] for x in manifest["cases"]]
    assert len(ids) == len(set(ids)) == 54, "Duplicate/missing source ID"
    assert ids == [f"RET-{i:03d}" for i in range(1, 55)], "IDs/order drifted"
    assert ids == [x["id"] for x in research["rows"]], "Research/source inventory mismatch"
    statuses = {}
    for item in manifest["cases"]:
        f = ROOT / item["json"]
        assert f.is_file(), f"Missing treatment JSON: {f}"
        assert (ROOT / item["journal"]).is_file(), f"Missing treatment journal: {item['id']}"
        row = json.loads(f.read_text(encoding="utf-8"))
        assert row["source_id"] == item["id"] and row["name"] == item["name"], f"Identity drift {item['id']}"
        state = row["implementation_status"]
        assert state in STATES, f"Invalid status {item['id']}: {state}"
        assert isinstance(row.get("receipts"), list), f"Receipt index missing for {item['id']}"
        kinds = {r.get("type") for r in row["receipts"]}
        assert kinds <= RECEIPT_TYPES, f"Unknown receipt type in {item['id']}"
        if state in {"FIXTURE_VALIDATED", "LIVE_VALIDATED", "CATALOG_INTEGRATED", "REVIEWED_ACCEPTED"}:
            assert "TEST_RECEIPT" in kinds, f"Claimed tested without test receipt: {item['id']}"
        if state in {"LIVE_VALIDATED", "CATALOG_INTEGRATED", "REVIEWED_ACCEPTED"}:
            assert {"RIGHTS_RECEIPT", "SOURCE_RECEIPT", "PRICE_EXTRACTION_RECEIPT", "IDENTITY_RECEIPT"} <= kinds, f"Live claim without receipts: {item['id']}"
            assert row["rights_status"] == "AUTHORIZED_IN_SCOPE", f"Live claim without authorized scope: {item['id']}"
        if state in {"CATALOG_INTEGRATED", "REVIEWED_ACCEPTED"}:
            assert "CATALOG_RECEIPT" in kinds, f"Catalog integration without receipt: {item['id']}"
        if state == "REVIEWED_ACCEPTED":
            assert "REVIEW_RECEIPT" in kinds, f"Accepted without independent review: {item['id']}"
        statuses[state] = statuses.get(state, 0) + 1
    lines = ["# Retailer treatment dashboard", "",
             "**Derived from individual treatment JSON.** Research-backed source inventory: 54. Generated with `scripts/validate_and_render.py`; do not edit manually.", "",
             "| ID | Retailer/source | Mechanism family | Treatment status |",
             "|---|---|---|---|"]
    for item in manifest["cases"]:
        row = json.loads((ROOT / item["json"]).read_text(encoding="utf-8"))
        lines.append(f"| [{item['id']}]({item['journal']}) | {item['name'].replace('|', '/')} | {item['family']} | {row['implementation_status']} |")
    lines.extend(["", "## Status totals", ""])
    for name, count in sorted(statuses.items()):
        lines.append(f"- {name}: {count}")
    content = "\n".join(lines) + "\n"
    path = ROOT / "DASHBOARD.md"
    if args.write:
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}; {len(ids)} cases")
    else:
        assert path.read_text(encoding="utf-8") == content, "DASHBOARD.md stale: use --write"
        print(f"OK: {len(ids)} treatment files and receipts structurally checked")
if __name__ == "__main__":
    main()

