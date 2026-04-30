"""mbse_param_rating_window - SysML Parametric Diagram for the rating-window guard.

Three «constraint» blocks, each rendered as a rectangle with a stereotype
tag and an inner formula:

  - NotSelfRating    : is_valid    <=> rater_id != ratee_id
  - RoleEligible     : is_eligible <=> (rater = ride.driver AND
                                        ratee in ride.passengers) OR
                                       (rater in ride.passengers AND
                                        ratee = ride.driver)
  - RatingWindowOpen : is_open     <=> (now - departure_time) >= delay
                       with delay = 7,200,000 ms = 2 h
                       (RATING_READY_DELAY_MS)

Value properties are drawn as small rectangles with binding connectors
(solid lines, no arrowheads) into the constraint blocks.  The chained
constraint output (NotSelfRating -> RoleEligible -> RatingWindowOpen)
feeds a Pass / Reject decision diamond.

Source-of-truth:
  campusride-backend/src/controllers/rating.controller.js (createRating guards)
  RATING_READY_DELAY_MS = 2 * 60 * 60 * 1000
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register, renderer  # noqa: E402


# Palette --------------------------------------------------------------------
CONSTRAINT_FILL = "#FDEBD0"
CONSTRAINT_BORDER = "#9C640C"

VALUE_FILL = "#D6EAF8"
VALUE_BORDER = "#1F618D"

CONST_FILL = "#FCF3CF"
CONST_BORDER = "#9A7D0A"

DECISION_FILL = "#D5F5E3"
DECISION_BORDER = "#1E8449"
REJECT_FILL = "#FADBD8"
REJECT_BORDER = "#922B21"

BIND_COLOR = "#1B2631"
CHAIN_COLOR = "#7D6608"


@renderer("mbse_param_rating_window")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, Polygon
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(figsize=(17, 11))
    ax.set_xlim(0, 34)
    ax.set_ylim(0, 22)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    ax.text(
        17, 21.3,
        "Parametric Diagram (SysML) - Rating Window Guard",
        fontsize=16, fontweight="bold", color="#0E2F44",
        ha="center", va="center",
    )
    ax.text(
        17, 20.55,
        "<<constraint>> blocks  +  value properties  +  binding connectors  "
        "(solid, no arrowhead);  chained -> Pass / Reject",
        fontsize=10.5, color="#566573", style="italic",
        ha="center", va="center",
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def constraint_block(x, y, w, h, name, formula, *, params=None):
        # outer block
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.05,rounding_size=0.30",
            linewidth=2.0, edgecolor=CONSTRAINT_BORDER,
            facecolor=CONSTRAINT_FILL, zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2, y + h - 0.36,
            "<<constraint>>",
            fontsize=9.0, color="#7E5109", style="italic",
            ha="center", va="center", zorder=5,
        )
        ax.text(
            x + w / 2, y + h - 0.85, name,
            fontsize=11, fontweight="bold", color="#1B2631",
            ha="center", va="center", zorder=5,
        )
        # constraint compartment
        inner_y = y + 0.4
        inner_h = h - 1.6
        inner = FancyBboxPatch(
            (x + 0.25, inner_y), w - 0.5, inner_h,
            boxstyle="round,pad=0.03,rounding_size=0.15",
            linewidth=1.0, edgecolor="#9C640C", facecolor="white",
            zorder=4,
        )
        ax.add_patch(inner)
        ax.text(
            x + w / 2, inner_y + inner_h / 2 + 0.15,
            "{ constraint }",
            fontsize=8.4, color="#9C640C", style="italic",
            ha="center", va="center", zorder=5,
        )
        ax.text(
            x + w / 2, inner_y + inner_h / 2 - 0.45, formula,
            fontsize=9.5, color="#1B2631",
            ha="center", va="center", zorder=5,
        )
        if params:
            ax.text(
                x + w / 2, y + 0.18, params,
                fontsize=8.2, color="#566573", style="italic",
                ha="center", va="bottom", zorder=5,
            )

    def value_box(x, y, w, h, name, value, *, fill=VALUE_FILL,
                  border=VALUE_BORDER, stereotype=None):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.03,rounding_size=0.18",
            linewidth=1.3, edgecolor=border,
            facecolor=fill, zorder=3,
        )
        ax.add_patch(box)
        if stereotype:
            ax.text(
                x + w / 2, y + h - 0.22,
                f"<<{stereotype}>>",
                fontsize=7.6, color=border, style="italic",
                ha="center", va="center", zorder=5,
            )
            ax.text(
                x + w / 2, y + h / 2 - 0.04, name,
                fontsize=8.6, fontweight="bold", color="#1B2631",
                ha="center", va="center", zorder=5,
            )
            ax.text(
                x + w / 2, y + 0.22, value,
                fontsize=8.2, color="#1B2631", style="italic",
                ha="center", va="center", zorder=5,
            )
        else:
            ax.text(
                x + w / 2, y + h / 2 + 0.20, name,
                fontsize=8.6, fontweight="bold", color="#1B2631",
                ha="center", va="center", zorder=5,
            )
            ax.text(
                x + w / 2, y + h / 2 - 0.30, value,
                fontsize=8.2, color="#1B2631", style="italic",
                ha="center", va="center", zorder=5,
            )

    def binding_connector(p_src, p_dst, *, color=BIND_COLOR, lw=1.3,
                          style="solid"):
        sx, sy = p_src
        dx, dy = p_dst
        ax.plot([sx, dx], [sy, dy], color=color, linewidth=lw,
                linestyle=style, zorder=2)
        # square ends
        for px, py in [(sx, sy), (dx, dy)]:
            ax.add_patch(
                FancyBboxPatch(
                    (px - 0.08, py - 0.08), 0.16, 0.16,
                    boxstyle="square,pad=0.0",
                    linewidth=1.0, edgecolor=color, facecolor="white",
                    zorder=3,
                )
            )

    def chain_arrow(p_src, p_dst, label, *, color=CHAIN_COLOR, lw=1.7):
        from matplotlib.patches import FancyArrowPatch
        sx, sy = p_src
        dx, dy = p_dst
        arrow = FancyArrowPatch(
            (sx, sy), (dx, dy),
            arrowstyle="-|>", mutation_scale=18,
            linewidth=lw, color=color,
            zorder=4,
        )
        ax.add_patch(arrow)
        ax.text(
            (sx + dx) / 2, (sy + dy) / 2 + 0.30, label,
            fontsize=9.0, fontweight="bold", color=color,
            ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor=color,
                      boxstyle="round,pad=0.15", linewidth=0.8,
                      alpha=0.97),
            zorder=5,
        )

    # ------------------------------------------------------------------
    # Three constraint blocks  (left -> right chain)
    # ------------------------------------------------------------------
    cb_w, cb_h = 8.2, 5.4
    cb_y = 9.0
    cb1_x = 1.0
    cb2_x = 12.5
    cb3_x = 24.0

    constraint_block(
        cb1_x, cb_y, cb_w, cb_h,
        "NotSelfRating",
        "is_valid  <=>  rater_id != ratee_id",
        params="params: rater_id, ratee_id",
    )
    constraint_block(
        cb2_x, cb_y, cb_w, cb_h,
        "RoleEligible",
        "is_eligible  <=>\n"
        "(rater = ride.driver  &  ratee in ride.passengers)\n"
        "or\n"
        "(rater in ride.passengers  &  ratee = ride.driver)",
        params="params: rater_role, ratee_role",
    )
    constraint_block(
        cb3_x, cb_y, cb_w, cb_h,
        "RatingWindowOpen",
        "is_open  <=>  (now - departure_time) >= delay",
        params="params: now, departure_time, delay",
    )

    # ------------------------------------------------------------------
    # Value properties (top row)
    # ------------------------------------------------------------------
    vb_w, vb_h = 4.8, 2.4
    vb_y = 17.0

    # User.id (rater) and User.id (ratee) feed NotSelfRating
    value_box(0.4, vb_y, vb_w, vb_h,
              "User.id  (rater)", "rater_id : UUID",
              stereotype="value property")
    value_box(5.6, vb_y, vb_w, vb_h,
              "User.id  (ratee)", "ratee_id : UUID",
              stereotype="value property")

    # Ride.driver_id + RideBooking.rider_id feed RoleEligible
    value_box(11.6, vb_y, vb_w, vb_h,
              "Ride.driver_id", "driver_id : UUID",
              stereotype="value property")
    value_box(16.7, vb_y, vb_w, vb_h,
              "RideBooking.rider_id", "rider_id : UUID",
              stereotype="value property")

    # Ride.departure_time, Date.now(), and the constant feed RatingWindowOpen
    value_box(22.0, vb_y, vb_w, vb_h,
              "Ride.departure_time", "departure_time : ts",
              stereotype="value property")
    value_box(27.0, vb_y, vb_w, vb_h,
              "Date.now()", "now : ts (ms)",
              stereotype="value property")
    # Constant block (slightly different visual)
    value_box(29.6, 14.5, 4.0, 2.0,
              "RATING_READY_DELAY_MS",
              "= 2 * 60 * 60 * 1000\n= 7,200,000 ms (2 h)",
              fill=CONST_FILL, border=CONST_BORDER,
              stereotype="constant")

    # ------------------------------------------------------------------
    # Binding connectors
    # ------------------------------------------------------------------
    # NotSelfRating bindings
    binding_connector((0.4 + vb_w / 2, vb_y),
                      (cb1_x + cb_w * 0.30, cb_y + cb_h))
    binding_connector((5.6 + vb_w / 2, vb_y),
                      (cb1_x + cb_w * 0.70, cb_y + cb_h))

    # RoleEligible bindings
    binding_connector((11.6 + vb_w / 2, vb_y),
                      (cb2_x + cb_w * 0.30, cb_y + cb_h))
    binding_connector((16.7 + vb_w / 2, vb_y),
                      (cb2_x + cb_w * 0.70, cb_y + cb_h))

    # RatingWindowOpen bindings
    binding_connector((22.0 + vb_w / 2, vb_y),
                      (cb3_x + cb_w * 0.20, cb_y + cb_h))
    binding_connector((27.0 + vb_w / 2, vb_y),
                      (cb3_x + cb_w * 0.50, cb_y + cb_h))
    binding_connector((29.6 + 4.0 / 2, 14.5),
                      (cb3_x + cb_w * 0.80, cb_y + cb_h))

    # ------------------------------------------------------------------
    # Chain arrows between constraint outputs
    # ------------------------------------------------------------------
    chain_arrow(
        (cb1_x + cb_w, cb_y + cb_h / 2),
        (cb2_x, cb_y + cb_h / 2),
        "is_valid &",
    )
    chain_arrow(
        (cb2_x + cb_w, cb_y + cb_h / 2),
        (cb3_x, cb_y + cb_h / 2),
        "is_eligible &",
    )

    # ------------------------------------------------------------------
    # Pass / Reject decision (bottom)
    # ------------------------------------------------------------------
    # Decision diamond
    cx, cy = 17.0, 5.5
    diamond_pts = [(cx, cy + 1.6), (cx + 2.4, cy),
                   (cx, cy - 1.6), (cx - 2.4, cy)]
    ax.add_patch(Polygon(diamond_pts, closed=True,
                         facecolor=DECISION_FILL,
                         edgecolor=DECISION_BORDER, linewidth=1.6,
                         zorder=3))
    ax.text(cx, cy + 0.30, "decision",
            fontsize=8.2, color=DECISION_BORDER, style="italic",
            ha="center", va="center", zorder=5)
    ax.text(cx, cy - 0.20,
            "is_valid &\nis_eligible &\nis_open ?",
            fontsize=9.0, fontweight="bold", color="#1B2631",
            ha="center", va="center", zorder=5)

    # Chain output from RatingWindowOpen down into the decision
    chain_arrow(
        (cb3_x + cb_w / 2, cb_y),
        (cx + 1.8, cy + 1.2),
        "is_open",
    )

    # Pass branch
    pass_box = FancyBboxPatch(
        (28.0, 4.5), 5.4, 2.2,
        boxstyle="round,pad=0.04,rounding_size=0.28",
        linewidth=1.6, edgecolor=DECISION_BORDER,
        facecolor="#EAFAF1", zorder=3,
    )
    ax.add_patch(pass_box)
    ax.text(30.7, 6.20, "[ true ]",
            fontsize=9.0, fontweight="bold", color=DECISION_BORDER,
            ha="center", va="center", zorder=5, style="italic")
    ax.text(30.7, 5.55,
            "Pass\n-> UPSERT ratings\n  (trip_id, rater_id, ratee_id)",
            fontsize=9.0, color="#1B2631",
            ha="center", va="center", zorder=5)

    # Reject branch
    rej_box = FancyBboxPatch(
        (0.6, 4.5), 5.4, 2.2,
        boxstyle="round,pad=0.04,rounding_size=0.28",
        linewidth=1.6, edgecolor=REJECT_BORDER,
        facecolor=REJECT_FILL, zorder=3,
    )
    ax.add_patch(rej_box)
    ax.text(3.3, 6.20, "[ false ]",
            fontsize=9.0, fontweight="bold", color=REJECT_BORDER,
            ha="center", va="center", zorder=5, style="italic")
    ax.text(3.3, 5.55,
            "Reject\n-> 400 / 403 to client\n  (window-not-open / role / self)",
            fontsize=9.0, color="#1B2631",
            ha="center", va="center", zorder=5)

    # decision -> pass / reject
    chain_arrow((cx + 2.4, cy), (28.0, cy + 0.3), "true",
                color=DECISION_BORDER, lw=1.5)
    chain_arrow((cx - 2.4, cy), (6.0, cy + 0.3), "false",
                color=REJECT_BORDER, lw=1.5)

    # ------------------------------------------------------------------
    # Footer note
    # ------------------------------------------------------------------
    ax.text(
        17, 1.9,
        "Source: rating.controller.js  -  RATING_READY_DELAY_MS = 2*60*60*1000  -  "
        "ratings holds 0 rows on 2026-04-23 (snapshot)",
        fontsize=9.0, color="#566573", style="italic",
        ha="center", va="center",
        bbox=dict(facecolor="#FBFCFC", edgecolor="#566573",
                  boxstyle="round,pad=0.25", linewidth=0.9),
    )

    # ------------------------------------------------------------------
    # Legend
    # ------------------------------------------------------------------
    legend_handles = [
        mpatches.Patch(facecolor=CONSTRAINT_FILL, edgecolor=CONSTRAINT_BORDER,
                       label="<<constraint>> block"),
        mpatches.Patch(facecolor=VALUE_FILL, edgecolor=VALUE_BORDER,
                       label="<<value property>>"),
        mpatches.Patch(facecolor=CONST_FILL, edgecolor=CONST_BORDER,
                       label="<<constant>>"),
        mpatches.Patch(facecolor=DECISION_FILL, edgecolor=DECISION_BORDER,
                       label="decision (UML)"),
        Line2D([0], [0], color=BIND_COLOR, linewidth=1.3,
               label="binding connector"),
        Line2D([0], [0], color=CHAIN_COLOR, linewidth=1.6,
               label="constraint output -> next"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left", bbox_to_anchor=(0.005, 0.03),
        frameon=True, fontsize=8.6, handlelength=1.6,
        handletextpad=0.6, ncol=1,
        framealpha=0.95, edgecolor="#566573",
    )

    plt.tight_layout(pad=0.3)

    pdf, png = save_mpl("mbse_param_rating_window", dpi=300)
    register("mbse_param_rating_window", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
