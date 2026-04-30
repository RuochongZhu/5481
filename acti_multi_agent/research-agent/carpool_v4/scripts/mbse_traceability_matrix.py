"""mbse_traceability_matrix - Requirements x Subsystem traceability matrix.

Rows: 10 condensed requirements (R.1..R.10) from the requirements spec.
Cols: 8 subsystems
       Auth | Ride-Match | Cost-Split | SOS-Safety | Schedule |
       Comm/Chat | Suggest-Alt | Monitor/Reward
Cells: filled square ("S") where the requirement is **satisfied** by that
       subsystem; "V" where the subsystem **verifies** the requirement.
Right-margin columns: Status (Active=green / Specified=yellow / Pending=red)
                      and Time Target (Immediate / Within seconds / etc).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


# ---- Subsystems (columns) ----
SUBSYSTEMS = [
    "Auth",
    "Ride-Match",
    "Cost-Split",
    "SOS-Safety",
    "Schedule",
    "Comm/Chat",
    "Suggest-Alt",
    "Monitor/Reward",
]

# ---- Requirements (rows). (id, short_label, status, time_target, [satisfy], [verify]) ----
# satisfy/verify use subsystem-name strings.
REQS = [
    ("R.1", ".edu Identity Auth",
     "Active", "Before first session",
     ["Auth"], ["Monitor/Reward"]),
    ("R.2", "Real-time Ride Match",
     "Active", "Within seconds",
     ["Ride-Match", "Auth"], ["Comm/Chat"]),
    ("R.3", "Verified Profile Badge",
     "Active", "Before booking",
     ["Auth", "Ride-Match"], []),
    ("R.4", "2h Rating Window",
     "Active", "Departure +2h",
     ["Schedule"], ["Monitor/Reward"]),
    ("R.5", "Bidirectional Rating Persist",
     "Active", "Departure +2h",
     ["Schedule", "Monitor/Reward"], []),
    ("R.6", "Avg-Rating Recompute",
     "Active", "On rating UPSERT",
     ["Monitor/Reward"], []),
    ("R.7", "Rating Update-in-Place",
     "Active", "Anytime post-rating",
     ["Schedule", "Monitor/Reward"], []),
    ("R.8", "Ride-Scoped Group Chat",
     "Active", "On first booking",
     ["Comm/Chat", "Ride-Match"], ["Auth"]),
    ("R.9", "WeChat Outreach Push",
     "Active", "On createRide",
     ["Comm/Chat", "Suggest-Alt"], []),
    ("R.10", "Cross-Module Points",
     "Specified", "Planned ahead",
     ["Monitor/Reward"], ["Auth", "Schedule"]),
]


STATUS_COLORS = {
    "Active":    "#2ECC71",
    "Specified": "#F39C12",
    "Pending":   "#E74C3C",
}
STATUS_TEXT_COLORS = {
    "Active":    "#0E6655",
    "Specified": "#7E5109",
    "Pending":   "#922B21",
}

CELL_SATISFY_COLOR = "#1A5276"     # dark blue for "S" satisfy cells
CELL_VERIFY_COLOR  = "#A04000"     # burnt orange for "V" verify cells

SUBSYSTEM_COLORS = {
    "Auth":           "#D6EAF8",
    "Ride-Match":     "#D5F5E3",
    "Cost-Split":     "#FCF3CF",
    "SOS-Safety":     "#FADBD8",
    "Schedule":       "#E8DAEF",
    "Comm/Chat":      "#D1F2EB",
    "Suggest-Alt":    "#FAE5D3",
    "Monitor/Reward": "#F5CBA7",
}


@renderer("mbse_traceability_matrix")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    n_subs = len(SUBSYSTEMS)
    n_reqs = len(REQS)

    # Layout (in matrix units; one cell = 1.0)
    LEFT_LABEL_W = 5.6   # row label column (R.x + short label)
    SUB_CELL_W = 1.6     # one subsystem cell width
    STATUS_W = 2.0
    TIME_W = 4.4

    # Total width units
    total_w = LEFT_LABEL_W + n_subs * SUB_CELL_W + STATUS_W + TIME_W
    # Heights
    HEADER_H = 4.5       # rotated subsystem names
    ROW_H = 1.2
    body_h = n_reqs * ROW_H
    title_h = 2.4
    legend_h = 2.6

    fig_w = 16.0
    fig_h = 9.5
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # Use matrix coordinates for the body, padding on top for header,
    # bottom for legend.
    ax.set_xlim(0, total_w)
    ax.set_ylim(0, body_h + HEADER_H + title_h + legend_h)
    ax.invert_yaxis()
    ax.axis("off")

    y_origin_title = 0.0
    y_origin_header = title_h
    y_origin_body = title_h + HEADER_H
    y_origin_legend = y_origin_body + body_h + 0.4

    # ---- Title ----
    ax.text(total_w / 2, y_origin_title + 0.7,
            "Figure: CampusRide v4.4 - Requirements x Subsystem Traceability Matrix",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="#1A1A1A")
    ax.text(total_w / 2, y_origin_title + 1.7,
            "S = subsystem satisfies requirement   |   "
            "V = subsystem verifies requirement   |   "
            "Status reflects 2026-04-23 production snapshot.",
            ha="center", va="center", fontsize=9.5, style="italic",
            color="#566573")

    # ---- Column headers ----
    # Row label header
    ax.add_patch(mpatches.Rectangle(
        (0, y_origin_header), LEFT_LABEL_W, HEADER_H,
        facecolor="#34495E", edgecolor="#1B2631", linewidth=1.0, zorder=2))
    ax.text(LEFT_LABEL_W / 2,
            y_origin_header + HEADER_H - 0.6,
            "Requirement",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color="white", zorder=3)
    ax.text(LEFT_LABEL_W / 2,
            y_origin_header + HEADER_H - 1.5,
            "(R.x label)",
            ha="center", va="center", fontsize=8.5,
            color="#D5DBDB", zorder=3, style="italic")

    # Subsystem headers (rotated 45°)
    for j, sub in enumerate(SUBSYSTEMS):
        x0 = LEFT_LABEL_W + j * SUB_CELL_W
        # header background tinted with subsystem color
        ax.add_patch(mpatches.Rectangle(
            (x0, y_origin_header), SUB_CELL_W, HEADER_H,
            facecolor=SUBSYSTEM_COLORS[sub], edgecolor="#34495E",
            linewidth=0.8, zorder=2))
        ax.text(x0 + SUB_CELL_W / 2,
                y_origin_header + HEADER_H - 0.6,
                sub,
                ha="center", va="bottom", rotation=45, rotation_mode="anchor",
                fontsize=10, fontweight="bold", color="#1A1A1A", zorder=3)

    # Status / Time-target headers
    sx = LEFT_LABEL_W + n_subs * SUB_CELL_W
    ax.add_patch(mpatches.Rectangle(
        (sx, y_origin_header), STATUS_W, HEADER_H,
        facecolor="#34495E", edgecolor="#1B2631", linewidth=1.0, zorder=2))
    ax.text(sx + STATUS_W / 2, y_origin_header + HEADER_H - 1.0, "Status",
            ha="center", va="center", fontsize=10.5, fontweight="bold",
            color="white", zorder=3)

    tx = sx + STATUS_W
    ax.add_patch(mpatches.Rectangle(
        (tx, y_origin_header), TIME_W, HEADER_H,
        facecolor="#34495E", edgecolor="#1B2631", linewidth=1.0, zorder=2))
    ax.text(tx + TIME_W / 2, y_origin_header + HEADER_H - 1.0, "Time Target",
            ha="center", va="center", fontsize=10.5, fontweight="bold",
            color="white", zorder=3)

    # ---- Body ----
    for i, (rid, label, status, ttarget, satisfy, verify) in enumerate(REQS):
        y_top = y_origin_body + i * ROW_H
        y_mid = y_top + ROW_H / 2

        # Alternating zebra stripe
        stripe_color = "#FBFCFC" if i % 2 == 0 else "#F4F6F7"
        ax.add_patch(mpatches.Rectangle(
            (0, y_top), total_w, ROW_H,
            facecolor=stripe_color, edgecolor="none", zorder=1))

        # Row label
        ax.text(0.30, y_mid, rid,
                ha="left", va="center", fontsize=10, fontweight="bold",
                color="#1A1A1A", zorder=4)
        ax.text(1.05, y_mid, label,
                ha="left", va="center", fontsize=9.6,
                color="#1A1A1A", zorder=4)

        # Subsystem cells
        for j, sub in enumerate(SUBSYSTEMS):
            x0 = LEFT_LABEL_W + j * SUB_CELL_W
            # Cell border
            ax.add_patch(mpatches.Rectangle(
                (x0, y_top), SUB_CELL_W, ROW_H,
                facecolor="white", edgecolor="#D5DBDB", linewidth=0.5,
                zorder=2))

            cx = x0 + SUB_CELL_W / 2
            cy = y_mid

            if sub in satisfy:
                # Filled square with "S"
                square_size = 0.78
                ax.add_patch(mpatches.FancyBboxPatch(
                    (cx - square_size / 2, cy - square_size / 2),
                    square_size, square_size,
                    boxstyle="round,pad=0.01,rounding_size=0.10",
                    facecolor=CELL_SATISFY_COLOR,
                    edgecolor="#0E2F44", linewidth=0.8, zorder=4))
                ax.text(cx, cy, "S",
                        ha="center", va="center",
                        fontsize=10, fontweight="bold",
                        color="white", zorder=5)
            elif sub in verify:
                # Hollow square with "V"
                square_size = 0.78
                ax.add_patch(mpatches.FancyBboxPatch(
                    (cx - square_size / 2, cy - square_size / 2),
                    square_size, square_size,
                    boxstyle="round,pad=0.01,rounding_size=0.10",
                    facecolor="white",
                    edgecolor=CELL_VERIFY_COLOR, linewidth=1.4, zorder=4))
                ax.text(cx, cy, "V",
                        ha="center", va="center",
                        fontsize=10, fontweight="bold",
                        color=CELL_VERIFY_COLOR, zorder=5)

        # Status badge
        sx = LEFT_LABEL_W + n_subs * SUB_CELL_W
        ax.add_patch(mpatches.Rectangle(
            (sx, y_top), STATUS_W, ROW_H,
            facecolor="white", edgecolor="#D5DBDB", linewidth=0.5, zorder=2))
        st_color = STATUS_COLORS.get(status, "#BDC3C7")
        st_text = STATUS_TEXT_COLORS.get(status, "#1A1A1A")
        bw, bh = STATUS_W - 0.50, ROW_H - 0.30
        ax.add_patch(mpatches.FancyBboxPatch(
            (sx + 0.25, y_top + 0.15), bw, bh,
            boxstyle="round,pad=0.01,rounding_size=0.20",
            facecolor=st_color, edgecolor=st_text, linewidth=1.0,
            alpha=0.92, zorder=4))
        ax.text(sx + STATUS_W / 2, y_mid, status,
                ha="center", va="center", fontsize=9.5, fontweight="bold",
                color=st_text, zorder=5)

        # Time target
        tx = sx + STATUS_W
        ax.add_patch(mpatches.Rectangle(
            (tx, y_top), TIME_W, ROW_H,
            facecolor="white", edgecolor="#D5DBDB", linewidth=0.5, zorder=2))
        ax.text(tx + 0.25, y_mid, ttarget,
                ha="left", va="center", fontsize=9.5,
                color="#1A1A1A", zorder=4)

    # ---- Outer frame ----
    ax.add_patch(mpatches.Rectangle(
        (0, y_origin_header), total_w, HEADER_H + body_h,
        facecolor="none", edgecolor="#1B2631", linewidth=1.4, zorder=10))

    # Vertical separator between row-label and subsystem columns
    ax.plot([LEFT_LABEL_W, LEFT_LABEL_W],
            [y_origin_header, y_origin_body + body_h],
            color="#1B2631", linewidth=1.0, zorder=11)
    ax.plot([LEFT_LABEL_W + n_subs * SUB_CELL_W,
             LEFT_LABEL_W + n_subs * SUB_CELL_W],
            [y_origin_header, y_origin_body + body_h],
            color="#1B2631", linewidth=1.0, zorder=11)
    ax.plot([LEFT_LABEL_W + n_subs * SUB_CELL_W + STATUS_W,
             LEFT_LABEL_W + n_subs * SUB_CELL_W + STATUS_W],
            [y_origin_header, y_origin_body + body_h],
            color="#1B2631", linewidth=1.0, zorder=11)
    # Horizontal separator under header
    ax.plot([0, total_w], [y_origin_body, y_origin_body],
            color="#1B2631", linewidth=1.0, zorder=11)

    # ---- Legend ----
    ly = y_origin_legend + 0.6
    ax.text(0.3, ly, "Legend:",
            ha="left", va="center", fontsize=10, fontweight="bold",
            color="#1A1A1A")

    # Satisfy
    cur_x = 2.0
    sq = 0.6
    ax.add_patch(mpatches.FancyBboxPatch(
        (cur_x, ly - sq / 2), sq, sq,
        boxstyle="round,pad=0.005,rounding_size=0.08",
        facecolor=CELL_SATISFY_COLOR, edgecolor="#0E2F44", linewidth=0.8))
    ax.text(cur_x + sq / 2, ly, "S",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color="white")
    ax.text(cur_x + sq + 0.3, ly,
            "Satisfy (subsystem implements requirement)",
            ha="left", va="center", fontsize=9, color="#1A1A1A")

    # Verify
    cur_x = 8.5
    ax.add_patch(mpatches.FancyBboxPatch(
        (cur_x, ly - sq / 2), sq, sq,
        boxstyle="round,pad=0.005,rounding_size=0.08",
        facecolor="white", edgecolor=CELL_VERIFY_COLOR, linewidth=1.4))
    ax.text(cur_x + sq / 2, ly, "V",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=CELL_VERIFY_COLOR)
    ax.text(cur_x + sq + 0.3, ly,
            "Verify (subsystem checks / observes requirement)",
            ha="left", va="center", fontsize=9, color="#1A1A1A")

    # Status legend
    ly2 = ly + 1.0
    ax.text(0.3, ly2, "Status:",
            ha="left", va="center", fontsize=10, fontweight="bold",
            color="#1A1A1A")
    cur_x = 2.0
    for st, color in STATUS_COLORS.items():
        bw, bh = 1.4, 0.55
        ax.add_patch(mpatches.FancyBboxPatch(
            (cur_x, ly2 - bh / 2), bw, bh,
            boxstyle="round,pad=0.005,rounding_size=0.12",
            facecolor=color, edgecolor=STATUS_TEXT_COLORS[st], linewidth=0.8,
            alpha=0.92))
        ax.text(cur_x + bw / 2, ly2, st,
                ha="center", va="center", fontsize=8.5, fontweight="bold",
                color=STATUS_TEXT_COLORS[st])
        cur_x += bw + 0.5

    pdf, png = save_mpl("mbse_traceability_matrix")
    register("mbse_traceability_matrix", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
