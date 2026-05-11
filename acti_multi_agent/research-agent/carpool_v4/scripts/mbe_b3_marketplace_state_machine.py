"""mbe_b3 — Marketplace item lifecycle and listing-creation side effects.

Left cluster: a three-state lifecycle for marketplace items
  active -> sold (final)
  active -> removed (final, soft-delete preserves comment threads and
                     rating history)

Right cluster: four named side-effects fired when a new listing is created
  - WeChat post queued for outreach
  - Aggregate counters initialised (views, favorites)
  - Comment threads enabled (soft-delete preserves discussion)
  - Cross-module direct-message contact thread to the seller

Snapshot reported in the figure: 15 items live in production, all in the
removed state; 12 cumulative views, zero favorites, zero comments. Safety
mechanisms for this module are not yet implemented and therefore not shown.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


PLATFORM_COLOR = "#1A5276"   # navy — platform spine
ACTIVE_COLOR   = "#1E8449"   # green — live listing
TERMINAL_COLOR = "#566573"   # cool grey — terminal states / neutral text
ACCENT_COLOR   = "#F39C12"   # orange — design highlight (soft-delete)
SIDE_COLOR     = "#B9770E"   # amber-brown — side-effects cluster


@renderer("mbe_b3_marketplace_state_machine")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 7.0))

    # ------------------------------------------------------------------
    # Canvas
    # ------------------------------------------------------------------
    X_MIN, X_MAX = 0.0, 16.0
    Y_MIN, Y_MAX = 0.0, 7.6

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, edge_color, *, fc="white", fs=10.0,
             bold=False, alpha=1.0):
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.04",
                facecolor=fc, edgecolor=edge_color, linewidth=1.4,
                alpha=alpha,
            )
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold" if bold else "normal",
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.4, ls="-"):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=14,
            )
        )

    # ------------------------------------------------------------------
    # LEFT cluster band: item state machine
    # ------------------------------------------------------------------
    LX0, LX1 = 0.3, 7.6
    LY0, LY1 = 0.6, 6.0
    ax.add_patch(
        FancyBboxPatch(
            (LX0, LY0), LX1 - LX0, LY1 - LY0,
            boxstyle="round,pad=0.02",
            facecolor=PLATFORM_COLOR, alpha=0.06,
            edgecolor=PLATFORM_COLOR, linewidth=0.8,
        )
    )
    ax.text(
        LX0 + 0.25, LY1 - 0.25,
        "Item state machine",
        ha="left", va="top",
        fontsize=11.5, fontweight="bold", color=PLATFORM_COLOR,
    )
    ax.text(
        LX0 + 0.25, LY1 - 0.65,
        "snapshot: 15 listings in production, all currently removed",
        ha="left", va="top",
        fontsize=9.0, style="italic", color="#566573",
    )

    # Start dot
    sx, sy = 1.05, 3.2
    ax.add_patch(
        plt.Circle((sx, sy), 0.18, facecolor="black",
                   edgecolor="black", zorder=3)
    )
    ax.text(sx, sy - 0.45, "new listing",
            ha="center", va="top", fontsize=9, color="#566573",
            style="italic")

    # active state
    ax_x, ax_y = 3.1, 3.2
    card(ax_x, ax_y, 2.1, 1.05,
         "active\nvisible to browsers",
         ACTIVE_COLOR, bold=True)

    # sold state (terminal)
    so_x, so_y = 6.1, 4.4
    card(so_x, so_y, 1.9, 0.95,
         "sold\n(final)",
         TERMINAL_COLOR, bold=True)
    # outer ring to mark terminal
    ax.add_patch(
        FancyBboxPatch(
            (so_x - 1.04, so_y - 0.55), 2.08, 1.10,
            boxstyle="round,pad=0.04",
            facecolor="none", edgecolor=TERMINAL_COLOR,
            linewidth=0.8, linestyle="--",
        )
    )

    # removed state (terminal, soft-delete highlight)
    rm_x, rm_y = 6.1, 1.95
    card(rm_x, rm_y, 1.9, 1.10,
         "removed\n(final, soft-delete)",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)
    ax.add_patch(
        FancyBboxPatch(
            (rm_x - 1.04, rm_y - 0.62), 2.08, 1.24,
            boxstyle="round,pad=0.04",
            facecolor="none", edgecolor=ACCENT_COLOR,
            linewidth=0.8, linestyle="--",
        )
    )

    # transitions
    arrow(sx + 0.20, sy, ax_x - 1.07, ax_y, ACTIVE_COLOR, lw=1.6)
    ax.text((sx + ax_x) / 2.0 - 0.15, sy + 0.30,
            "create",
            ha="center", va="bottom",
            fontsize=9.5, color=ACTIVE_COLOR, style="italic")

    arrow(ax_x + 0.7, ax_y + 0.45, so_x - 1.0, so_y - 0.30,
          TERMINAL_COLOR, lw=1.5)
    ax.text(4.55, 3.95, "seller marks sold",
            ha="center", va="center",
            fontsize=9.0, color=TERMINAL_COLOR, style="italic",
            rotation=22)

    arrow(ax_x + 0.7, ax_y - 0.45, rm_x - 1.0, rm_y + 0.30,
          ACCENT_COLOR, lw=1.5)
    ax.text(4.55, 2.45, "seller removes",
            ha="center", va="center",
            fontsize=9.0, color=ACCENT_COLOR, style="italic",
            rotation=-22)

    # Soft-delete note attached to "removed"
    ax.text(
        rm_x, rm_y - 0.95,
        "soft-delete keeps comment threads\nand past rating history intact",
        ha="center", va="top",
        fontsize=8.8, color="#566573", style="italic",
    )

    # ------------------------------------------------------------------
    # RIGHT cluster band: side effects on create
    # ------------------------------------------------------------------
    RX0, RX1 = 8.4, 15.7
    RY0, RY1 = 0.6, 6.0
    ax.add_patch(
        FancyBboxPatch(
            (RX0, RY0), RX1 - RX0, RY1 - RY0,
            boxstyle="round,pad=0.02",
            facecolor=SIDE_COLOR, alpha=0.06,
            edgecolor=SIDE_COLOR, linewidth=0.8,
        )
    )
    ax.text(
        RX0 + 0.25, RY1 - 0.25,
        "Side effects on create",
        ha="left", va="top",
        fontsize=11.5, fontweight="bold", color=SIDE_COLOR,
    )
    ax.text(
        RX0 + 0.25, RY1 - 0.65,
        "fired the moment a listing becomes active",
        ha="left", va="top",
        fontsize=9.0, style="italic", color="#566573",
    )

    # Four side-effect cards stacked
    cx = (RX0 + RX1) / 2.0
    cw = (RX1 - RX0) - 0.9
    ch = 0.95
    rows_y = [4.55, 3.45, 2.35, 1.25]
    side_specs = [
        (
            "WeChat post queued",
            "outreach to external groups\nvia mini-program or web link",
        ),
        (
            "View and favorite counters",
            "initialised at zero; updated as\nshoppers browse and bookmark",
        ),
        (
            "Comment threads enabled",
            "shoppers can ask questions;\nthreads survive item removal",
        ),
        (
            "Cross-module contact thread",
            "tap-to-message opens a direct\nthread with the seller",
        ),
    ]
    for y, (title, body) in zip(rows_y, side_specs):
        ax.add_patch(
            FancyBboxPatch(
                (cx - cw / 2, y - ch / 2), cw, ch,
                boxstyle="round,pad=0.04",
                facecolor="white", edgecolor=SIDE_COLOR, linewidth=1.4,
            )
        )
        ax.text(
            cx - cw / 2 + 0.18, y + 0.22, title,
            ha="left", va="center",
            fontsize=10.5, fontweight="bold", color="#1B2631",
        )
        ax.text(
            cx - cw / 2 + 0.18, y - 0.18, body,
            ha="left", va="center",
            fontsize=9.5, color="#1B2631",
        )

    # Trigger arrow: lift straight up from "active" before turning right,
    # so we never cross the sold/removed terminal cards. The bridge runs
    # in the white strip between the cluster bands and the subtitle.
    bridge_y = 6.25
    lift_x = ax_x  # rise directly above the active card
    drop_x = RX0 + 0.45
    arrow(ax_x, ax_y + 0.55, lift_x, bridge_y - 0.05,
          SIDE_COLOR, lw=1.4, ls="--")
    arrow(lift_x, bridge_y, drop_x, bridge_y,
          SIDE_COLOR, lw=1.4, ls="--")
    arrow(drop_x, bridge_y, drop_x, RY1 - 0.05,
          SIDE_COLOR, lw=1.4, ls="--")
    ax.text(
        (lift_x + drop_x) / 2.0, bridge_y + 0.18,
        "on create, fan out to side effects",
        ha="center", va="bottom",
        fontsize=9.5, color=SIDE_COLOR, style="italic",
    )

    # ------------------------------------------------------------------
    # Snapshot strip across the bottom
    # ------------------------------------------------------------------
    ax.text(
        (X_MIN + X_MAX) / 2.0, 0.25,
        "Production snapshot:  15 listings, all removed   "
        "12 views   0 favorites   0 comments",
        ha="center", va="center",
        fontsize=10.0, color="#566573",
    )

    # ------------------------------------------------------------------
    # Title + design-intent subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Marketplace item lifecycle and listing-creation side effects",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2.0, 6.85,
        "Soft-delete keeps social context (comments, ratings) alive after "
        "an item leaves the market; one create event fans out to four "
        "cross-module side effects.",
        ha="center", va="center", fontsize=10, style="italic",
        color="#566573",
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(Y_MIN - 0.2, Y_MAX + 0.2)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_b3_marketplace_state_machine", dpi=300)
    register("mbe_b3_marketplace_state_machine", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
