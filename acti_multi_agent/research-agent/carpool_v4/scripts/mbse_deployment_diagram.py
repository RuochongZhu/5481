"""mbse_deployment_diagram - UML Deployment Diagram for CampusRide v4.4.

Three primary «device» nodes in a row:
  - Browser/Mobile (left): Vue 3 + Vite SPA (bundle.js artifact)
  - Railway Container (centre): Node.js 18 + Express runtime, 23 controllers
    + 19 services + Socket.IO server artifacts
  - Supabase Cluster (right): Postgres + RLS, 18 core tables, RLS policies,
    RPC functions

Three external sidecar «device» nodes around the cluster:
  - Resend SMTP service
  - WeChat Mini-Program API
  - TCAT bus schedule API (read-only consumer)

Edges are «communication path» links labelled with the protocol
(HTTPS REST + WebSocket; Postgres wire protocol; SMTP via Resend API;
HTTPS REST → wechat-link.service → WeChat).  A footer pins the
2026-04-23 snapshot facts (184 users, 82 wxgroup_notice_record rows,
www.campusgo.college).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import setup_mpl, save_mpl, register, renderer  # noqa: E402


# Palette --------------------------------------------------------------------
DEVICE_FILL = "#FBFCFC"
DEVICE_BORDER = "#1A5276"

EXEC_FILL = "#D6EAF8"
EXEC_BORDER = "#1F618D"

ARTIFACT_FILL = "#FDEBD0"
ARTIFACT_BORDER = "#9C640C"

SIDE_FILL = "#FDEDEC"
SIDE_BORDER = "#922B21"

PATH_COLOR = "#1B2631"
PATH_DASHED = "#7D6608"


@renderer("mbse_deployment_diagram")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    from matplotlib.lines import Line2D

    # Landscape, A4-readable canvas
    fig, ax = plt.subplots(figsize=(18, 11.5))
    ax.set_xlim(0, 36)
    ax.set_ylim(0, 22)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    ax.text(
        18, 21.3,
        "Deployment Diagram - CampusRide v4.4",
        fontsize=16, fontweight="bold", color="#0E2F44",
        ha="center", va="center",
    )
    ax.text(
        18, 20.55,
        "<<device>> nodes,  <<execution environment>>,  artifacts,  "
        "and <<communication path>> protocol bindings",
        fontsize=10.5, color="#566573", style="italic",
        ha="center", va="center",
    )

    # ------------------------------------------------------------------
    # Helper: device, exec env, artifact, sidecar, comm-path
    # ------------------------------------------------------------------
    def device(x, y, w, h, name, *, fill=DEVICE_FILL, border=DEVICE_BORDER,
               stereotype="device", lw=2.0):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.05,rounding_size=0.4",
            linewidth=lw, edgecolor=border,
            facecolor=fill, zorder=2,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2, y + h - 0.45,
            f"<<{stereotype}>>",
            fontsize=9.0, color="#566573", style="italic",
            ha="center", va="center", zorder=4,
        )
        ax.text(
            x + w / 2, y + h - 1.05, name,
            fontsize=12, fontweight="bold", color="#1B2631",
            ha="center", va="center", zorder=4,
        )

    def exec_env(x, y, w, h, name, sub):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.04,rounding_size=0.25",
            linewidth=1.4, edgecolor=EXEC_BORDER,
            facecolor=EXEC_FILL, zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2, y + h - 0.32,
            "<<execution environment>>",
            fontsize=8.2, color="#1F618D", style="italic",
            ha="center", va="center", zorder=4,
        )
        ax.text(
            x + w / 2, y + h - 0.74, name,
            fontsize=10.5, fontweight="bold", color="#1B2631",
            ha="center", va="center", zorder=4,
        )
        if sub:
            ax.text(
                x + w / 2, y + 0.32, sub,
                fontsize=8.2, color="#1B2631", style="italic",
                ha="center", va="center", zorder=4,
            )

    def artifact(x, y, w, h, label):
        # UML artifact: rectangle with a small "page corner" annotation
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            linewidth=1.2, edgecolor=ARTIFACT_BORDER,
            facecolor=ARTIFACT_FILL, zorder=4,
        )
        ax.add_patch(box)
        # tiny "doc" icon top-right (use plain ASCII to avoid font warnings)
        ax.text(
            x + w - 0.18, y + h - 0.20,
            "[doc]",
            fontsize=7.0, color=ARTIFACT_BORDER, fontweight="bold",
            ha="right", va="top", zorder=5,
        )
        ax.text(
            x + 0.20, y + h / 2,
            "<<artifact>>",
            fontsize=7.5, color=ARTIFACT_BORDER, style="italic",
            ha="left", va="bottom", zorder=5,
        )
        ax.text(
            x + 0.20, y + h / 2 - 0.05, label,
            fontsize=8.6, color="#1B2631",
            ha="left", va="top", zorder=5,
        )

    def sidecar(x, y, w, h, name, sub):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.04,rounding_size=0.30",
            linewidth=1.4, edgecolor=SIDE_BORDER,
            facecolor=SIDE_FILL, zorder=2,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2, y + h - 0.36,
            "<<device>>",
            fontsize=8.2, color="#922B21", style="italic",
            ha="center", va="center", zorder=4,
        )
        ax.text(
            x + w / 2, y + h - 0.86, name,
            fontsize=10, fontweight="bold", color="#1B2631",
            ha="center", va="center", zorder=4,
        )
        if sub:
            ax.text(
                x + w / 2, y + 0.32, sub,
                fontsize=8.2, color="#1B2631", style="italic",
                ha="center", va="center", zorder=4,
            )

    def comm_path(p_src, p_dst, label, *, color=PATH_COLOR, style="-",
                  lw=1.6, label_dy=0.0, rad=0.0, label_pos=0.50):
        sx, sy = p_src
        dx, dy = p_dst
        arrow = FancyArrowPatch(
            (sx, sy), (dx, dy),
            arrowstyle="-", mutation_scale=14,
            linewidth=lw, color=color,
            connectionstyle=f"arc3,rad={rad}",
            linestyle=style, zorder=5,
        )
        ax.add_patch(arrow)
        # small open square at each end to suggest «communication path»
        for px, py in [(sx, sy), (dx, dy)]:
            ax.add_patch(
                FancyBboxPatch(
                    (px - 0.10, py - 0.10), 0.20, 0.20,
                    boxstyle="square,pad=0.0",
                    linewidth=1.2, edgecolor=color, facecolor="white",
                    zorder=6,
                )
            )
        lx = sx + (dx - sx) * label_pos
        ly = sy + (dy - sy) * label_pos + label_dy
        ax.text(
            lx, ly,
            f"<<communication path>>\n{label}",
            fontsize=8.4, color=color,
            ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor=color,
                      boxstyle="round,pad=0.20", linewidth=0.8,
                      alpha=0.97),
            zorder=7,
        )

    # ------------------------------------------------------------------
    # Three primary devices (left -> right)
    # ------------------------------------------------------------------
    # 1) Browser / Mobile
    bx, by, bw, bh = 0.8, 7.5, 8.0, 9.0
    device(bx, by, bw, bh, "Browser / Mobile")
    exec_env(bx + 0.5, by + 4.7, bw - 1.0, 2.6,
             "Vue 3 + Vite SPA",
             "client renderer; JWT in localStorage")
    artifact(bx + 0.7, by + 0.9, bw - 1.4, 3.4,
             "bundle.js\n  - vue-router\n  - pinia store\n"
             "  - socket.io-client\n  - components / views")

    # 2) Railway Container
    rx, ry, rw, rh = 13.0, 5.5, 10.0, 11.5
    device(rx, ry, rw, rh, "Railway Container")
    exec_env(rx + 0.5, ry + 7.5, rw - 1.0, 2.8,
             "Node.js 18 + Express",
             "PORT 3001 - app.js")
    artifact(rx + 0.7, ry + 4.2, rw - 1.4, 3.0,
             "23 controllers + 19 services\n"
             "  - carpooling, marketplace,\n    activity, group, message,\n"
             "    notification, points, ...\n"
             "  - notification.service\n  - rideCarpoolGroup.service")
    artifact(rx + 0.7, ry + 0.7, rw - 1.4, 3.2,
             "Socket.IO server\n  - JWT auth middleware\n"
             "  - room namespacing\n    user:{id} / activity:{id} /\n"
             "    thread:{id} / ride:{id}\n"
             "  - Redis adapter (planned)")

    # 3) Supabase Cluster
    sx, sy, sw, sh = 27.0, 5.5, 8.5, 11.5
    device(sx, sy, sw, sh, "Supabase Cluster")
    exec_env(sx + 0.4, sy + 7.5, sw - 0.8, 2.8,
             "Postgres + RLS",
             "project bwimyvkwkenrtumsfjzt")
    artifact(sx + 0.6, sy + 4.2, sw - 1.2, 3.0,
             "18 core tables\n  users, rides, ride_bookings,\n"
             "  ratings, groups, messages,\n  marketplace_items,\n"
             "  activities, notifications,\n  wxgroup_notice_record, ...")
    artifact(sx + 0.6, sy + 0.7, sw - 1.2, 3.2,
             "RLS policies\n+ RPC functions\n"
             "  - increment_user_points\n  - calculate_distance\n"
             "  - is_checkin_period")

    # ------------------------------------------------------------------
    # Three sidecar «device» nodes
    # ------------------------------------------------------------------
    # Resend (top-right of railway)
    rs_x, rs_y, rs_w, rs_h = 14.5, 1.6, 7.5, 2.7
    sidecar(rs_x, rs_y, rs_w, rs_h,
            "Resend SMTP service",
            "transactional verification email\n(@cornell.edu loop)")

    # WeChat (above Supabase)
    wx_x, wx_y, wx_w, wx_h = 27.5, 1.6, 7.5, 2.7
    sidecar(wx_x, wx_y, wx_w, wx_h,
            "WeChat Mini-Program API",
            "outreach link resolution\n(mini-program short-link, H5 fallback)")

    # TCAT (top of canvas, between browser & railway)
    tc_x, tc_y, tc_w, tc_h = 4.8, 18.0, 6.5, 2.4
    sidecar(tc_x, tc_y, tc_w, tc_h,
            "TCAT Bus Schedule API",
            "read-only campus transit reference")

    # ------------------------------------------------------------------
    # Communication paths
    # ------------------------------------------------------------------
    # Browser -> Railway: HTTPS REST + WebSocket
    comm_path(
        (bx + bw, by + bh / 2 + 1.0),
        (rx, ry + rh / 2 + 2.5),
        "HTTPS REST + WebSocket\n(Bearer JWT)",
        color=PATH_COLOR, lw=1.8,
    )

    # Railway -> Supabase: Postgres wire protocol (via @supabase/supabase-js)
    comm_path(
        (rx + rw, ry + rh / 2 + 1.5),
        (sx, sy + sh / 2 + 1.5),
        "Postgres wire / REST\n(supabase-js + RPC)",
        color=PATH_COLOR, lw=1.8,
    )
    # Railway -> Supabase: socket-emit RLS notify channel (extra)
    comm_path(
        (rx + rw, ry + rh / 2 - 1.5),
        (sx, sy + sh / 2 - 1.5),
        "RLS-scoped queries\n(JWT row context)",
        color=PATH_COLOR, lw=1.4, style="--", label_dy=-0.10,
    )

    # Railway -> Resend: SMTP via Resend API (HTTPS)
    comm_path(
        (rx + rw / 2 - 1.0, ry),
        (rs_x + rs_w / 2 - 1.0, rs_y + rs_h),
        "SMTP via\nResend HTTPS API",
        color=PATH_DASHED, lw=1.4,
    )

    # Railway -> WeChat: HTTPS REST through wechat-link.service
    comm_path(
        (rx + rw, ry),
        (wx_x + wx_w / 2 - 0.8, wx_y + wx_h),
        "HTTPS REST\n-> wechat-link.service\n-> WeChat short-link API",
        color=PATH_DASHED, lw=1.4, label_dy=-0.10,
    )

    # Browser -> TCAT: read-only HTTPS GET
    comm_path(
        (bx + bw / 2 + 1.0, by + bh),
        (tc_x + 1.0, tc_y),
        "HTTPS GET\n(read-only schedule)",
        color="#7F8C8D", lw=1.2, style=":",
    )

    # ------------------------------------------------------------------
    # Snapshot footer
    # ------------------------------------------------------------------
    ax.text(
        18, 0.45,
        "Snapshot 2026-04-23  -  184 users (170 verified, 92.4%)  -  "
        "82 wxgroup_notice_record rows (62 mkt / 16 ride / 4 act)  -  "
        "served at www.campusgo.college",
        fontsize=10, fontweight="bold", color="#1A5276",
        ha="center", va="center",
        bbox=dict(facecolor="#EBF5FB", edgecolor="#1A5276",
                  boxstyle="round,pad=0.30", linewidth=1.2),
    )

    # ------------------------------------------------------------------
    # Legend
    # ------------------------------------------------------------------
    legend_handles = [
        mpatches.Patch(facecolor=DEVICE_FILL, edgecolor=DEVICE_BORDER,
                       label="<<device>>  primary node"),
        mpatches.Patch(facecolor=SIDE_FILL, edgecolor=SIDE_BORDER,
                       label="<<device>>  sidecar / external"),
        mpatches.Patch(facecolor=EXEC_FILL, edgecolor=EXEC_BORDER,
                       label="<<execution environment>>"),
        mpatches.Patch(facecolor=ARTIFACT_FILL, edgecolor=ARTIFACT_BORDER,
                       label="<<artifact>>  deployable unit"),
        Line2D([0], [0], color=PATH_COLOR, linewidth=1.8,
               label="<<communication path>>  active"),
        Line2D([0], [0], color=PATH_DASHED, linewidth=1.4, linestyle="--",
               label="<<communication path>>  third-party API"),
        Line2D([0], [0], color="#7F8C8D", linewidth=1.2, linestyle=":",
               label="<<communication path>>  read-only reference"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left", bbox_to_anchor=(0.005, 0.025),
        frameon=True, fontsize=8.6, handlelength=1.6,
        handletextpad=0.6, ncol=1, columnspacing=1.0,
        framealpha=0.95, edgecolor="#566573",
    )

    plt.tight_layout(pad=0.3)

    pdf, png = save_mpl("mbse_deployment_diagram", dpi=300)
    register("mbse_deployment_diagram", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
