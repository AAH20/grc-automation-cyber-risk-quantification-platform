from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class Attribution(str, Enum):
    DIRECT = "DIRECT"
    CONTRIBUTORY = "CONTRIBUTORY"
    CAPACITY = "CAPACITY"
    EXCLUDED = "EXCLUDED"


@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    contract_value: float
    grc_blocker: str
    opened_at: str
    resolved_at: str | None
    commercial_owner_confirmed: bool
    automation_contribution_pct: float
    attribution: Attribution
    finance_approved_attributable_value: float | None = None


def evaluate_opportunity(opportunity: Opportunity) -> dict[str, Any]:
    if opportunity.contract_value < 0:
        raise ValueError("contract value cannot be negative")
    if not 0 <= opportunity.automation_contribution_pct <= 100:
        raise ValueError("automation contribution must be between 0 and 100")
    if not opportunity.grc_blocker.strip():
        raise ValueError("a documented GRC blocker is required")
    if opportunity.finance_approved_attributable_value is not None and not 0 <= opportunity.finance_approved_attributable_value <= opportunity.contract_value:
        raise ValueError("Finance-approved attributable value must be within contract value")

    eligible_direct = (
        opportunity.attribution is Attribution.DIRECT
        and opportunity.commercial_owner_confirmed
        and opportunity.resolved_at is not None
    )
    confirmed_unblocked = opportunity.contract_value if eligible_direct else 0.0
    weighted_influence = (
        opportunity.contract_value * opportunity.automation_contribution_pct / 100
        if opportunity.attribution in {Attribution.DIRECT, Attribution.CONTRIBUTORY}
        else 0.0
    )
    result = asdict(opportunity)
    result["attribution"] = opportunity.attribution.value
    recognized_for_roi = opportunity.finance_approved_attributable_value if eligible_direct and opportunity.finance_approved_attributable_value is not None else 0.0
    result.update({
        "confirmed_contract_value_unblocked": round(confirmed_unblocked, 2),
        "modeled_weighted_influence": round(weighted_influence, 2),
        "recognized_value_for_roi": round(recognized_for_roi, 2),
        "included_in_recognized_value": recognized_for_roi > 0,
        "boundary": "Confirmed contract value unblocked, modeled influence, and Finance-approved ROI value are separate measures.",
    })
    return result
