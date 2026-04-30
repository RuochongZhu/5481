"""mbse_req_spec - System requirements specification table.

Twelve "The system shall..." requirements anchored to the HoQ engineering
characteristics (EC1-EC12) and the §5.11-5.15 design decisions DD1-DD5.
Status reflects the 2026-04-23 Railway-backed production snapshot reported
in §5.10:
  - Deployed (green): observed in production schema or controllers
  - Specified (yellow): present in code but not yet provisioned in prod
  - Pending (red): explicitly future work / out of current cohort

Modeled on a SysML / MBSE requirements-spec table.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


# (id, anchor, requirement_text, subsystem, verification_method, status, evidence)
REQS = [
    ("R.1", "EC1", "The system shall verify .edu institutional identity "
                   "before granting access to any module.",
     "Auth", "Test", "Deployed",
     "170/184 verified (92.4%) at 2026-04-23"),
    ("R.2", "EC2", "The system shall maintain bidirectional Socket.IO + "
                   "REST channels secured by JWT.",
     "Substrate", "Test", "Deployed",
     "Express 5.1 + Socket.IO on Railway"),
    ("R.3", "EC3", "The system shall display a verified-Cornell badge on "
                   "every driver and rider profile card.",
     "Carpool", "Inspection", "Deployed",
     "ride/profile cards live in UI"),
    ("R.4", "EC4", "The system shall enforce a 2-hour post-departure "
                   "delay before opening the rating window.",
     "Rating", "Test", "Deployed",
     "RATING_READY_DELAY_MS const"),
    ("R.5", "EC5", "The system shall persist bidirectional ratings keyed "
                   "on (trip_id, rater_id, ratee_id).",
     "Rating", "Test", "Deployed",
     "schema enforced; 0 rows in prod"),
    ("R.6", "EC6", "The system shall recompute users.avg_rating across "
                   "ratings + activity_ratings on each rating UPSERT.",
     "Rating", "Test", "Deployed",
     "RPC recompute_user_rating"),
    ("R.7", "EC7", "The system shall offer update-in-place rating "
                   "revision (with documented dispute-window limitation).",
     "Rating", "Demo", "Deployed",
     "1 row per (trip,rater,ratee)"),
    ("R.8", "EC8", "The system shall auto-create a ride-scoped group "
                   "chat on first booking, expiring departure +1h.",
     "Messaging", "Test", "Deployed",
     "8 rating-reminder + 16 ride pushes"),
    ("R.9", "EC9", "The system shall write to wxgroup_notice_record on "
                   "createRide / marketplace_item / activity creation.",
     "Outreach", "Test", "Deployed",
     "82 rows: 62 mkt / 16 ride / 4 act"),
    ("R.10", "EC10", "The system shall award/deduct points via "
                     "point_transactions atomic with users.points RPC.",
     "Points", "Test", "Specified",
     "point_rules=0; table missing in prod"),
    ("R.11", "EC11", "The system shall implement REPLY_REQUIRED guard on "
                     "cold DMs (HTTP 403 until the recipient replies).",
     "Messaging", "Test", "Deployed",
     "context_type DM gating live"),
    ("R.12", "EC12", "The system shall accept multi-institution domains "
                     "via a configurable .edu whitelist.",
     "Auth", "Test", "Pending",
     "Cornell-only as of 2026-04"),
]

# Subsystem palette (adds visual orientation to the Subsystem column).
SUBSYSTEM_COLORS = {
    "Auth":      "#D6EAF8",
    "Substrate": "#E8DAEF",
    "Carpool":   "#D5F5E3",
    "Rating":    "#FCF3CF",
    "Messaging": "#FADBD8",
    "Outreach":  "#FDEBD0",
    "Points":    "#F4ECF7",
}

STATUS_COLORS = {
    "Deployed":  "#82E0AA",   # green
    "Specified": "#F8C471",   # yellow / amber
    "Pending":   "#F1948A",   # red / coral
}
STATUS_TEXT = {
    "Deployed":  "#1D8348",
    "Specified": "#9C640C",
    "Pending":   "#922B21",
}

VM_COLORS = {
    "Test":       "#5DADE2",
    "Inspection": "#A569BD",
    "Demo":       "#48C9B0",
    "Analysis":   "#F5B041",
}


@renderer("mbse_req_spec")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    headers = ["ID", "EC", "Requirement (\"The system shall...\")",
               "Subsystem", "Verification", "Status", "Evidence / Live trace"]
    # Column widths (relative units, must sum to 1.0 for x in [0,1]).
    col_widths = [0.040, 0.040, 0.435, 0.080, 0.085, 0.090, 0.230]
    assert abs(sum(col_widths) - 1.0) < 1e-9

    n_rows = len(REQS)
    fig_w = 17.0
    row_h = 0.78           # taller rows so 2-line wrapped text fits
    header_h = 0.95
    title_h = 0.95
    fig_h = title_h + header_h + n_rows * row_h + 0.85

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    # Compute x offsets for each column.
    x_edges = [0.0]
    for w in col_widths:
        x_edges.append(x_edges[-1] + w)

    # ----- Title -----
    title_y = fig_h - 0.30
    ax.text(0.5, title_y,
            "Figure: CampusRide v4.4 - Requirements Specification "
            "(R.1-R.12 anchored to HoQ EC1-EC12)",
            ha="center", va="center", fontsize=13.5, fontweight="bold",
            color="#1A1A1A")
    ax.text(0.5, title_y - 0.45,
            "Status reflects the Railway-backed production snapshot of 2026-04-23 "
            "(184 users, 170 verified). Evidence column quotes deployed rows / files.",
            ha="center", va="center", fontsize=9.2, style="italic", color="#566573")

    # ----- Header row -----
    header_y_top = fig_h - title_h
    header_y_bot = header_y_top - header_h
    # Banner background
    ax.add_patch(mpatches.Rectangle(
        (0, header_y_bot), 1, header_h,
        facecolor="#34495E", edgecolor="#1B2631", linewidth=1.0, zorder=2))
    for j, h in enumerate(headers):
        x0 = x_edges[j]
        x1 = x_edges[j + 1]
        ax.text((x0 + x1) / 2, (header_y_top + header_y_bot) / 2, h,
                ha="center", va="center", fontsize=10.5, fontweight="bold",
                color="white", zorder=3)
        # Vertical separator
        if j > 0:
            ax.plot([x0, x0], [header_y_bot, header_y_top],
                    color="#5D6D7E", linewidth=0.6, zorder=3)

    # ----- Body rows -----
    body_top = header_y_bot
    for i, (rid, ec, text, subsys, vm, status, evid) in enumerate(REQS):
        y_top = body_top - i * row_h
        y_bot = y_top - row_h
        y_mid = (y_top + y_bot) / 2

        # Row background tinted by status (very pale)
        row_tint = {
            "Deployed":  "#EAFAF1",
            "Specified": "#FEF9E7",
            "Pending":   "#FDEDEC",
        }[status]
        ax.add_patch(mpatches.Rectangle(
            (0, y_bot), 1, row_h,
            facecolor=row_tint, edgecolor="none", zorder=1))

        # ID column - bold dark
        cx = (x_edges[0] + x_edges[1]) / 2
        ax.text(cx, y_mid, rid, ha="center", va="center",
                fontsize=10.0, fontweight="bold", color="#1A1A1A", zorder=4)

        # EC anchor column - small badge style
        cx = (x_edges[1] + x_edges[2]) / 2
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - 0.014, y_mid - 0.18), 0.028, 0.36,
            boxstyle="round,pad=0.005,rounding_size=0.006",
            facecolor="#D6EAF8", edgecolor="#2874A6", linewidth=0.7,
            zorder=4))
        ax.text(cx, y_mid, ec, ha="center", va="center",
                fontsize=8.4, fontweight="bold", color="#1B4F72", zorder=5)

        # Requirement text (left aligned, padded). Wrap to fit column width.
        import textwrap
        x0 = x_edges[2] + 0.008
        wrapped = textwrap.fill(text, width=80)
        # Limit to 2 lines max for vertical fit
        lines = wrapped.split("\n")
        if len(lines) > 2:
            lines = [lines[0], " ".join(lines[1:])]
            # If second line still too long, truncate with ellipsis
            if len(lines[1]) > 90:
                lines[1] = lines[1][:87] + "..."
        wrapped = "\n".join(lines)
        ax.text(x0, y_mid, wrapped, ha="left", va="center",
                fontsize=9.0, color="#1A1A1A", zorder=4,
                linespacing=1.15)

        # Subsystem chip
        cx = (x_edges[3] + x_edges[4]) / 2
        chip_color = SUBSYSTEM_COLORS.get(subsys, "#ECECEC")
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - 0.034, y_mid - 0.20), 0.068, 0.40,
            boxstyle="round,pad=0.005,rounding_size=0.012",
            facecolor=chip_color, edgecolor="#566573", linewidth=0.6,
            zorder=4))
        ax.text(cx, y_mid, subsys, ha="center", va="center",
                fontsize=8.6, fontweight="bold", color="#1A1A1A", zorder=5)

        # Verification method chip
        cx = (x_edges[4] + x_edges[5]) / 2
        vm_color = VM_COLORS.get(vm, "#BDC3C7")
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - 0.030, y_mid - 0.18), 0.060, 0.36,
            boxstyle="round,pad=0.005,rounding_size=0.010",
            facecolor=vm_color, edgecolor="#34495E", linewidth=0.6,
            alpha=0.85, zorder=4))
        ax.text(cx, y_mid, vm, ha="center", va="center",
                fontsize=8.6, fontweight="bold", color="white", zorder=5)

        # Status badge (filled)
        cx = (x_edges[5] + x_edges[6]) / 2
        st_color = STATUS_COLORS[status]
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - 0.038, y_mid - 0.20), 0.076, 0.40,
            boxstyle="round,pad=0.005,rounding_size=0.014",
            facecolor=st_color, edgecolor=STATUS_TEXT[status],
            linewidth=1.0, zorder=4))
        ax.text(cx, y_mid, status, ha="center", va="center",
                fontsize=9.0, fontweight="bold", color=STATUS_TEXT[status],
                zorder=5)

        # Evidence column
        x0 = x_edges[6] + 0.008
        ax.text(x0, y_mid, evid, ha="left", va="center",
                fontsize=8.4, style="italic", color="#566573", zorder=4)

        # Row separator
        ax.plot([0, 1], [y_bot, y_bot],
                color="#D5DBDB", linewidth=0.5, zorder=2)
        # Vertical separators inside body
        for j in range(1, len(col_widths)):
            x = x_edges[j]
            ax.plot([x, x], [y_bot, y_top],
                    color="#E5E8E8", linewidth=0.4, zorder=2)

    # Outer border
    bottom = body_top - n_rows * row_h
    ax.add_patch(mpatches.Rectangle(
        (0, bottom), 1, header_y_top - bottom,
        facecolor="none", edgecolor="#1B2631", linewidth=1.2, zorder=10))

    # ----- Legend below table -----
    legend_y = bottom - 0.20
    ax.text(0.005, legend_y, "Verification:",
            ha="left", va="center", fontsize=8.8, fontweight="bold",
            color="#1A1A1A")
    x_cursor = 0.078
    for vm, color in VM_COLORS.items():
        ax.add_patch(mpatches.FancyBboxPatch(
            (x_cursor, legend_y - 0.10), 0.040, 0.20,
            boxstyle="round,pad=0.004,rounding_size=0.008",
            facecolor=color, edgecolor="#34495E", linewidth=0.5))
        ax.text(x_cursor + 0.020, legend_y, vm,
                ha="center", va="center", fontsize=7.8,
                fontweight="bold", color="white")
        x_cursor += 0.052

    ax.text(0.385, legend_y, "Status:",
            ha="left", va="center", fontsize=8.8, fontweight="bold",
            color="#1A1A1A")
    x_cursor = 0.435
    for st, color in STATUS_COLORS.items():
        ax.add_patch(mpatches.FancyBboxPatch(
            (x_cursor, legend_y - 0.10), 0.058, 0.20,
            boxstyle="round,pad=0.004,rounding_size=0.012",
            facecolor=color, edgecolor=STATUS_TEXT[st], linewidth=0.8))
        ax.text(x_cursor + 0.029, legend_y, st,
                ha="center", va="center", fontsize=7.8,
                fontweight="bold", color=STATUS_TEXT[st])
        x_cursor += 0.072

    ax.text(0.665, legend_y,
            "EC = Engineering Characteristic anchor (HoQ §5.16). "
            "Subsystem chips colored by service.",
            ha="left", va="center", fontsize=7.8,
            style="italic", color="#566573")

    pdf, png = save_mpl("mbse_req_spec")
    register("mbse_req_spec", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
