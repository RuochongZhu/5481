"""mbe_d1 — Cross-module messaging substrate.

Three messaging surfaces (direct messages, group chat, system messages) sit on
top of a single shared real-time substrate. The non-obvious design choices are:
(1) DMs can be bound to a trip / listing / activity, so a conversation carries
its originating context; (2) a light-touch first-message friction guard makes
cold DMs require a reply before further messages can flow.
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

# Surface palette (one color per surface, used for its card border).
DM_COLOR = "#1F618D"        # blue-ish for direct messages
GROUP_COLOR = "#1E8449"     # green for group chat
SYS_COLOR = "#B7950B"       # amber for system messages
BIND_COLOR = "#6C3483"      # purple for cross-module binding


@renderer("mbe_d1_messaging_substrate")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 7.8))

    X_MIN, X_MAX = 0.0, 16.5
    Y_MIN, Y_MAX = -0.4, 8.2

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=9.5,
             alpha=1.0, bold=False, title=None):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=color, linewidth=1.4, alpha=alpha,
            )
        )
        if title is not None:
            ax.text(
                x, y + h / 2 - 0.22, title,
                ha="center", va="center",
                fontsize=fs + 1.0, color=color, fontweight="bold",
            )
            ax.text(
                x, y - 0.12, text,
                ha="center", va="center",
                fontsize=fs, color="#1B2631",
                fontweight="bold" if bold else "normal",
                wrap=True,
            )
        else:
            ax.text(
                x, y, text,
                ha="center", va="center",
                fontsize=fs, color="#1B2631",
                fontweight="bold" if bold else "normal",
                wrap=True,
            )

    def arrow(x0, y0, x1, y1, color, *, style="-|>", lw=1.4, ls="-",
              mut=12):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle=style, color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=mut,
            )
        )

    # ------------------------------------------------------------------
    # Layout: left two-thirds = surfaces + substrate; right column = binding
    # ------------------------------------------------------------------
    LEFT_LEFT, LEFT_RIGHT = 0.4, 10.6
    RIGHT_LEFT, RIGHT_RIGHT = 11.4, 16.2

    # Light separator between left block and right column
    ax.plot([10.95, 10.95], [0.4, 6.7],
            color=NEUTRAL, linewidth=0.6, linestyle=(0, (4, 4)),
            alpha=0.6)

    # ------------------------------------------------------------------
    # Top tier — three surface cards (left block)
    # ------------------------------------------------------------------
    SURFACE_Y = 5.5
    SURFACE_W, SURFACE_H = 3.05, 1.5
    surface_xs = [
        LEFT_LEFT + 0.55 + SURFACE_W / 2,                           # DM
        LEFT_LEFT + 0.55 + SURFACE_W * 1.5 + 0.45,                  # Group
        LEFT_LEFT + 0.55 + SURFACE_W * 2.5 + 0.90,                  # System
    ]

    # 1. Direct messages
    card(
        surface_xs[0], SURFACE_Y, SURFACE_W, SURFACE_H,
        "One-to-one threads\nbetween two users\n\nSnapshot: 22 messages",
        DM_COLOR, title="Direct messages",
    )

    # 2. Group chat
    card(
        surface_xs[1], SURFACE_Y, SURFACE_W, SURFACE_H,
        "Many-to-many threads\nin community groups\n\nSnapshot: 2 messages",
        GROUP_COLOR, title="Group chat",
    )

    # 3. System messages
    card(
        surface_xs[2], SURFACE_Y, SURFACE_W, SURFACE_H,
        "Platform-to-user feedback\nand announcements\n\nSnapshot: 10 rows",
        SYS_COLOR, title="System messages",
    )

    # ------------------------------------------------------------------
    # Cold-DM guard callout (attached to the DM surface)
    # ------------------------------------------------------------------
    GUARD_Y = 7.05
    card(
        surface_xs[0], GUARD_Y, 3.4, 0.65,
        "Cold-DM guard: first message allowed,\n"
        "further messages wait for one reply",
        ACCENT_COLOR, fc="#FEF5E7", fs=9, bold=True,
    )
    arrow(
        surface_xs[0], GUARD_Y - 0.35,
        surface_xs[0], SURFACE_Y + SURFACE_H / 2 + 0.02,
        ACCENT_COLOR, ls="--", lw=1.2,
    )

    # ------------------------------------------------------------------
    # Bottom tier — shared real-time substrate
    # ------------------------------------------------------------------
    SUB_Y = 2.6
    SUB_W, SUB_H = 9.6, 1.35
    SUB_X = LEFT_LEFT + 0.4 + SUB_W / 2

    ax.add_patch(
        FancyBboxPatch(
            (SUB_X - SUB_W / 2, SUB_Y - SUB_H / 2), SUB_W, SUB_H,
            boxstyle="round,pad=0.04",
            facecolor=PLATFORM_COLOR, edgecolor="#0E2F44",
            linewidth=2.0,
        )
    )
    ax.text(
        SUB_X, SUB_Y + 0.34, "Shared real-time substrate",
        ha="center", va="center",
        fontsize=12.5, color="white", fontweight="bold",
    )
    ax.text(
        SUB_X, SUB_Y - 0.08,
        "Per-user channels  -  per-thread channels  -  presence and typing indicators",
        ha="center", va="center",
        fontsize=9.8, color="white",
    )
    ax.text(
        SUB_X, SUB_Y - 0.42,
        "All three surfaces emit and receive on the same transport.",
        ha="center", va="center",
        fontsize=9.2, color="#D6EAF8", style="italic",
    )

    # Surface -> substrate arrows (down), labeled with the carried event.
    surface_bottom = SURFACE_Y - SURFACE_H / 2
    sub_top = SUB_Y + SUB_H / 2
    labels = [
        ("New message", DM_COLOR, surface_xs[0]),
        ("New message", GROUP_COLOR, surface_xs[1]),
        ("Notification", SYS_COLOR, surface_xs[2]),
    ]
    for lbl, col, x in labels:
        arrow(x, surface_bottom - 0.05, x, sub_top + 0.05,
              col, style="<|-|>", lw=1.5)
        ax.text(
            x + 0.08, (surface_bottom + sub_top) / 2, lbl,
            ha="left", va="center", fontsize=9, color=col,
            style="italic",
        )

    # ------------------------------------------------------------------
    # Right column — Cross-module binding
    # ------------------------------------------------------------------
    BIND_TITLE_Y = 7.05
    ax.text(
        (RIGHT_LEFT + RIGHT_RIGHT) / 2, BIND_TITLE_Y,
        "Cross-module binding",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color=BIND_COLOR,
    )
    ax.text(
        (RIGHT_LEFT + RIGHT_RIGHT) / 2, BIND_TITLE_Y - 0.34,
        "A direct message can be tied\nto a trip, listing, or activity",
        ha="center", va="center",
        fontsize=9.5, color=NEUTRAL, style="italic",
    )

    bind_x = (RIGHT_LEFT + RIGHT_RIGHT) / 2
    bind_w, bind_h = 4.4, 0.9
    bind_ys = [5.55, 4.30, 3.05]
    bind_items = [
        ("Bound to a trip",
         "DM opened from a ride card\n(passenger / driver side-channel)"),
        ("Bound to a listing",
         "DM opened from \"Contact seller\"\non a marketplace item"),
        ("Bound to an activity",
         "DM opened from an activity card\n(inquiry or update thread)"),
    ]
    for (title, body), y in zip(bind_items, bind_ys):
        card(bind_x, y, bind_w, bind_h, body, BIND_COLOR,
             fc="#F4ECF7", fs=9.0, title=title)

    # Connector from DM surface to the binding column
    arrow(
        surface_xs[0] + SURFACE_W / 2 - 0.05, SURFACE_Y,
        bind_x - bind_w / 2, bind_ys[0],
        BIND_COLOR, ls="--", lw=1.3,
    )
    arrow(
        surface_xs[0] + SURFACE_W / 2 - 0.05, SURFACE_Y - 0.25,
        bind_x - bind_w / 2, bind_ys[1],
        BIND_COLOR, ls="--", lw=1.0, mut=10,
    )
    arrow(
        surface_xs[0] + SURFACE_W / 2 - 0.05, SURFACE_Y - 0.45,
        bind_x - bind_w / 2, bind_ys[2],
        BIND_COLOR, ls="--", lw=1.0, mut=10,
    )

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Cross-module messaging substrate",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, Y_MAX - 0.3,
        "Three message surfaces share one real-time substrate; "
        "direct messages can carry the context of the module they came from.",
        ha="center", va="center", fontsize=10.5, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(Y_MIN, Y_MAX + 0.2)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_d1_messaging_substrate", dpi=300)
    register("mbe_d1_messaging_substrate", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
