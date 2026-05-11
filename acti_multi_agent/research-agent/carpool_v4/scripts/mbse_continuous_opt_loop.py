"""mbse_continuous_opt_loop - Closed-loop control diagram for §5.18.

Continuous Optimization Loop rendered as a control-system block diagram:

  Inputs (left, 4 telemetry channels):
    - Registration cadence  (3 / 70 / 111 = 184 over 3 months)
    - Notification fan-out residue  (54 rows, 10 event types)
    - WeChat outreach counter  (82 rows: 62 mkt / 16 ride / 4 act)
    - User feedback inbox  (10 system_messages, 2026-01-10..2026-02-11)

  Summing junction (Σ) -> Monthly snapshot review  (human-in-the-loop)
                       -> HoQ refresh (Figure ref:mbse-req-spec)
                       -> Release-track decisions

  Release decisions branch into 3 outputs:
    (1) Provision points subsystem            (EC10)
    (2) Add dispute-window mechanism          (EC5 / EC7)
    (3) Institution-domain whitelist           (EC12)

  All 3 release tracks -> Codebase deploy (Railway push)

  Closing feedback arrow (dashed, with monthly clock icon) goes back
  from "Codebase deploy" to the four telemetry channels.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register, renderer  # noqa: E402


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
TELEMETRY_FILL = "#D6EAF8"
TELEMETRY_BORDER = "#1F618D"

REVIEW_FILL = "#FCF3CF"
REVIEW_BORDER = "#9A7D0A"

HOQ_FILL = "#E8DAEF"
HOQ_BORDER = "#6C3483"

DECISION_FILL = "#FDEBD0"
DECISION_BORDER = "#9C640C"

RELEASE_FILL = "#D5F5E3"
RELEASE_BORDER = "#1E8449"

DEPLOY_FILL = "#FADBD8"
DEPLOY_BORDER = "#922B21"

SUM_FILL = "#FBFCFC"
SUM_BORDER = "#1B2631"

FEEDBACK_COLOR = "#7D3C98"
FORWARD_COLOR = "#1B2631"


@renderer("mbse_continuous_opt_loop")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(figsize=(22, 13))
    ax.set_xlim(0, 44)
    ax.set_ylim(0, 26)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    ax.text(
        22, 25.2,
        "Continuous Optimization Loop - CampusRide v4.4 (control-system view)",
        fontsize=20, fontweight="bold", color="#0E2F44",
        ha="center", va="center",
    )
    ax.text(
        22, 24.4,
        "4 telemetry channels  ->  summing junction  ->  monthly snapshot review (human-in-the-loop)  "
        "->  HoQ refresh  ->  release-track decisions  ->  Codebase deploy  ->  (dashed monthly feedback)",
        fontsize=12, color="#566573", style="italic",
        ha="center", va="center",
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def block(x, y, w, h, title, sub=None, *, fill=TELEMETRY_FILL,
              border=TELEMETRY_BORDER, lw=1.6, header=None):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.05,rounding_size=0.20",
            facecolor=fill, edgecolor=border, linewidth=lw, zorder=3,
        )
        ax.add_patch(box)
        # Optional small header band (e.g., "telemetry")
        if header:
            ax.text(x + w / 2, y + h - 0.32, header,
                    fontsize=8.2, color=border, style="italic",
                    ha="center", va="center", zorder=5)
            tx = x + w / 2
            ty = y + h - 1.05
        else:
            tx = x + w / 2
            ty = y + h - 0.55
        ax.text(tx, ty, title,
                fontsize=10.5, fontweight="bold", color="#1B2631",
                ha="center", va="center", zorder=5)
        if sub:
            ax.text(x + w / 2, y + 0.55, sub,
                    fontsize=8.4, color="#1B2631",
                    ha="center", va="center", zorder=5)
        return dict(left=(x, y + h / 2),
                    right=(x + w, y + h / 2),
                    top=(x + w / 2, y + h),
                    bottom=(x + w / 2, y),
                    x=x, y=y, w=w, h=h)

    def sum_junction(cx, cy, r=0.85):
        """Summing junction: circle with Σ inside and four small +/+ marks."""
        ax.add_patch(Circle((cx, cy), r,
                            facecolor=SUM_FILL, edgecolor=SUM_BORDER,
                            linewidth=2.0, zorder=4))
        ax.text(cx, cy, "Σ",
                fontsize=22, fontweight="bold", color=SUM_BORDER,
                ha="center", va="center", zorder=6)
        # tiny + signs at the four cardinal sides
        for (ox, oy) in [(-r * 1.10, 0), (0, r * 1.10),
                         (r * 1.10, 0), (0, -r * 1.10)]:
            ax.text(cx + ox, cy + oy, "+",
                    fontsize=10, color=SUM_BORDER, fontweight="bold",
                    ha="center", va="center", zorder=6)
        return dict(left=(cx - r, cy), right=(cx + r, cy),
                    top=(cx, cy + r), bottom=(cx, cy - r),
                    center=(cx, cy), r=r)

    def fwd_arrow(p_src, p_dst, *, color=FORWARD_COLOR, lw=1.6, label=None,
                  rad=0.0, label_dy=0.30):
        arr = FancyArrowPatch(
            p_src, p_dst,
            arrowstyle="-|>",
            color=color, linewidth=lw, zorder=2,
            mutation_scale=14,
            connectionstyle=f"arc3,rad={rad}",
        )
        ax.add_patch(arr)
        if label:
            mx = (p_src[0] + p_dst[0]) / 2
            my = (p_src[1] + p_dst[1]) / 2 + label_dy
            ax.text(mx, my, label,
                    fontsize=8.5, color=color, fontweight="bold",
                    ha="center", va="center",
                    bbox=dict(facecolor="white", edgecolor=color,
                              boxstyle="round,pad=0.15", linewidth=0.7,
                              alpha=0.95),
                    zorder=5)

    def feedback_arrow(p_src, p_dst, *, color=FEEDBACK_COLOR, lw=1.6,
                       rad=0.0, label=None, label_xy=None):
        arr = FancyArrowPatch(
            p_src, p_dst,
            arrowstyle="-|>",
            color=color, linewidth=lw, zorder=2,
            linestyle=(0, (5, 4)),
            mutation_scale=14,
            connectionstyle=f"arc3,rad={rad}",
        )
        ax.add_patch(arr)
        if label and label_xy is not None:
            mx, my = label_xy
            ax.text(mx, my, label,
                    fontsize=9.0, color=color, fontweight="bold",
                    ha="center", va="center",
                    bbox=dict(facecolor="white", edgecolor=color,
                              boxstyle="round,pad=0.18", linewidth=0.8,
                              alpha=0.95),
                    zorder=5)

    def human_icon(cx, cy, *, size=0.55, color=REVIEW_BORDER):
        """Small stick-figure denoting human-in-the-loop."""
        # Head
        ax.add_patch(Circle((cx, cy + size * 0.85), size * 0.30,
                            facecolor="white", edgecolor=color, linewidth=1.2,
                            zorder=6))
        # Body
        ax.plot([cx, cx], [cy + size * 0.55, cy - size * 0.10],
                color=color, linewidth=1.4, zorder=6)
        # Arms
        ax.plot([cx - size * 0.55, cx + size * 0.55],
                [cy + size * 0.30, cy + size * 0.30],
                color=color, linewidth=1.4, zorder=6)
        # Legs
        ax.plot([cx, cx - size * 0.40], [cy - size * 0.10, cy - size * 0.70],
                color=color, linewidth=1.4, zorder=6)
        ax.plot([cx, cx + size * 0.40], [cy - size * 0.10, cy - size * 0.70],
                color=color, linewidth=1.4, zorder=6)

    def clock_icon(cx, cy, *, r=0.55, color=FEEDBACK_COLOR):
        """Simple clock face."""
        ax.add_patch(Circle((cx, cy), r,
                            facecolor="white", edgecolor=color,
                            linewidth=1.4, zorder=6))
        # 12 + 6 + 3 + 9 ticks
        for ang_deg in (0, 90, 180, 270):
            a = math.radians(ang_deg)
            x1, y1 = cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a)
            x2, y2 = cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a)
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.0, zorder=7)
        # Hands: hour to 1 (~30deg from 12), minute to 12
        a_h = math.radians(60)   # 1 o'clock-ish
        ax.plot([cx, cx + r * 0.45 * math.cos(a_h)],
                [cy, cy + r * 0.45 * math.sin(a_h)],
                color=color, linewidth=1.4, zorder=7)
        a_m = math.radians(90)
        ax.plot([cx, cx + r * 0.65 * math.cos(a_m)],
                [cy, cy + r * 0.65 * math.sin(a_m)],
                color=color, linewidth=1.2, zorder=7)

    # ------------------------------------------------------------------
    # 1. Four telemetry channels (left column)
    # ------------------------------------------------------------------
    tel_x = 0.5
    tel_w = 7.5
    tel_h = 2.6
    tel_y_top = 21.5
    tel_v_gap = 0.6

    tel_titles = [
        ("Registration cadence",
         "3 / 70 / 111 = 184 users\n(Jan / Feb / Mar; 170 verified)"),
        ("Notification fan-out residue",
         "54 rows across 10 event types\n(durable health metric)"),
        ("WeChat outreach counter",
         "82 rows: 62 mkt + 16 ride + 4 act\n(grassroots bridge)"),
        ("User feedback inbox",
         "10 system_messages\n(sender_type=user, feedback)"),
    ]
    tel_anchors = []
    for i, (title, sub) in enumerate(tel_titles):
        y = tel_y_top - tel_h - i * (tel_h + tel_v_gap)
        a = block(tel_x, y, tel_w, tel_h, title, sub,
                  fill=TELEMETRY_FILL, border=TELEMETRY_BORDER,
                  header="«telemetry»")
        tel_anchors.append(a)

    # ------------------------------------------------------------------
    # 2. Summing junction (just right of the telemetry stack)
    # ------------------------------------------------------------------
    sum_cx = 11.0
    sum_cy = 13.5
    sj = sum_junction(sum_cx, sum_cy, r=1.0)

    # Arrows: each telemetry.right -> summing junction (left side of circle)
    for a in tel_anchors:
        # Approach the circle along its perimeter (use a slightly off-center
        # destination so multiple arrows do not collide)
        # offset y by direction
        dy_off = a["right"][1] - sj["center"][1]
        # Compute a point on the circle facing the source
        sx, sy = a["right"]
        cx, cy = sj["center"]
        ang = math.atan2(sy - cy, sx - cx)
        dst = (cx + sj["r"] * math.cos(ang),
               cy + sj["r"] * math.sin(ang))
        fwd_arrow((sx + 0.05, sy), dst, color=TELEMETRY_BORDER, lw=1.4,
                  rad=0.0)

    # ------------------------------------------------------------------
    # 3. Monthly snapshot review (with human-in-the-loop icon)
    # ------------------------------------------------------------------
    rev = block(14.0, 12.0, 7.5, 3.2,
                "Monthly snapshot review",
                "scan 4 channels +\nfeedback inbox; triage manually",
                fill=REVIEW_FILL, border=REVIEW_BORDER,
                header="(human-in-the-loop)")
    fwd_arrow(sj["right"], rev["left"], lw=1.6,
              label="aggregated\nsignal", label_dy=0.55)
    # human icon to the right-top of the review block
    human_icon(rev["x"] + rev["w"] - 0.85, rev["y"] + rev["h"] - 0.95,
               size=0.7)

    # ------------------------------------------------------------------
    # 4. HoQ refresh
    # ------------------------------------------------------------------
    hoq = block(23.0, 12.0, 7.0, 3.2,
                "HoQ refresh",
                "Figure ref:mbse-req-spec\nupdate CR x EC cell statuses",
                fill=HOQ_FILL, border=HOQ_BORDER,
                header="«artifact»")
    fwd_arrow(rev["right"], hoq["left"], lw=1.6,
              label="updated CR/EC\nrelationships", label_dy=0.55)

    # ------------------------------------------------------------------
    # 5. Release-track decisions
    # ------------------------------------------------------------------
    dec = block(31.5, 12.0, 7.0, 3.2,
                "Release-track decisions",
                "rank by leverage x risk\n(consult Fig. mbse-fmea)",
                fill=DECISION_FILL, border=DECISION_BORDER,
                header="«decision»")
    fwd_arrow(hoq["right"], dec["left"], lw=1.6,
              label="prioritized\nbacklog", label_dy=0.55)

    # ------------------------------------------------------------------
    # 6. Three release tracks (right side, stacked)
    # ------------------------------------------------------------------
    rel_w = 8.5
    rel_h = 2.4
    rel_x = 35.0
    rel_y_top = 22.0
    rel_v_gap = 0.55

    rel_titles = [
        ("(1) Provision points subsystem",
         "EC10  |  point_rules + point_transactions"),
        ("(2) Add dispute-window mechanism",
         "EC5 / EC7  |  rating revision constraint"),
        ("(3) Institution-domain whitelist",
         "EC12  |  multi-campus expansion gate"),
    ]
    rel_anchors = []
    for i, (title, sub) in enumerate(rel_titles):
        y = rel_y_top - rel_h - i * (rel_h + rel_v_gap)
        a = block(rel_x, y, rel_w, rel_h, title, sub,
                  fill=RELEASE_FILL, border=RELEASE_BORDER,
                  header="«release-track»")
        rel_anchors.append(a)
    # decision -> each release track
    for a in rel_anchors:
        # right edge of decision -> left edge of track
        # use slight curvature for visual separation
        # Decision exits from the right edge mid-y, then bends up/down
        sx, sy = dec["right"]
        dx, dy = a["left"]
        rad = -0.20 if dy > sy else 0.20
        fwd_arrow((sx, sy), (dx, dy), lw=1.3, rad=rad,
                  color=DECISION_BORDER)

    # ------------------------------------------------------------------
    # 7. Codebase deploy (bottom-right, gathering all three tracks)
    # ------------------------------------------------------------------
    dep = block(31.0, 4.5, 11.0, 2.6,
                "Codebase deploy",
                "Railway push  |  prod environment\nverify with Fig. mbse-verif TP.x",
                fill=DEPLOY_FILL, border=DEPLOY_BORDER,
                header="«deploy»")
    # Each release track -> deploy
    for a in rel_anchors:
        sx, sy = a["bottom"]
        dx, dy = dep["top"]
        # offset destination x for better visual separation
        # by track index
        idx = rel_anchors.index(a)
        dst_x = dep["top"][0] + (idx - 1) * 1.8
        dst = (dst_x, dep["top"][1])
        fwd_arrow((sx, sy), dst, color=RELEASE_BORDER, lw=1.2,
                  rad=0.0)

    # ------------------------------------------------------------------
    # 8. Closing feedback loop: deploy -> telemetry channels (dashed)
    # We route as an L-shaped path in three segments (avoids crossing
    # the decision/HoQ/review row).
    # ------------------------------------------------------------------
    # Path: deploy.bottom -> down to y=2.0 -> left to x=4.5 -> up to telemetry
    deploy_pt = (dep["x"] + dep["w"] / 2, dep["y"])
    p1 = (deploy_pt[0], 2.5)
    p2 = (4.5, 2.5)
    # Final feedback target: bottom-most telemetry channel (registration etc)
    tel_target = (tel_anchors[-1]["bottom"][0],
                  tel_anchors[-1]["bottom"][1])

    # Draw dashed manual segments using a single curved arrow with markers
    # Use Line2D for the segments (no head) and a final arrow with head.
    ax.plot([deploy_pt[0], p1[0]], [deploy_pt[1], p1[1]],
            color=FEEDBACK_COLOR, linewidth=1.6,
            linestyle=(0, (5, 4)), zorder=2)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
            color=FEEDBACK_COLOR, linewidth=1.6,
            linestyle=(0, (5, 4)), zorder=2)
    # Final segment with arrowhead -> bottom of last telemetry block
    feedback_arrow(p2, tel_target, color=FEEDBACK_COLOR, lw=1.6, rad=0.0)

    # Branch the feedback to all four telemetry blocks (light dashed)
    for a in tel_anchors[:-1]:
        ax.plot([4.5, a["bottom"][0]], [2.5, 2.5],
                color=FEEDBACK_COLOR, linewidth=0.8,
                linestyle=(0, (1, 3)), zorder=2)
        ax.plot([a["bottom"][0], a["bottom"][0]], [2.5, a["bottom"][1]],
                color=FEEDBACK_COLOR, linewidth=0.8,
                linestyle=(0, (1, 3)), zorder=2)
        # Tiny arrowhead at telemetry bottom
        feedback_arrow((a["bottom"][0], a["bottom"][1] - 0.6),
                       (a["bottom"][0], a["bottom"][1] - 0.05),
                       color=FEEDBACK_COLOR, lw=1.0)

    # Clock icon at the start of the feedback loop, with monthly cadence label
    clock_icon(deploy_pt[0] + 1.4, 2.0, r=0.55)
    ax.text(deploy_pt[0] + 2.4, 2.0,
            "monthly cadence",
            fontsize=9.5, fontweight="bold", color=FEEDBACK_COLOR,
            ha="left", va="center",
            bbox=dict(facecolor="white", edgecolor=FEEDBACK_COLOR,
                      boxstyle="round,pad=0.18", linewidth=0.9,
                      alpha=0.95),
            zorder=6)

    # Label the dashed loop near its left turn
    ax.text(p2[0] + 1.5, p2[1] + 0.5,
            "feedback (dashed) -> next snapshot",
            fontsize=8.5, color=FEEDBACK_COLOR, style="italic",
            ha="left", va="bottom",
            bbox=dict(facecolor="white", edgecolor=FEEDBACK_COLOR,
                      boxstyle="round,pad=0.15", linewidth=0.7,
                      alpha=0.95),
            zorder=6)

    # ------------------------------------------------------------------
    # Legend
    # ------------------------------------------------------------------
    legend_handles = [
        mpatches.Patch(facecolor=TELEMETRY_FILL, edgecolor=TELEMETRY_BORDER,
                       label="telemetry channel (instrumented)"),
        mpatches.Patch(facecolor=REVIEW_FILL, edgecolor=REVIEW_BORDER,
                       label="human-in-the-loop review"),
        mpatches.Patch(facecolor=HOQ_FILL, edgecolor=HOQ_BORDER,
                       label="HoQ artifact refresh"),
        mpatches.Patch(facecolor=DECISION_FILL, edgecolor=DECISION_BORDER,
                       label="decision block"),
        mpatches.Patch(facecolor=RELEASE_FILL, edgecolor=RELEASE_BORDER,
                       label="release track"),
        mpatches.Patch(facecolor=DEPLOY_FILL, edgecolor=DEPLOY_BORDER,
                       label="deploy block"),
        Line2D([0], [0], color=FORWARD_COLOR, linewidth=1.5,
               label="forward path"),
        Line2D([0], [0], color=FEEDBACK_COLOR, linewidth=1.5,
               linestyle=(0, (5, 4)), label="feedback (monthly)"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left", bbox_to_anchor=(0.005, 0.005),
        frameon=True, fontsize=8.6, handlelength=1.8,
        handletextpad=0.6, ncol=4,
        framealpha=0.95, edgecolor="#566573",
    )

    plt.tight_layout(pad=0.3)

    pdf, png = save_mpl("mbse_continuous_opt_loop", dpi=240)
    register("mbse_continuous_opt_loop", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
