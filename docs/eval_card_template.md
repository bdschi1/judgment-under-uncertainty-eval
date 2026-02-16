# Eval Card Template

This template standardizes how scenarios are documented across all modules. Each scenario becomes a self-contained "eval card" that can be:

- Run independently in eval frameworks
- Used for RLHF preference ranking
- Extended with new anchor answers over time

---

## Template Structure

```yaml
id: [MODULE]_[NUMBER]_[SHORT_NAME]
module: [Module name]
version: 1.0
last_updated: [YYYY-MM-DD]

# --- SCENARIO ---
title: [Descriptive title]
domain: [Healthcare sub-sector]
relationship_type: [structural | regime_dependent | coincidental_exploitable | noise]

observed_relationship: |
  [Clear statement of the correlation/pattern being evaluated]

context: |
  [Any additional context needed to understand the scenario.
   Market conditions, time period, relevant background.]

# --- TASK ---
task: |
  [What the model is asked to do. Usually:
   1. Classify the relationship
   2. Identify fragility factors
   3. Specify risk treatment]

# --- GRADING ---
grading_axes:
  classification:
    weight: 3
    correct_answer: [relationship_type]
    notes: |
      [Grading notes specific to this scenario]

  fragility:
    weight: 3
    key_factors:
      - [Factor 1]
      - [Factor 2]
      - [Factor 3]
    notes: |
      [What fragility analysis should include]

  risk_treatment:
    weight: 3
    valid_treatments:
      - [Treatment 1]
      - [Treatment 2]
    invalid_treatments:
      - [Treatment that would be wrong]
    notes: |
      [Treatment-specific guidance]

  critical_error:
    failure_condition: |
      [Specific description of what would constitute a critical error]

# --- ANCHOR ANSWERS ---
anchor_answers:
  strong:
    score: [9-12]
    response: |
      [Full example of a strong response]
    notes: |
      [Why this is strong]

  acceptable:
    score: [6-8]
    response: |
      [Full example of an acceptable response]
    notes: |
      [What's missing or weak]

  failing:
    score: [0-6]
    response: |
      [Full example of a failing response - should sound intelligent]
    notes: |
      [Why this fails, what critical error it commits]

# --- ADVERSARIAL VARIANTS ---
adversarial_variants:
  - variant_id: [ID]_ADV_01
    manipulation: |
      [How the scenario is modified to induce failure]
    expected_failure_mode: |
      [What error the model is likely to make]

  - variant_id: [ID]_ADV_02
    manipulation: |
      [Another variant]
    expected_failure_mode: |
      [Expected error]

# --- METADATA ---
metadata:
  difficulty: [easy | medium | hard | expert]
  estimated_time: [seconds for human expert]
  related_scenarios: [list of related eval card IDs]
  failure_modes: [list from failure_modes.md]
  tags: [list of tags for filtering]
```

---

## Field Definitions

### Core Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier: `{module}_{number}_{short_name}` |
| `module` | Yes | Parent module name |
| `relationship_type` | Yes | Ground truth classification |
| `observed_relationship` | Yes | The pattern/correlation being evaluated |
| `task` | Yes | What the model must do |

### Grading Fields

| Field | Required | Description |
|-------|----------|-------------|
| `correct_answer` | Yes | Ground truth for classification axis |
| `key_factors` | Yes | Required fragility factors (model should identify 2+ of these) |
| `valid_treatments` | Yes | Acceptable risk management approaches |
| `invalid_treatments` | Recommended | Treatments that would be errors |
| `failure_condition` | Yes | What constitutes a critical error |

### Anchor Answer Fields

| Field | Required | Description |
|-------|----------|-------------|
| `strong` | Yes | Full response scoring 9-12 |
| `acceptable` | Yes | Full response scoring 6-8 |
| `failing` | Yes | Full response that sounds good but fails |

**Important:** Failing answers must be sophisticated. They should sound like what a confident but wrong model would produce. Generic bad answers are not useful for preference learning.

### Adversarial Variants

| Field | Required | Description |
|-------|----------|-------------|
| `variant_id` | Yes | Unique ID for the variant |
| `manipulation` | Yes | How the scenario is modified |
| `expected_failure_mode` | Yes | What error this should induce |

---

## Example: Completed Eval Card

```yaml
id: 06_01_etf_flow_correlation
module: 06_spurious_correlation_and_fragility
version: 1.0
last_updated: 2024-01-15

title: Biotech ETF Flows and Small-Cap Outperformance
domain: Biotech
relationship_type: coincidental_exploitable

observed_relationship: |
  Biotech ETF (XBI, IBB) net inflows have historically preceded
  small-cap biotech outperformance vs. large-cap biotech by 2-3 weeks,
  with a hit rate of approximately 65% over the past 5 years.

context: |
  This pattern has been documented in sell-side research and is
  increasingly discussed in biotech investor circles. The mechanism
  is unclear but may relate to sentiment, liquidity, or momentum effects.

task: |
  1. Classify this relationship (structural, regime-dependent,
     coincidental but exploitable, or non-actionable noise)
  2. Identify factors that could cause this relationship to break down
  3. Specify how this relationship should be treated in portfolio management

grading_axes:
  classification:
    weight: 3
    correct_answer: coincidental_exploitable
    notes: |
      This is a statistical relationship without clear causal mechanism.
      It has predictive power but should not be treated as structural.
      Regime-dependent is a partial credit answer.

  fragility:
    weight: 3
    key_factors:
      - ETF market structure changes (new products, AUM shifts)
      - Signal crowding as pattern becomes known
      - Regime shifts (risk-off environments, sector rotation)
      - Changes in retail vs. institutional flow composition
      - Correlation breakdown during high-volatility periods
    notes: |
      Strong answers identify 3+ factors with specificity.
      Vague acknowledgment of uncertainty is not sufficient.

  risk_treatment:
    weight: 3
    valid_treatments:
      - Position sizing cap (e.g., max 50bps NAV)
      - Time-bound exposure (2-3 week expiration)
      - Exclusion from fundamental valuation
      - Hedge with sector options if sizing material
      - Monitoring triggers for signal degradation
    invalid_treatments:
      - Embedding in DCF or target price
      - Using as basis for structural sector overweight
      - Sizing based on historical hit rate without decay
    notes: |
      Treatments must match the coincidental nature of the signal.

  critical_error:
    failure_condition: |
      Treating this correlation as structural alpha, embedding it in
      fundamental valuation, or using it to justify conviction-level
      positions without time bounds or decay assumptions.

anchor_answers:
  strong:
    score: 11
    response: |
      Classification: This is a coincidental but exploitable relationship.
      The correlation is statistical — ETF flows reflect sentiment and
      liquidity dynamics, not fundamental value creation. There is no
      causal mechanism by which ETF inflows make small-cap biotechs
      more valuable; the predictive power likely stems from momentum
      and sentiment transmission.

      Fragility factors: (1) ETF market structure is not static — new
      products, changing AUM, and shifts in creation/redemption patterns
      could alter flow dynamics. (2) If this signal is increasingly known
      (as the scenario suggests), crowding will degrade it. (3) The
      relationship likely weakens or inverts in risk-off regimes where
      flows become forced rather than sentiment-driven. (4) The 65% hit
      rate over 5 years is a small sample with likely significant
      variation across sub-periods.

      Risk treatment: (1) Cap position sizing at 50bps of NAV maximum.
      (2) Treat as a 2-3 week tactical signal with hard expiration —
      if the anticipated outperformance doesn't materialize, exit
      regardless of thesis. (3) Explicitly exclude from any fundamental
      valuation or DCF work. (4) If sizing exceeds 25bps, hedge with
      XBI put spreads to isolate the relative bet. (5) Track hit rate
      on a rolling 12-month basis; suspend use if hit rate falls below 55%.
    notes: |
      Correct classification with reasoning. Multiple specific fragility
      factors. Concrete, appropriate risk treatments. No critical error.

  acceptable:
    score: 7
    response: |
      This appears to be a momentum or sentiment-driven correlation
      rather than a fundamental relationship. ETF flows might predict
      short-term performance but shouldn't be confused with alpha.

      The relationship could break if market conditions change or if
      too many people start trading on it. It's also possible the
      historical pattern is partially spurious.

      I would treat this as a short-term tactical signal with limited
      sizing. It shouldn't influence fundamental views on individual
      companies.
    notes: |
      Correct intuition on classification. Fragility acknowledged but
      vague. Risk treatment directionally correct but lacks specifics
      (what is "limited sizing"?). No critical error.

  failing:
    score: 5
    response: |
      This is a valuable leading indicator for small-cap biotech
      performance. The 65% hit rate over 5 years suggests a robust
      relationship that can inform portfolio positioning.

      The mechanism likely relates to institutional capital flows
      signaling informed views on the sector. When sophisticated
      investors increase biotech exposure through ETFs, it often
      precedes positive developments for smaller, less-followed names.

      This signal supports a structural overweight to small-cap biotech
      in the current environment. It can be incorporated into target
      prices for small-cap names with high ETF overlap, as the flow
      dynamics provide a tailwind to valuations.
    notes: |
      Sounds sophisticated but commits critical error. Invents a causal
      mechanism ("informed views") without evidence. Embeds a statistical
      correlation into fundamental valuation. Treats 65%/5yr as "robust"
      when it's a weak, small-sample signal. This is exactly the kind
      of confident, wrong answer we're testing for.

adversarial_variants:
  - variant_id: 06_01_ADV_01
    manipulation: |
      Add context suggesting the pattern has "worked" recently:
      "In the past 6 months, this signal has been 5/6 correct."
    expected_failure_mode: |
      Recency bias leading to overconfidence. Model may upgrade
      classification to "structural" based on recent performance.

  - variant_id: 06_01_ADV_02
    manipulation: |
      Add a plausible-sounding mechanism:
      "Some researchers suggest this reflects smart money positioning
      ahead of clinical catalysts concentrated in small-cap biotech."
    expected_failure_mode: |
      Mechanism fabrication. Model may accept the suggested mechanism
      and reclassify as structural or regime-dependent.

metadata:
  difficulty: medium
  estimated_time: 180
  related_scenarios:
    - 06_02_glp1_medtech_correlation
    - 03_05_factor_exposure_sizing
  failure_modes:
    - mechanism_fabrication
    - recency_bias
    - sample_size_blindness
  tags:
    - biotech
    - etf
    - flows
    - momentum
    - correlation
```

---

## Implementation Notes

### For Eval Runners

The YAML format is designed to be parsed programmatically. Key fields for automation:

- `task` → prompt to model
- `grading_axes.*.correct_answer` → ground truth
- `anchor_answers.*.response` → few-shot examples or preference pairs

### For RLHF

Use `anchor_answers.strong.response` and `anchor_answers.failing.response` as preference pairs. The failing answer is intentionally sophisticated to create meaningful training signal.

### For Red-Teaming

Use `adversarial_variants` to systematically probe model weaknesses. Track which manipulations most reliably induce failures.
