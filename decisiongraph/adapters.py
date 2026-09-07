from __future__ import annotations

import json
from typing import Any

from .evidence import evidence_digest
from .models import EvidenceClass, EvidenceReceipt


def _canonical(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def aws_privileged_mfa_receipt(
    users: list[dict[str, Any]], *, account_id: str, observed_at: str, valid_until: str
) -> EvidenceReceipt:
    privileged = sorted(
        ({"user": str(user["UserName"]), "mfa": bool(user.get("MFAActive", False))} for user in users if user.get("Privileged", False)),
        key=lambda item: item["user"],
    )
    missing = [item["user"] for item in privileged if not item["mfa"]]
    statement = "All privileged human identities use MFA." if not missing else f"Privileged identities without MFA: {', '.join(missing)}."
    payload = {"account_id": account_id, "privileged": privileged}
    return EvidenceReceipt(
        evidence_id=f"aws-iam-mfa-{account_id}", evidence_class=EvidenceClass.OBSERVED,
        resource=f"arn:aws:iam::{account_id}:root", collector="decisiongraph-aws-iam@0.1.0",
        observed_at=observed_at, valid_until=valid_until, digest=evidence_digest(_canonical(payload)),
        scope=(f"aws-account:{account_id}", "identity", "privileged-access"),
        source_uri=f"aws://iam/{account_id}/credential-report", statement=statement,
    )


def kubernetes_audit_receipt(
    events: list[dict[str, Any]], *, cluster: str, observed_at: str, valid_until: str
) -> EvidenceReceipt:
    normalized = sorted(
        ({"auditID": event.get("auditID"), "verb": event.get("verb"), "stage": event.get("stage"), "user": (event.get("user") or {}).get("username") } for event in events),
        key=lambda item: str(item["auditID"]),
    )
    missing_identity = sum(1 for item in normalized if not item["user"])
    completed = sum(1 for item in normalized if item["stage"] in {"ResponseComplete", "Panic"})
    statement = f"{completed}/{len(normalized)} events reached a terminal audit stage; {missing_identity} lack actor identity."
    return EvidenceReceipt(
        evidence_id=f"k8s-audit-{cluster}", evidence_class=EvidenceClass.OBSERVED,
        resource=f"kubernetes://{cluster}/apiserver", collector="decisiongraph-k8s-audit@0.1.0",
        observed_at=observed_at, valid_until=valid_until, digest=evidence_digest(_canonical(normalized)),
        scope=(f"kubernetes-cluster:{cluster}", "audit", "control-plane"),
        source_uri=f"kubernetes://{cluster}/audit-events", statement=statement,
    )


def log_query_receipt(
    *, backend: str, endpoint_alias: str, query: str, result: list[dict[str, Any]], observed_at: str, valid_until: str
) -> EvidenceReceipt:
    supported = {"elastic", "opensearch", "victorialogs", "wazuh"}
    if backend not in supported:
        raise ValueError(f"unsupported log backend: {backend}")
    if not query.strip():
        raise ValueError("query is required")
    payload = {"backend": backend, "endpoint_alias": endpoint_alias, "query": query, "result": result}
    return EvidenceReceipt(
        evidence_id=f"log-query-{backend}-{endpoint_alias}", evidence_class=EvidenceClass.OBSERVED,
        resource=f"log-backend://{backend}/{endpoint_alias}", collector=f"decisiongraph-{backend}@0.1.0",
        observed_at=observed_at, valid_until=valid_until, digest=evidence_digest(_canonical(payload)),
        scope=(f"log-backend:{endpoint_alias}", "security-telemetry"),
        source_uri=f"log-backend://{backend}/{endpoint_alias}/query", statement=f"Query returned {len(result)} evidence records.",
    )
