# Module 05: Risk Attribution

## Status: Planned

## Core Idea

This module evaluates whether an AI can analyze portfolio returns and risks that:

- Correctly attribute performance to sources (alpha vs. factor vs. luck)
- Identify drawdown drivers accurately
- Separate idiosyncratic from systematic exposure
- Avoid hindsight bias in attribution

## Key Concepts to Test

### Risk Attribution Dimensions

| Dimension | What It Tests |
|-----------|---------------|
| Source identification | What drove the return? |
| Factor decomposition | Alpha vs. beta vs. factor |
| Drawdown analysis | What caused the loss? |
| Prospective application | What does this mean going forward? |

### Healthcare-Specific Attribution Challenges

- **Biotech volatility** — Stock-specific vs. sector vs. market
- **Policy risk** — Reimbursement events affecting multiple names
- **Factor exposure** — Healthcare quality/growth/low-vol tilts
- **Event clustering** — Clinical readouts coinciding with market stress
- **Correlation shifts** — Healthcare defensiveness in different regimes

## Planned Scenarios

1. **Alpha vs. factor** — Was outperformance skill or exposure?
2. **Drawdown attribution** — What caused the loss?
3. **Policy event** — Attributing cross-name moves to common factor
4. **Correlation analysis** — Changing healthcare beta
5. **Hindsight test** — Was the ex-post obvious ex-ante?

## Common Failure Modes

- `alpha_attribution`: Crediting skill for factor exposure
- `hindsight_bias`: "Should have seen it" after the fact
- `correlation_blindness`: Missing common driver across positions
- `sample_size_blindness`: Drawing conclusions from short periods

## Grading Approach

Uses universal rubric adapted for risk attribution:

1. **Source accuracy**: Are drivers correctly identified?
2. **Factor awareness**: Is factor vs. alpha distinguished?
3. **Prospective framing**: Is forward-looking implication clear?
4. **Critical error**: Attributing factor return to stock-picking skill

---

*This module is in planning. Scenarios will be developed following the eval card template.*
