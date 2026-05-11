# AI Report Validation System (Module 9 Homework)

> SYSEN 5381 — Module 9: AI for Text Analysis
> A customized multi-reviewer validation system that performs qualitative content
> analysis on AI-generated earthquake situation reports and compares 3 prompts
> using one-way ANOVA + Tukey HSD.

---

## What this is

A 5-reviewer LLM evaluation panel (each reviewer plays a distinct domain persona)
scores AI-generated earthquake situation reports along 5 customized dimensions.
The system generates 12 reports per prompt across 3 prompts (n=36 reports, 180
reviewer evaluations) and runs a statistical experiment to test whether prompt
design produces significantly different report quality.

Pattern borrowed (and stripped down) from Phase 5 of the carpool_v4 research-agent
at `../acti_multi_agent/research-agent/carpool_v4/src/scoring.py`.

## Headline result

```
Group means (composite, scale 0-10):
  A: Minimal      n=12  mean=6.06  sd=0.40
  B: Structured   n=12  mean=7.13  sd=0.22
  C: Enhanced     n=12  mean=8.66  sd=0.24

One-way ANOVA on composite score:
  F(2, 33) = 229.30      p = 4.4e-20      η² = 0.93   (large effect)

Tukey HSD post-hoc (all three pairwise comparisons reject H0):
  A vs B  Δ=+1.07  p_adj < 1e-3
  A vs C  Δ=+2.60  p_adj < 1e-3
  B vs C  Δ=+1.53  p_adj < 1e-3
```

Per-dimension breakdown reveals where the prompts differ: `completeness_compliance`
(η² = 0.99), `operational_actionability` (0.93), and `calibrated_uncertainty` (0.86)
account for nearly all the separation. `factual_grounding` is **not** significantly
different across prompts (p = 0.15) — an honest finding worth reporting.

## File layout

```
homework_module9_validation/
├── README.md                     <- this file
├── requirements.txt              <- Python dependencies
├── .env.example                  <- required env vars (symlink .env to a real one)
├── run_experiment.sh             <- one-command pipeline
│
├── docs/
│   ├── validation_criteria.md    <- rubric table + LAB-Likert comparison
│   ├── experimental_design.md    <- prompts, sample size, methodology
│   └── statistical_analysis.md   <- hypotheses, results, interpretation
│
├── prompts/
│   ├── _shared_context.txt       <- shared eval preamble (injected into every reviewer)
│   ├── prompt_a_minimal.txt      <- Prompt A (LAB PROMPT_V1)
│   ├── prompt_b_structured.txt   <- Prompt B (LAB PROMPT_V2)
│   ├── prompt_c_enhanced.txt     <- Prompt C (PROMPT_FINAL + persona + anti-hallucination)
│   └── reviewers/
│       ├── factual_grounding.txt
│       ├── operational_actionability.txt
│       ├── communication_clarity.txt
│       ├── calibrated_uncertainty.txt
│       └── completeness_compliance.txt
│
├── src/
│   ├── config.py                 <- constants: models, weights, paths
│   ├── llm_client.py             <- Anthropic SDK wrapper w/ retry + error classification
│   ├── data_variants.py          <- builds seed + 12 reproducible variants
│   ├── report_generator.py       <- LLM call to produce one report
│   ├── reviewer.py               <- single-reviewer + strict-JSON parser (+ repair pass)
│   ├── panel.py                  <- runs all 5 reviewers + weighted composite
│   ├── pipeline.py               <- end-to-end orchestration (resumable)
│   └── statistical_analysis.py   <- ANOVA + Tukey + plots
│
├── data/
│   ├── seed_digest.json          <- synthetic USGS-like digest (n=150 events, 30d)
│   └── variants/                 <- 12 deterministic variants
│
└── outputs/
    ├── generated_reports/        <- 36 markdown reports (12 × 3 prompts)
    ├── reviewer_scores/          <- per-reviewer JSON + AGGREGATE per report
    ├── results/                  <- CSVs + anova_results.json
    └── figures/                  <- 4 PNG plots
```

## Setup

1. **Python environment**: Python 3.9+ with the packages in `requirements.txt`.
   The research-agent virtualenv works out of the box. Otherwise:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **`.env` file**: the project reads `ANTHROPIC_API_KEY` from a `.env` file. The
   default `.env` here is a symlink to the carpool_v4 .env. To use a different
   key, edit `.env.example` and copy it to `.env`.

## Run

### One-command full experiment
```bash
./run_experiment.sh
```

### Step by step
```bash
# Step 1: build 12 data variants (~1 sec)
python3 -m src.data_variants

# Step 2: smoke test (6 reports, ~30 reviewer evals, ~1 min)
python3 -m src.pipeline --smoke

# Step 3: full experiment (36 reports, ~180 reviewer evals, 3-5 min)
python3 -m src.pipeline

# Step 4: statistical analysis + plots
python3 -m src.statistical_analysis
```

The pipeline is **resumable** — re-running skips already-completed (prompt, variant)
pairs. To force a rerun, pass `--no-resume` or delete the relevant files in
`outputs/`.

## Customizing

- **Number of reports per prompt**: edit `N_VARIANTS` in `src/config.py` (default 12).
  Note you can only request up to the number of variant files in `data/variants/`
  (currently 12).
- **Models**: edit `HOMEWORK_GEN_MODEL` / `HOMEWORK_REVIEW_MODEL` in `.env` or
  `src/config.py`. Defaults: `claude-sonnet-4-6` for both.
- **Reviewer weights**: `REVIEW_WEIGHTS` in `src/config.py` (must sum to 1.0).
- **Rubric**: edit any file under `prompts/reviewers/`. Keep the JSON schema stable.

## How the validation system differs from LAB Likert

| Feature | LAB Likert | This system |
|---------|------------|-------------|
| Number of evaluators | 1 (single AI rater) | 5 (per-persona panel) |
| Scale | 1-5 Likert (single rating per dimension) | 0-10 anchored to a 5-item binary checklist + qualitative judgment |
| Score independence | one Likert can mean different things to different raters | concrete pass/fail items reduce rater drift |
| Composite | unweighted mean | weighted (factual 30%, action 20%, clarity 15%, calibration 20%, completeness 15%) |
| Output structure | single number | strict-JSON dict: score + checklist + evidence quotes + criticisms + publish vote |
| Auditability | reader cannot reconstruct the judgment | each false checklist item is justified with a quote from the report |

See `docs/validation_criteria.md` for the full rubric table.

## Screenshots for submission

Each command below produces a screenshot-able terminal session or plot. Copy
them into `outputs/screenshots/` and reference them in your write-up.

1. **System in action** — terminal during the full pipeline run:
   ```bash
   python3 -m src.pipeline 2>&1 | tee outputs/screenshots/01_pipeline_run.log
   ```
   Screenshot: lines 1-25 showing `[X/36] prompt_x/variant_NN composite=X.YY`.

2. **Validation result for one report** — example JSON output:
   ```bash
   cat outputs/reviewer_scores/prompt_c__variant_00_last_7d__factual_grounding.json
   ```

3. **Rubric** — the validation criteria file:
   ```bash
   cat docs/validation_criteria.md
   ```

4. **Statistical analysis output** — the terminal summary:
   ```bash
   python3 -m src.statistical_analysis 2>&1 | tee outputs/screenshots/04_stats.log
   ```

5. **Comparison across prompts** — open these plots:
   - `outputs/figures/boxplot_composite.png`
   - `outputs/figures/heatmap_dimension_x_prompt.png`
   - `outputs/figures/violin_by_dimension.png`
   - `outputs/figures/effect_size_chart.png`
