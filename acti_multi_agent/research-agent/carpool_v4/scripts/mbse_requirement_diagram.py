"""mbse_requirement_diagram - SysML Requirement Diagram (3-column swimlane).

Three-column "swim" layout with explicit matplotlib positioning so the
12 requirement blocks sit on a clean 4-column x 3-row grid in the centre,
F-findings stack on the left, and the right side is split into a
Subsystems half (top) and TestCases half (bottom).

Edge type / style discipline (chosen to keep the four arrow types
visually distinct even when their paths cross):

  derive   : F-finding -> Requirement      dashed,  ACCENT_DERIVE   orange
                                          routed via a stepped path
                                          (horizontal then vertical).
  refine   : Requirement -> Requirement    solid,   ACCENT_REFINE   grey
                                          short bezier rad=-0.25 inside
                                          the centre band.
  satisfy  : Subsystem -> Requirement      solid,   ACCENT_SATISFY  navy
                                          straight line, arrow tip on R.
  verify   : TestCase -> Requirement       dotted,  ACCENT_VERIFY   green
                                          straight line, arrow tip on R.

Density discipline (so the centre stays readable):
  - One derive edge per F-finding -> the *primary* R it motivates.
  - One satisfy edge per subsystem -> its anchor R.
  - One verify edge per TP test -> its anchor R.
  - Refine edges are kept to four (one per primitive at most).

The 12 requirements R.1..R.12 are the canonical concept-level set from
`mbse_req_spec.py`, relabelled R.1..R.12 here for compactness; the
Identity / Safety / Rating / Rewards primitive is preserved as a coloured
column header strip inside the centre band.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import (  # noqa: E402
    setup_mpl, save_mpl, register, renderer,
)


# ---------------------------------------------------------------------------
# Palette - one colour per relationship type so the four arrow types stay
# visually distinct even when they cross.
# ---------------------------------------------------------------------------
NAVY = "#1A5276"
TEXT = "#1B2631"
GREY_MUTED = "#7B7D7D"

ACCENT_DERIVE = "#D35400"   # F -> R         derive   (dashed orange)
ACCENT_REFINE = "#566573"   # R -> R         refine   (solid grey)
ACCENT_SATISFY = "#1F618D"  # Subsystem -> R satisfy  (solid navy)
ACCENT_VERIFY = "#1E8449"   # TP -> R        verify   (dotted green)

PRIMITIVE = {
    "Identity": {"fill": "#D6EAF8", "border": "#1F618D"},
    "Safety":   {"fill": "#FDEBD0", "border": "#B9770E"},  # priority band
    "Rating":   {"fill": "#FCF3CF", "border": "#9A7D0A"},
    "Rewards":  {"fill": "#E8DAEF", "border": "#6C3483"},
}

# 12 requirements: R.1..R.12, grouped by primitive (3 each, 4 columns).
# Each entry: (rid, primitive, short_text)
REQS = [
    ("R.1",  "Identity", "Verified-only access\nto ride and activity\nmodules"),
    ("R.2",  "Identity", "Verified-campus badge\non every profile card"),
    ("R.3",  "Identity", "Guest read-only\nbrowsing (no messaging)"),
    ("R.4",  "Safety",   "First-message gating\n(reply required)"),
    ("R.5",  "Safety",   "Trip-bound chat closes\n1 h after trip"),
    ("R.6",  "Safety",   "Geo-fenced check-in\nwithin venue radius"),
    ("R.7",  "Rating",   "Rating prompt opens\n2 h after trip"),
    ("R.8",  "Rating",   "Bidirectional independent\ndriver/rider rating"),
    ("R.9",  "Rating",   "Revisable rating until\ndispute window closes"),
    ("R.10", "Rewards",  "Points awarded on\ntrip/activity completion"),
    ("R.11", "Rewards",  "Atomic balance updates\n(award and redemption)"),
    ("R.12", "Rewards",  "Top redemptions gated\nby verified badge"),
]

# F-findings (left swim column). Each derives ONE primary R.
# (fid, label, primary_r)
FINDINGS = [
    ("F1", "Trip gap on\nsmall-town\ncampuses",     "R.1"),
    ("F2", "Trust hinges on\n.edu-scoped\nidentity", "R.2"),
    ("F3", "Safety is the\ndominant WTP\ndriver",   "R.5"),
    ("F4", "Rating fairness\nis the top\nfriction", "R.7"),
    ("F5", "Driver subset\nasks for rating\nappeals", "R.9"),
    ("F6", "Long-distance\nsupply needs\nincentives", "R.10"),
]

# Subsystem blocks (right-top swim column). Each satisfies ONE anchor R.
# (sid, label, anchor_r)
SUBSYSTEMS = [
    ("S1", "Identity Service\n(.edu verifier)",    "R.1"),
    ("S2", "Profile Service\n(badge tile)",        "R.2"),
    ("S3", "Messaging Service\n(cold-DM gate)",    "R.4"),
    ("S4", "Carpool Service\n(trip-bound chat)",   "R.5"),
    ("S5", "Geo Service\n(check-in radius)",       "R.6"),
    ("S6", "Rating Service\n(2 h delay queue)",    "R.7"),
    ("S7", "Points Ledger\n(atomic balance)",      "R.11"),
]

# TP test boxes (right-bottom swim column). Each verifies ONE anchor R.
# (tid, label, anchor_r)
TPS = [
    ("TP1", "Verified-only\naccess test",       "R.1"),
    ("TP2", "Cold-DM gating\nE2E test",          "R.4"),
    ("TP3", "Trip-chat\nexpiry test",            "R.5"),
    ("TP4", "Check-in\nradius test",             "R.6"),
    ("TP5", "Rating-window\ntiming test",        "R.7"),
    ("TP6", "Bidirectional\nrating test",        "R.8"),
    ("TP7", "Points ledger\natomicity test",     "R.11"),
    ("TP8", "Verified-gate\nredemption test",    "R.12"),
]

# Refine relationships (solid grey, sparse).  R.x refines R.y when R.x is
# a specialisation of R.y inside the same primitive.
REFINES = [
    ("R.2", "R.1"),
    ("R.5", "R.4"),
    ("R.9", "R.8"),
    ("R.12", "R.10"),
]


@renderer("mbse_requirement_diagram")
def render():
    setup_mpl()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch

    fig, ax = plt.subplots(figsize=(20.0, 14.0))
    X_MIN, X_MAX = 0.0, 22.0
    Y_MIN, Y_MAX = 0.0, 16.0
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_aspect("auto")
    ax.axis("off")

    # ------------------------------------------------------------------
    # Title + subtitle
    # ------------------------------------------------------------------
    ax.set_title(
        "Requirement diagram - identity-verified campus carpool platform",
        fontsize=15, fontweight="bold", pad=12,
    )
    ax.text(
        (X_MIN + X_MAX) / 2, 15.55,
        "F-findings (left) derive 12 requirements R.1..R.12 (centre); "
        "subsystems satisfy and TP test cases verify (right).",
        ha="center", va="center", fontsize=11, style="italic",
        color=GREY_MUTED,
    )

    # ------------------------------------------------------------------
    # Swim-column band backgrounds (very faint), drawn first so they sit
    # behind everything else.  The three bands tell the reader at a glance
    # which zone they are in.
    # ------------------------------------------------------------------
    LEFT_BAND  = (0.40,  4.20,  0.40, 14.20)   # x, w, y, h
    MID_BAND   = (5.00, 11.20,  0.40, 14.20)
    RIGHT_BAND = (16.50, 5.20,  0.40, 14.20)

    for (x, w, y, h, fc, ec) in [
        (*LEFT_BAND,  "#FEF5E7", ACCENT_DERIVE),
        (*MID_BAND,   "#FBFCFC", NAVY),
        (*RIGHT_BAND, "#F4FBF7", ACCENT_VERIFY),
    ]:
        ax.add_patch(Rectangle(
            (x, y), w, h,
            facecolor=fc, edgecolor=ec, linewidth=1.3,
            alpha=0.55, zorder=0,
        ))

    # Band titles
    ax.text(LEFT_BAND[0] + LEFT_BAND[1] / 2, LEFT_BAND[2] + LEFT_BAND[3] - 0.30,
            "Formative-survey findings",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=ACCENT_DERIVE, zorder=1)
    ax.text(MID_BAND[0] + MID_BAND[1] / 2, MID_BAND[2] + MID_BAND[3] - 0.30,
            "Requirements (4 primitives x 3 rows)",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=NAVY, zorder=1)
    ax.text(RIGHT_BAND[0] + RIGHT_BAND[1] / 2,
            RIGHT_BAND[2] + RIGHT_BAND[3] - 0.30,
            "Subsystems (top)  -  Test cases (bottom)",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=ACCENT_SATISFY, zorder=1)

    # Visual divider between subsystems half and TP half on the right band.
    DIVIDER_Y = RIGHT_BAND[2] + 6.30
    ax.plot(
        [RIGHT_BAND[0] + 0.20, RIGHT_BAND[0] + RIGHT_BAND[1] - 0.20],
        [DIVIDER_Y, DIVIDER_Y],
        color=GREY_MUTED, linewidth=0.8, linestyle=(0, (4, 3)),
        zorder=1,
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def card(cx, cy, w, h, body_text, *, header=None, header_color=NAVY,
             edge_color=NAVY, fc="white", body_fs=9.0, header_fs=10.0):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=fc, edgecolor=edge_color, linewidth=1.3,
            zorder=3,
        ))
        if header:
            ax.text(cx, cy + h / 2 - 0.30, header,
                    ha="center", va="center",
                    fontsize=header_fs, fontweight="bold",
                    color=header_color, zorder=4)
            ax.text(cx, cy - 0.18, body_text,
                    ha="center", va="center",
                    fontsize=body_fs, color=TEXT, zorder=4)
        else:
            ax.text(cx, cy, body_text,
                    ha="center", va="center",
                    fontsize=body_fs, color=TEXT, zorder=4)
        return dict(
            cx=cx, cy=cy, w=w, h=h,
            top=(cx, cy + h / 2), bottom=(cx, cy - h / 2),
            left=(cx - w / 2, cy), right=(cx + w / 2, cy),
        )

    # ------------------------------------------------------------------
    # CENTRE: 12 requirement blocks on a 4 x 3 grid.
    # We compute exact x positions per primitive column and y positions
    # per row so the grid is perfectly aligned.
    # ------------------------------------------------------------------
    centre_x0 = MID_BAND[0] + 0.55
    centre_x1 = MID_BAND[0] + MID_BAND[1] - 0.55
    n_cols = 4
    col_w = (centre_x1 - centre_x0) / n_cols
    col_centres = [centre_x0 + col_w * (i + 0.5) for i in range(n_cols)]

    row_top_y = MID_BAND[2] + MID_BAND[3] - 2.30   # leave room for column header
    row_gap = 3.65
    row_centres = [row_top_y - row_gap * i for i in range(3)]

    # Column-primitive header strips
    primitive_order = ["Identity", "Safety", "Rating", "Rewards"]
    for i, prim in enumerate(primitive_order):
        p = PRIMITIVE[prim]
        cx = col_centres[i]
        ax.add_patch(FancyBboxPatch(
            (cx - col_w / 2 + 0.10, row_top_y + 0.85),
            col_w - 0.20, 0.55,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=p["fill"], edgecolor=p["border"], linewidth=1.2,
            zorder=2,
        ))
        ax.text(cx, row_top_y + 1.13, prim,
                ha="center", va="center",
                fontsize=11, fontweight="bold",
                color=p["border"], zorder=3)

    # Place the 12 R cards.
    REQ_W = col_w - 0.45
    REQ_H = 2.35

    r_anchors: dict[str, dict] = {}
    for rid, prim, text in REQS:
        col_idx = primitive_order.index(prim)
        # Row index within primitive: 0, 1, 2 in order of appearance.
        peers = [r for r in REQS if r[1] == prim]
        row_idx = peers.index((rid, prim, text))
        cx = col_centres[col_idx]
        cy = row_centres[row_idx]
        p = PRIMITIVE[prim]
        r_anchors[rid] = card(
            cx, cy, REQ_W, REQ_H,
            text,
            header=f"«requirement» {rid}",
            header_color=p["border"],
            edge_color=p["border"],
            fc="white",
            body_fs=8.8,
            header_fs=10.0,
        )

    # ------------------------------------------------------------------
    # LEFT: F-findings, vertically stacked, single column.
    # ------------------------------------------------------------------
    f_x = LEFT_BAND[0] + LEFT_BAND[1] / 2
    f_w = LEFT_BAND[1] - 0.80
    f_h = 1.75
    n_findings = len(FINDINGS)
    # Distribute findings between y_top and y_bot of the band.
    f_y_top = LEFT_BAND[2] + LEFT_BAND[3] - 1.50
    f_y_bot = LEFT_BAND[2] + 1.00
    f_step = (f_y_top - f_y_bot) / (n_findings - 1)
    f_anchors: dict[str, dict] = {}
    for i, (fid, text, _) in enumerate(FINDINGS):
        cy = f_y_top - f_step * i
        f_anchors[fid] = card(
            f_x, cy, f_w, f_h,
            text,
            header=fid,
            header_color=ACCENT_DERIVE,
            edge_color=ACCENT_DERIVE,
            fc="white",
            body_fs=8.5,
            header_fs=11.0,
        )

    # ------------------------------------------------------------------
    # RIGHT: subsystems on top, TP test cases on bottom.
    # ------------------------------------------------------------------
    s_x = RIGHT_BAND[0] + RIGHT_BAND[1] / 2
    s_w = RIGHT_BAND[1] - 0.80
    s_h = 1.05

    # Top half: 7 subsystems between sub-band-top and the divider.
    s_y_top = RIGHT_BAND[2] + RIGHT_BAND[3] - 1.40
    s_y_bot = DIVIDER_Y + 0.65
    n_sub = len(SUBSYSTEMS)
    s_step = (s_y_top - s_y_bot) / (n_sub - 1)
    s_anchors: dict[str, dict] = {}
    for i, (sid, text, _) in enumerate(SUBSYSTEMS):
        cy = s_y_top - s_step * i
        s_anchors[sid] = card(
            s_x, cy, s_w, s_h,
            text,
            header=f"«subsystem» {sid}",
            header_color=ACCENT_SATISFY,
            edge_color=ACCENT_SATISFY,
            fc="white",
            body_fs=8.0,
            header_fs=9.0,
        )

    # Bottom half: 8 TP test cases between divider and band bottom.
    t_y_top = DIVIDER_Y - 0.65
    t_y_bot = RIGHT_BAND[2] + 0.70
    n_tp = len(TPS)
    t_step = (t_y_top - t_y_bot) / (n_tp - 1)
    t_anchors: dict[str, dict] = {}
    for i, (tid, text, _) in enumerate(TPS):
        cy = t_y_top - t_step * i
        t_anchors[tid] = card(
            s_x, cy, s_w, s_h,
            text,
            header=f"«testCase» {tid}",
            header_color=ACCENT_VERIFY,
            edge_color=ACCENT_VERIFY,
            fc="white",
            body_fs=8.0,
            header_fs=9.0,
        )

    # ------------------------------------------------------------------
    # Edges - one routing style per relationship type so they stay
    # visually distinct even when they cross.
    # ------------------------------------------------------------------

    def stepped_edge(p_src, p_dst, color, *, ls, lw, label,
                     waypoint_x=None, label_pos="mid", label_fs=8):
        """Stepped (orthogonal) path: horizontal -> vertical -> horizontal.

        waypoint_x: the vertical-segment x. Defaults to midpoint.
        """
        x0, y0 = p_src
        x1, y1 = p_dst
        if waypoint_x is None:
            waypoint_x = (x0 + x1) / 2
        verts = [(x0, y0), (waypoint_x, y0), (waypoint_x, y1), (x1, y1)]
        codes = [MPath.MOVETO, MPath.LINETO, MPath.LINETO, MPath.LINETO]
        path = MPath(verts, codes)
        ax.add_patch(PathPatch(
            path, facecolor="none", edgecolor=color,
            linewidth=lw, linestyle=ls, zorder=2, capstyle="round",
            joinstyle="round",
        ))
        # Arrow head as a tiny triangle just before the destination.
        ax.add_patch(FancyArrowPatch(
            (waypoint_x, y1), (x1, y1),
            arrowstyle="-|>", color=color, linewidth=lw,
            mutation_scale=11, zorder=2,
        ))
        # Label placement
        if label_pos == "mid":
            lx = waypoint_x
            ly = (y0 + y1) / 2
        elif label_pos == "src":
            lx = (x0 + waypoint_x) / 2
            ly = y0 + 0.18
        else:  # dst
            lx = (waypoint_x + x1) / 2
            ly = y1 + 0.18
        ax.text(lx, ly, label,
                ha="center", va="center",
                fontsize=label_fs, color=color, style="italic",
                bbox=dict(facecolor="white", edgecolor="none",
                          pad=1.2, alpha=0.9),
                zorder=4)

    def straight_edge(p_src, p_dst, color, *, ls, lw, label, label_fs=8):
        ax.add_patch(FancyArrowPatch(
            p_src, p_dst,
            arrowstyle="-|>", color=color,
            linewidth=lw, linestyle=ls,
            mutation_scale=11,
            connectionstyle="arc3,rad=0",
            zorder=2,
        ))
        lx = (p_src[0] + p_dst[0]) / 2
        ly = (p_src[1] + p_dst[1]) / 2 + 0.10
        ax.text(lx, ly, label,
                ha="center", va="center",
                fontsize=label_fs, color=color, style="italic",
                bbox=dict(facecolor="white", edgecolor="none",
                          pad=1.2, alpha=0.85),
                zorder=4)

    def bezier_edge(p_src, p_dst, color, *, ls, lw, label, rad=-0.25,
                    label_fs=8):
        ax.add_patch(FancyArrowPatch(
            p_src, p_dst,
            arrowstyle="-|>", color=color,
            linewidth=lw, linestyle=ls,
            mutation_scale=10,
            connectionstyle=f"arc3,rad={rad}",
            zorder=2,
        ))
        lx = (p_src[0] + p_dst[0]) / 2
        ly = (p_src[1] + p_dst[1]) / 2 + (0.40 if rad > 0 else -0.40)
        ax.text(lx, ly, label,
                ha="center", va="center",
                fontsize=label_fs, color=color, style="italic",
                bbox=dict(facecolor="white", edgecolor="none",
                          pad=1.2, alpha=0.85),
                zorder=4)

    # derive : F -> R (stepped, dashed orange).  Find a waypoint between
    # the F band and the R column to keep parallel runs visible.
    derive_waypoint_x = LEFT_BAND[0] + LEFT_BAND[1] + 0.35
    for fid, _t, primary_r in FINDINGS:
        f = f_anchors[fid]
        r = r_anchors[primary_r]
        stepped_edge(
            f["right"], r["left"],
            ACCENT_DERIVE,
            ls=(0, (5, 3)), lw=1.4,
            label="«derive»",
            waypoint_x=derive_waypoint_x,
            label_pos="src",
            label_fs=8.0,
        )

    # satisfy : Subsystem -> R (straight, solid navy).  Subsystems sit on
    # the right band; their straight horizontal-ish line travels left to
    # the R block they realise.
    for sid, _t, anchor_r in SUBSYSTEMS:
        s = s_anchors[sid]
        r = r_anchors[anchor_r]
        straight_edge(
            s["left"], r["right"],
            ACCENT_SATISFY,
            ls="-", lw=1.3,
            label="«satisfy»",
            label_fs=8.0,
        )

    # verify : TP -> R (straight, dotted green)
    for tid, _t, anchor_r in TPS:
        t = t_anchors[tid]
        r = r_anchors[anchor_r]
        straight_edge(
            t["left"], r["right"],
            ACCENT_VERIFY,
            ls=(0, (1, 2)), lw=1.5,
            label="«verify»",
            label_fs=8.0,
        )

    # refine : R -> R (bezier, solid grey, internal to centre band).
    # rad=-0.30 lifts the arc above the row baseline so it doesn't sit
    # on top of the satisfy/verify horizontals.
    for src_id, dst_id in REFINES:
        src = r_anchors[src_id]
        dst = r_anchors[dst_id]
        # Use top edges so the arc sits in the gap between rows.
        bezier_edge(
            src["top"], dst["top"],
            ACCENT_REFINE,
            ls="-", lw=1.0,
            label="«refine»",
            rad=-0.4,
            label_fs=7.5,
        )

    # ------------------------------------------------------------------
    # Legend strip across the bottom
    # ------------------------------------------------------------------
    legend_y = 0.10
    legend_items = [
        ("derive  (F -> R)",      ACCENT_DERIVE,   (0, (5, 3))),
        ("refine  (R -> R)",      ACCENT_REFINE,   "-"),
        ("satisfy (Subsys -> R)", ACCENT_SATISFY,  "-"),
        ("verify  (TP -> R)",     ACCENT_VERIFY,   (0, (1, 2))),
    ]
    spacing = 4.6
    start_x = (X_MAX - (len(legend_items) - 1) * spacing) / 2 - 1.0
    for i, (label, color, ls) in enumerate(legend_items):
        cx = start_x + i * spacing
        # Sample line
        ax.plot(
            [cx, cx + 1.0], [legend_y, legend_y],
            color=color, linewidth=1.6, linestyle=ls, solid_capstyle="round",
        )
        # Arrow tip
        ax.add_patch(FancyArrowPatch(
            (cx + 0.95, legend_y), (cx + 1.10, legend_y),
            arrowstyle="-|>", color=color, linewidth=1.4,
            mutation_scale=10,
        ))
        ax.text(cx + 1.30, legend_y, label,
                ha="left", va="center", fontsize=9, color=TEXT)

    pdf, png = save_mpl("mbse_requirement_diagram", dpi=300)
    register("mbse_requirement_diagram", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
