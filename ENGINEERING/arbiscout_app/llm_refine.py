#!/usr/bin/env python3
"""Optional LLM identity refinement for already-extracted saved eBay listings.

The LLM only filters listings that the local parser already extracted. It never
fetches eBay, invents listings or creates prices. Only sanitized structured
records are sent; raw HTML, cookies and credentials are not.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import re
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import ebay_comparison as ebay
import run_test

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

ROOT = Path(__file__).resolve().parent
PROMPT_VERSION = "retailer-identity-v1"
ALLOWED_VERDICTS = {"EXACT_MATCH", "WRONG_CONFIG", "WRONG_MODEL",
                    "USED_OR_REFURB", "PARTS_OR_DAMAGED", "UNKNOWN"}
USED_RE = re.compile(r"\b(?:used|pre[ -]?owned|refurbished|renewed|open[ -]?box|"
                     r"scratch(?:ed|es)?|dent(?:ed|s)?|for parts|repair only)\b", re.I)
SYSTEM_PROMPT = (
    "You are a strict product-identity adjudicator for purchase research. "
    "You receive one retailer offer and sold eBay listings already extracted by a local parser. "
    "Your only job is to remove listings that are not the same item. "
    "Never invent listings, prices, dates or attributes. If the title does not prove the "
    "configuration or condition, return UNKNOWN. Return JSON only, with no prose."
)
USER_RULES = (
    "Classify every listing. EXACT_MATCH only when the model and configuration match and "
    "the condition is comparable. Reject WRONG_MODEL, WRONG_CONFIG (RAM, storage, CPU/GPU, "
    "screen, bundle, quantity), USED_OR_REFURB when the retailer offer is new, PARTS_OR_DAMAGED, "
    "and UNKNOWN when evidence is insufficient. Preserve the exact item_id. "
    'Return {"listings":[{"item_id":"...","verdict":"EXACT_MATCH|WRONG_CONFIG|'
    'WRONG_MODEL|USED_OR_REFURB|PARTS_OR_DAMAGED|UNKNOWN","confidence":0.0,'
    '"reason":"...","attributes":{"model":null,"ram":null,"storage":null,'
    '"condition":null}}]}.'
)


def load_env(path=ROOT / ".env"):
    if not Path(path).is_file():
        return
    for raw in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[7:].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key, value)


def env(*names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value.strip()
    return ""


def retailer_payload(product):
    return {key: product.get(key) for key in (
        "key", "title", "model", "mpn", "sku", "brand", "condition",
        "category", "current_price", "regular_price", "variant_count",
        "kroger_zip", "url") if product.get(key) is not None}


def listing_payload(observation):
    return {key: observation.get(key) for key in (
        "item_id", "title", "displayed_price", "paid_price", "price_status",
        "sold_at", "item_url") if observation.get(key) is not None}


def listing_id(observation):
    return str(observation.get("item_id") or hashlib.sha256(
        json.dumps(listing_payload(observation), sort_keys=True).encode()).hexdigest()[:20])


def cache_key(model, retailer, listing):
    raw = json.dumps({"model": model, "retailer": retailer, "listing": listing},
                     sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def prompt_payload(retailer, listings):
    return {"retailer": retailer, "sold_listings": listings}


def parse_llm_content(content):
    text = (content or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("LLM response did not contain a JSON object")
    return json.loads(text[start:end + 1])


def normalize_verdicts(payload, valid_ids):
    items = payload.get("listings") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("LLM response did not contain a listings array")
    out = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("item_id") or "")
        if item_id not in valid_ids:
            continue
        verdict = str(item.get("verdict") or "UNKNOWN").upper().replace(" ", "_")
        if verdict not in ALLOWED_VERDICTS:
            verdict = "UNKNOWN"
        try:
            confidence = max(0.0, min(1.0, float(item.get("confidence", 0))))
        except (TypeError, ValueError):
            confidence = 0.0
        out[item_id] = {
            "verdict": verdict,
            "confidence": confidence,
            "reason": str(item.get("reason") or "")[:500],
            "attributes": item.get("attributes") if isinstance(item.get("attributes"), dict) else {},
        }
    return out


def post_json(url, payload, api_key, timeout=90):
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + api_key,
                 "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
        data = response.read(4_000_001)
        if len(data) > 4_000_000:
            raise RuntimeError("LLM response larger than safe maximum")
        return json.loads(data.decode("utf-8", errors="replace"))


def call_llm(base_url, api_key, model, retailer, listings, timeout=90):
    url = base_url.rstrip("/") + "/chat/completions"
    user = USER_RULES + "\n\n" + json.dumps(prompt_payload(retailer, listings),
                                            indent=2, ensure_ascii=False)
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": user}],
    }
    try:
        data = post_json(url, {**payload, "response_format": {"type": "json_object"}},
                         api_key, timeout)
    except HTTPError as exc:
        if exc.code not in (400, 422):
            raise
        data = post_json(url, payload, api_key, timeout)
    except URLError as exc:
        raise RuntimeError("LLM connection failed: " + str(exc)[:200]) from exc
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected LLM response shape") from exc
    return parse_llm_content(content)


def load_products(output):
    selection = output / "selection.json"
    if selection.is_file():
        data = json.loads(selection.read_text(encoding="utf-8"))
        return data.get("products") or []
    products = output / "retailer" / "products.json"
    if products.is_file():
        return json.loads(products.read_text(encoding="utf-8"))
    return []


def load_observations(output):
    path = output / "comparisons" / "sold_observations.json"
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def load_comparisons(output):
    path = output / "comparisons" / "comparisons.json"
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def load_cache(path):
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (ValueError, OSError):
        return {}


def write_top10(output, records, receipt):
    winners = run_test.rank_provisional(records, 10)
    (output / "top10.json").write_text(json.dumps(winners, indent=2) + "\n", encoding="utf-8")
    fields = ["rank", "retailer_key", "title", "retailer_url", "retailer_current_price",
              "retailer_regular_price", "kroger_zip", "kroger_location_id",
              "ebay_sold_url", "ebay_sold_low_30d", "ebay_sold_high_30d",
              "ebay_sold_mean_30d", "ebay_typical_low_30d", "ebay_typical_high_30d",
              "ebay_displayed_median_30d", "bestbuy_below_ebay_low",
              "indicative_gap_dollars", "indicative_gap_percent",
              "matched_displayed_sales", "evidence_status"]
    with (output / "top10.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(winners)
    (output / "index.html").write_text(run_test.render_dashboard(winners, receipt),
                                       encoding="utf-8")
    return winners


def refine(output, model, base_url, api_key, min_confidence=0.8, max_listings=120):
    output = Path(output)
    products = load_products(output)
    observations = load_observations(output)
    existing = {row.get("retailer", {}).get("key"): row for row in load_comparisons(output)}
    receipt_path = output / "run_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.is_file() else {}
    receipt.setdefault("synthetic_demo", False)
    receipt.setdefault("selected_retail_offers", len(products))
    receipt.setdefault("positive_provisional_count", 0)
    receipt.setdefault("top_ten_count", 0)
    receipt.setdefault("actual_paid_verified_count", 0)
    as_of = datetime.now(timezone.utc)
    if receipt.get("as_of_utc"):
        try:
            as_of = datetime.fromisoformat(receipt["as_of_utc"])
        except ValueError:
            pass
    by_retailer = {}
    for observation in observations:
        by_retailer.setdefault(observation.get("retailer_key"), []).append(observation)
    cache_path = output / "comparisons" / "llm_cache.json"
    cache = load_cache(cache_path)
    records = []
    retailer_reports = []
    total_listings = total_exact = total_removed = total_unknown = 0

    for product in products:
        key = product.get("key") or product.get("url") or product.get("title")
        source_observations = by_retailer.get(key, [])[:max_listings]
        if not source_observations:
            continue
        retailer = retailer_payload(product)
        listings = [listing_payload(o) for o in source_observations]
        valid_ids = {listing_id(o) for o in source_observations}
        verdicts = {}
        pending = []
        for observation in source_observations:
            lid = listing_id(observation)
            ck = cache_key(model, retailer, listing_payload(observation))
            cached = cache.get(ck)
            if cached and cached.get("verdict") in ALLOWED_VERDICTS:
                verdicts[lid] = cached
            else:
                pending.append((lid, ck, listing_payload(observation)))
        for start in range(0, len(pending), 40):
            batch = pending[start:start + 40]
            payload = call_llm(base_url, api_key, model, retailer,
                               [item[2] for item in batch])
            parsed = normalize_verdicts(payload, {item[0] for item in batch})
            for lid, ck, _listing in batch:
                verdict = parsed.get(lid) or {
                    "verdict": "UNKNOWN", "confidence": 0.0,
                    "reason": "LLM did not return a verdict", "attributes": {}}
                verdicts[lid] = verdict
                cache[ck] = verdict

        exact = []
        unknown = 0
        for observation in source_observations:
            lid = listing_id(observation)
            verdict = verdicts.get(lid) or {"verdict": "UNKNOWN", "confidence": 0.0}
            if verdict["verdict"] == "EXACT_MATCH" and verdict["confidence"] >= min_confidence:
                title = str(observation.get("title") or "")
                if str(product.get("condition") or "").lower() == "new" and USED_RE.search(title):
                    verdict = {**verdict, "verdict": "USED_OR_REFURB",
                               "reason": "Deterministic condition guard"}
                elif observation.get("price_status") in ("UNKNOWN_ACCEPTED_OFFER", "AMBIGUOUS_RANGE"):
                    verdict = {**verdict, "verdict": "UNKNOWN",
                               "reason": "Price status is not a usable displayed sale"}
                else:
                    exact.append(observation)
            if verdict["verdict"] == "UNKNOWN":
                unknown += 1
        comparison = ebay.qualify(product, exact, as_of)
        comparison["diagnostics"]["llm_exact"] = len(exact)
        comparison["diagnostics"]["llm_removed"] = len(source_observations) - len(exact)
        comparison["diagnostics"]["llm_unknown"] = unknown
        previous = existing.get(key, {})
        record = {
            "retailer": product,
            "ebay_search_url": previous.get("ebay_search_url") or ebay.search_url(
                product.get("ebay_query") or product.get("title") or ""),
            "ebay_status": "LLM_REFINED" if exact else "NO_LLM_EXACT_MATCH",
            "fixture_index": previous.get("fixture_index"),
            "fixture_file": previous.get("fixture_file") or "LLM refined",
            "comparison": comparison,
            "llm_refinement": {
                "model": model,
                "prompt_version": PROMPT_VERSION,
                "listings": len(source_observations),
                "exact": len(exact),
                "removed": len(source_observations) - len(exact),
                "unknown": unknown,
                "min_confidence": min_confidence,
            },
        }
        records.append(record)
        retailer_reports.append({
            "key": key, "title": product.get("title"),
            "listings": len(source_observations), "exact": len(exact),
            "removed": len(source_observations) - len(exact),
            "unknown": unknown, "sample_count": comparison["sample_count"],
            "median": comparison.get("historical_median"), "gap": comparison.get("gap"),
            "verdicts": [{"item_id": listing_id(o), **verdicts.get(listing_id(o), {})}
                         for o in source_observations],
        })
        total_listings += len(source_observations)
        total_exact += len(exact)
        total_removed += len(source_observations) - len(exact)
        total_unknown += unknown

    output.mkdir(parents=True, exist_ok=True)
    (output / "comparisons").mkdir(parents=True, exist_ok=True)
    raw_path = output / "comparisons" / "comparisons_raw.json"
    current_path = output / "comparisons" / "comparisons.json"
    if not raw_path.is_file() and current_path.is_file():
        raw_path.write_text(current_path.read_text(encoding="utf-8"), encoding="utf-8")
    (output / "comparisons" / "comparisons.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "comparisons" / "comparisons_llm.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    summary = {
        "ok": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "prompt_version": PROMPT_VERSION,
        "min_confidence": min_confidence,
        "retailers": retailer_reports,
        "listings": total_listings,
        "exact": total_exact,
        "removed": total_removed,
        "unknown": total_unknown,
    }
    (output / "comparisons" / "llm_verdicts.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    receipt["llm_refinement"] = {
        "model": model, "prompt_version": PROMPT_VERSION,
        "min_confidence": min_confidence, "listings": total_listings,
        "exact": total_exact, "removed": total_removed, "unknown": total_unknown,
        "generated_at": summary["generated_at"],
    }
    receipt["source_mode"] = "LLM_REFINED_SAVED_EBAY_HTML"
    receipt["positive_provisional_count"] = sum(
        1 for row in records
        if row["comparison"].get("status") == "PROVISIONAL_SOLD_DISPLAY_COMPARISON"
        and (row["comparison"].get("gap") or 0) > 0)
    receipt["top_ten_count"] = len(run_test.rank_provisional(records, 10))
    receipt["source_status_counts"] = {}
    for row in records:
        status = row.get("ebay_status")
        receipt["source_status_counts"][status] = receipt["source_status_counts"].get(status, 0) + 1
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    write_top10(output, records, receipt)
    return summary


def main(argv=None):
    load_env()
    parser = argparse.ArgumentParser(description="Optional LLM identity refinement for saved eBay evidence")
    parser.add_argument("--output", default="catalog/selected")
    parser.add_argument("--model", default=env("LLM_MODEL") or "deepseek-chat")
    parser.add_argument("--base-url", default=env("LLM_BASE_URL") or "https://api.deepseek.com/v1")
    try:
        default_confidence = float(env("LLM_MIN_CONFIDENCE") or "0.8")
    except ValueError:
        default_confidence = 0.8
    parser.add_argument("--min-confidence", type=float, default=default_confidence)
    parser.add_argument("--max-listings", type=int, default=120)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    api_key = env("LLM_API_KEY", "DEEPSEEK_API_KEY")
    if not api_key:
        print("Missing LLM_API_KEY or DEEPSEEK_API_KEY in .env or the environment.", file=sys.stderr)
        return 2
    try:
        summary = refine(Path(args.output), args.model, args.base_url, api_key,
                         args.min_confidence, args.max_listings)
    except Exception as exc:
        print("LLM refinement failed: " + str(exc)[:500], file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(f"LLM refinement: {summary['exact']} exact / {summary['removed']} removed "
              f"from {summary['listings']} listing(s) using {summary['model']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
