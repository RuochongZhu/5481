#!/usr/bin/env bash
# Module 9 Homework: one-command full pipeline.
# Runs:
#   1) build 12 data variants
#   2) full experiment (36 reports + 180 reviewer evals)
#   3) statistical analysis + plots
#
# Resumable: re-running skips any (prompt, variant) pair whose outputs exist.

set -e
cd "$(dirname "$0")"

# Find a Python with the right packages. Prefer the research-agent venv.
PY="/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/.venv/bin/python3"
if [ ! -x "$PY" ]; then
    PY="$(command -v python3)"
fi
echo "Using Python: $PY"
echo

echo "=== Step 1: Build 12 data variants ==="
"$PY" -m src.data_variants
echo

echo "=== Step 2: Run full experiment (36 reports, 180 reviewer evaluations) ==="
"$PY" -m src.pipeline
echo

echo "=== Step 3: Statistical analysis + plots ==="
"$PY" -m src.statistical_analysis
echo

echo "Done. Key artifacts:"
echo "  outputs/results/anova_results.json"
echo "  outputs/results/scores_long.csv"
echo "  outputs/figures/boxplot_composite.png"
echo "  outputs/figures/violin_by_dimension.png"
echo "  outputs/figures/heatmap_dimension_x_prompt.png"
echo "  outputs/figures/effect_size_chart.png"
