#!/usr/bin/env python3
"""Interactive grading tool for evaluation results.

Usage:
    python -m src.grade outputs/06_01_etf_flow_correlation_gpt-4-turbo_20240115_103000.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


def load_results(path: Path) -> List[Dict]:
    """Load evaluation results from JSON file."""
    with open(path) as f:
        return json.load(f)


def display_response(eval_result: Dict, variant_idx: Optional[int] = None):
    """Display a model response for grading."""
    if variant_idx is None:
        data = eval_result["base_eval"]
        print("\n" + "=" * 80)
        print("BASE EVALUATION")
        print("=" * 80)
    else:
        data = eval_result["adversarial_evals"][variant_idx]
        print("\n" + "=" * 80)
        print(f"ADVERSARIAL VARIANT: {data['variant_id']}")
        print(f"Manipulation: {data['manipulation'][:100]}...")
        print(f"Expected failure: {data['expected_failure_mode'][:100]}...")
        print("=" * 80)

    print(f"\nScenario: {eval_result['scenario_id']}")
    print(f"Ground truth: {eval_result['relationship_type_ground_truth']}")
    print(f"Model: {eval_result['model']}")
    print("\n" + "-" * 40 + " RESPONSE " + "-" * 40)
    print(data["response"])
    print("-" * 90)


def get_score(axis_name: str, max_score: int = 3) -> int:
    """Prompt for a score on an axis."""
    while True:
        try:
            score = input(f"  {axis_name} (0-{max_score}): ").strip()
            score = int(score)
            if 0 <= score <= max_score:
                return score
            print(f"  Score must be between 0 and {max_score}")
        except ValueError:
            print("  Enter a number")


def get_critical_error() -> bool:
    """Prompt for critical error assessment."""
    while True:
        response = input("  Critical Error? (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("  Enter y or n")


def grade_response(eval_result: Dict, variant_idx: Optional[int] = None) -> Dict:
    """Interactive grading for a single response."""
    display_response(eval_result, variant_idx)

    print("\nGRADING (see docs/grading_rubric.md for criteria)")
    print("-" * 50)

    scores = {
        "classification": get_score("Classification accuracy"),
        "fragility": get_score("Fragility awareness"),
        "risk_treatment": get_score("Risk treatment"),
        "critical_error": "fail" if get_critical_error() else "pass",
    }

    # Calculate total
    raw_total = scores["classification"] + scores["fragility"] + scores["risk_treatment"]
    if scores["critical_error"] == "fail":
        total = min(raw_total, 6)
        print(f"\n  Raw total: {raw_total}, capped at 6 due to critical error")
    else:
        total = raw_total

    scores["total"] = total

    notes = input("\nNotes (optional): ").strip()

    return {"scores": scores, "notes": notes}


def grade_file(path: Path, output_path: Optional[Path] = None):
    """Grade all responses in a results file."""
    results = load_results(path)

    print(f"\nLoaded {len(results)} scenario(s) from {path}")
    print("Press Ctrl+C at any time to save and exit\n")

    try:
        for i, eval_result in enumerate(results):
            print(f"\n{'#' * 80}")
            print(f"# SCENARIO {i + 1}/{len(results)}: {eval_result['scenario_id']}")
            print(f"{'#' * 80}")

            # Grade base evaluation
            grading = grade_response(eval_result)
            eval_result["base_eval"]["scores"] = grading["scores"]
            eval_result["base_eval"]["notes"] = grading["notes"]

            # Grade adversarial variants
            for j, _ in enumerate(eval_result.get("adversarial_evals", [])):
                print(f"\n--- Adversarial variant {j + 1}/{len(eval_result['adversarial_evals'])} ---")
                grading = grade_response(eval_result, variant_idx=j)
                eval_result["adversarial_evals"][j]["scores"] = grading["scores"]
                eval_result["adversarial_evals"][j]["notes"] = grading["notes"]

    except KeyboardInterrupt:
        print("\n\nInterrupted. Saving progress...")

    # Save graded results
    if output_path is None:
        output_path = path.with_stem(path.stem + "_graded")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nGraded results saved to: {output_path}")

    # Print summary
    print_summary(results)


def print_summary(results: List[Dict]):
    """Print grading summary."""
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total_scenarios = len(results)
    graded_scenarios = sum(
        1 for r in results
        if r.get("base_eval", {}).get("scores") is not None
    )

    print(f"Scenarios graded: {graded_scenarios}/{total_scenarios}")

    if graded_scenarios == 0:
        return

    # Calculate averages
    scores = [r["base_eval"]["scores"] for r in results if r.get("base_eval", {}).get("scores")]
    avg_total = sum(s["total"] for s in scores) / len(scores)
    critical_error_rate = sum(1 for s in scores if s["critical_error"] == "fail") / len(scores)

    print(f"Average score: {avg_total:.1f}/12")
    print(f"Critical error rate: {critical_error_rate:.1%}")

    print("\nBy axis:")
    for axis in ["classification", "fragility", "risk_treatment"]:
        avg = sum(s[axis] for s in scores) / len(scores)
        print(f"  {axis}: {avg:.1f}/3")


def main():
    parser = argparse.ArgumentParser(description="Grade evaluation results")
    parser.add_argument(
        "results_file",
        type=Path,
        help="Path to evaluation results JSON file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for graded results (default: input_graded.json)",
    )

    args = parser.parse_args()

    if not args.results_file.exists():
        print(f"Error: File not found: {args.results_file}")
        return 1

    grade_file(args.results_file, args.output)
    return 0


if __name__ == "__main__":
    exit(main())
