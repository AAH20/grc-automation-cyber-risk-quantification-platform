"""Evidence-backed GRC decision engineering primitives."""

from .engine import DecisionGraph
from .economics import calculate_economics
from .evidence import qualify_evidence
from .risk import simulate_loss
from .board import build_board_pack
from .revenue import evaluate_opportunity

__all__ = ["DecisionGraph", "build_board_pack", "calculate_economics", "evaluate_opportunity", "qualify_evidence", "simulate_loss"]
__version__ = "0.1.0"
