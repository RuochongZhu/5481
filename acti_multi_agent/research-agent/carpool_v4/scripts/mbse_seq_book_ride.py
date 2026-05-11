"""mbse_seq_book_ride — SysML Sequence Diagram for the booking interaction.

Three horizontal swim-lanes (Passenger / Platform / Driver). Time flows
left-to-right. Solid arrows = synchronous request; dashed arrows =
asynchronous notification or return. Cards on each lane describe what the
actor does at that temporal position; no implementation references.
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
GREY = "#566573"


@renderer("mbse_seq_book_ride")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(15.5, 6.8))

    # ------------------------------------------------------------------
    # Swim-lanes (horizontal). Passenger top, Platform middle, Driver bottom.
    # ------------------------------------------------------------------
    LANES = {
        "Passenger": (RIDER_COLOR,    4.0),
        "Platform":  (PLATFORM_COLOR, 2.5),
        "Driver":    (DRIVER_COLOR,   1.0),
    }
    LANE_HEIGHT = 1.1

    X_MIN, X_MAX = 0.0, 18.5
    LABEL_RIGHT = 1.6  # right edge of the lane-label strip

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
            X_MIN + 0.15, y, name,
            ha="left", va="center",
            fontsize=12, fontweight="bold",
            color=color,
        )

    # ------------------------------------------------------------------
    # Time axis along the bottom, anchored to action x-positions
    # ------------------------------------------------------------------
    TIMES = [
        (3.2,  "Booking moment"),
        (7.6,  "Seat reserved"),
        (10.2, "Both sides confirmed"),
        (12.8, "Trip happens"),
        (16.5, "Post-trip window"),
    ]
    y_axis = 0.05
    ax.plot([X_MIN + 0.4, X_MAX - 0.3], [y_axis, y_axis],
            color=GREY, linewidth=1.0)
    for x, lbl in TIMES:
        ax.plot([x, x], [y_axis - 0.05, y_axis + 0.05],
                color=GREY, linewidth=1.0)
        ax.text(x, y_axis - 0.18, lbl,
                ha="center", va="top", fontsize=9, color=GREY,
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
    # 1. Passenger requests to join trip (sync request)
    # ------------------------------------------------------------------
    card(3.2, py, 1.9, 0.55, "Request to join trip",
         RIDER_COLOR, bold=True)
    arrow(3.2, py - 0.28, 3.7, sy + 0.30, RIDER_COLOR)

    # ------------------------------------------------------------------
    # 2. Platform: validate seat availability and reserve
    # ------------------------------------------------------------------
    card(5.1, sy, 2.4, 0.65,
         "Check seats remaining\nand reserve one",
         PLATFORM_COLOR, bold=True)

    # ------------------------------------------------------------------
    # 3. Conflict branch (dashed = error return) — annotated above lane
    # ------------------------------------------------------------------
    arrow(5.1, sy + 0.33, 5.1, py - 0.28, ACCENT_COLOR, ls="--")
    ax.text(
        5.35, (sy + py) / 2 + 0.05,
        "if full:\nseat unavailable",
        ha="left", va="center", fontsize=8.5, style="italic",
        color=ACCENT_COLOR,
    )

    # ------------------------------------------------------------------
    # 4. Booking record created + mark trip as full when last seat taken
    # ------------------------------------------------------------------
    card(7.6, sy, 2.2, 0.65,
         "Booking record created\n(mark trip full if last seat)",
         PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # 5. Confirmation back to passenger (dashed = async return)
    # ------------------------------------------------------------------
    card(10.0, py, 2.0, 0.55, "Booking confirmed", RIDER_COLOR)
    arrow(8.2, sy + 0.33, 9.6, py - 0.28, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # 6. Driver notified of new rider (dashed = async push)
    # ------------------------------------------------------------------
    card(10.0, dy, 2.0, 0.55, "New rider notified", DRIVER_COLOR)
    arrow(8.2, sy - 0.33, 9.6, dy + 0.28, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # 7. Trip-bound chat opened — async to both sides
    # ------------------------------------------------------------------
    card(12.6, sy, 2.3, 0.65,
         "Trip-bound chat opened\n(expires after trip)",
         PLATFORM_COLOR)
    arrow(12.6, sy + 0.33, 12.6, py - 0.28, PLATFORM_COLOR, ls="--")
    arrow(12.6, sy - 0.33, 12.6, dy + 0.28, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # 8. Rating window — accent callout at the post-trip position
    # ------------------------------------------------------------------
    card(15.4, sy, 2.4, 0.65,
         "Rating window opens\n2 hours after trip ends",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)
    ax.plot([15.4, 15.4], [y_axis + 0.05, sy - 0.45],
            linestyle=":", color=ACCENT_COLOR, linewidth=1.0)

    # ------------------------------------------------------------------
    # 9. Both sides receive a tap-to-rate prompt (async)
    # ------------------------------------------------------------------
    card(17.6, py, 1.5, 0.55,
         "Tap-to-rate\ndriver", RIDER_COLOR, fs=9)
    card(17.6, dy, 1.5, 0.55,
         "Tap-to-rate\npassenger", DRIVER_COLOR, fs=9)
    arrow(16.7, sy + 0.33, 17.1, py - 0.28, ACCENT_COLOR, ls="--")
    arrow(16.7, sy - 0.33, 17.1, dy + 0.28, ACCENT_COLOR, ls="--")

    # ------------------------------------------------------------------
    # Title + italic subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Booking interaction across passenger, platform, and driver",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 5.05,
        "Sequence as horizontal swim-lanes; solid arrows are synchronous "
        "requests, dashed arrows are asynchronous confirmations or pushes.",
        ha="center", va="center", fontsize=10, style="italic",
        color=GREY,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.6, 5.3)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_seq_book_ride", dpi=300)
    register("mbse_seq_book_ride", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
