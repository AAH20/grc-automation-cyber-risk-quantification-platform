from __future__ import annotations

from typing import Any


RECOGNIZED_CATEGORIES = {"VERIFIED_SAVINGS", "CONFIRMED_DIRECT_REVENUE", "VALIDATED_LOSS_REDUCTION"}


def calculate_economics(inputs: dict[str, Any]) -> dict[str, Any]:
    baseline_hours = float(inputs["baseline_hours"])
    current_hours = float(inputs["current_hours"])
    annual_volume = float(inputs["annual_volume"])
    loaded_rate = float(inputs["loaded_hourly_rate"])
    annual_cost = float(inputs["annual_platform_cost"])
    implementation_cost = float(inputs["implementation_cost"])
    entries = inputs.get("value_entries", [])

    labor_savings = max(0.0, baseline_hours - current_hours) * annual_volume * loaded_rate
    recognized_entries = sum(float(entry["amount"]) for entry in entries if entry["category"] in RECOGNIZED_CATEGORIES and entry.get("confirmed", False))
    excluded_entries = sum(float(entry["amount"]) for entry in entries if not (entry["category"] in RECOGNIZED_CATEGORIES and entry.get("confirmed", False)))
    recognized_value = labor_savings + recognized_entries
    first_year_cost = annual_cost + implementation_cost
    net_value = recognized_value - first_year_cost
    roi = net_value / first_year_cost * 100 if first_year_cost else 0.0
    monthly_value = recognized_value / 12
    payback = first_year_cost / monthly_value if monthly_value else None
    return {
        "annual_labor_savings": round(labor_savings, 2),
        "confirmed_additional_value": round(recognized_entries, 2),
        "recognized_value": round(recognized_value, 2),
        "excluded_value": round(excluded_entries, 2),
        "first_year_cost": round(first_year_cost, 2),
        "first_year_net_value": round(net_value, 2),
        "first_year_roi_pct": round(roi, 2),
        "payback_months": round(payback, 2) if payback is not None else None,
        "disclaimer": "Capacity and unconfirmed attribution are excluded from recognized value.",
    }
