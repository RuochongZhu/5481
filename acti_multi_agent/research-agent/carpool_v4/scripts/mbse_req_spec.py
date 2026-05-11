"""mbse_req_spec - System requirements specification table.

Twelve concept-level requirements grouped by four design primitives
(Identity, Safety, Rating, Rewards). The table reads as a paper-ready
specification list, not an engineering checklist: statements are in
plain English, sources point to the formative survey findings or
adversarial categories, and priority is graded High / Medium / Low.

Style: per `_mbe_style_guide.md` §1 and §4 (matrix / traceability row).
Navy header, alternating white / light-grey body rows, accent colour
(#F39C12) reserved for the highest-priority category band (Safety).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


PLATFORM_COLOR = "#1A5276"   # navy header band
ACCENT_COLOR = "#F39C12"     # highest-priority category accent
TEXT_COLOR = "#1B2631"
MUTED_COLOR = "#566573"
ROW_LIGHT = "#FFFFFF"
ROW_DARK = "#F4F6F7"
BORDER_COLOR = "#AEB6BF"

# Four design-primitive categories. Each category maps to a soft band
# colour used in the leftmost group label. Safety carries the accent.
CATEGORIES = [
    {
        "name": "Identity",
        "band": "#D6EAF8",
        "stripe": PLATFORM_COLOR,
        "is_accent": False,
    },
    {
        "name": "Safety",
        "band": "#FDEBD0",
        "stripe": ACCENT_COLOR,
        "is_accent": True,
    },
    {
        "name": "Rating",
        "band": "#FCF3CF",
        "stripe": "#9A7D0A",
        "is_accent": False,
    },
    {
        "name": "Rewards",
        "band": "#E8DAEF",
        "stripe": "#6C3483",
        "is_accent": False,
    },
]

# (category, req_id, statement, source, priority)
# Statements are in plain English, no implementation references.
REQS = [
    # ---------- Identity ----------
    ("Identity", "R1.1",
     "Only verified campus members can access ride and activity modules.",
     "Beat 3 - identity primitive", "High"),
    ("Identity", "R1.2",
     "Every profile card shows a verified-campus badge alongside the name.",
     "Beat 5 - rider trust signal", "High"),
    ("Identity", "R1.3",
     "Guests may browse posts read-only without the ability to message.",
     "Beat 7 - sample scoping", "Medium"),

    # ---------- Safety (highest priority category) ----------
    ("Safety", "R2.1",
     "First-message contact requires the receiver to reply before a thread opens.",
     "Beat 5 - cold-DM concern", "High"),
    ("Safety", "R2.2",
     "Trip-bound chat closes automatically one hour after the trip ends.",
     "Beat 6 - trip-bound chat", "High"),
    ("Safety", "R2.3",
     "Check-in is granted only inside the venue radius and time window.",
     "Beat 6 - check-in design", "High"),

    # ---------- Rating ----------
    ("Rating", "R3.1",
     "The rating prompt opens two hours after the trip ends, not in the vehicle.",
     "Beat 5 - F4 rating fairness", "High"),
    ("Rating", "R3.2",
     "Driver and passenger rate each other independently and bidirectionally.",
     "Beat 5 - F4 mutual rating", "High"),
    ("Rating", "R3.3",
     "A user may revise their own rating until the dispute window closes.",
     "Beat 7 - dispute scoping", "Medium"),

    # ---------- Rewards ----------
    ("Rewards", "R4.1",
     "Posting a trip, activity, or item earns campus points on completion.",
     "Beat 6 - rewards loop", "Medium"),
    ("Rewards", "R4.2",
     "Point balance updates atomically so award and redemption never desync.",
     "Beat 6 - rewards integrity", "Medium"),
    ("Rewards", "R4.3",
     "Highest-value redemptions are gated behind a verified-campus badge.",
     "Beat 7 - gamification risk", "Low"),
]

PRIORITY_COLORS = {
    "High":   {"fill": "#F5B7B1", "edge": "#922B21", "text": "#641E16"},
    "Medium": {"fill": "#FAD7A0", "edge": "#9A7D0A", "text": "#7D6608"},
    "Low":    {"fill": "#D5DBDB", "edge": "#566573", "text": "#1B2631"},
}


@renderer("mbse_req_spec")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    # --------------------------------------------------------------
    # Geometry. Coordinate system: x in [0, 1], y in figure units.
    # --------------------------------------------------------------
    headers = ["Req ID", "Statement", "Source", "Priority"]
    # Leftmost group-label strip + 4 data columns. Widths sum to 1.
    group_w = 0.090
    col_widths = [0.075, 0.520, 0.225, 0.090]
    assert abs(group_w + sum(col_widths) - 1.0) < 1e-9

    n_rows = len(REQS)
    fig_w = 14.0
    row_h = 0.62
    header_h = 0.75
    title_h = 1.05
    legend_h = 0.55
    fig_h = title_h + header_h + n_rows * row_h + legend_h + 0.30

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    # Column edges (inside the data area, after the group strip).
    x_edges = [group_w]
    for w in col_widths:
        x_edges.append(x_edges[-1] + w)

    # --------------------------------------------------------------
    # Title + italic subtitle (design intent, one sentence)
    # --------------------------------------------------------------
    title_y = fig_h - 0.32
    ax.text(0.5, title_y,
            "Requirements specification by design primitive",
            ha="center", va="center",
            fontsize=14, fontweight="bold", color=TEXT_COLOR)
    ax.text(0.5, title_y - 0.42,
            "Twelve concept-level requirements grouped by primitive; "
            "Safety carries the highest-priority band by design.",
            ha="center", va="center",
            fontsize=10, style="italic", color=MUTED_COLOR)

    # --------------------------------------------------------------
    # Header row (navy banner)
    # --------------------------------------------------------------
    header_top = fig_h - title_h
    header_bot = header_top - header_h

    # Group-strip header cell (matches navy banner)
    ax.add_patch(mpatches.Rectangle(
        (0, header_bot), 1, header_h,
        facecolor=PLATFORM_COLOR, edgecolor=PLATFORM_COLOR,
        linewidth=0, zorder=2))
    ax.text(group_w / 2, (header_top + header_bot) / 2, "Category",
            ha="center", va="center", fontsize=10.5,
            fontweight="bold", color="white", zorder=3)
    for j, h in enumerate(headers):
        x0, x1 = x_edges[j], x_edges[j + 1]
        ax.text((x0 + x1) / 2, (header_top + header_bot) / 2, h,
                ha="center", va="center", fontsize=10.5,
                fontweight="bold", color="white", zorder=3)
        # Subtle vertical separator between header cells
        ax.plot([x0, x0], [header_bot, header_top],
                color="#5D6D7E", linewidth=0.6, zorder=3)
    ax.plot([group_w, group_w], [header_bot, header_top],
            color="#FFFFFF", linewidth=0.8, alpha=0.4, zorder=3)

    # --------------------------------------------------------------
    # Body rows, grouped by category. We draw category bands first
    # (one per group) and then individual rows on top.
    # --------------------------------------------------------------
    body_top = header_bot
    # Walk categories in declared order.
    row_index = 0
    for cat in CATEGORIES:
        cat_rows = [r for r in REQS if r[0] == cat["name"]]
        if not cat_rows:
            continue
        n = len(cat_rows)
        cat_top = body_top - row_index * row_h
        cat_bot = cat_top - n * row_h

        # Group-label strip (left band, full category height)
        ax.add_patch(mpatches.Rectangle(
            (0, cat_bot), group_w, n * row_h,
            facecolor=cat["band"],
            edgecolor=cat["stripe"], linewidth=1.0,
            zorder=2))
        # Vertical accent stripe on the inner edge
        stripe_w = 0.008
        ax.add_patch(mpatches.Rectangle(
            (group_w - stripe_w, cat_bot), stripe_w, n * row_h,
            facecolor=cat["stripe"], edgecolor="none", zorder=3))
        # Category label, rotated, vertically centred
        ax.text(group_w / 2 - 0.005, (cat_top + cat_bot) / 2,
                cat["name"], ha="center", va="center",
                fontsize=11, fontweight="bold", color=cat["stripe"],
                rotation=90, zorder=4)
        # Optional accent flag on the highest-priority category
        if cat["is_accent"]:
            ax.text(group_w / 2 - 0.005, cat_top - 0.18,
                    "TOP", ha="center", va="center",
                    fontsize=7, fontweight="bold",
                    color=ACCENT_COLOR, zorder=5)

        # Individual rows
        for k, (_, rid, stmt, source, prio) in enumerate(cat_rows):
            y_top = cat_top - k * row_h
            y_bot = y_top - row_h
            y_mid = (y_top + y_bot) / 2

            # Alternating row tint (white / light grey)
            row_bg = ROW_LIGHT if (row_index + k) % 2 == 0 else ROW_DARK
            ax.add_patch(mpatches.Rectangle(
                (group_w, y_bot), 1 - group_w, row_h,
                facecolor=row_bg, edgecolor="none", zorder=1))

            # Req ID (centred, monospace-like)
            cx = (x_edges[0] + x_edges[1]) / 2
            ax.text(cx, y_mid, rid,
                    ha="center", va="center",
                    fontsize=10, fontweight="bold",
                    color=TEXT_COLOR, zorder=4)

            # Statement (left-aligned, wrapped)
            import textwrap
            x0 = x_edges[1] + 0.010
            wrapped = textwrap.fill(stmt, width=72)
            lines = wrapped.split("\n")
            if len(lines) > 2:
                lines = [lines[0], " ".join(lines[1:])]
                if len(lines[1]) > 80:
                    lines[1] = lines[1][:77] + "..."
            ax.text(x0, y_mid, "\n".join(lines),
                    ha="left", va="center",
                    fontsize=9.5, color=TEXT_COLOR, zorder=4,
                    linespacing=1.2)

            # Source (left-aligned, italic muted)
            x0 = x_edges[2] + 0.010
            ax.text(x0, y_mid, source,
                    ha="left", va="center",
                    fontsize=9, style="italic",
                    color=MUTED_COLOR, zorder=4)

            # Priority badge (rounded fill)
            cx = (x_edges[3] + x_edges[4]) / 2
            pc = PRIORITY_COLORS[prio]
            ax.add_patch(mpatches.FancyBboxPatch(
                (cx - 0.034, y_mid - 0.16), 0.068, 0.32,
                boxstyle="round,pad=0.005,rounding_size=0.012",
                facecolor=pc["fill"], edgecolor=pc["edge"],
                linewidth=0.9, zorder=4))
            ax.text(cx, y_mid, prio,
                    ha="center", va="center",
                    fontsize=9, fontweight="bold",
                    color=pc["text"], zorder=5)

            # Row separator (thin)
            ax.plot([group_w, 1], [y_bot, y_bot],
                    color="#E5E8E8", linewidth=0.5, zorder=2)

            # Vertical separators inside body
            for j in range(1, len(col_widths)):
                x = x_edges[j]
                ax.plot([x, x], [y_bot, y_top],
                        color="#E5E8E8", linewidth=0.4, zorder=2)

        # Heavier separator at the end of the category block
        ax.plot([0, 1], [cat_bot, cat_bot],
                color=BORDER_COLOR, linewidth=1.0, zorder=3)
        row_index += n

    body_bot = body_top - n_rows * row_h

    # Outer border around the whole table (header + body)
    ax.add_patch(mpatches.Rectangle(
        (0, body_bot), 1, header_top - body_bot,
        facecolor="none", edgecolor=PLATFORM_COLOR,
        linewidth=1.4, zorder=10))

    # --------------------------------------------------------------
    # Legend strip (priority key)
    # --------------------------------------------------------------
    legend_y = body_bot - 0.30
    ax.text(0.005, legend_y, "Priority key:",
            ha="left", va="center",
            fontsize=9, fontweight="bold", color=TEXT_COLOR)
    x_cursor = 0.090
    for prio in ["High", "Medium", "Low"]:
        pc = PRIORITY_COLORS[prio]
        ax.add_patch(mpatches.FancyBboxPatch(
            (x_cursor, legend_y - 0.11), 0.058, 0.22,
            boxstyle="round,pad=0.004,rounding_size=0.010",
            facecolor=pc["fill"], edgecolor=pc["edge"], linewidth=0.7))
        ax.text(x_cursor + 0.029, legend_y, prio,
                ha="center", va="center",
                fontsize=8, fontweight="bold", color=pc["text"])
        x_cursor += 0.072

    # Accent legend chip
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.330, legend_y - 0.11), 0.018, 0.22,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor=ACCENT_COLOR, edgecolor=ACCENT_COLOR, linewidth=0.6))
    ax.text(0.355, legend_y,
            "Accent marks the top-priority category (Safety).",
            ha="left", va="center",
            fontsize=8.5, style="italic", color=MUTED_COLOR)

    pdf, png = save_mpl("mbse_req_spec", dpi=300)
    register("mbse_req_spec", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
