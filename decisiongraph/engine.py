from __future__ import annotations

from datetime import datetime, timezone

from .evidence import qualify_evidence
from .models import ControlEvaluation, EvidenceReceipt, Qualification, Verdict


class DecisionGraph:
    def __init__(self) -> None:
        self.receipts: dict[str, EvidenceReceipt] = {}
        self.control_edges: dict[str, set[str]] = {}

    def add_evidence(self, receipt: EvidenceReceipt) -> None:
        if receipt.evidence_id in self.receipts:
            raise ValueError(f"duplicate evidence id: {receipt.evidence_id}")
        self.receipts[receipt.evidence_id] = receipt

    def map_control(self, control_id: str, evidence_ids: set[str]) -> None:
        missing = evidence_ids - self.receipts.keys()
        if missing:
            raise ValueError(f"unknown evidence ids: {sorted(missing)}")
        self.control_edges[control_id] = set(evidence_ids)

    def evaluate(self, control_id: str, *, required_scope: set[str], now: datetime | None = None) -> ControlEvaluation:
        now = now or datetime.now(timezone.utc)
        evidence_ids = self.control_edges.get(control_id, set())
        if not evidence_ids:
            return ControlEvaluation(control_id, Verdict.UNKNOWN, (), "no evidence mapped", now.isoformat())
        assessments = [qualify_evidence(self.receipts[item], required_scope=required_scope, now=now) for item in sorted(evidence_ids)]
        if any(item.status in {Qualification.REJECTED, Qualification.EXPIRED} for item in assessments):
            verdict, reason = Verdict.FAIL, "one or more mapped evidence receipts failed qualification"
        elif any(item.status is Qualification.UNKNOWN for item in assessments):
            verdict, reason = Verdict.UNKNOWN, "one or more mapped evidence receipts are unavailable"
        else:
            verdict, reason = Verdict.PASS, "all mapped evidence receipts qualified"
        return ControlEvaluation(control_id, verdict, tuple(sorted(evidence_ids)), reason, now.isoformat())
