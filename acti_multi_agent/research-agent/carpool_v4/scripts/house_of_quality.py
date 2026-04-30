"""House of Quality (HoQ) for CampusRide v4.4.

Maps survey-derived customer requirements (F1-F6) to engineering characteristics
(the design features in §5), with implementation status and importance weights
suitable for a continuous-optimization audit and a multi-campus expansion brief.

Run:
    .venv/bin/python carpool_v4/scripts/house_of_quality.py
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "carpool_v4" / "output" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["pdf.fonttype"] = 42

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

# (label, importance 1-5, evidence anchor)
CUSTOMER_REQS = [
    ("Affordable rides", 5, "F1: 28/32 perceive Uber as higher priced"),
    ("Reliable availability", 4, "F1: 23/32 report Uber availability difficulty"),
    ("Identity-verified peers", 5, "F3: .edu WTP mean 67.3 / median 79"),
    ("In-trip safety", 5, "F3: location-share WTP 69.1; SOS 63.5"),
    ("Fair driver feedback", 5, "F5: driver/both unfair-rating tolerance 29.1"),
    ("Cost-splitting benefit", 5, "F4: financial motivation 63.6, top tier"),
    ("Cross-module coordination", 4, "Grassroots literature + 17/21 mandarin WeChat"),
    ("Long-distance matching", 4, "F6: 12/33 long-distance supply willingness"),
    ("Post-trip resolution channel", 3, "Audit gap (§5.10 limitations)"),
    ("Transferable to other campuses", 3, "Multi-campus generalization argument"),
]

# (short label, full label, status, target / metric, deployed evidence)
ENG_CHARS = [
    ("EC1", ".edu email gate",          "deployed", "100% .edu addresses",        "184/184 @cornell.edu"),
    ("EC2", "Verified-Cornell badge",   "deployed", "On every driver/passenger card", "ride/profile cards live"),
    ("EC3", "Real-time location share", "deployed", "Sub-2s update jitter",        "Socket.IO room scoped"),
    ("EC4", "One-tap SOS",              "deployed", "<3s notif fan-out",           "0 activations to date"),
    ("EC5", "1-5 bidirectional rating", "deployed", "Both sides rate",             "0 rows in production"),
    ("EC6", "2h post-departure delay",  "deployed", "Window opens at +2h",         "8 reminder rows queued"),
    ("EC7", "Update-in-place revision", "deployed", "1 row per (trip,rater,ratee)","schema enforced"),
    ("EC8", "Ride-scoped group chat",   "deployed", "1h post-departure expiry",    "82 wxgroup pushes ride-tagged"),
    ("EC9", "WeChat cross-post bridge", "deployed", "Auto on every new artifact",  "62 marketplace / 16 ride / 4 act."),
    ("EC10", "Cross-module points",     "specified","Per-rule cap below cash",      "0 point_rules in production"),
    ("EC11", "3-distance ride taxonomy","deployed", "in/short/long zones",         "ride model live"),
    ("EC12", "Institution-domain WL",   "pending",  ".edu domain → cohort cohort",  "Cornell-only as of 2026-04"),
]

STATUS_COLORS = {
    "deployed":  "#2ECC71",
    "specified": "#F39C12",
    "pending":   "#7F8C8D",
}

# Relationship matrix: rows = CUSTOMER_REQS, cols = ENG_CHARS
# 9 = strong (●), 3 = medium (◐), 1 = weak (○), 0 = none
REL = [
    # EC1 EC2 EC3 EC4 EC5 EC6 EC7 EC8 EC9 EC10 EC11 EC12
    [   0,   0,   0,   0,   0,   0,   0,   0,   3,   3,   0,   0],   # Affordable rides
    [   0,   0,   0,   0,   0,   0,   0,   3,   3,   0,   3,   0],   # Reliable availability
    [   9,   9,   0,   0,   3,   0,   0,   1,   0,   0,   0,   9],   # Identity-verified peers
    [   1,   0,   9,   9,   3,   0,   0,   3,   0,   0,   0,   0],   # In-trip safety
    [   0,   0,   0,   0,   3,   9,   3,   0,   0,   1,   0,   0],   # Fair driver feedback
    [   0,   0,   0,   0,   0,   0,   0,   0,   3,   1,   0,   0],   # Cost-splitting
    [   3,   1,   0,   0,   0,   0,   0,   9,   9,   3,   0,   0],   # Cross-module coordination
    [   0,   0,   0,   0,   0,   0,   0,   0,   3,   0,   9,   0],   # Long-distance matching
    [   0,   0,   0,   0,   3,   0,   9,   3,   0,   0,   0,   0],   # Post-trip resolution
    [   9,   1,   0,   0,   0,   0,   0,   0,   3,   0,   0,   9],   # Multi-campus transferable
]

# Roof correlations: positive(+1, +2 strong), negative(-1, -2 strong), 0 none
# Indexed by (i, j) with i < j among ENG_CHARS
ROOF = {
    (0, 1):  +2,   # .edu gate ↔ Cornell badge: strong positive (one enables the other)
    (0, 11): +2,   # .edu gate ↔ inst-domain whitelist: strong positive (special case)
    (2, 3):  +1,   # location share ↔ SOS: positive (shared safety substrate)
    (4, 5):  +1,   # rating ↔ 2h delay: positive (both rating mechanism)
    (4, 6):  -2,   # rating ↔ update-in-place: NEG (revision can be retaliatory)
    (4, 9):  +1,   # rating ↔ points: positive (good ratings reinforce point loop)
    (5, 6):  -1,   # 2h delay ↔ update-in-place: NEG (delay nullified if revisable forever)
    (7, 8):  +2,   # ride-scoped chat ↔ wechat bridge: strong positive (coupled comms)
    (7, 11): +1,   # ride-scoped chat ↔ inst-domain whitelist: positive (campus-bounded)
    (10, 7): +1,   # 3-distance taxonomy ↔ ride-scoped chat: positive (long trips need chat)
}

# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def _draw_relationship_marker(ax, x, y, val, size=0.36):
    if val == 9:
        ax.add_patch(plt.Circle((x, y), size, color="#1A5276", zorder=3))
        ax.text(x, y, "●", color="white", ha="center", va="center",
                fontsize=11, fontweight="bold", zorder=4)
    elif val == 3:
        ax.add_patch(plt.Circle((x, y), size, edgecolor="#1A5276",
                                facecolor="#5DADE2", linewidth=1.5, zorder=3))
    elif val == 1:
        ax.add_patch(plt.Circle((x, y), size * 0.55, edgecolor="#1A5276",
                                facecolor="white", linewidth=1.0, zorder=3))


def _draw_roof_marker(ax, x, y, val, size=0.18):
    if val == +2:
        ax.text(x, y, "▲", ha="center", va="center", fontsize=11,
                color="#27AE60", fontweight="bold")
    elif val == +1:
        ax.text(x, y, "△", ha="center", va="center", fontsize=10,
                color="#27AE60")
    elif val == -1:
        ax.text(x, y, "▽", ha="center", va="center", fontsize=10,
                color="#C0392B")
    elif val == -2:
        ax.text(x, y, "▼", ha="center", va="center", fontsize=11,
                color="#C0392B", fontweight="bold")


# ---------------------------------------------------------------------------
# Build figure
# ---------------------------------------------------------------------------

def build_hoq() -> Path:
    n_cr = len(CUSTOMER_REQS)
    n_ec = len(ENG_CHARS)
    rel_arr = np.array(REL, dtype=int)

    # Compute technical importance: sum_i (importance_i × rel[i,j])
    importance = np.array([cr[1] for cr in CUSTOMER_REQS])
    tech_importance = (rel_arr * importance[:, None]).sum(axis=0)
    tech_importance_pct = tech_importance / tech_importance.sum() * 100

    fig, ax = plt.subplots(figsize=(22, 17))
    ax.set_aspect("equal")
    ax.axis("off")

    # Geometry
    cell = 1.0
    matrix_x0 = 7.5  # left edge of relationship matrix

    # Layout y-coords (top to bottom): roof(top), HOW labels, matrix rows, status/target/importance(below)
    # Place from bottom upward:
    ROW_TGT_PCT = 0.5            # technical importance bar bottom
    ROW_TGT_TXT = ROW_TGT_PCT + 2.0  # target / metric text (1.5 tall)
    ROW_STATUS  = ROW_TGT_TXT + 1.6  # status badge (1.0 tall)
    MATRIX_BOT  = ROW_STATUS + 1.4  # matrix bottom edge
    MATRIX_TOP  = MATRIX_BOT + n_cr * cell  # matrix top edge
    HOW_LABELS  = MATRIX_TOP + 0.6    # HOW (EC) labels just above matrix
    ROOF_BASE   = HOW_LABELS + 3.4    # roof correlations begin above labels

    # ---------- HOW labels (vertical, above matrix) ----------
    for j, (short, full, status, target, evid) in enumerate(ENG_CHARS):
        x = matrix_x0 + j * cell + cell/2
        ax.text(x, HOW_LABELS + 0.05, f"{short}: {full}",
                ha="left", va="bottom", rotation=45,
                fontsize=10, fontweight="bold")

    # ---------- Roof (correlation triangle) ----------
    # Build a proper diamond roof: vertical position scales with horizontal distance |j-i|
    roof_dy = 0.30
    # Roof outer border (true triangle)
    apex_x = matrix_x0 + n_ec * cell / 2
    apex_y = ROOF_BASE + (n_ec - 1) * roof_dy * 0.5 + 0.6
    base_left  = (matrix_x0,                ROOF_BASE - 0.10)
    base_right = (matrix_x0 + n_ec * cell,  ROOF_BASE - 0.10)
    ax.plot([base_left[0], apex_x], [base_left[1], apex_y],
            color="#999", lw=1.0, alpha=0.7, zorder=1)
    ax.plot([base_right[0], apex_x], [base_right[1], apex_y],
            color="#999", lw=1.0, alpha=0.7, zorder=1)
    ax.plot([base_left[0], base_right[0]], [base_left[1], base_right[1]],
            color="#999", lw=1.0, alpha=0.7, zorder=1)
    # Faint internal grid for the diamond cells
    for d in range(1, n_ec):
        x_lo = matrix_x0 + d * cell / 2
        x_hi = matrix_x0 + n_ec * cell - d * cell / 2
        y = ROOF_BASE + (d - 1) * roof_dy
        ax.plot([x_lo, x_hi], [y, y], color="#DDD", lw=0.4, alpha=0.5, zorder=1)
    for (i, j), val in ROOF.items():
        x_mid = matrix_x0 + (i + j) / 2 * cell + cell/2
        y = ROOF_BASE + (j - i - 1) * roof_dy
        _draw_roof_marker(ax, x_mid, y, val, size=0.15)

    # ---------- WHAT (Customer Req) labels + importance column ----------
    imp_col_x = matrix_x0 - 7.4
    for i, (label, imp, evid) in enumerate(CUSTOMER_REQS):
        # WHATs label (left of matrix)
        y = MATRIX_BOT + (n_cr - 1 - i) * cell + cell/2
        ax.text(matrix_x0 - 0.20, y + 0.13, label,
                ha="right", va="center", fontsize=10.5, fontweight="bold")
        # Evidence pointer in smaller text on a separate line
        ax.text(matrix_x0 - 0.20, y - 0.27, evid,
                ha="right", va="center", fontsize=7.8, color="#555", style="italic")
        # Importance column
        ax.add_patch(plt.Rectangle(
            (imp_col_x - 0.40, y - cell/2 + 0.08), 0.80, cell - 0.16,
            facecolor="#FCF3CF", edgecolor="#B7950B", lw=0.8, zorder=2))
        ax.text(imp_col_x, y, str(imp),
                ha="center", va="center", fontsize=12, fontweight="bold",
                color="#7D6608", zorder=3)

    # Headers
    ax.text(imp_col_x, MATRIX_TOP + 0.20, "Imp",
            ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.text(matrix_x0 - 0.20, MATRIX_TOP + 0.20, "WHAT (Customer Requirement)",
            ha="right", va="bottom", fontsize=11, fontweight="bold")
    ax.text(matrix_x0 + n_ec * cell / 2, ROOF_BASE + (n_ec - 1) * roof_dy * 0.5 + 1.0,
            "HOW (Engineering Characteristic) →", ha="center", va="bottom",
            fontsize=12, fontweight="bold")

    # ---------- Relationship matrix ----------
    for i in range(n_cr):
        for j in range(n_ec):
            x = matrix_x0 + j * cell + cell/2
            y = MATRIX_BOT + (n_cr - 1 - i) * cell + cell/2
            # cell border
            ax.add_patch(plt.Rectangle(
                (matrix_x0 + j * cell, MATRIX_BOT + (n_cr - 1 - i) * cell),
                cell, cell, facecolor="white",
                edgecolor="#CCC", lw=0.5, zorder=1))
            _draw_relationship_marker(ax, x, y, rel_arr[i, j])

    # ---------- Bottom: status / target / tech-importance bars ----------
    max_pct = tech_importance_pct.max()
    for j, (short, full, status, target, evid) in enumerate(ENG_CHARS):
        x_left = matrix_x0 + j * cell
        x_mid = x_left + cell/2

        # Status badge
        color = STATUS_COLORS.get(status, "#999")
        ax.add_patch(plt.Rectangle(
            (x_left + 0.06, ROW_STATUS + 0.10), cell - 0.12, 0.85,
            facecolor=color, alpha=0.85, edgecolor="black", lw=0.5, zorder=2))
        ax.text(x_mid, ROW_STATUS + 0.52, status,
                ha="center", va="center", fontsize=8.5, color="white",
                fontweight="bold", zorder=3)

        # Target / Live evidence panel (taller, more legible)
        ax.add_patch(plt.Rectangle(
            (x_left + 0.04, ROW_TGT_TXT), cell - 0.08, 1.45,
            facecolor="#FBFCFC", edgecolor="#CCC", lw=0.4, zorder=1))
        # Wrap text into multiple lines via textwrap
        import textwrap
        target_lines = textwrap.wrap(target, width=14) or [""]
        for k, line in enumerate(target_lines[:2]):
            ax.text(x_mid, ROW_TGT_TXT + 1.20 - k * 0.22, line,
                    ha="center", va="center", fontsize=7.2, color="#222")
        evid_lines = textwrap.wrap(evid, width=15) or [""]
        for k, line in enumerate(evid_lines[:2]):
            ax.text(x_mid, ROW_TGT_TXT + 0.55 - k * 0.22, line,
                    ha="center", va="center", fontsize=6.5, color="#666", style="italic")

        # Tech-importance bar (height proportional to %)
        bar_h = 1.30 * tech_importance_pct[j] / max_pct
        ax.add_patch(plt.Rectangle(
            (x_left + 0.18, ROW_TGT_PCT), cell - 0.36, bar_h,
            facecolor="#5499C7", edgecolor="#1F618D", lw=0.6, zorder=2))
        ax.text(x_mid, ROW_TGT_PCT + bar_h + 0.10,
                f"{tech_importance_pct[j]:.0f}%",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold",
                color="#1F618D")

    # Row labels for bottom rows
    label_x = matrix_x0 - 0.20
    ax.text(label_x, ROW_STATUS + 0.52, "Status",
            ha="right", va="center", fontsize=10, fontweight="bold")
    ax.text(label_x, ROW_TGT_TXT + 0.72, "Target / Live evidence",
            ha="right", va="center", fontsize=10, fontweight="bold")
    ax.text(label_x, ROW_TGT_PCT + 0.55, "Technical\nimportance",
            ha="right", va="center", fontsize=10, fontweight="bold")

    # ---------- Title ----------
    fig.suptitle("CampusRide House of Quality (v4.4): Survey Findings → Engineering Characteristics → Implementation Status",
                 fontsize=15, fontweight="bold", y=0.985)
    fig.text(0.5, 0.957,
             "WHATs derived from formative survey findings F1–F6 (N=111 eligible / 44 finished); "
             "HOWs are §5 design features against deployed controllers/services. "
             "Technical importance = Σ(WHAT importance × relationship strength).",
             ha="center", fontsize=10, style="italic", color="#444")

    # ---------- Legend (3 vertical stacked rows below the tech-importance bars) ----------
    legend_label_x = matrix_x0 - 0.20
    legend_left_x = matrix_x0 + 0.2

    # Row 1: Relationship
    legend_y1 = ROW_TGT_PCT - 1.3
    ax.text(legend_label_x, legend_y1, "Relationship:",
            ha="right", va="center", fontsize=10.5, fontweight="bold")
    rel_legend = [("●", "Strong (9)", "#1A5276"), ("◐", "Medium (3)", "#5DADE2"), ("○", "Weak (1)", "white")]
    for k, (sym, lab, fc) in enumerate(rel_legend):
        cx = legend_left_x + k * 2.0
        ax.add_patch(plt.Circle((cx, legend_y1), 0.20, facecolor=fc,
                                edgecolor="#1A5276", lw=1.2, zorder=3))
        if sym == "●":
            ax.text(cx, legend_y1, "●", color="white", ha="center", va="center",
                    fontsize=9, fontweight="bold", zorder=4)
        ax.text(cx + 0.35, legend_y1, lab, ha="left", va="center", fontsize=10)

    # Row 2: Roof correlation
    legend_y2 = legend_y1 - 0.85
    ax.text(legend_label_x, legend_y2, "Roof correlation:",
            ha="right", va="center", fontsize=10.5, fontweight="bold")
    roof_legend_items = [("▲","strong+","#27AE60"), ("△","weak+","#27AE60"),
                         ("▽","weak−","#C0392B"), ("▼","strong−","#C0392B")]
    for k, (sym, lab, c) in enumerate(roof_legend_items):
        cx = legend_left_x + k * 2.0
        ax.text(cx, legend_y2, sym, ha="center", va="center",
                fontsize=13, color=c, fontweight="bold")
        ax.text(cx + 0.30, legend_y2, lab, ha="left", va="center", fontsize=10)

    # Row 3: Status
    legend_y3 = legend_y2 - 0.85
    ax.text(legend_label_x, legend_y3, "Status:",
            ha="right", va="center", fontsize=10.5, fontweight="bold")
    for k, (status, color) in enumerate([("deployed","#2ECC71"), ("specified","#F39C12"), ("pending","#7F8C8D")]):
        cx = legend_left_x + k * 2.5
        ax.add_patch(plt.Rectangle((cx - 0.30, legend_y3 - 0.22), 0.60, 0.44,
                                   facecolor=color, alpha=0.85, edgecolor="black", lw=0.5))
        ax.text(cx + 0.40, legend_y3, status,
                ha="left", va="center", fontsize=10)

    # ---------- Final extents ----------
    x_min = matrix_x0 - 8.4
    x_max = matrix_x0 + n_ec * cell + 0.6
    y_min = legend_y3 - 0.7
    y_max = apex_y + 0.6
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    plt.tight_layout(rect=(0, 0, 1, 0.945))

    pdf = OUT_DIR / "v8_house_of_quality.pdf"
    png = OUT_DIR / "v8_house_of_quality.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {pdf.relative_to(REPO_ROOT)}")
    print(f"Wrote {png.relative_to(REPO_ROOT)}")
    return pdf


if __name__ == "__main__":
    build_hoq()
