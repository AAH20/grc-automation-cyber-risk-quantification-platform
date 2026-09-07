from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ciso_assistant import import_framework_catalog
from .economics import calculate_economics
from .risk import RiskDistribution, simulate_loss


def main() -> int:
    parser = argparse.ArgumentParser(prog="grc-decisiongraph", description="Evidence-backed GRC decision engineering")
    sub = parser.add_subparsers(dest="command", required=True)
    economics = sub.add_parser("economics")
    economics.add_argument("inputs", type=Path)
    economics.add_argument("--output", type=Path, required=True)
    risk = sub.add_parser("risk")
    risk.add_argument("inputs", type=Path)
    risk.add_argument("--output", type=Path, required=True)
    catalog = sub.add_parser("import-ciso-assistant")
    catalog.add_argument("inputs", type=Path)
    catalog.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.inputs.read_text())
    if args.command == "economics":
        result = calculate_economics(payload)
    elif args.command == "risk":
        result = simulate_loss(RiskDistribution(**payload["frequency"]), RiskDistribution(**payload["magnitude"]), iterations=payload.get("iterations", 20_000), seed=payload.get("seed", 42))
    else:
        result = import_framework_catalog(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
