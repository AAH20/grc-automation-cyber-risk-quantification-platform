from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class EvidenceClass(str, Enum):
    OBSERVED = "OBSERVED"
    DECLARED = "DECLARED"
    EXERCISED = "EXERCISED"
    ATTESTED = "ATTESTED"
    INFERRED = "INFERRED"
    UNAVAILABLE = "UNAVAILABLE"


class Qualification(str, Enum):
    QUALIFIED = "QUALIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class MappingStrength(str, Enum):
    EXACT = "EXACT"
    SUBSTANTIAL = "SUBSTANTIAL"
    PARTIAL = "PARTIAL"
    RELATED = "RELATED"


@dataclass(frozen=True)
class EvidenceReceipt:
    evidence_id: str
    evidence_class: EvidenceClass
    resource: str
    collector: str
    observed_at: str
    valid_until: str
    digest: str
    scope: tuple[str, ...]
    source_uri: str
    statement: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["evidence_class"] = self.evidence_class.value
        value["scope"] = list(self.scope)
        return value


@dataclass(frozen=True)
class EvidenceAssessment:
    evidence_id: str
    status: Qualification
    checks: dict[str, Verdict]
    reasons: tuple[str, ...]
    qualified_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "status": self.status.value,
            "checks": {key: value.value for key, value in self.checks.items()},
            "reasons": list(self.reasons),
            "qualified_at": self.qualified_at,
        }


@dataclass(frozen=True)
class Requirement:
    framework_id: str
    requirement_id: str
    title: str
    objective: str


@dataclass(frozen=True)
class CrossMapping:
    source: str
    target: str
    strength: MappingStrength
    coverage_pct: float
    rationale: str
    reviewer: str
    mapping_version: str


@dataclass(frozen=True)
class ControlEvaluation:
    control_id: str
    verdict: Verdict
    evidence_ids: tuple[str, ...]
    reason: str
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
