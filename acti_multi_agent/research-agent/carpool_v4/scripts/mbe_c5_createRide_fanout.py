"""mbe_c5 — What happens when a driver publishes a trip.

A systems-level interaction diagram, not an engineering call-graph. Three
swim-lanes (Driver, Platform, WeChat groups) and a temporal axis to the
right.

Design principles (consistent with the rest of the `mbe_*` set):
  - No file/line references, no SQL, no programming-language artifacts.
  - User-facing outcomes only; implementation detail collapsed into platform
    actions.
  - Highlight one or two non-obvious design choices (here: shareable link
    with web fallback, batched outreach queue shared across modules).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, DRIVER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
WECHAT_COLOR = "#566573"      # the external-channel lane is intentionally faint
ACCENT_COLOR = "#F39C12"      # for the shareable-link / fallback callout


@renderer("mbe_c5_createRide_fanout")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(14, 7.0))

    # ------------------------------------------------------------------
    # Swim-lane y-coordinates
    # ------------------------------------------------------------------
    LANES = {
        "Driver":         (DRIVER_COLOR,   4.9),
        "Platform":       (PLATFORM_COLOR, 2.7),
        "WeChat groups":  (WECHAT_COLOR,   1.0),
    }
    LANE_HEIGHT = 1.15

    X_MIN, X_MAX = 0.0, 16.5
    LABEL_RIGHT = 1.5  # right edge of the lane-label strip

    # Draw lane bands. The WeChat-groups lane is faded — it is an external
    # channel, not an actor we control.
    for name, (color, y) in LANES.items():
        alpha = 0.05 if name == "WeChat groups" else 0.07
        ax.add_patch(
            FancyBboxPatch(
                (X_MIN, y - LANE_HEIGHT / 2),
                X_MAX - X_MIN, LANE_HEIGHT,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=alpha,
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
        (3.4,  "Publish moment"),
        (6.5,  "Listed instantly"),
        (9.6,  "Outreach queued"),
        (13.8, "Batched + posted"),
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
    # Lane y shortcuts
    # ------------------------------------------------------------------
    dy = LANES["Driver"][1]
    sy = LANES["Platform"][1]
    wy = LANES["WeChat groups"][1]

    # ------------------------------------------------------------------
    # 1. Driver action: publish a trip
    # ------------------------------------------------------------------
    card(3.4, dy, 3.2, 0.85,
         "Publish a trip\norigin / destination / time / seats / price",
         DRIVER_COLOR, bold=True, fs=9.2)

    # ------------------------------------------------------------------
    # 2. Platform fans out to two outcomes
    # ------------------------------------------------------------------
    # (a) Trip is listed (browsable by passengers)
    card(6.5, sy, 2.4, 0.7,
         "Trip listed\n(browsable by passengers)",
         PLATFORM_COLOR, bold=True)
    arrow(3.4, dy - 0.45, 6.0, sy + 0.32, DRIVER_COLOR)

    # (b) WeChat post queued
    card(9.6, sy, 2.5, 0.7,
         "Outreach post queued\n(text card + shareable link)",
         PLATFORM_COLOR, bold=True)
    arrow(4.5, dy - 0.45, 8.7, sy + 0.32, DRIVER_COLOR, ls="--")

    # ------------------------------------------------------------------
    # 3. Accent callout: the shareable-link / web-fallback design choice
    # Anchored above the queued-post card and tied to it with a dotted line.
    # ------------------------------------------------------------------
    card(9.6, sy + 1.25, 3.1, 0.6,
         "Shareable link with web fallback",
         ACCENT_COLOR, fc="#FEF5E7", bold=True, fs=9.5)
    ax.plot([9.6, 9.6], [sy + 0.95, sy + 0.4],
            linestyle=":", color=ACCENT_COLOR, linewidth=1.2)

    # ------------------------------------------------------------------
    # 4. Dispatch worker: drains the queue in batches
    # ------------------------------------------------------------------
    card(12.7, sy, 2.4, 0.7,
         "Dispatch worker\nbatches and sends",
         PLATFORM_COLOR)
    arrow(10.85, sy, 11.5, sy, PLATFORM_COLOR)

    # ------------------------------------------------------------------
    # 5. Posts arrive in WeChat groups
    # ------------------------------------------------------------------
    card(13.8, wy, 2.6, 0.7,
         "Trip appears in WeChat groups",
         WECHAT_COLOR)
    arrow(12.7, sy - 0.35, 13.8, wy + 0.32, PLATFORM_COLOR, ls="--")

    # ------------------------------------------------------------------
    # 6. Sibling sources feeding the same queue (snapshot finding).
    # A small bundle in the WeChat-groups lane on the left of the dispatch
    # worker, showing ride-publish is one of three sources.
    # ------------------------------------------------------------------
    sib_x = 7.5
    sib_y = wy
    sib_w, sib_h = 4.6, 0.9

    ax.add_patch(
        FancyBboxPatch(
            (sib_x - sib_w / 2, sib_y - sib_h / 2), sib_w, sib_h,
            boxstyle="round,pad=0.03",
            facecolor="#F4F6F7", edgecolor=WECHAT_COLOR, linewidth=1.0,
            alpha=0.95,
        )
    )
    ax.text(sib_x, sib_y + 0.22,
            "Same outreach queue, three sources",
            ha="center", va="center",
            fontsize=9.5, color="#1B2631", fontweight="bold")
    ax.text(sib_x, sib_y - 0.05,
            "Marketplace 62   ·   Ride 16   ·   Activities 4",
            ha="center", va="center",
            fontsize=9.0, color="#1B2631")
    ax.text(sib_x, sib_y - 0.27,
            "(snapshot of 82 outbound posts)",
            ha="center", va="center",
            fontsize=8.5, color="#566573", style="italic")

    # Tie the sibling-source bundle into the dispatch worker (it consumes
    # from the shared queue).
    arrow(sib_x + sib_w / 2, sib_y,
          12.0, sy - 0.35, WECHAT_COLOR, ls=":", lw=1.1)

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "What happens when a driver publishes a trip",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        8.3, 6.05,
        "Publishing fans out to an in-app listing and an outreach post; "
        "the post carries a shareable link with a web fallback so it opens "
        "for users without the mini-program.",
        ha="center", va="center", fontsize=10, style="italic",
        color="#566573",
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.6, 6.3)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_c5_createRide_fanout", dpi=300)
    register("mbe_c5_createRide_fanout", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
