# Module 07: Probabilistic Judgment & Calibration

Tests whether AI models can assign **calibrated probabilities** to uncertain financial outcomes — not just classify relationships, but quantify uncertainty with appropriate confidence.

Inspired by [Prophet Arena](https://prophetarena.co) (Xu et al., UChicago DSI / SIGMA Lab, 2025), which demonstrated that probabilistic forecasting with proper scoring rules is a more robust measure of AI intelligence than static benchmarks.

## Core Idea

Module 06 asks: *"What kind of relationship is this?"*
Module 07 asks: *"What is the probability of this outcome, and how confident should you be?"*

Good probability estimation requires:
1. **Base rate awareness** — anchoring to relevant historical frequencies
2. **Regime adjustment** — updating base rates for current conditions
3. **Uncertainty acknowledgment** — expressing ranges, not false precision
4. **Independent judgment** — not outsourcing estimates to market prices or authority

## What This Module Is NOT

- Not about point-estimate forecasting ("the stock will go to $150")
- Not about technical analysis or pattern recognition
- Not about backtesting strategies
- Not about getting the "right answer" — it's about **calibration** (is your 75% really 75%?)

## Scenarios

| ID | Title | Type | Domain | Key Calibration Test |
|----|-------|------|--------|---------------------|
| 07_01 | FDA PDUFA Outcome Probability | Regime-dependent | Biotech | Base rate adjustment (85% → ~75-80%) for regulatory regime |
| 07_02 | 12-Month Recession Probability | Regime-dependent | Healthcare Services | Yield curve signal with QE distortion, small-N sample |
| 07_03 | Earnings Beat/Miss Probability | Coincidental exploitable | Pharma | Historical beat rate adjustment for patent cliff context |
| 07_04 | Merger Completion Probability | Regime-dependent | MedTech | Antitrust regime shift, market-implied vs independent estimate |
| 07_05 | Fed Rate Cut Probability | Regime-dependent | Biotech | Futures-implied probability critique, cross-ref to 06_05 |

## Calibration Scoring

Each scenario includes a `calibration_axes` section with:

- **`ground_truth_range`**: The defensible probability range given the evidence. Not the "correct" probability (that's unknowable) but the range a well-calibrated analyst should fall within.
- **`uncertainty_acknowledgment`**: Does the model express a range around its estimate?
- **`base_rate_integration`**: Does the model reference and adjust from relevant base rates?

These are scored separately from the standard 4-axis rubric (0-12) using `src/calibration.py`.

## New Failure Modes (Category 5)

| Mode | Definition |
|------|-----------|
| `overconfidence` | Probabilities too near 0% or 100% without justification |
| `false_precision` | "73.2%" without acknowledging estimate uncertainty |
| `base_rate_neglect` | Ignoring relevant historical frequencies |
| `market_price_anchoring` | Deferring to market-implied probabilities without adjustment |

## References

- Xu, H. et al. (2025). "Prophet Arena: Benchmarking LLM Forecasting with Dynamic, Anti-Overfitting Evaluation." University of Chicago, Data Science Institute / SIGMA Lab. https://prophetarena.co
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.
- Tetlock, P. & Gardner, D. (2015). *Superforecasting*. Crown.
