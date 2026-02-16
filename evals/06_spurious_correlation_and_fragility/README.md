# Module 06: Spurious Correlation and Fragility

## Core Idea

In finance, correlations can be exploitable without being causal — but only if their fragility is correctly identified, sized, and constrained.

This module evaluates whether an AI:

- Understands that prediction ≠ causation
- Can exploit conditional dependence **without capitalizing it as structural alpha**
- Knows how to hedge, decay, or quarantine spurious relationships
- Avoids the critical failure: **turning coincidence into conviction**

## What This Module Is NOT

- ❌ Not about "finding spurious correlations"
- ❌ Not about feature engineering
- ❌ Not about statistical significance testing
- ❌ Not about philosophical causality arguments

**It is about decision quality once a correlation is observed.**

---

## Scenarios

| ID | Title | Relationship Type | Difficulty |
|----|-------|-------------------|------------|
| 06_01 | Biotech ETF Flows and Small-Cap Outperformance | Coincidental Exploitable | Medium |
| 06_02 | GLP-1 News and MedTech Multiple Expansion | Regime-Dependent | Hard |
| 06_03 | Low-Volatility Factor in Healthcare Services | Regime-Dependent | Medium |
| 06_04 | Pharma R&D Spend and Life Sciences Tools Revenue | Structural (with caveats) | Medium |
| 06_05 | Small-Cap Biotech and Rate Cuts | Regime-Dependent | Hard |

---

## How to Use This Module

### For Evaluation

Run each scenario as a standalone prompt. Score using the universal rubric (see `/docs/grading_rubric.md`).

### For RLHF

Use the strong/failing anchor answer pairs for preference learning. The failing answers are intentionally sophisticated.

### For Red-Teaming

Use the adversarial variants to probe model weaknesses. Track which manipulations reliably induce critical errors.

---

## Key Concepts Tested

### Relationship Classification

Models must correctly distinguish:

| Type | Definition | Appropriate Treatment |
|------|------------|----------------------|
| Structural | Causal, mechanism-based, durable | Can inform valuation |
| Regime-Dependent | Valid only under specific conditions | Conditional exposure, state monitoring |
| Coincidental Exploitable | Predictive but not causal | Size limits, expiration, no valuation impact |
| Non-Actionable Noise | No reliable signal | Ignore |

### Fragility Awareness

For any non-structural relationship, models must identify:

1. What sustains the relationship
2. What would break it
3. Historical precedents for breakdown
4. Expected decay timeline

### Risk Treatment

Models must specify concrete controls, not generic language:

| Treatment | When to Use |
|-----------|-------------|
| Position sizing cap | All non-structural relationships |
| Time-bound expiration | Coincidental and regime-dependent |
| Exclusion from valuation | Anything not structural |
| Hedge requirement | Material sizing on fragile signals |
| Monitoring triggers | Regime-dependent relationships |

---

## Critical Error

The single most important evaluation axis:

> **Did the model misclassify an environmental, regime-dependent, or spurious correlation as durable structural alpha?**

This error is caught when:
- A coincidental correlation is embedded in DCF terminal value
- Factor exposure is treated as stock-specific alpha
- A regime-dependent relationship is projected forward unconditionally
- Conviction is built on pattern without mechanism

An answer that commits this error is **capped at 6/12** regardless of other scores.

---

## Module-Specific Grading Notes

### Common Partial Credit Situations

- Classifying as "regime-dependent" when "coincidental" is more accurate: -1 on classification
- Right intuition on fragility but vague factors: -1 on fragility
- Appropriate caution but no specific sizing guidance: -1 on treatment

### Common Full Failure Situations

- Inventing a mechanism to explain a correlation → critical error
- "This signal can be incorporated into our structural view" → critical error
- Treating 5-year hit rate as "robust" without sample size adjustment → fragility = 0

### Adversarial Robustness

Strong models should resist:
- Recency bias manipulation ("worked 5/6 times recently")
- Authority anchoring ("research shows...")
- Mechanism suggestion ("likely reflects smart money...")

Scenarios include adversarial variants designed to induce these failures.
