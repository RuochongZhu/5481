"""mbe_e2 - 5-Reviewer Radial Pattern.

Polar / radial diagram showing the 5 reviewer roles, their weights, focus,
and the auto-backtrack policy. Source: §3.2, §6 of the CampusRide draft.

Each reviewer occupies an angular wedge proportional to its weight
(Narrative 25% = 90 deg, Coverage 25% = 90 deg, Gap 20% = 72 deg,
Contradiction 15% = 54 deg, Honesty 15% = 54 deg). Wedges are colored
per the brief and labeled with name + weight + focus + slash command.
The center holds the scoring formula; the right-hand callout panel lists
the auto-backtrack gates (overall < 0.85, honesty < 0.80, disagreement >
0.3 -> human-in-loop).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import renderer, setup_mpl, save_mpl, register


@renderer("mbe_e2_5_reviewer_radial")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import Wedge, FancyBboxPatch
    import numpy as np

    # --- Reviewer data --------------------------------------------------------
    # Order: largest weight first (clockwise from top).
    reviewers = [
        # name,         weight, color,     focus_zh,         focus_en,                cmd
        ("Narrative",     0.25, "#16A085", "叙事逻辑流",       "narrative logic flow",   "/review-narrative"),
        ("Coverage",      0.25, "#2980B9", "类别覆盖完整性",    "category coverage",      "/review-coverage"),
        ("Gap",           0.20, "#8E44AD", "研究空白可信度",    "gap credibility",        "/review-gap"),
        ("Contradiction", 0.15, "#E67E22", "矛盾处理诚实度",    "contradiction honesty",  "/review-contradiction"),
        ("Honesty",       0.15, "#C0392B", "过度论断与范围控制", "scope discipline",       "/review-honesty"),
    ]

    # --- Figure ---------------------------------------------------------------
    fig = plt.figure(figsize=(13.5, 9.5))
    # Two-column layout: left polar wedges, right callouts
    ax = fig.add_axes([0.02, 0.06, 0.58, 0.84])  # left polar area (cartesian)
    ax_right = fig.add_axes([0.62, 0.06, 0.36, 0.84])  # right callouts
    ax.set_aspect("equal")
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
    ax.axis("off")
    ax_right.axis("off")
    ax_right.set_xlim(0, 1)
    ax_right.set_ylim(0, 1)

    # --- Wedges ---------------------------------------------------------------
    # matplotlib.patches.Wedge angles measured CCW from +x axis (3 o'clock).
    # We want to start at the TOP (90 deg) and go CLOCKWISE.
    # For each reviewer i, span = weight * 360. Going clockwise from 90 means
    # theta1 = 90 - cumulative_to_end, theta2 = 90 - cumulative_to_start.
    R_OUTER = 1.18
    R_INNER = 0.42
    cumulative = 0.0
    wedge_meta = []
    for name, w, color, fzh, fen, cmd in reviewers:
        span = w * 360.0
        # Going clockwise from 90: end angle (smaller) = 90 - cumulative - span
        theta2 = 90.0 - cumulative           # leading edge (CCW boundary)
        theta1 = 90.0 - cumulative - span    # trailing edge
        wedge = Wedge(
            center=(0, 0), r=R_OUTER, theta1=theta1, theta2=theta2,
            width=R_OUTER - R_INNER,
            facecolor=color, edgecolor="white", linewidth=2.2,
            alpha=0.92, zorder=3,
        )
        ax.add_patch(wedge)
        # Soft outer ring for emphasis
        outer_ring = Wedge(
            center=(0, 0), r=R_OUTER + 0.04, theta1=theta1, theta2=theta2,
            width=0.04, facecolor=color, edgecolor="none",
            alpha=0.35, zorder=2.5,
        )
        ax.add_patch(outer_ring)
        wedge_meta.append((name, w, color, fzh, fen, cmd, theta1, theta2))
        cumulative += span

    # --- Wedge labels ---------------------------------------------------------
    for name, w, color, fzh, fen, cmd, theta1, theta2 in wedge_meta:
        mid_deg = (theta1 + theta2) / 2.0
        mid_rad = np.deg2rad(mid_deg)
        # Inner label: name + weight, placed at mid-radius
        r_label = (R_OUTER + R_INNER) / 2.0
        lx = r_label * np.cos(mid_rad)
        ly = r_label * np.sin(mid_rad)
        ax.text(
            lx, ly + 0.06, name,
            ha="center", va="center", fontsize=12.5, fontweight="bold",
            color="white", zorder=5,
        )
        ax.text(
            lx, ly - 0.06, f"{int(w * 100)}%",
            ha="center", va="center", fontsize=14.5, fontweight="bold",
            color="white", zorder=5,
        )

        # Outer label: focus (en) + slash command, placed beyond outer ring
        r_outer_label = R_OUTER + 0.20
        ox = r_outer_label * np.cos(mid_rad)
        oy = r_outer_label * np.sin(mid_rad)
        # Determine alignment based on which side of the figure
        if ox > 0.05:
            ha = "left"
        elif ox < -0.05:
            ha = "right"
        else:
            ha = "center"

        ax.text(
            ox, oy + 0.05, fen,
            ha=ha, va="center", fontsize=10.0, fontweight="bold",
            color=color, zorder=5,
        )
        ax.text(
            ox, oy - 0.07, cmd,
            ha=ha, va="center", fontsize=8.6, family="monospace",
            color="#34495E", zorder=5,
        )

    # --- Center: title + scoring formula -------------------------------------
    # Soft white core
    core = mpatches.Circle(
        (0, 0), R_INNER - 0.02, facecolor="white",
        edgecolor="#BDC3C7", linewidth=1.2, zorder=4,
    )
    ax.add_patch(core)
    ax.text(
        0, 0.18, "5-Reviewer\nEval (P5)",
        ha="center", va="center", fontsize=13.0, fontweight="bold",
        color="#1A1A1A", zorder=6,
    )
    ax.text(
        0, -0.05, "weighted score =",
        ha="center", va="center", fontsize=8.0, color="#566573", zorder=6,
    )
    ax.text(
        0, -0.16,
        "0.25 N + 0.25 C\n+ 0.20 G\n+ 0.15 Co + 0.15 H",
        ha="center", va="center", fontsize=8.2, family="monospace",
        color="#1A1A1A", zorder=6,
    )

    # --- Top annotation (above polar plot) -----------------------------------
    ax.text(
        0, 1.48,
        "Weights total 100%; backtrack policy is multi-gate, not weighted-average alone.",
        ha="center", va="center", fontsize=10.5, fontweight="bold",
        color="#1A1A1A",
    )

    # --- Right-hand callout: auto-backtrack policy ---------------------------
    ax_right.text(
        0.5, 0.97, "Auto-backtrack policy",
        ha="center", va="top", fontsize=13.0, fontweight="bold",
        color="#1A1A1A",
    )

    callouts = [
        ("if  overall < 0.85",
         "backtrack to weakest-dimension phase",
         "#16A085"),
        ("if  honesty < 0.80",
         "backtrack to P4 (Evidence Inventory)\nregardless of overall score",
         "#C0392B"),
        ("if  reviewer disagreement > 0.3",
         "pause -> human-in-loop confirmation",
         "#E67E22"),
    ]
    y_top = 0.88
    box_h = 0.18
    gap = 0.04
    for i, (cond, action, accent) in enumerate(callouts):
        y0 = y_top - i * (box_h + gap) - box_h
        # Box
        box = FancyBboxPatch(
            (0.04, y0), 0.92, box_h,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#F8F9F9", edgecolor=accent, linewidth=1.6,
            transform=ax_right.transAxes, zorder=2,
        )
        ax_right.add_patch(box)
        # Accent bar
        ax_right.add_patch(mpatches.Rectangle(
            (0.04, y0), 0.018, box_h,
            facecolor=accent, edgecolor="none",
            transform=ax_right.transAxes, zorder=3,
        ))
        ax_right.text(
            0.09, y0 + box_h - 0.045, cond,
            ha="left", va="top", fontsize=10.5, fontweight="bold",
            family="monospace", color=accent,
        )
        ax_right.text(
            0.09, y0 + box_h - 0.085, action,
            ha="left", va="top", fontsize=9.6, color="#1A1A1A",
        )

    # Quality-gate footer on the right column
    ax_right.text(
        0.5, 0.18,
        "Cat-J active < 3  ->  not done",
        ha="center", va="center", fontsize=9.0,
        color="#566573", style="italic",
    )
    ax_right.text(
        0.5, 0.14,
        "fallback placeholder remains  ->  not done",
        ha="center", va="center", fontsize=9.0,
        color="#566573", style="italic",
    )
    ax_right.text(
        0.5, 0.10,
        "corpus is append-only; no paper deleted",
        ha="center", va="center", fontsize=9.0,
        color="#566573", style="italic",
    )

    # --- Bottom annotation (full-figure) -------------------------------------
    fig.text(
        0.5, 0.025,
        "Each reviewer is context-isolated; only injected with "
        "scoring.PAPER_CONTEXT_V4 (3 contributions + evidence standards + verb discipline).",
        ha="center", va="bottom", fontsize=10.0, style="italic",
        color="#1A1A1A",
    )

    pdf, png = save_mpl("mbe_e2_5_reviewer_radial")
    register("mbe_e2_5_reviewer_radial", "ok", png_path=png)


if __name__ == "__main__":
    render()
