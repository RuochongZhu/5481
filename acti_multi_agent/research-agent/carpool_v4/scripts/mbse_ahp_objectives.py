"""mbse_ahp_objectives - Analytical Hierarchy Process tree.

Three-tier hierarchy:
  Tier 0: CampusRide Design Objective (root)
  Tier 1: 3 top-level criteria with weights summing to 1.00
            - User Experience & Trust          (0.50)
            - Operational Efficiency & Reach   (0.33)
            - Cost-Sharing & Sustainability    (0.17)
  Tier 2: 4 + 3 + 3 = 10 sub-criteria (sub-weights normalized within criterion)
  Tier 3: composite weight = top * sub, displayed as numeric leaf labels

Pure-matplotlib horizontal layout (no graphviz dependency) so the figure
renders identically across environments.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


# Top-level criteria: (label, weight, color_main, color_light, color_dark)
CRITERIA = [
    ("User Experience\n& Trust", 0.50,
     "#3498DB", "#D6EAF8", "#1F618D"),
    ("Operational Efficiency\n& Reach", 0.33,
     "#27AE60", "#D5F5E3", "#1E8449"),
    ("Cost-Sharing\n& Sustainability", 0.17,
     "#E91E63", "#F9D5DD", "#A93226"),
]

# Sub-criteria, grouped by parent index. Each: (label, sub_weight, anchor_note)
SUBS = [
    [
        (".edu Identity\nTrust Primitive",       0.30, "F3 mean 67.3"),
        ("Real-time Location\nSharing",          0.25, "F3 69.1"),
        ("Emergency SOS\nPath",                  0.25, "F3 63.5"),
        ("Rating Fairness\n(Driver-side, F5)",   0.20, "F5 N=19: 29.1"),
    ],
    [
        ("Driver Supply for\nLong-Distance (F6)", 0.40, "F6 12/33 willing"),
        ("Fair Cost-Splitting",                   0.30, "F4 financial 63.6"),
        ("Reliability under\nPeak / Concurrent",  0.30, "Socket.IO room"),
    ],
    [
        ("Reduce Solo\nCar Miles",                0.30, "sustainability"),
        ("TCAT / Public Transit\nIntegration",    0.40, "alt-mode bridge"),
        ("Frequent-User\nReward Loop",            0.30, "Points specified"),
    ],
]


def _box(ax, cx, cy, w, h, text,
         facecolor, edgecolor, fontsize, fontweight="normal",
         text_color="#1A1A1A", radius=0.04, lw=1.0, zorder=4):
    import matplotlib.patches as mpatches
    box = mpatches.FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw,
        zorder=zorder,
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight,
            color=text_color, linespacing=1.05, zorder=zorder + 1)


@renderer("mbse_ahp_objectives")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt

    # Verify weights sum to 1.0
    assert abs(sum(c[1] for c in CRITERIA) - 1.0) < 1e-9
    for parent_idx, group in enumerate(SUBS):
        assert abs(sum(s[1] for s in group) - 1.0) < 1e-9, (
            f"sub-weights for criterion {parent_idx} must sum to 1.0")

    # Layout: vertical tree, root at top, criteria mid, subs + composites bottom
    # Reserve left margin (x in [0, 12]) for tier band labels.
    fig_w, fig_h = 22.0, 12.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 130)        # extra horizontal canvas to spread sub-criteria
    ax.set_ylim(0, 100)
    ax.axis("off")

    LEFT_MARGIN = 12

    # ---- Root (Tier 0) ----
    root_x, root_y = (LEFT_MARGIN + 130) / 2, 89
    _box(ax, root_x, root_y, 50, 8,
         "CampusRide Design Objective\n(maximize verified-campus mobility utility)",
         facecolor="#34495E", edgecolor="#1B2631", lw=1.6,
         fontsize=14, fontweight="bold", text_color="white", radius=0.08,
         zorder=6)

    # ---- Criteria (Tier 1) ----
    # Three criteria distributed across the canvas, horizontally even-spaced.
    crit_y = 75
    avail_left = LEFT_MARGIN + 8
    avail_right = 128
    avail_span = avail_right - avail_left
    crit_xs = [avail_left + avail_span * frac for frac in (1/6, 3/6, 5/6)]
    crit_w, crit_h = 30, 10

    for i, (label, weight, c_main, c_light, c_dark) in enumerate(CRITERIA):
        cx = crit_xs[i]
        # Box
        _box(ax, cx, crit_y, crit_w, crit_h,
             label,
             facecolor=c_light, edgecolor=c_dark, lw=2.0,
             fontsize=13, fontweight="bold", text_color=c_dark, radius=0.07,
             zorder=5)
        # Weight badge above the box
        wx = cx - crit_w / 2 + 4.5
        wy = crit_y + crit_h / 2 - 1.5
        from matplotlib.patches import Circle
        ax.add_patch(Circle((wx, wy), 2.6,
                            facecolor=c_main, edgecolor=c_dark, lw=1.4,
                            zorder=7))
        ax.text(wx, wy, f"{weight:.2f}",
                ha="center", va="center", fontsize=11, fontweight="bold",
                color="white", zorder=8)

        # Connector root -> criterion
        ax.plot([root_x, cx], [root_y - 4.0, crit_y + crit_h / 2],
                color=c_dark, linewidth=1.6, zorder=2,
                solid_capstyle="round")

    # ---- Sub-criteria (Tier 2) ----
    sub_y = 50
    sub_w, sub_h = 9.5, 9
    sub_gap_x = 0.8
    composite_y = 28
    leaf_w, leaf_h = 7.5, 5.5

    # Track all sub centers for edges
    all_sub_centers = []  # list of list of (cx, cy)

    for parent_idx, group in enumerate(SUBS):
        parent_cx = crit_xs[parent_idx]
        parent_color = CRITERIA[parent_idx][2]
        parent_light = CRITERIA[parent_idx][3]
        parent_dark = CRITERIA[parent_idx][4]
        n = len(group)

        # Horizontal span allocated to this criterion
        total_w = n * sub_w + (n - 1) * sub_gap_x
        start_x = parent_cx - total_w / 2 + sub_w / 2

        centers = []
        for k, (label, sub_w_val, anchor) in enumerate(group):
            cx = start_x + k * (sub_w + sub_gap_x)
            cy = sub_y

            _box(ax, cx, cy, sub_w, sub_h, label,
                 facecolor="white", edgecolor=parent_color, lw=1.4,
                 fontsize=8.6, fontweight="bold", text_color=parent_dark,
                 radius=0.05, zorder=4)

            # Sub-weight band (top stripe)
            import matplotlib.patches as mpatches
            stripe = mpatches.FancyBboxPatch(
                (cx - sub_w / 2 + 0.15, cy + sub_h / 2 - 1.6),
                sub_w - 0.30, 1.4,
                boxstyle="round,pad=0.005,rounding_size=0.025",
                facecolor=parent_light, edgecolor="none", zorder=5)
            ax.add_patch(stripe)
            ax.text(cx, cy + sub_h / 2 - 0.95,
                    f"local w = {sub_w_val:.2f}",
                    ha="center", va="center",
                    fontsize=8.0, fontweight="bold", color=parent_dark,
                    zorder=6)

            # Anchor evidence (italic, below box label)
            ax.text(cx, cy - sub_h / 2 + 0.7,
                    anchor,
                    ha="center", va="center",
                    fontsize=7.2, style="italic", color="#566573",
                    zorder=6)

            centers.append((cx, cy))

            # Connector criterion -> sub
            ax.plot([parent_cx, cx],
                    [crit_y - crit_h / 2, cy + sub_h / 2],
                    color=parent_color, linewidth=1.0, zorder=1,
                    alpha=0.85, solid_capstyle="round")

            # ---- Composite leaf (Tier 3) ----
            composite = CRITERIA[parent_idx][1] * sub_w_val
            _box(ax, cx, composite_y, leaf_w, leaf_h,
                 f"{composite:.3f}",
                 facecolor=parent_color, edgecolor=parent_dark, lw=1.4,
                 fontsize=15, fontweight="bold", text_color="white",
                 radius=0.08, zorder=4)
            ax.text(cx, composite_y - leaf_h / 2 - 1.4,
                    f"= {CRITERIA[parent_idx][1]:.2f} × {sub_w_val:.2f}",
                    ha="center", va="center",
                    fontsize=7.6, color="#566573", style="italic")

            # Connector sub -> composite
            ax.plot([cx, cx],
                    [cy - sub_h / 2, composite_y + leaf_h / 2],
                    color=parent_dark, linewidth=1.0, zorder=1,
                    linestyle=(0, (3, 2)))

        all_sub_centers.append(centers)

    # ---- Tier band labels on the left margin ----
    band_x = 5
    for y, lbl in [
        (root_y, "TIER 0\nObjective"),
        (crit_y, "TIER 1\nCriteria"),
        (sub_y, "TIER 2\nSub-criteria"),
        (composite_y, "TIER 3\nComposite\nweights"),
    ]:
        ax.text(band_x, y, lbl, ha="center", va="center",
                fontsize=9.2, fontweight="bold", color="#7F8C8D",
                bbox=dict(boxstyle="round,pad=0.5",
                          facecolor="#F2F4F4", edgecolor="#BDC3C7",
                          linewidth=0.6))

    # ---- Title + caption ----
    title_x = (LEFT_MARGIN + 130) / 2
    ax.text(title_x, 98.5,
            "Figure: AHP Decision Hierarchy for CampusRide v4.4 Design Objectives",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color="#1A1A1A")
    ax.text(title_x, 95.0,
            "Top-level weights elicited from F1-F6 prioritization "
            "(passenger WTP + driver tolerance asymmetry); "
            "sub-weights normalized within each criterion. "
            "Tier 3 leaves show composite weight = top × sub.",
            ha="center", va="center", fontsize=10.5, style="italic",
            color="#566573")

    # ---- Composite-weight summary band at bottom ----
    summary_y = 16
    ax.text(title_x, summary_y + 4.5,
            "Composite weights sum to 1.000 (Σ across all 10 leaves)",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color="#1A1A1A")

    # Mini horizontal bar of all 10 composites for at-a-glance compare
    composites = []
    for parent_idx, group in enumerate(SUBS):
        for label, sub_w_val, _ in group:
            composites.append((label.replace("\n", " "),
                               CRITERIA[parent_idx][1] * sub_w_val,
                               CRITERIA[parent_idx][2]))
    composites_sorted = sorted(composites, key=lambda x: -x[1])
    bar_x0 = LEFT_MARGIN + 5
    bar_y0 = 6
    bar_w_total = 130 - bar_x0 - 5
    cumulative = 0
    total = sum(c[1] for c in composites)
    for label, w, color in composites_sorted:
        seg_w = (w / total) * bar_w_total
        import matplotlib.patches as mpatches
        ax.add_patch(mpatches.Rectangle(
            (bar_x0 + cumulative, bar_y0), seg_w, 4.0,
            facecolor=color, edgecolor="white", linewidth=0.8, zorder=4))
        if seg_w > 4.5:
            ax.text(bar_x0 + cumulative + seg_w / 2, bar_y0 + 2.0,
                    f"{w:.3f}",
                    ha="center", va="center", fontsize=9,
                    fontweight="bold", color="white", zorder=5)
        cumulative += seg_w
    # Bar border
    ax.add_patch(mpatches.Rectangle(
        (bar_x0, bar_y0), bar_w_total, 4.0,
        facecolor="none", edgecolor="#34495E", linewidth=1.0, zorder=6))
    ax.text(bar_x0 + bar_w_total / 2, bar_y0 - 1.6,
            "(stacked bar of composite priorities, sorted descending)",
            ha="center", va="center", fontsize=8.5, style="italic",
            color="#566573")

    pdf, png = save_mpl("mbse_ahp_objectives")
    register("mbse_ahp_objectives", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
