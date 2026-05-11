"""mbe_d3 — WeChat outreach pipeline (grassroots-to-platform bridge).

A systems-level LR pipeline showing how three internal producers fan into a
single outreach queue, get batched, and arrive at external WeChat groups.
Implementation detail (table names, endpoint paths, code lines, SQL) is
collapsed into design-intent labels per the unified style guide.

Design choices we surface explicitly:
  - Shareable links built with a web fallback (deep-link to mini-program;
    if the link API fails, the message still ships with a plain web URL).
  - Batching is event-driven, not on a clock: dispatch when 3+ posts are
    pending, or when the oldest pending post is over 24 hours old.

Snapshot finding (2026-04-23): 82 posts (62 marketplace, 16 ride, 4
activity), 2026-01-17 → 2026-04-11. Marketplace dominates outbound
outreach but yielded zero buyer activity — cross-posting works but
organic uptake hasn't followed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


PLATFORM_COLOR = "#1A5276"   # navy — platform internals (queue, dispatcher)
PRODUCER_COLOR = "#2980B9"   # blue — producer events
SINK_COLOR = "#C0392B"       # red — external sink (WeChat groups)
ACCENT_COLOR = "#F39C12"     # orange — design highlight
NEUTRAL = "#566573"


@renderer("mbe_d3_wechat_outreach_pipeline")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(15, 8.0))

    X_MIN, X_MAX = 0.0, 16.5
    Y_MIN, Y_MAX = -1.6, 7.6

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=10,
             bold=False, alpha=1.0):
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

    # ------------------------------------------------------------------
    # Column x-positions
    # ------------------------------------------------------------------
    X_PROD = 2.2
    X_QUEUE = 6.4
    X_DISPATCH = 10.6
    X_SINK = 14.6

    # ------------------------------------------------------------------
    # Producer cards (left column)
    # ------------------------------------------------------------------
    PROD_W, PROD_H = 3.2, 0.95
    Y_TRIP = 4.8
    Y_LIST = 3.2
    Y_ACT = 1.6

    card(X_PROD, Y_TRIP, PROD_W, PROD_H,
         "New trip posted\n(rideshare)", PRODUCER_COLOR, bold=True)
    card(X_PROD, Y_LIST, PROD_W, PROD_H,
         "New marketplace listing\n(buy / sell)", PRODUCER_COLOR, bold=True)
    card(X_PROD, Y_ACT, PROD_W, PROD_H,
         "New activity published\n(events)", PRODUCER_COLOR, bold=True)

    ax.text(
        X_PROD, 5.75,
        "Producers",
        ha="center", va="center", fontsize=11, fontweight="bold",
        color=PRODUCER_COLOR,
    )

    # ------------------------------------------------------------------
    # Queue (center-left)
    # ------------------------------------------------------------------
    QUEUE_W, QUEUE_H = 3.0, 1.4
    Y_QUEUE = 3.2
    card(X_QUEUE, Y_QUEUE, QUEUE_W, QUEUE_H,
         "Outreach queue\n(pending posts,\nawaiting dispatch)",
         PLATFORM_COLOR, bold=True)

    ax.text(
        X_QUEUE, 5.75,
        "Platform",
        ha="center", va="center", fontsize=11, fontweight="bold",
        color=PLATFORM_COLOR,
    )

    # Snapshot annotation under the queue (shifted right of the
    # accent dotted line so they don't cross)
    ax.text(
        X_QUEUE + 0.6, Y_QUEUE - 1.4,
        "Snapshot (2026-04-23): 82 posts\n"
        "62 marketplace, 16 ride, 4 activity\n"
        "2026-01-17 to 2026-04-11",
        ha="center", va="center", fontsize=9, color=NEUTRAL, style="italic",
    )

    # ------------------------------------------------------------------
    # Shareable link callout (accent) — design highlight
    # Sits along the producer -> queue path; producers append a deep-link
    # to message text while building outreach content. Drawn as one
    # callout attached via a dotted accent line to the queue intake.
    # ------------------------------------------------------------------
    LINK_W, LINK_H = 3.4, 1.05
    X_LINK = X_PROD + 0.4   # slightly right of producer column, below it
    Y_LINK = 0.0
    card(
        X_LINK, Y_LINK, LINK_W, LINK_H,
        "Build shareable link\nWeChat short link API,\n"
        "with plain web URL as fallback",
        ACCENT_COLOR, fc="#FEF5E7", bold=True, fs=9.5,
    )
    # Dotted accent line from the link callout up to the queue's left edge
    # (intake side). Routed to avoid crossing the snapshot annotation.
    arrow(X_LINK + LINK_W / 2 - 0.3, Y_LINK + LINK_H / 2,
          X_QUEUE - QUEUE_W / 2 - 0.05, Y_QUEUE - 0.45,
          ACCENT_COLOR, ls=":", lw=1.1)
    ax.text(
        X_LINK, Y_LINK + LINK_H / 2 + 0.25,
        "Design choice",
        ha="center", va="center", fontsize=9, color=ACCENT_COLOR,
        style="italic", fontweight="bold",
    )

    # ------------------------------------------------------------------
    # Producer -> Queue arrows
    # ------------------------------------------------------------------
    for y in (Y_TRIP, Y_LIST, Y_ACT):
        arrow(X_PROD + PROD_W / 2, y,
              X_QUEUE - QUEUE_W / 2, Y_QUEUE,
              PRODUCER_COLOR)

    # Volume labels next to producer→queue arrows
    ax.text(
        (X_PROD + X_QUEUE) / 2 + 0.3, (Y_TRIP + Y_QUEUE) / 2 + 0.55,
        "16", ha="center", va="center", fontsize=9, color=PRODUCER_COLOR,
        fontweight="bold",
    )
    ax.text(
        (X_PROD + X_QUEUE) / 2 + 0.3, Y_QUEUE + 0.18,
        "62", ha="center", va="center", fontsize=10, color=PRODUCER_COLOR,
        fontweight="bold",
    )
    ax.text(
        (X_PROD + X_QUEUE) / 2 + 0.3, (Y_ACT + Y_QUEUE) / 2 - 0.55,
        "4", ha="center", va="center", fontsize=9, color=PRODUCER_COLOR,
        fontweight="bold",
    )

    # ------------------------------------------------------------------
    # Batch dispatcher (center-right)
    # ------------------------------------------------------------------
    DISP_W, DISP_H = 3.4, 1.7
    Y_DISP = 3.2
    card(X_DISPATCH, Y_DISP, DISP_W, DISP_H,
         "Batch dispatcher\n\n"
         "Sends a batch when\n"
         "3+ posts are pending,\n"
         "or oldest is over 24 h old",
         PLATFORM_COLOR, bold=True)

    arrow(X_QUEUE + QUEUE_W / 2, Y_QUEUE,
          X_DISPATCH - DISP_W / 2, Y_DISP,
          PLATFORM_COLOR, lw=1.6)
    ax.text(
        (X_QUEUE + X_DISPATCH) / 2, Y_QUEUE + 0.35,
        "pull pending",
        ha="center", va="center", fontsize=9, color=NEUTRAL, style="italic",
    )

    # ------------------------------------------------------------------
    # External WeChat groups sink (right)
    # ------------------------------------------------------------------
    SINK_W, SINK_H = 3.4, 1.7
    Y_SINK = 3.2
    card(X_SINK, Y_SINK, SINK_W, SINK_H,
         "External WeChat groups\n(Cornell student channels)\n\n"
         "Authors curate; out-of-band\nfrom platform identity check",
         SINK_COLOR, bold=True)

    ax.text(
        X_SINK, 5.75,
        "External",
        ha="center", va="center", fontsize=11, fontweight="bold",
        color=SINK_COLOR,
    )

    arrow(X_DISPATCH + DISP_W / 2, Y_DISP,
          X_SINK - SINK_W / 2, Y_SINK,
          SINK_COLOR, lw=1.6)
    ax.text(
        (X_DISPATCH + X_SINK) / 2, Y_DISP + 0.35,
        "merged post",
        ha="center", va="center", fontsize=9, color=NEUTRAL, style="italic",
    )

    # ------------------------------------------------------------------
    # Title + italic subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "WeChat outreach pipeline: bridging platform events to grassroots groups",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 6.55,
        "Three producers fan into one outreach queue; a batch dispatcher "
        "pushes merged posts to external groups.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Bottom italic finding
    ax.text(
        (X_MIN + X_MAX) / 2, -1.15,
        "Marketplace dominates outbound outreach (62/82) but yielded zero "
        "buyer activity: cross-posting works, organic uptake has not yet followed.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_d3_wechat_outreach_pipeline", dpi=300)
    register("mbe_d3_wechat_outreach_pipeline", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
