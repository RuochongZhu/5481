# Screenshots / Deliverable Outputs

This folder collects the terminal logs and output samples that map 1-to-1 onto
the 4-5 screenshots required by the assignment rubric. Open each file in your
terminal and take a screenshot, OR open the referenced PNG plot.

## Mapping to homework requirements

| # | Required screenshot | Where to find it | What to capture |
|---|---------------------|------------------|-----------------|
| 1 | **System in action** | `01_pipeline_full_run.log` | Terminal tail showing the 36-job progress bar and the `=== SUMMARY ===` section. Or re-run live with `python3 -m src.pipeline`. |
| 2 | **Sample validation result for one report** | `02_sample_reviewer_output.txt` and `03_sample_aggregate.txt` | The first shows ONE reviewer's per-dimension JSON output (factual_grounding on prompt_c/variant_03). The second shows the AGGREGATE composite. |
| 3 | **Validation criteria / rubric** | `../../docs/validation_criteria.md` | Open in any markdown viewer and screenshot the **rubric table** + the **LAB-Likert comparison table**. |
| 4 | **Statistical analysis results** | `04_stats_summary.log` | Terminal output of `python3 -m src.statistical_analysis` showing ANOVA F-statistic, p-value, η², Tukey HSD, and per-dimension breakdown. |
| 5 | **Comparison of scores across prompts (visual)** | `../figures/boxplot_composite.png` (primary), with `../figures/heatmap_dimension_x_prompt.png` and `../figures/violin_by_dimension.png` (supporting) | Open the PNGs directly. The boxplot shows three non-overlapping distributions for A, B, C. |

## Optional: bonus screenshots

| # | Screenshot | Source |
|---|------------|--------|
| 6 | **Effect-size chart** | `../figures/effect_size_chart.png` |
| 7 | **External validation (LAB reports)** | `05_external_validation.log` — shows the 3 original Module 3 LAB reports scoring 2.0-3.0, much lower than the experiment reports, confirming face validity of the reviewer panel. |
| 8 | **Sample raw report** | `../generated_reports/prompt_c/variant_03_last_30d.md` (a polished Prompt-C output) vs `../generated_reports/prompt_a/variant_03_last_30d.md` (the minimal Prompt-A counterpart). Open in a markdown viewer for a visual diff. |

## How to retake any screenshot from scratch

```bash
cd /Users/zhuricardo/Desktop/GitHub/5481/homework_module9_validation/

# 1: full pipeline (resumable — uses cache by default)
python3 -m src.pipeline 2>&1 | tee outputs/screenshots/01_pipeline_full_run.log

# 2: one reviewer + one aggregate output
cat outputs/reviewer_scores/prompt_c__variant_03_last_30d__factual_grounding.json
cat outputs/reviewer_scores/prompt_c__variant_03_last_30d__AGGREGATE.json

# 3: rubric (in a markdown viewer)
open docs/validation_criteria.md

# 4: statistical analysis
python3 -m src.statistical_analysis 2>&1 | tee outputs/screenshots/04_stats_summary.log

# 5: boxplot and friends
open outputs/figures/boxplot_composite.png
```
