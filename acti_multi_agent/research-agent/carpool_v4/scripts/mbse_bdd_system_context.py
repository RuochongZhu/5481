"""mbse_bdd_system_context - SysML-style Block Definition Diagram.

Hub-and-spoke layout: center «system» CampusRide v4.4 block, with two
columns of «actor» blocks on the left (human roles) and two columns of
«external system» blocks on the right.  Edge labels describe the
direction of interaction using v4.4 deployment-snapshot facts (§5.10).

Implemented as a matplotlib figure rather than graphviz for tight
control over label placement / spacing on an A4-readable canvas.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import setup_mpl, save_mpl, register  # noqa: E402


# Visual palette
SYSTEM_FILL = "#1A5276"
SYSTEM_BORDER = "#0E2F44"

ACTOR_FILL = "#FDEBD0"      # warm peach
ACTOR_BORDER = "#B9770E"
ACTOR_EDGE = "#7E5109"

EXTSYS_FILL = "#D6EAF8"     # sky blue
EXTSYS_BORDER = "#1F618D"
EXTSYS_EDGE = "#1F618D"

PASSIVE_EDGE = "#7F8C8D"


@renderer("mbse_bdd_system_context")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    from matplotlib.lines import Line2D

    # ------------------------------------------------------------------
    # Canvas (landscape A4-readable)
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 36)
    ax.set_ylim(-1.5, 22)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    ax.text(
        18, 21.2,
        "Figure A: System Context (BDD)  -  CampusRide v4.4",
        fontsize=16, fontweight="bold", color="#0E2F44",
        ha="center", va="center",
    )
    ax.text(
        18, 20.5,
        "boundary, actors, and external systems  -  snapshot 2026-04-23",
        fontsize=10.5, color="#566573", style="italic",
        ha="center", va="center",
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def draw_block(x, y, w, h, stereotype, name, sub, fill, border,
                   font_color="#1A1A1A", lw=1.4, fontsize=11.5):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.04,rounding_size=0.30",
            linewidth=lw, edgecolor=border,
            facecolor=fill, zorder=4,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2, y + h - 0.42,
            f"<<{stereotype}>>",
            fontsize=8.6, color="#566573", style="italic",
            ha="center", va="center", zorder=6,
        )
        ax.text(
            x + w / 2, y + h - 0.96, name,
            fontsize=fontsize, fontweight="bold", color=font_color,
            ha="center", va="center", zorder=6,
        )
        if sub:
            ax.text(
                x + w / 2, y + 0.45, sub,
                fontsize=8.4, color=font_color, style="italic",
                ha="center", va="center", zorder=6,
            )

    def draw_label_arrow(p_src, p_dst, label, color, style="-",
                         lw=1.3, label_pos=0.55, label_dx=0.0,
                         label_dy=0.0, rad=0.0):
        sx, sy = p_src
        dx, dy = p_dst
        arrow = FancyArrowPatch(
            (sx, sy), (dx, dy),
            arrowstyle="-|>", mutation_scale=14,
            linewidth=lw, color=color,
            connectionstyle=f"arc3,rad={rad}",
            linestyle=style, zorder=5,
        )
        ax.add_patch(arrow)
        # Label at fractional position along straight line
        lx = sx + (dx - sx) * label_pos + label_dx
        ly = sy + (dy - sy) * label_pos + label_dy
        ax.text(
            lx, ly, label,
            fontsize=8.4, color=color,
            ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor=color,
                      boxstyle="round,pad=0.18", linewidth=0.7,
                      alpha=0.97),
            zorder=6,
        )

    # ------------------------------------------------------------------
    # Center system block
    # ------------------------------------------------------------------
    sx, sy, sw, sh = 13.5, 8.5, 9.0, 5.0
    sys_box = FancyBboxPatch(
        (sx, sy), sw, sh,
        boxstyle="round,pad=0.05,rounding_size=0.45",
        linewidth=2.6, edgecolor=SYSTEM_BORDER,
        facecolor=SYSTEM_FILL, zorder=4,
    )
    ax.add_patch(sys_box)
    ax.text(
        sx + sw / 2, sy + sh - 0.55, "<<system>>",
        fontsize=11, color="#D6EAF8", style="italic",
        ha="center", va="center", zorder=6,
    )
    ax.text(
        sx + sw / 2, sy + sh - 1.45, "CampusRide v4.4",
        fontsize=20, fontweight="bold", color="white",
        ha="center", va="center", zorder=6,
    )
    ax.text(
        sx + sw / 2, sy + sh - 2.30,
        "identity-verified multi-module\ncampus platform",
        fontsize=10.5, color="#EAF2F8",
        ha="center", va="center", zorder=6,
    )
    ax.text(
        sx + sw / 2, sy + 0.80,
        "6 modules  -  184 verified users  -  www.campusgo.college",
        fontsize=8.8, color="#AED6F1", style="italic",
        ha="center", va="center", zorder=6,
    )

    sys_left = (sx, sy + sh / 2)
    sys_right = (sx + sw, sy + sh / 2)
    sys_top = (sx + sw / 2, sy + sh)
    sys_bot = (sx + sw / 2, sy)

    # ------------------------------------------------------------------
    # Actors (left side) - 5 actors stacked vertically
    # ------------------------------------------------------------------
    actor_w, actor_h = 5.0, 2.4
    actor_x = 0.6
    actor_ys = [17.5, 14.5, 11.5, 8.5, 5.5]  # top to bottom (y is bottom of box)

    actors = [
        ("Riders",
         "passenger-side WTP\n(survey N=111)"),
        ("Drivers",
         "Driver/Both N=19\nF5 fairness asymmetry"),
        ("Activity Organizers",
         "publish events\nwith geo-checkin"),
        ("Marketplace Sellers",
         "list items, set\ncontext_type DM"),
        ("Cornell IT /\n.edu Domain Authority",
         "@cornell.edu\nissuance authority"),
    ]
    actor_centers = []
    for (name, sub), ay in zip(actors, actor_ys):
        draw_block(actor_x, ay, actor_w, actor_h,
                   "actor", name, sub,
                   fill=ACTOR_FILL, border=ACTOR_BORDER,
                   font_color="#1A1A1A", fontsize=11)
        actor_centers.append((actor_x + actor_w, ay + actor_h / 2))

    # Section header for actors
    ax.text(
        actor_x + actor_w / 2, 20.45, "Human actors",
        fontsize=12, fontweight="bold", color=ACTOR_BORDER,
        ha="center", va="center",
    )

    # ------------------------------------------------------------------
    # External systems (right side) - 7 external systems in 2 columns
    # ------------------------------------------------------------------
    ext_w, ext_h = 5.6, 2.2
    # Single column on the far right -- spreads labels along straight arrows
    ext_col_x = [29.0]
    # 7 externals stacked top-to-bottom
    extsys = [
        # (name, sub, col, row_y)
        ("Resend Email API",
         "transactional verification mail", 0, 17.8),
        ("WeChat Mini-Program API",
         "outreach push + H5 fallback", 0, 15.0),
        ("Supabase Postgres + Storage",
         "project bwimyvkwkenrtumsfjzt", 0, 12.2),
        ("Railway Hosting Platform",
         "Express 5.1 + Socket.IO runtime", 0, 9.4),
        ("TCAT Bus Schedule API",
         "campus transit reference", 0, 6.6),
        ("Google Maps Geocoding",
         "address <-> lat/lng resolution", 0, 3.8),
        ("External commercial rideshare\n(Uber / Lyft)",
         "competitor reference (no API)", 0, 1.0),
    ]
    ext_anchors = {}  # name_short -> (left_x, mid_y) for arrows
    for (name, sub, col, row_y) in extsys:
        x0 = ext_col_x[col]
        draw_block(x0, row_y, ext_w, ext_h,
                   "external system", name, sub,
                   fill=EXTSYS_FILL, border=EXTSYS_BORDER,
                   font_color="#1A1A1A", fontsize=10.5)
        ext_anchors[name] = (x0, row_y + ext_h / 2)  # left edge midpoint

    # Section header for externals
    ax.text(
        ext_col_x[0] + ext_w / 2, 20.45,
        "External systems",
        fontsize=12, fontweight="bold", color=EXTSYS_BORDER,
        ha="center", va="center",
    )

    # ------------------------------------------------------------------
    # Edges: actors -> system  (orange)
    # ------------------------------------------------------------------
    actor_edge_specs = [
        # (actor_idx, label, system_anchor_dy_offset, label_offset_y)
        (0, "browse + book rides\nJWT REST + Socket.IO",
         +1.6,  +0.20),
        (1, "publish ride\n(triggers 16 ride WeChat pushes)",
         +0.8,  +0.10),
        (2, "create activity\n(0 rows live)",
         -0.0,  +0.0),
        (3, "list item\n(15 items 'removed')",
         -0.8,  -0.10),
        (4, ".edu identity verification token\n(170/184 verified, 92.4%)",
         -1.6,  -0.20),
    ]
    for idx, label, dy_off, lab_dy in actor_edge_specs:
        src = actor_centers[idx]
        dst = (sx, sy + sh / 2 + dy_off)
        # bend slightly more for top/bottom rows
        rad = -0.10 * (dy_off / 1.6) if dy_off != 0 else 0.0
        # special emphasis for the .edu identity edge
        lw = 1.6 if idx == 4 else 1.2
        draw_label_arrow(src, dst, label, ACTOR_EDGE, lw=lw,
                         label_pos=0.50, label_dy=lab_dy, rad=rad)

    # ------------------------------------------------------------------
    # Edges: system -> external systems  (blue)
    # ------------------------------------------------------------------
    # Externals at midpoint y values (top to bottom): 18.9, 16.1, 13.3, 10.5,
    # 7.7, 4.9, 2.1.  System center y = 11.  We point each system-edge
    # anchor at a slightly different y to spread arrow origins.
    ext_edge_specs = [
        # name, label, system_anchor_y, style, lw, rad
        ("Resend Email API",
         "verification email\nvia Resend",
         12.6, "-", 1.3, +0.0),
        ("WeChat Mini-Program API",
         "WeChat outreach push\n(82: 62 mkt / 16 ride / 4 act)",
         12.0, "-", 1.7, +0.0),
        ("Supabase Postgres + Storage",
         "Supabase JS REST + RPC\nincrement_user_points,\ncalculate_distance",
         11.4, "-", 1.5, +0.0),
        ("Railway Hosting Platform",
         "deployed on Railway",
         10.6, ":", 1.2, +0.0),
        ("TCAT Bus Schedule API",
         "reference (read)\nno production API call",
         10.0, "--", 1.1, +0.0),
        ("Google Maps Geocoding",
         "geocoding (planned)\nride origin/destination",
         9.4, "--", 1.1, +0.0),
        ("External commercial rideshare\n(Uber / Lyft)",
         "positioning reference\n(competitor)",
         8.7, ":", 1.0, +0.0),
    ]
    for name, label, anchor_y, style, lw, rad in ext_edge_specs:
        src = (sx + sw, anchor_y)
        dst = ext_anchors[name]
        color = PASSIVE_EDGE if style == ":" else EXTSYS_EDGE
        draw_label_arrow(src, dst, label, color, style=style, lw=lw,
                         label_pos=0.50, rad=rad)

    # ------------------------------------------------------------------
    # Legend
    # ------------------------------------------------------------------
    legend_handles = [
        mpatches.Patch(facecolor=SYSTEM_FILL, edgecolor=SYSTEM_BORDER,
                       label="«system»  CampusRide boundary"),
        mpatches.Patch(facecolor=ACTOR_FILL, edgecolor=ACTOR_BORDER,
                       label="«actor»  human role"),
        mpatches.Patch(facecolor=EXTSYS_FILL, edgecolor=EXTSYS_BORDER,
                       label="«external system»  third-party service"),
        Line2D([0], [0], color=ACTOR_EDGE, linewidth=1.5,
               label="actor -> system interaction"),
        Line2D([0], [0], color=EXTSYS_EDGE, linewidth=1.5,
               label="system -> external (active)"),
        Line2D([0], [0], color=EXTSYS_EDGE, linewidth=1.2, linestyle="--",
               label="planned / read-only"),
        Line2D([0], [0], color=PASSIVE_EDGE, linewidth=1.0, linestyle=":",
               label="reference / no API call"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center", bbox_to_anchor=(0.5, 0.005),
        frameon=True, fontsize=9.0, handlelength=1.8,
        handletextpad=0.7, ncol=4, columnspacing=1.3,
        framealpha=0.95, edgecolor="#566573",
    )

    plt.tight_layout(pad=0.4)

    pdf, png = save_mpl("mbse_bdd_system_context", dpi=300)
    register("mbse_bdd_system_context", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
