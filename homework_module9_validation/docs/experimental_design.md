# Experimental Design

## Research question

Do AI-generated earthquake situation reports produced under different writing
prompts differ in measurable quality, as judged by a 5-reviewer LLM panel?

## Independent variable

**Prompt** (categorical, 3 levels):

| ID | Label | Source | Notes |
|----|-------|--------|-------|
| **A** | Minimal | `lab_ai_reporter.py::PROMPT_V1` (verbatim) | "Write a short plain-language summary in 6 bullet points." |
| **B** | Structured | `lab_ai_reporter.py::PROMPT_V2` (verbatim) | Required markdown sections: Executive Summary, Key Observations, Risk Watch, Data Caveat. |
| **C** | Enhanced | `lab_ai_reporter.py::PROMPT_FINAL` + (1) state-coordinator persona + (2) explicit anti-hallucination rules + (3) "no forecasting" guardrail + (4) tone hints + (5) exact section template with a 5th "Recommended Monitoring Actions" section. |

Verbatim text is in `prompts/`. Prompt C is documented in `prompts/prompt_c_enhanced.txt`.

The three prompts form a deliberate ladder along the dimensions the homework asks
about: structural scaffolding (B > A) and instruction-following pressure (C > B > A).

## Dependent variables

**Primary**: weighted composite score in [0, 10] computed from 5 reviewer dimensions
(see `docs/validation_criteria.md`).

**Secondary (per-dimension)**: each of the 5 reviewer scores in [0, 10]:
- `factual_grounding`
- `operational_actionability`
- `communication_clarity`
- `calibrated_uncertainty`
- `completeness_compliance`

## Held constant (between groups)

The following are FIXED across all 36 reports to isolate the prompt effect:

| Held constant | Value |
|---------------|-------|
| Generator model | `claude-sonnet-4-6` |
| Reviewer model  | `claude-sonnet-4-6` |
| Generator temperature | 0.7 |
| Reviewer temperature  | 0.0 (deterministic scoring) |
| Reviewer panel composition | 5 fixed personas + rubrics |
| Reviewer weights | factual 0.30, action 0.20, clarity 0.15, calibration 0.20, completeness 0.15 |
| Source data | 12 cached variants in `data/variants/variant_NN.json` |

## Sample design

| Slot | Count | Notes |
|------|-------|-------|
| Prompts | 3 | A, B, C |
| Data variants per prompt | 12 | each derived from the same seed digest via filters (date window, magnitude floor, region focus, subsample) |
| Reports per prompt | 12 | one per variant |
| Reports total | 36 | = 3 × 12 |
| Reviewer evaluations per report | 5 | one per dimension |
| Reviewer evaluations total | 180 | = 36 × 5 |
| Aggregate composite scores | 36 | one per report |

Each (prompt, variant) cell is a distinct sample. The 12 variants are
deterministic (seeded at SEED=42 in `src/data_variants.py`), so the experiment
is fully reproducible offline.

### Why 12 per prompt?

For a one-way ANOVA with 3 groups (df_between=2, df_within=33), n=12 per group
gives ~0.80 power to detect a medium effect (Cohen's f ≈ 0.5) at α = 0.05. The
actual effect we observed is much larger (η² = 0.93, Cohen's f ≈ 3.7), so n=12
is well above the minimum required.

### Why these specific 12 variants?

The 12 variants are designed to expose prompts to **realistic content variation**
so that the experiment is not dominated by a single corner-case digest. The
variants split into three families:

1. **Date-window slices (variants 0-3)**: last 7d / 14d / 21d / 30d — exposes
   prompts to different event counts (38 → 150 events).
2. **Magnitude-floor slices (variants 4-7)**: ≥ 4.0 / 4.5 / 5.0 / 5.5 — exposes
   prompts to different intensity profiles (150 → 12 events; M5.5+ is rare).
3. **Region-focus / subsample slices (variants 8-11)**: Indonesia, Alaska,
   50% subsample, 30% subsample — varies regional density and total event count.

## Procedure

```
for variant in 12 variants:
    digest = load_variant(variant)
    for prompt in [A, B, C]:
        report = LLM(prompt + digest)               # temperature 0.7
        for reviewer in 5 reviewers:
            score = LLM(reviewer_prompt + digest + report)  # temperature 0.0
            save(score)
        composite = Σ weight[r] × score[r]
        save(composite)
```

Reports are generated and scored in parallel (3 outer workers × 5 inner workers).
The pipeline (`src/pipeline.py`) is resumable: if a report or score already
exists, it is reused.

## Operationalization of scoring

The reviewer LLM is provided with:
- The source data digest (JSON)
- The generated report (markdown)
- Its persona + checklist + scoring band + strict JSON output schema

The reviewer returns strict JSON parsed by `src/reviewer.py`. The parser:
- Extracts the first JSON object from the response
- Repairs common LLM errors (trailing commas, split-quote spans glued by em-dash)
- Coerces booleans
- Clips `score_0_10` to [0, 10]
- Falls back to score 0.0 with `_parse_status: "failed"` if all repair attempts fail

In the full 180-evaluation run, the parser handled 100% of responses successfully
after the em-dash repair pass was added (initially 2 failed; both were rescued
by the repair).

## Threats to validity

| Threat | Mitigation |
|--------|------------|
| **Single-rater bias** | 5 reviewers, role-isolated |
| **LLM rater drift across runs** | Reviewer temperature = 0; scoring is deterministic |
| **Self-evaluation bias** | Generator and reviewer use the same model family — could plausibly inflate scores for outputs that "look like Claude prose". We control for this by using identical generator+reviewer model and varying only the **input prompt**; whatever bias exists applies equally to A, B, C. |
| **Anchoring on dimension** | Each reviewer is told to evaluate ONLY one dimension and not opine on others |
| **Confounding via variant difficulty** | Each prompt sees the same 12 variants in the same order |
| **Cherry-picking** | All 36 reports + 180 scores are saved verbatim under `outputs/`. The data is auditable. |

## Out of scope

The system is one-way (review only — no closed-loop rewrite). The reviewer
suggestions are **not** fed back to a rewriter, since the experiment isolates the
**prompt → report** function, not iterative refinement.
