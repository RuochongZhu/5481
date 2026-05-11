"""mbe_c3 — Rating window timeline + bidirectional submission flow.

Conceptual figure for HCI readers. Top: a horizontal time axis from booking
to revisable horizon, partitioned into three zones (pre-departure /
during-trip / open window) with the 2-hour gate highlighted. Bottom: a
simple bidirectional sequence — passenger and driver each tap-rate, the
rating is recorded (revisable), and the user's average rating updates.
A side text-box surfaces three open design proposals not yet implemented.
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

GREY_ZONE = "#ECEFF1"
GREY_BORDER = "#7F8C8D"
YELLOW_ZONE = "#FCF3CF"
YELLOW_BORDER = "#B7950B"
GREEN_ZONE = "#D4EFDF"
GREEN_BORDER = "#1E8449"


@renderer("mbe_c3_rating_2h_delay_flow")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(14, 8.0),
        gridspec_kw=dict(height_ratios=[1.15, 1.0], hspace=0.22),
    )
    fig.subplots_adjust(top=0.97, bottom=0.03, left=0.04, right=0.98)

    # =====================================================================
    # TOP PANEL — rating-window timeline
    # =====================================================================
    X_MIN, X_MAX = 0.0, 16.0

    # Time anchors along the axis
    X_T0 = 1.5     # booking moment
    X_DEP = 7.5    # trip happens (departure)
    X_GATE = 10.0  # trip + 2 hours (rating opens)
    X_LATE = 14.5  # revisable horizon

    band_y = 1.4
    band_h = 1.1

    # Three zones
    ax_top.add_patch(Rectangle(
        (X_MIN + 0.4, band_y - band_h / 2),
        X_DEP - (X_MIN + 0.4), band_h,
        facecolor=GREY_ZONE, edgecolor=GREY_BORDER, linewidth=0.8, zorder=1,
    ))
    ax_top.add_patch(Rectangle(
        (X_DEP, band_y - band_h / 2),
        X_GATE - X_DEP, band_h,
        facecolor=YELLOW_ZONE, edgecolor=YELLOW_BORDER, linewidth=0.8, zorder=1,
    ))
    ax_top.add_patch(Rectangle(
        (X_GATE, band_y - band_h / 2),
        (X_MAX - 0.4) - X_GATE, band_h,
        facecolor=GREEN_ZONE, edgecolor=GREEN_BORDER, linewidth=0.8, zorder=1,
    ))

    # Zone labels (inside bands)
    ax_top.text(
        (X_MIN + 0.4 + X_DEP) / 2, band_y, "Pre-departure\n(rating not yet eligible)",
        ha="center", va="center", fontsize=10, color=NEUTRAL, style="italic",
        zorder=3,
    )
    ax_top.text(
        (X_DEP + X_GATE) / 2, band_y, "During trip\n(submission blocked)",
        ha="center", va="center", fontsize=10, color="#7E5109",
        fontweight="bold", zorder=3,
    )
    ax_top.text(
        (X_GATE + (X_MAX - 0.4)) / 2, band_y,
        "Rating window OPEN\n(rating recorded; remains revisable)",
        ha="center", va="center", fontsize=10, color="#196F3D",
        fontweight="bold", zorder=3,
    )

    # Time axis (below the bands)
    axis_y = 0.4
    ax_top.plot(
        [X_MIN + 0.4, X_MAX - 0.3], [axis_y, axis_y],
        color=NEUTRAL, linewidth=1.1, zorder=4,
    )
    ax_top.annotate(
        "", xy=(X_MAX - 0.2, axis_y), xytext=(X_MAX - 0.5, axis_y),
        arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.1),
        zorder=4,
    )
    ax_top.text(
        X_MAX - 0.15, axis_y - 0.18, "time",
        ha="right", va="top", fontsize=9, color=NEUTRAL, style="italic",
    )

    # Tick marks + labels
    ticks = [
        (X_T0,   "T0\nBooking"),
        (X_DEP,  "Trip happens"),
        (X_GATE, "Trip + 2 hours\n(rating opens)"),
        (X_LATE, "Later\n(rating still revisable)"),
    ]
    for x, lbl in ticks:
        ax_top.plot(
            [x, x], [axis_y - 0.08, axis_y + 0.08],
            color=NEUTRAL, linewidth=1.1, zorder=5,
        )
        ax_top.text(
            x, axis_y - 0.28, lbl,
            ha="center", va="top", fontsize=9.2, color="#1B2631",
        )

    # Highlight the 2-hour gate with the accent color (vertical marker)
    ax_top.plot(
        [X_GATE, X_GATE], [axis_y + 0.05, band_y + band_h / 2 + 0.55],
        color=ACCENT_COLOR, linewidth=2.0, linestyle="--", zorder=6,
    )
    ax_top.add_patch(FancyBboxPatch(
        (X_GATE - 1.5, band_y + band_h / 2 + 0.55),
        3.0, 0.55,
        boxstyle="round,pad=0.04",
        facecolor="#FEF5E7", edgecolor=ACCENT_COLOR, linewidth=1.4, zorder=7,
    ))
    ax_top.text(
        X_GATE, band_y + band_h / 2 + 0.82,
        "2-hour gate: rating becomes available\n2 hours after the trip ends",
        ha="center", va="center", fontsize=9.5, color="#7D4E0F",
        fontweight="bold", zorder=8,
    )

    # Booking marker callout (small flag above T0)
    ax_top.add_patch(FancyBboxPatch(
        (X_T0 - 1.0, band_y + band_h / 2 + 0.55),
        2.0, 0.45,
        boxstyle="round,pad=0.04",
        facecolor="white", edgecolor=RIDER_COLOR, linewidth=1.3, zorder=7,
    ))
    ax_top.text(
        X_T0, band_y + band_h / 2 + 0.78, "Trip booked",
        ha="center", va="center", fontsize=9.5, color=RIDER_COLOR,
        fontweight="bold", zorder=8,
    )

    # Title + subtitle (top panel)
    ax_top.text(
        X_MIN + 0.2, 4.05,
        "Rating window: when can riders and drivers rate each other?",
        ha="left", va="center", fontsize=14, fontweight="bold", color="#1B2631",
    )
    ax_top.text(
        X_MIN + 0.2, 3.65,
        "The post-trip window opens 2 hours after the trip ends; "
        "ratings are recorded but remain revisable thereafter.",
        ha="left", va="center", fontsize=10.5, style="italic", color=NEUTRAL,
    )

    ax_top.set_xlim(X_MIN, X_MAX)
    ax_top.set_ylim(-0.4, 4.3)
    ax_top.axis("off")

    # =====================================================================
    # BOTTOM PANEL — bidirectional submission flow + side note
    # =====================================================================
    # Allocate the right-hand strip for the open-design side box.
    BX_MIN, BX_MAX = 0.0, 16.0
    SIDE_LEFT = 11.4  # everything to the right of this is the side note

    ax_bot.set_xlim(BX_MIN, BX_MAX)
    ax_bot.set_ylim(-0.2, 3.6)
    ax_bot.axis("off")

    # Lane y-coordinates
    PY = 2.55  # passenger lane
    SY = 1.55  # platform lane
    DY = 0.55  # driver lane
    LANE_H = 0.85

    LANES = [
        ("Passenger", RIDER_COLOR, PY),
        ("Platform",  PLATFORM_COLOR, SY),
        ("Driver",    DRIVER_COLOR, DY),
    ]
    LANE_RIGHT = SIDE_LEFT - 0.3
    for name, color, y in LANES:
        ax_bot.add_patch(FancyBboxPatch(
            (BX_MIN + 0.1, y - LANE_H / 2),
            LANE_RIGHT - (BX_MIN + 0.1), LANE_H,
            boxstyle="round,pad=0.02",
            facecolor=color, alpha=0.07,
            edgecolor=color, linewidth=0.8, zorder=1,
        ))
        ax_bot.text(
            BX_MIN + 0.25, y, name,
            ha="left", va="center", fontsize=11, fontweight="bold", color=color,
        )

    # Helpers
    def card(x, y, w, h, text, color, *, fc="white", fs=9.5, bold=False):
        ax_bot.add_patch(FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.04",
            facecolor=fc, edgecolor=color, linewidth=1.4, zorder=3,
        ))
        ax_bot.text(
            x, y, text,
            ha="center", va="center", fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal", zorder=4,
        )

    def arrow(x0, y0, x1, y1, color, *, ls="-", lw=1.4):
        ax_bot.add_patch(FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle="-|>", color=color,
            linewidth=lw, linestyle=ls, mutation_scale=12, zorder=2,
        ))

    # Step columns
    X_TAP = 3.5     # both actors tap-rate (passenger & driver simultaneously)
    X_REC = 6.7     # platform records the rating
    X_AVG = 9.7     # platform updates each user's average

    # 1. Passenger taps to rate
    card(X_TAP, PY, 2.4, 0.6,
         "Tap-to-rate prompt\n(passenger rates driver)",
         RIDER_COLOR, bold=True)
    # 2. Driver taps to rate
    card(X_TAP, DY, 2.4, 0.6,
         "Tap-to-rate prompt\n(driver rates passenger)",
         DRIVER_COLOR, bold=True)

    # 3. Platform records both ratings (single card on platform lane)
    card(X_REC, SY, 2.5, 0.65,
         "Rating recorded\n(revisable)",
         PLATFORM_COLOR, bold=True)
    arrow(X_TAP + 1.2, PY - 0.2, X_REC - 1.25, SY + 0.25, RIDER_COLOR)
    arrow(X_TAP + 1.2, DY + 0.2, X_REC - 1.25, SY - 0.25, DRIVER_COLOR)

    # 4. Platform updates each user's average rating
    card(X_AVG, SY, 2.6, 0.65,
         "User's average rating\nupdated",
         PLATFORM_COLOR)
    arrow(X_REC + 1.25, SY, X_AVG - 1.30, SY, PLATFORM_COLOR)

    # 5. Echo the new average back to both actors (dashed)
    arrow(X_AVG, SY + 0.32, X_AVG, PY - 0.30, PLATFORM_COLOR, ls="--")
    arrow(X_AVG, SY - 0.32, X_AVG, DY + 0.30, PLATFORM_COLOR, ls="--")

    # Bottom-panel title + subtitle
    ax_bot.text(
        BX_MIN + 0.2, 3.45,
        "Bidirectional rating: each side rates the other, then averages update",
        ha="left", va="center", fontsize=13, fontweight="bold", color="#1B2631",
    )
    ax_bot.text(
        BX_MIN + 0.2, 3.13,
        "Snapshot: 0 ratings submitted in production "
        "(formative design, not yet validated by usage).",
        ha="left", va="center", fontsize=10, style="italic", color=NEUTRAL,
    )

    # ------------------------------------------------------------------
    # Side text-box: open design proposals (not yet implemented)
    # ------------------------------------------------------------------
    side_x = SIDE_LEFT + 0.2
    side_w = (BX_MAX - 0.2) - side_x
    side_y = 0.15
    side_h = 3.20

    ax_bot.add_patch(FancyBboxPatch(
        (side_x, side_y), side_w, side_h,
        boxstyle="round,pad=0.04",
        facecolor="#FDFEFE", edgecolor=ACCENT_COLOR, linewidth=1.4, zorder=3,
    ))
    ax_bot.text(
        side_x + 0.20, side_y + side_h - 0.25,
        "Open design proposals\n(not yet implemented)",
        ha="left", va="top", fontsize=10.5, fontweight="bold",
        color=ACCENT_COLOR, zorder=4,
    )
    bullets = [
        "Pre-publication dispute window\n(flag a rating before it goes live)",
        "Cross-trip trend protection\n(buffer against retaliatory dips)",
        "Mandatory justification\n(low scores require a written reason)",
    ]
    bullet_y = side_y + side_h - 0.95
    for b in bullets:
        ax_bot.text(
            side_x + 0.30, bullet_y, "•",
            ha="left", va="top", fontsize=11, color=ACCENT_COLOR,
            fontweight="bold", zorder=4,
        )
        ax_bot.text(
            side_x + 0.55, bullet_y, b,
            ha="left", va="top", fontsize=9.4, color="#1B2631", zorder=4,
        )
        bullet_y -= 0.65

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    pdf, png = save_mpl("mbe_c3_rating_2h_delay_flow", dpi=300)
    register("mbe_c3_rating_2h_delay_flow", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
