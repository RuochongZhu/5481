"""mbe_c4 — Geo-Verified Activity Check-in Pipeline.

A conceptual check-in funnel for HCI readers. The participant moves from
left to right through two design gates (time window, distance), then is
either checked in (and rewarded) or quietly turned away. Spoof attempts
leave a forensic trail by design.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer, RIDER_COLOR,
)


PLATFORM_COLOR = "#1A5276"
ACCENT_COLOR = "#F39C12"
NEUTRAL = "#566573"
REJECT_TINT = "#B0B7BC"


@renderer("mbe_c4_geo_checkin_pipeline")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

    fig, ax = plt.subplots(figsize=(14, 6.0))

    X_MIN, X_MAX = 0.0, 16.0
    Y_MAIN = 3.2          # main funnel row
    Y_REJECT = 1.5        # quiet rejection row (faint)
    Y_FORENSIC = 4.9      # side annotation row

    # ------------------------------------------------------------------
    # Funnel band: a faint wide-to-narrow polygon behind the main row
    # ------------------------------------------------------------------
    funnel = Polygon(
        [
            (0.6, Y_MAIN + 1.05),
            (15.4, Y_MAIN + 0.45),
            (15.4, Y_MAIN - 0.45),
            (0.6, Y_MAIN - 1.05),
        ],
        closed=True,
        facecolor=RIDER_COLOR, alpha=0.05,
        edgecolor=RIDER_COLOR, linewidth=0.8,
    )
    ax.add_patch(funnel)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(x, y, w, h, text, color, *, fc="white", fs=10.0,
             alpha=1.0, bold=False, text_color="#1B2631"):
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
            fontsize=fs, color=text_color,
            fontweight="bold" if bold else "normal",
        )

    def diamond(x, y, w, h, text, *, color=ACCENT_COLOR,
                fc="#FEF5E7", fs=9.5):
        pts = [(x, y + h / 2), (x + w / 2, y),
               (x, y - h / 2), (x - w / 2, y)]
        ax.add_patch(
            Polygon(pts, closed=True,
                    facecolor=fc, edgecolor=color, linewidth=1.6)
        )
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fs, color="#1B2631",
            fontweight="bold",
        )

    def arrow(x0, y0, x1, y1, color, *, lw=1.4, ls="-", alpha=1.0,
              style="-|>"):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle=style, color=color,
                linewidth=lw, linestyle=ls,
                mutation_scale=12, alpha=alpha,
            )
        )

    # ------------------------------------------------------------------
    # Stage positions along the funnel (5 main stages)
    # ------------------------------------------------------------------
    # 1. Open app  -> 2. Registered? -> 3. Time window -> 4. Distance ->
    # 5. Checked in + small reward
    STAGES = [
        # (x, kind, payload)
        (1.7, "card",    "Participant\nopens app", RIDER_COLOR, True),
        (4.6, "card",    "Registered\nfor this activity?", PLATFORM_COLOR, False),
        (7.8, "diamond", "Within\ncheck-in window\n(~±30 min)"),
        (10.9, "diamond", "At the venue\n(within ~100 m)"),
        (14.2, "card",   "Checked in\n+ small reward", ACCENT_COLOR, True),
    ]

    # Stage 1: open app (rider color)
    card(1.7, Y_MAIN, 2.1, 0.95, "Participant\nopens app",
         RIDER_COLOR, bold=True)

    # Stage 2: registered? (platform gate)
    card(4.6, Y_MAIN, 2.2, 0.95, "Registered\nfor this activity?",
         PLATFORM_COLOR, bold=True)

    # Stage 3: time-window gate (accent diamond)
    diamond(7.8, Y_MAIN, 2.5, 1.4,
            "Within check-in window\n(~±30 min around\nstart / end)")

    # Stage 4: distance gate (accent diamond)
    diamond(10.9, Y_MAIN, 2.4, 1.4,
            "At the venue\n(within ~100 m)")

    # Stage 5: success terminal (accent fill)
    card(14.2, Y_MAIN, 2.4, 0.95,
         "Check-in record\n+ small reward",
         ACCENT_COLOR, fc="#FEF5E7", bold=True)

    # ------------------------------------------------------------------
    # Forward arrows along the main funnel
    # ------------------------------------------------------------------
    arrow(2.85, Y_MAIN, 3.45, Y_MAIN, NEUTRAL)
    arrow(5.85, Y_MAIN, 6.45, Y_MAIN, NEUTRAL)
    arrow(9.20, Y_MAIN, 9.55, Y_MAIN, NEUTRAL)
    arrow(12.25, Y_MAIN, 12.95, Y_MAIN, NEUTRAL)

    # ------------------------------------------------------------------
    # Reject lane (faint) — three quiet rejection paths
    # ------------------------------------------------------------------
    reject_label = "Quietly turned away"
    # Reject hub on the lower row
    card(7.8, Y_REJECT, 3.3, 0.7, reject_label, REJECT_TINT,
         fc="#F4F6F7", fs=9.5, text_color=NEUTRAL)

    # 2 -> reject (not registered)
    arrow(4.6, Y_MAIN - 0.5, 6.4, Y_REJECT + 0.35, REJECT_TINT,
          ls=(0, (3, 3)), alpha=0.9)
    ax.text(5.3, (Y_MAIN + Y_REJECT) / 2 + 0.05,
            "not registered", ha="center", va="center",
            fontsize=8.5, color=NEUTRAL, style="italic")

    # 3 -> reject (outside window)
    arrow(7.8, Y_MAIN - 0.7, 7.8, Y_REJECT + 0.36, REJECT_TINT,
          ls=(0, (3, 3)), alpha=0.9)
    ax.text(8.32, (Y_MAIN + Y_REJECT) / 2,
            "outside window", ha="left", va="center",
            fontsize=8.5, color=NEUTRAL, style="italic")

    # 4 -> reject (too far)
    arrow(10.9, Y_MAIN - 0.7, 9.3, Y_REJECT + 0.35, REJECT_TINT,
          ls=(0, (3, 3)), alpha=0.9)
    ax.text(10.35, (Y_MAIN + Y_REJECT) / 2 + 0.05,
            "too far away", ha="center", va="center",
            fontsize=8.5, color=NEUTRAL, style="italic")

    # ------------------------------------------------------------------
    # Forensic-trail side annotation (small, off to the side)
    # ------------------------------------------------------------------
    # Anchored above the distance gate (where spoof attempts are most likely).
    forensic_x = 10.9
    ax.add_patch(
        FancyBboxPatch(
            (forensic_x - 2.05, Y_FORENSIC - 0.35), 4.1, 0.7,
            boxstyle="round,pad=0.04",
            facecolor="#FEF9E7", edgecolor=ACCENT_COLOR, linewidth=1.0,
        )
    )
    ax.text(
        forensic_x, Y_FORENSIC,
        "Spoof attempts captured: device + IP\n"
        "(privacy-respecting forensic trail)",
        ha="center", va="center",
        fontsize=8.8, color="#7D6608", style="italic",
    )
    arrow(forensic_x, Y_FORENSIC - 0.38,
          forensic_x, Y_MAIN + 0.72,
          ACCENT_COLOR, ls=(0, (2, 2)), lw=1.0, alpha=0.8,
          style="-")

    # ------------------------------------------------------------------
    # Stage labels along the bottom (a thin guide axis)
    # ------------------------------------------------------------------
    y_axis = 0.45
    ax.plot([0.6, 15.4], [y_axis, y_axis],
            color=NEUTRAL, linewidth=0.8, alpha=0.6)
    STAGE_TICKS = [
        (1.7, "1. Open app"),
        (4.6, "2. Identity gate"),
        (7.8, "3. Time gate"),
        (10.9, "4. Distance gate"),
        (14.2, "5. Confirm + reward"),
    ]
    for x, lbl in STAGE_TICKS:
        ax.plot([x, x], [y_axis - 0.05, y_axis + 0.05],
                color=NEUTRAL, linewidth=0.8, alpha=0.6)
        ax.text(x, y_axis - 0.18, lbl,
                ha="center", va="top", fontsize=9, color=NEUTRAL,
                style="italic")

    # ------------------------------------------------------------------
    # Snapshot footer (formative, no production check-ins yet)
    # ------------------------------------------------------------------
    ax.text(
        8.0, -0.35,
        "Snapshot: 0 check-ins recorded in production "
        "(formative; design exists ahead of deployment)",
        ha="center", va="center",
        fontsize=9, color=NEUTRAL, style="italic",
    )

    # ------------------------------------------------------------------
    # Title + italic subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Geo-verified activity check-in",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.text(
        8.0, 5.85,
        "Two lightweight gates (time window, venue distance) keep check-in "
        "cheap to pass for honest participants while leaving a forensic "
        "trail for spoof attempts.",
        ha="center", va="center", fontsize=10, style="italic",
        color=NEUTRAL,
    )

    # Cosmetic
    ax.set_xlim(X_MIN - 0.2, X_MAX + 0.2)
    ax.set_ylim(-0.7, 6.3)
    ax.set_aspect("auto")
    ax.axis("off")

    pdf, png = save_mpl("mbe_c4_geo_checkin_pipeline", dpi=300)
    register("mbe_c4_geo_checkin_pipeline", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
