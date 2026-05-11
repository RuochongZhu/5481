"""mbse_state_machine_unified - Three coupled lifecycles on one canvas.

Concept-level UML state machine across three modules:

  - Trip          : active -> full -> completed | cancelled
  - Booking       : confirmed -> cancelled
  - Trip-bound chat (carpool group): created -> active -> expired

Cross-cluster dashed edges show the design-level couplings:
  * Confirming the last booking flips the trip to full.
  * Confirming the first booking opens the trip-bound chat.
  * Cancelling a booking can re-open a previously-full trip.
  * Rescheduling the trip extends the chat-expiry deadline.

Paper-style: matplotlib only, no file/line references, no method names,
no SQL, plain English transition labels.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


# Palette (per style guide)
PLATFORM_COLOR = "#1A5276"  # navy — trip cluster + structure
RIDER_COLOR = "#2980B9"     # blue — booking cluster (passenger-owned)
DRIVER_COLOR = "#C0392B"    # red — group cluster (driver-anchored chat)
ACCENT_COLOR = "#F39C12"    # orange — cross-cluster triggers
NEUTRAL_GREY = "#566573"

# Lighter alpha tints per state semantics
ACTIVE_FILL = "#D5F5E3"      # green-tint  (open / accepting)
FULL_FILL = "#FCF3CF"        # yellow-tint (saturated)
COMPLETED_FILL = "#D6EAF8"   # blue-tint   (final, success)
CANCELLED_FILL = "#FADBD8"   # red-tint    (final, abort)
CONFIRMED_FILL = "#D5F5E3"   # green-tint  (booking accepted)
CREATED_FILL = "#FDEBD0"     # peach-tint  (chat just opened)
CHAT_ACTIVE_FILL = "#D5F5E3" # green-tint  (chat open window)
EXPIRED_FILL = "#EAEDED"     # grey-tint   (final, read-only)


@renderer("mbse_state_machine_unified")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

    fig, ax = plt.subplots(figsize=(15, 10.0))

    X_MIN, X_MAX = 0.0, 14.5

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def state(x, y, w, h, label, *, fill, border=PLATFORM_COLOR,
              terminal=False, bold=True, fs=10.0):
        """Rounded state box; if terminal, draw a thin outer ring."""
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
                          boxstyle="round,pad=0.18", alpha=0.92),
            )

    def cluster_band(y_center, height, label, color):
        """Soft background band for a cluster + left-side label."""
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN + 0.15, y_center - height / 2),
                X_MAX - X_MIN - 0.3, height,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=0.07,
                edgecolor=color, linewidth=0.8,
            )
        )
        ax.text(
            X_MIN + 0.35, y_center + height / 2 - 0.25,
            label,
            ha="left", va="top",
            fontsize=11, fontweight="bold",
            color=color, style="italic",
        )

    # ------------------------------------------------------------------
    # TOP cluster: Trip lifecycle (driver-owned)
    # ------------------------------------------------------------------
    TOP_Y = 8.3
    TOP_H = 2.2
    cluster_band(TOP_Y, TOP_H,
                 "Trip lifecycle  (driver-owned)", PLATFORM_COLOR)

    initial_dot(0.95, TOP_Y + 0.05)
    state(2.55, TOP_Y, 1.95, 0.85, "active\nseats remaining",
          fill=ACTIVE_FILL, border=PLATFORM_COLOR)
    state(5.30, TOP_Y, 1.65, 0.85, "full\nlast seat taken",
          fill=FULL_FILL, border=PLATFORM_COLOR)
    state(8.40, TOP_Y + 0.55, 1.85, 0.80, "completed",
          fill=COMPLETED_FILL, border=PLATFORM_COLOR, terminal=True)
    state(8.40, TOP_Y - 0.55, 1.85, 0.80, "cancelled",
          fill=CANCELLED_FILL, border=PLATFORM_COLOR, terminal=True)

    arrow(1.10, TOP_Y + 0.05, 1.60, TOP_Y, color=PLATFORM_COLOR,
          label="Driver creates trip", ly=TOP_Y + 0.32)
    arrow(3.55, TOP_Y, 4.50, TOP_Y, color=PLATFORM_COLOR,
          label="Last seat fills", ly=TOP_Y + 0.30)
    arrow(6.15, TOP_Y + 0.15, 7.50, TOP_Y + 0.55, color=PLATFORM_COLOR,
          label="Driver completes trip",
          lx=6.85, ly=TOP_Y + 0.62)
    # active -> cancelled (curve down then right)
    arrow(2.55, TOP_Y - 0.42, 7.45, TOP_Y - 0.78,
          color=PLATFORM_COLOR, rad=-0.34,
          label="Driver cancels  (before departure)",
          lx=4.20, ly=TOP_Y - 1.00)
    # full -> cancelled (short)
    arrow(5.95, TOP_Y - 0.30, 7.45, TOP_Y - 0.55,
          color=PLATFORM_COLOR, rad=-0.10,
          label="Driver cancels",
          lx=6.95, ly=TOP_Y - 0.18)

    # ------------------------------------------------------------------
    # MIDDLE cluster: Booking lifecycle (passenger-owned)
    # ------------------------------------------------------------------
    MID_Y = 4.7
    MID_H = 1.8
    cluster_band(MID_Y, MID_H,
                 "Booking lifecycle  (passenger-owned)", RIDER_COLOR)

    initial_dot(0.95, MID_Y)
    state(2.85, MID_Y, 2.20, 0.80, "confirmed\non reservation",
          fill=CONFIRMED_FILL, border=RIDER_COLOR)
    state(8.40, MID_Y, 2.10, 0.80, "cancelled",
          fill=CANCELLED_FILL, border=RIDER_COLOR, terminal=True)

    arrow(1.10, MID_Y, 1.75, MID_Y, color=RIDER_COLOR,
          label="Passenger reserves seat",
          lx=1.45, ly=MID_Y + 0.32)
    arrow(3.95, MID_Y, 7.35, MID_Y, color=RIDER_COLOR,
          label="Passenger or driver cancels  (before departure)",
          ly=MID_Y + 0.30)

    # ------------------------------------------------------------------
    # BOTTOM cluster: Trip-bound chat lifecycle
    # ------------------------------------------------------------------
    BOT_Y = 1.4
    BOT_H = 2.0
    cluster_band(BOT_Y, BOT_H,
                 "Trip-bound chat lifecycle  (auto-managed)", DRIVER_COLOR)

    initial_dot(0.95, BOT_Y)
    state(2.85, BOT_Y, 2.20, 0.85, "created\nchat opened",
          fill=CREATED_FILL, border=DRIVER_COLOR)
    state(5.65, BOT_Y, 2.20, 0.85, "active\nwithin chat window",
          fill=CHAT_ACTIVE_FILL, border=DRIVER_COLOR)
    state(8.40, BOT_Y, 2.10, 0.85, "expired\nread-only",
          fill=EXPIRED_FILL, border=DRIVER_COLOR, terminal=True)

    arrow(1.10, BOT_Y, 1.75, BOT_Y, color=DRIVER_COLOR,
          label="First booking opens chat", ly=BOT_Y + 0.30)
    arrow(3.95, BOT_Y, 4.55, BOT_Y, color=DRIVER_COLOR,
          label="First message", ly=BOT_Y + 0.30)
    arrow(6.75, BOT_Y, 7.35, BOT_Y, color=DRIVER_COLOR,
          label="1 hour after departure",
          ly=BOT_Y + 0.30)

    # ------------------------------------------------------------------
    # Cross-cluster dashed triggers (ACCENT_COLOR)
    # ------------------------------------------------------------------
    # Booking confirmed -> Trip becomes full (last seat)
    # Routed left to avoid the trip-cancel curves underneath the trip cluster.
    arrow(
        2.85, MID_Y + 0.40,
        5.05, TOP_Y - 0.45,
        color=ACCENT_COLOR, ls="--", lw=1.7, rad=0.40,
        label="If last seat:\nbooking flips trip to full",
        lx=1.40, ly=6.05, label_color=ACCENT_COLOR, label_fs=9.0,
    )

    # Booking confirmed -> Chat created (first booking)
    arrow(
        2.85, MID_Y - 0.40,
        2.85, BOT_Y + 0.45,
        color=ACCENT_COLOR, ls="--", lw=1.7, rad=0.0,
        label="First booking opens trip-bound chat",
        lx=4.40, ly=3.05, label_color=ACCENT_COLOR, label_fs=9.0,
    )

    # Booking cancelled -> Trip re-opens (was full)
    arrow(
        8.40, MID_Y + 0.40,
        5.85, TOP_Y - 0.45,
        color=ACCENT_COLOR, ls="--", lw=1.7, rad=-0.18,
        label=("If trip was full: cancellation\n"
               "re-opens trip to active"),
        lx=8.50, ly=6.05, label_color=ACCENT_COLOR, label_fs=9.0,
    )

    # Trip rescheduled -> Chat expiry shifts.
    # Polyline along the empty right gutter so it never crosses
    # any state box. Only the final segment carries the
    # arrowhead.
    GUTTER_X = 13.20
    GUTTER_TOP = 6.95   # high in the trip↔booking gutter strip
    # Trip active -> down a bit (small stub) to clear cancel curves
    ax.plot(
        [3.55, GUTTER_X], [GUTTER_TOP, GUTTER_TOP],
        color=ACCENT_COLOR, linestyle="--", linewidth=1.7,
    )
    # Stub from active down to the horizontal
    ax.plot(
        [3.55, 3.55], [TOP_Y - 0.42, GUTTER_TOP],
        color=ACCENT_COLOR, linestyle="--", linewidth=1.7,
    )
    # Down the right gutter (plain line) into the chat↔booking strip.
    GUTTER_BOT = BOT_Y + 0.95   # midway between chat band top and booking band
    ax.plot(
        [GUTTER_X, GUTTER_X], [GUTTER_TOP, GUTTER_BOT],
        color=ACCENT_COLOR, linestyle="--", linewidth=1.7,
    )
    # Across to above chat-active (plain line; horizontal in
    # the empty strip just above the chat cluster band)
    ax.plot(
        [GUTTER_X, 5.65], [GUTTER_BOT, GUTTER_BOT],
        color=ACCENT_COLOR, linestyle="--", linewidth=1.7,
    )
    # Drop into chat-active from directly above (arrowhead here only)
    arrow(
        5.65, GUTTER_BOT,
        5.65, BOT_Y + 0.45,
        color=ACCENT_COLOR, ls="--", lw=1.7, rad=0.0,
    )
    ax.text(
        13.85, 4.95,
        "Driver\nreschedules\ntrip:\n"
        "chat-expiry\ndeadline shifts",
        ha="center", va="center",
        fontsize=9.0, color=ACCENT_COLOR,
        bbox=dict(facecolor="white", edgecolor="none",
                  boxstyle="round,pad=0.18", alpha=0.92),
    )

    # Trip completed: explicit no-trigger note
    ax.text(
        11.40, MID_Y,
        "Trip completion does not\n"
        "alter bookings or chat;\n"
        "chat expires on its own\n"
        "1-hour post-departure timer.",
        ha="center", va="center",
        fontsize=9, style="italic", color=NEUTRAL_GREY,
        bbox=dict(facecolor="#FBFCFC", edgecolor=NEUTRAL_GREY,
                  boxstyle="round,pad=0.35", linewidth=0.9),
    )
    arrow(
        9.45, TOP_Y + 0.55,
        11.40, MID_Y + 0.45,
        color=NEUTRAL_GREY, ls=":", lw=1.0, rad=-0.10,
    )

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Unified state machines: trip, booking, and trip-bound chat",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 10.10,
        "Three coupled lifecycles; orange dashed edges mark the "
        "design-level cross-module triggers.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL_GREY,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.1, 10.4)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbse_state_machine_unified", dpi=300)
    register("mbse_state_machine_unified", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
