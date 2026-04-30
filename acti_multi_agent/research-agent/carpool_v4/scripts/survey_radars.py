"""Survey radar figures (Q24 tolerance, Q26 motivation, Q30 severity-by-distance).

Implements the three prompts in research-agent/propt.md against the Qualtrics
export `Cornell Carpool System Survey_April 21, 2026_22.55.csv`.

Run:
    ./.venv/bin/python carpool_v4/scripts/survey_radars.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV_PATH = Path(
    "/Users/zhuricardo/Downloads/Cornell Carpool System Survey_April 21, 2026_22.55.csv"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "carpool_v4" / "output" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DRIVER_COLOR = "#C0392B"
RIDER_COLOR = "#2980B9"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]


def load_survey() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, header=0, skiprows=[1, 2])
    df = df[df["Status"] != "Survey Preview"].copy()
    return df


def subsets(df: pd.DataFrame, cols: list[str], require_any: bool = False):
    """Return (driver_both_df, rider_df). If require_any=False, drop rows
    missing any axis (Q24 prompt rule). If True, keep rows with at least
    one non-null axis (Rider-only / Q26 rule)."""
    db_mask = df["Q3"].isin(["Driver", "Both"])
    rd_mask = df["Q3"] == "Rider"

    db = df[db_mask].copy()
    rd = df[rd_mask].copy()
    for c in cols:
        db[c] = pd.to_numeric(db[c], errors="coerce")
        rd[c] = pd.to_numeric(rd[c], errors="coerce")

    if require_any:
        db = db[db[cols].notna().any(axis=1)]
        rd = rd[rd[cols].notna().any(axis=1)]
    else:
        db = db.dropna(subset=cols, how="any")
        rd = rd.dropna(subset=cols, how="any")
    return db, rd


def radar_axes(ax, n_axes: int, axis_labels: list[str], r_max: float, r_step: float):
    angles = np.linspace(0, 2 * np.pi, n_axes, endpoint=False)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(axis_labels, fontsize=11)
    ticks = np.arange(r_step, r_max + 0.001, r_step)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{int(t)}" for t in ticks], fontsize=9)
    ax.set_ylim(0, r_max)
    ax.set_rlabel_position(180 / n_axes)
    return angles


def plot_series(ax, angles, values, color, alpha_fill, linestyle, label):
    vals = np.concatenate([values, values[:1]])
    ang = np.concatenate([angles, angles[:1]])
    ax.plot(ang, vals, color=color, linewidth=2.0, linestyle=linestyle, label=label)
    ax.fill(ang, vals, color=color, alpha=alpha_fill)


# ---------------------------------------------------------------------------
# Prompt 1 — Q24 driver tolerance
# ---------------------------------------------------------------------------

def make_q24(df: pd.DataFrame):
    cols = ["Q24_1", "Q24_2", "Q24_3", "Q24_4"]
    # Per-axis dropna (Q3-membership + at least one axis filled). This matches
    # the v4.2 Table 2 / F5 cohort rule: Driver/Both N=19, Rider-only N=11–12.
    db, rd = subsets(df, cols, require_any=True)

    means_db = db[cols].mean()
    means_rd = rd[cols].mean()
    n_db_axis = db[cols].notna().sum()
    n_rd_axis = rd[cols].notna().sum()

    print("\n=== Q24 Tolerance (per-axis dropna) ===")
    print(f"Driver/Both per-axis N: {n_db_axis.to_dict()}")
    print(f"Rider-only per-axis N: {n_rd_axis.to_dict()}")
    table = pd.DataFrame({
        "Driver/Both mean": means_db.round(2),
        "Driver/Both N": n_db_axis,
        "Rider-only mean": means_rd.round(2),
        "Rider-only N": n_rd_axis,
    })
    print(table.to_string())

    expectations = {
        "DB Q24_3": (means_db["Q24_3"], 29.1, 1.0),
        "DB Q24_4": (means_db["Q24_4"], 52.0, 5.0),
        "RD Q24_2": (means_rd["Q24_2"], 19.0, 5.0),
    }
    for k, (got, want, tol) in expectations.items():
        if abs(got - want) > tol:
            print(f"  WARNING: {k} mean {got:.2f} differs from expected {want} by >{tol} pts")

    axis_order = ["Q24_3", "Q24_1", "Q24_4", "Q24_2"]
    axis_labels = [
        "Unfair rating\n(Q24_3)",
        "Late arrival\n(Q24_1)",
        "Non-standard\nroute (Q24_4)",
        "Destination\nchange (Q24_2)",
    ]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    angles = radar_axes(ax, 4, axis_labels, r_max=60, r_step=15)

    db_vals = np.array([means_db[c] for c in axis_order])
    rd_vals = np.array([means_rd[c] for c in axis_order])

    def _n_label(ns):
        lo, hi = int(ns.min()), int(ns.max())
        return f"{lo}" if lo == hi else f"{lo}–{hi}"

    plot_series(ax, angles, db_vals, DRIVER_COLOR, 0.25, "-",
                f"Driver/Both (N={_n_label(n_db_axis)})")
    plot_series(ax, angles, rd_vals, RIDER_COLOR, 0.15, "--",
                f"Rider-only (N={_n_label(n_rd_axis)})")

    ax.legend(loc="center left", bbox_to_anchor=(1.25, 1.0), frameon=False, fontsize=10)

    pdf = OUT_DIR / "q24_tolerance_radar.pdf"
    png = OUT_DIR / "q24_tolerance_radar.png"
    fig.savefig(pdf, bbox_inches="tight", dpi=300)
    fig.savefig(png, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"saved: {pdf.name}, {png.name}")


# ---------------------------------------------------------------------------
# Prompt 2 — Q26 motivation
# ---------------------------------------------------------------------------

def make_q26(df: pd.DataFrame):
    # NOTE: actual question-text mapping is
    #   Q26_1 = Splitting fuel costs
    #   Q26_2 = Social expansion
    #   Q26_3 = Platform rewards
    #   Q26_4 = Environmental impact
    cols = ["Q26_1", "Q26_2", "Q26_3", "Q26_4"]
    full = df.copy()
    for c in cols:
        full[c] = pd.to_numeric(full[c], errors="coerce")

    full_means = full[cols].mean()
    full_n = full[cols].notna().sum()
    print("\n=== Q26 Motivation (full sample) ===")
    print(pd.DataFrame({"mean": full_means.round(2), "N": full_n}).to_string())

    expect = {"Q26_1": 63.6, "Q26_2": 45.6, "Q26_3": 48.3, "Q26_4": 44.5}
    for k, want in expect.items():
        got = full_means[k]
        if abs(got - want) > 3:
            print(f"  WARNING: full-sample {k} mean {got:.2f} differs from expected {want} by >3 pts")

    db, rd = subsets(df, cols, require_any=True)
    means_db = db[cols].mean()
    means_rd = rd[cols].mean()
    n_db_axis = db[cols].notna().sum()
    n_rd_axis = rd[cols].notna().sum()
    print("\n=== Q26 by subset ===")
    print(pd.DataFrame({
        "DB mean": means_db.round(2), "DB N": n_db_axis,
        "RD mean": means_rd.round(2), "RD N": n_rd_axis,
    }).to_string())

    # Visual order: fuel (top), rewards (right), social (bottom), environmental (left)
    axis_order = ["Q26_1", "Q26_3", "Q26_2", "Q26_4"]
    axis_labels = [
        "Splitting\nfuel costs",
        "Platform rewards\n(Points)",
        "Social\nexpansion",
        "Environmental\nimpact",
    ]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    angles = radar_axes(ax, 4, axis_labels, r_max=80, r_step=20)

    db_vals = np.array([means_db[c] for c in axis_order])
    rd_vals = np.array([means_rd[c] for c in axis_order])

    db_n_label = int(n_db_axis.min())
    rd_n_label = int(n_rd_axis.min())

    plot_series(ax, angles, db_vals, DRIVER_COLOR, 0.25, "-", f"Driver/Both (N={db_n_label})")
    plot_series(ax, angles, rd_vals, RIDER_COLOR, 0.15, "--", f"Rider-only (N={rd_n_label})")

    ax.legend(loc="center left", bbox_to_anchor=(1.25, 1.0), frameon=False, fontsize=10)

    pdf = OUT_DIR / "q26_motivation_radar.pdf"
    png = OUT_DIR / "q26_motivation_radar.png"
    fig.savefig(pdf, bbox_inches="tight", dpi=300)
    fig.savefig(png, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"saved: {pdf.name}, {png.name}")


# ---------------------------------------------------------------------------
# Prompt 3 — Q30 severity by distance (3-panel radar)
# ---------------------------------------------------------------------------

# Actual question-text mapping (overrides the prompt's assumed order).
Q30_PAIN_LABEL = {
    1: ("Expensive parking fee", "Expensive\nparking fee"),
    2: ("Bus delays", "Bus\ndelays"),
    3: ("Inflexible schedule", "Inflexible\nschedule"),
    4: ("Inconsistent operating hours", "Inconsistent\noperating hours"),
    5: ("Safety hazards", "Safety\nhazards"),
    6: ("Luggage restrictions", "Luggage\nrestrictions"),
    7: ("Limited coverage", "Limited\ncoverage"),
    8: ("Weather disruptions", "Weather\ndisruptions"),
}
DISTANCE_LABEL = {
    1: "Within Ithaca",
    2: "Short Trips (1–3 hrs)",
    3: "Long-Distance (3+ hrs)",
}


def make_q30(df: pd.DataFrame):
    pain_ids = sorted(Q30_PAIN_LABEL.keys())
    distance_ids = [1, 2, 3]
    all_cols = [f"Q30_{p}_{d}" for p in pain_ids for d in distance_ids]
    full = df.copy()
    for c in all_cols:
        full[c] = pd.to_numeric(full[c], errors="coerce")

    print("\n=== Q30 likert range check ===")
    stacked = full[all_cols].stack()
    print(f"min={stacked.min()}, max={stacked.max()}, n_obs={len(stacked)}")

    db_full = full[full["Q3"].isin(["Driver", "Both"])]
    rd_full = full[full["Q3"] == "Rider"]

    series = {}  # (subset, distance) -> (means_array, per_axis_n_min)
    rows = []
    for subset_name, sub in [("Driver/Both", db_full), ("Rider-only", rd_full)]:
        for d in distance_ids:
            cols = [f"Q30_{p}_{d}" for p in pain_ids]
            means = sub[cols].mean().to_numpy()
            ns = sub[cols].notna().sum()
            series[(subset_name, d)] = (means, int(ns.min()), int(ns.max()))
            for p, m, n in zip(pain_ids, means, ns):
                rows.append({
                    "subset": subset_name,
                    "distance": DISTANCE_LABEL[d],
                    "pain": Q30_PAIN_LABEL[p][0],
                    "N": int(n),
                    "mean": round(float(m), 2) if not np.isnan(m) else None,
                })

    table = pd.DataFrame(rows)
    print("\n=== Q30 by subset × distance × pain ===")
    print(table.to_string(index=False))

    # Global radius: max mean across all series, rounded up.
    flat = np.concatenate([v[0] for v in series.values()])
    flat = flat[~np.isnan(flat)]
    r_max_raw = float(flat.max())
    r_max = int(np.ceil(r_max_raw + 1.0))
    if r_max < 4:
        r_max = 4
    r_step = max(1, r_max // 4)

    axis_labels = [Q30_PAIN_LABEL[p][1] for p in pain_ids]

    fig, axes = plt.subplots(1, 3, figsize=(18, 7), subplot_kw={"projection": "polar"})
    for ax, d in zip(axes, distance_ids):
        angles = radar_axes(ax, len(pain_ids), axis_labels, r_max=r_max, r_step=r_step)
        ax.set_title(DISTANCE_LABEL[d], fontsize=12, pad=20)

        db_means, db_nmin, db_nmax = series[("Driver/Both", d)]
        rd_means, rd_nmin, rd_nmax = series[("Rider-only", d)]
        db_label = f"Driver/Both (N={db_nmin if db_nmin == db_nmax else f'{db_nmin}–{db_nmax}'})"
        rd_label = f"Rider-only (N={rd_nmin if rd_nmin == rd_nmax else f'{rd_nmin}–{rd_nmax}'})"

        plot_series(ax, angles, db_means, DRIVER_COLOR, 0.25, "-", db_label)
        plot_series(ax, angles, rd_means, RIDER_COLOR, 0.15, "--", rd_label)

        for label in ax.get_xticklabels():
            label.set_fontsize(9)

    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="center right", bbox_to_anchor=(0.98, 0.5),
               frameon=False, fontsize=10)
    fig.subplots_adjust(left=0.04, right=0.86, top=0.88, bottom=0.05, wspace=0.45)

    pdf = OUT_DIR / "q30_severity_by_distance.pdf"
    png = OUT_DIR / "q30_severity_by_distance.png"
    fig.savefig(pdf, dpi=300)
    fig.savefig(png, dpi=300)
    plt.close(fig)
    print(f"saved: {pdf.name}, {png.name}")


def main() -> int:
    if not CSV_PATH.exists():
        print(f"CSV not found at {CSV_PATH}", file=sys.stderr)
        return 1
    df = load_survey()
    print(f"loaded {len(df)} rows after dropping Survey Preview; Q3 values: {df['Q3'].unique()}")
    make_q24(df)
    make_q26(df)
    make_q30(df)
    print(f"\nAll figures written to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
