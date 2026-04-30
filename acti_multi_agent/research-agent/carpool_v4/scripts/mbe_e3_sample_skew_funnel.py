"""mbe_e3 — Three-Layer Sample Skew Funnel.

A funnel/Sankey-style figure showing how the formative survey's N=117 raw
Qualtrics entries flow down through eligibility, branch into three concurrent
skew tracks (language, role, completion), and finally resolve to the F5-anchor
N=19 Driver/Both subset and N=12 Rider-only control.

Source-of-truth: §3.1 + §4.2 + §7.2 of the CampusRide draft (the
"three-layer sample skew" callout). Numbers are from the v4.2 cohort
correction (117 → 111 eligible; 91/111 reported native language; F5 reported
on N=19 Driver/Both with N=12 Rider-only control).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    renderer, setup_mpl, save_mpl, register, DRIVER_COLOR, RIDER_COLOR,
)


# --- Palette ---------------------------------------------------------------
MAND_COLOR = "#1ABC9C"     # Mandarin
ENG_COLOR = "#F39C12"      # English
OTH_COLOR = "#BDC3C7"      # Other / unreported
GREY_NR = "#95A5A6"        # not-reported
COMPLETED = "#27AE60"      # finished all
NOT_FINISHED = "#A9DFBF"   # partially completed (lighter green)
EXCLUDED = "#E74C3C"       # excluded (test rows)
TRUNK = "#34495E"          # neutral dark

# Layout constants (data coordinates)
FIG_W, FIG_H = 13.0, 8.0


@renderer("mbe_e3_sample_skew_funnel")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("auto")
    ax.axis("off")

    # =====================================================================
    # Title
    # =====================================================================
    ax.text(50, 97,
            "Three-Layer Sample Skew of the Formative Survey",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TRUNK)
    ax.text(50, 93.6,
            "Qualtrics N=117 raw  >  N=111 eligible  >  branching skew tracks  >  "
            "F5 anchor on N=19 Driver/Both",
            ha="center", va="center", fontsize=10, color="#555555",
            style="italic")

    # =====================================================================
    # Track 1: Eligibility funnel  (top band, y ~ 80-90)
    # =====================================================================
    # Three boxes: 117 raw  -- exclude 6 -->  111 eligible
    def box(x, y, w, h, label, fill, edge, fontsize=10, weight="normal",
            text_color="black"):
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.6",
            linewidth=1.4, edgecolor=edge, facecolor=fill,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label,
                ha="center", va="center", fontsize=fontsize,
                color=text_color, fontweight=weight)
        return rect

    # Track 1 label
    ax.text(2.0, 85, "TRACK 1\nEligibility",
            ha="left", va="center", fontsize=9.5, color=TRUNK,
            fontweight="bold")

    # Raw entries (wide, on the left)
    box(13, 80, 22, 9, "N=117\nQualtrics raw entries",
        fill="#FDEBD0", edge="#B9770E", fontsize=11, weight="bold")
    # Excluded
    box(40, 80, 18, 9, "−6\nSurvey-Preview\ntest rows",
        fill="#FADBD8", edge=EXCLUDED, fontsize=9.5, text_color=EXCLUDED)
    # Eligible
    box(63, 80, 22, 9, "N=111\neligible respondents",
        fill="#D6EAF8", edge="#1F618D", fontsize=11, weight="bold")

    # Arrows
    ax.annotate("", xy=(40, 84.5), xytext=(35, 84.5),
                arrowprops=dict(arrowstyle="->", color=TRUNK, lw=1.4))
    ax.annotate("", xy=(63, 84.5), xytext=(58, 84.5),
                arrowprops=dict(arrowstyle="->", color=TRUNK, lw=1.4))

    # =====================================================================
    # Trunk descending from 111 → branch point at y ~ 73
    # =====================================================================
    ax.annotate("", xy=(74, 74), xytext=(74, 80),
                arrowprops=dict(arrowstyle="-", color=TRUNK, lw=1.6))
    # Horizontal trunk that fans out into 3 tracks
    ax.annotate("", xy=(74, 73), xytext=(74, 73),
                arrowprops=dict(arrowstyle="-", color=TRUNK, lw=1.4))

    # =====================================================================
    # Track 2: Language skew (left column),  Track 3: Role skew (middle),
    # Track 4: Completion skew (right column).
    # All three branch from the eligible-111 node.
    # =====================================================================

    # Header row for the three branching tracks
    track_y_top = 70
    track_x = {
        "lang": 6,       # column 1 left edge
        "role": 38,      # column 2 left edge
        "comp": 70,      # column 3 left edge
    }
    track_w = 26

    # Track header bars
    for key, label, color in [
        ("lang", "TRACK 2 — Language skew", "#117A65"),
        ("role", "TRACK 3 — Role skew", "#7B241C"),
        ("comp", "TRACK 4 — Completion skew", "#1F618D"),
    ]:
        x = track_x[key]
        rect = Rectangle((x, track_y_top), track_w, 3.5,
                         facecolor=color, edgecolor="none", alpha=0.92)
        ax.add_patch(rect)
        ax.text(x + track_w / 2, track_y_top + 1.75, label,
                ha="center", va="center", fontsize=10, fontweight="bold",
                color="white")

    # Connectors: from the 111 box down/over to each track header
    for key in ("lang", "role", "comp"):
        x = track_x[key] + track_w / 2
        ax.annotate("", xy=(x, track_y_top + 3.5), xytext=(74, 80),
                    arrowprops=dict(arrowstyle="-", color=TRUNK,
                                    lw=1.0, alpha=0.55,
                                    connectionstyle="arc3,rad=0.0"))

    # ---------- Track 2: Language skew ------------------------------------
    # Stage A: 111 → 91 reported / 20 didn't report
    # Stage B: of 91 → 72 Mandarin / 15 English / 4 Other
    lang_x = track_x["lang"]
    # Stage A: stacked horizontal bar
    stage_a_y = 62
    stage_a_h = 5.5
    # Bar width split: 91/111 vs 20/111
    total = 111
    rep_w = (91 / total) * track_w
    nrp_w = (20 / total) * track_w
    ax.add_patch(Rectangle((lang_x, stage_a_y), rep_w, stage_a_h,
                           facecolor="#A3E4D7", edgecolor="#117A65",
                           linewidth=1.2))
    ax.add_patch(Rectangle((lang_x + rep_w, stage_a_y), nrp_w, stage_a_h,
                           facecolor=GREY_NR, edgecolor="#7F8C8D",
                           linewidth=1.0))
    ax.text(lang_x + rep_w / 2, stage_a_y + stage_a_h / 2,
            "reported\nnative lang.\n91", ha="center", va="center",
            fontsize=8, color="#0E6251")
    ax.text(lang_x + rep_w + nrp_w / 2, stage_a_y + stage_a_h / 2,
            "n/r\n20", ha="center", va="center", fontsize=7.5,
            color="#2C3E50")

    # Stage B: stacked bar of the 91 sub-cohort
    stage_b_y = 52
    stage_b_h = 6
    sub = 91
    m_w = (72 / sub) * track_w
    e_w = (15 / sub) * track_w
    o_w = (4 / sub) * track_w
    ax.add_patch(Rectangle((lang_x, stage_b_y), m_w, stage_b_h,
                           facecolor=MAND_COLOR, edgecolor="#0E6251",
                           linewidth=1.2))
    ax.add_patch(Rectangle((lang_x + m_w, stage_b_y), e_w, stage_b_h,
                           facecolor=ENG_COLOR, edgecolor="#9C640C",
                           linewidth=1.2))
    ax.add_patch(Rectangle((lang_x + m_w + e_w, stage_b_y), o_w, stage_b_h,
                           facecolor=OTH_COLOR, edgecolor="#7F8C8D",
                           linewidth=1.0))
    ax.text(lang_x + m_w / 2, stage_b_y + stage_b_h / 2,
            "Mandarin\n72 (79%)", ha="center", va="center",
            fontsize=9, color="white", fontweight="bold")
    ax.text(lang_x + m_w + e_w / 2, stage_b_y + stage_b_h / 2,
            "English\n15 (16%)", ha="center", va="center",
            fontsize=8, color="white", fontweight="bold")
    ax.text(lang_x + m_w + e_w + o_w / 2, stage_b_y + stage_b_h / 2 + 1.6,
            "Other", ha="center", va="center", fontsize=7,
            color="#2C3E50")
    ax.text(lang_x + m_w + e_w + o_w / 2, stage_b_y + stage_b_h / 2 - 1.6,
            "4 (5%)", ha="center", va="center", fontsize=7,
            color="#2C3E50")

    # Connector from stage A → stage B (only the 91 subcohort)
    ax.annotate("", xy=(lang_x + rep_w / 2, stage_b_y + stage_b_h),
                xytext=(lang_x + rep_w / 2, stage_a_y),
                arrowprops=dict(arrowstyle="->", color="#117A65",
                                lw=1.2, alpha=0.7))

    # Stage labels
    ax.text(lang_x - 0.5, stage_a_y + stage_a_h / 2,
            "Stage A\n(N=111)", ha="right", va="center",
            fontsize=8, color="#117A65", fontweight="bold")
    ax.text(lang_x - 0.5, stage_b_y + stage_b_h / 2,
            "Stage B\n(N=91)", ha="right", va="center",
            fontsize=8, color="#117A65", fontweight="bold")

    # ---------- Track 3: Role skew ----------------------------------------
    role_x = track_x["role"]
    # Stage A: 56 Rider, 23 Driver, 22 Both, 10 unreported (sum=111)
    stage_a_y_r = 62
    stage_a_h_r = 5.5
    total_r = 111
    r_w = (56 / total_r) * track_w
    d_w = (23 / total_r) * track_w
    b_w = (22 / total_r) * track_w
    u_w = (10 / total_r) * track_w
    ax.add_patch(Rectangle((role_x, stage_a_y_r), r_w, stage_a_h_r,
                           facecolor=RIDER_COLOR, edgecolor="#1A5276",
                           linewidth=1.2))
    ax.add_patch(Rectangle((role_x + r_w, stage_a_y_r), d_w, stage_a_h_r,
                           facecolor=DRIVER_COLOR, edgecolor="#7B241C",
                           linewidth=1.2))
    ax.add_patch(Rectangle((role_x + r_w + d_w, stage_a_y_r),
                           b_w, stage_a_h_r,
                           facecolor="#E59866", edgecolor="#7B241C",
                           linewidth=1.2))
    ax.add_patch(Rectangle((role_x + r_w + d_w + b_w, stage_a_y_r),
                           u_w, stage_a_h_r,
                           facecolor=GREY_NR, edgecolor="#7F8C8D",
                           linewidth=1.0))

    ax.text(role_x + r_w / 2, stage_a_y_r + stage_a_h_r / 2,
            "Rider\n56", ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold")
    ax.text(role_x + r_w + d_w / 2, stage_a_y_r + stage_a_h_r / 2,
            "Drv\n23", ha="center", va="center",
            fontsize=7.5, color="white", fontweight="bold")
    ax.text(role_x + r_w + d_w + b_w / 2, stage_a_y_r + stage_a_h_r / 2,
            "Both\n22", ha="center", va="center",
            fontsize=7.5, color="white", fontweight="bold")
    ax.text(role_x + r_w + d_w + b_w + u_w / 2,
            stage_a_y_r + stage_a_h_r / 2,
            "n/r\n10", ha="center", va="center",
            fontsize=7, color="#2C3E50")

    ax.text(role_x - 0.5, stage_a_y_r + stage_a_h_r / 2,
            "Stage A\n(N=111)", ha="right", va="center",
            fontsize=8, color="#7B241C", fontweight="bold")

    # Stage B: pooled Driver/Both = 45 self-identified driver-experienced
    stage_b_y_r = 52
    stage_b_h_r = 6
    pooled_w = ((23 + 22) / total_r) * track_w
    rider_w = (56 / total_r) * track_w
    # Show the pooled box (offset under driver+both region of stage A)
    pooled_x = role_x + r_w
    ax.add_patch(FancyBboxPatch(
        (pooled_x, stage_b_y_r), pooled_w, stage_b_h_r,
        boxstyle="round,pad=0.02,rounding_size=0.4",
        facecolor="#F5CBA7", edgecolor=DRIVER_COLOR, linewidth=1.6))
    ax.text(pooled_x + pooled_w / 2, stage_b_y_r + stage_b_h_r / 2,
            "Driver + Both = 45\n(driver-experienced)",
            ha="center", va="center", fontsize=8.5, color="#7B241C",
            fontweight="bold")
    # Show the rider-only control box
    ax.add_patch(FancyBboxPatch(
        (role_x, stage_b_y_r), rider_w, stage_b_h_r,
        boxstyle="round,pad=0.02,rounding_size=0.4",
        facecolor="#AED6F1", edgecolor=RIDER_COLOR, linewidth=1.4))
    ax.text(role_x + rider_w / 2, stage_b_y_r + stage_b_h_r / 2,
            "Rider-only pool = 56", ha="center", va="center",
            fontsize=8.5, color="#1A5276", fontweight="bold")

    ax.text(role_x - 0.5, stage_b_y_r + stage_b_h_r / 2,
            "Stage B\n(pooled)", ha="right", va="center",
            fontsize=8, color="#7B241C", fontweight="bold")

    # Stage C: Q24 analyzable subsets
    stage_c_y_r = 42
    stage_c_h_r = 6
    # Driver/Both Q24
    db_x = role_x + r_w
    ax.add_patch(FancyBboxPatch(
        (db_x, stage_c_y_r), pooled_w, stage_c_h_r,
        boxstyle="round,pad=0.02,rounding_size=0.4",
        facecolor=DRIVER_COLOR, edgecolor="#641E16", linewidth=1.8))
    ax.text(db_x + pooled_w / 2, stage_c_y_r + stage_c_h_r / 2 + 1.0,
            "Q24 Driver/Both", ha="center", va="center", fontsize=8.5,
            color="white", fontweight="bold")
    ax.text(db_x + pooled_w / 2, stage_c_y_r + stage_c_h_r / 2 - 1.4,
            "N=19 (loose) / 17 (strict)", ha="center", va="center",
            fontsize=8, color="white")
    # Rider Q24 control
    ax.add_patch(FancyBboxPatch(
        (role_x, stage_c_y_r), rider_w, stage_c_h_r,
        boxstyle="round,pad=0.02,rounding_size=0.4",
        facecolor=RIDER_COLOR, edgecolor="#154360", linewidth=1.6))
    ax.text(role_x + rider_w / 2, stage_c_y_r + stage_c_h_r / 2 + 1.0,
            "Q24 Rider-only control", ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold")
    ax.text(role_x + rider_w / 2, stage_c_y_r + stage_c_h_r / 2 - 1.4,
            "N=12 (loose) / 11 (strict)", ha="center", va="center",
            fontsize=8, color="white")

    ax.text(role_x - 0.5, stage_c_y_r + stage_c_h_r / 2,
            "Stage C\nQ24 subset", ha="right", va="center",
            fontsize=8, color="#7B241C", fontweight="bold")

    # Connectors A→B and B→C inside Track 3
    ax.annotate("", xy=(db_x + pooled_w / 2, stage_b_y_r + stage_b_h_r),
                xytext=(role_x + r_w + d_w / 2 + 1, stage_a_y_r),
                arrowprops=dict(arrowstyle="->", color=DRIVER_COLOR,
                                lw=1.2, alpha=0.7))
    ax.annotate("", xy=(db_x + pooled_w / 2, stage_c_y_r + stage_c_h_r),
                xytext=(db_x + pooled_w / 2, stage_b_y_r),
                arrowprops=dict(arrowstyle="->", color=DRIVER_COLOR,
                                lw=1.6, alpha=0.85))
    ax.annotate("", xy=(role_x + rider_w / 2, stage_c_y_r + stage_c_h_r),
                xytext=(role_x + rider_w / 2, stage_b_y_r),
                arrowprops=dict(arrowstyle="->", color=RIDER_COLOR,
                                lw=1.4, alpha=0.85))

    # ---------- Track 4: Completion skew ----------------------------------
    comp_x = track_x["comp"]
    stage_a_y_c = 62
    stage_a_h_c = 5.5
    total_c = 111
    fin_w = (44 / total_c) * track_w
    par_w = (67 / total_c) * track_w
    ax.add_patch(Rectangle((comp_x, stage_a_y_c), fin_w, stage_a_h_c,
                           facecolor=COMPLETED, edgecolor="#196F3D",
                           linewidth=1.2))
    ax.add_patch(Rectangle((comp_x + fin_w, stage_a_y_c), par_w, stage_a_h_c,
                           facecolor=NOT_FINISHED, edgecolor="#52BE80",
                           linewidth=1.0))
    ax.text(comp_x + fin_w / 2, stage_a_y_c + stage_a_h_c / 2,
            "Finished\n44 (40%)", ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold")
    ax.text(comp_x + fin_w + par_w / 2, stage_a_y_c + stage_a_h_c / 2,
            "Partial\n67 (60%)", ha="center", va="center",
            fontsize=8.5, color="#1B4F33", fontweight="bold")

    ax.text(comp_x - 0.5, stage_a_y_c + stage_a_h_c / 2,
            "Stage A\n(N=111)", ha="right", va="center",
            fontsize=8, color="#1F618D", fontweight="bold")

    # Stage B implication (annotation on completion):
    impl_y = 50
    ax.text(comp_x + track_w / 2, impl_y + 4.5,
            "Implication", ha="center", va="center", fontsize=9,
            color="#1F618D", fontweight="bold")
    ax.add_patch(FancyBboxPatch(
        (comp_x + 0.5, impl_y - 4.5), track_w - 1.0, 8.5,
        boxstyle="round,pad=0.02,rounding_size=0.4",
        facecolor="#EBF5FB", edgecolor="#1F618D", linewidth=1.2))
    ax.text(comp_x + track_w / 2, impl_y + 1.4,
            "Per-question N varies.",
            ha="center", va="center", fontsize=8.5, color="#1B4F72")
    ax.text(comp_x + track_w / 2, impl_y - 1.0,
            "F1–F4 use loose dropna.",
            ha="center", va="center", fontsize=8.5, color="#1B4F72")
    ax.text(comp_x + track_w / 2, impl_y - 3.4,
            "F5 strictly subsets to Q24-completers.",
            ha="center", va="center", fontsize=8.5, color="#1B4F72",
            style="italic")

    # =====================================================================
    # Funnel narrowing visual cue: dashed envelope from wide top to narrow F5
    # =====================================================================
    from matplotlib.patches import Polygon
    envelope = Polygon(
        [(13, 89), (85, 89),    # top edge of Track 1 117/111 boxes
         (75, 16), (25, 16)],   # narrow at F5 callout
        closed=True, fill=False,
        edgecolor="#BDC3C7", linestyle=(0, (4, 3)), linewidth=1.0,
        alpha=0.65,
    )
    ax.add_patch(envelope)

    # =====================================================================
    # F5 anchor callout box (bottom)
    # =====================================================================
    callout_x, callout_y = 14, 4.0
    callout_w, callout_h = 72, 11.5
    ax.add_patch(FancyBboxPatch(
        (callout_x, callout_y), callout_w, callout_h,
        boxstyle="round,pad=0.02,rounding_size=0.8",
        facecolor="#FDEDEC", edgecolor=DRIVER_COLOR, linewidth=2.2))
    ax.text(callout_x + 1.5, callout_y + callout_h - 1.6,
            "F5 anchor (rating-fairness asymmetry)",
            ha="left", va="center", fontsize=11.5, fontweight="bold",
            color=DRIVER_COLOR)
    ax.text(callout_x + 1.5, callout_y + callout_h - 4.2,
            "• F5 sample = N=19 Driver/Both (loose per-item dropna); "
            "Rider-only control N=12.",
            ha="left", va="center", fontsize=9.5, color="#641E16")
    ax.text(callout_x + 1.5, callout_y + callout_h - 6.6,
            "• Modal CHI sample size = 12 (Caine 2016); "
            "N=19 falls within the formative-design distribution.",
            ha="left", va="center", fontsize=9.5, color="#641E16")
    ax.text(callout_x + 1.5, callout_y + callout_h - 9.0,
            "• Full-sample N=30 mixed reporting is methodologically "
            "inappropriate (cf. §4.2).",
            ha="left", va="center", fontsize=9.5, color="#641E16",
            style="italic")

    # Arrow from Track 3 Stage C (Driver/Both N=19 box) into the callout
    ax.annotate(
        "", xy=(45, callout_y + callout_h),
        xytext=(role_x + r_w + d_w / 2 + 5, stage_c_y_r),
        arrowprops=dict(arrowstyle="->", color=DRIVER_COLOR, lw=2.0,
                        alpha=0.9, connectionstyle="arc3,rad=-0.15"),
    )

    # =====================================================================
    # Legend
    # =====================================================================
    legend_handles = [
        mpatches.Patch(facecolor=MAND_COLOR, edgecolor="#0E6251",
                       label="Mandarin"),
        mpatches.Patch(facecolor=ENG_COLOR, edgecolor="#9C640C",
                       label="English"),
        mpatches.Patch(facecolor=OTH_COLOR, edgecolor="#7F8C8D",
                       label="Other / not reported"),
        mpatches.Patch(facecolor=RIDER_COLOR, edgecolor="#1A5276",
                       label="Rider-only"),
        mpatches.Patch(facecolor=DRIVER_COLOR, edgecolor="#641E16",
                       label="Driver / Both (driver-experienced)"),
        mpatches.Patch(facecolor=COMPLETED, edgecolor="#196F3D",
                       label="Completed"),
        mpatches.Patch(facecolor=NOT_FINISHED, edgecolor="#52BE80",
                       label="Partially completed"),
    ]
    ax.legend(handles=legend_handles, loc="lower center",
              bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False,
              fontsize=8.5, handlelength=1.2, columnspacing=1.4)

    plt.tight_layout()
    pdf, png = save_mpl("mbe_e3_sample_skew_funnel", dpi=300)
    register("mbe_e3_sample_skew_funnel", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
