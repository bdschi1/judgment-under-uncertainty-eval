# Usage Guide

This document explains how to use the evaluation framework for different purposes.

---

## Quick Start

### 1. Setup

```bash
# Clone the repo
git clone https://github.com/[username]/judgment-under-uncertainty-eval.git
cd judgment-under-uncertainty-eval

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[all]"  # Full install
# Or minimal: pip install -e .

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run a Single Evaluation

```bash
python -m src.run_eval \
  --scenario evals/06_spurious_correlation_and_fragility/scenarios/06_01_etf_flow_correlation.yaml \
  --model gpt-4-turbo \
  --output outputs/
```

### 3. Run All Scenarios in a Module

```bash
python -m src.run_eval \
  --module 06_spurious_correlation_and_fragility \
  --model claude-3-opus-20240229 \
  --output outputs/
```

---

## Use Cases

### A. Evaluating a Model

**Goal:** Test how well a model handles judgment-under-uncertainty scenarios.

**Steps:**

1. Choose scenarios (single, module, or all)
2. Run evaluation against target model
3. Review outputs and scores

```bash
# Run Module 06 against GPT-4
python -m src.run_eval \
  --module 06_spurious_correlation_and_fragility \
  --model gpt-4-turbo \
  --output outputs/gpt4_module06/
```

**Output:** For each scenario, you get:
- Model's raw response
- Scores on each axis (0-3)
- Critical error flag (pass/fail)
- Total score (0-12, capped at 6 if critical error)

### B. Manual Evaluation (No Code)

If you don't want to run code, you can use the scenarios directly:

1. **Open a scenario YAML file** (e.g., `06_01_etf_flow_correlation.yaml`)

2. **Copy the prompt** from `observed_relationship` + `context` + `task`

3. **Paste into your model interface** (ChatGPT, Claude, API playground)

4. **Grade the response** using `docs/grading_rubric.md`:
   - Classification (0-3)
   - Fragility (0-3)
   - Risk Treatment (0-3)
   - Critical Error (Pass/Fail)

5. **Compare to anchor answers** in the YAML to calibrate your grading

### C. Creating RLHF Preference Pairs

**Goal:** Generate training data for preference learning.

Each scenario contains `strong` and `failing` anchor answers designed as preference pairs:

```python
import yaml

with open("evals/06_.../scenarios/06_01_etf_flow_correlation.yaml") as f:
    scenario = yaml.safe_load(f)

# Extract preference pair
prompt = f"{scenario['observed_relationship']}\n\n{scenario['task']}"
chosen = scenario['anchor_answers']['strong']['response']
rejected = scenario['anchor_answers']['failing']['response']

# Format for your RLHF pipeline
preference_pair = {
    "prompt": prompt,
    "chosen": chosen,
    "rejected": rejected,
}
```

**Key insight:** The `failing` answers are intentionally sophisticated—they sound confident and tell coherent stories. This creates meaningful training signal.

### D. Red-Teaming with Adversarial Variants

**Goal:** Test model robustness against manipulations.

Each scenario has `adversarial_variants` that modify the prompt to induce failures:

```python
# Load scenario
with open("evals/06_.../scenarios/06_01_etf_flow_correlation.yaml") as f:
    scenario = yaml.safe_load(f)

# Get base prompt
base_prompt = f"{scenario['observed_relationship']}\n\n{scenario['task']}"

# Get adversarial variant
variant = scenario['adversarial_variants'][0]
manipulation = variant['manipulation']
expected_failure = variant['expected_failure_mode']

# Create adversarial prompt (manually combine base + manipulation)
adversarial_prompt = f"{scenario['observed_relationship']}\n\n{manipulation}\n\n{scenario['task']}"

# Run both through model, compare responses
# If model fails on adversarial but passes on base, it's susceptible to this manipulation
```

### E. Extending to New Domains

**Goal:** Create scenarios for non-healthcare domains.

1. **Copy the template** from `docs/eval_card_template.md`

2. **Adapt for your domain:**
   - Change `domain` field
   - Write domain-specific `observed_relationship`
   - Adjust `grading_axes` notes for domain context
   - Create domain-appropriate anchor answers

3. **Maintain the core structure:**
   - 4 relationship types (structural, regime-dependent, coincidental, noise)
   - 4 grading axes (classification, fragility, treatment, critical error)
   - 3 anchor answers (strong, acceptable, failing)
   - Adversarial variants

---

## Grading Calibration

### Using Anchor Answers

Before grading model outputs, calibrate by reviewing anchor answers:

1. Read the **strong** answer — this is a 9-11/12
2. Read the **acceptable** answer — this is a 6-8/12
3. Read the **failing** answer — this is 0-6/12 (capped due to critical error)

Ask yourself: "Is this model response closer to strong, acceptable, or failing?"

### Common Grading Mistakes

| Mistake | How to Avoid |
|---------|--------------|
| Rewarding length | Grade on content, not word count |
| Accepting hedge words as fragility | "Might not work" ≠ fragility analysis |
| Missing subtle critical errors | Check if correlation is treated as structural |
| Inconsistent axis scoring | Score each axis independently |

### Inter-Rater Reliability

If multiple people are grading:
- Axes 1-3: Accept ±1 point variance
- Axis 4 (critical error): Must agree on Pass/Fail
- If disagreement on Axis 4, discuss and reach consensus

---

## Output Format

### Single Scenario Output

```json
{
  "scenario_id": "06_01_etf_flow_correlation",
  "model": "gpt-4-turbo",
  "timestamp": "2024-01-15T10:30:00Z",
  "response": "Model's full response text...",
  "scores": {
    "classification": 2,
    "fragility": 3,
    "risk_treatment": 2,
    "critical_error": "pass"
  },
  "total_score": 7,
  "notes": "Grader notes..."
}
```

### Module Summary Output

```json
{
  "module": "06_spurious_correlation_and_fragility",
  "model": "gpt-4-turbo",
  "timestamp": "2024-01-15T10:45:00Z",
  "scenarios_run": 5,
  "average_score": 7.4,
  "critical_error_rate": 0.2,
  "scores_by_scenario": {
    "06_01": 7,
    "06_02": 8,
    "06_03": 5,
    "06_04": 9,
    "06_05": 8
  }
}
```

---

## Metrics to Track

### Per-Model Metrics

| Metric | What It Measures |
|--------|------------------|
| **Average Score** | Overall judgment quality (0-12) |
| **Critical Error Rate (CER)** | % of scenarios with critical error |
| **Axis Breakdown** | Where does the model struggle? |

### Adversarial Metrics

| Metric | What It Measures |
|--------|------------------|
| **Adversarial Robustness Rate (ARR)** | % correct on adversarial / % correct on base |
| **Manipulation Susceptibility** | Which manipulations cause most failures |

### Cross-Model Comparison

| Metric | What It Measures |
|--------|------------------|
| **Rank by CER** | Which models avoid critical errors best |
| **Score Distribution** | Consistency vs. variance |

---

## FAQ

**Q: Can I run this without API keys?**

Yes. Use the "Manual Evaluation" workflow — copy prompts to any model interface and grade by hand.

**Q: How long does a full evaluation take?**

Module 06 (5 scenarios) takes ~5-10 minutes with API calls, depending on rate limits. Manual grading adds ~10-15 minutes per scenario.

**Q: Can I add my own scenarios?**

Yes. See `CONTRIBUTING.md` for the scenario template and submission process.

**Q: What if I disagree with the ground truth classification?**

Open an issue. The classifications are judgment calls; reasonable people can disagree. But the grading rubric should still apply to whatever classification you use.

**Q: Is this only for healthcare?**

The current scenarios are healthcare-focused, but the framework (relationship types, grading axes, failure modes) applies to any domain with regime-dependent or spurious correlations.
