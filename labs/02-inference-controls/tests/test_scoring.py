import pytest
from src.scoring import BinStat, agreement_rate, brier_score, calibration_bins, normalize_answer


def test_normalize_whitespace_case_and_trailing_period() -> None:
    assert normalize_answer("  408 ") == "408"
    assert normalize_answer("ALICE") == "alice"
    assert normalize_answer("Alice.") == "alice"


def test_normalize_keeps_decimal_point_and_drops_only_one_period() -> None:
    assert normalize_answer("3.5") == "3.5"
    assert normalize_answer("3.5.") == "3.5"
    assert normalize_answer("end..") == "end."


def test_brier_perfect_and_uninformative() -> None:
    assert brier_score([(1.0, True), (0.0, False)]) == 0.0
    assert brier_score([(0.5, True), (0.5, False)]) == pytest.approx(0.25)


def test_brier_penalises_overconfidence() -> None:
    assert brier_score([(0.9, True), (0.9, False)]) == pytest.approx(0.41)


def test_brier_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        brier_score([])
    with pytest.raises(ValueError):
        brier_score([(1.2, True)])


def test_bins_group_by_confidence() -> None:
    pairs = [(0.2, False), (0.4, False), (0.6, True), (1.0, True)]
    low, high = calibration_bins(pairs, n_bins=2)
    assert low.n == 2
    assert low.mean_confidence == pytest.approx(0.3)
    assert low.accuracy == pytest.approx(0.0)
    assert high.n == 2
    assert high.mean_confidence == pytest.approx(0.8)
    assert high.accuracy == pytest.approx(1.0)


def test_bin_edges_and_empty_bins() -> None:
    bins = calibration_bins([(0.5, True)], n_bins=2)
    assert [b.n for b in bins] == [0, 1]
    assert bins[0] == BinStat(0, None, None)

    five = calibration_bins([(1.0, True)])
    assert len(five) == 5
    assert [b.n for b in five] == [0, 0, 0, 0, 1]


def test_bins_reject_bad_input() -> None:
    with pytest.raises(ValueError):
        calibration_bins([(0.5, True)], n_bins=0)
    with pytest.raises(ValueError):
        calibration_bins([(-0.1, True)])


def test_agreement_counts_questions_where_all_runs_match() -> None:
    runs = {"q1": ["A", "a ", " A"], "q2": ["1", "2", "1"]}
    assert agreement_rate(runs) == pytest.approx(0.5)
    assert agreement_rate({"q1": ["x", "x"], "q2": ["7"]}) == pytest.approx(1.0)


def test_agreement_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        agreement_rate({})
    with pytest.raises(ValueError):
        agreement_rate({"q1": []})
