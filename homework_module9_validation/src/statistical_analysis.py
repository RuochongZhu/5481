"""Statistical analysis: ANOVA + Tukey HSD + effect size + plots.

Run after the pipeline has produced reviewer JSON files in outputs/reviewer_scores/.

Outputs:
  - outputs/results/scores_long.csv     long-format tidy data
  - outputs/results/scores_wide.csv     pivoted by dimension
  - outputs/results/summary_stats.csv   mean ± SD per (prompt, dimension)
  - outputs/results/anova_results.json  primary ANOVA + per-dimension ANOVA + effect size
  - outputs/results/tukey_hsd.csv       pairwise post-hoc
  - outputs/figures/*.png               4 plots

CLI:
    python -m src.statistical_analysis
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from .config import (
    FIGURES_DIR,
    PROMPT_IDS,
    PROMPT_LABELS,
    RESULTS_DIR,
    REVIEWER_IDS,
    REVIEWER_PERSONAS,
    REVIEW_WEIGHTS,
    SCORE_KEY,
)
from .panel import load_all_aggregates, load_all_reviewer_results

log = logging.getLogger("hw_validator")

ALPHA = 0.05
EFFECT_SIZE_LABELS = {
    0.01: "small",
    0.06: "medium",
    0.14: "large",
}


# ---------------------------------------------------------------------------
# Tidy data
# ---------------------------------------------------------------------------

def build_long_dataframe() -> pd.DataFrame:
    """One row per (prompt, variant, reviewer)."""
    rows = []
    for r in load_all_reviewer_results():
        rows.append({
            "prompt_id":   r.get("_prompt_id"),
            "variant_id":  r.get("_variant_id"),
            "reviewer_id": r.get("_reviewer_id") or r.get("dimension"),
            "score":       float(r.get(SCORE_KEY, 0.0)),
            "checklist_count": int(r.get("checklist_count", 0)),
            "would_publish":   r.get("would_publish", "conditional"),
        })
    return pd.DataFrame(rows)


def build_wide_dataframe(long_df: pd.DataFrame) -> pd.DataFrame:
    """One row per (prompt, variant); columns: each dimension + composite."""
    wide = long_df.pivot_table(
        index=["prompt_id", "variant_id"],
        columns="reviewer_id",
        values="score",
        aggfunc="first",
    ).reset_index()
    wide.columns.name = None

    # Compute composite from saved aggregates (authoritative)
    aggs = {(a["prompt_id"], a["variant_id"]): a["composite_score_0_10"]
            for a in load_all_aggregates()}
    wide["composite"] = wide.apply(
        lambda row: aggs.get((row["prompt_id"], row["variant_id"])), axis=1,
    )
    return wide


# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------

def summary_stats(wide: pd.DataFrame) -> pd.DataFrame:
    """Mean, SD, min, max, n per (prompt, dimension/composite)."""
    metrics = list(REVIEWER_IDS) + ["composite"]
    rows = []
    for p in PROMPT_IDS:
        sub = wide[wide["prompt_id"] == p]
        for m in metrics:
            if m not in sub:
                continue
            vals = sub[m].dropna().values
            rows.append({
                "prompt_id": p,
                "metric":    m,
                "n":         int(len(vals)),
                "mean":      float(np.mean(vals)) if len(vals) else float("nan"),
                "sd":        float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0,
                "min":       float(np.min(vals)) if len(vals) else float("nan"),
                "max":       float(np.max(vals)) if len(vals) else float("nan"),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Statistical tests
# ---------------------------------------------------------------------------

def _eta_squared(groups: list[np.ndarray]) -> float:
    """Eta-squared (between-group / total sum of squares)."""
    all_vals = np.concatenate(groups)
    grand = float(np.mean(all_vals))
    ss_between = sum(len(g) * (np.mean(g) - grand) ** 2 for g in groups)
    ss_total   = sum((x - grand) ** 2 for x in all_vals)
    if ss_total == 0:
        return 0.0
    return float(ss_between / ss_total)


def _effect_size_label(eta2: float) -> str:
    if eta2 < 0.01:
        return "negligible"
    if eta2 < 0.06:
        return "small"
    if eta2 < 0.14:
        return "medium"
    return "large"


def run_anova_on_metric(
    wide: pd.DataFrame,
    metric: str,
) -> dict[str, Any]:
    groups = []
    raw_groups = {}
    for p in PROMPT_IDS:
        g = wide.loc[wide["prompt_id"] == p, metric].dropna().values
        groups.append(g)
        raw_groups[p] = g.tolist()

    # Assumption checks
    shapiro = {}
    for p, g in zip(PROMPT_IDS, groups):
        if len(g) >= 3:
            stat, pval = stats.shapiro(g)
            shapiro[p] = {"W": float(stat), "p": float(pval)}
    levene_stat, levene_p = stats.levene(*groups, center="median")

    # Primary ANOVA
    f, anova_p = stats.f_oneway(*groups)
    eta2 = _eta_squared(groups)
    df_between = len(groups) - 1
    df_within  = sum(len(g) for g in groups) - len(groups)

    # Robust nonparametric check
    kw_stat, kw_p = stats.kruskal(*groups)

    return {
        "metric": metric,
        "groups": {p: {"n": int(len(g)), "mean": float(np.mean(g)),
                       "sd": float(np.std(g, ddof=1)) if len(g) > 1 else 0.0}
                   for p, g in zip(PROMPT_IDS, groups)},
        "raw_groups": raw_groups,
        "assumptions": {
            "shapiro_wilk_normality_per_group": shapiro,
            "levene_homoscedasticity": {"W": float(levene_stat), "p": float(levene_p)},
        },
        "anova": {
            "F": float(f),
            "p": float(anova_p),
            "df_between": int(df_between),
            "df_within":  int(df_within),
            "eta_squared": float(eta2),
            "effect_size_label": _effect_size_label(eta2),
            "significant_at_0.05": bool(anova_p < ALPHA),
        },
        "kruskal_wallis_robustness": {
            "H": float(kw_stat),
            "p": float(kw_p),
            "significant_at_0.05": bool(kw_p < ALPHA),
        },
    }


def tukey_post_hoc(wide: pd.DataFrame, metric: str = "composite") -> pd.DataFrame:
    """Pairwise Tukey HSD on the requested metric across prompts."""
    sub = wide[["prompt_id", metric]].dropna()
    res = pairwise_tukeyhsd(sub[metric].values, sub["prompt_id"].values, alpha=ALPHA)
    rows = []
    for r in res._results_table.data[1:]:
        rows.append({
            "group1":         r[0],
            "group2":         r[1],
            "mean_diff":      float(r[2]),
            "p_adj":          float(r[3]),
            "ci_lower":       float(r[4]),
            "ci_upper":       float(r[5]),
            "reject_h0":      bool(r[6]),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def _setup_style():
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)


def plot_boxplot_composite(wide: pd.DataFrame, out_path: Path):
    _setup_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    order = list(PROMPT_IDS)
    palette = {p: c for p, c in zip(order, ["#cccccc", "#88aacc", "#88cc99"])}
    sns.boxplot(
        data=wide, x="prompt_id", y="composite",
        order=order, ax=ax, hue="prompt_id", palette=palette, legend=False,
        width=0.55, fliersize=4, linewidth=1.2,
    )
    sns.stripplot(
        data=wide, x="prompt_id", y="composite",
        order=order, ax=ax, color="#333333", size=4, alpha=0.85, jitter=0.18,
    )
    # Mean markers
    means = wide.groupby("prompt_id")["composite"].mean()
    for i, p in enumerate(order):
        if p in means:
            ax.scatter(i, means[p], marker="D", s=60, color="red", zorder=5,
                       label="mean" if i == 0 else None)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([PROMPT_LABELS[p] for p in order])
    ax.set_xlabel("Prompt")
    ax.set_ylabel("Weighted Composite Score (0-10)")
    ax.set_title("Composite Score by Prompt (n=12 per group)")
    ax.set_ylim(0, 10)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


def plot_violin_by_dimension(wide: pd.DataFrame, out_path: Path):
    _setup_style()
    metrics = list(REVIEWER_IDS)
    fig, axes = plt.subplots(1, len(metrics), figsize=(4 * len(metrics), 4.5), sharey=True)
    order = list(PROMPT_IDS)
    palette = {p: c for p, c in zip(order, ["#cccccc", "#88aacc", "#88cc99"])}
    for ax, m in zip(axes, metrics):
        sns.violinplot(
            data=wide, x="prompt_id", y=m, order=order, ax=ax,
            inner="quartile", cut=0, hue="prompt_id", palette=palette, legend=False,
            linewidth=1.0,
        )
        sns.stripplot(
            data=wide, x="prompt_id", y=m, order=order, ax=ax,
            color="#222222", size=3, alpha=0.7, jitter=0.18,
        )
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels(["A", "B", "C"])
        ax.set_title(f"{m.replace('_', ' ').title()}\n({REVIEWER_PERSONAS[m]})", fontsize=10)
        ax.set_xlabel("Prompt")
        ax.set_ylabel("Score (0-10)")
        ax.set_ylim(0, 10)
    fig.suptitle("Per-Dimension Score Distribution by Prompt", y=1.02, fontsize=13)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_heatmap(summary: pd.DataFrame, out_path: Path):
    _setup_style()
    metrics = list(REVIEWER_IDS) + ["composite"]
    df = summary[summary["metric"].isin(metrics)].pivot(
        index="metric", columns="prompt_id", values="mean",
    )
    df = df.reindex(metrics)
    df.columns = [PROMPT_LABELS[c] for c in df.columns]
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    sns.heatmap(df, annot=True, fmt=".2f", cmap="RdYlGn", vmin=0, vmax=10,
                cbar_kws={"label": "Mean Score (0-10)"}, ax=ax,
                linewidths=0.5, linecolor="white")
    ax.set_title("Mean Score: Dimension × Prompt")
    ax.set_xlabel("")
    ax.set_ylabel("Dimension")
    pretty = [m.replace("_", " ").title() for m in metrics]
    ax.set_yticklabels(pretty, rotation=0)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


def plot_effect_sizes(per_dim_results: list[dict], out_path: Path):
    _setup_style()
    metrics = [r["metric"] for r in per_dim_results]
    etas    = [r["anova"]["eta_squared"] for r in per_dim_results]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bar_colors = []
    for e in etas:
        if e < 0.06:
            bar_colors.append("#bbbbbb")
        elif e < 0.14:
            bar_colors.append("#f4a261")
        else:
            bar_colors.append("#2a9d8f")
    pretty = [m.replace("_", " ").title() for m in metrics]
    ax.bar(pretty, etas, color=bar_colors, edgecolor="#333")
    for t, v in zip([0.01, 0.06, 0.14], ["small", "medium", "large"]):
        ax.axhline(t, ls="--", lw=0.8, color="#666666")
        ax.text(len(metrics) - 0.5, t, f" {v} ({t:.2f})", va="bottom",
                ha="right", fontsize=8, color="#555")
    ax.set_ylabel("η² (eta-squared)")
    ax.set_ylim(0, max(1.0, max(etas) * 1.15))
    ax.set_title("Effect Size by Dimension (η²)")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------

def run_analysis() -> dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    long_df = build_long_dataframe()
    wide_df = build_wide_dataframe(long_df)

    long_df.to_csv(RESULTS_DIR / "scores_long.csv", index=False)
    wide_df.to_csv(RESULTS_DIR / "scores_wide.csv", index=False)

    summary = summary_stats(wide_df)
    summary.to_csv(RESULTS_DIR / "summary_stats.csv", index=False)

    # Primary ANOVA on composite
    primary = run_anova_on_metric(wide_df, "composite")
    primary["family"] = "primary"
    primary["alpha"] = ALPHA

    # Per-dimension ANOVA with Bonferroni correction (5 tests -> alpha=0.01)
    bonf_alpha = ALPHA / len(REVIEWER_IDS)
    per_dim = []
    for rid in REVIEWER_IDS:
        res = run_anova_on_metric(wide_df, rid)
        res["family"] = "per_dimension"
        res["alpha_bonferroni"] = bonf_alpha
        res["anova"]["significant_at_bonferroni"] = (
            res["anova"]["p"] < bonf_alpha
        )
        per_dim.append(res)

    # Tukey HSD on composite
    tukey_df = tukey_post_hoc(wide_df, "composite")
    tukey_df.to_csv(RESULTS_DIR / "tukey_hsd.csv", index=False)

    # Save bundled results
    results = {
        "alpha_primary": ALPHA,
        "alpha_per_dimension_bonferroni": bonf_alpha,
        "n_per_group": int(wide_df.groupby("prompt_id").size().min()),
        "groups": list(PROMPT_IDS),
        "weights": REVIEW_WEIGHTS,
        "primary": primary,
        "per_dimension": per_dim,
        "tukey_hsd_composite": tukey_df.to_dict(orient="records"),
    }
    (RESULTS_DIR / "anova_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    # Plots
    fig_paths = {
        "boxplot_composite": plot_boxplot_composite(
            wide_df, FIGURES_DIR / "boxplot_composite.png"),
        "violin_by_dimension": plot_violin_by_dimension(
            wide_df, FIGURES_DIR / "violin_by_dimension.png"),
        "heatmap_dimension_x_prompt": plot_heatmap(
            summary, FIGURES_DIR / "heatmap_dimension_x_prompt.png"),
        "effect_size_chart": plot_effect_sizes(
            per_dim, FIGURES_DIR / "effect_size_chart.png"),
    }
    results["figures"] = {k: str(v) for k, v in fig_paths.items()}
    return results


def print_summary(results: dict[str, Any]):
    print("=" * 72)
    print("STATISTICAL ANALYSIS SUMMARY")
    print("=" * 72)
    print(f"  n per group       : {results['n_per_group']}")
    print(f"  α (primary)       : {results['alpha_primary']}")
    print(f"  α (per-dim, Bonf.): {results['alpha_per_dimension_bonferroni']:.4f}")
    print()

    print("Group means (composite):")
    for p, info in results["primary"]["groups"].items():
        print(f"  {PROMPT_LABELS[p]:18s}  n={info['n']:2d}  "
              f"mean={info['mean']:.3f}  sd={info['sd']:.3f}")
    print()

    p_an = results["primary"]["anova"]
    print(f"PRIMARY ONE-WAY ANOVA on composite score:")
    print(f"  F({p_an['df_between']}, {p_an['df_within']}) = {p_an['F']:.3f}")
    print(f"  p = {p_an['p']:.3e}    "
          f"{'SIGNIFICANT' if p_an['significant_at_0.05'] else 'not significant'} at α=0.05")
    print(f"  η² = {p_an['eta_squared']:.4f}  ({p_an['effect_size_label']} effect)")
    kw = results["primary"]["kruskal_wallis_robustness"]
    print(f"  Kruskal-Wallis H = {kw['H']:.3f}, p = {kw['p']:.3e} "
          f"({'sig.' if kw['significant_at_0.05'] else 'n.s.'})")
    print()

    print("TUKEY HSD post-hoc (composite):")
    for r in results["tukey_hsd_composite"]:
        verdict = "*** REJECT H0" if r["reject_h0"] else "  (n.s.)"
        print(f"  {r['group1']:9s} vs {r['group2']:9s}  "
              f"Δ={r['mean_diff']:+.3f}  p_adj={r['p_adj']:.3e}  {verdict}")
    print()

    print("PER-DIMENSION ANOVA (Bonferroni-corrected α):")
    bonf = results["alpha_per_dimension_bonferroni"]
    for d in results["per_dimension"]:
        a = d["anova"]
        sig = (
            "***" if a["p"] < bonf
            else ("(0.05)" if a["p"] < 0.05 else "n.s.")
        )
        print(f"  {d['metric']:30s}  F={a['F']:6.2f}  "
              f"p={a['p']:.3e}  η²={a['eta_squared']:.3f}  {sig}")
    print("=" * 72)


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    results = run_analysis()
    print_summary(results)
    print()
    print("Artifacts:")
    print(f"  outputs/results/anova_results.json")
    print(f"  outputs/results/scores_long.csv")
    print(f"  outputs/results/scores_wide.csv")
    print(f"  outputs/results/summary_stats.csv")
    print(f"  outputs/results/tukey_hsd.csv")
    print(f"  outputs/figures/*.png")


if __name__ == "__main__":
    main()
