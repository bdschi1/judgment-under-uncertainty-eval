# Module 03: Portfolio Construction

## Status: Planned

## Core Idea

This module evaluates whether an AI can construct and critique portfolio decisions that:

- Separate position sizing from thesis conviction
- Recognize unintended factor exposures
- Size to survive, not just to maximize expected return
- Manage correlation and concentration appropriately

## Key Concepts to Test

### Portfolio Judgment Dimensions

| Dimension | What It Tests |
|-----------|---------------|
| Sizing discipline | Does position size match uncertainty level? |
| Factor awareness | Are unintended exposures identified? |
| Correlation awareness | Are concentration risks recognized? |
| Regime conditioning | Are positions appropriate for multiple states? |

### Healthcare-Specific Portfolio Challenges

- **Biotech event sizing**: Binary outcomes require special treatment
- **Sector correlation**: Healthcare names move together in stress
- **Factor exposure**: Low-vol, quality, growth tilts in healthcare
- **Policy concentration**: Reimbursement regime affects many names
- **Pipeline correlation**: Therapeutic area concentration

## Planned Scenarios

1. **Event sizing** — Position size for binary biotech catalyst
2. **Factor exposure** — Unintended sector factor tilts
3. **Correlation stress** — Healthcare names in risk-off
4. **Concentration risk** — Therapeutic area or policy exposure
5. **Regime-conditional sizing** — Position sizes across environments

## Common Failure Modes

- `sizing_mismatch`: Position size inconsistent with conviction level
- `factor_blindness`: Unrecognized factor exposure treated as alpha
- `correlation_blindness`: Concentrated risk not identified
- `regime_blindness`: Position inappropriate for possible states

## Grading Approach

Uses universal rubric adapted for portfolio construction:

1. **Sizing appropriateness**: Does size match conviction and uncertainty?
2. **Exposure identification**: Are unintended risks named?
3. **Stress consideration**: Are adverse scenarios considered?
4. **Critical error**: Sizing for expected case without survival constraint

---

*This module is in planning. Scenarios will be developed following the eval card template.*
