"""Source-free CLI for reviewing explicitly supplied market observations."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .core import rank


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Rank evidence-backed resale opportunities from a JSON file")
    p.add_argument("input", type=Path, help="JSON containing assumptions and candidates")
    p.add_argument("--as-of", type=date.fromisoformat, default=date.today(), help="YYYY-MM-DD; for reproducible results")
    p.add_argument("--top", type=int, default=10, help="maximum number of eligible results")
    args = p.parse_args(argv)
    if args.top < 1:
        p.error("--top must be positive")
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not isinstance(raw.get("assumptions"), dict) or not isinstance(raw.get("candidates"), list):
            raise ValueError("expected top-level 'assumptions' object and 'candidates' array")
        if any(not isinstance(candidate, dict) for candidate in raw["candidates"]):
            raise ValueError("each candidate must be an object")
        results = rank(raw["candidates"], raw["assumptions"], args.as_of)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        p.exit(2, f"Input error: {exc}\n")
    eligible = [r for r in results if r["status"].startswith("ELIGIBLE")]
    print(f"ArbiScout | as-of {args.as_of} | {len(eligible)}/{len(results)} eligible (VERIFY BEFORE BUYING)")
    for index, r in enumerate(eligible[:args.top], 1):
        estimate = r["estimates"]
        print(f"{index}. {r['name']} | est. profit ${estimate['profit']} | ROI {estimate['roi_pct']}% | sold/30d {estimate['sold_count_30d']} | {r['id']}")
    other = [r for r in results if not r["status"].startswith("ELIGIBLE")]
    if other:
        print("\nNot recommended / needs review:")
        for r in other:
            print(f"- {r['name']}: {'; '.join(r['reasons'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
