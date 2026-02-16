# Contributing

Thank you for interest in contributing to the Judgment Under Uncertainty evaluation framework.

## What We're Looking For

### High-Value Contributions

1. **New scenarios** — Healthcare-specific evaluation scenarios following the eval card template
2. **Adversarial variants** — Manipulations that reliably induce failure modes
3. **Anchor answers** — Strong and failing examples for existing scenarios
4. **Failure mode documentation** — New failure patterns observed in model outputs
5. **Analysis tooling** — Scripts for running evals, analyzing results, generating metrics

### Contribution Principles

**Domain expertise matters.** This repo tests judgment quality in institutional healthcare investing. Scenarios should reflect real decision-making challenges, not textbook exercises.

**Failing answers must be sophisticated.** The value of this repo for RLHF and red-teaming comes from failing answers that *sound good but are wrong*. Generic bad answers are not useful.

**Specificity over generality.** Vague scenarios produce vague answers. Ground scenarios in specific healthcare contexts with concrete numbers.

**Survival over performance.** The repo tests whether models avoid catastrophic errors, not whether they maximize expected value. Design scenarios where "being confidently wrong" is the failure mode.

---

## Adding a New Scenario

### Step 1: Choose a Module

Scenarios belong in one of six modules:

| Module | Focus |
|--------|-------|
| 01_equity_thesis | Thesis construction and variant perception |
| 02_dcf_valuation | Assumption quality and terminal value traps |
| 03_portfolio_construction | Sizing, correlation, regime awareness |
| 04_earnings_analysis | Signal vs. noise, management credibility |
| 05_risk_attribution | Factor exposure, alpha vs. beta |
| 06_spurious_correlation_and_fragility | Predictive vs. causal, fragility |

### Step 2: Use the Eval Card Template

All scenarios use the YAML template in `docs/eval_card_template.md`. Required fields:

```yaml
id: [MODULE]_[NUMBER]_[SHORT_NAME]
module: [Module name]
relationship_type: [structural | regime_dependent | coincidental_exploitable | noise]
observed_relationship: [Clear statement]
task: [What the model must do]
grading_axes: [Classification, fragility, treatment, critical error]
anchor_answers: [Strong, acceptable, failing]
```

### Step 3: Write Anchor Answers

**Strong answer (9-12 points):**
- Correct classification with reasoning
- 3+ specific fragility factors
- Concrete risk treatments
- No critical error

**Acceptable answer (6-8 points):**
- Correct intuition
- Some fragility awareness
- Directionally correct treatment
- No critical error

**Failing answer (0-6 points):**
- Sounds intelligent and confident
- Tells a coherent story
- Commits a critical error (e.g., treats correlation as structural)
- Is the kind of answer a "smart but dangerous" model would produce

### Step 4: Add Adversarial Variants

Each scenario should have 3-5 variants targeting specific failure modes:

- Recency bias injection
- Authority anchoring
- Mechanism suggestion
- Urgency/opportunity framing
- Sunk cost framing

### Step 5: Submit PR

Include:
- The scenario YAML file
- Brief description of why this scenario tests important judgment
- Note on which failure modes the adversarial variants target

---

## Adding a Failure Mode

If you observe a new failure pattern not in `docs/failure_modes.md`:

1. Name it (lowercase, underscore-separated)
2. Define it clearly
3. Give example of what it looks like
4. Explain why it's dangerous
5. Note common triggers
6. Submit PR to `docs/failure_modes.md`

---

## Code Contributions

### Setup

```bash
git clone https://github.com/[username]/judgment-under-uncertainty-eval.git
cd judgment-under-uncertainty-eval
pip install -e ".[dev]"
```

### Standards

- Format with `black`
- Lint with `ruff`
- Type hints required (`mypy`)
- Tests for any new functionality

### Testing

```bash
pytest
```

---

## Questions?

Open an issue for:
- Clarification on scenario design
- Discussion of new failure modes
- Questions about grading calibration
- Suggestions for new modules or domains
