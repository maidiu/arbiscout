"""Deterministic candidate adjudication; every dollar uses Decimal arithmetic.

This module does *not* fetch live data. Observations must be supplied explicitly.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

CENT = Decimal("0.01")


def dec(value: Any, name: str) -> Decimal:
    """Parse a non-negative finite input amount without floating arithmetic."""
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{name} must be a finite non-negative number")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{name} must be numeric") from None
    if not number.is_finite() or number < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return number


def money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def normalized(value: Any) -> str:
    return "".join(c.lower() for c in str(value or "") if c.isalnum())


def identity_check(retail: dict, market: dict) -> list[str]:
    """Conservatively confirm an item match, never fuzzy-match or infer variants."""
    reasons = []
    a, b = retail.get("identity", {}), market.get("identity", {})
    if not isinstance(a, dict) or not isinstance(b, dict):
        return ["missing identity objects"]
    for field in ("brand", "model", "gtin"):
        left, right = normalized(a.get(field)), normalized(b.get(field))
        if left and right and left != right:
            reasons.append(f"product {field} mismatch")
    if not (normalized(a.get("gtin")) and normalized(a.get("gtin")) == normalized(b.get("gtin"))):
        if not (normalized(a.get("brand")) and normalized(a.get("brand")) == normalized(b.get("brand"))
                and normalized(a.get("model")) and normalized(a.get("model")) == normalized(b.get("model"))):
            reasons.append("insufficient exact shared product identity")
    a_condition, b_condition = normalized(a.get("condition")), normalized(b.get("condition"))
    if not a_condition or not b_condition:
        reasons.append("missing item condition")
    elif a_condition != b_condition:
        reasons.append("item condition mismatch")
    return reasons


def age_days(value: str, as_of: date) -> int:
    try:
        observed = date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError("observation date must be YYYY-MM-DD") from None
    return (as_of - observed).days


def adjudicate(candidate: dict, assumptions: dict, as_of: date) -> dict:
    """Return a candidate decision, with explicit rejection/review reasons."""
    name = str(candidate.get("name") or "Unnamed product")
    key = str(candidate.get("id") or name)
    retail = candidate.get("retail", {})
    market = candidate.get("market", {})
    result: dict[str, Any] = {"id": key, "name": name, "status": "REVIEW", "reasons": [], "estimates": {}}
    reasons: list[str] = result["reasons"]
    try:
        if not isinstance(retail, dict) or not isinstance(market, dict):
            raise ValueError("retail and market objects are required")
        reasons.extend(identity_check(retail, market))
        if not str(retail.get("source_url") or "").startswith("https://"):
            reasons.append("missing retail HTTPS source URL")
        if not str(market.get("evidence_ref") or "").strip():
            reasons.append("missing market evidence reference")
        if market.get("source_type") not in ("manual_completed_sales", "licensed_completed_sales"):
            reasons.append("no verified completed-sales data source")
        if retail.get("in_stock") is not True:
            reasons.append("retail availability unconfirmed")
        maximum_age = int(assumptions.get("maximum_age_days", 14))
        if maximum_age < 0:
            raise ValueError("maximum_age_days cannot be negative")
        for source, item in (("retail", retail), ("market", market)):
            try:
                age = age_days(item.get("observed_on"), as_of)
                if age < 0:
                    reasons.append(f"{source} observation is in the future")
                elif age > maximum_age:
                    reasons.append(f"{source} observation is stale ({age} days)")
            except ValueError as exc:
                reasons.append(f"{source}: {exc}")
        sold_count = market.get("sold_count_30d")
        active_count = market.get("active_competing_listings")
        if isinstance(sold_count, bool) or not isinstance(sold_count, int) or sold_count < 0:
            reasons.append("missing valid 30-day sold count")
            sold_count = 0
        if isinstance(active_count, bool) or not isinstance(active_count, int) or active_count < 0:
            reasons.append("missing valid active listing count")
            active_count = None
        sold_price = dec(market.get("sold_price_estimate"), "sold_price_estimate")
        if sold_price == 0:
            reasons.append("sold price estimate is zero")
        buy_price = dec(retail.get("price"), "retail price")
        tax_rate = dec(retail.get("sales_tax_rate", "0"), "retail sales tax rate")
        if tax_rate > 1:
            raise ValueError("sales_tax_rate must be a fraction from 0 to 1")
        acquisition_shipping = dec(retail.get("shipping_cost", "0"), "retail shipping")
        outbound_shipping = dec(assumptions.get("outbound_shipping", "0"), "outbound shipping")
        packaging = dec(assumptions.get("packaging_cost", "0"), "packaging")
        return_reserve = dec(assumptions.get("return_reserve", "0"), "return reserve")
        fee_rate = dec(assumptions.get("ebay_fee_rate"), "eBay fee rate")
        promotion_rate = dec(assumptions.get("promotion_rate", "0"), "promotion rate")
        fee_fixed = dec(assumptions.get("ebay_fee_fixed", "0"), "fixed selling fee")
        buyer_shipping = dec(assumptions.get("buyer_shipping_collected", "0"), "buyer-paid shipping")
        buyer_sales_tax = dec(assumptions.get("buyer_sales_tax", "0"), "buyer sales tax")
        if fee_rate > 1 or promotion_rate > 1:
            raise ValueError("fee and promotion rates must be fractions")
        acquisition = buy_price * (1 + tax_rate) + acquisition_shipping
        receipts = sold_price + buyer_shipping
        # eBay fee base commonly includes applicable buyer sales tax. This input is
        # explicit, not guessed, and fee settings must be configured for the seller.
        fee_base = receipts + buyer_sales_tax
        fees = fee_base * fee_rate + fee_fixed + receipts * promotion_rate
        estimated_profit = receipts - acquisition - fees - outbound_shipping - packaging - return_reserve
        roi = estimated_profit / acquisition if acquisition > 0 else None
        result["estimates"] = {
            "sold_price": str(money(sold_price)),
            "acquisition_cost": str(money(acquisition)),
            "fees": str(money(fees)),
            "profit": str(money(estimated_profit)),
            "roi_pct": str(money(roi * 100)) if roi is not None else None,
            "sold_count_30d": sold_count,
            "active_competing_listings": active_count,
        }
        if roi is None:
            reasons.append("acquisition cost is zero; ROI undefined")
        if estimated_profit < dec(assumptions.get("min_profit", "10"), "min_profit"):
            reasons.append("below minimum estimated profit")
        if roi is None or roi < dec(assumptions.get("min_roi", "0.30"), "min_roi"):
            reasons.append("below minimum estimated ROI")
        if sold_count < int(assumptions.get("min_sold_30d", 5)):
            reasons.append("insufficient completed-sales count")
        # A rough ranking heuristic, not a statistically validated sale probability.
        if not reasons:
            result["status"] = "ELIGIBLE_VERIFY_BEFORE_BUYING"
            result["score"] = str(money(estimated_profit + Decimal(min(sold_count, 30)) / Decimal(10)))
    except (ValueError, TypeError, KeyError, ArithmeticError) as exc:
        reasons.append(f"invalid or missing evidence: {exc}")
    return result


def rank(candidates: list[dict], assumptions: dict, as_of: date) -> list[dict]:
    output = [adjudicate(item, assumptions, as_of) for item in candidates]
    output.sort(key=lambda row: (row["status"] != "ELIGIBLE_VERIFY_BEFORE_BUYING", -Decimal(row.get("score", "0")), row["id"]))
    return output
