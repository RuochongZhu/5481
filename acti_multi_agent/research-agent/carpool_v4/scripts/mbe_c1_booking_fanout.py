"""mbe_c1 — What happens when a passenger books a trip.

A systems-level interaction diagram, not an engineering call-graph. Three
swim-lanes (Passenger, Platform, Driver) and a temporal axis to the right.

Design principles (applies to the whole `mbe_*` set after pivot):
  - No file/line references, no SQL, no programming-language artifacts.
  - User-facing outcomes only; implementation detail collapsed into platform
    actions.
  - Highlight one or two non-obvious design choices (here: rating window
    deferred 2 hours, trip-bound chat instead of permanent groups).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"  # for the deferred-rating callout


@renderer("mbe_c1_booking_fanout")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 6.5))

    # ------------------------------------------------------------------
    # Swim-lane y-coordinates
    # ------------------------------------------------------------------
    LANES = {
        "Passenger": (RIDER_COLOR, 4.0),
        "Platform":  (PLATFORM_COLOR, 2.5),
        "Driver":    (DRIVER_COLOR, 1.0),
    }
    LANE_HEIGHT = 1.1

    # Horizontal canvas extent. We reserve an x<1.4 strip for lane labels.
    X_MIN, X_MAX = 0.0, 16.5
    LABEL_RIGHT = 1.4  # right edge of the lane-label strip

    # Draw lane bands
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
    # Temporal markers along the bottom (anchored to action x-positions)
    # ------------------------------------------------------------------
    TIMES = [
        (4.5,  "Booking moment"),
        (9.8,  "Trip happens"),
        (11.7, "Trip + 2 hours"),
        (14.5, "(rating remains revisable)"),
    ]
    y_axis = 0.05
    ax.plot([X_MIN + 0.4, X_MAX - 0.3], [y_axis, y_axis],
            color="#566573", linewidth=1.0)
    for x, lbl in TIMES:
        ax.plot([x, x], [y_axis - 0.05, y_axis + 0.05],
                color="#566573", linewidth=1.0)
        ax.text(x, y_axis - 0.18, lbl,
                ha="center", va="top", fontsize=9, color="#566573",
                style="italic")

    # ------------------------------------------------------------------
    # Helper: draw an action card
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

    def arrow(x0, y0, x1, y1, color, *, style="-|>", lw=1.4, ls="-"):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle=style, color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=12,
            )
        )

    # ------------------------------------------------------------------
    # The action cards
    # ------------------------------------------------------------------
    py = LANES["Passenger"][1]
    sy = LANES["Platform"][1]
    dy = LANES["Driver"][1]

    # All five booking-cluster cards happen synchronously at "Booking moment".
    # Cards 6/7 happen later, at "Trip + 2 hours" and beyond.

    # 1. Passenger requests booking
    card(2.5, py, 1.7, 0.55, "Request to join trip",
         RIDER_COLOR, bold=True)

    # 2. Platform: reserve seat (and possibly close trip)
    card(4.4, sy, 2.2, 0.6,
         "Reserve seat\n(close trip if last seat)",
         PLATFORM_COLOR, bold=True)
    arrow(3.35, py - 0.2, 3.9, sy + 0.25, RIDER_COLOR)

    # 3. Confirmation to passenger
    card(6.5, py, 1.9, 0.55, "Booking confirmed", RIDER_COLOR)
    arrow(4.95, sy + 0.25, 5.95, py - 0.2, PLATFORM_COLOR)

    # 4. Notify driver
    card(6.5, dy, 1.9, 0.55, "New rider notified", DRIVER_COLOR)
    arrow(4.95, sy - 0.25, 5.95, dy + 0.2, PLATFORM_COLOR)

    # 5. Trip-bound chat opened
    card(8.7, sy, 2.4, 0.65,
         "Trip-bound chat opened\n(expires 1 h after trip)",
         PLATFORM_COLOR)
    arrow(8.7, sy + 0.33, 8.7, py - 0.25, PLATFORM_COLOR, ls="--")
    arrow(8.7, sy - 0.33, 8.7, dy + 0.25, PLATFORM_COLOR, ls="--")

    # 6. Rating window deferred — accent callout (much later in time)
    card(11.7, sy, 2.4, 0.65,
         "Rating window opens\n2 hours after trip ends",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)
    ax.plot([11.7, 11.7], [y_axis + 0.05, sy - 0.45],
            linestyle=":", color=ACCENT_COLOR, linewidth=1.0)

    # 7. Both sides receive a tap-to-rate prompt
    card(14.5, py, 2.4, 0.6,
         "Tap-to-rate prompt\n(passenger rates driver)", RIDER_COLOR)
    card(14.5, dy, 2.4, 0.6,
         "Tap-to-rate prompt\n(driver rates passenger)", DRIVER_COLOR)
    arrow(12.95, sy + 0.25, 13.3, py - 0.22, ACCENT_COLOR)
    arrow(12.95, sy - 0.25, 13.3, dy + 0.22, ACCENT_COLOR)

    # ------------------------------------------------------------------
    # Title + caption strip
    # ------------------------------------------------------------------
    ax.set_title(
        "What happens when a passenger books a trip",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        8.5, 5.05,
        "Bidirectional rating; the post-trip window is deferred by design "
        "to remove the in-vehicle rating moment.",
        ha="center", va="center", fontsize=10, style="italic",
        color="#566573",
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.6, 5.3)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_c1_booking_fanout", dpi=300)
    register("mbe_c1_booking_fanout", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
