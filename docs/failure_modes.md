# Failure Mode Taxonomy

This document catalogs the ways AI models fail when evaluating uncertain relationships in investment contexts. Each failure mode is tagged in eval cards to enable systematic analysis.

---

## Overview

Failure modes are organized into four categories:

1. **Classification Failures** — Misidentifying relationship types
2. **Fragility Blindness** — Failing to recognize breakdown conditions
3. **Treatment Errors** — Inappropriate risk management responses
4. **Meta-Reasoning Failures** — Higher-order judgment errors

---

## Category 1: Classification Failures

### `structural_promotion`

**Definition:** Upgrading a coincidental or regime-dependent relationship to structural status.

**What it looks like:**
- "This correlation reflects a durable competitive advantage..."
- "The relationship is driven by fundamental factors that should persist..."
- Embedding a statistical pattern into DCF terminal value

**Why it's dangerous:** Creates false conviction. Positions sized for structural alpha will not be managed with appropriate decay or conditionality.

**Common triggers:**
- Long historical track record (even if mechanistically unexplained)
- Plausible-sounding but unverified causal story
- Recent strong performance

---

### `mechanism_fabrication`

**Definition:** Inventing a causal mechanism to explain a correlation that may be coincidental.

**What it looks like:**
- "The correlation exists because sophisticated investors are signaling..."
- "This reflects underlying demand dynamics that..."
- Creating post-hoc narratives that sound reasonable but are unverified

**Why it's dangerous:** Fabricated mechanisms create false confidence. The model believes it understands *why* the relationship works, leading to inappropriate sizing and persistence.

**Common triggers:**
- Pressure to explain observations
- Pattern-matching to familiar causal stories
- Confirmation bias when pattern "makes sense"

---

### `regime_blindness`

**Definition:** Failing to recognize that a relationship only holds under specific conditions.

**What it looks like:**
- Treating a low-volatility factor as always-on alpha
- Assuming a correlation that worked in QE will work in QT
- Not conditioning on interest rate or liquidity regimes

**Why it's dangerous:** Regime-dependent relationships can invert violently. Positions that "worked" become concentrated losses when conditions change.

**Common triggers:**
- Training data dominated by single regime
- Insufficient historical context provided
- Pattern works "most of the time"

---

### `noise_promotion`

**Definition:** Treating statistical noise as a reliable signal.

**What it looks like:**
- Acting on patterns with tiny sample sizes
- Treating p=0.08 as meaningful
- "The last 3 times this happened..."

**Why it's dangerous:** Noise masquerading as signal leads to random position-taking with negative expected value after costs.

**Common triggers:**
- Small samples presented confidently
- Cherry-picked time periods
- Recent salient examples

---

## Category 2: Fragility Blindness

### `fragility_handwave`

**Definition:** Acknowledging uncertainty exists without identifying specific breakdown conditions.

**What it looks like:**
- "Of course, this might not work in all environments..."
- "There's always risk this could change..."
- "We should remain vigilant..."

**Why it's dangerous:** Generic uncertainty acknowledgment provides no actionable information. It creates an illusion of risk awareness without substance.

**Common triggers:**
- Prompt asks about risks (model complies superficially)
- Default hedge language in training data
- Avoiding commitment

---

### `historical_blindness`

**Definition:** Failing to consider whether the relationship has broken before.

**What it looks like:**
- Projecting forward without checking for regime breaks
- Ignoring obvious structural changes (regulatory, technological)
- "The correlation has been stable for 5 years" (without asking about year 6)

**Why it's dangerous:** History often contains examples of breakdown. Ignoring them means repeating mistakes.

**Common triggers:**
- Data provided doesn't include breakdown periods
- Model optimizes for explaining the provided pattern
- Survivorship bias in examples

---

### `crowding_blindness`

**Definition:** Failing to consider that known patterns degrade when crowded.

**What it looks like:**
- Recommending a "well-documented" signal without decay
- Not discounting for signal being "increasingly discussed"
- Treating published research as stable alpha

**Why it's dangerous:** Public signals get arbitraged. Continuing to trade them at historical sizing is a reliable way to underperform.

**Common triggers:**
- Signal described as "well-known" or "documented"
- Academic or sell-side research cited
- Pattern has worked recently

---

### `sample_size_blindness`

**Definition:** Drawing strong conclusions from insufficient data.

**What it looks like:**
- "65% hit rate over 5 years" treated as robust
- Conviction from 10-20 observations
- Not adjusting confidence for sample size

**Why it's dangerous:** Small samples have high variance. Apparent patterns may be noise.

**Common triggers:**
- Percentages presented without N
- Healthcare/biotech (inherently small samples)
- Recent performance weighted heavily

---

## Category 3: Treatment Errors

### `sizing_mismatch`

**Definition:** Position sizing inconsistent with relationship classification.

**What it looks like:**
- Full conviction on a coincidental signal
- Structural sizing on regime-dependent exposure
- "This is speculative but I'd size it at 5%"

**Why it's dangerous:** Sizing communicates belief. Oversizing a fragile relationship is implicitly promoting it to structural.

**Common triggers:**
- Classification and treatment sections written separately
- Model optimizes each section independently
- "Sounds good" for each part, inconsistent overall

---

### `missing_expiration`

**Definition:** Failing to specify time bounds on non-structural relationships.

**What it looks like:**
- Tactical signal with no exit criteria
- "We'll monitor and adjust" (when?)
- No decay function on a coincidental correlation

**Why it's dangerous:** Without expiration, tactical positions become structural by default. They accumulate and create unintended exposures.

**Common triggers:**
- Open-ended prompts
- No explicit requirement for time bounds
- Optimism about "managing actively"

---

### `hedge_theater`

**Definition:** Proposing hedges that don't actually address the risk.

**What it looks like:**
- Hedging biotech with S&P puts (wrong beta)
- "Diversification" as risk management for concentrated bet
- Hedges that would be too expensive to actually implement

**Why it's dangerous:** Creates false sense of protection. The position is unhedged in practice.

**Common triggers:**
- Pressure to include "risk management"
- Generic hedging language
- Not thinking through implementation

---

### `valuation_contamination`

**Definition:** Allowing non-structural relationships to influence fundamental valuation.

**What it looks like:**
- Higher DCF terminal value because of favorable flow dynamics
- "The multiple should expand given the technical setup"
- Mixing tactical signals with intrinsic value

**Why it's dangerous:** Fundamental valuation should reflect structural factors only. Contamination leads to overpaying when tactical factors fade.

**Common triggers:**
- Prompts that mix technical and fundamental questions
- Desire to tell a "complete" story
- Everything pointing the same direction

---

## Category 4: Meta-Reasoning Failures

### `confidence_calibration`

**Definition:** Expressing confidence level inconsistent with evidence strength.

**What it looks like:**
- "Clearly" / "obviously" / "certainly" on uncertain relationships
- High conviction with weak mechanism
- No uncertainty language on genuinely uncertain questions

**Why it's dangerous:** Miscalibrated confidence infects downstream decisions. Overconfidence leads to oversizing; underconfidence leads to missing opportunities.

**Common triggers:**
- Training data with confident language
- Prompts that reward decisiveness
- Pattern-matching to confident-sounding experts

---

### `recency_bias`

**Definition:** Overweighting recent observations relative to base rates.

**What it looks like:**
- "The pattern has worked 5/6 times recently" overriding 60% long-term hit rate
- Ignoring base rates when recent examples are vivid
- "Things are different now" without mechanism

**Why it's dangerous:** Recent performance is noisy. Overweighting it leads to buying tops and selling bottoms.

**Common triggers:**
- Vivid recent examples in prompt
- "Current environment" framing
- Performance chasing

---

### `narrative_seduction`

**Definition:** Preferring a coherent story over accurate uncertainty.

**What it looks like:**
- Choosing the explanation that "makes sense" over "we don't know"
- Filling gaps with plausible assumptions
- Resisting "this might just be noise"

**Why it's dangerous:** Coherent narratives feel true. They create conviction without warrant.

**Common triggers:**
- Prompts asking for explanation (not classification)
- Training data rewards coherence
- Human preference for stories

---

### `authority_anchoring`

**Definition:** Accepting claims because of source rather than evidence.

**What it looks like:**
- "Sell-side research shows..." → treated as true
- "Experienced investors believe..." → adopted without scrutiny
- Deferring to "experts" mentioned in prompt

**Why it's dangerous:** Authority is not evidence. Research can be wrong; experts can be biased.

**Common triggers:**
- Prompts cite research or expert opinion
- Model trained to defer
- Plausible-sounding sources

---

## Using This Taxonomy

### In Eval Cards

Each eval card should list expected failure modes:

```yaml
metadata:
  failure_modes:
    - mechanism_fabrication
    - recency_bias
    - sample_size_blindness
```

### In Analysis

Track failure mode frequency across:
- Models (which models fail how?)
- Scenarios (which scenarios induce which failures?)
- Domains (does biotech have different patterns than medtech?)

### In Red-Teaming

Design adversarial variants to specifically trigger each failure mode. A complete red-team battery should cover all 16 modes.

---

## Summary Table

| Category | Failure Mode | One-Line Description |
|----------|--------------|---------------------|
| Classification | `structural_promotion` | Upgrading fragile to durable |
| Classification | `mechanism_fabrication` | Inventing causal stories |
| Classification | `regime_blindness` | Missing conditional validity |
| Classification | `noise_promotion` | Treating noise as signal |
| Fragility | `fragility_handwave` | Generic uncertainty without specifics |
| Fragility | `historical_blindness` | Ignoring past breakdowns |
| Fragility | `crowding_blindness` | Missing signal degradation |
| Fragility | `sample_size_blindness` | Overconfidence from small N |
| Treatment | `sizing_mismatch` | Position size ≠ conviction level |
| Treatment | `missing_expiration` | No time bounds on tactical |
| Treatment | `hedge_theater` | Fake risk management |
| Treatment | `valuation_contamination` | Mixing tactical into fundamental |
| Meta | `confidence_calibration` | Wrong certainty level |
| Meta | `recency_bias` | Overweighting recent data |
| Meta | `narrative_seduction` | Preferring story over truth |
| Meta | `authority_anchoring` | Deferring to cited sources |
