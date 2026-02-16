"""Tests for scenario YAML validation."""

import os
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent
EVALS_DIR = REPO_ROOT / "evals"

REQUIRED_SCENARIO_FIELDS = [
    "id",
    "module",
    "relationship_type",
    "observed_relationship",
    "task",
    "grading_axes",
    "anchor_answers",
]

VALID_RELATIONSHIP_TYPES = [
    "structural",
    "regime_dependent",
    "coincidental_exploitable",
    "noise",
]

REQUIRED_GRADING_AXES = [
    "classification",
    "fragility",
    "risk_treatment",
    "critical_error",
]

REQUIRED_ANCHOR_ANSWERS = [
    "strong",
    "acceptable",
    "failing",
]


def get_scenario_files():
    """Find all scenario YAML files in the evals directory."""
    scenario_files = []
    for module_dir in EVALS_DIR.iterdir():
        if module_dir.is_dir():
            scenarios_dir = module_dir / "scenarios"
            if scenarios_dir.exists():
                for yaml_file in scenarios_dir.glob("*.yaml"):
                    scenario_files.append(yaml_file)
    return scenario_files


@pytest.fixture
def scenario_files():
    """Fixture providing all scenario files."""
    return get_scenario_files()


class TestScenarioStructure:
    """Tests for scenario YAML structure and required fields."""

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_scenario_is_valid_yaml(self, scenario_file):
        """Test that scenario files are valid YAML."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"{scenario_file} is empty or invalid YAML"

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_scenario_has_required_fields(self, scenario_file):
        """Test that scenarios have all required top-level fields."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        for field in REQUIRED_SCENARIO_FIELDS:
            assert field in data, f"{scenario_file} missing required field: {field}"

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_relationship_type_is_valid(self, scenario_file):
        """Test that relationship_type is one of the valid options."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        rel_type = data.get("relationship_type")
        assert rel_type in VALID_RELATIONSHIP_TYPES, (
            f"{scenario_file} has invalid relationship_type: {rel_type}. "
            f"Must be one of: {VALID_RELATIONSHIP_TYPES}"
        )

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_grading_axes_complete(self, scenario_file):
        """Test that all required grading axes are present."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        grading_axes = data.get("grading_axes", {})
        for axis in REQUIRED_GRADING_AXES:
            assert axis in grading_axes, (
                f"{scenario_file} missing grading axis: {axis}"
            )

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_anchor_answers_complete(self, scenario_file):
        """Test that all required anchor answers are present."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        anchor_answers = data.get("anchor_answers", {})
        for answer_type in REQUIRED_ANCHOR_ANSWERS:
            assert answer_type in anchor_answers, (
                f"{scenario_file} missing anchor answer: {answer_type}"
            )

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_anchor_answers_have_response(self, scenario_file):
        """Test that each anchor answer has a response field."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        anchor_answers = data.get("anchor_answers", {})
        for answer_type, answer in anchor_answers.items():
            assert "response" in answer, (
                f"{scenario_file} anchor answer '{answer_type}' missing 'response' field"
            )
            assert len(answer["response"]) > 100, (
                f"{scenario_file} anchor answer '{answer_type}' response seems too short"
            )


class TestScenarioContent:
    """Tests for scenario content quality."""

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_id_matches_filename(self, scenario_file):
        """Test that scenario ID matches the filename."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        expected_id = scenario_file.stem
        actual_id = data.get("id")
        assert actual_id == expected_id, (
            f"Scenario ID '{actual_id}' doesn't match filename '{expected_id}'"
        )

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_failing_answer_has_critical_error_explanation(self, scenario_file):
        """Test that failing answers explain the critical error."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        failing = data.get("anchor_answers", {}).get("failing", {})
        notes = failing.get("notes", "")

        # Check that notes mention critical error
        assert "critical error" in notes.lower() or "critical_error" in notes.lower(), (
            f"{scenario_file} failing answer notes should explain the critical error"
        )

    @pytest.mark.parametrize("scenario_file", get_scenario_files())
    def test_has_adversarial_variants(self, scenario_file):
        """Test that scenarios have adversarial variants."""
        with open(scenario_file) as f:
            data = yaml.safe_load(f)

        variants = data.get("adversarial_variants", [])
        assert len(variants) >= 2, (
            f"{scenario_file} should have at least 2 adversarial variants"
        )


class TestScenarioConsistency:
    """Tests for consistency across scenarios."""

    def test_at_least_one_scenario_exists(self, scenario_files):
        """Test that at least one scenario exists."""
        assert len(scenario_files) > 0, "No scenario files found"

    def test_module_06_has_all_scenarios(self):
        """Test that Module 06 has all expected scenarios."""
        module_06_dir = EVALS_DIR / "06_spurious_correlation_and_fragility" / "scenarios"
        expected_scenarios = [
            "06_01_etf_flow_correlation.yaml",
            "06_02_glp1_medtech_correlation.yaml",
            "06_03_low_vol_healthcare_services.yaml",
            "06_04_pharma_rd_tools.yaml",
            "06_05_smallcap_biotech_rates.yaml",
        ]

        for scenario in expected_scenarios:
            assert (module_06_dir / scenario).exists(), (
                f"Expected scenario not found: {scenario}"
            )
