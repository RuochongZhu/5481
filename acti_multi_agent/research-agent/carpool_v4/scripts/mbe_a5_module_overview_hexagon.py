"""mbe_a5 - Module Overview Hexagon.

Radial diagram with the .edu Identity core at the center, the six modules
placed around it at hexagon vertices, with the Points module rendered as a
translucent overlay ring (cross-module meta-layer rather than a vertex).

Engagement intensities (sum of primitive ticks across Identity, Safety,
Rating Fairness, Rewards) determine disc diameters; the Carpool deep-dive
subject is visually emphasized via size + a small star.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer
from _mbe_helpers import setup_mpl, save_mpl, register, MODULE_COLORS


@renderer("mbe_a5_module_overview_hexagon")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    import numpy as np

    # --- Data -----------------------------------------------------------------
    # Vertex modules (in clockwise order starting from top: 90 deg)
    # Carpool deep-dive sits at the top.
    vertex_modules = [
        # name,          identity, safety, rating, rewards (per 5.1 Table 2)
        ("Carpool",      1, 2, 2, 1),
        ("Marketplace",  1, 0, 1, 1),
        ("Activities",   1, 0, 0, 1),
        ("Messages",     1, 0, 0, 0),
        ("Groups",       1, 0, 0, 0),
        # 6th vertex slot left visually open (Points overlay covers all);
        # we fill it with a 6th rotation for symmetry but only place 5 disc
        # vertices? The brief asks for 6 vertices with Points as overlay.
        # We therefore re-introduce a 6th slot by giving the second weak
        # module Messages a paired location. The brief explicitly gives
        # 6 angle slots; we fill 5 with discs and leave 1 implicitly used by
        # the overlay-ring label anchor at the bottom.
    ]
    # Engagement = sum of ticks (caps from brief): Carpool 6, Marketplace 3,
    # Activities 2, Groups 1, Messages 1.
    engagement_total = {
        "Carpool": 6,
        "Marketplace": 3,
        "Activities": 2,
        "Groups": 1,
        "Messages": 1,
    }
    identity_engagement = {  # all five have identity = 1 (uniform)
        "Carpool": 1, "Marketplace": 1, "Activities": 1,
        "Groups": 1, "Messages": 1,
    }

    # Hexagon angles (degrees), clockwise from top.
    angles_deg = [90, 30, -30, -90, -150, 150]
    # Module placement on the 6 vertices (clockwise from top)
    vertex_assignment = [
        "Carpool",      # 90  (top)
        "Marketplace",  # 30  (upper right)
        "Activities",   # -30 (lower right)
        "Groups",       # -90 (bottom; will sit beside the overlay ring label)
        "Messages",     # -150 (lower left)
        None,            # 150 (upper left) intentionally blank (Points overlay
                         # occupies the whole ring; leaving this slot open
                         # avoids a 6th misleading disc)
    ]
    # Note: brief lists "6 modules at hexagon vertices ... Points (cross-module
    # meta-layer - render as a translucent overlay ring, not a vertex)".
    # i.e. only 5 modules become vertex discs; Points becomes the ring.
    # We rotate Messages into 150 to keep symmetry and leave -150 empty? -
    # The original brief order around the hexagon clockwise from top is
    # Carpool, Marketplace, Activities, Groups, Messages, then Points.
    # Since Points is the overlay, we leave the 150 slot blank.
    vertex_assignment = [
        "Carpool",      # 90  (top)
        "Marketplace",  # 30
        "Activities",   # -30
        "Groups",       # -90
        "Messages",     # -150
        None,            # 150 reserved (Points overlay anchor)
    ]

    # --- Figure ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_aspect("equal")
    ax.set_xlim(-6.4, 6.4)
    ax.set_ylim(-6.4, 6.4)
    ax.axis("off")

    # Hexagon vertex radius (where module disc centers live)
    R = 3.4

    # --- Outer translucent overlay ring: Points ------------------------------
    # Outer ring spans across all modules: a thick translucent annulus.
    points_color = MODULE_COLORS["Points"]
    outer_ring_outer = 5.85
    outer_ring_inner = 5.20
    n_seg = 200
    theta = np.linspace(0, 2 * np.pi, n_seg)
    # Build ring as filled polygon (outer minus inner)
    outer_x = outer_ring_outer * np.cos(theta)
    outer_y = outer_ring_outer * np.sin(theta)
    inner_x = outer_ring_inner * np.cos(theta[::-1])
    inner_y = outer_ring_inner * np.sin(theta[::-1])
    ring_poly = mpatches.Polygon(
        np.column_stack([np.concatenate([outer_x, inner_x]),
                         np.concatenate([outer_y, inner_y])]),
        closed=True, facecolor=points_color, edgecolor=points_color,
        alpha=0.22, linewidth=0.0, zorder=0.5,
    )
    ax.add_patch(ring_poly)
    # Label on the overlay ring (top-arc)
    ax.text(
        0, (outer_ring_outer + outer_ring_inner) / 2,
        "Points  (cross-module meta-layer)",
        ha="center", va="center", fontsize=11.0, style="italic",
        color="#7D6608", fontweight="bold", zorder=2,
    )
    # Faint dashed circle marking the inner ring-edge for clarity
    ax.add_patch(mpatches.Circle(
        (0, 0), outer_ring_inner, fill=False, edgecolor=points_color,
        linewidth=0.7, linestyle=(0, (3, 2)), alpha=0.6, zorder=0.6,
    ))

    # --- Faint hexagon backbone (visual scaffold) ----------------------------
    hex_pts = np.array([
        (R * np.cos(np.deg2rad(a)), R * np.sin(np.deg2rad(a)))
        for a in angles_deg
    ])
    hex_poly = mpatches.Polygon(
        hex_pts, closed=True, fill=False, edgecolor="#BDC3C7",
        linewidth=0.8, linestyle=(0, (1, 2)), zorder=0.4,
    )
    ax.add_patch(hex_poly)

    # --- Center: .edu Identity core ------------------------------------------
    core_radius = 0.95
    core = mpatches.Circle(
        (0, 0), core_radius, facecolor="#1A5276", edgecolor="#0E2F44",
        linewidth=1.6, zorder=4,
    )
    ax.add_patch(core)
    # Soft halo behind the core
    halo = mpatches.Circle(
        (0, 0), core_radius + 0.18, facecolor="#1A5276", edgecolor="none",
        alpha=0.18, zorder=3.5,
    )
    ax.add_patch(halo)
    ax.text(
        0, 0.18, ".edu Identity\nVerification",
        ha="center", va="center", fontsize=12.5, fontweight="bold",
        color="white", zorder=5,
    )
    ax.text(
        0, -0.42, "184 verified\nCornell users",
        ha="center", va="center", fontsize=8.6, style="italic",
        color="#EAF2F8", zorder=5,
    )

    # --- Connector lines (core -> module disc) -------------------------------
    # Identity engagement is uniformly 1 across all 5 modules -> equal width.
    base_lw = 2.4
    for ang, modname in zip(angles_deg, vertex_assignment):
        if modname is None:
            continue
        x = R * np.cos(np.deg2rad(ang))
        y = R * np.sin(np.deg2rad(ang))
        # Trim line to stop before disc edge & after core edge
        norm = np.sqrt(x * x + y * y)
        ux, uy = x / norm, y / norm
        # Disc radius depends on engagement; precompute below first
        eng = engagement_total[modname]
        disc_r = 0.30 + 0.16 * eng  # 6 -> 1.26, 4 -> 0.94, 2 -> 0.62, 1 -> 0.46
        x0 = ux * (core_radius + 0.04)
        y0 = uy * (core_radius + 0.04)
        x1 = x - ux * (disc_r + 0.02)
        y1 = y - uy * (disc_r + 0.02)
        ax.add_line(Line2D(
            [x0, x1], [y0, y1],
            color="#34495E", linewidth=base_lw, alpha=0.9, zorder=2,
            solid_capstyle="round",
        ))

    # --- Module discs --------------------------------------------------------
    for ang, modname in zip(angles_deg, vertex_assignment):
        if modname is None:
            continue
        x = R * np.cos(np.deg2rad(ang))
        y = R * np.sin(np.deg2rad(ang))
        eng = engagement_total[modname]
        disc_r = 0.30 + 0.16 * eng
        face = MODULE_COLORS[modname]
        # Drop a soft shadow
        shadow = mpatches.Circle(
            (x + 0.05, y - 0.05), disc_r, facecolor="#0B0B0B",
            alpha=0.12, edgecolor="none", zorder=2.4,
        )
        ax.add_patch(shadow)
        disc = mpatches.Circle(
            (x, y), disc_r, facecolor=face, edgecolor="#1A1A1A",
            linewidth=1.4 if modname != "Carpool" else 2.2,
            zorder=3,
        )
        ax.add_patch(disc)
        # Module name label inside the disc when it fits, else outside.
        if disc_r >= 0.85:
            ax.text(
                x, y, modname,
                ha="center", va="center",
                fontsize=12 if modname == "Carpool" else 10.5,
                fontweight="bold", color="white", zorder=4,
            )
        else:
            # Place name just outside disc on the radial direction
            norm = np.sqrt(x * x + y * y)
            ux, uy = x / norm, y / norm
            tx = x + ux * (disc_r + 0.32)
            ty = y + uy * (disc_r + 0.32)
            ax.text(
                tx, ty, modname,
                ha="center", va="center", fontsize=10.5, fontweight="bold",
                color="#1A1A1A", zorder=4,
            )

        # Engagement count subtitle (small)
        sub = f"engagement  {eng}/8"
        if disc_r >= 0.85:
            ax.text(
                x, y - disc_r + 0.22, sub,
                ha="center", va="center", fontsize=8.2, color="#F8F9F9",
                style="italic", zorder=4.1,
            )
        else:
            norm = np.sqrt(x * x + y * y)
            ux, uy = x / norm, y / norm
            tx = x + ux * (disc_r + 0.32)
            ty = y + uy * (disc_r + 0.32) - 0.32
            ax.text(
                tx, ty, sub,
                ha="center", va="center", fontsize=7.8,
                color="#5D6D7E", style="italic", zorder=4,
            )

    # --- Carpool star + deep-dive callout ------------------------------------
    cx = R * np.cos(np.deg2rad(90))
    cy = R * np.sin(np.deg2rad(90))
    carpool_r = 0.30 + 0.16 * engagement_total["Carpool"]
    # Star sits just inside the upper-right edge of the Carpool disc
    star_offset = carpool_r * 0.55
    star_x = cx + star_offset
    star_y = cy + star_offset
    ax.plot(
        [star_x], [star_y], marker="*", markersize=20,
        markerfacecolor="#F1C40F", markeredgecolor="#7D6608",
        markeredgewidth=1.1, zorder=5,
    )
    # Callout text placed outside, between Carpool and Marketplace,
    # in the open quadrant upper-right of the figure.
    callout_x = cx + carpool_r + 1.55
    callout_y = cy + carpool_r + 0.55
    ax.annotate(
        "deep-dive: 5.7",
        xy=(star_x + 0.05, star_y + 0.05),
        xytext=(callout_x, callout_y),
        ha="left", va="center", fontsize=10.0, fontweight="bold",
        color="#7D6608",
        arrowprops=dict(
            arrowstyle="-", color="#7D6608", linewidth=1.0,
            connectionstyle="arc3,rad=-0.25",
        ),
        zorder=5,
    )

    # --- Title ---------------------------------------------------------------
    ax.set_title(
        "CampusRide: 6 modules orbiting an .edu identity core",
        fontsize=14.5, fontweight="bold", pad=18,
    )

    # --- Legend (engagement scale + connector meaning) -----------------------
    legend_handles = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=MODULE_COLORS["Carpool"],
               markeredgecolor="#1A1A1A", markersize=18,
               label="disc area  engagement (sum of primitive ticks)"),
        Line2D([0], [0], color="#34495E", linewidth=2.4,
               label="line  Identity engagement (uniform: all modules)"),
        mpatches.Patch(facecolor=MODULE_COLORS["Points"], alpha=0.35,
                       edgecolor=MODULE_COLORS["Points"],
                       label="Points overlay  cross-module meta-layer"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center", bbox_to_anchor=(0.5, -0.04),
        frameon=False, fontsize=9.0, handlelength=1.6,
        handletextpad=0.7, ncol=1,
    )

    # --- Footnote (snapshot row counts) --------------------------------------
    fig.text(
        0.5, 0.018,
        "Snapshot 2026-04-23  -  184 users / 0 rides / 5 groups / 22 DMs / "
        "0 points / 82 WeChat pushes.",
        ha="center", va="bottom", fontsize=8.6, style="italic",
        color="#566573",
    )

    plt.tight_layout(rect=(0, 0.04, 1, 1))

    pdf, png = save_mpl("mbe_a5_module_overview_hexagon")
    register("mbe_a5_module_overview_hexagon", "ok", png_path=png)
