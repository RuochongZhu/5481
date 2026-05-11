"""mbe_d2 -- Points sources, ledger, and sinks (paper-ready, matplotlib LR fan).

Design principles (per `_mbe_style_guide.md`):
  - matplotlib swim-flow, not graphviz.
  - English labels only; no SQL, no method names, no error codes, no file:line.
  - Top red callout: production-reality flag.
  - Bottom italic subtitle: design rationale (F4 finding 48.3 < 63.6).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


PLATFORM_COLOR = "#1A5276"   # navy — the platform / ledger
ACCENT_COLOR = "#F39C12"     # orange — design highlight
SOURCE_COLOR = "#1E8449"     # green — earning
SINK_COLOR = "#B9540B"       # burnt orange — spending
FLAG_RED = "#922B21"         # red — production-reality callout
GREY = "#566573"             # neutral text / subtitle


@renderer("mbe_d2_points_award_deduct")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(15, 8.2))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=9.5,
             alpha=1.0, bold=False, fontcolor="#1B2631"):
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
            fontsize=fs, color=fontcolor,
            fontweight="bold" if bold else "normal",
            wrap=True,
        )

    def cluster_band(x, y, w, h, color, label, *, fs=11):
        # Faint background band per source-cluster.
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=0.08,
                edgecolor=color, linewidth=0.8,
            )
        )
        # Label sits ABOVE the band, not inside (avoids card overlap).
        ax.text(
            x, y + h / 2 + 0.10, label,
            ha="center", va="bottom",
            fontsize=fs, fontweight="bold", color=color,
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.2, ls="-", alpha=0.85):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle="-|>", color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=12, alpha=alpha,
            )
        )

    # ------------------------------------------------------------------
    # Canvas extent
    # ------------------------------------------------------------------
    X_MIN, X_MAX = 0.0, 18.0
    Y_MIN, Y_MAX = 0.0, 10.0

    # ------------------------------------------------------------------
    # TOP: production-reality flag (red callout)
    # ------------------------------------------------------------------
    flag_y = 9.35
    ax.add_patch(
        FancyBboxPatch(
            (1.0, flag_y - 0.45), X_MAX - 2.0, 0.9,
            boxstyle="round,pad=0.04",
            facecolor="#FDEDEC", edgecolor=FLAG_RED, linewidth=2.0,
        )
    )
    ax.text(
        X_MAX / 2, flag_y + 0.10,
        "Not yet provisioned in production  -  design ready, behaviorally inert",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color=FLAG_RED,
    )
    ax.text(
        X_MAX / 2, flag_y - 0.22,
        "Zero earning rules active  |  ledger not provisioned  |  all 184 verified users carry a zero balance",
        ha="center", va="center",
        fontsize=9.5, color=FLAG_RED, style="italic",
    )

    # ------------------------------------------------------------------
    # LEFT: source clusters (3 sub-clusters)
    # ------------------------------------------------------------------
    SRC_X = 2.5
    SRC_W = 3.4

    # System bonuses cluster
    sys_y, sys_band_h = 7.20, 1.70
    cluster_band(SRC_X, sys_y, SRC_W + 0.3, sys_band_h,
                 SOURCE_COLOR, "System bonuses")
    sys_items = [
        (sys_y + 0.50, "Registration bonus"),
        (sys_y + 0.00, "Profile completion bonus"),
        (sys_y - 0.50, "Daily login bonus"),
    ]
    for yy, lbl in sys_items:
        card(SRC_X, yy, SRC_W, 0.42, lbl, SOURCE_COLOR, fs=9.5)

    # Activity rewards cluster
    act_y, act_band_h = 5.05, 1.70
    cluster_band(SRC_X, act_y, SRC_W + 0.3, act_band_h,
                 SOURCE_COLOR, "Activity rewards")
    act_items = [
        (act_y + 0.50, "Activity participation"),
        (act_y + 0.00, "Activity check-in reward"),
        (act_y - 0.50, "Streak bonus (consecutive days)"),
    ]
    for yy, lbl in act_items:
        card(SRC_X, yy, SRC_W, 0.42, lbl, SOURCE_COLOR, fs=9.5)

    # Trip & community rewards cluster
    trip_y, trip_band_h = 2.90, 1.70
    cluster_band(SRC_X, trip_y, SRC_W + 0.3, trip_band_h,
                 SOURCE_COLOR, "Trip & community rewards")
    trip_items = [
        (trip_y + 0.50, "Ride completion"),
        (trip_y + 0.00, "Marketplace transaction"),
        (trip_y - 0.50, "Referral bonus"),
    ]
    for yy, lbl in trip_items:
        card(SRC_X, yy, SRC_W, 0.42, lbl, SOURCE_COLOR, fs=9.5)

    # ------------------------------------------------------------------
    # CENTER: Points ledger (atomic balance update)
    # ------------------------------------------------------------------
    LED_X = 9.0
    LED_Y = 5.05
    LED_W = 4.2
    LED_H = 1.9
    ax.add_patch(
        FancyBboxPatch(
            (LED_X - LED_W / 2, LED_Y - LED_H / 2), LED_W, LED_H,
            boxstyle="round,pad=0.04",
            facecolor=PLATFORM_COLOR, edgecolor="#0E2F44", linewidth=2.4,
        )
    )
    ax.text(
        LED_X, LED_Y + 0.42,
        "Points ledger",
        ha="center", va="center",
        fontsize=14, fontweight="bold", color="white",
    )
    ax.text(
        LED_X, LED_Y + 0.02,
        "atomic balance update",
        ha="center", va="center",
        fontsize=10.5, color="white", style="italic",
    )
    ax.text(
        LED_X, LED_Y - 0.45,
        "earn  +  spend  ->  user balance",
        ha="center", va="center",
        fontsize=9.5, color="#D4E6F1",
    )

    # ------------------------------------------------------------------
    # RIGHT: sinks
    # ------------------------------------------------------------------
    SINK_X = 15.3
    SINK_W = 3.5

    sink_y_top = 5.85
    sink_y_bot = 4.25

    # Cluster band around sinks (drawn first so cards sit on top)
    cluster_band(SINK_X, 5.05, SINK_W + 0.4, 2.6, SINK_COLOR, "Sinks")

    card(SINK_X, sink_y_top, SINK_W, 0.95,
         "Coupons\n(redeem for discounts)",
         SINK_COLOR, fs=10.5, bold=True)
    card(SINK_X, sink_y_bot, SINK_W, 0.95,
         "Pay-with-points\n(activity entry fees)",
         SINK_COLOR, fs=10.5, bold=True)

    # ------------------------------------------------------------------
    # Arrows: sources -> ledger (fan-in)
    # ------------------------------------------------------------------
    src_right_x = SRC_X + SRC_W / 2 + 0.05
    led_left_x = LED_X - LED_W / 2 - 0.05
    for cluster_center_y in (sys_y, act_y, trip_y):
        for offset in (0.50, 0.00, -0.50):
            arrow(src_right_x, cluster_center_y + offset,
                  led_left_x, LED_Y,
                  SOURCE_COLOR, lw=1.0, alpha=0.65)

    # Arrows: ledger -> sinks (fan-out)
    led_right_x = LED_X + LED_W / 2 + 0.05
    sink_left_x = SINK_X - SINK_W / 2 - 0.05
    arrow(led_right_x, LED_Y + 0.20, sink_left_x, sink_y_top,
          SINK_COLOR, lw=1.6)
    arrow(led_right_x, LED_Y - 0.20, sink_left_x, sink_y_bot,
          SINK_COLOR, lw=1.6)

    # Earn / spend captions on the central pipes
    ax.text(
        (src_right_x + led_left_x) / 2, LED_Y + LED_H / 2 + 0.30,
        "earn",
        ha="center", va="bottom",
        fontsize=11, color=SOURCE_COLOR, fontweight="bold", style="italic",
    )
    ax.text(
        (led_right_x + sink_left_x) / 2, LED_Y + LED_H / 2 + 0.30,
        "spend",
        ha="center", va="bottom",
        fontsize=11, color=SINK_COLOR, fontweight="bold", style="italic",
    )

    # ------------------------------------------------------------------
    # Accent callout: design choice (cap below cash price)
    # ------------------------------------------------------------------
    callout_x, callout_y = LED_X, 2.55
    callout_w, callout_h = 6.6, 0.85
    ax.add_patch(
        FancyBboxPatch(
            (callout_x - callout_w / 2, callout_y - callout_h / 2),
            callout_w, callout_h,
            boxstyle="round,pad=0.04",
            facecolor="#FEF5E7", edgecolor=ACCENT_COLOR, linewidth=1.6,
        )
    )
    ax.text(
        callout_x, callout_y,
        "Design choice: point value capped well below per-seat cash price\n"
        "so points complement (not substitute) financial motivation",
        ha="center", va="center",
        fontsize=10, color="#7E5109", fontweight="bold",
    )
    # Dotted tether from ledger down to callout
    ax.plot([callout_x, callout_x],
            [LED_Y - LED_H / 2 - 0.05, callout_y + callout_h / 2 + 0.02],
            linestyle=":", color=ACCENT_COLOR, linewidth=1.2)

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Points: sources, ledger, and sinks",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        X_MAX / 2, 8.55,
        "Earning fans in from system, activity, and trip rewards; spending fans out "
        "to coupons and pay-with-points entry fees.",
        ha="center", va="center", fontsize=10.5, style="italic", color=GREY,
    )

    # Bottom rationale subtitle (italic grey, F4 finding)
    ax.text(
        X_MAX / 2, 0.55,
        "Design rationale: gamification ranked 48.3 vs financial 63.6 (F4) — points are "
        "intentionally a complement to cash, not a replacement.",
        ha="center", va="center",
        fontsize=10, style="italic", color=GREY,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(Y_MIN - 0.2, Y_MAX + 0.1)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_d2_points_award_deduct", dpi=300)
    register("mbe_d2_points_award_deduct", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
