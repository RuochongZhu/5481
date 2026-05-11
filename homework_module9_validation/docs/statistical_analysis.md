# Statistical Analysis

## Hypotheses

**Primary hypothesis** (one-way ANOVA on weighted composite score):

- H₀: μ_A = μ_B = μ_C (the three prompts produce equally-scored reports on average)
- H₁: at least one mean differs
- α = 0.05

**Secondary hypotheses** (per-dimension, one-way ANOVA × 5 dimensions):

- For each dimension d ∈ {factual_grounding, operational_actionability, communication_clarity, calibrated_uncertainty, completeness_compliance}: H₀ᵈ: μ_A^d = μ_B^d = μ_C^d.
- Family-wise α corrected by Bonferroni: α' = 0.05 / 5 = **0.01**.

## Assumption checks

For a one-way ANOVA to be valid we need approximate normality within groups and
homogeneity of variance across groups. We ran both checks:

### Shapiro-Wilk per group (normality)
| Group | W | p | Conclusion |
|-------|---|---|-----------|
| A | 0.961 | 0.794 | Fail to reject normality |
| B | 0.966 | 0.867 | Fail to reject normality |
| C | 0.937 | 0.456 | Fail to reject normality |

All three p-values are well above 0.05, so we do not detect non-normality.

### Levene's test (homoscedasticity)
W = 1.83, p = 0.177. We do not detect unequal variances.

### Robustness via Kruskal-Wallis (nonparametric)
H = 31.16, p = 1.7 × 10⁻⁷. Significant — consistent with the parametric result.

## Primary result: one-way ANOVA on composite score

**F(2, 33) = 229.30, p = 4.4 × 10⁻²⁰**

- η² = 0.93 (very large effect, far beyond the conventional "large" threshold of 0.14)
- We reject H₀ at α = 0.05 with overwhelming evidence.

### Group means (composite, scale 0-10)
| Prompt        | n  | mean | SD   | min  | max  |
|---------------|----|------|------|------|------|
| A: Minimal    | 12 | 6.06 | 0.40 | 5.42 | 6.72 |
| B: Structured | 12 | 7.13 | 0.22 | 6.78 | 7.55 |
| C: Enhanced   | 12 | 8.66 | 0.24 | 8.22 | 8.97 |

### Tukey HSD post-hoc (all three pairwise comparisons)
| Comparison | Δ (mean diff) | adj. p | 95% CI | Reject H₀? |
|------------|---------------|--------|--------|-----------|
| A vs B | +1.067 | < 1e-3 | [0.811, 1.322] | **yes** |
| A vs C | +2.596 | < 1e-3 | [2.340, 2.851] | **yes** |
| B vs C | +1.529 | < 1e-3 | [1.273, 1.785] | **yes** |

The full table (with raw p_adj values from statsmodels) is at
`outputs/results/tukey_hsd.csv`.

## Secondary result: per-dimension ANOVA

Each dimension was tested independently. Bonferroni-corrected α = 0.01.

| Dimension | F | p | η² | Sig. at 0.01? |
|-----------|---|---|-----|---------------|
| **Completeness Compliance** | 2271.14 | 4.6e-36 | 0.993 | **yes** |
| **Operational Actionability** | 216.50 | 1.1e-19 | 0.929 | **yes** |
| **Calibrated Uncertainty** | 99.68 | 1.0e-14 | 0.858 | **yes** |
| **Communication Clarity** | 12.00 | 1.2e-4 | 0.421 | **yes** |
| **Factual Grounding** | 2.00 | 0.152 | 0.108 | **no** |

**Interpretation**: the composite-score separation is driven by 4 of the 5
dimensions. Factual grounding does NOT significantly differ across prompts
(η² = 0.11, p = 0.15 > 0.01). This makes substantive sense: even a minimal
prompt asking for an earthquake summary will yield factually-grounded output
from a competent model — the prompt does not need to teach factuality.

**Surprising finding** in `operational_actionability`: Prompt B (Structured)
actually scored **lower** than Prompt A (Minimal) on actionability (4.62 vs 5.54),
even though B is more elaborate. Inspection of the reviewer comments shows that
B's strict section layout pushes content into a "Risk Watch" subsection that the
Emergency Coordinator reviewer reads as *descriptive* rather than *prescriptive*,
whereas A's 6-bullet format often happens to include a prioritized action item
in one of the bullets. Prompt C dominates both because it explicitly demands a
"Recommended Monitoring Actions" numbered list. This is an honest secondary
finding — not all "more structure" is "more action".

## Visualization (in `outputs/figures/`)

- `boxplot_composite.png` — composite score by prompt; three non-overlapping distributions.
- `violin_by_dimension.png` — 5-panel grid showing the distribution shape per dimension per prompt.
- `heatmap_dimension_x_prompt.png` — mean score for each (dimension × prompt) cell.
- `effect_size_chart.png` — η² per dimension with horizontal small/medium/large reference lines.

## Conclusion

Prompt C (Enhanced) produces statistically and meaningfully better earthquake
situation reports than Prompts A (Minimal) and B (Structured), as judged by a
5-reviewer LLM panel. The primary one-way ANOVA on composite score yields
F(2, 33) = 229.30, p = 4.4 × 10⁻²⁰, η² = 0.93. All three pairwise comparisons
(Tukey HSD) reject H₀. The result is robust to nonparametric testing
(Kruskal-Wallis p = 1.7 × 10⁻⁷) and meets standard ANOVA assumptions
(Shapiro-Wilk p > 0.45 per group; Levene p = 0.18).

The per-dimension breakdown clarifies WHERE the prompts differ:
**completeness, actionability, and calibration** are the dimensions where
prompt design has the largest leverage. **Factual grounding** is roughly equal
across prompts — a useful insight: when the underlying model is capable of
factual recall, prompt design adds value mostly by shaping STRUCTURE,
ACTIONABILITY, and EPISTEMIC CALIBRATION.
