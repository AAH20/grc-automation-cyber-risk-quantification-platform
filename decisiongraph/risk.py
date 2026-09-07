from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskDistribution:
    minimum: float
    mode: float
    maximum: float

    def validate(self) -> None:
        if not 0 <= self.minimum <= self.mode <= self.maximum:
            raise ValueError("distribution must satisfy 0 <= minimum <= mode <= maximum")


def simulate_loss(
    frequency: RiskDistribution,
    magnitude: RiskDistribution,
    *,
    iterations: int = 20_000,
    seed: int = 42,
) -> dict[str, float]:
    frequency.validate()
    magnitude.validate()
    if iterations < 100:
        raise ValueError("iterations must be at least 100")
    rng = random.Random(seed)
    losses = sorted(
        rng.triangular(frequency.minimum, frequency.maximum, frequency.mode)
        * rng.triangular(magnitude.minimum, magnitude.maximum, magnitude.mode)
        for _ in range(iterations)
    )

    def percentile(pct: float) -> float:
        return losses[min(len(losses) - 1, round((len(losses) - 1) * pct))]

    return {
        "mean": round(sum(losses) / len(losses), 2),
        "p10": round(percentile(0.10), 2),
        "p50": round(percentile(0.50), 2),
        "p90": round(percentile(0.90), 2),
        "iterations": iterations,
        "seed": seed,
    }
