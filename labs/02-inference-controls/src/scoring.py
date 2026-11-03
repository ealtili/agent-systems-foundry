"""Pure scoring functions. You implement them; tests/test_scoring.py is the contract."""

from collections.abc import Mapping, Sequence
from typing import NamedTuple


class BinStat(NamedTuple):
    n: int
    mean_confidence: float | None
    accuracy: float | None


def normalize_answer(raw: str) -> str:
    """Canonical form used to compare answers.

    Contract: strip surrounding whitespace, casefold, then drop ONE trailing "."
    ("Alice." -> "alice", "3.5." -> "3.5", "3.5" stays "3.5").
    """
    raise NotImplementedError


def brier_score(pairs: Sequence[tuple[float, bool]]) -> float:
    """Mean squared error between stated confidence and outcome (True=1, False=0).

    Raises ValueError for an empty sequence or a confidence outside [0, 1].
    """
    raise NotImplementedError


def calibration_bins(pairs: Sequence[tuple[float, bool]], n_bins: int = 5) -> list[BinStat]:
    """Group (confidence, correct) pairs into n_bins equal-width bins over [0, 1].

    Bin i covers [i/n, (i+1)/n); the last bin also includes 1.0. Always returns n_bins entries
    in ascending order. An empty bin has n == 0 and None for mean_confidence and accuracy.
    Raises ValueError if n_bins < 1 or a confidence is outside [0, 1].
    """
    raise NotImplementedError


def agreement_rate(answers_by_question: Mapping[str, Sequence[str]]) -> float:
    """Fraction of questions whose runs all agree after normalize_answer.

    A question with a single run trivially agrees. Raises ValueError for an empty mapping
    or a question with no runs.
    """
    raise NotImplementedError
