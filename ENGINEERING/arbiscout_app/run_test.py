#!/usr/bin/env python3
"""Top 20 retailer offers -> eBay sold records -> own 30-day filter -> top ten.

All displayed sold-listing price gaps remain provisional, not actual-paid truth.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from datetime import datetime, timedelta, timezone
from html import escape
import json
from pathlib import Path
import subprocess
import sys
import webbrowser
import ebay_comparison as ebay


def rank_provisional(rows, limit=10):
    candidates = []
    for row in rows:
        comp = row["comparison"]
        if comp.get("status") != "PROVISIONAL_SOLD_DISPLAY_COMPARISON":
            continue
        if comp.get("gap") is None or comp["gap"] <= 0:
            continue
        retail = row["retailer"]
        candidates.append({
            "retailer_key": retail["key"], "title": retail["title"],
            "retailer_url": retail["url"], "retailer_current_price": retail["current_price"],
            "retailer_regular_price": retail["regular_price"],
            "ebay_sold_url": row["ebay_search_url"],
            "ebay_sold_low_30d": comp.get("sold_low"),
            "ebay_sold_high_30d": comp.get("sold_high"),
            "ebay_sold_mean_30d": comp.get("sold_mean"),
            "ebay_typical_low_30d": comp.get("typical_low"),
            "ebay_typical_high_30d": comp.get("typical_high"),
            "ebay_displayed_median_30d": comp["historical_median"],
            "bestbuy_below_ebay_low": comp.get("retail_below_low"),
            "indicative_gap_dollars": comp["gap"],
            "indicative_gap_percent": comp["gap_percent"],
            "matched_displayed_sales": comp["sample_count"],
            "evidence_status": "PROVISIONAL_DISPLAYED_SOLD_NOT_ACTUAL_PAID",
        })
    candidates.sort(key=lambda r: (-r["indicative_gap_dollars"],
                                   -(r["indicative_gap_percent"] or 0), r["title"].casefold()))
    winners = candidates[:limit]
    for i, item in enumerate(winners, 1):
        item["rank"] = i
    return winners


def render_dashboard(winners, receipt):
    trs = []
    money = lambda x: "—" if x is None else "$" + format(float(x), ",.2f")
    for r in winners:
        low, high = r.get("ebay_sold_low_30d"), r.get("ebay_sold_high_30d")
        sold_range = "—" if low is None else "{} – {}".format(money(low), money(high))
        tlow, thigh = r.get("ebay_typical_low_30d"), r.get("ebay_typical_high_30d")
        typical = "—" if tlow is None else "{} – {}".format(money(tlow), money(thigh))
        versus = "Below eBay low" if r.get("bestbuy_below_ebay_low") else "Below eBay median"
        below_low = "1" if r.get("bestbuy_below_ebay_low") else "0"
        trs.append(
            "<tr data-below-low='" + below_low + "'><td>{}</td><td><b>{}</b><br><a href='{}'>Retailer</a> · "
            "<a href='{}'>eBay sold</a></td><td>{}</td><td>{}<br><small>mean {}</small></td>"
            "<td>{}</td><td>{}</td><td><b>{}</b> ({}%)</td><td><b>{}</b></td><td>{}</td></tr>".format(
                r["rank"], escape(r["title"]),
                escape(r["retailer_url"], quote=True), escape(r["ebay_sold_url"], quote=True),
                money(r["retailer_current_price"]), sold_range, money(r.get("ebay_sold_mean_30d")),
                typical, money(r["ebay_displayed_median_30d"]),
                money(r["indicative_gap_dollars"]), r["indicative_gap_percent"],
                versus, r["matched_displayed_sales"]))
    rows = "".join(trs) or "<tr><td colspan='9'>No positive eligible displayed-price gaps. Zero is a valid result.</td></tr>"
    heading = ("SYNTHETIC DEMO — ALL PRICES AND SALES ARE FICTIONAL"
               if receipt["synthetic_demo"] else "TEST RESULTS — PROVISIONAL DISPLAYED PRICES")
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>ArbiScout 30-day top ten test</title><style>"
        "body{font:15px system-ui,sans-serif;max-width:1500px;margin:30px auto;padding:0 20px;"
        "background:#f7f9fc;color:#172634;line-height:1.5}"
        "table{width:100%;border-collapse:collapse;background:white}"
        "td,th{padding:12px;border-bottom:1px solid #dce4eb;text-align:left}"
        "th{background:#e8eef5}.alert{background:#fff4df;border-left:4px solid #b77316;"
        "padding:15px}a{color:#125ba4}</style></head><body>"
        "<h1>ArbiScout · top-ten 30-day eBay gap test</h1><strong>" + escape(heading)
        + "</strong><p class='alert'>This page ranks <b>indicative</b> differences"
        " between displayed eBay sold-listing values and observed retailer prices."
        " Accepted Best Offers may have different actual paid prices. Exact variant,"
        " condition, stock, shipping and checkout price are not independently verified."
        " <b>No listing here is an accepted real purchase opportunity.</b></p>"
        "<p><b>{}</b> retailer offers checked · <b>{}</b> positive provisional comparisons"
        " · <b>0</b> verified actual-paid comparisons.</p>".format(
            receipt["selected_retail_offers"], receipt["positive_provisional_count"])
        + "<p>ArbiScout computes its own preceding 30-day cutoff from sold dates,"
        " excludes dated-out sales, missing dates, mismatches, and unresolved Best Offers,"
        " then ranks by absolute price difference. The candidate 20 are initially"
        " chosen by retailer markdown. Sold range is the lowest–highest usable 30-day"
        " sold price; typical middle 50% is the interquartile range.</p>"
        "<p><label><input type='checkbox' id='belowlow'> Only show rows where Best Buy"
        " is below the eBay sold low</label></p>"
        "<table><thead><tr><th>#</th><th>Product and sources</th><th>Retail price</th>"
        "<th>eBay sold low – high</th><th>Typical middle 50%</th><th>Displayed eBay 30d median</th>"
        "<th>Indicative gap</th><th>Best Buy vs eBay</th><th>Valid records</th>"
        "</tr></thead><tbody>" + rows + "</tbody></table>"
        "<p><a href='comparisons/index.html'>All comparisons, missing data and exclusions</a>"
        " · <a href='retailer/index.html'>Retail deal dashboard</a></p>"
        "<script>document.getElementById('belowlow').onchange=function(){"
        "var checked=this.checked;"
        "document.querySelectorAll('tbody tr[data-below-low]').forEach(function(tr){"
        "tr.style.display=checked&&tr.getAttribute('data-below-low')!=='1'?'none':'';"
        "})}</script>"
        "</body></html>"
    )


def make_demo_retail(path):
    path.mkdir(parents=True, exist_ok=True)
    cards = []
    for i in range(20):
        name = "ArbiScout Fictional Device DM{}".format(1000 + i)
        cards.append(
            '<div class="product-item"><h3>{}</h3><a href="https://shop.example.com/product/dm{}">'
            'Details</a><span class="sale-price">&#36;{:.2f}</span>'
            '<del>&#36;{:.2f}</del></div>'.format(name, 1000 + i, 69.99 + 3*i, 250 + 8*i))
    target = path / "fictional_retail.html"
    target.write_text("<html><main>" + "".join(cards) + "</main></html>", encoding="utf-8")
    return target


def make_demo_sold(path, products, at):
    path.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(ebay.choose_deals(products, 20), 1):
        cards = []
        title = escape(item["title"])
        for k in range(3):
            cards.append(
                "<li class='s-item'><a class='s-item__link' href='https://www.ebay.com/itm/{}'>"
                "<h3 class='s-item__title'>{}</h3></a><span class='s-item__price'>"
                "&#36;{:.2f}</span><span class='s-item__ended-date'>Sold {}</span></li>".format(
                    880000000000 + 10*i + k, title,
                    float(item["current_price"]) + 40 + 4*i + 2*k,
                    (at-timedelta(days=k+1)).strftime("%b %d, %Y")))
        for item_id, amt, days, extra in [
            (990000000000+i, 9000, 45, ""),
            (770000000000+i, 8000, 2, "<span>Best offer accepted</span>")]:
            cards.append(
                "<li class='s-item'><a class='s-item__link' href='https://www.ebay.com/itm/{}'>"
                "<h3 class='s-item__title'>{}</h3></a><span class='s-item__price'>"
                "&#36;{:.2f}</span><span class='s-item__ended-date'>Sold {}</span>{}</li>".format(
                    item_id, title, amt, (at-timedelta(days=days)).strftime("%b %d, %Y"), extra))
        (path / "{:02d}.html".format(i)).write_text(
            "<html><body>" + "".join(cards) + "</body></html>", encoding="utf-8")


def execute(*, snapshot=None, url=None, ebay_pages=None, ebay_live=False, demo=False,
            output="arbiscout_test", as_of=None, mode="http", browser_visible=False,
            timeout=20, delay=1.5, reuse_retailer=False, delete_ebay_pages=False,
            ebay_auto_match=False, include_current_only=None, keep_selection=False):
    if demo and (snapshot or url or ebay_pages or ebay_live):
        raise ValueError("Demo cannot mix with real sources")
    if ebay_pages and ebay_live:
        raise ValueError("Choose saved eBay pages or live eBay, not both")
    if not demo and not snapshot and not url and not reuse_retailer:
        raise ValueError("Provide --snapshot, --url or --demo")
    if snapshot and not Path(snapshot).is_file():
        raise ValueError("Saved retailer HTML does not exist")
    if ebay_pages and not Path(ebay_pages).is_dir():
        raise ValueError("Saved eBay folder does not exist")
    at = as_of or datetime.now(timezone.utc)
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    if demo:
        snapshot, url = make_demo_retail(root / "synthetic_input"), "https://shop.example.com/sale"
    elif snapshot:
        url = url or "https://www.bestbuy.com/black-friday"
    command = [sys.executable, str(Path(__file__).with_name("arbiscout.py")),
               "--outdir", str(root / "retailer")]
    if snapshot:
        command += ["--snapshot", str(snapshot), "--snapshot-url", str(url), "--offline"]
    else:
        command += ["--url", str(url), "--depth", "2", "--max-listings", "12",
                    "--max-products", "0", "--mode", mode,
                    "--timeout", str(timeout), "--delay", str(delay), "--save-html"]
        if browser_visible:
            command.append("--browser-visible")
    if reuse_retailer:
        if not (root / "retailer" / "products.json").is_file():
            raise ValueError("--reuse-retailer needs an existing retailer/products.json")
    else:
        subprocess.run(command, check=True)
    products_path = root / "retailer" / "products.json"
    products = json.loads(products_path.read_text(encoding="utf-8"))
    if include_current_only is None:
        include_current_only = any(p.get("current_price") is not None and
                                   p.get("regular_price") is None for p in products)
    if demo:
        ebay_pages = root / "synthetic_input" / "ebay"
        make_demo_sold(ebay_pages, products, at)
        (root / "synthetic_input" / "NOTICE.txt").write_text(
            "FICTIONAL retailer and eBay input only. No real market data.\n", encoding="utf-8")
    rows = ebay.compare_top20(
        products_path, root / "comparisons", top=20, fixture_dir=ebay_pages,
        live=ebay_live, as_of=at, auto_match=ebay_auto_match,
        require_discount=not include_current_only,
        deals_override=products if keep_selection else None)
    match_report = {}
    match_path = root / "comparisons" / "fixture_match.json"
    if ebay_auto_match and match_path.is_file():
        match_report = json.loads(match_path.read_text(encoding="utf-8"))
    if delete_ebay_pages and ebay_pages and not demo:
        targets = set(Path(ebay_pages).glob("[0-9][0-9].html"))
        for item in match_report.get("matched", []):
            targets.add(Path(ebay_pages) / item["file"])
        for fixture in sorted(targets):
            try:
                fixture.unlink()
            except OSError:
                pass
    winners = rank_provisional(rows, 10)
    count = sum(r["comparison"].get("status") == "PROVISIONAL_SOLD_DISPLAY_COMPARISON"
                and (r["comparison"].get("gap") or 0) > 0 for r in rows)
    receipt = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "as_of_utc": at.isoformat(),
        "window_start_utc": (at-timedelta(days=30)).isoformat(),
        "synthetic_demo": bool(demo), "selected_retail_offers": len(rows),
        "positive_provisional_count": count, "top_ten_count": len(winners),
        "actual_paid_verified_count": 0,
        "source_mode": ("SYNTHETIC_DEMO" if demo else "SAVED_EBAY_HTML"
                        if ebay_pages else "ROBOTS_CHECKED_LIVE_ATTEMPT"
                        if ebay_live else "NO_EBAY_RESULTS"),
        "source_status_counts": dict(Counter(r["ebay_status"] for r in rows)),
        "include_current_only": bool(include_current_only),
        "keep_selection": bool(keep_selection),
        "evidence_ceiling": "PROVISIONAL_DISPLAYED_PRICE_NOT_ACTUAL_PAID",
    }
    if ebay_auto_match:
        receipt["matched_fixture_files"] = len(match_report.get("matched", []))
        receipt["unmatched_fixture_files"] = match_report.get("unmatched", [])
    (root / "top10.json").write_text(json.dumps(winners, indent=2) + "\n", encoding="utf-8")
    with (root / "top10.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["rank", "retailer_key", "title", "retailer_url", "retailer_current_price",
                  "retailer_regular_price", "ebay_sold_url", "ebay_sold_low_30d",
                  "ebay_sold_high_30d", "ebay_sold_mean_30d", "ebay_typical_low_30d",
                  "ebay_typical_high_30d", "ebay_displayed_median_30d", "bestbuy_below_ebay_low",
                  "indicative_gap_dollars", "indicative_gap_percent", "matched_displayed_sales",
                  "evidence_status"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(winners)
    (root / "run_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    (root / "index.html").write_text(render_dashboard(winners, receipt), encoding="utf-8")
    return receipt


def main(argv=None):
    p = argparse.ArgumentParser(description="Retailer top 20 -> 30d eBay -> provisional top ten")
    p.add_argument("--snapshot", help="Locally saved retailer HTML, used offline")
    p.add_argument("--url", help="Original source URL; or permitted live retailer URL")
    p.add_argument("--ebay-pages", help="Saved eBay sold results 01.html..20.html")
    p.add_argument("--ebay-live", action="store_true", help="Explicit robots-checked live request")
    p.add_argument("--mode", choices=("http", "browser"), default="http", help="Retailer fetch mode")
    p.add_argument("--browser-visible", action="store_true", help="Show the browser window")
    p.add_argument("--timeout", type=int, default=20, help="Per-page timeout in seconds")
    p.add_argument("--delay", type=float, default=1.5, help="Minimum seconds between fetches")
    p.add_argument("--reuse-retailer", action="store_true",
                   help="Skip crawling and reuse the existing OUTPUT/retailer/products.json")
    p.add_argument("--delete-ebay-pages", action="store_true",
                   help="Delete consumed eBay fixture files after processing")
    p.add_argument("--ebay-auto-match", action="store_true",
                   help="Match saved eBay pages to candidates by their search query instead of 01.html..20.html")
    p.add_argument("--include-current-only", action="store_true", default=None,
                   help="Include products with a current price but no regular price (auto-detected by default)")
    p.add_argument("--discount-only", dest="include_current_only", action="store_false",
                   help="Only include products that have a regular price")
    p.add_argument("--keep-selection", action="store_true",
                   help="Compare the products.json rows in file order instead of re-selecting top 20 by discount")
    p.add_argument("--demo", action="store_true", help="20 completely fictional end-to-end records")
    p.add_argument("--as-of", help="YYYY-MM-DD for repeatable test")
    p.add_argument("--output", default="arbiscout_test")
    p.add_argument("--open", action="store_true")
    a = p.parse_args(argv)
    try:
        at = datetime.fromisoformat(a.as_of).replace(tzinfo=timezone.utc) if a.as_of else None
        receipt = execute(snapshot=a.snapshot, url=a.url, ebay_pages=a.ebay_pages,
                          ebay_live=a.ebay_live, demo=a.demo, output=a.output, as_of=at,
                          mode=a.mode, browser_visible=a.browser_visible,
                          timeout=a.timeout, delay=a.delay, reuse_retailer=a.reuse_retailer,
                          delete_ebay_pages=a.delete_ebay_pages,
                          ebay_auto_match=a.ebay_auto_match,
                          include_current_only=a.include_current_only,
                          keep_selection=a.keep_selection)
    except (ValueError, subprocess.CalledProcessError) as exc:
        p.error(str(exc))
    print("Checked", receipt["selected_retail_offers"], "retailer offers;",
          receipt["positive_provisional_count"], "provisional positive gaps;",
          receipt["top_ten_count"], "ranked;", 0, "verified actual-paid.")
    print("Dashboard:", (Path(a.output)/"index.html").resolve())
    if a.open:
        webbrowser.open((Path(a.output)/"index.html").resolve().as_uri())


if __name__ == "__main__":
    main()
