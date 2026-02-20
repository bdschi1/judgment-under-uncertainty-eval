"""Tests for calibration scoring module."""

from __future__ import annotations

import pytest

from src.calibration import (
    brier_score,
    expected_calibration_error,
    log_loss_score,
    parse_probability_from_response,
    score_probability_quality,
)


class TestBrierScore:
    """Tests for Brier score computation."""

    def test_perfect_positive(self):
        assert brier_score(1.0, 1) == 0.0

    def test_perfect_negative(self):
        assert brier_score(0.0, 0) == 0.0

    def test_worst_positive(self):
        assert brier_score(0.0, 1) == 1.0

    def test_worst_negative(self):
        assert brier_score(1.0, 0) == 1.0

    def test_moderate_prediction(self):
        assert abs(brier_score(0.7, 1) - 0.09) < 0.01

    def test_fifty_fifty(self):
        assert brier_score(0.5, 1) == 0.25
        assert brier_score(0.5, 0) == 0.25

    def test_range_validation_high(self):
        with pytest.raises(ValueError):
            brier_score(1.5, 1)

    def test_range_validation_low(self):
        with pytest.raises(ValueError):
            brier_score(-0.1, 0)

    def test_outcome_validation(self):
        with pytest.raises(ValueError):
            brier_score(0.5, 2)


class TestLogLoss:
    """Tests for log loss computation."""

    def test_good_prediction(self):
        assert log_loss_score(0.9, 1) < 0.2

    def test_bad_prediction(self):
        assert log_loss_score(0.1, 1) > 2.0

    def test_perfect_prediction(self):
        # Near-perfect (eps prevents exact 0)
        assert log_loss_score(1.0, 1) < 0.001

    def test_symmetric(self):
        loss_pos = log_loss_score(0.8, 1)
        loss_neg = log_loss_score(0.2, 0)
        assert abs(loss_pos - loss_neg) < 0.001

    def test_range_validation(self):
        with pytest.raises(ValueError):
            log_loss_score(1.5, 1)


class TestECE:
    """Tests for Expected Calibration Error."""

    def test_perfectly_calibrated(self):
        probs = [0.5] * 100
        outcomes = [0] * 50 + [1] * 50
        ece, bins = expected_calibration_error(probs, outcomes)
        assert ece < 0.05

    def test_overconfident(self):
        probs = [0.9] * 100
        outcomes = [0] * 50 + [1] * 50
        ece, bins = expected_calibration_error(probs, outcomes)
        assert ece > 0.3

    def test_empty_input(self):
        ece, bins = expected_calibration_error([], [])
        assert ece == 0.0
        assert bins == []

    def test_returns_bins(self):
        probs = [0.1, 0.5, 0.9]
        outcomes = [0, 1, 1]
        ece, bins = expected_calibration_error(probs, outcomes)
        assert len(bins) == 10

    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            expected_calibration_error([0.5], [0, 1])


class TestScoreProbabilityQuality:
    """Tests for probability quality scoring."""

    def test_within_range(self):
        result = score_probability_quality(0.75, (0.70, 0.85))
        assert result["calibration_score"] == 3

    def test_at_boundary(self):
        result = score_probability_quality(0.70, (0.70, 0.85))
        assert result["calibration_score"] == 3

    def test_near_range(self):
        result = score_probability_quality(0.65, (0.70, 0.85))
        assert result["calibration_score"] == 2

    def test_moderate_distance(self):
        result = score_probability_quality(0.50, (0.70, 0.85))
        assert result["calibration_score"] == 1

    def test_far_from_range(self):
        result = score_probability_quality(0.30, (0.70, 0.85))
        assert result["calibration_score"] == 0

    def test_no_range_expressed(self):
        result = score_probability_quality(0.75, (0.70, 0.85))
        assert result["range_acknowledgment"] == 0

    def test_range_acknowledged(self):
        result = score_probability_quality(0.75, (0.70, 0.85), expressed_range=(0.70, 0.80))
        assert result["range_acknowledgment"] == 1

    def test_range_overlaps_ground_truth(self):
        result = score_probability_quality(0.75, (0.70, 0.85), expressed_range=(0.70, 0.80))
        assert result["range_quality"] == 1

    def test_range_no_overlap(self):
        result = score_probability_quality(0.40, (0.70, 0.85), expressed_range=(0.30, 0.50))
        assert result["range_quality"] == 0

    def test_total_calibration_max(self):
        result = score_probability_quality(0.75, (0.70, 0.85), expressed_range=(0.70, 0.80))
        assert result["total_calibration"] == 5  # 3 + 1 + 1


class TestParseResponse:
    """Tests for probability extraction from free text."""

    def test_percentage_format(self):
        result = parse_probability_from_response("I estimate a 75% probability of approval")
        assert result is not None
        assert abs(result["point_estimate"] - 0.75) < 0.01

    def test_percent_word(self):
        result = parse_probability_from_response("approximately 80 percent chance")
        assert result is not None
        assert abs(result["point_estimate"] - 0.80) < 0.01

    def test_range_format_dash(self):
        result = parse_probability_from_response("The probability is 70-80%")
        assert result is not None
        assert result["range_low"] is not None
        assert abs(result["range_low"] - 0.70) < 0.01
        assert abs(result["range_high"] - 0.80) < 0.01

    def test_range_format_to(self):
        result = parse_probability_from_response("I'd say 65% to 75% is defensible")
        assert result is not None
        assert result["range_low"] is not None

    def test_range_midpoint(self):
        result = parse_probability_from_response("70-80% probability")
        assert result is not None
        assert abs(result["point_estimate"] - 0.75) < 0.01

    def test_no_probability(self):
        result = parse_probability_from_response("This is a complex situation with many factors")
        assert result is None

    def test_ignores_extreme_values(self):
        # 0% and 100% are typically not probability estimates in context
        result = parse_probability_from_response("The market dropped 100% of its gains")
        assert result is None

    def test_decimal_format(self):
        result = parse_probability_from_response("probability of 0.75 for this outcome")
        assert result is not None
        assert abs(result["point_estimate"] - 0.75) < 0.01
