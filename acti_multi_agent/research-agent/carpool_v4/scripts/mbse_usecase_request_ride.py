"""mbse_usecase_request_ride — Use-case diagram for the request-ride flow.

Hand-drawn with matplotlib (stick-figure actors + use-case ovals + dashed
include/extend connectors). Three actors flank a system boundary box:
    Rider (top-left)   Activity Organizer (bottom-left)   Driver (right)

Use cases inside the boundary are arranged in 3 horizontal priority bands
(high on top, medium middle, low bottom) so:
    - Actor association lines fan out left-to-right without back-tracking.
    - «include» arrows stay within or cross at most one band, gently bent.
    - «extend» arrows stay within or cross at most one band, gently bent
      in the opposite direction so they remain visually distinguishable
      from «include» even where they share endpoints.

Use cases inside the boundary are colour-coded by priority:
    high   = red (#E74C3C)
    medium = orange (#E67E22)
    low    = tan (#D7B17B)

This is an MBSE-style overview, not a state-machine. References:
  campusride-backend/src/controllers/carpooling.controller.js:511-709
  draft §5.2, §5.7.3, §5.7.5, §5.11
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


# Priority palette
HIGH_FILL = "#FADBD8"
HIGH_BORDER = "#C0392B"
MED_FILL = "#FDEBD0"
MED_BORDER = "#CA6F1E"
LOW_FILL = "#F5E7CE"
LOW_BORDER = "#A37438"

ACTOR_COLOR = "#1B2631"
SYS_BORDER = "#34495E"
SYS_TITLE = "#34495E"
INCLUDE_COLOR = "#2874A6"
EXTEND_COLOR = "#7D3C98"
ASSOC_COLOR = "#7B8A8B"


@renderer("mbse_usecase_request_ride")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch

    # Wider aspect ratio gives more horizontal room for the 3-column band.
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 22)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # System boundary (rounded rectangle covering the use cases)
    # ------------------------------------------------------------------
    sys_x, sys_y, sys_w, sys_h = 6.5, 1.6, 19.0, 18.2
    ax.add_patch(
        FancyBboxPatch(
            (sys_x, sys_y), sys_w, sys_h,
            boxstyle="round,pad=0.15,rounding_size=0.4",
            facecolor="#FBFCFC", edgecolor=SYS_BORDER, linewidth=1.6,
        )
    )
    ax.text(
        sys_x + sys_w / 2, sys_y + sys_h - 0.5,
        "CampusRide Carpool System",
        ha="center", va="center",
        fontsize=13, fontweight="bold", color=SYS_TITLE,
    )

    # ------------------------------------------------------------------
    # Stick-figure actor helper
    # ------------------------------------------------------------------
    def stick_figure(cx, cy, label, role_note=""):
        """Draw a stick figure centred horizontally at cx with feet at cy."""
        head_r = 0.30
        head_y = cy + 2.10
        head = Ellipse((cx, head_y), 2 * head_r, 2 * head_r,
                       facecolor="white", edgecolor=ACTOR_COLOR, linewidth=1.6)
        ax.add_patch(head)
        ax.plot([cx, cx], [cy + 1.80, cy + 0.80],
                color=ACTOR_COLOR, linewidth=1.6, solid_capstyle="round")
        ax.plot([cx - 0.55, cx + 0.55], [cy + 1.30, cy + 1.30],
                color=ACTOR_COLOR, linewidth=1.6, solid_capstyle="round")
        ax.plot([cx, cx - 0.45], [cy + 0.80, cy],
                color=ACTOR_COLOR, linewidth=1.6, solid_capstyle="round")
        ax.plot([cx, cx + 0.45], [cy + 0.80, cy],
                color=ACTOR_COLOR, linewidth=1.6, solid_capstyle="round")
        label_lines = label.split("\n")
        line_step = 0.45
        first_line_y = cy - 0.35
        for i, line in enumerate(label_lines):
            ax.text(cx, first_line_y - i * line_step, line,
                    ha="center", va="top",
                    fontsize=11, fontweight="bold", color=ACTOR_COLOR)
        if role_note:
            note_y = first_line_y - len(label_lines) * line_step - 0.05
            ax.text(cx, note_y, role_note, ha="center", va="top",
                    fontsize=8.5, style="italic", color="#566573")
        return {
            "right": (cx + 0.55, cy + 1.30),
            "left":  (cx - 0.55, cy + 1.30),
            "head":  (cx, head_y),
            "shoulder_r_high":  (cx + 0.55, cy + 1.55),
            "shoulder_r_low":   (cx + 0.55, cy + 1.05),
            "shoulder_l_high":  (cx - 0.55, cy + 1.55),
            "shoulder_l_low":   (cx - 0.55, cy + 1.05),
        }

    # Rider top-left (aligned to HIGH band), Organizer bottom-left (aligned
    # to LOW band), Driver mid-right (between MED and CONFIRM rows).
    rider = stick_figure(2.6, 14.8, "Rider", "(passenger)")
    organizer = stick_figure(2.6, 4.8, "Activity\nOrganizer",
                             "(creates ride for event)")
    driver = stick_figure(29.4, 9.4, "Driver", "(.edu-verified)")

    # ------------------------------------------------------------------
    # Use case ovals — 3 priority bands × 2-to-4 columns
    # ------------------------------------------------------------------
    UC_W, UC_H = 4.3, 1.6

    def use_case(cx, cy, text, priority):
        if priority == "high":
            fc, ec = HIGH_FILL, HIGH_BORDER
        elif priority == "medium":
            fc, ec = MED_FILL, MED_BORDER
        else:
            fc, ec = LOW_FILL, LOW_BORDER
        ell = Ellipse((cx, cy), UC_W, UC_H,
                      facecolor=fc, edgecolor=ec, linewidth=1.4)
        ax.add_patch(ell)
        ax.text(cx, cy, text, ha="center", va="center",
                fontsize=9.6, color="#1B2631", wrap=True)
        # Anchor points along the ellipse perimeter — including 45° anchors
        # for cleaner diagonal exits without crossing the ellipse text.
        import math
        a, b = UC_W / 2, UC_H / 2
        def edge_at(deg):
            r = math.radians(deg)
            return (cx + a * math.cos(r), cy + b * math.sin(r))
        return {
            "left":   (cx - a, cy),
            "right":  (cx + a, cy),
            "top":    (cx, cy + b),
            "bottom": (cx, cy - b),
            "tl":     edge_at(135),
            "tr":     edge_at(45),
            "bl":     edge_at(-135),
            "br":     edge_at(-45),
            "center": (cx, cy),
        }

    # ------- HIGH band (top, y = 17.0) -------
    HIGH_Y = 17.0
    uc_browse = use_case(10.0, HIGH_Y, "Browse rides", "high")
    uc_submit = use_case(15.6, HIGH_Y, "Submit ride request /\nbook seat", "high")
    uc_match  = use_case(21.2, HIGH_Y, "System matches\navailable rides", "high")

    # Confirm sits between high and medium bands. Place it right of centre
    # so its «include» edges to match/notif have unambiguous direction and
    # do not stack with the submit→match horizontal include.
    uc_confirm = use_case(18.4, 13.6, "Confirm booking", "high")

    # ------- MEDIUM band (middle) -------
    # Stagger the medium band into two sub-rows so the «extend» arrows from
    # chat→confirm and rate→confirm cannot collide. Chat sits LEFT of
    # confirm at y=10.8; rate sits BELOW confirm at y=10.8 too but in a
    # different column. WeChat moves further right.
    MED_Y = 10.8
    uc_notif  = use_case(10.0, MED_Y, "Receive 5+2\nnotification bundle", "medium")
    uc_chat   = use_case(14.6, MED_Y, "Auto-create ride-scoped\ngroup chat", "medium")
    uc_wechat = use_case(22.2, MED_Y, "WeChat outreach\non createRide", "medium")
    # Rate moved to its own row at y=7.6 so its «extend» edge to confirm
    # has a clean vertical run that does not touch the chat→confirm edge.
    uc_rate   = use_case(18.4, 7.4,  "Submit rating\nafter 2h delay\n(0 rows in prod)",
                         "medium")

    # ------- LOW band (bottom, y = 4.0) -------
    LOW_Y = 4.0
    uc_award = use_case(10.0, LOW_Y,
                        "Award / deduct points\n(designed; inert)", "low")
    uc_sos   = use_case(22.2, LOW_Y,
                        "Trigger SOS\n(designed; 0 invocations)", "low")

    # ------------------------------------------------------------------
    # Solid actor-to-use-case associations (sparse strategy)
    # ------------------------------------------------------------------
    def assoc(p0, p1, color=ASSOC_COLOR, lw=1.0,
              connectionstyle="arc3,rad=0.0"):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="-", color=color, linewidth=lw,
            mutation_scale=8, alpha=0.65,
            connectionstyle=connectionstyle,
        ))

    # Rider — primary participant in browse/submit/notif/rate. We DROP
    # rider→sos to avoid a long diagonal across all bands; SOS is shown
    # as Driver-anchored, and the Italic call-out makes its read-only
    # nature explicit.
    assoc(rider["right"], uc_browse["tl"])
    assoc(rider["right"], uc_submit["tl"],
          connectionstyle="arc3,rad=-0.04")
    assoc(rider["shoulder_r_low"], uc_notif["tl"],
          connectionstyle="arc3,rad=0.05")
    assoc(rider["shoulder_r_low"], uc_rate["tl"],
          connectionstyle="arc3,rad=0.18")

    # Organizer — only the use cases the organizer DIRECTLY initiates.
    # Browsing rides on behalf of an event and triggering WeChat outreach.
    assoc(organizer["right"], uc_browse["bl"],
          connectionstyle="arc3,rad=-0.10")
    assoc(organizer["right"], uc_wechat["bl"],
          connectionstyle="arc3,rad=-0.05")

    # Driver — primary participant in match/confirm/chat/wechat/award/sos.
    # Strategy: lines from driver enter use cases from their RIGHT side
    # exclusively, fanning out vertically. Notif lies far across the
    # diagram, so we DROP the noisy driver→notif line — confirm─include→
    # notif already establishes the structural relationship.
    assoc(driver["shoulder_l_high"], uc_match["right"],
          connectionstyle="arc3,rad=0.06")
    assoc(driver["left"], uc_confirm["tr"],
          connectionstyle="arc3,rad=-0.18")
    assoc(driver["left"], uc_wechat["right"],
          connectionstyle="arc3,rad=0.0")
    assoc(driver["shoulder_l_low"], uc_chat["right"],
          connectionstyle="arc3,rad=-0.05")
    # Award is far across the diagram — route the line via a strong
    # downward arc that hugs the lower edge of the system boundary so it
    # never crosses the medium band. Sos is directly below driver, short.
    assoc(driver["shoulder_l_low"], uc_award["right"],
          connectionstyle="arc3,rad=0.45")
    assoc(driver["shoulder_l_low"], uc_sos["tr"],
          connectionstyle="arc3,rad=0.18")

    # ------------------------------------------------------------------
    # «include» / «extend» dashed arrows between use cases
    # ------------------------------------------------------------------
    def stereotype_arrow(p0, p1, label, color,
                         label_offset=(0, 0.22),
                         connectionstyle="arc3,rad=0.0"):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="->", color=color, linewidth=1.5,
            linestyle="--", mutation_scale=14,
            connectionstyle=connectionstyle,
        ))
        mx = (p0[0] + p1[0]) / 2 + label_offset[0]
        my = (p0[1] + p1[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center",
                fontsize=9, color=color, style="italic", fontweight="bold",
                bbox=dict(facecolor="white", edgecolor=color,
                          boxstyle="round,pad=0.20", alpha=0.97,
                          linewidth=0.6))

    # «include» edges (blue). All three stay in the upper-right quadrant:
    #   submit ─include→ match     (horizontal across HIGH band)
    #   confirm ─include→ match    (short vertical, gentle right bow)
    #   confirm ─include→ notif    (long diagonal across the diagram, bent
    #                               LOW so it does not pass through chat)
    stereotype_arrow(uc_submit["right"], uc_match["left"],
                     "«include»", INCLUDE_COLOR,
                     label_offset=(0, 0.32))
    stereotype_arrow(uc_confirm["top"], uc_match["br"],
                     "«include»", INCLUDE_COLOR,
                     label_offset=(1.20, -0.40),
                     connectionstyle="arc3,rad=0.22")
    # Notif route: confirm sits at (18.4, 13.6); notif sits at (10.0, 10.8);
    # chat sits at (14.6, 10.8) directly between them at the lower y. We
    # exit confirm at LEFT and arc UPWARD (positive rad) so the path
    # swings ABOVE chat (peaking around y~14.5-15) and descends into
    # notif's TOP. Empty space above the medium band absorbs the arc
    # without touching chat, browse, or submit.
    stereotype_arrow(uc_confirm["left"], uc_notif["top"],
                     "«include»", INCLUDE_COLOR,
                     label_offset=(-0.4, 0.40),
                     connectionstyle="arc3,rad=0.45")

    # «extend» edges (purple). Each is staged so it cannot collide with the
    # «include» edges above:
    #   chat ─extend→ confirm   (short diagonal up-right; positive rad bows
    #                            ABOVE the confirm-include-notif edge)
    #   rate ─extend→ confirm   (clean vertical run — rate is now directly
    #                            below confirm)
    #   award ─extend→ rate     (long diagonal up-right within the lower
    #                            half; positive rad bows away from rate-
    #                            confirm)
    stereotype_arrow(uc_chat["tr"], uc_confirm["bl"],
                     "«extend»", EXTEND_COLOR,
                     label_offset=(-0.20, 0.30),
                     connectionstyle="arc3,rad=0.18")
    stereotype_arrow(uc_rate["top"], uc_confirm["bottom"],
                     "«extend»", EXTEND_COLOR,
                     label_offset=(0.85, 0.0),
                     connectionstyle="arc3,rad=0.0")
    stereotype_arrow(uc_award["tr"], uc_rate["bl"],
                     "«extend»", EXTEND_COLOR,
                     label_offset=(0.0, 0.32),
                     connectionstyle="arc3,rad=0.15")

    # ------------------------------------------------------------------
    # Priority legend (top-right, OUTSIDE system boundary so it does not
    # overlap any use case)
    # ------------------------------------------------------------------
    legend_x, legend_y = 30.6, 18.6
    ax.text(legend_x, legend_y + 0.6, "Priority", ha="center",
            fontsize=10, fontweight="bold", color="#1B2631")
    for i, (lab, fc, ec) in enumerate([
        ("high",   HIGH_FILL, HIGH_BORDER),
        ("medium", MED_FILL,  MED_BORDER),
        ("low",    LOW_FILL,  LOW_BORDER),
    ]):
        y = legend_y - i * 0.65
        ax.add_patch(Ellipse((legend_x - 0.7, y), 0.85, 0.4,
                             facecolor=fc, edgecolor=ec, linewidth=1.2))
        ax.text(legend_x + 0.0, y, lab, ha="left", va="center",
                fontsize=9.5, color="#1B2631")

    # «include» / «extend» legend (bottom-right, OUTSIDE system boundary)
    leg2_x = 27.5
    leg2_y = 3.5
    ax.text(leg2_x, leg2_y + 0.7, "Connectors",
            ha="left", fontsize=10, fontweight="bold", color="#1B2631")
    ax.add_patch(FancyArrowPatch(
        (leg2_x, leg2_y), (leg2_x + 1.6, leg2_y),
        arrowstyle="-", color=ASSOC_COLOR, linewidth=1.2, mutation_scale=8,
    ))
    ax.text(leg2_x + 1.8, leg2_y, "actor association",
            ha="left", va="center", fontsize=9, color="#1B2631")
    ax.add_patch(FancyArrowPatch(
        (leg2_x, leg2_y - 0.55), (leg2_x + 1.6, leg2_y - 0.55),
        arrowstyle="->", color=INCLUDE_COLOR, linewidth=1.4,
        linestyle="--", mutation_scale=12,
    ))
    ax.text(leg2_x + 1.8, leg2_y - 0.55, "«include»",
            ha="left", va="center", fontsize=9, color=INCLUDE_COLOR,
            style="italic")
    ax.add_patch(FancyArrowPatch(
        (leg2_x, leg2_y - 1.10), (leg2_x + 1.6, leg2_y - 1.10),
        arrowstyle="->", color=EXTEND_COLOR, linewidth=1.4,
        linestyle="--", mutation_scale=12,
    ))
    ax.text(leg2_x + 1.8, leg2_y - 1.10, "«extend»",
            ha="left", va="center", fontsize=9, color=EXTEND_COLOR,
            style="italic")

    # ------------------------------------------------------------------
    # Title + footer
    # ------------------------------------------------------------------
    ax.text(16.0, 21.3,
            "Use-Case Diagram — Request a Carpool Ride",
            ha="center", va="center",
            fontsize=15, fontweight="bold", color="#1B2631")
    ax.text(16.0, 0.6,
            "Solid lines = actor associations (only PRIMARY initiator drawn "
            "where secondary lines would cross).  Dashed «include» (blue) = "
            "mandatory sub-flow; dashed «extend» (purple) = optional, "
            "condition-gated extension.  Italic counts (e.g. 0 rows in prod) "
            "annotate honesty-corrected designed-but-uninstrumented use cases.",
            ha="center", va="center",
            fontsize=9.5, style="italic", color="#566573", wrap=True)

    pdf, png = save_mpl("mbse_usecase_request_ride", dpi=300)
    register("mbse_usecase_request_ride", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
