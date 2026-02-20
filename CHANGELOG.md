# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Module 07: Probabilistic Judgment & Calibration
- 5 scenarios testing calibrated probability estimation for financial events:
  - 07_01: FDA PDUFA Binary Outcome Probability
  - 07_02: 12-Month Recession Probability
  - 07_03: Earnings Beat/Miss Probability (Large-Cap Pharma)
  - 07_04: MedTech Merger Completion Probability
  - 07_05: Fed Rate Cut Probability and Biotech Impact
- Each scenario includes calibration_axes with ground_truth_range for automated scoring
- Strong, acceptable, and failing anchor answers with calibration-specific reasoning
- 3 adversarial variants per scenario targeting calibration failure modes

#### Calibration Scoring Module (`src/calibration.py`)
- Brier score, log loss, and Expected Calibration Error (ECE) metrics
- Probability quality scoring (0-3 scale matching existing grading axes)
- Free-text probability extraction from model responses
- Aggregate calibration report generation
- CLI interface for standalone use
- Scoring methodology inspired by Prophet Arena (Xu et al., UChicago DSI / SIGMA Lab, 2025)

#### Failure Mode Taxonomy
- Category 5: Calibration Failures with 4 new modes:
  - `overconfidence` — probabilities too near extremes without justification
  - `false_precision` — exact estimates without uncertainty ranges
  - `base_rate_neglect` — ignoring relevant historical frequencies
  - `market_price_anchoring` — deferring to market-implied probabilities

#### Tests
- `tests/test_calibration.py` — unit tests for all calibration functions
- `TestModule07Scenarios` in `tests/test_scenarios.py` — scenario validation

## [0.1.0] - 2024-01-15

### Added

- Initial repository structure
- Universal grading rubric (4 axes, 0-12 scale, critical error check)
- Eval card template (YAML format)
- Failure mode taxonomy (16 failure modes across 4 categories)

#### Module 06: Spurious Correlation and Fragility
- Complete module with 5 scenarios:
  - 06_01: Biotech ETF Flows and Small-Cap Outperformance
  - 06_02: GLP-1 News and MedTech Multiple Expansion
  - 06_03: Low-Volatility Factor in Healthcare Services
  - 06_04: Pharma R&D Spend and Life Sciences Tools Revenue
  - 06_05: Small-Cap Biotech Performance Following Rate Cuts
- Strong, acceptable, and failing anchor answers for each scenario
- 3-4 adversarial variants per scenario

#### Modules 01-05
- Placeholder READMEs with module concepts and planned scenarios:
  - 01: Equity Thesis Construction
  - 02: DCF Valuation Judgment
  - 03: Portfolio Construction
  - 04: Earnings Analysis
  - 05: Risk Attribution

#### Documentation
- Main README with repo overview and usage guidance
- Adversarial variants documentation for RLHF and red-teaming
- Contributing guidelines
- MIT License

### Notes

This is the initial release focused on Module 06 as a proof of concept. Modules 01-05 are planned for future releases.
