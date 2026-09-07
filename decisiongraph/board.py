from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


REQUIRED_OPTION_FIELDS = {"name", "cost", "p50_residual_exposure", "time_days", "business_impact"}


def build_board_pack(payload: dict[str, Any], *, generated_at: str | None = None) -> dict[str, Any]:
    required = {"decision_id", "title", "business_objective", "current_p50_exposure", "risk_tolerance", "options", "recommended_option", "evidence_ids", "decision_owner", "decision_due"}
    missing = required - payload.keys()
    if missing:
        raise ValueError(f"missing board-pack fields: {sorted(missing)}")
    options = payload["options"]
    if len(options) < 2:
        raise ValueError("board packs require at least two alternatives")
    if any(REQUIRED_OPTION_FIELDS - option.keys() for option in options):
        raise ValueError("each alternative requires cost, residual exposure, time, and business impact")
    names = {option["name"] for option in options}
    if payload["recommended_option"] not in names:
        raise ValueError("recommended option must reference a defined alternative")
    if not payload["evidence_ids"]:
        raise ValueError("board pack requires evidence lineage")

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema_version": "1.0",
        **payload,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "pack_sha256": hashlib.sha256(canonical).hexdigest(),
        "evidence_boundary": "Decision support only; accountable owner approval is required.",
    }


def render_board_markdown(pack: dict[str, Any]) -> str:
    lines = [
        f"# {pack['title']}", "", f"**Decision ID:** {pack['decision_id']}",
        f"**Decision owner:** {pack['decision_owner']}", f"**Decision due:** {pack['decision_due']}", "",
        "## Decision context", "", f"- Business objective: {pack['business_objective']}",
        f"- Current P50 exposure: ${pack['current_p50_exposure']:,.0f}", f"- Risk tolerance: ${pack['risk_tolerance']:,.0f}", "",
        "## Alternatives", "", "| Alternative | Cost | P50 residual exposure | Time | Business impact |", "|---|---:|---:|---:|---|",
    ]
    for option in pack["options"]:
        lines.append(f"| {option['name']} | ${option['cost']:,.0f} | ${option['p50_residual_exposure']:,.0f} | {option['time_days']} days | {option['business_impact']} |")
    lines.extend(["", "## Recommended decision", "", pack["recommended_option"], "", "## Evidence lineage", "", *(f"- `{item}`" for item in pack["evidence_ids"]), "", f"Receipt: `{pack['pack_sha256']}`", ""])
    return "\n".join(lines)
