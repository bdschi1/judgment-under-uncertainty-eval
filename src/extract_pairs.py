#!/usr/bin/env python3
"""Extract preference pairs from scenarios for RLHF training.

Usage:
    # Extract from all scenarios
    python -m src.extract_pairs --output preference_pairs.jsonl

    # Extract from specific module
    python -m src.extract_pairs --module 06_spurious_correlation_and_fragility --output pairs.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

import yaml


def load_scenario(path: Path) -> dict:
    """Load a scenario YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def build_prompt(scenario: dict) -> str:
    """Build the evaluation prompt from a scenario."""
    parts = []

    parts.append("## Observed Relationship")
    parts.append(scenario["observed_relationship"].strip())

    if "context" in scenario:
        parts.append("\n## Context")
        parts.append(scenario["context"].strip())

    parts.append("\n## Task")
    parts.append(scenario["task"].strip())

    return "\n\n".join(parts)


def extract_preference_pair(scenario: dict) -> dict:
    """Extract a preference pair from a scenario."""
    prompt = build_prompt(scenario)

    return {
        "scenario_id": scenario["id"],
        "prompt": prompt,
        "chosen": scenario["anchor_answers"]["strong"]["response"].strip(),
        "rejected": scenario["anchor_answers"]["failing"]["response"].strip(),
        "chosen_score": scenario["anchor_answers"]["strong"].get("score", 11),
        "rejected_score": scenario["anchor_answers"]["failing"].get("score", 5),
        "rejection_reason": scenario["anchor_answers"]["failing"].get("notes", ""),
        "relationship_type": scenario["relationship_type"],
    }


def get_all_scenarios(evals_dir: Path, module: Optional[str] = None) -> List[Path]:
    """Get all scenario files, optionally filtered by module."""
    scenarios = []

    if module:
        module_dir = evals_dir / module / "scenarios"
        if module_dir.exists():
            scenarios.extend(module_dir.glob("*.yaml"))
    else:
        for module_dir in evals_dir.iterdir():
            if module_dir.is_dir():
                scenarios_dir = module_dir / "scenarios"
                if scenarios_dir.exists():
                    scenarios.extend(scenarios_dir.glob("*.yaml"))

    return sorted(scenarios)


def main():
    parser = argparse.ArgumentParser(description="Extract RLHF preference pairs from scenarios")
    parser.add_argument(
        "--module",
        type=str,
        help="Extract from specific module only",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("preference_pairs.jsonl"),
        help="Output JSONL file",
    )
    parser.add_argument(
        "--format",
        choices=["jsonl", "json"],
        default="jsonl",
        help="Output format (jsonl for streaming, json for array)",
    )

    args = parser.parse_args()

    evals_dir = Path(__file__).parent.parent / "evals"
    scenarios = get_all_scenarios(evals_dir, args.module)

    print(f"Found {len(scenarios)} scenario(s)")

    pairs = []
    for scenario_path in scenarios:
        print(f"  Processing: {scenario_path.name}")
        scenario = load_scenario(scenario_path)
        pair = extract_preference_pair(scenario)
        pairs.append(pair)

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "jsonl":
        with open(args.output, "w") as f:
            for pair in pairs:
                f.write(json.dumps(pair) + "\n")
    else:
        with open(args.output, "w") as f:
            json.dump(pairs, f, indent=2)

    print(f"\nExtracted {len(pairs)} preference pairs to {args.output}")
    print("\nFormat:")
    print("  - prompt: The scenario task")
    print("  - chosen: Strong anchor answer (9-11/12)")
    print("  - rejected: Failing anchor answer (commits critical error)")


if __name__ == "__main__":
    main()
