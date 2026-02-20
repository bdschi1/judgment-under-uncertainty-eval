#!/usr/bin/env python3
"""Calibration scoring for probabilistic evaluation scenarios.

Implements proper scoring rules for evaluating probability estimates from
AI models in financial decision contexts. Scoring methodology inspired by
Prophet Arena (Xu et al., UChicago DSI / SIGMA Lab, 2025), adapted for
domain-specific financial event evaluation.

Metrics:
    - Brier score: quadratic scoring rule (0 = perfect, 1 = worst)
    - Log loss: logarithmic scoring rule
    - ECE: Expected Calibration Error (binned calibration metric)
    - Probability quality score: custom 0-3 scale against ground truth ranges

Usage:
    python -m src.calibration results.json --scenarios-dir evals/07_.../scenarios/
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


def brier_score(predicted_prob: float, actual_outcome: int) -> float:
    """Compute Brier score for a single prediction.

    Brier score = (predicted_probability - actual_outcome)^2
    Range: 0 (perfect) to 1 (worst).

    Args:
        predicted_prob: Model's predicted probability in [0, 1].
        actual_outcome: Actual binary outcome (0 or 1).

    Returns:
        Brier score (lower is better).

    Raises:
        ValueError: If predicted_prob is not in [0, 1] or outcome not in {0, 1}.
    """
    if not 0.0 <= predicted_prob <= 1.0:
        raise ValueError(f"predicted_prob must be in [0, 1], got {predicted_prob}")
    if actual_outcome not in (0, 1):
        raise ValueError(f"actual_outcome must be 0 or 1, got {actual_outcome}")
    return (predicted_prob - actual_outcome) ** 2


def log_loss_score(
    predicted_prob: float, actual_outcome: int, eps: float = 1e-15
) -> float:
    """Compute log loss (cross-entropy) for a single prediction.

    Args:
        predicted_prob: Model's predicted probability in [0, 1].
        actual_outcome: Actual binary outcome (0 or 1).
        eps: Small value to avoid log(0).

    Returns:
        Log loss (lower is better). Range: 0 to ~34.5.

    Raises:
        ValueError: If predicted_prob is not in [0, 1] or outcome not in {0, 1}.
    """
    if not 0.0 <= predicted_prob <= 1.0:
        raise ValueError(f"predicted_prob must be in [0, 1], got {predicted_prob}")
    if actual_outcome not in (0, 1):
        raise ValueError(f"actual_outcome must be 0 or 1, got {actual_outcome}")
    p = max(eps, min(1 - eps, predicted_prob))
    if actual_outcome == 1:
        return -math.log(p)
    return -math.log(1 - p)


def expected_calibration_error(
    predicted_probs: List[float],
    actual_outcomes: List[int],
    n_bins: int = 10,
) -> Tuple[float, List[Dict]]:
    """Compute Expected Calibration Error (ECE) across multiple predictions.

    ECE = sum(|bin_accuracy - bin_confidence| * bin_weight)

    Args:
        predicted_probs: List of predicted probabilities.
        actual_outcomes: List of actual binary outcomes.
        n_bins: Number of calibration bins.

    Returns:
        Tuple of (ECE value, list of per-bin statistics).
    """
    if len(predicted_probs) != len(actual_outcomes):
        raise ValueError("predicted_probs and actual_outcomes must have same length")
    if not predicted_probs:
        return 0.0, []

    bin_edges = [i / n_bins for i in range(n_bins + 1)]
    bins_data: List[Dict] = []
    total = len(predicted_probs)
    ece = 0.0

    for b in range(n_bins):
        low, high = bin_edges[b], bin_edges[b + 1]
        indices = [
            i
            for i, p in enumerate(predicted_probs)
            if (low <= p < high) or (b == n_bins - 1 and p == high)
        ]

        if not indices:
            bins_data.append({
                "bin_range": (low, high),
                "count": 0,
                "avg_confidence": 0.0,
                "avg_accuracy": 0.0,
                "gap": 0.0,
            })
            continue

        bin_probs = [predicted_probs[i] for i in indices]
        bin_outcomes = [actual_outcomes[i] for i in indices]
        avg_confidence = sum(bin_probs) / len(bin_probs)
        avg_accuracy = sum(bin_outcomes) / len(bin_outcomes)
        gap = abs(avg_accuracy - avg_confidence)
        weight = len(indices) / total
        ece += gap * weight

        bins_data.append({
            "bin_range": (low, high),
            "count": len(indices),
            "avg_confidence": round(avg_confidence, 4),
            "avg_accuracy": round(avg_accuracy, 4),
            "gap": round(gap, 4),
        })

    return round(ece, 4), bins_data


def score_probability_quality(
    estimated_prob: float,
    ground_truth_range: Tuple[float, float],
    expressed_range: Optional[Tuple[float, float]] = None,
) -> Dict:
    """Score the quality of a probability estimate against ground truth range.

    Calibration score (0-3, matching existing grading axis scale):
        3: Within ground truth range
        2: Within 10 percentage points of nearest range boundary
        1: Within 20 percentage points
        0: More than 20 percentage points away

    Additional scores:
        range_acknowledgment (0-1): Did the model express a range?
        range_quality (0-1): Does the expressed range overlap ground truth?

    Args:
        estimated_prob: Model's probability estimate in [0, 1].
        ground_truth_range: (low, high) defensible probability range in [0, 1].
        expressed_range: Optional (low, high) range the model expressed.

    Returns:
        Dict with calibration_score, range_acknowledgment, range_quality,
        total_calibration.
    """
    gt_low, gt_high = ground_truth_range

    # Distance from range
    if gt_low <= estimated_prob <= gt_high:
        distance = 0.0
    else:
        distance = min(abs(estimated_prob - gt_low), abs(estimated_prob - gt_high))

    # Calibration score (0-3)
    if distance == 0.0:
        calibration_score = 3
    elif distance <= 0.10:
        calibration_score = 2
    elif distance <= 0.20:
        calibration_score = 1
    else:
        calibration_score = 0

    # Range acknowledgment
    range_acknowledgment = 1 if expressed_range is not None else 0

    # Range quality
    range_quality = 0
    if expressed_range is not None:
        er_low, er_high = expressed_range
        # Check overlap
        if er_low <= gt_high and er_high >= gt_low:
            range_quality = 1

    total = calibration_score + range_acknowledgment + range_quality

    return {
        "calibration_score": calibration_score,
        "range_acknowledgment": range_acknowledgment,
        "range_quality": range_quality,
        "total_calibration": total,
        "distance_from_range": round(distance, 4),
    }


def parse_probability_from_response(response: str) -> Optional[Dict]:
    """Extract probability estimates from a model's free-text response.

    Looks for patterns like:
        - "75% probability"
        - "probability of 75%"
        - "I estimate 70-80%"
        - "approximately 0.75"
        - "a 75 percent chance"

    Returns:
        Dict with point_estimate (float in [0,1]), range_low (optional),
        range_high (optional), or None if no probability found.
    """
    text = response.lower()

    # Pattern 1: Range like "70-80%" or "70% to 80%"
    range_pattern = r'(\d{1,3})[\s]*(?:%|percent)?\s*(?:-|to)\s*(\d{1,3})\s*(?:%|percent)'
    range_match = re.search(range_pattern, text)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        if 0 <= low <= 100 and 0 <= high <= 100 and low < high:
            point = (low + high) / 2
            return {
                "point_estimate": point / 100,
                "range_low": low / 100,
                "range_high": high / 100,
            }

    # Pattern 2: Single percentage like "75%" or "75 percent"
    pct_pattern = r'(\d{1,3})\s*(?:%|percent)'
    pct_matches = re.findall(pct_pattern, text)
    if pct_matches:
        # Take the first reasonable probability
        for match in pct_matches:
            val = float(match)
            if 1 <= val <= 99:  # Exclude 0% and 100% as likely not probability estimates
                return {
                    "point_estimate": val / 100,
                    "range_low": None,
                    "range_high": None,
                }

    # Pattern 3: Decimal like "0.75" or "probability of 0.75"
    dec_pattern = r'(?:probability|likelihood|chance|estimate)[^\d]*?(0\.\d{1,4})'
    dec_match = re.search(dec_pattern, text)
    if dec_match:
        val = float(dec_match.group(1))
        if 0 < val < 1:
            return {
                "point_estimate": val,
                "range_low": None,
                "range_high": None,
            }

    return None


def calibration_report(predictions: List[Dict]) -> Dict:
    """Generate a comprehensive calibration report from model predictions.

    Each prediction dict should have:
        - scenario_id: str
        - predicted_prob: float (0-1)
        - ground_truth_range: [low, high] (0-100)
        - expressed_range: optional [low, high] (0-100)

    Returns:
        Dict with per-scenario scores and aggregate metrics.
    """
    per_scenario: List[Dict] = []
    all_scores: List[int] = []

    for pred in predictions:
        gt_range = pred["ground_truth_range"]
        gt_low = gt_range[0] / 100
        gt_high = gt_range[1] / 100

        expressed = None
        if pred.get("expressed_range"):
            expressed = (pred["expressed_range"][0] / 100, pred["expressed_range"][1] / 100)

        quality = score_probability_quality(
            pred["predicted_prob"], (gt_low, gt_high), expressed
        )

        per_scenario.append({
            "scenario_id": pred["scenario_id"],
            "predicted_prob": pred["predicted_prob"],
            "ground_truth_range": pred["ground_truth_range"],
            **quality,
        })
        all_scores.append(quality["calibration_score"])

    avg_calibration = sum(all_scores) / len(all_scores) if all_scores else 0
    range_acknowledgment_rate = (
        sum(1 for s in per_scenario if s["range_acknowledgment"] == 1) / len(per_scenario)
        if per_scenario
        else 0
    )

    return {
        "num_scenarios": len(predictions),
        "avg_calibration_score": round(avg_calibration, 2),
        "range_acknowledgment_rate": round(range_acknowledgment_rate, 2),
        "per_scenario": per_scenario,
    }


def main():
    """CLI for computing calibration scores from evaluation results."""
    parser = argparse.ArgumentParser(
        description="Compute calibration metrics from evaluation results"
    )
    parser.add_argument(
        "results_file",
        type=Path,
        help="Graded results JSON with probability estimates",
    )
    parser.add_argument(
        "--scenarios-dir",
        type=Path,
        help="Path to scenario YAMLs for ground truth ranges",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for calibration report JSON",
    )

    args = parser.parse_args()

    if not args.results_file.exists():
        print(f"Error: File not found: {args.results_file}")
        return 1

    # Load results
    with open(args.results_file) as f:
        results = json.load(f)

    # Load ground truth ranges from scenarios if provided
    gt_ranges: Dict[str, List[float]] = {}
    if args.scenarios_dir and args.scenarios_dir.exists():
        for yaml_file in args.scenarios_dir.glob("*.yaml"):
            with open(yaml_file) as f:
                scenario = yaml.safe_load(f)
            cal_axes = scenario.get("calibration_axes", {})
            prob_est = cal_axes.get("probability_estimate", {})
            if "ground_truth_range" in prob_est:
                gt_ranges[scenario["id"]] = prob_est["ground_truth_range"]

    # Extract predictions from results
    predictions: List[Dict] = []
    for result in results:
        scenario_id = result.get("scenario_id", "")
        base_eval = result.get("base_eval", {})
        response = base_eval.get("response", "")

        parsed = parse_probability_from_response(response)
        if parsed is None:
            print(f"  Warning: No probability found in response for {scenario_id}")
            continue

        gt_range = gt_ranges.get(scenario_id)
        if gt_range is None:
            print(f"  Warning: No ground truth range for {scenario_id}")
            continue

        expressed_range = None
        if parsed["range_low"] is not None and parsed["range_high"] is not None:
            expressed_range = [parsed["range_low"] * 100, parsed["range_high"] * 100]

        predictions.append({
            "scenario_id": scenario_id,
            "predicted_prob": parsed["point_estimate"],
            "ground_truth_range": gt_range,
            "expressed_range": expressed_range,
        })

    if not predictions:
        print("No predictions with matching ground truth found.")
        return 1

    report = calibration_report(predictions)

    # Print summary
    print(f"\nCalibration Report ({report['num_scenarios']} scenarios)")
    print("=" * 60)
    print(f"Average calibration score: {report['avg_calibration_score']}/3")
    print(f"Range acknowledgment rate: {report['range_acknowledgment_rate']:.0%}")
    print()
    for s in report["per_scenario"]:
        print(
            f"  {s['scenario_id']}: "
            f"est={s['predicted_prob']:.0%}, "
            f"gt={s['ground_truth_range']}, "
            f"cal={s['calibration_score']}/3"
        )

    # Save if output specified
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())
