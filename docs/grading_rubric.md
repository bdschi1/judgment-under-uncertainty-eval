# Universal Grading Rubric

This rubric applies to all evaluation modules. Every model response is scored on four axes.

---

## Scoring Overview

| Axis | Weight | Range | Description |
|------|--------|-------|-------------|
| Classification Accuracy | Core | 0-3 | Correct categorization of relationship type |
| Fragility Awareness | Core | 0-3 | Recognition of breakdown conditions |
| Risk Treatment | Core | 0-3 | Concrete, actionable controls specified |
| Critical Error Avoidance | Binary | Pass/Fail | Did not misclassify spurious as structural |

**Maximum Score: 12 points** (if no critical error)
**Critical Error: Automatic cap at 6 points** regardless of other scores

---

## Axis 1: Classification Accuracy (0-3)

Did the model correctly classify the observed relationship?

### Relationship Types

| Type | Definition | Example |
|------|------------|---------|
| **Structural** | Mechanism-based, durable across regimes | Drug efficacy → revenue (assuming approval) |
| **Regime-Dependent** | Valid only under specific macro/policy conditions | Low-vol factor works in risk-off environments |
| **Coincidental but Exploitable** | Statistically predictive, no causal mechanism | ETF flows predict short-term returns |
| **Non-Actionable Noise** | No reliable predictive or causal value | Spurious correlation, sample artifact |

### Scoring

| Score | Criteria |
|-------|----------|
| 3 | Correct classification with explicit reasoning for why alternatives were rejected |
| 2 | Correct classification, reasoning present but incomplete |
| 1 | Partially correct (e.g., "regime-dependent" when "coincidental" was more accurate) |
| 0 | Incorrect classification or no classification attempted |

---

## Axis 2: Fragility Awareness (0-3)

Does the model identify why and how the relationship can break?

### Components of Strong Fragility Analysis

1. **Mechanism vulnerability** — What sustains the relationship? What would disrupt it?
2. **Regime conditions** — Under what macro/policy states does it hold?
3. **Historical precedent** — Has it broken before? What happened?
4. **Time horizon** — Is decay expected? Over what period?

### Scoring

| Score | Criteria |
|-------|----------|
| 3 | Identifies 3+ fragility factors with specific, concrete examples |
| 2 | Identifies 2 fragility factors, some specificity |
| 1 | Acknowledges fragility exists but vague or generic |
| 0 | No fragility discussion or claims relationship is robust without justification |

---

## Axis 3: Risk Treatment & Actionability (0-3)

Does the model specify concrete controls for managing the relationship?

### Valid Risk Treatments

| Treatment | When Appropriate |
|-----------|------------------|
| **Position sizing cap** | Coincidental relationships; regime-dependent exposures |
| **Hedge requirement** | Exploitable correlations with identifiable risk factors |
| **Time decay / expiration** | Relationships expected to weaken; event-driven setups |
| **Exclusion from valuation** | Do not embed in DCF terminal value or structural models |
| **Monitoring triggers** | Conditions that would invalidate the thesis |
| **Quarantine** | Track but do not act until conditions clarify |

### Scoring

| Score | Criteria |
|-------|----------|
| 3 | 2+ specific treatments with rationale; treatments match relationship type |
| 2 | 1-2 treatments specified, appropriate but incomplete rationale |
| 1 | Generic risk language ("be careful", "monitor closely") without specifics |
| 0 | No risk treatment or inappropriate treatment (e.g., "size up" on spurious signal) |

---

## Axis 4: Critical Error Avoidance (Binary)

**The single most important axis.**

### Critical Error Definition

> Misclassified an environmental, regime-dependent, or spurious correlation as **durable structural alpha**.

### What This Looks Like

- Embedding a coincidental correlation in a DCF terminal value
- Treating factor exposure as stock-specific alpha
- Projecting a regime-dependent relationship forward without conditionality
- Building conviction on a pattern without mechanism

### Scoring

| Result | Effect |
|--------|--------|
| **Pass** | No penalty; total score = sum of Axes 1-3 |
| **Fail** | Total score capped at 6, regardless of Axes 1-3 |

### Why This Matters

A model that scores 3/3/3 on the first three axes but commits a critical error has produced a **dangerous output**. It sounds competent, tells a coherent story, and will confidently lose money.

The critical error check is designed to catch exactly this failure mode.

---

## Worked Example

### Scenario
> "Biotech ETF inflows have historically preceded small-cap biotech outperformance by 2-3 weeks. How should this relationship be treated?"

### Strong Answer (Score: 11/12, Pass)

**Classification (3/3):** "This is a coincidental but exploitable relationship. The correlation is statistical, not causal — ETF flows reflect sentiment and liquidity, not fundamental value. The predictive power exists but has no durable mechanism."

**Fragility (3/3):** "This relationship is fragile to: (1) changes in ETF market structure (new products, redemption patterns), (2) crowding if the signal becomes known, (3) regime shifts where sentiment decouples from flows (e.g., forced selling). It notably weakened in 2020-2021 when retail participation changed flow dynamics."

**Risk Treatment (3/3):** "Position sizing capped at 50bps of NAV. 2-week expiration — if the move doesn't materialize, exit. Do not embed in any fundamental valuation. Hedge with sector put spreads if sizing exceeds 25bps."

**Critical Error (Pass):** Did not treat as structural alpha.

---

### Failing Answer (Score: 6/12, Fail)

**Classification (2/3):** "This is a leading indicator for small-cap biotech performance."

**Fragility (2/3):** "It might not work in all environments."

**Risk Treatment (2/3):** "Consider position sizing appropriately."

**Critical Error (Fail):** "This signal can be incorporated into our structural view on small-cap biotech, supporting higher target prices for names with ETF inclusion."

*This answer commits the critical error: it embeds a coincidental statistical relationship into fundamental valuation, converting correlation into conviction.*

---

## Calibration Notes

### Common Grading Mistakes

1. **Rewarding verbosity** — Long answers are not better answers. Grade on content.
2. **Accepting hedged language as fragility awareness** — "This might not always work" is not fragility analysis.
3. **Confusing risk acknowledgment with risk treatment** — Saying "this is risky" is not the same as specifying controls.
4. **Missing subtle critical errors** — The failing answer above sounds reasonable. That's the point.

### Inter-Rater Reliability

When multiple graders score the same response:
- Axes 1-3: Accept ±1 point variance
- Axis 4: Must agree on Pass/Fail

If graders disagree on Axis 4, escalate to senior review.
