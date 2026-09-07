from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ciso_assistant import import_framework_catalog
from .board import build_board_pack, render_board_markdown
from .economics import calculate_economics
from .revenue import Attribution, Opportunity, evaluate_opportunity
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
    board = sub.add_parser("board-pack")
    board.add_argument("inputs", type=Path)
    board.add_argument("--output", type=Path, required=True)
    board.add_argument("--markdown", type=Path)
    contract = sub.add_parser("contract")
    contract.add_argument("inputs", type=Path)
    contract.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.inputs.read_text())
    if args.command == "economics":
        result = calculate_economics(payload)
    elif args.command == "risk":
        result = simulate_loss(RiskDistribution(**payload["frequency"]), RiskDistribution(**payload["magnitude"]), iterations=payload.get("iterations", 20_000), seed=payload.get("seed", 42))
    elif args.command == "import-ciso-assistant":
        result = import_framework_catalog(payload)
    elif args.command == "board-pack":
        result = build_board_pack(payload)
        if args.markdown:
            args.markdown.parent.mkdir(parents=True, exist_ok=True)
            args.markdown.write_text(render_board_markdown(result))
    else:
        payload["attribution"] = Attribution(payload["attribution"])
        result = evaluate_opportunity(Opportunity(**payload))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
