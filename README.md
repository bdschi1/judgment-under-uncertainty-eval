# Judgment Under Uncertainty Eval

[![CI](https://github.com/bdschi1/judgment-under-uncertainty-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/bdschi1/judgment-under-uncertainty-eval/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-145%20passed-brightgreen)

Domain-expert evaluation framework for testing whether AI models can separate alpha from environmental exposure, manage risk ex-ante, and avoid seductive but dangerous reasoning patterns — focused on healthcare investing.

> The failure mode we care about most: **confidently dying** — producing answers that sound intelligent, tell coherent stories, and quietly convert correlation into conviction.

---

## How It Works

Each evaluation follows the same flow:

```
Scenario YAML (observed relationship + context + task)
       |
       v
  Model Response
  (via API or manual paste)
       |
       v
  4-Axis Grading (0-3 each, 12 total)
       |
       +-------+-------+
       v               v
  Anchor Comparison    Adversarial Variants
  (strong/acceptable/  (recency injection,
   failing examples)    authority anchoring)
       |
       v
  RLHF Pair Extraction
  (chosen/rejected for preference learning)
```

---

## Grading System

Every response is scored on **4 axes (0-3 each, 12 total)**:

| Axis | What It Tests |
|------|---------------|
| **Classification Accuracy** | Correctly classifies the relationship: structural, regime-dependent, coincidental-but-exploitable, or noise |
| **Fragility Awareness** | Identifies why the relationship might break, what sustains it, and historical precedents for breakdown |
| **Risk Treatment** | Specifies concrete controls: position sizing, hedging, time decay, exclusion from terminal value models |
| **Critical Error Avoidance** | Binary gate — misclassifying environmental or spurious correlation as durable alpha is an automatic fail |

Full rubric: `docs/grading_rubric.md`

---

## Modules

| Module | Focus | Scenarios | Status |
|--------|-------|-----------|--------|
| 01 — Equity Thesis | Thesis construction, variant perception | — | Planned |
| 02 — DCF Valuation | Assumption quality, terminal value traps | — | Planned |
| 03 — Portfolio Construction | Sizing, correlation, regime awareness | — | Planned |
| 04 — Earnings Analysis | Noise vs signal, management credibility | — | Planned |
| 05 — Risk Attribution | Factor exposure, drawdown analysis | — | Planned |
| 06 — Spurious Correlation & Fragility | Predictive vs causal, fragility management | 5 | **Active** |
| 07 — Probabilistic Judgment & Calibration | Calibrated probability estimates, proper scoring | 5 | **Active** |

### Active Scenarios (Module 06)

| Scenario | Setup |
|----------|-------|
| 06_01 — ETF Flow Correlation | Passive flow mechanics vs fundamental signal |
| 06_02 — GLP-1 MedTech Correlation | Obesity drug thesis bleeding into device volumes |
| 06_03 — Low-Vol Healthcare Services | Realized vol collapse masking policy tail risk |
| 06_04 — Pharma R&D Tools | R&D spending correlation vs pipeline optionality |
| 06_05 — Small-Cap Biotech Rates | Rate sensitivity in pre-revenue biotech |

### Active Scenarios (Module 07)

| Scenario | Setup |
|----------|-------|
| 07_01 — FDA PDUFA Outcome | Binary approval probability with base rate adjustment for regulatory regime shift |
| 07_02 — Recession Probability | Yield curve signal calibration with small-N awareness and QE distortion |
| 07_03 — Earnings Beat/Miss | Historical beat rate adjustment for patent cliff structural break |
| 07_04 — Merger Completion | Antitrust regime shift, market-implied vs independent probability estimate |
| 07_05 — Fed Rate Cut | Futures-implied probability critique, risk premia adjustment |

---

## Healthcare Domain

All scenarios are healthcare-specific — a domain that naturally embeds binary outcomes, reflexivity, regulation, skew, and regime shifts:

| Sub-Sector | Why It Matters |
|------------|----------------|
| Biotech (clinical-stage) | Binary outcomes, skew, reflexivity |
| Pharma | Pipeline optionality, patent cliffs, pricing risk |
| MedTech | Procedure volumes, hospital CapEx cycles |
| Life Sciences Tools | R&D spending correlation, cyclicality |
| Diagnostics | Reimbursement regime dependence |
| Healthcare Services | Policy exposure, labor economics |

---

## Failure Modes

The scenarios are designed to surface specific AI failure patterns:

- **Alpha/Environment Confusion** — Treating sector beta as stock-specific alpha
- **False Certainty** — Unhedged risks embedded in base case
- **Backward-Looking Risk** — Using trailing vol when forward risk dominates
- **Narrative Attribution** — Declaring failure without factor decomposition
- **Correlation-as-Causation** — Converting observed correlation into structural thesis
- **Overconfidence** — Probabilities too near 0%/100% without justification
- **False Precision** — "73.2%" without acknowledging estimate uncertainty
- **Base Rate Neglect** — Ignoring relevant historical frequencies
- **Market Price Anchoring** — Deferring to market-implied probabilities without adjustment

Full taxonomy (20 modes across 5 categories): `docs/failure_modes.md`

---

## Key Features

- **Expert-designed scenarios** — Each scenario is written from institutional healthcare PM experience, not scraped or generated
- **4-axis universal grading** — Same scoring system across all modules, anchored with strong/acceptable/failing examples
- **Adversarial variants** — Each scenario includes variants that target specific failure modes (recency injection, authority anchoring, false precision)
- **RLHF-ready** — Extract chosen/rejected preference pairs directly from graded responses
- **Manual or automated** — Run scenarios through API (GPT-4, Claude) or copy-paste into any model and grade by hand
- **Conceptual foundations** — Evaluation philosophy operationalized from López de Prado (prediction usefulness ≠ causal permanence), Paleologo (survival-first risk management), and Prophet Arena (calibrated probabilistic forecasting as intelligence measure)

---

## Setup

```bash
git clone https://github.com/bdschi1/judgment-under-uncertainty-eval.git
cd judgment-under-uncertainty-eval
pip install -e "."
```

Optional dependencies:

```bash
pip install -e ".[api]"        # OpenAI + Anthropic for automated evals
pip install -e ".[analysis]"   # pandas, numpy, matplotlib, seaborn
pip install -e ".[dev]"        # pytest, black, ruff, mypy
pip install -e ".[all]"        # Everything
```

For automated evaluation, set API keys in `.env`:

```bash
cp .env.example .env
# Add OPENAI_API_KEY and/or ANTHROPIC_API_KEY
```

## Run

### Automated evaluation

```bash
# Single scenario against GPT-4
python -m src.run_eval \
  --scenario evals/06_spurious_correlation_and_fragility/scenarios/06_01_etf_flow_correlation.yaml \
  --model gpt-4-turbo

# All scenarios in a module against Claude (with adversarial variants)
python -m src.run_eval \
  --module 06_spurious_correlation_and_fragility \
  --model claude-3-opus-20240229 \
  --adversarial
```

### Interactive grading

```bash
python -m src.grade outputs/06_01_etf_flow_correlation_gpt-4-turbo_*.json
```

### Extract RLHF preference pairs

```bash
python -m src.extract_pairs --output preference_pairs.jsonl
```

### Manual evaluation (no code)

1. Open any scenario YAML
2. Copy `observed_relationship` + `context` + `task` as a prompt
3. Paste into any model
4. Grade using `docs/grading_rubric.md`
5. Compare to anchor answers in the YAML

---

## Project Structure

```
judgment-under-uncertainty-eval/
├── evals/
│   ├── 01_equity_thesis/                    Planned
│   ├── 02_dcf_valuation/                    Planned
│   ├── 03_portfolio_construction/           Planned
│   ├── 04_earnings_analysis/                Planned
│   ├── 05_risk_attribution/                 Planned
│   ├── 06_spurious_correlation_and_fragility/
│   │   ├── README.md                        Module overview
│   │   └── scenarios/                       5 YAML scenario files
│   └── 07_probabilistic_judgment_and_calibration/
│       ├── README.md                        Module overview + Prophet Arena citation
│       └── scenarios/                       5 YAML scenario files
├── adversarial/
│   └── README.md                            Red-teaming & preference learning guide
├── docs/
│   ├── grading_rubric.md                    Universal 4-axis scoring system
│   ├── eval_card_template.md                Standardized scenario format
│   ├── failure_modes.md                     Taxonomy of critical errors
│   └── usage.md                             Detailed usage documentation
├── src/
│   ├── run_eval.py                          CLI evaluation runner (OpenAI/Anthropic)
│   ├── grade.py                             Interactive grading tool
│   ├── extract_pairs.py                     RLHF preference pair extraction
│   └── calibration.py                       Calibration scoring (Brier, log loss, ECE)
├── tests/
│   ├── test_scenarios.py                    Scenario validation tests
│   └── test_calibration.py                  Calibration scoring tests
├── fundamental.md                           PM-oriented explanation
├── CONTRIBUTING.md
├── CHANGELOG.md
└── pyproject.toml
```

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=src
black .
ruff check .
mypy src/
```

---

## Stack

- **Scenarios**: [PyYAML](https://pyyaml.org) + [Pydantic](https://docs.pydantic.dev)
- **Evaluation**: [OpenAI](https://platform.openai.com) + [Anthropic](https://docs.anthropic.com) (optional, for automated runs)
- **Analysis**: [pandas](https://pandas.pydata.org) + [matplotlib](https://matplotlib.org) + [seaborn](https://seaborn.pydata.org) (optional)

## References

- Xu, H. et al. (2025). "Prophet Arena: Benchmarking LLM Forecasting with Dynamic, Anti-Overfitting Evaluation." University of Chicago, Data Science Institute / SIGMA Lab. [prophetarena.co](https://prophetarena.co)
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.
- Tetlock, P. & Gardner, D. (2015). *Superforecasting*. Crown.
- Paleologo, G. (2021). *Advanced Portfolio Management*. Wiley.

## License

MIT

---

![Python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-191919?style=flat&logo=anthropic&logoColor=white)
