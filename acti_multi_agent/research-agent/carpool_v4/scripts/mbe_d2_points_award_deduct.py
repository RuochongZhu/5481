"""mbe_d2 -- Points Award / Deduct Architecture (LR fan-in / fan-out).

Source-of-truth: campusride-backend/src/services/points.service.js:122-236.

Layout (rankdir=LR):
  Left  : 13 point sources, partitioned into two sub-clusters
            * System (registration, verification, daily_login, profile_complete)
            * Activity-triggered (5 rules)
            * plus rideshare_completion, marketplace_transaction,
              referral, consecutive_checkin
  Center: awardPoints({...}) and deductPoints({...}) services with their
          three downstream effects each (point_transactions INSERT,
          increment_user_points RPC, Socket.IO emit).
  Right : Sinks (coupons table, activities.entry_fee_points).

Top   : RED production-reality flag (NOT yet provisioned).
Bottom: italic-grey design-rationale annotation (cf. F4).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import renderer, make_digraph, render_dot, register  # noqa: E402


# --- palette ---------------------------------------------------------------
SRC_FILL = "#D5F5E3"          # green tint
SRC_BORDER = "#1E8449"
SRC_FILL_ALT = "#E8F8F5"      # paler green for sub-cluster bg

CENTER_FILL = "#1A5276"        # dark blue
CENTER_FONT = "white"
CENTER_BORDER = "#0E2F44"

EFFECT_FILL = "#D6EAF8"
EFFECT_BORDER = "#1F618D"

SINK_FILL = "#FAE5D3"          # orange tint
SINK_BORDER = "#B9540B"

FLAG_FILL = "#F5B7B1"          # red callout fill
FLAG_BORDER = "#922B21"

RAT_FILL = "#FBFCFC"
RAT_BORDER = "#7F8C8D"


# 13 source rules (label -> (display_name, base_value_text))
SOURCES_SYSTEM = [
    ("src_registration",  "registration\\n(+10)\\none-shot on `users` insert"),
    ("src_verification",  "verification\\n(+5)\\non `is_verified` flip"),
    ("src_daily_login",   "daily_login\\n(+1)\\nidempotent / calendar day"),
    ("src_profile",       "profile_complete\\n(+15)\\non avatar + major populated"),
]

SOURCES_ACTIVITY = [
    ("src_act_create",    "activity_creation\\n(+15)"),
    ("src_act_part",      "activity_participation\\n(+10)"),
    ("src_act_org",       "activity_organization\\n(+30)\\norganizer bonus at completion"),
    ("src_act_checkin",   "activity_checkin\\n(+5)\\ngeo-verified  (cf. mbe_c4)"),
    ("src_act_complete",  "activity_completion\\n(+15)"),
]

SOURCES_OTHER = [
    ("src_rideshare",     "rideshare_completion\\n(+15)"),
    ("src_market",        "marketplace_transaction\\n(+8)"),
    ("src_referral",      "referral\\n(+30)"),
    ("src_streak",        "consecutive_checkin\\n(streak; multiplier honored)"),
]


@renderer("mbe_d2_points_award_deduct")
def render():
    g = make_digraph("d2_points", rankdir="LR")
    g.attr(
        nodesep="0.35", ranksep="1.0", splines="spline",
        label=(
            "Points Award / Deduct Architecture  "
            "(services/points.service.js:122-236)"
        ),
        labelloc="t", fontsize="14", fontname="Helvetica-Bold",
    )
    g.attr("node", fontsize="10")
    g.attr("edge", fontsize="9")

    # =========================================================================
    # TOP: production reality flag (red)
    # =========================================================================
    flag_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD><FONT POINT-SIZE=\"13\"><B>"
        "&#9888; Production deployment status: NOT yet provisioned"
        "</B></FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
        "&#8226; <B>point_rules</B> rows: <B>0</B><BR ALIGN=\"LEFT\"/>"
        "&#8226; <B>point_transactions</B> table: <B>DOES NOT EXIST</B> (REST returns PGRST205)<BR ALIGN=\"LEFT\"/>"
        "&#8226; 184 user rows, all <B>users.points = 0</B><BR ALIGN=\"LEFT\"/>"
        "&#8226; Design is implementation-ready but behaviorally inert"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "prod_flag",
        label=flag_label,
        shape="box", style="rounded,filled,bold",
        fillcolor=FLAG_FILL, color=FLAG_BORDER,
        penwidth="3.0", margin="0.22",
    )

    # =========================================================================
    # LEFT: sources — three sub-clusters
    # =========================================================================
    with g.subgraph(name="cluster_sources") as outer:
        outer.attr(
            label="13 point sources (base values from POINT_RULES)",
            style="rounded,filled",
            fillcolor="#FBFEFC", color=SRC_BORDER,
            penwidth="1.6",
            fontname="Helvetica-Bold", fontsize="12",
            margin="14",
        )

        # --- System sub-cluster ---
        with outer.subgraph(name="cluster_sys") as c:
            c.attr(
                label="System: registration, verification, daily, profile",
                style="rounded,filled",
                fillcolor=SRC_FILL_ALT, color=SRC_BORDER,
                penwidth="1.4",
                fontname="Helvetica-Bold", fontsize="10",
                margin="10",
            )
            for nid, lbl in SOURCES_SYSTEM:
                c.node(nid, label=lbl,
                       shape="box", style="rounded,filled",
                       fillcolor=SRC_FILL, color=SRC_BORDER, penwidth="1.2")

        # --- Activity-triggered sub-cluster ---
        with outer.subgraph(name="cluster_act") as c:
            c.attr(
                label="Activity-triggered: 5 rules",
                style="rounded,filled",
                fillcolor=SRC_FILL_ALT, color=SRC_BORDER,
                penwidth="1.4",
                fontname="Helvetica-Bold", fontsize="10",
                margin="10",
            )
            for nid, lbl in SOURCES_ACTIVITY:
                c.node(nid, label=lbl,
                       shape="box", style="rounded,filled",
                       fillcolor=SRC_FILL, color=SRC_BORDER, penwidth="1.2")

        # --- Other (rideshare/market/referral/streak) ---
        with outer.subgraph(name="cluster_other") as c:
            c.attr(
                label="Other: rideshare, marketplace, referral, streak",
                style="rounded,filled",
                fillcolor=SRC_FILL_ALT, color=SRC_BORDER,
                penwidth="1.4",
                fontname="Helvetica-Bold", fontsize="10",
                margin="10",
            )
            for nid, lbl in SOURCES_OTHER:
                c.node(nid, label=lbl,
                       shape="box", style="rounded,filled",
                       fillcolor=SRC_FILL, color=SRC_BORDER, penwidth="1.2")

    # =========================================================================
    # CENTER: awardPoints + deductPoints
    # =========================================================================
    award_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD><FONT POINT-SIZE=\"13\"><B>awardPoints(...)</B></FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">"
        "{user_id, source, reason, points,<BR/>"
        " ruleType, multiplier}"
        "</FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">points.service.js:122-185</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "awardPoints",
        label=award_label,
        shape="box", style="filled,bold",
        fillcolor=CENTER_FILL, fontcolor=CENTER_FONT,
        color=CENTER_BORDER, penwidth="3.0", margin="0.22",
    )

    deduct_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD><FONT POINT-SIZE=\"13\"><B>deductPoints(...)</B></FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">{user_id, points}</FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">points.service.js:188-236</FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">"
        "guard: users.points &#8805; points<BR/>"
        "else  INSUFFICIENT_POINTS"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "deductPoints",
        label=deduct_label,
        shape="box", style="filled,bold",
        fillcolor=CENTER_FILL, fontcolor=CENTER_FONT,
        color=CENTER_BORDER, penwidth="3.0", margin="0.22",
    )

    # --- award effects ---
    g.node(
        "award_eff_tx",
        label=(
            "INSERT  point_transactions\\l"
            "  (user_id, rule_type, points,\\l"
            "   source, reason, metadata,\\l"
            "   multiplier, created_at)\\l"
        ),
        shape="box", style="rounded,filled",
        fillcolor=EFFECT_FILL, color=EFFECT_BORDER, penwidth="1.4",
    )
    g.node(
        "award_eff_rpc",
        label=(
            "RPC  increment_user_points(\\l"
            "  user_id, points_to_add)\\l"
            "atomic UPDATE  users.points\\l"
        ),
        shape="box", style="rounded,filled",
        fillcolor=EFFECT_FILL, color=EFFECT_BORDER, penwidth="1.4",
    )
    g.node(
        "award_eff_socket",
        label=(
            "Socket.IO\\l"
            "socketManager.sendPointsUpdate\\l"
            "-> emit on  user:{userId}  room\\l"
        ),
        shape="box", style="rounded,filled",
        fillcolor=EFFECT_FILL, color=EFFECT_BORDER, penwidth="1.4",
    )

    g.edge("awardPoints", "award_eff_tx",
           color=EFFECT_BORDER, arrowhead="vee", penwidth="1.4")
    g.edge("awardPoints", "award_eff_rpc",
           color=EFFECT_BORDER, arrowhead="vee", penwidth="1.4")
    g.edge("awardPoints", "award_eff_socket",
           color=EFFECT_BORDER, arrowhead="vee", penwidth="1.4")

    # --- deduct effects ---
    g.node(
        "deduct_eff_rpc",
        label=(
            "RPC  increment_user_points(\\l"
            "  user_id, -points)   <- NEGATIVE\\l"
        ),
        shape="box", style="rounded,filled",
        fillcolor=EFFECT_FILL, color=EFFECT_BORDER, penwidth="1.4",
    )
    g.node(
        "deduct_eff_tx",
        label=(
            "INSERT  point_transactions\\l"
            "  type='spent'\\l"
        ),
        shape="box", style="rounded,filled",
        fillcolor=EFFECT_FILL, color=EFFECT_BORDER, penwidth="1.4",
    )
    g.edge("deductPoints", "deduct_eff_rpc",
           color=EFFECT_BORDER, arrowhead="vee", penwidth="1.4")
    g.edge("deductPoints", "deduct_eff_tx",
           color=EFFECT_BORDER, arrowhead="vee", penwidth="1.4")

    # =========================================================================
    # RIGHT: sinks
    # =========================================================================
    with g.subgraph(name="cluster_sinks") as c:
        c.attr(
            label="Sinks (spend targets)",
            style="rounded,filled",
            fillcolor="#FEF5E7", color=SINK_BORDER,
            penwidth="1.6",
            fontname="Helvetica-Bold", fontsize="12",
            margin="14",
        )
        c.node(
            "sink_coupons",
            label=(
                "coupons table\\l"
                "(currently EMPTY: 0 rows)\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor=SINK_FILL, color=SINK_BORDER, penwidth="1.4",
        )
        c.node(
            "sink_entry_fee",
            label=(
                "activities.entry_fee_points\\l"
                "pay-with-points option for\\l"
                "organizer-priced activities\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor=SINK_FILL, color=SINK_BORDER, penwidth="1.4",
        )

    # deductPoints feeds the sinks (logically the user redeems)
    g.edge("deduct_eff_rpc", "sink_coupons",
           color=SINK_BORDER, arrowhead="vee", style="dashed",
           label="redeem", fontcolor=SINK_BORDER)
    g.edge("deduct_eff_rpc", "sink_entry_fee",
           color=SINK_BORDER, arrowhead="vee", style="dashed",
           label="pay entry", fontcolor=SINK_BORDER)

    # =========================================================================
    # Sources -> awardPoints  (fan-in)
    # =========================================================================
    all_sources = (
        [nid for nid, _ in SOURCES_SYSTEM]
        + [nid for nid, _ in SOURCES_ACTIVITY]
        + [nid for nid, _ in SOURCES_OTHER]
    )
    for nid in all_sources:
        g.edge(nid, "awardPoints",
               color=SRC_BORDER, arrowhead="vee",
               penwidth="1.0", arrowsize="0.7")

    # =========================================================================
    # BOTTOM: design rationale (italic grey)
    # =========================================================================
    rat_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\" COLOR=\"#566573\">"
        "<I><B>Design rationale.</B>  "
        "Base-point payouts are capped well below per-seat cash price "
        "(~$22-38) so points <B>complement</B>, not <B>substitute</B>, "
        "the cash motivation lever<BR ALIGN=\"LEFT\"/>"
        "(cf. F4: gamification 48.3 vs financial 63.6 in &#167;4 motivation finding).</I>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "rationale",
        label=rat_label,
        shape="box", style="rounded,filled",
        fillcolor=RAT_FILL, color=RAT_BORDER,
        penwidth="1.0", margin="0.18",
    )

    # Invisible anchors to push flag to top and rationale to bottom of the
    # rank order without distorting the LR backbone.
    g.edge("prod_flag", "awardPoints", style="invis", constraint="false")
    g.edge("awardPoints", "rationale", style="invis", constraint="false")
    g.edge("deductPoints", "rationale", style="invis", constraint="false")

    pdf, png = render_dot(g, "mbe_d2_points_award_deduct", dpi=300)
    register("mbe_d2_points_award_deduct", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
