#!/usr/bin/env python3
"""Optional LLM identity refinement for already-extracted saved eBay listings.

The LLM only adjudicates identity. It never calculates medians or gaps, never
fetches eBay and never invents listings or prices. Only compact identity fields
are sent: retailer id/title/model/condition and listing id/title.
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
PROMPT_VERSION = "retailer-identity-v2"
ALLOWED_VERDICTS = {"EXACT_MATCH", "WRONG_CONFIG", "WRONG_MODEL",
                    "USED_OR_REFURB", "PARTS_OR_DAMAGED", "UNKNOWN"}
USED_RE = re.compile(r"\b(?:used|pre[ -]?owned|refurbished|renewed|open[ -]?box|"
                     r"scratch(?:ed|es)?|dent(?:ed|s)?|for parts|repair only)\b", re.I)
SYSTEM_PROMPT = (
    "You are a practical product-identity filter for purchase research. "
    "You receive several retailer offers and their sold eBay listing titles, already "
    "extracted by a local parser. Remove only listings that are obviously a different "
    "product. Do not require every retailer specification to appear in the sold title: "
    "missing optional specs or missing condition are not contradictions. If the listing "
    "clearly names the same brand, model/family and product type, mark EXACT_MATCH. "
    "Do not calculate prices, medians, gaps or profits. Never invent listings, prices, "
    "dates or attributes. Return JSON only, with no prose."
)
USER_RULES = (
    "Classify every listing. EXACT_MATCH only when the model and configuration match and "
    "the condition is comparable. Reject WRONG_MODEL, WRONG_CONFIG (RAM, storage, CPU/GPU, "
    "screen, bundle, quantity), USED_OR_REFURB when the retailer offer is new, PARTS_OR_DAMAGED, "
    "and UNKNOWN when evidence is insufficient. Echo retailer_id and item_id exactly. "
    'Return {"listings":[{"retailer_id":"...","item_id":"...",'
    '"verdict":"EXACT_MATCH|WRONG_CONFIG|WRONG_MODEL|USED_OR_REFURB|'
    'PARTS_OR_DAMAGED|UNKNOWN","confidence":0.0,"reason":"...",'
    '"attributes":{"model":null,"ram":null,"storage":null,"condition":null}}]}.'
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


def listing_id(observation):
    if observation.get("item_id"):
        return str(observation["item_id"])
    raw = json.dumps({"title": observation.get("title")}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def retailer_identity(product):
    return {key: product.get(key) for key in (
        "title", "model", "mpn", "sku", "brand", "condition", "category")
        if product.get(key) is not None}


def listing_identity(observation):
    return {"item_id": listing_id(observation), "title": observation.get("title") or "",
            "condition": observation.get("condition") or "UNKNOWN"}


def observations_fingerprint(observations):
    payload = [{key: observation.get(key) for key in
                ("item_id", "title", "displayed_price", "sold_at", "price_status")}
               for observation in observations]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest()


def cache_key(model, retailer_id, retailer, listing):
    raw = json.dumps({"model": model, "prompt_version": PROMPT_VERSION,
                      "retailer_id": retailer_id, "retailer": retailer,
                      "listing": listing},
                     sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_llm_content(content):
    text = (content or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("LLM response did not contain a JSON object")
    return json.loads(text[start:end + 1])


def normalize_verdicts(payload, valid_pairs):
    items = payload.get("listings") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("LLM response did not contain a listings array")
    out = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        pair = (str(item.get("retailer_id") or ""), str(item.get("item_id") or ""))
        if pair not in valid_pairs:
            continue
        verdict = str(item.get("verdict") or "UNKNOWN").upper().replace(" ", "_")
        if verdict not in ALLOWED_VERDICTS:
            verdict = "UNKNOWN"
        try:
            confidence = max(0.0, min(1.0, float(item.get("confidence", 0))))
        except (TypeError, ValueError):
            confidence = 0.0
        out[pair] = {
            "verdict": verdict,
            "confidence": confidence,
            "reason": str(item.get("reason") or "")[:500],
            "attributes": item.get("attributes") if isinstance(item.get("attributes"), dict) else {},
        }
    return out


def post_json(url, payload, api_key, timeout=120):
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


def call_llm(base_url, api_key, model, retailers, timeout=120):
    url = base_url.rstrip("/") + "/chat/completions"
    user = USER_RULES + "\n\n" + json.dumps({"retailers": retailers},
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


def payload_chars(retailers):
    return len(json.dumps({"retailers": retailers}, separators=(",", ":"),
                          ensure_ascii=False))


def build_jobs(retailers, max_chars):
    if not retailers:
        return []
    if payload_chars(retailers) <= max_chars:
        return [{"retailers": retailers}]
    jobs = []
    current = []
    for item in retailers:
        if payload_chars([item]) > max_chars:
            if current:
                jobs.append({"retailers": current})
                current = []
            chunk = []
            for listing in item.get("listings", []):
                trial = {**item, "listings": chunk + [listing]}
                if chunk and payload_chars([trial]) > max_chars:
                    jobs.append({"retailers": [{**item, "listings": chunk}]})
                    chunk = []
                chunk.append(listing)
            if chunk:
                jobs.append({"retailers": [{**item, "listings": chunk}]})
            continue
        trial = current + [item]
        if current and payload_chars(trial) > max_chars:
            jobs.append({"retailers": current})
            current = [item]
        else:
            current = trial
    if current:
        jobs.append({"retailers": current})
    return jobs


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


def refine(output, model, base_url, api_key, min_confidence=0.8, max_listings=500,
           only_keys=None, max_input_chars=80000):
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
    only = set(only_keys or [])
    selected = []
    pending_groups = []
    for product in products:
        key = product.get("key") or product.get("url") or product.get("title")
        if only and key not in only:
            continue
        source_observations = by_retailer.get(key, [])[:max_listings]
        if not source_observations:
            continue
        retailer = retailer_identity(product)
        pending = []
        for observation in source_observations:
            lid = listing_id(observation)
            listing = listing_identity(observation)
            ck = cache_key(model, key, retailer, listing)
            cached = cache.get(ck)
            if not (cached and cached.get("verdict") in ALLOWED_VERDICTS):
                pending.append({"item_id": lid, "title": listing["title"],
                                "condition": listing.get("condition")})
        if pending:
            pending_groups.append({"retailer_id": key, "retailer": retailer,
                                   "listings": pending})
        selected.append((key, product, source_observations, retailer))

    jobs = build_jobs(pending_groups, max_input_chars)
    input_chars = 0
    for job in jobs:
        input_chars += payload_chars(job["retailers"])
        payload = call_llm(base_url, api_key, model, job["retailers"])
        valid_pairs = {(r["retailer_id"], listing["item_id"])
                       for r in job["retailers"] for listing in r["listings"]}
        parsed = normalize_verdicts(payload, valid_pairs)
        for retailer_id, _retailer, listings in (
                (r["retailer_id"], r["retailer"], r["listings"]) for r in job["retailers"]):
            for listing in listings:
                pair = (retailer_id, listing["item_id"])
                verdict = parsed.get(pair) or {
                    "verdict": "UNKNOWN", "confidence": 0.0,
                    "reason": "LLM did not return a verdict", "attributes": {}}
                ck = cache_key(model, retailer_id, _retailer, listing)
                cache[ck] = verdict

    records = []
    retailer_reports = []
    total_listings = total_exact = total_removed = total_unknown = 0
    for key, product, source_observations, retailer in selected:
        verdicts = {}
        for observation in source_observations:
            lid = listing_id(observation)
            ck = cache_key(model, key, retailer, listing_identity(observation))
            verdicts[lid] = cache.get(ck) or {
                "verdict": "UNKNOWN", "confidence": 0.0,
                "reason": "No cached or returned verdict", "attributes": {}}
        exact = []
        unknown = 0
        for observation in source_observations:
            lid = listing_id(observation)
            verdict = verdicts.get(lid) or {"verdict": "UNKNOWN", "confidence": 0.0}
            if verdict["verdict"] == "EXACT_MATCH" and verdict["confidence"] >= min_confidence:
                title = str(observation.get("title") or "")
                if str(product.get("condition") or "").lower() == "new" and (
                        USED_RE.search(title) or observation.get("condition") in
                        ("USED", "REFURBISHED", "OPEN_BOX", "PARTS")):
                    verdict = {**verdict, "verdict": "USED_OR_REFURB",
                               "reason": "Deterministic condition guard"}
                elif ebay.BAD_MATCH.search(title):
                    verdict = {**verdict, "verdict": "PARTS_OR_DAMAGED",
                               "reason": "Deterministic parts/bundle guard"}
                elif observation.get("price_status") in ("UNKNOWN_ACCEPTED_OFFER", "AMBIGUOUS_RANGE"):
                    verdict = {**verdict, "verdict": "UNKNOWN",
                               "reason": "Price status is not a usable displayed sale"}
                else:
                    exact.append(observation)
            if verdict["verdict"] == "UNKNOWN":
                unknown += 1
        comparison = ebay.qualify(product, exact, as_of, identity_verified=True)
        before = (existing.get(key) or {}).get("comparison") or {}
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
            "llm_checked": True,
            "llm_refinement": {
                "model": model, "prompt_version": PROMPT_VERSION,
                "listings": len(source_observations), "exact": len(exact),
                "removed": len(source_observations) - len(exact), "unknown": unknown,
                "min_confidence": min_confidence, "jobs": len(jobs),
                "input_chars": input_chars,
                "before_sample_count": before.get("sample_count"),
                "before_median": before.get("historical_median"),
                "before_gap": before.get("gap"),
                "after_sample_count": comparison.get("sample_count"),
                "after_median": comparison.get("historical_median"),
                "after_gap": comparison.get("gap"),
                "evidence_fingerprint": observations_fingerprint(source_observations),
            },
        }
        records.append(record)
        retailer_reports.append({
            "key": key, "title": product.get("title"),
            "listings": len(source_observations), "exact": len(exact),
            "removed": len(source_observations) - len(exact), "unknown": unknown,
            "sample_count": comparison["sample_count"],
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
    raw_records = []
    if raw_path.is_file():
        try:
            raw_records = json.loads(raw_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raw_records = []
    base = raw_records or list(existing.values())
    processed = {row.get("retailer", {}).get("key"): row for row in records}
    merged = []
    for row in base:
        key = row.get("retailer", {}).get("key")
        merged.append(processed.pop(key, row))
    merged.extend(processed.values())
    records = merged
    (output / "comparisons" / "comparisons.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "comparisons" / "comparisons_llm.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    summary = {
        "ok": True, "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": model, "prompt_version": PROMPT_VERSION,
        "min_confidence": min_confidence, "jobs": len(jobs),
        "input_chars": input_chars, "retailers": retailer_reports,
        "listings": total_listings, "exact": total_exact,
        "removed": total_removed, "unknown": total_unknown,
    }
    (output / "comparisons" / "llm_verdicts.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    receipt["llm_refinement"] = {
        "model": model, "prompt_version": PROMPT_VERSION,
        "min_confidence": min_confidence, "jobs": len(jobs),
        "input_chars": input_chars, "listings": total_listings,
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
    parser.add_argument("--model", default=env("LLM_MODEL", "DEEPSEEK_MODEL") or "deepseek-chat")
    parser.add_argument("--base-url",
                        default=env("LLM_BASE_URL", "DEEPSEEK_BASE_URL") or "https://api.deepseek.com/v1")
    try:
        default_confidence = float(env("LLM_MIN_CONFIDENCE") or "0.8")
    except ValueError:
        default_confidence = 0.8
    try:
        default_chars = int(env("LLM_MAX_INPUT_CHARS") or "80000")
    except ValueError:
        default_chars = 80000
    parser.add_argument("--min-confidence", type=float, default=default_confidence)
    parser.add_argument("--max-listings", type=int, default=500)
    parser.add_argument("--max-input-chars", type=int, default=default_chars)
    parser.add_argument("--keys-file", help="JSON file containing only the retailer keys to refine")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    api_key = env("LLM_API_KEY", "DEEPSEEK_API_KEY")
    if not api_key:
        print("Missing LLM_API_KEY or DEEPSEEK_API_KEY in .env or the environment.", file=sys.stderr)
        return 2
    only_keys = None
    if args.keys_file:
        try:
            raw_keys = json.loads(Path(args.keys_file).read_text(encoding="utf-8"))
            only_keys = raw_keys if isinstance(raw_keys, list) else raw_keys.get("keys", [])
        except (OSError, ValueError) as exc:
            print("Could not read --keys-file: " + str(exc), file=sys.stderr)
            return 2
    try:
        summary = refine(Path(args.output), args.model, args.base_url, api_key,
                         args.min_confidence, args.max_listings, only_keys,
                         args.max_input_chars)
    except Exception as exc:
        print("LLM refinement failed: " + str(exc)[:500], file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(f"LLM refinement: {summary['exact']} exact / {summary['removed']} removed "
              f"from {summary['listings']} listing(s) in {summary['jobs']} job(s) "
              f"using {summary['model']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
