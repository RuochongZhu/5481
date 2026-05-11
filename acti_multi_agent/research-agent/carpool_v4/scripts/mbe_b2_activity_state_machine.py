"""mbe_b2 — Activity & Participant Lifecycles.

Two co-located state machines, paper-style:
  Top cluster:    Activity    (draft -> published -> ongoing -> completed | cancelled)
  Bottom cluster: Participant (registered -> checked-in | absent | no-show)

The participant transition into "checked-in" carries the two design gates
(check-in window and venue radius) as plain-English annotations; reward
earned on check-in. No code references, file paths, or column names.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, RIDER_COLOR, DRIVER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"
TERMINAL_GOOD = "#196F3D"   # checked-in (good terminal)
TERMINAL_NEU = "#7F8C8D"    # absent / cancelled (neutral terminal)
TERMINAL_BAD = "#922B21"    # no-show (bad terminal)


# Activity-cluster palette (re-uses b1 hues; live=blue lane, terminal greys/red)
ACTIVITY_LANE = RIDER_COLOR     # blue lane band
PARTICIPANT_LANE = DRIVER_COLOR  # red lane band — distinguishes from activity


@renderer("mbe_b2_activity_state_machine")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 8.2))

    X_MIN, X_MAX = 0.0, 16.5

    # ------------------------------------------------------------------
    # Cluster vertical layout
    #   Activity cluster:    y in [4.6, 7.4],   row centerline yA = 6.0
    #   Participant cluster: y in [0.6, 3.4],   row centerline yP = 2.0
    # ------------------------------------------------------------------
    yA = 6.0
    yP = 2.0
    BAND_HEIGHT = 2.8

    def lane_band(y_center, color, title, subtitle):
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN, y_center - BAND_HEIGHT / 2),
                X_MAX - X_MIN, BAND_HEIGHT,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=0.07,
                edgecolor=color, linewidth=0.8,
            )
        )
        ax.text(
            X_MIN + 0.15, y_center + BAND_HEIGHT / 2 - 0.22,
            title,
            ha="left", va="top",
            fontsize=12, fontweight="bold", color=color,
        )
        ax.text(
            X_MIN + 0.15, y_center + BAND_HEIGHT / 2 - 0.55,
            subtitle,
            ha="left", va="top",
            fontsize=9.5, style="italic", color=NEUTRAL,
        )

    lane_band(yA, ACTIVITY_LANE,
              "Activity lifecycle",
              "Organiser-owned event, advances on time and on demand.")
    lane_band(yP, PARTICIPANT_LANE,
              "Participant lifecycle",
              "Per-attendee outcome.")

    # ------------------------------------------------------------------
    # Helper: draw a state card (rounded box, white fill, colored edge)
    # ------------------------------------------------------------------
    def state(x, y, w, h, text, color, *, fc="white", fs=10.5,
              bold=True, terminal=False):
        # Outer ring for terminal states (UML "double border")
        if terminal:
            ax.add_patch(
                FancyBboxPatch(
                    (x - w / 2 - 0.07, y - h / 2 - 0.07),
                    w + 0.14, h + 0.14,
                    boxstyle="round,pad=0.04",
                    facecolor="none", edgecolor=color, linewidth=1.0,
                )
            )
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=color, linewidth=1.6,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
        )

    def init_dot(x, y, color="#1B2631"):
        ax.plot(x, y, marker="o", markersize=9,
                markerfacecolor=color, markeredgecolor=color)

    def arrow(x0, y0, x1, y1, color, *, lw=1.5, ls="-"):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=14,
                shrinkA=2, shrinkB=2,
            )
        )

    def edge_label(x, y, text, color, fs=8.8, italic=False, bg=True):
        if bg:
            ax.text(
                x, y, text,
                ha="center", va="center",
                fontsize=fs, color=color,
                style="italic" if italic else "normal",
                bbox=dict(boxstyle="round,pad=0.2",
                          facecolor="white", edgecolor="none", alpha=0.85),
            )
        else:
            ax.text(
                x, y, text,
                ha="center", va="center",
                fontsize=fs, color=color,
                style="italic" if italic else "normal",
            )

    # ==================================================================
    # ACTIVITY CLUSTER  (top)
    # ==================================================================
    # Horizontal layout: start dot -> draft -> published -> ongoing -> completed
    # Cancelled sits below the main row (fork from published / ongoing).
    A_y = yA + 0.25  # main horizontal row
    cancel_y = yA - 0.85

    init_dot(1.0, A_y, color=ACTIVITY_LANE)

    # State cards
    state(2.6, A_y, 1.7, 0.7, "draft", ACTIVITY_LANE, fc="#F4F6F7")
    state(5.4, A_y, 2.0, 0.7, "published", ACTIVITY_LANE, fc="#EBF5FB")
    state(8.6, A_y, 2.0, 0.7, "ongoing", ACTIVITY_LANE, fc="#D6EAF8")
    state(11.8, A_y, 2.0, 0.7, "completed", ACTIVITY_LANE,
          fc="#F4ECF7", terminal=True)
    state(8.6, cancel_y, 2.1, 0.7, "cancelled", TERMINAL_BAD,
          fc="#FDEDEC", terminal=True)

    # Forward edges
    arrow(1.18, A_y, 1.75, A_y, ACTIVITY_LANE)
    arrow(3.45, A_y, 4.4, A_y, ACTIVITY_LANE)
    edge_label(3.93, A_y + 0.32, "Organiser publishes",
               ACTIVITY_LANE)

    arrow(6.4, A_y, 7.6, A_y, ACTIVITY_LANE)
    edge_label(7.0, A_y + 0.32, "Start time reached",
               ACTIVITY_LANE)

    arrow(9.6, A_y, 10.8, A_y, ACTIVITY_LANE)
    edge_label(10.2, A_y + 0.32, "End time reached",
               ACTIVITY_LANE)

    # Cancellation edges (dashed, fork down to cancelled)
    arrow(5.4, A_y - 0.36, 8.0, cancel_y + 0.4,
          NEUTRAL, ls="--", lw=1.2)
    arrow(8.6, A_y - 0.36, 8.6, cancel_y + 0.4,
          NEUTRAL, ls="--", lw=1.2)
    edge_label(6.6, (A_y + cancel_y) / 2 - 0.15,
               "Organiser cancels", NEUTRAL, italic=True)

    # ==================================================================
    # PARTICIPANT CLUSTER  (bottom)
    # ==================================================================
    P_y = yP + 0.15

    init_dot(1.0, P_y, color=PARTICIPANT_LANE)

    state(2.6, P_y, 1.9, 0.7, "registered", PARTICIPANT_LANE, fc="#FDEBD0")
    state(8.6, P_y + 0.85, 2.5, 0.85,
          "checked-in\n(reward earned)", TERMINAL_GOOD,
          fc="#E9F7EF", fs=10.0, terminal=True)
    state(8.6, P_y - 1.0, 2.1, 0.7,
          "absent", TERMINAL_NEU, fc="#F4F6F7", terminal=True)
    state(12.5, P_y - 1.0, 2.1, 0.7,
          "no-show", TERMINAL_BAD, fc="#FDEDEC", terminal=True)

    # registered <- start
    arrow(1.18, P_y, 1.65, P_y, PARTICIPANT_LANE)
    edge_label(1.4, P_y - 0.42, "Sign-up",
               PARTICIPANT_LANE, fs=8.6, bg=False)

    # registered -> checked-in (the load-bearing transition)
    arrow(3.6, P_y + 0.15, 7.3, P_y + 0.7,
          TERMINAL_GOOD, lw=2.0)

    # Two design-parameter gates, plain English, on the gated edge.
    # Place them stacked above the slanted arrow so neither overlaps the
    # registered card or the lane subtitle.
    gate_x = 5.6
    gate_y_top = P_y + 1.55
    gate_y_bot = P_y + 0.85

    ax.text(
        gate_x, gate_y_top,
        "Within check-in window\n(design parameter: ~ +/- 30 min)",
        ha="center", va="center", fontsize=8.6,
        color=ACCENT_COLOR, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25",
                  facecolor="#FEF5E7", edgecolor=ACCENT_COLOR,
                  linewidth=1.0),
    )
    ax.text(
        gate_x, gate_y_bot,
        "At venue\n(design parameter: within ~ 100 m)",
        ha="center", va="center", fontsize=8.6,
        color=ACCENT_COLOR, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25",
                  facecolor="#FEF5E7", edgecolor=ACCENT_COLOR,
                  linewidth=1.0),
    )
    edge_label(7.05, P_y + 0.30, "Awards small reward",
               TERMINAL_GOOD, fs=8.8, italic=True)

    # registered -> absent  (organiser-marked, dashed)
    arrow(3.6, P_y - 0.18, 7.55, P_y - 0.95,
          NEUTRAL, ls="--", lw=1.3)
    edge_label(5.4, P_y - 0.65, "Organiser marks absent",
               NEUTRAL, fs=8.6, italic=True)

    # registered -> no-show  (auto on activity completion)
    arrow(3.6, P_y - 0.05, 11.45, P_y - 0.95,
          NEUTRAL, ls=":", lw=1.3)
    edge_label(8.0, P_y - 1.4,
               "Auto-resolved when activity completes  (no check-in recorded)",
               NEUTRAL, fs=8.6, italic=True)

    # ==================================================================
    # Cross-cluster contextual link (activity completes -> no-show fires)
    # ==================================================================
    arrow(11.8, A_y - 0.36, 12.5, P_y - 0.62,
          NEUTRAL, ls=":", lw=1.0)
    edge_label(13.3, (A_y + (P_y - 0.4)) / 2,
               "On activity end:\nunchecked  ->  no-show",
               NEUTRAL, fs=8.4, italic=True)

    # ==================================================================
    # Title + subtitle
    # ==================================================================
    ax.set_title(
        "Activity and participant lifecycles",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 8.0,
        "Two co-located state machines; check-in is gated by a time "
        "window and a venue radius, and a successful check-in awards a "
        "small reward.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.4, 8.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_b2_activity_state_machine", dpi=300)
    register("mbe_b2_activity_state_machine", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
