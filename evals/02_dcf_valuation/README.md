# Module 02: DCF Valuation Judgment

## Status: Planned

## Core Idea

This module evaluates whether an AI can construct and critique DCF valuations that:

- Separate knowable from unknowable assumptions
- Avoid embedding regime-dependent relationships in terminal value
- Recognize when precision is false precision
- Appropriately discount speculative components

## Key Concepts to Test

### Valuation Judgment Dimensions

| Dimension | What It Tests |
|-----------|---------------|
| Assumption quality | Are inputs defensible or fabricated? |
| Terminal value discipline | Is TV appropriately constrained? |
| Uncertainty acknowledgment | Are ranges provided where appropriate? |
| Sensitivity awareness | Are key drivers identified? |

### Healthcare-Specific Valuation Challenges

- **Biotech rNPV**: Probability-adjusting pipeline value
- **Patent cliff modeling**: Revenue decay assumptions
- **Reimbursement risk**: Policy scenarios in DCF
- **M&A optionality**: Value of strategic alternatives
- **Growth normalization**: Distinguishing cyclical vs. secular

## Planned Scenarios

1. **Terminal value anchor** — Appropriate TV multiple for healthcare services
2. **Biotech rNPV** — Pipeline probability and peak sales estimation
3. **Patent cliff modeling** — Generic entry assumptions
4. **Margin expansion thesis** — Sustainability of operating leverage
5. **Growth normalization** — COVID-era data in projections

## Common Failure Modes

- `valuation_contamination`: Non-structural factors in terminal value
- `false_precision`: 2-decimal output from 1-significant-figure inputs
- `terminal_value_dominance`: TV is entire thesis
- `assumption_fabrication`: Making up inputs without basis

## Grading Approach

Uses universal rubric adapted for valuation:

1. **Assumption quality**: Are inputs defensible?
2. **Uncertainty acknowledgment**: Is appropriate humility shown?
3. **Sensitivity identification**: Are key drivers flagged?
4. **Critical error**: Fabricated precision or contaminated TV

---

*This module is in planning. Scenarios will be developed following the eval card template.*
