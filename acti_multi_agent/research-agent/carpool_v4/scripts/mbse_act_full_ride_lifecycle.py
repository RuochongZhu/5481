"""mbse_act_full_ride_lifecycle — Full ride lifecycle as an activity diagram.

A SysML-flavored activity view across three swim-lanes (Driver / Platform /
Passenger). This is the longer-timeline counterpart to c1: where c1 zooms
into the booking moment, this figure stretches across the whole ride
(publish -> list -> book -> meet -> trip -> rate -> close).

Design principles (shared with the unified mbe / mbse style):
  - matplotlib only; no graphviz code-language artifacts.
  - User-facing outcomes only; engineering machinery is collapsed away.
  - Snapshot numbers (184 verified members, 16/82 pushes) are kept as
    findings, not as implementation notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"   # orange — design highlights (deferred rating)
GREY = "#566573"


@renderer("mbse_act_full_ride_lifecycle")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(16, 7.0))

    # ------------------------------------------------------------------
    # Swim-lane y-coordinates
    # ------------------------------------------------------------------
    LANES = {
        "Driver":    (DRIVER_COLOR, 4.0),
        "Platform":  (PLATFORM_COLOR, 2.5),
        "Passenger": (RIDER_COLOR, 1.0),
    }
    LANE_HEIGHT = 1.15

    X_MIN, X_MAX = 0.0, 19.0
    LABEL_RIGHT = 1.4

    # Lane bands + labels
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
    # Temporal axis along the bottom
    # ------------------------------------------------------------------
    PHASES = [
        (2.5,  "Trip published"),
        (5.0,  "Listed in feed"),
        (7.5,  "Booking moment"),
        (10.0, "Pre-trip coordination"),
        (12.5, "Trip happens"),
        (15.0, "Trip + 2 hours"),
        (17.5, "Trip closed"),
    ]
    y_axis = 0.05
    ax.plot([X_MIN + 0.4, X_MAX - 0.3], [y_axis, y_axis],
            color=GREY, linewidth=1.0)
    for x, lbl in PHASES:
        ax.plot([x, x], [y_axis - 0.05, y_axis + 0.05],
                color=GREY, linewidth=1.0)
        ax.text(x, y_axis - 0.20, lbl,
                ha="center", va="top", fontsize=9, color=GREY,
                style="italic")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=9.2,
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

    dy_ = LANES["Driver"][1]
    sy_ = LANES["Platform"][1]
    py_ = LANES["Passenger"][1]

    # ------------------------------------------------------------------
    # Phase 1 — Trip published (Driver -> Platform)
    # ------------------------------------------------------------------
    card(2.5, dy_, 2.0, 0.55, "Driver publishes trip",
         DRIVER_COLOR, bold=True)
    card(2.5, sy_, 2.2, 0.65,
         "Trip recorded\n(184 verified members eligible)",
         PLATFORM_COLOR)
    arrow(2.5, dy_ - 0.28, 2.5, sy_ + 0.33, DRIVER_COLOR)

    # ------------------------------------------------------------------
    # Phase 2 — Listed in feed + external outreach
    # ------------------------------------------------------------------
    card(5.0, sy_, 2.4, 0.65,
         "Trip appears in feed\n+ external outreach queue\n(16 of 82 pushes sent)",
         PLATFORM_COLOR)
    card(5.0, py_, 2.0, 0.55, "Riders browse feed",
         RIDER_COLOR)
    arrow(3.7, sy_, 3.8, sy_, PLATFORM_COLOR)
    arrow(5.0, sy_ - 0.33, 5.0, py_ + 0.28, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # Phase 3 — Booking moment (the c1-zoom)
    # ------------------------------------------------------------------
    card(7.5, py_, 1.9, 0.55, "Request to join trip",
         RIDER_COLOR, bold=True)
    card(7.5, sy_, 2.4, 0.65,
         "Reserve seat\n(close trip if last seat)",
         PLATFORM_COLOR, bold=True)
    arrow(7.5, py_ + 0.28, 7.5, sy_ - 0.33, RIDER_COLOR)

    # Confirmation back to passenger + driver gets notified
    card(8.7, py_, 1.7, 0.5, "Booking confirmed",
         RIDER_COLOR, fs=8.8)
    card(8.7, dy_, 1.7, 0.5, "New rider notified",
         DRIVER_COLOR, fs=8.8)
    arrow(8.4, sy_ + 0.33, 8.55, dy_ - 0.25, PLATFORM_COLOR)
    arrow(8.4, sy_ - 0.33, 8.55, py_ + 0.25, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # Phase 4 — Pre-trip coordination (chat opened, departure approach)
    # ------------------------------------------------------------------
    card(10.0, sy_, 2.6, 0.7,
         "Trip-bound chat opened\n(expires 1 h after trip)",
         PLATFORM_COLOR)
    arrow(10.0, sy_ + 0.36, 10.0, dy_ - 0.28, PLATFORM_COLOR, ls="--")
    arrow(10.0, sy_ - 0.36, 10.0, py_ + 0.28, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # Phase 5 — Trip happens (driver picks up, ride completes)
    # ------------------------------------------------------------------
    card(12.5, dy_, 2.0, 0.55, "Pick up & drive",
         DRIVER_COLOR, bold=True)
    card(12.5, py_, 2.0, 0.55, "Ride completed",
         RIDER_COLOR)
    card(12.5, sy_, 2.2, 0.6, "Trip marked complete",
         PLATFORM_COLOR)
    arrow(12.5, dy_ - 0.28, 12.5, sy_ + 0.30, DRIVER_COLOR)
    arrow(12.5, sy_ - 0.30, 12.5, py_ + 0.28, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # Phase 6 — Deferred rating window (accent callout)
    # ------------------------------------------------------------------
    card(15.0, sy_, 2.6, 0.7,
         "Rating window opens\n2 hours after trip ends",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)
    ax.plot([15.0, 15.0], [y_axis + 0.05, sy_ - 0.40],
            linestyle=":", color=ACCENT_COLOR, linewidth=1.0)
    arrow(13.6, sy_, 13.7, sy_, PLATFORM_COLOR)

    card(15.0, dy_, 2.4, 0.6,
         "Tap-to-rate prompt\n(driver rates passenger)",
         DRIVER_COLOR)
    card(15.0, py_, 2.4, 0.6,
         "Tap-to-rate prompt\n(passenger rates driver)",
         RIDER_COLOR)
    arrow(15.0, sy_ + 0.36, 15.0, dy_ - 0.30, ACCENT_COLOR)
    arrow(15.0, sy_ - 0.36, 15.0, py_ + 0.30, ACCENT_COLOR)

    # ------------------------------------------------------------------
    # Phase 7 — Trip closed (chat retired, reputation updated)
    # ------------------------------------------------------------------
    card(17.6, sy_, 2.4, 0.7,
         "Reputation updated\nchat retired",
         PLATFORM_COLOR)
    arrow(16.2, dy_ - 0.30, 17.0, sy_ + 0.35, DRIVER_COLOR, ls="--")
    arrow(16.2, py_ + 0.30, 17.0, sy_ - 0.35, RIDER_COLOR, ls="--")

    # End marker
    ax.add_patch(
        FancyBboxPatch(
            (18.55, sy_ - 0.18), 0.36, 0.36,
            boxstyle="round,pad=0.02",
            facecolor=GREY, edgecolor=GREY, linewidth=1.0,
        )
    )
    ax.text(18.73, sy_, "End",
            ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold")
    arrow(18.2, sy_, 18.55, sy_, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # Title + italic subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Full ride lifecycle: publish to close",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        9.5, 5.10,
        "Three actors meet only at the trip itself; the rating moment is "
        "deliberately deferred so judgement happens off-vehicle.",
        ha="center", va="center", fontsize=10, style="italic",
        color=GREY,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.7, 5.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_act_full_ride_lifecycle", dpi=300)
    register("mbse_act_full_ride_lifecycle", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
