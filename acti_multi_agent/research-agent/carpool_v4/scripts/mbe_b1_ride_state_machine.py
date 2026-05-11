"""mbe_b1 — Trip + Booking state machines.

Two stacked UML-style state machines on one canvas:
  - Top cluster: Trip status lifecycle (active / full / completed / cancelled)
  - Bottom cluster: Booking status lifecycle (confirmed / cancelled)

A dashed cross-link shows that a confirmed booking can flip the trip to
`full` when it claims the last seat.

Paper-style: matplotlib only, no file/line references, no method names,
plain English transition labels.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


PLATFORM_COLOR = "#1A5276"   # navy — state borders
ACCENT_COLOR = "#F39C12"     # orange — cross-link

# Lighter alpha tints per state semantics
ACTIVE_FILL = "#D5F5E3"      # green-tint  (open / accepting)
FULL_FILL = "#FCF3CF"        # yellow-tint (saturated)
COMPLETED_FILL = "#D6EAF8"   # blue-tint   (final, success)
CANCELLED_FILL = "#FADBD8"   # red-tint    (final, abort)
CONFIRMED_FILL = "#D5F5E3"   # green-tint  (booking accepted)

NEUTRAL_GREY = "#566573"


@renderer("mbe_b1_ride_state_machine")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

    fig, ax = plt.subplots(figsize=(13, 7.8))

    X_MIN, X_MAX = 0.0, 13.0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def state(x, y, w, h, label, *, fill, border=PLATFORM_COLOR,
              terminal=False, bold=True, fs=10.5):
        """Rounded state box; if terminal, draw a thin outer ring (peripheries=2)."""
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fill, edgecolor=border, linewidth=1.6,
            )
        )
        if terminal:
            pad = 0.09
            ax.add_patch(
                FancyBboxPatch(
                    (x - w / 2 - pad, y - h / 2 - pad),
                    w + 2 * pad, h + 2 * pad,
                    boxstyle="round,pad=0.04",
                    facecolor="none", edgecolor=border, linewidth=1.0,
                )
            )
        ax.text(
            x, y, label,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
        )

    def initial_dot(x, y, color="#1B2631"):
        ax.add_patch(Circle((x, y), 0.13, facecolor=color, edgecolor=color))

    def arrow(x0, y0, x1, y1, *, color=PLATFORM_COLOR, ls="-",
              lw=1.5, rad=0.0, label=None, lx=None, ly=None,
              label_color=None, label_fs=9):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=14,
                connectionstyle=f"arc3,rad={rad}",
            )
        )
        if label is not None:
            if lx is None:
                lx = (x0 + x1) / 2
            if ly is None:
                ly = (y0 + y1) / 2
            ax.text(
                lx, ly, label,
                ha="center", va="center",
                fontsize=label_fs,
                color=label_color or color,
                bbox=dict(facecolor="white", edgecolor="none",
                          boxstyle="round,pad=0.18", alpha=0.9),
            )

    def cluster_band(y_center, height, label):
        """Soft background band for a cluster + left-side label."""
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN + 0.15, y_center - height / 2),
                X_MAX - X_MIN - 0.3, height,
                boxstyle="round,pad=0.02",
                facecolor=PLATFORM_COLOR, alpha=0.05,
                edgecolor=PLATFORM_COLOR, linewidth=0.8,
            )
        )
        ax.text(
            X_MIN + 0.35, y_center + height / 2 - 0.25,
            label,
            ha="left", va="top",
            fontsize=11, fontweight="bold",
            color=PLATFORM_COLOR, style="italic",
        )

    # ------------------------------------------------------------------
    # TOP cluster: Trip status
    # ------------------------------------------------------------------
    TOP_Y = 5.6
    TOP_H = 2.5
    cluster_band(TOP_Y, TOP_H, "Trip status  (driver-owned trip lifecycle)")

    # Layout (left → right)
    initial_dot(0.95, TOP_Y + 0.05)
    state(2.55, TOP_Y, 1.95, 0.85, "active\nseats remaining",
          fill=ACTIVE_FILL)
    state(5.30, TOP_Y, 1.65, 0.85, "full\nlast seat taken",
          fill=FULL_FILL)
    state(8.40, TOP_Y + 0.55, 1.85, 0.85, "completed",
          fill=COMPLETED_FILL, terminal=True)
    state(8.40, TOP_Y - 0.55, 1.85, 0.85, "cancelled",
          fill=CANCELLED_FILL, terminal=True)

    # Initial → active
    arrow(1.10, TOP_Y + 0.05, 1.60, TOP_Y,
          label="Driver creates trip",
          ly=TOP_Y + 0.32)

    # active → full  (last seat taken)
    arrow(3.55, TOP_Y, 4.50, TOP_Y,
          label="Last seat fills",
          ly=TOP_Y + 0.30)

    # full → completed
    arrow(6.15, TOP_Y + 0.15, 7.50, TOP_Y + 0.55,
          label="Driver marks complete",
          lx=6.85, ly=TOP_Y + 0.62)

    # active → cancelled  (curve down-right, well below `full` box)
    arrow(2.95, TOP_Y - 0.42, 7.45, TOP_Y - 0.60,
          rad=-0.30,
          label="Driver cancels  (before departure)",
          lx=4.80, ly=TOP_Y - 1.20)

    # full → cancelled  (short, downward-right)
    arrow(5.95, TOP_Y - 0.42, 7.45, TOP_Y - 0.55,
          rad=-0.05,
          label="Driver cancels",
          lx=6.75, ly=TOP_Y - 0.30)

    # ------------------------------------------------------------------
    # BOTTOM cluster: Booking status
    # ------------------------------------------------------------------
    BOT_Y = 1.5
    BOT_H = 1.9
    cluster_band(BOT_Y, BOT_H, "Booking status  (passenger-owned booking lifecycle)")

    initial_dot(0.95, BOT_Y)
    state(2.85, BOT_Y, 2.20, 0.85, "confirmed\non reservation",
          fill=CONFIRMED_FILL)
    state(8.40, BOT_Y, 2.10, 0.85, "cancelled",
          fill=CANCELLED_FILL, terminal=True)

    arrow(1.10, BOT_Y, 1.75, BOT_Y,
          label="Passenger reserves seat",
          ly=BOT_Y + 0.30)

    arrow(3.95, BOT_Y, 7.35, BOT_Y,
          label="Passenger or driver cancels  (before departure)",
          ly=BOT_Y + 0.30)

    # ------------------------------------------------------------------
    # Cross-link: confirmed booking → trip becomes full (when last seat)
    # ------------------------------------------------------------------
    arrow(
        3.55, BOT_Y + 0.45,                # from top-right of confirmed
        5.30, TOP_Y - 0.45,                # to bottom of full
        color=ACCENT_COLOR, ls="--", lw=1.8, rad=0.10,
        label=("If last seat: confirming a booking\n"
               "transitions the trip to full"),
        lx=2.55, ly=3.55, label_color=ACCENT_COLOR, label_fs=9.5,
    )

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Trip and booking state machines",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 7.35,
        "Two coupled lifecycles: a confirmed booking can flip the trip "
        "to full when it takes the last seat.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL_GREY,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.2, 7.7)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_b1_ride_state_machine", dpi=300)
    register("mbe_b1_ride_state_machine", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
