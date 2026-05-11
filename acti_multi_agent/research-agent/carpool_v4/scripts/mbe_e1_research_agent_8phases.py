"""mbe_e1 — Research-Agent 8-Phase Pipeline (paper figure).

A horizontal block diagram of the thesis-conditioned evidence pipeline used
to ground the CampusRide paper. The diagram emphasizes the methodological
contribution: an eight-phase, two-tier reading workflow that ends in a
five-reviewer evaluation with a principled auto-backtrack rule.

Design choices:
  - matplotlib (not graphviz): a clean LR pipeline with phase cards.
  - Phases colored by tier: fast tier (light blue) for high-volume reading
    and bookkeeping; deep tier (light purple) for relational and
    evaluative phases.
  - External corpus sources fan in from the left into Phase 1.
  - Phase 5 routes a red dashed auto-backtrack arrow back to {P3.5, P3.7,
    P4} when overall < 0.85 or honesty < 0.80.
  - A small footnote box lists the state invariants at concept level.
  - Italic subtitle states the design intent in one sentence.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


# Tier and accent palette
FAST_FILL = "#D6EAF8"      # light blue (fast tier)
FAST_BORDER = "#2874A6"
DEEP_FILL = "#E8DAEF"      # light purple (deep tier)
DEEP_BORDER = "#7D3C98"
SOURCE_FILL = "#D5F5E3"    # light green for external sources
SOURCE_BORDER = "#229954"
INVAR_FILL = "#FCF3CF"     # light yellow for invariants box
INVAR_BORDER = "#B7950B"
BACKTRACK = "#C0392B"      # red dashed for auto-backtrack
NEUTRAL = "#566573"
INK = "#1B2631"


@renderer("mbe_e1_research_agent_8phases")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(20.0, 7.6))

    # ------------------------------------------------------------------
    # Layout grid
    # ------------------------------------------------------------------
    # Phase cards arranged left-to-right on a single row.
    PHASE_Y = 4.2
    CARD_W = 2.55
    CARD_H = 1.65

    # x-centers for the eight phase cards (start at x=4 to leave room for
    # the source cluster on the left, then evenly space ~2.85 apart).
    PHASE_X = [4.0, 6.85, 9.70, 12.55, 15.40, 18.25, 21.10, 23.95]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, title, body, fill, border, *, title_fs=10.5,
             body_fs=8.8, tier_tag=None):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fill, edgecolor=border, linewidth=1.5,
            )
        )
        ax.text(x, y + h / 2 - 0.22, title,
                ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=INK)
        ax.text(x, y - 0.05, body,
                ha="center", va="center",
                fontsize=body_fs, color=INK)
        if tier_tag is not None:
            ax.text(x, y - h / 2 + 0.18, tier_tag,
                    ha="center", va="center",
                    fontsize=8, style="italic", color=border)

    def arrow(x0, y0, x1, y1, color, *, lw=1.6, ls="-",
              style="-|>", mut=14, alpha=1.0):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle=style, color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=mut, alpha=alpha,
            )
        )

    # ------------------------------------------------------------------
    # External corpus sources (fan-in into P1)
    # ------------------------------------------------------------------
    SRC_X = 0.95
    src_names = ["OpenAlex", "Semantic Scholar", "arXiv", "Lens", "Crossref"]
    src_y_top, src_y_bot = 5.85, 2.55
    n = len(src_names)
    src_ys = [src_y_top - i * (src_y_top - src_y_bot) / (n - 1)
              for i in range(n)]

    # Sources cluster band
    ax.add_patch(
        FancyBboxPatch(
            (SRC_X - 0.95, src_y_bot - 0.45),
            1.95, (src_y_top - src_y_bot) + 0.9,
            boxstyle="round,pad=0.04",
            facecolor=SOURCE_FILL, edgecolor=SOURCE_BORDER,
            linewidth=1.0, alpha=0.45,
        )
    )
    ax.text(SRC_X, src_y_top + 0.55,
            "External corpus\nsources",
            ha="center", va="center",
            fontsize=10, fontweight="bold", color=SOURCE_BORDER)

    for name, y in zip(src_names, src_ys):
        ax.add_patch(
            FancyBboxPatch(
                (SRC_X - 0.85, y - 0.22), 1.7, 0.44,
                boxstyle="round,pad=0.03",
                facecolor="white", edgecolor=SOURCE_BORDER, linewidth=1.1,
            )
        )
        ax.text(SRC_X, y, name, ha="center", va="center",
                fontsize=9.2, color=INK)

    # Fan-in arrows: each source -> P1's left edge
    p1_left_x = PHASE_X[0] - CARD_W / 2
    for y in src_ys:
        arrow(SRC_X + 0.85, y, p1_left_x - 0.05, PHASE_Y,
              SOURCE_BORDER, lw=1.0, mut=10, alpha=0.85)

    # ------------------------------------------------------------------
    # Eight phase cards
    # ------------------------------------------------------------------
    PHASES = [
        ("P1",  "Corpus Assembly",
         "Merge external sources\ninto a deduplicated\ncorpus snapshot",
         "fast"),
        ("P2",  "Classification",
         "Assign one of ten\ncategories per paper;\nflag low confidence",
         "fast"),
        ("P2.5", "Deep Extraction",
         "Pull seven structured\nfields from each paper\n(claim, methods, ...)",
         "fast"),
        ("P3",  "Relationship Graph",
         "Edges across papers:\noverlap, mirror,\nsuccession, conflict",
         "deep"),
        ("P3.5", "Narrative Chain",
         "Seven beats; spine in\ncitation order; one\npaper per beat",
         "deep"),
        ("P3.7", "Contradiction Map",
         "Genuine disagreements\nonly; severity tagged;\nbeat-attributed",
         "deep"),
        ("P4",  "Evidence Inventory",
         "Cross-reference findings\nagainst supporting\ncitations",
         "fast"),
        ("P5",  "Five-Reviewer Eval",
         "Narrative / Coverage /\nGap / Contradiction /\nHonesty",
         "deep"),
    ]

    for (code, name, body, tier), x in zip(PHASES, PHASE_X):
        if tier == "fast":
            fill, border = FAST_FILL, FAST_BORDER
            tag = "fast tier"
        else:
            fill, border = DEEP_FILL, DEEP_BORDER
            tag = "deep tier"
        title = f"{code}  {name}"
        card(x, PHASE_Y, CARD_W, CARD_H, title, body, fill, border,
             tier_tag=tag)

    # ------------------------------------------------------------------
    # LR chain arrows P1 -> P2 -> ... -> P5
    # ------------------------------------------------------------------
    for i in range(len(PHASE_X) - 1):
        x0 = PHASE_X[i] + CARD_W / 2
        x1 = PHASE_X[i + 1] - CARD_W / 2
        arrow(x0 + 0.02, PHASE_Y, x1 - 0.02, PHASE_Y,
              "#34495E", lw=1.8, mut=14)

    # ------------------------------------------------------------------
    # Auto-backtrack arrows from P5 back to P3.5, P3.7, P4
    # Routed below the row to avoid overlapping the forward chain.
    # ------------------------------------------------------------------
    p5_x = PHASE_X[7]
    p5_bottom = PHASE_Y - CARD_H / 2
    bt_y = 2.3  # backtrack channel y

    targets = [
        (PHASE_X[4], "weakest = Narrative"),                 # P3.5
        (PHASE_X[5], "weakest = Contradiction"),             # P3.7
        (PHASE_X[6], "honesty < 0.80\nor weakest = Coverage / Gap"),  # P4
    ]

    # P5 down stub
    arrow(p5_x, p5_bottom - 0.02, p5_x, bt_y + 0.02,
          BACKTRACK, lw=1.7, ls="--", mut=10)

    # Horizontal channel from P5 leftward
    leftmost_target = min(t[0] for t in targets)
    ax.plot([leftmost_target, p5_x], [bt_y, bt_y],
            color=BACKTRACK, linewidth=1.7, linestyle=(0, (5, 4)))

    # Up stubs into each target
    for tx, label in targets:
        target_bottom = PHASE_Y - CARD_H / 2
        arrow(tx, bt_y + 0.02, tx, target_bottom - 0.04,
              BACKTRACK, lw=1.7, ls="--", mut=12)
        ax.text(tx, bt_y - 0.32, label,
                ha="center", va="top",
                fontsize=8.4, color=BACKTRACK, style="italic")

    # Backtrack rule label near the channel
    ax.text((leftmost_target + p5_x) / 2, bt_y + 0.22,
            "Auto-backtrack: overall < 0.85  or  honesty < 0.80",
            ha="center", va="bottom",
            fontsize=9.4, fontweight="bold", color=BACKTRACK)

    # ------------------------------------------------------------------
    # State invariants footnote (small box bottom-right)
    # ------------------------------------------------------------------
    inv_x, inv_y, inv_w, inv_h = 19.4, 0.55, 8.2, 1.2
    ax.add_patch(
        FancyBboxPatch(
            (inv_x - inv_w / 2, inv_y - inv_h / 2), inv_w, inv_h,
            boxstyle="round,pad=0.05",
            facecolor=INVAR_FILL, edgecolor=INVAR_BORDER, linewidth=1.2,
        )
    )
    ax.text(inv_x, inv_y + inv_h / 2 - 0.20,
            "State invariants",
            ha="center", va="center",
            fontsize=10, fontweight="bold", color=INVAR_BORDER)
    inv_lines = (
        "Append-only corpus  -  papers are never removed\n"
        "Pruned papers stay in the snapshot but are filtered downstream\n"
        "Reviewer disagreement above threshold pauses the loop for human review"
    )
    ax.text(inv_x, inv_y - 0.10, inv_lines,
            ha="center", va="center",
            fontsize=8.7, color=INK)

    # ------------------------------------------------------------------
    # Tier legend (bottom-left)
    # ------------------------------------------------------------------
    leg_x, leg_y, leg_w, leg_h = 6.5, 0.55, 10.6, 1.2
    ax.add_patch(
        FancyBboxPatch(
            (leg_x - leg_w / 2, leg_y - leg_h / 2), leg_w, leg_h,
            boxstyle="round,pad=0.05",
            facecolor="#F8F9F9", edgecolor=NEUTRAL, linewidth=1.0,
        )
    )
    ax.text(leg_x, leg_y + leg_h / 2 - 0.20,
            "Legend",
            ha="center", va="center",
            fontsize=10, fontweight="bold", color=NEUTRAL)

    # Legend swatches
    sw_y = leg_y - 0.10
    sw_w, sw_h = 0.32, 0.22

    def swatch(cx, color, edge, label):
        ax.add_patch(
            FancyBboxPatch(
                (cx - sw_w / 2, sw_y - sw_h / 2), sw_w, sw_h,
                boxstyle="round,pad=0.02",
                facecolor=color, edgecolor=edge, linewidth=1.2,
            )
        )
        ax.text(cx + sw_w / 2 + 0.1, sw_y, label,
                ha="left", va="center", fontsize=8.8, color=INK)

    swatch(leg_x - 4.85, FAST_FILL, FAST_BORDER,
           "fast tier (high-volume reading)")
    swatch(leg_x - 0.85, DEEP_FILL, DEEP_BORDER,
           "deep tier (relational / evaluative)")
    # Dashed line example
    ax.plot([leg_x + 3.10, leg_x + 3.65], [sw_y, sw_y],
            color=BACKTRACK, linewidth=1.7, linestyle=(0, (5, 4)))
    ax.text(leg_x + 3.75, sw_y, "auto-backtrack",
            ha="left", va="center", fontsize=8.8, color=INK)

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Research-Agent: an eight-phase, thesis-conditioned evidence pipeline",
        fontsize=14, fontweight="bold", pad=16,
    )
    ax.text(
        14.0, 6.95,
        "Reviewer disagreement triggers human-in-loop, not silent override.",
        ha="center", va="center",
        fontsize=11, style="italic", color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Axis cosmetics
    # ------------------------------------------------------------------
    ax.set_xlim(-0.4, 25.6)
    ax.set_ylim(-0.3, 7.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_e1_research_agent_8phases", dpi=300)
    register("mbe_e1_research_agent_8phases", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
