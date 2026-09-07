from __future__ import annotations

from typing import Any


def import_framework_catalog(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a CISO Assistant framework-library export without copying its content."""
    objects = payload.get("frameworks") or payload.get("results") or payload.get("objects")
    if not isinstance(objects, list):
        raise ValueError("expected a framework list in frameworks, results, or objects")
    normalized = []
    for item in objects:
        identifier = item.get("urn") or item.get("id") or item.get("name")
        if not identifier:
            raise ValueError("every framework requires an urn, id, or name")
        normalized.append({
            "external_id": str(identifier),
            "name": str(item.get("name") or identifier),
            "version": str(item.get("version") or "unspecified"),
            "provider": "ciso-assistant",
        })
    return {"provider": "ciso-assistant", "framework_count": len(normalized), "frameworks": normalized}
