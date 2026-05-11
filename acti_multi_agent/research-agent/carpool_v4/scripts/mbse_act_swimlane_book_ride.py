"""mbse_act_swimlane_book_ride — SysML activity view of the booking happy path.

Peer figure to c1: same booking activity, told in the SysML activity-diagram
dialect with explicit decisions, a parallel fork-join, and final nodes.
Three swim-lanes (Passenger, Platform, Driver) with a temporal axis at the
bottom. Implementation references are intentionally suppressed; cards read
as English sentences for HCI readers.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"


@renderer("mbse_act_swimlane_book_ride")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

    fig, ax = plt.subplots(figsize=(14, 6.8))

    # ------------------------------------------------------------------
    # Swim-lane y-coordinates
    # ------------------------------------------------------------------
    LANES = {
        "Passenger": (RIDER_COLOR, 4.0),
        "Platform":  (PLATFORM_COLOR, 2.5),
        "Driver":    (DRIVER_COLOR, 1.0),
    }
    LANE_HEIGHT = 1.15

    X_MIN, X_MAX = 0.0, 16.5

    # Lane bands
    for name, (color, y) in LANES.items():
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN, y - LANE_HEIGHT / 2),
                X_MAX - X_MIN, LANE_HEIGHT,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=0.07,
                edgecolor=color, linewidth=0.8,
            )
        )
        ax.text(
            X_MIN + 0.1, y, name,
            ha="left", va="center",
            fontsize=12, fontweight="bold",
            color=color,
        )

    # ------------------------------------------------------------------
    # Temporal markers along the bottom
    # ------------------------------------------------------------------
    TIMES = [
        (1.6,  "Start"),
        (4.6,  "Booking moment"),
        (8.7,  "Notification fan-out"),
        (11.6, "Trip-bound chat ready"),
        (14.6, "Activity ends"),
    ]
    y_axis = 0.10
    ax.plot([X_MIN + 0.4, X_MAX - 0.3], [y_axis, y_axis],
            color=NEUTRAL, linewidth=1.0)
    for x, lbl in TIMES:
        ax.plot([x, x], [y_axis - 0.05, y_axis + 0.05],
                color=NEUTRAL, linewidth=1.0)
        ax.text(x, y_axis - 0.18, lbl,
                ha="center", va="top", fontsize=9, color=NEUTRAL,
                style="italic")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=9.5,
             alpha=1.0, bold=False):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=color, linewidth=1.4, alpha=alpha,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
            wrap=True,
        )

    def diamond(x, y, w, h, text, color, *, fc="#FEF5E7", fs=9):
        # Decision diamond drawn as a rotated polygon
        from matplotlib.patches import Polygon
        pts = [(x, y + h / 2), (x + w / 2, y),
               (x, y - h / 2), (x - w / 2, y)]
        ax.add_patch(Polygon(pts, closed=True,
                             facecolor=fc, edgecolor=color, linewidth=1.4))
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fs, color="#1B2631", wrap=True)

    def fork_bar(x, y, w, color):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - 0.04), w, 0.08,
                boxstyle="round,pad=0.005",
                facecolor=color, edgecolor=color, linewidth=1.0,
            )
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.4, ls="-"):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=12,
            )
        )

    py = LANES["Passenger"][1]
    sy = LANES["Platform"][1]
    dy = LANES["Driver"][1]

    # ------------------------------------------------------------------
    # Initial nodes (filled disc) on Passenger lane
    # ------------------------------------------------------------------
    ax.add_patch(Circle((1.6, py), 0.13, facecolor=NEUTRAL,
                        edgecolor=NEUTRAL, zorder=3))

    # 1. Passenger requests booking
    card(3.2, py, 1.9, 0.55, "Request to join trip",
         RIDER_COLOR, bold=True)
    arrow(1.75, py, 2.25, py, NEUTRAL)

    # 2. Platform: check seats decision (diamond)
    diamond(4.6, sy, 1.7, 0.95,
            "Trip active &\nseats remaining?",
            PLATFORM_COLOR)
    arrow(3.5, py - 0.25, 4.25, sy + 0.45, RIDER_COLOR)

    # 3. Reserve seat
    card(6.7, sy, 2.0, 0.55,
         "Reserve seat for rider",
         PLATFORM_COLOR, bold=True)
    arrow(5.45, sy, 5.7, sy, PLATFORM_COLOR)
    ax.text(5.55, sy + 0.18, "yes", fontsize=8.5,
            color=PLATFORM_COLOR, ha="center")

    # 4. Last-seat decision
    diamond(8.6, sy, 1.4, 0.85,
            "Last seat\ntaken?", PLATFORM_COLOR, fs=8.5)
    arrow(7.7, sy, 7.95, sy, PLATFORM_COLOR)

    # 4a. Mark trip full (above lane, accent path)
    card(8.6, sy + 0.85, 2.1, 0.45,
         "Mark trip as full", PLATFORM_COLOR, fs=9)
    arrow(8.6, sy + 0.45, 8.6, sy + 0.6, PLATFORM_COLOR)
    ax.text(8.85, sy + 0.55, "yes", fontsize=8.5,
            color=PLATFORM_COLOR, ha="left")

    # ------------------------------------------------------------------
    # Parallel fork: confirmation to passenger + driver notification
    # ------------------------------------------------------------------
    fork_x = 9.7
    fork_bar(fork_x, sy, 1.0, "#1B2631")
    arrow(9.3, sy, fork_x - 0.5, sy, PLATFORM_COLOR)
    ax.text(9.45, sy - 0.18, "no", fontsize=8.5,
            color=PLATFORM_COLOR, ha="center")

    # Confirmation card on Passenger lane
    card(11.0, py, 2.1, 0.55,
         "Booking confirmation received", RIDER_COLOR)
    arrow(fork_x + 0.1, sy + 0.04, 10.4, py - 0.25, PLATFORM_COLOR)

    # Driver notification card on Driver lane
    card(11.0, dy, 2.3, 0.55,
         "New rider notified in real-time", DRIVER_COLOR)
    arrow(fork_x + 0.1, sy - 0.04, 10.4, dy + 0.25, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # Trip-bound chat (accent — non-obvious design choice)
    # ------------------------------------------------------------------
    card(12.5, sy, 2.4, 0.7,
         "Open trip-bound chat\n(expires shortly after trip)",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)
    arrow(11.65, sy, 11.4, sy, PLATFORM_COLOR)
    # Dashed taps to both lanes — chat is reachable from both sides
    arrow(12.5, sy + 0.35, 12.5, py - 0.25, ACCENT_COLOR, ls="--")
    arrow(12.5, sy - 0.35, 12.5, dy + 0.25, ACCENT_COLOR, ls="--")

    # ------------------------------------------------------------------
    # Join + activity-final nodes
    # ------------------------------------------------------------------
    join_x = 13.9
    fork_bar(join_x, sy, 0.9, "#1B2631")
    arrow(13.7, sy, join_x - 0.45, sy, PLATFORM_COLOR)

    # Final activity node on Platform lane (bullseye)
    final_x = 15.4
    ax.add_patch(Circle((final_x, sy), 0.18, facecolor="white",
                        edgecolor=NEUTRAL, linewidth=1.4, zorder=3))
    ax.add_patch(Circle((final_x, sy), 0.10, facecolor=NEUTRAL,
                        edgecolor=NEUTRAL, zorder=4))
    arrow(join_x + 0.45, sy, final_x - 0.22, sy, PLATFORM_COLOR)

    # Final nodes on rider + driver lanes
    ax.add_patch(Circle((final_x, py), 0.18, facecolor="white",
                        edgecolor=NEUTRAL, linewidth=1.4, zorder=3))
    ax.add_patch(Circle((final_x, py), 0.10, facecolor=NEUTRAL,
                        edgecolor=NEUTRAL, zorder=4))
    arrow(12.1, py, final_x - 0.22, py, RIDER_COLOR)

    ax.add_patch(Circle((final_x, dy), 0.18, facecolor="white",
                        edgecolor=NEUTRAL, linewidth=1.4, zorder=3))
    ax.add_patch(Circle((final_x, dy), 0.10, facecolor=NEUTRAL,
                        edgecolor=NEUTRAL, zorder=4))
    arrow(12.2, dy, final_x - 0.22, dy, DRIVER_COLOR)

    # ------------------------------------------------------------------
    # Snapshot annotation (findings — allowed)
    # ------------------------------------------------------------------
    ax.text(
        8.25, 5.05,
        "Activity diagram of the booking happy path: a fork issues "
        "rider confirmation and driver alert in parallel, then a single join "
        "closes the activity.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    ax.text(
        15.4, 0.10,
        "Snapshot: 184 verified riders, 16 ride pushes, driver subset N=19",
        ha="right", va="bottom", fontsize=8.5, color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    ax.set_title(
        "Booking activity across passenger, platform, and driver lanes",
        fontsize=14, fontweight="bold", pad=14,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.6, 5.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_act_swimlane_book_ride", dpi=300)
    register("mbse_act_swimlane_book_ride", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
