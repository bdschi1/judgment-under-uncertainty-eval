#!/usr/bin/env python3
"""Run evaluations against AI models.

Usage:
    # Single scenario
    python -m src.run_eval --scenario evals/06_.../scenarios/06_01_etf_flow_correlation.yaml --model gpt-4-turbo

    # Full module
    python -m src.run_eval --module 06_spurious_correlation_and_fragility --model claude-3-opus-20240229

    # With adversarial variants
    python -m src.run_eval --scenario ... --model ... --adversarial
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


def load_scenario(path: Path) -> dict:
    """Load a scenario YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def build_prompt(scenario: dict, adversarial_variant: Optional[dict] = None) -> str:
    """Build the evaluation prompt from a scenario."""
    parts = []

    # Observed relationship
    parts.append("## Observed Relationship")
    parts.append(scenario["observed_relationship"].strip())

    # Context if present
    if "context" in scenario:
        parts.append("\n## Context")
        parts.append(scenario["context"].strip())

    # Adversarial manipulation if provided
    if adversarial_variant:
        parts.append("\n## Additional Information")
        parts.append(adversarial_variant["manipulation"].strip())

    # Task
    parts.append("\n## Task")
    parts.append(scenario["task"].strip())

    # Module 07: add explicit probability instruction
    if scenario.get("module", "").startswith("07"):
        parts.append("\n## Important")
        parts.append(
            "For this scenario, you must provide explicit numerical probability "
            "estimates (0-100%) with justification. Do not just give qualitative "
            "assessments. Provide a point estimate and a defensible range."
        )

    return "\n\n".join(parts)


def call_openai(prompt: str, model: str) -> str:
    """Call OpenAI API."""
    if OpenAI is None:
        raise ImportError("openai package not installed. Run: pip install openai")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a senior healthcare investment analyst. Provide thorough, specific analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000,
    )
    return response.choices[0].message.content


def call_anthropic(prompt: str, model: str) -> str:
    """Call Anthropic API."""
    if Anthropic is None:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system="You are a senior healthcare investment analyst. Provide thorough, specific analysis.",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def call_model(prompt: str, model: str) -> str:
    """Route to appropriate API based on model name."""
    if model.startswith("gpt") or model.startswith("o1"):
        return call_openai(prompt, model)
    elif model.startswith("claude"):
        return call_anthropic(prompt, model)
    else:
        raise ValueError(f"Unknown model: {model}. Expected gpt-* or claude-*")


def get_scenarios_for_module(module_name: str) -> List[Path]:
    """Get all scenario files for a module."""
    evals_dir = Path(__file__).parent.parent / "evals"
    module_dir = evals_dir / module_name / "scenarios"

    if not module_dir.exists():
        raise FileNotFoundError(f"Module not found: {module_dir}")

    return sorted(module_dir.glob("*.yaml"))


def run_single_eval(
    scenario_path: Path,
    model: str,
    include_adversarial: bool = False,
) -> dict:
    """Run evaluation on a single scenario."""
    scenario = load_scenario(scenario_path)
    results = {
        "scenario_id": scenario["id"],
        "scenario_path": str(scenario_path),
        "model": model,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "relationship_type_ground_truth": scenario["relationship_type"],
        "base_eval": None,
        "adversarial_evals": [],
    }

    # Run base evaluation
    print(f"  Running base eval for {scenario['id']}...")
    prompt = build_prompt(scenario)
    response = call_model(prompt, model)
    results["base_eval"] = {
        "prompt": prompt,
        "response": response,
        "scores": None,  # To be filled by human grader
        "notes": "",
    }

    # Run adversarial variants if requested
    if include_adversarial and "adversarial_variants" in scenario:
        for variant in scenario["adversarial_variants"]:
            print(f"    Running adversarial variant {variant['variant_id']}...")
            adv_prompt = build_prompt(scenario, variant)
            adv_response = call_model(adv_prompt, model)
            results["adversarial_evals"].append({
                "variant_id": variant["variant_id"],
                "manipulation": variant["manipulation"],
                "expected_failure_mode": variant["expected_failure_mode"],
                "prompt": adv_prompt,
                "response": adv_response,
                "scores": None,
                "notes": "",
            })

    return results


def save_results(results: dict | list, output_dir: Path, filename: str):
    """Save results to JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Run judgment-under-uncertainty evaluations")
    parser.add_argument(
        "--scenario",
        type=Path,
        help="Path to a single scenario YAML file",
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Module name to run all scenarios (e.g., 06_spurious_correlation_and_fragility)",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to evaluate (e.g., gpt-4-turbo, claude-3-opus-20240229)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs"),
        help="Output directory for results",
    )
    parser.add_argument(
        "--adversarial",
        action="store_true",
        help="Include adversarial variants",
    )

    args = parser.parse_args()

    if not args.scenario and not args.module:
        parser.error("Must specify either --scenario or --module")

    if args.scenario and args.module:
        parser.error("Specify only one of --scenario or --module")

    # Determine scenarios to run
    if args.scenario:
        scenarios = [args.scenario]
    else:
        scenarios = get_scenarios_for_module(args.module)

    print(f"Running {len(scenarios)} scenario(s) against {args.model}")
    print(f"Adversarial variants: {'Yes' if args.adversarial else 'No'}")
    print()

    all_results = []
    for scenario_path in scenarios:
        print(f"Evaluating: {scenario_path.name}")
        result = run_single_eval(scenario_path, args.model, args.adversarial)
        all_results.append(result)

    # Save results
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    if args.scenario:
        filename = f"{args.scenario.stem}_{args.model}_{timestamp}.json"
    else:
        filename = f"{args.module}_{args.model}_{timestamp}.json"

    save_results(all_results, args.output, filename)

    print()
    print("Evaluation complete. Results saved.")
    print("Next step: Review responses and add scores using the grading rubric.")
    print("See: docs/grading_rubric.md")


if __name__ == "__main__":
    main()
