from __future__ import annotations

from collections import defaultdict

from .models import CrossMapping, MappingStrength


class CrossMapRegistry:
    """Versioned, directional mappings. Transitive mappings are never inferred."""

    def __init__(self, mappings: list[CrossMapping]):
        self._mappings = list(mappings)
        self._by_source: dict[str, list[CrossMapping]] = defaultdict(list)
        for mapping in mappings:
            if not 0 <= mapping.coverage_pct <= 100:
                raise ValueError("coverage_pct must be between 0 and 100")
            if mapping.strength is MappingStrength.EXACT and mapping.coverage_pct != 100:
                raise ValueError("EXACT mappings require 100% coverage")
            if not mapping.rationale or not mapping.reviewer:
                raise ValueError("mapping rationale and reviewer are required")
            self._by_source[mapping.source].append(mapping)

    def direct(self, source: str) -> list[CrossMapping]:
        return list(self._by_source.get(source, []))

    def find(self, source: str, target: str) -> CrossMapping | None:
        return next((item for item in self.direct(source) if item.target == target), None)

    def coverage(self, source_prefix: str, target_prefix: str) -> float:
        relevant = [m.coverage_pct for m in self._mappings if m.source.startswith(source_prefix) and m.target.startswith(target_prefix)]
        return round(sum(relevant) / len(relevant), 2) if relevant else 0.0
