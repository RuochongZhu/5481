"""mbe_b4 — Trip-Bound Group Chat Lifecycle.

Conceptual lifecycle diagram (HCI/CHI readers, not engineers). A horizontal
timeline shows the chat moving through Created -> Open -> Expired, with two
side branches: cancellation removes a member (chat survives), reschedule
shifts the expiry. The 1-hour-after-trip expiry is the design choice worth
highlighting.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"  # for the 1h-after-trip expiry choice
NEUTRAL = "#566573"


@renderer("mbe_b4_ride_carpool_chat_lifecycle")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

    fig, ax = plt.subplots(figsize=(14, 8.0))

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    X_MIN, X_MAX = 0.0, 16.5
    MAIN_Y = 5.0          # main lane (chat lifecycle)
    BRANCH_UP_Y = 6.7     # reschedule branch (above)
    MEMBER_Y = 3.55       # membership icons row (just below main lane)
    BRANCH_DN_Y = 2.0     # cancellation branch (below)
    AXIS_Y = 0.55         # temporal axis

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=10,
             alpha=1.0, bold=False, ls="solid"):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=color, linewidth=1.4,
                linestyle=ls, alpha=alpha,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
            wrap=True,
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.6, ls="-", scale=14):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=scale,
            )
        )

    # ------------------------------------------------------------------
    # Main lane band (chat lifecycle)
    # ------------------------------------------------------------------
    ax.add_patch(
        FancyBboxPatch(
            (X_MIN, MAIN_Y - 0.65), X_MAX - X_MIN, 1.3,
            boxstyle="round,pad=0.02",
            facecolor=PLATFORM_COLOR, alpha=0.07,
            edgecolor=PLATFORM_COLOR, linewidth=0.8,
        )
    )
    ax.text(
        X_MIN + 0.15, MAIN_Y + 0.78, "Chat lifecycle",
        ha="left", va="center",
        fontsize=11, fontweight="bold", color=PLATFORM_COLOR,
    )

    # ------------------------------------------------------------------
    # Main timeline cards: Created -> Open -> Expired
    # ------------------------------------------------------------------
    X_CREATED = 2.6
    X_OPEN = 7.5
    X_TRIP = 10.6
    X_EXPIRED = 13.8

    # 1. Created (first booking auto-creates the chat)
    card(X_CREATED, MAIN_Y, 3.4, 0.95,
         "Chat created\nFirst booking opens the\ntrip-bound group chat",
         PLATFORM_COLOR, bold=True, fs=10)

    # 2. Open (driver = creator, passengers = members)
    card(X_OPEN, MAIN_Y, 3.0, 0.95,
         "Open\nMembers exchange\ntrip-coordination messages",
         PLATFORM_COLOR, bold=True, fs=10)

    # 3. Expired (1 h after trip end) -- accent
    card(X_EXPIRED, MAIN_Y, 3.2, 0.95,
         "Expired\nChat closes 1 hour\nafter the trip ends",
         ACCENT_COLOR, fc="#FEF5E7", bold=True, fs=10)

    # Arrows along the main lane
    arrow(X_CREATED + 1.7, MAIN_Y, X_OPEN - 1.5, MAIN_Y, PLATFORM_COLOR)
    arrow(X_OPEN + 1.5, MAIN_Y, X_EXPIRED - 1.6, MAIN_Y, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # Membership icons just below the "Open" card: 1 driver + 2 passengers
    # Placed compactly on a single row so they sit above the cancel branch.
    # ------------------------------------------------------------------
    ax.text(X_OPEN - 1.65, MEMBER_Y, "Members:",
            ha="right", va="center", fontsize=9,
            color=NEUTRAL, style="italic")

    def member_icon(x, y, color, label):
        ax.add_patch(Circle((x, y), 0.16, facecolor=color,
                            edgecolor="white", linewidth=1.2))
        ax.text(x + 0.24, y, label,
                ha="left", va="center", fontsize=8.5, color=color,
                fontweight="bold")

    member_icon(X_OPEN - 1.45, MEMBER_Y, DRIVER_COLOR, "Driver (creator)")
    member_icon(X_OPEN + 0.20, MEMBER_Y, RIDER_COLOR, "Passenger")
    member_icon(X_OPEN + 1.55, MEMBER_Y, RIDER_COLOR, "Passenger")

    # ------------------------------------------------------------------
    # Side branch (above): Reschedule shifts the expiry
    # ------------------------------------------------------------------
    card(X_OPEN + 1.4, BRANCH_UP_Y, 4.4, 0.95,
         "Trip rescheduled\nExpiry shifts to 1 hour after\nthe new trip end time",
         ACCENT_COLOR, fc="#FFFFFF", fs=9.5, ls="dashed")
    UP_X = X_OPEN + 1.0
    arrow(UP_X, MAIN_Y + 0.5, UP_X, BRANCH_UP_Y - 0.5,
          ACCENT_COLOR, ls="--", lw=1.4)
    ax.text(UP_X + 0.18, (MAIN_Y + 0.5 + BRANCH_UP_Y - 0.5) / 2,
            "on reschedule", ha="left", va="center",
            fontsize=9, color=ACCENT_COLOR, style="italic")
    # Effect arrow back into the expired box
    arrow(X_OPEN + 3.6, BRANCH_UP_Y - 0.5, X_EXPIRED - 0.4, MAIN_Y + 0.5,
          ACCENT_COLOR, ls=":", lw=1.4, scale=12)
    ax.text(X_EXPIRED - 1.4, MAIN_Y + 0.85, "expiry shifts",
            ha="center", va="center",
            fontsize=8.5, color=ACCENT_COLOR, style="italic")

    # ------------------------------------------------------------------
    # Side branch (below): Cancellation removes a member
    # ------------------------------------------------------------------
    card(X_OPEN + 1.4, BRANCH_DN_Y, 4.4, 0.95,
         "Passenger cancels\nThe member is removed;\nchat survives for the others",
         RIDER_COLOR, fc="#FFFFFF", fs=9.5, ls="dashed")
    # Drop from the main lane down past the membership row, routed slightly
    # right of the membership icons so the "on cancel" label has clean space.
    DN_X = X_OPEN + 2.7
    arrow(DN_X, MAIN_Y - 0.5, DN_X, BRANCH_DN_Y + 0.5,
          RIDER_COLOR, ls="--", lw=1.4)
    ax.text(DN_X + 0.18, (MAIN_Y - 0.5 + BRANCH_DN_Y + 0.5) / 2,
            "on cancel", ha="left", va="center",
            fontsize=9, color=RIDER_COLOR, style="italic")

    # ------------------------------------------------------------------
    # Temporal axis at the bottom
    # ------------------------------------------------------------------
    ax.plot([X_MIN + 0.6, X_MAX - 0.4], [AXIS_Y, AXIS_Y],
            color=NEUTRAL, linewidth=1.0)
    TIMES = [
        (X_CREATED, "First booking"),
        (X_OPEN,   "Trip-coordination window"),
        (X_TRIP,   "Trip ends"),
        (X_EXPIRED, "Trip end + 1 hour"),
    ]
    for x, lbl in TIMES:
        ax.plot([x, x], [AXIS_Y - 0.07, AXIS_Y + 0.07],
                color=NEUTRAL, linewidth=1.0)
        ax.text(x, AXIS_Y - 0.25, lbl,
                ha="center", va="top", fontsize=9, color=NEUTRAL,
                style="italic")

    # Faint vertical guideline tying "Trip ends" / "+1 hour" to the lane
    ax.plot([X_TRIP, X_TRIP], [AXIS_Y + 0.1, BRANCH_DN_Y - 0.6],
            linestyle=":", color=NEUTRAL, linewidth=0.9, alpha=0.6)
    ax.plot([X_EXPIRED, X_EXPIRED], [AXIS_Y + 0.1, MAIN_Y - 0.55],
            linestyle=":", color=ACCENT_COLOR, linewidth=0.9, alpha=0.8)

    # ------------------------------------------------------------------
    # Snapshot footer (findings, not implementation)
    # ------------------------------------------------------------------
    ax.text(
        (X_MIN + X_MAX) / 2, -0.05,
        "Snapshot: 0 trip-bound chats currently live; indirect evidence "
        "from 8 post-trip rating reminders and 16 WeChat ride pushes "
        "tied to historical bookings.",
        ha="center", va="center", fontsize=9.5, color=NEUTRAL, style="italic",
    )

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Trip-bound group chat lifecycle",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 7.85,
        "The chat is scoped to a single trip and closes one hour after "
        "it ends, by design, to keep coordination time-boxed.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.4, 8.1)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_b4_ride_carpool_chat_lifecycle", dpi=300)
    register("mbe_b4_ride_carpool_chat_lifecycle", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
