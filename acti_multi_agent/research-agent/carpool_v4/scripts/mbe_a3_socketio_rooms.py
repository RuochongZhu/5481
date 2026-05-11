"""mbe_a3 — Real-time substrate (hub-and-spoke).

Three concept-level channel types radiate from a single authenticated
real-time hub:

  - Per-user channel        (real-time push targeted at one person)
  - Per-activity channel    (live chat scoped to one activity)
  - Per-thread channel      (DM and group-typing indicators)

A small dashed inset shows that guests connect read-only without an
account. Multi-instance support is mentioned in the caption as a design
choice (no product names).

Style follows scripts/_mbe_style_guide.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"

# Per-channel accent colors (kept distinct, paper-style muted).
USER_COLOR = "#B9770E"      # warm amber — per-user
ACT_COLOR = "#1E8449"       # mint green — per-activity
THREAD_COLOR = "#1F618D"    # deep blue — per-thread


@renderer("mbe_a3_socketio_rooms")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

    fig, ax = plt.subplots(figsize=(13, 7.6))

    # ------------------------------------------------------------------
    # Hub (center)
    # ------------------------------------------------------------------
    HUB_X, HUB_Y = 6.5, 3.9
    HUB_R = 1.15

    ax.add_patch(
        Circle(
            (HUB_X, HUB_Y), HUB_R,
            facecolor=PLATFORM_COLOR, edgecolor="#0E2F44",
            linewidth=1.6, zorder=2,
        )
    )
    ax.text(
        HUB_X, HUB_Y + 0.18,
        "Real-time substrate",
        ha="center", va="center",
        color="white", fontsize=12.5, fontweight="bold", zorder=3,
    )
    ax.text(
        HUB_X, HUB_Y - 0.18,
        "(authenticated)",
        ha="center", va="center",
        color="white", fontsize=10.5, style="italic", zorder=3,
    )

    # ------------------------------------------------------------------
    # Helper: spoke card
    # ------------------------------------------------------------------
    def spoke(cx, cy, w, h, title, lines, color):
        ax.add_patch(
            FancyBboxPatch(
                (cx - w / 2, cy - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor="white", edgecolor=color, linewidth=1.4,
                zorder=2,
            )
        )
        # Title bar
        ax.text(
            cx, cy + h / 2 - 0.32,
            title,
            ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=color,
        )
        # Body lines (concept-level descriptions of what flows through)
        body_top = cy + h / 2 - 0.78
        for i, line in enumerate(lines):
            ax.text(
                cx, body_top - i * 0.34,
                line,
                ha="center", va="center",
                fontsize=9.7, color="#1B2631",
            )

    def hub_arrow(x1, y1, color):
        # Arrow goes from hub edge (toward target) to a point just outside
        # the spoke card. We trim from both ends.
        import math
        dx, dy = x1 - HUB_X, y1 - HUB_Y
        dist = math.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist
        sx, sy = HUB_X + ux * (HUB_R + 0.05), HUB_Y + uy * (HUB_R + 0.05)
        ex, ey = x1 - ux * 0.05, y1 - uy * 0.05
        ax.add_patch(
            FancyArrowPatch(
                (sx, sy), (ex, ey),
                arrowstyle="-|>", color=color,
                linewidth=1.8, mutation_scale=14, zorder=1,
            )
        )

    # ------------------------------------------------------------------
    # Three spokes (top, lower-left, lower-right)
    # ------------------------------------------------------------------
    SPOKE_W, SPOKE_H = 4.2, 1.85

    # 1. Per-user channel (top)
    user_cx, user_cy = HUB_X, HUB_Y + 2.65
    spoke(
        user_cx, user_cy, SPOKE_W, SPOKE_H,
        "Per-user channel",
        [
            "Real-time push to a single user",
            "Personal alerts and reminders",
            "Presence updates (online / away)",
        ],
        USER_COLOR,
    )
    # arrow ends at bottom-center of spoke card
    hub_arrow(user_cx, user_cy - SPOKE_H / 2, USER_COLOR)

    # 2. Per-activity channel (lower-left)
    act_cx, act_cy = HUB_X - 4.0, HUB_Y - 2.05
    spoke(
        act_cx, act_cy, SPOKE_W, SPOKE_H,
        "Per-activity channel",
        [
            "Live chat scoped to one activity",
            "Activity-wide announcements",
            "Members join on entering activity",
        ],
        ACT_COLOR,
    )
    hub_arrow(act_cx + SPOKE_W / 2 - 0.1, act_cy + SPOKE_H / 2 - 0.1, ACT_COLOR)

    # 3. Per-thread channel (lower-right)
    th_cx, th_cy = HUB_X + 4.0, HUB_Y - 2.05
    spoke(
        th_cx, th_cy, SPOKE_W, SPOKE_H,
        "Per-thread channel",
        [
            "Direct messages and group threads",
            "Typing indicators (sender excluded)",
            "Members join on opening the thread",
        ],
        THREAD_COLOR,
    )
    hub_arrow(th_cx - SPOKE_W / 2 + 0.1,
              th_cy + SPOKE_H / 2 - 0.1, THREAD_COLOR)

    # ------------------------------------------------------------------
    # Guest read-only inset (small, dashed, lower-left of hub)
    # ------------------------------------------------------------------
    guest_w, guest_h = 2.6, 0.95
    guest_cx, guest_cy = 1.7, 5.7
    ax.add_patch(
        FancyBboxPatch(
            (guest_cx - guest_w / 2, guest_cy - guest_h / 2),
            guest_w, guest_h,
            boxstyle="round,pad=0.04",
            facecolor="white", edgecolor=NEUTRAL,
            linewidth=1.2, linestyle="--", zorder=2,
        )
    )
    ax.text(
        guest_cx, guest_cy + 0.18,
        "Guest connection",
        ha="center", va="center",
        fontsize=10.5, fontweight="bold", color=NEUTRAL,
    )
    ax.text(
        guest_cx, guest_cy - 0.18,
        "Read-only access token",
        ha="center", va="center",
        fontsize=9.5, style="italic", color=NEUTRAL,
    )
    # Dashed connector to the hub
    ax.add_patch(
        FancyArrowPatch(
            (guest_cx + guest_w / 2 - 0.05, guest_cy - 0.25),
            (HUB_X - HUB_R - 0.05, HUB_Y + 0.55),
            arrowstyle="-|>", color=NEUTRAL,
            linewidth=1.0, linestyle="--",
            mutation_scale=10, zorder=1,
        )
    )

    # ------------------------------------------------------------------
    # Title + subtitle + caption
    # ------------------------------------------------------------------
    ax.set_title(
        "Real-time substrate: three channel types from one authenticated hub",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        HUB_X, 7.55,
        "An authenticated connection is required; messages are scoped by "
        "channel type, and the substrate is designed to fan out across "
        "multiple instances.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(-0.4, 13.4)
    ax.set_ylim(-0.4, 7.9)
    ax.set_aspect("equal")
    ax.axis("off")

    pdf, png = save_mpl("mbe_a3_socketio_rooms", dpi=300)
    register("mbe_a3_socketio_rooms", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
