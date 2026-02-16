```markdown
# Judgment Under Uncertainty — PM‑Oriented Explanation (Repo‑Specific)

This repo is a **judgment evaluation framework** for healthcare investing: it tests whether an AI (or junior analyst) can separate alpha from environment, recognize fragility, and manage risk ex‑ante rather than producing smart‑sounding but dangerous narratives.

---

## What this repo actually gives you

At a concrete level, you get three main artifact types:

- **Scenarios** (YAML files under `evals/`)  
  Each scenario encodes a specific healthcare investing situation: the observed relationship (e.g., “ETF flows vs. stock returns”), context, and the analysis task you’d give an analyst or model.

- **Grading rubrics** (described in `docs/grading_rubric.md`)  
  A universal 4‑axis scoring system (0–3 points per axis, 0–12 total) that tells you how to grade a response:
  - Classification Accuracy
  - Fragility Awareness
  - Risk Treatment & Actionability
  - Critical Error Avoidance

- **Anchor answers**  
  For each scenario, there are anchor answers at different quality levels (strong / acceptable / failing), including adversarial variants that sound intelligent but violate core principles.

There is also an **adversarial** module (`adversarial/`) that documents how “confidently wrong” answers are constructed for preference learning and red‑teaming.

---

## Repository layout in PM terms

```text
judgment-under-uncertainty-eval/
├── README.md
├── docs/
│   ├── grading_rubric.md      # 4-axis scoring system
│   ├── eval_card_template.md  # Standard scenario format
│   └── failure_modes.md       # Taxonomy of critical errors
├── evals/
│   ├── 01_equity_thesis/
│   ├── 02_dcf_valuation/
│   ├── 03_portfolio_construction/
│   ├── 04_earnings_analysis/
│   ├── 05_risk_attribution/
│   └── 06_spurious_correlation_and_fragility/
└── adversarial/
    └── README.md              # Adversarial variants for preference learning
```

- `docs/grading_rubric.md`  
  Defines the 4 scoring axes and how to assign 0–3 for each, with examples.

- `docs/failure_modes.md`  
  Catalog of critical error types (e.g., misclassifying environment as alpha, ignoring fragility) that you want an AI to avoid.

- `evals/` subfolders  
  Each module (equity thesis, DCF, portfolio construction, earnings, risk attribution, spurious correlation) contains:
  - Healthcare‑specific scenarios.
  - Rubric references.
  - Anchor answers at multiple quality levels.
  - Adversarial variants.

---

## Healthcare‑specific focus

All scenarios are written for **healthcare** but target judgment rather than industry trivia. Sub‑sectors covered include:

- **Biotech** (clinical‑stage, small/large‑cap): binary outcomes, skew, reflexivity.
- **Pharma**: pipeline optionality, patent cliffs, pricing and policy risk.
- **MedTech**: procedure volumes, hospital CapEx cycles.
- **Life Sciences Tools**: R&D spend correlation, cyclicality vs structural.
- **Diagnostics**: reimbursement regimes and payer behavior.
- **Healthcare Services**: policy exposure, labor economics, utilization cycles.

These are chosen because they naturally combine binary outcomes, regime shifts, regulation, and skew—conditions where LLMs often hallucinate competence or convert correlation into conviction.

---

## The grading system: the four axes

Every answer is graded 0–3 on four axes (total 12):

### 1. Classification Accuracy

Did the answer correctly classify the observed relationship as:

- **Structural**  
  Durable, mechanism‑based (e.g., a reimbursement rule directly driving unit economics).

- **Regime‑dependent**  
  Valid only under specific macro/policy conditions (e.g., low‑rate environment, specific policy regime).

- **Coincidental but exploitable**  
  Predictive but non‑causal; something you can trade with controls, not call “alpha.”

- **Non‑actionable noise**  
  Relationship not reliably predictive or too unstable to act on.

### 2. Fragility Awareness

Does the answer show awareness of:

- Why the relationship might break.
- What conditions keep it alive (policy, liquidity, behavior).
- Historical precedents where similar patterns failed.

### 3. Risk Treatment & Actionability

Beyond labeling the relationship, does the answer specify:

- Position sizing constraints (e.g., cap risk, starter size only).
- Hedging requirements (what to hedge and how).
- Time decay / expiration (don’t embed it in terminal value).
- Explicit exclusion from structural models or long‑term forecasts.

### 4. Critical Error Avoidance (binary gate)

The key failure this framework hunts:

> Misclassifying environmental or spurious correlation as durable alpha.

If an answer crosses this line—e.g., treats a policy‑driven uplift as permanent stock‑specific skill and embeds it into terminal value—it **fails**, even if other aspects are polished.

---

## Example: how a scenario works

Take a scenario in the active module `06_spurious_correlation_and_fragility`, such as `06_01_etf_flow_correlation.yaml`:

- **Observed relationship**  
  For instance, “ETF healthcare flows appear tightly correlated with a specific basket of mid‑cap biotech names.”

- **Context**  
  Details on flows, time period, macro backdrop, how many names are involved, and what’s known about ownership.

- **Task**  
  Ask the model to:
  - Classify the relationship (structural vs regime‑dependent vs exploitable vs noise).
  - Discuss fragility.
  - Propose a concrete risk management approach if trading it at all.

- **Anchor answers**  
  In the same module:
  - A strong answer that classifies it as regime‑dependent or exploitable, lays out fragility (e.g., passive flows, policy changes, liquidity), and proposes tight sizing and hedging.
  - A failing, adversarial answer that calls it structural alpha and bakes it into long‑term valuation or “safe” sizing.

You run a model (or analyst) on this scenario and score them using the rubric.

---

## Conceptual foundations translated into behavior

The framework operationalizes ideas like:

- **Prediction vs causality**  
  A relationship can be predictive today but not durable; trade it as fragile, don’t build your terminal value or sizing around it.

- **Survival‑first risk management**  
  Separate idiosyncratic edge from environment, and size risk intentionally rather than because a backtest looks good.

Crucially, the repo tests whether a model behaves accordingly in concrete cases, rather than just repeating these ideas in abstract prose.

---

## How to run the code

The repo includes Python tooling (under `src/`) to automate evaluations:

### Install

```bash
git clone https://github.com/[username]/judgment-under-uncertainty-eval.git
cd judgment-under-uncertainty-eval
pip install -e ".[all]"

# Optional: configure LLM API keys
cp .env.example .env
# Edit .env with your OpenAI/Anthropic keys
```

### Run evaluations

Run a single scenario with a specific model:

```bash
python -m src.run_eval \
  --scenario evals/06_spurious_correlation_and_fragility/scenarios/06_01_etf_flow_correlation.yaml \
  --model gpt-4-turbo
```

Run all scenarios in a module:

```bash
python -m src.run_eval \
  --module 06_spurious_correlation_and_fragility \
  --model claude-3-opus-20240229 \
  --adversarial  # include adversarial variants
```

### Grade and extract preference data

Interactive grading of responses:

```bash
python -m src.grade outputs/06_01_etf_flow_correlation_gpt-4-turbo_*.json
```

Generate RLHF preference pairs (chosen vs rejected):

```bash
python -m src.extract_pairs --output preference_pairs.jsonl
```

---

## Manual use (no code)

You can use the repo even without running Python:

1. Open a scenario YAML (e.g., `evals/06_spurious_correlation_and_fragility/scenarios/06_01_etf_flow_correlation.yaml`).
2. Copy `observed_relationship` + `context` + `task` into any LLM (or give to an analyst).
3. Grade the answer using `docs/grading_rubric.md`.
4. Compare it to the anchor answers defined for that scenario.

This makes it a practical tool for model comparison or analyst training.

---

## Modules and current status

The modules are:

| Module | Focus                                        | Status   |
|--------|----------------------------------------------|----------|
| 01     | Equity Thesis: thesis & variant perception   | Planned  |
| 02     | DCF Valuation: assumptions & terminal traps  | Planned  |
| 03     | Portfolio Construction: sizing, correlation  | Planned  |
| 04     | Earnings Analysis: noise vs signal           | Planned  |
| 05     | Risk Attribution: factor vs idiosyncratic    | Planned  |
| 06     | Spurious Correlation & Fragility             | Active   |

The **active** module (06) already contains fully‑fleshed healthcare scenarios, rubrics, anchor answers, and adversarial variants; the others define the evaluation skeleton and can be populated with additional content.

---

## How you might use this as a PM

Some concrete patterns:

- **Model selection and tuning**  
  Run several LLMs on the same healthcare scenarios to see which ones avoid “confidently dying” and treat fragility appropriately.

- **RLHF / preference learning**  
  Use the anchor + adversarial answers and extracted pairs to train reward models that prefer survivable reasoning over slick narratives.

- **Red‑teaming**  
  Use `--adversarial` runs to see how easily a model can be coaxed into misclassifying environment as alpha.

- **Analyst calibration**  
  Give the same scenarios to human analysts, grade them on the 4 axes, and compare their judgment to your own and to the AI.

In short, this repo is the scaffolding for turning your tacit judgment about **what keeps you alive in healthcare investing** into explicit, machine‑gradable tests for both AI and humans.
```
