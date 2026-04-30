"""mbe_c3 — Rating Window Timeline + Submission Flow.

Two-panel matplotlib figure documenting the 2-hour post-departure
rating-readiness delay and the rating-submission upsert path.

  Top panel (ax1):  Horizontal timeline anchored to `departure_time`
                    semantics, showing the three time zones (pre-departure
                    grey / during-trip yellow / open-window green) and
                    annotated key events (T0 bookRide fan-out, T_dep ride,
                    T_dep + 2h readiness gate via RATING_READY_DELAY_MS,
                    T_dep + 7d revisable upsert).
  Bottom panel (ax2): Horizontal flow with all 4 guards, the UPSERT step,
                    and the migration-008 rating-aggregation trigger.

Source-of-truth:
  campusride-backend/src/controllers/rating.controller.js:22-100
  campusride-backend/src/controllers/carpooling.controller.js:12
    (RATING_READY_DELAY_MS constant)
  supabase/migrations/008_ratings_and_admin.sql:82-100
    (update_user_rating_on_new_rating trigger)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, DRIVER_COLOR, RIDER_COLOR,
)


# Palette
GREY_ZONE = "#ECEFF1"     # pre-departure
YELLOW_ZONE = "#FCF3CF"   # during trip (rating blocked, 403)
GREEN_ZONE = "#D4EFDF"    # rating window open

GREY_BORDER = "#7F8C8D"
YELLOW_BORDER = "#B7950B"
GREEN_BORDER = "#1E8449"

ACCENT_GATE = "#27AE60"   # the 2h-readiness threshold marker
TIMELINE_AXIS = "#34495E"
TICK_COLOR = "#1B2631"

GUARD_FILL = "#FDF2E9"
GUARD_BORDER = "#CA6F1E"
DB_FILL = "#D5F5E3"
DB_BORDER = "#1E8449"
TRIGGER_FILL = "#D6EAF8"
TRIGGER_BORDER = "#1F618D"
ENTRY_FILL = "#F4ECF7"
ENTRY_BORDER = "#6C3483"

SIDE_BG = "#FDFEFE"
SIDE_BORDER = "#566573"


@renderer("mbe_c3_rating_2h_delay_flow")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(13, 7))
    gs = GridSpec(
        2, 1, figure=fig, height_ratios=[2.6, 1.0],
        hspace=0.55, left=0.045, right=0.985, top=0.93, bottom=0.05,
    )
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    # =====================================================================
    # TOP: timeline anchored to departure_time semantics
    # =====================================================================
    # X coordinate is symbolic units relative to T_dep. We draw on a
    # 0..14 axis where:
    #   x=1   -> T0 (booking_time)
    #   x=2.4 -> T0 + 1d (placeholder; departure_time variable)
    #   x=5.5 -> T_dep (ride departs)
    #   x=7.0 -> T_dep + 2h (rating window opens)
    #   x=9.0 -> T_dep + 24h (typical decay; reminder still surfaces)
    #   x=12.0 -> T_dep + 7d (still revisable via update-in-place upsert)
    X_T0 = 1.0
    X_T0_1D = 2.4
    X_DEP = 5.5
    X_DEP_2H = 7.0
    X_DEP_24H = 9.0
    X_DEP_7D = 12.0

    ax1.set_xlim(0.0, 13.5)
    ax1.set_ylim(-3.4, 3.2)

    # Three zones.
    ax1.add_patch(mpatches.Rectangle(
        (0.0, -0.45), X_DEP - 0.0, 0.9,
        facecolor=GREY_ZONE, edgecolor=GREY_BORDER, linewidth=0.8, zorder=1,
    ))
    ax1.add_patch(mpatches.Rectangle(
        (X_DEP, -0.45), X_DEP_2H - X_DEP, 0.9,
        facecolor=YELLOW_ZONE, edgecolor=YELLOW_BORDER, linewidth=0.8, zorder=1,
    ))
    ax1.add_patch(mpatches.Rectangle(
        (X_DEP_2H, -0.45), 13.5 - X_DEP_2H, 0.9,
        facecolor=GREEN_ZONE, edgecolor=GREEN_BORDER, linewidth=0.8, zorder=1,
    ))

    # Zone labels (inside band).
    ax1.text(
        X_DEP / 2.0, 0.0, "pre-departure (no rating; not yet eligible)",
        ha="center", va="center", fontsize=9.4, color="#566573", style="italic",
        zorder=3,
    )
    ax1.text(
        (X_DEP + X_DEP_2H) / 2.0, 0.0,
        "during trip\n(rating endpoint blocks: HTTP 403)",
        ha="center", va="center", fontsize=9.0, color="#7E5109",
        fontweight="bold", zorder=3,
    )
    ax1.text(
        (X_DEP_2H + 13.5) / 2.0, 0.0,
        "rating window OPEN  (readiness gate satisfied; upsert revisable)",
        ha="center", va="center", fontsize=9.4, color="#196F3D",
        fontweight="bold", zorder=3,
    )

    # Timeline axis on top of the zones.
    ax1.plot(
        [0.05, 13.45], [-0.45, -0.45],
        color=TIMELINE_AXIS, linewidth=1.2, zorder=4,
    )
    ax1.annotate(
        "", xy=(13.48, -0.45), xytext=(13.30, -0.45),
        arrowprops=dict(arrowstyle="-|>", color=TIMELINE_AXIS, lw=1.2),
        zorder=4,
    )
    ax1.text(
        13.50, -0.85, "time", ha="right", va="top",
        fontsize=8.8, color=TIMELINE_AXIS, style="italic",
    )

    # Tick marks + tick labels.
    ticks = [
        (X_T0, "T0\n(booking_time)"),
        (X_T0_1D, "T0 + 1d\n(placeholder)"),
        (X_DEP, "T_dep\n(departure_time;\nvariable distance)"),
        (X_DEP_2H, "T_dep + 2h\n(RATING_READY_DELAY_MS)"),
        (X_DEP_24H, "T_dep + 24h\n(typical decay)"),
        (X_DEP_7D, "T_dep + 7d\n(still revisable)"),
    ]
    for x, lbl in ticks:
        ax1.plot(
            [x, x], [-0.62, -0.28], color=TICK_COLOR, linewidth=1.1, zorder=5,
        )
        ax1.text(
            x, -0.82, lbl, ha="center", va="top",
            fontsize=8.6, color=TICK_COLOR,
        )

    # Highlight T_dep + 2h with a vertical accent line crossing both bands.
    ax1.plot(
        [X_DEP_2H, X_DEP_2H], [-0.45, 2.95],
        color=ACCENT_GATE, linewidth=1.8, linestyle="--", zorder=6,
    )
    ax1.text(
        X_DEP_2H + 0.12, 2.92,
        "readiness gate:\nnow >= departure_time + 2h",
        ha="left", va="top", fontsize=9.0, color=ACCENT_GATE,
        fontweight="bold",
    )

    # ---- Event annotations above the timeline -------------------------------
    # T0: bookRide fan-out
    _annot_event(
        ax1, x=X_T0, y_top=2.55,
        title="T0: bookRide()",
        body=(
            "5 immediate notifications +\n"
            "2 ride_rating_reminder rows queued\n"
            "(data.showAfter = T_dep + 2h)"
        ),
        edge=RIDER_COLOR,
    )

    # T_dep: ride happens
    _annot_event(
        ax1, x=X_DEP, y_top=2.55,
        title="T_dep: ride happens",
        body=(
            "soft window for completeRide()\n"
            "by driver (no hard timeout)"
        ),
        edge=DRIVER_COLOR,
    )

    # T_dep + 2h: rating window opens — placed below the timeline
    _annot_event_below(
        ax1, x=X_DEP_2H, y_bot=-1.55,
        title="T_dep + 2h: rating opens",
        body=(
            "reminders surface as\n"
            "tap-to-rate notification cards"
        ),
        edge=ACCENT_GATE,
    )

    # T_dep + 7d: still revisable (placed below the timeline so it does not
    # collide with the figure-right side note above ax1).
    _annot_event_below(
        ax1, x=X_DEP_7D, y_bot=-1.55,
        title="T_dep + 7d (illustrative)",
        body=(
            "rating still revisable via\n"
            "update-in-place UPSERT key\n"
            "(trip_id, rater_id, ratee_id)"
        ),
        edge=GREEN_BORDER,
    )

    # Title for the top panel.
    ax1.set_title(
        "Rating window timeline  —  RATING_READY_DELAY_MS = 2 h  "
        "(rating.controller.js:22-100; carpooling.controller.js:12)",
        fontsize=11.5, fontweight="bold", loc="left", pad=10,
    )

    ax1.set_xticks([])
    ax1.set_yticks([])
    for spine in ax1.spines.values():
        spine.set_visible(False)

    # =====================================================================
    # BOTTOM: rating-submission flow with all 4 guards + upsert + trigger
    # =====================================================================
    ax2.set_xlim(0.0, 13.5)
    ax2.set_ylim(0.0, 2.4)
    ax2.set_xticks([])
    ax2.set_yticks([])
    for spine in ax2.spines.values():
        spine.set_visible(False)

    # Define horizontal slots for 7 nodes. Reserve right side for side note.
    # Available drawing region: 0.10 .. 9.85; side note 10.0 .. 13.4
    flow_xs = [0.55, 2.05, 3.65, 5.40, 7.20, 8.65, 9.95]
    flow_w = [1.30, 1.40, 1.60, 1.65, 1.30, 1.20, 1.10]  # not used directly
    cy = 1.10

    nodes = [
        # (x_center, label, fill, border, halfwidth, halfheight, role-color)
        (
            0.95,
            "POST /api/v1/ratings\n-> createRating\n[rating.controller.js]",
            ENTRY_FILL, ENTRY_BORDER, 0.78, 0.55, None,
        ),
        (
            2.75,
            "Guard 1\nnow ≥ departure_time\n+ RATING_READY_DELAY_MS\nelse 403",
            GUARD_FILL, GUARD_BORDER, 0.78, 0.62, ACCENT_GATE,
        ),
        (
            4.55,
            "Guard 2\nrater is driver OR\nnon-cancelled passenger\nof the trip",
            GUARD_FILL, GUARD_BORDER, 0.80, 0.62, None,
        ),
        (
            6.45,
            "Guard 3\nrole-pairing\ndriver -> passengers only\npassenger -> driver only",
            GUARD_FILL, GUARD_BORDER, 0.92, 0.62,
            "ROLE",  # marker; rendered with stripe
        ),
        (
            8.30,
            "Guard 4\nrater_id ≠ ratee_id",
            GUARD_FILL, GUARD_BORDER, 0.65, 0.45, None,
        ),
        (
            9.85,
            "UPSERT\nratings(trip_id,\n rater_id, ratee_id)\nOVERWRITE on conflict",
            DB_FILL, DB_BORDER, 0.85, 0.62, None,
        ),
        (
            11.85,
            "Trigger\nupdate_user_rating_on_new_rating()\n[migration 008 L82-100]\nrecompute users.avg_rating\n+ users.total_ratings",
            TRIGGER_FILL, TRIGGER_BORDER, 1.20, 0.78, None,
        ),
    ]

    centers = []
    for (cx, lbl, fc, bc, hw, hh, role) in nodes:
        rect = mpatches.FancyBboxPatch(
            (cx - hw, cy - hh), 2 * hw, 2 * hh,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=fc, edgecolor=bc, linewidth=1.3, zorder=3,
        )
        ax2.add_patch(rect)
        ax2.text(
            cx, cy, lbl,
            ha="center", va="center", fontsize=8.2, color="#1A1A1A",
            zorder=4,
        )
        centers.append((cx, hw))

        # Optional left-edge stripe for the role-paired guard.
        if role == "ROLE":
            ax2.add_patch(mpatches.Rectangle(
                (cx - hw, cy - hh), 0.10, hh,
                facecolor=DRIVER_COLOR, edgecolor="none", zorder=4,
            ))
            ax2.add_patch(mpatches.Rectangle(
                (cx - hw, cy - hh + hh), 0.10, hh,
                facecolor=RIDER_COLOR, edgecolor="none", zorder=4,
            ))
        elif role is not None:
            # Single accent stripe (used by readiness-gate guard to echo
            # the timeline color).
            ax2.add_patch(mpatches.Rectangle(
                (cx - hw, cy - hh), 0.10, 2 * hh,
                facecolor=role, edgecolor="none", zorder=4,
            ))

    # Connect adjacent nodes with arrows.
    for i in range(len(centers) - 1):
        cx_a, hw_a = centers[i]
        cx_b, hw_b = centers[i + 1]
        x_start = cx_a + hw_a + 0.04
        x_end = cx_b - hw_b - 0.04
        ax2.annotate(
            "", xy=(x_end, cy), xytext=(x_start, cy),
            arrowprops=dict(
                arrowstyle="-|>", color="#34495E", lw=1.3, mutation_scale=12,
            ),
            zorder=2,
        )

    # Bottom-panel title.
    ax2.text(
        0.05, 2.30,
        "Rating-submission flow  —  4 guards -> UPSERT -> migration-008 aggregation trigger",
        ha="left", va="top", fontsize=10.5, fontweight="bold", color="#1B2631",
    )

    # Role-pairing legend swatches (to explain the stripe).
    ax2.add_patch(mpatches.Rectangle(
        (4.65, 0.07), 0.14, 0.18,
        facecolor=DRIVER_COLOR, edgecolor="none",
    ))
    ax2.text(
        4.83, 0.16, "driver", ha="left", va="center",
        fontsize=8.2, color=DRIVER_COLOR, fontweight="bold",
    )
    ax2.add_patch(mpatches.Rectangle(
        (5.55, 0.07), 0.14, 0.18,
        facecolor=RIDER_COLOR, edgecolor="none",
    ))
    ax2.text(
        5.73, 0.16, "passenger", ha="left", va="center",
        fontsize=8.2, color=RIDER_COLOR, fontweight="bold",
    )
    ax2.text(
        6.55, 0.16,
        "(stripe on Guard 3 indicates role-paired permission)",
        ha="left", va="center", fontsize=8.0, color="#566573", style="italic",
    )

    # =====================================================================
    # Side note (top-right of figure, anchored to ax1 area)
    # =====================================================================
    side_text = (
        "NOT implemented (open design proposals):\n"
        "  • pre-publication dispute window\n"
        "  • cross-trip trend protection\n"
        "  • mandatory justification on low scores\n"
        "\n"
        "ratings table holds 0 rows in the\n"
        "2026-04-23 production snapshot."
    )
    # Place the box in figure coordinates so it sits to the right of the
    # event annotations without overlapping them.
    fig.text(
        0.985, 0.86, side_text,
        ha="right", va="top", fontsize=8.7, color="#1B2631",
        bbox=dict(
            boxstyle="round,pad=0.5,rounding_size=0.4",
            facecolor=SIDE_BG, edgecolor=SIDE_BORDER, linewidth=1.0,
        ),
    )

    pdf, png = save_mpl("mbe_c3_rating_2h_delay_flow")
    register("mbe_c3_rating_2h_delay_flow", "ok", png_path=png)
    return pdf, png


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _annot_event(ax, x, y_top, title, body, edge, anchor="center"):
    """Draw an event callout above the timeline at x, with leader line."""
    if anchor == "left":
        ha = "left"
        text_x = x + 0.05
    else:
        ha = "center"
        text_x = x

    # Leader line from timeline (y=-0.45..0.45) up to box bottom.
    ax.plot(
        [x, x], [0.48, y_top - 0.78],
        color=edge, linewidth=1.0, linestyle=":", zorder=5,
    )

    label = f"{title}\n{body}"
    ax.text(
        text_x, y_top, label,
        ha=ha, va="top", fontsize=8.4, color="#1B2631",
        bbox=dict(
            boxstyle="round,pad=0.30,rounding_size=0.25",
            facecolor="#FFFFFF", edgecolor=edge, linewidth=1.1,
        ),
        zorder=7,
    )


def _annot_event_below(ax, x, y_bot, title, body, edge):
    """Draw an event callout below the timeline (under the tick labels)."""
    # Leader line from below-tick area down to box top.
    ax.plot(
        [x, x], [-1.10, y_bot + 0.05],
        color=edge, linewidth=1.0, linestyle=":", zorder=5,
    )
    label = f"{title}\n{body}"
    ax.text(
        x, y_bot, label,
        ha="center", va="top", fontsize=8.4, color="#1B2631",
        bbox=dict(
            boxstyle="round,pad=0.30,rounding_size=0.25",
            facecolor="#FFFFFF", edgecolor=edge, linewidth=1.1,
        ),
        zorder=7,
    )
