"""mbe_c5 — createRide() Fan-Out (WeChat outreach origin).

Replaces the inaccurate WeChat-outreach branch previously attached to
`bookRide` in mbe_c1. The wxgroup_notice_record INSERT actually fires when
a driver PUBLISHES a ride, not when a passenger BOOKS one.

Source-of-truth: controllers/carpooling.controller.js:78-172 (createRide).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import make_digraph, render_dot, register, renderer  # noqa: E402


CENTRAL_FILL = "#1A5276"
CENTRAL_FONT = "white"
CENTRAL_BORDER = "#0E2F44"

BR_GREEN_FILL = "#D5F5E3"
BR_GREEN_BORDER = "#1E8449"

BR_PURPLE_FILL = "#E8DAEF"
BR_PURPLE_BORDER = "#6C3483"

BR_GREY_FILL = "#F2F4F4"
BR_GREY_BORDER = "#566573"


@renderer("mbe_c5_createRide_fanout")
def render():
    g = make_digraph("c5_createRide_fanout", rankdir="LR")
    g.attr(
        nodesep="0.45", ranksep="1.0", splines="spline",
        label=(
            "createRide() Fan-Out  "
            "(controllers/carpooling.controller.js:78-172)"
        ),
        labelloc="t", fontsize="14", fontname="Helvetica-Bold",
    )
    g.attr("node", fontsize="10")
    g.attr("edge", fontsize="9")

    # Central node
    central_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD><FONT POINT-SIZE=\"15\"><B>createRide()</B></FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"10\">POST /api/v1/carpooling/rides</FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">"
        "carpooling.controller.js:78-172"
        "</FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">driver-side entrypoint</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "createRide",
        label=central_label,
        shape="box", style="filled,bold",
        fillcolor=CENTRAL_FILL, fontcolor=CENTRAL_FONT,
        color=CENTRAL_BORDER, penwidth="3.0", margin="0.22",
    )

    # =========================================================================
    # (1) rides INSERT  [green]
    # =========================================================================
    with g.subgraph(name="cluster_rides") as c:
        c.attr(
            label="(1) Persist ride\\ncarpooling.controller.js:108-138",
            style="rounded,filled",
            fillcolor=BR_GREEN_FILL, color=BR_GREEN_BORDER,
            penwidth="2.0", fontname="Helvetica-Bold",
            fontsize="11", margin="14",
        )
        c.node(
            "ride_insert",
            label=(
                "INSERT rides (status='active')\\l"
                "  driver_id, title, departure/destination_location\\l"
                "  departure_time, available_seats, price_per_seat\\l"
                "  vehicle_info, preferences, contact_info, rules\\l"
                "RETURNING *  with driver embed\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=BR_GREEN_BORDER, penwidth="1.4",
        )
        c.node(
            "ride_outcome",
            label="rides.status = 'active'\\n(initial state for mbe_b1)",
            shape="note", style="filled",
            fillcolor="#EAFAF1", color=BR_GREEN_BORDER, fontsize="9",
        )
        c.edge("ride_insert", "ride_outcome",
               color=BR_GREEN_BORDER, arrowhead="vee")

    # =========================================================================
    # (2) WeChat outreach pipeline  [purple]
    # =========================================================================
    with g.subgraph(name="cluster_wechat") as c:
        c.attr(
            label=(
                "(2) WeChat outreach\\n"
                "carpooling.controller.js:145-162    "
                "wechat-link.service.js:81-88"
            ),
            style="rounded,filled",
            fillcolor=BR_PURPLE_FILL, color=BR_PURPLE_BORDER,
            penwidth="2.0", fontname="Helvetica-Bold",
            fontsize="11", margin="14",
        )

        c.node(
            "wechat_h5",
            label=(
                "rideH5Link =\\l"
                "  https://www.campusgo.college\\l"
                "         /rideshare/{ride.id}\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=BR_PURPLE_BORDER, penwidth="1.2",
        )
        c.node(
            "wechat_link",
            label=(
                "wechatLinkService.getBestNoticeLink(rideH5Link)\\l"
                "  try:  generateMiniProgramShortLink(rideH5Link)\\l"
                "        -> WeChat API\\l"
                "  fallback:  return rideH5Link\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=BR_PURPLE_BORDER, penwidth="1.2",
        )
        c.node(
            "wechat_content",
            label=(
                "noticeContent =\\l"
                "  '🚗 打车 | {fromSimple} -> {toSimple}\\\\n{rideLink}'\\l"
                "  via simplifyLocation()\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=BR_PURPLE_BORDER, penwidth="1.2",
        )
        c.node(
            "wechat_insert",
            label=(
                "INSERT wxgroup_notice_record\\l"
                "  (content = noticeContent,\\l"
                "   sendtime = NULL)\\l"
                "wrapped in try/catch (warn-only)\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor="#FBEEFB", color=BR_PURPLE_BORDER, penwidth="1.6",
        )
        c.node(
            "wechat_annot",
            label="snapshot (2026-04-23):\\n16 of 82 rows are ride pushes\\n(this is per-ride-create, NOT per-booking)",
            shape="note", style="filled",
            fillcolor="#F5EEF8", color=BR_PURPLE_BORDER, fontsize="9",
        )

        c.edge("wechat_h5", "wechat_link",
               color=BR_PURPLE_BORDER, arrowhead="vee")
        c.edge("wechat_link", "wechat_content",
               color=BR_PURPLE_BORDER, arrowhead="vee")
        c.edge("wechat_content", "wechat_insert",
               color=BR_PURPLE_BORDER, arrowhead="vee")
        c.edge("wechat_insert", "wechat_annot",
               style="dotted", color=BR_PURPLE_BORDER, arrowhead="none")

    # =========================================================================
    # Downstream poller (off-flow grey block on right)
    # =========================================================================
    with g.subgraph(name="cluster_poller") as c:
        c.attr(
            label=(
                "Asynchronous downstream\\n"
                "app.js:165-281, 313-328  (batch poller)"
            ),
            style="rounded,dashed,filled",
            fillcolor=BR_GREY_FILL, color=BR_GREY_BORDER,
            penwidth="1.5", fontname="Helvetica",
            fontsize="11", margin="14",
        )
        c.node(
            "poller",
            label=(
                "GET /wxgroup_notice_wait[_v2]\\l"
                "Batch when 3+ unsent rows OR oldest >= 24h\\l"
                "Concatenate '1. ... 2. ... 3. ...'  -> external WeChat groups\\l"
                "UPDATE sendtime = NY-time NOW()\\l"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=BR_GREY_BORDER, penwidth="1.2",
        )

    # createRide -> branch heads
    g.edge("createRide", "ride_insert",
           label="(1)", color=BR_GREEN_BORDER, fontcolor=BR_GREEN_BORDER,
           penwidth="1.6", arrowhead="vee")
    g.edge("createRide", "wechat_h5",
           label="(2)", color=BR_PURPLE_BORDER, fontcolor=BR_PURPLE_BORDER,
           penwidth="1.6", arrowhead="vee")

    # wechat insert flows asynchronously into the poller
    g.edge("wechat_insert", "poller",
           label="awaits poller drain",
           style="dashed", color=BR_GREY_BORDER, fontcolor=BR_GREY_BORDER,
           constraint="false", arrowhead="vee")

    # Footer
    footer_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
        "<B>Per ride publish:</B>  "
        "1 <I>rides</I> row  +  "
        "1 <I>wxgroup_notice_record</I> row  +  "
        "0 notifications  +  "
        "0 group rows (created lazily on first booking, see mbe_b4 / mbe_c1)"
        "</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\" COLOR=\"#1B4F72\">"
        "Sibling outreach paths: marketplace.controller.js:70 (62 of 82),  "
        "activity.service.js:147 (4 of 82).  All converge on "
        "wxgroup_notice_record as the same queue."
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "footer",
        label=footer_label,
        shape="box", style="rounded,filled",
        fillcolor="#FBFCFC", color="#566573",
        penwidth="1.0", margin="0.18",
    )
    g.edge("createRide", "footer", style="invis", constraint="false")

    pdf, png = render_dot(g, "mbe_c5_createRide_fanout", dpi=300)
    register("mbe_c5_createRide_fanout", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
