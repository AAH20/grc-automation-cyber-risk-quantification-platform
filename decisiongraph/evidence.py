from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone

from .models import EvidenceAssessment, EvidenceClass, EvidenceReceipt, Qualification, Verdict

SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def evidence_digest(payload: bytes) -> str:
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def qualify_evidence(
    receipt: EvidenceReceipt,
    *,
    required_scope: set[str],
    now: datetime | None = None,
) -> EvidenceAssessment:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    checks: dict[str, Verdict] = {}
    reasons: list[str] = []

    if receipt.evidence_class is EvidenceClass.UNAVAILABLE:
        checks = {name: Verdict.UNKNOWN for name in ("provenance", "integrity", "freshness", "scope", "relevance")}
        return EvidenceAssessment(receipt.evidence_id, Qualification.UNKNOWN, checks, ("evidence unavailable",), now.isoformat())

    checks["provenance"] = Verdict.PASS if receipt.collector and receipt.source_uri else Verdict.FAIL
    checks["integrity"] = Verdict.PASS if SHA256_PATTERN.match(receipt.digest) else Verdict.FAIL
    checks["freshness"] = Verdict.PASS if _time(receipt.valid_until) >= now else Verdict.FAIL
    checks["scope"] = Verdict.PASS if required_scope.issubset(set(receipt.scope)) else Verdict.FAIL
    checks["relevance"] = Verdict.PASS if receipt.statement.strip() else Verdict.FAIL

    labels = {
        "provenance": "collector or source provenance missing",
        "integrity": "digest is not a valid SHA-256 receipt",
        "freshness": "evidence validity window expired",
        "scope": "evidence does not cover required scope",
        "relevance": "evidence statement missing",
    }
    reasons.extend(labels[name] for name, verdict in checks.items() if verdict is Verdict.FAIL)
    if checks["freshness"] is Verdict.FAIL:
        status = Qualification.EXPIRED
    elif any(verdict is Verdict.FAIL for verdict in checks.values()):
        status = Qualification.REJECTED
    else:
        status = Qualification.QUALIFIED
    return EvidenceAssessment(receipt.evidence_id, status, checks, tuple(reasons), now.isoformat())
