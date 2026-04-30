"""mbe_d3 — WeChat Group Outreach Pipeline.

LR pipeline showing how module events become WeChat-group push notices via
the `wxgroup_notice_record` queue + batch poller + link service.

Source-of-truth:
  campusride-backend/app.js:165-281, 313-328
  campusride-backend/src/services/wechat-link.service.js:81-88
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import renderer, make_digraph, render_dot, register  # noqa: E402


# Palette ---------------------------------------------------------------------
PROD_FILL = "#D6EAF8"      # producers — light blue tints
PROD_BORDER = "#1F618D"
PROD_FILL_HI = "#AED6F1"   # the largest producer (62/82)

QUEUE_FILL = "#FCF3CF"     # yellow — queue table
QUEUE_BORDER = "#B7950B"

LINK_FILL = "#FAE5D3"      # orange — external API
LINK_BORDER = "#B9540B"

POLL_FILL = "#D5F5E3"      # green — server batch logic
POLL_BORDER = "#1E8449"

DEC_FILL = "#FCF3CF"
DEC_BORDER = "#B7950B"

WECHAT_FILL = "#FADBD8"    # pink/light red — external sink
WECHAT_BORDER = "#922B21"

ANNOT_FILL = "#FBFCFC"
ANNOT_BORDER = "#566573"


@renderer("mbe_d3_wechat_outreach_pipeline")
def render():
    g = make_digraph("d3_wechat", rankdir="LR")
    g.attr(
        nodesep="0.30", ranksep="0.45", splines="spline",
        label=(
            "WeChat Group Outreach Pipeline  "
            "(app.js:165-281, 313-328 · wechat-link.service.js:81-88)"
        ),
        labelloc="t", fontsize="14", fontname="Helvetica-Bold",
    )
    g.attr("node", fontsize="10")
    g.attr("edge", fontsize="9")

    # ---- LEFT: Producers cluster ------------------------------------------
    with g.subgraph(name="cluster_producers") as c:
        c.attr(
            label="Producers (module events → INSERT into queue)",
            style="rounded,filled", fillcolor="#EBF5FB",
            color=PROD_BORDER, fontname="Helvetica-Bold", fontsize="11",
            margin="10",
        )
        c.node(
            "prod_ride",
            label=(
                "<<B>New ride created</B><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "rideshare module<BR/>"
                "content: \"rideshare 内容...\"<BR/>"
                "<B>16 / 82</B> rows in snapshot"
                "</FONT>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor=PROD_FILL, color=PROD_BORDER, penwidth="1.4",
        )
        c.node(
            "prod_market",
            label=(
                "<<B>New marketplace listing</B><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "marketplace module<BR/>"
                "content: \"二手上新 &lt;title&gt;...\"<BR/>"
                "<B>62 / 82</B> rows  (largest producer)"
                "</FONT>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor=PROD_FILL_HI, color=PROD_BORDER, penwidth="1.8",
        )
        c.node(
            "prod_act",
            label=(
                "<<B>New activity published</B><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "activities module<BR/>"
                "content: \"新活动 &lt;title&gt;...\"<BR/>"
                "<B>4 / 82</B> rows"
                "</FONT>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor=PROD_FILL, color=PROD_BORDER, penwidth="1.4",
        )

    # ---- CENTER 1: link service (used during row construction) ------------
    g.node(
        "link_svc",
        label=(
            "<<B>wechatLinkService.getBestNoticeLink(h5_url)</B>"
            "<FONT POINT-SIZE=\"9\"> [wechat-link.service.js:81-88]</FONT><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "<B>try</B> generateMiniProgramShortLink(target_url)<BR/>"
            "  → WeChat API: page_url_query = {queryKey}={target_url}<BR/>"
            "<B>fallback</B> on any API failure: return raw H5 URL<BR/>"
            "(append resulting link to message text)"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=LINK_FILL, color=LINK_BORDER, penwidth="1.6",
    )

    # ---- CENTER 2: queue table -------------------------------------------
    g.node(
        "queue",
        label=(
            "<<B>wxgroup_notice_record</B>  "
            "<FONT POINT-SIZE=\"9\">(queue table)</FONT><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "id · content TEXT · sendtime TIMESTAMPTZ (NULL = unsent)<BR/>"
            "created_at · updated_at<BR/>"
            "<B>snapshot:</B> 82 rows · 2026-01-17 → 2026-04-11"
            "</FONT>>"
        ),
        shape="cylinder", style="filled",
        fillcolor=QUEUE_FILL, color=QUEUE_BORDER, penwidth="2.0",
        fontsize="11",
    )

    # ---- CENTER 3: Batch poller cluster -----------------------------------
    with g.subgraph(name="cluster_poller") as c:
        c.attr(
            label="Batch poller endpoints",
            style="rounded,filled", fillcolor="#E8F8F5",
            color=POLL_BORDER, fontname="Helvetica-Bold", fontsize="11",
            margin="10",
        )
        c.node(
            "endpoint_v1",
            label=(
                "<<B>GET /wxgroup_notice_wait</B>"
                "<FONT POINT-SIZE=\"9\"> [app.js:165]</FONT><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "original endpoint (one-row poll)"
                "</FONT>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor=POLL_FILL, color=POLL_BORDER, penwidth="1.4",
        )
        c.node(
            "endpoint_v2",
            label=(
                "<<B>GET /wxgroup_notice_wait_v2</B>"
                "<FONT POINT-SIZE=\"9\"> [app.js:220]</FONT><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "v2 with batching"
                "</FONT>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor=POLL_FILL, color=POLL_BORDER, penwidth="1.4",
        )
        c.node(
            "batch_decision",
            label=(
                "<<B>Batch decision</B>"
                "<FONT POINT-SIZE=\"9\"> [app.js:313-328]</FONT><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "trigger if <B>3+ unsent rows</B><BR/>"
                "OR <B>oldest row ≥ 24h old</B>"
                "</FONT>>"
            ),
            shape="diamond", style="filled",
            fillcolor=DEC_FILL, color=DEC_BORDER, penwidth="1.8",
            height="1.2", width="2.4", fixedsize="false", margin="0.18",
        )
        c.node(
            "merge",
            label=(
                "<<B>Merge + dispatch</B><BR/>"
                "<FONT POINT-SIZE=\"9\">"
                "concat: \"1. notice1\\n\\n2. notice2\\n\\n3. notice3\"<BR/>"
                "on dispatch: <B>UPDATE sendtime = NY_TIMEZONE_NOW</B><BR/>"
                "for the batched record ids"
                "</FONT>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor=POLL_FILL, color=POLL_BORDER, penwidth="1.4",
        )

    # ---- RIGHT: WeChat groups sink ----------------------------------------
    g.node(
        "wechat_groups",
        label=(
            "<<B>External WeChat groups</B><BR/>"
            "<FONT POINT-SIZE=\"10\">(Cornell student channels)</FONT><BR/>"
            "<FONT POINT-SIZE=\"9\"><I>"
            "Authors curate; out-of-band from<BR/>"
            "platform identity verification"
            "</I></FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=WECHAT_FILL, color=WECHAT_BORDER, penwidth="1.8",
        fontsize="11",
    )

    # ---- Bottom annotations ----------------------------------------------
    g.node(
        "annot_bridge",
        label=(
            "Cross-posting bridges grassroots WeChat coordination practice\\l"
            "(cf. §2.2 + §5.7.5) to platform-published events.\\l"
        ),
        shape="note", style="filled",
        fillcolor="#FEF9E7", color=ANNOT_BORDER, fontsize="9",
    )
    g.node(
        "annot_uptake",
        label=(
            "62 marketplace pushes account for the platform's primary outbound\\l"
            "channel — yet marketplace_items snapshot is all `removed`,\\l"
            "suggesting cross-posting works but organic uptake hasn't followed\\l"
            "(cf. §5.10).\\l"
        ),
        shape="note", style="filled",
        fillcolor="#FEF9E7", color=ANNOT_BORDER, fontsize="9",
    )

    # ---- Edges: producers -> queue (with link_svc as side-call) -----------
    # Each producer INSERTs directly into the queue; link_svc is a side
    # helper invoked while building content (drawn off-rank below).
    for src in ("prod_ride", "prod_market", "prod_act"):
        g.edge(src, "queue",
               label="INSERT (sendtime=NULL)",
               color=PROD_BORDER, fontcolor=PROD_BORDER, arrowhead="vee")
    # link_svc as a side-call (non-constraining) — every producer calls it
    # while constructing the content text.
    g.edge("prod_market", "link_svc",
           label="getBestNoticeLink(h5_url)",
           color=LINK_BORDER, fontcolor=LINK_BORDER,
           style="dashed", arrowhead="vee", constraint="false")
    g.edge("link_svc", "queue",
           label="link appended",
           color=LINK_BORDER, fontcolor=LINK_BORDER,
           style="dashed", arrowhead="vee", constraint="false")

    # ---- Edges: queue -> poller endpoints ---------------------------------
    g.edge("queue", "endpoint_v1",
           label="SELECT WHERE sendtime IS NULL",
           color=QUEUE_BORDER, fontcolor=QUEUE_BORDER, arrowhead="vee")
    g.edge("queue", "endpoint_v2",
           label="SELECT unsent rows",
           color=QUEUE_BORDER, fontcolor=QUEUE_BORDER, arrowhead="vee")

    # v2 path goes through batch_decision -> merge
    g.edge("endpoint_v2", "batch_decision",
           color=POLL_BORDER, arrowhead="vee")
    g.edge("batch_decision", "merge",
           label="3+ rows OR ≥24h",
           color=DEC_BORDER, fontcolor=DEC_BORDER, arrowhead="vee")
    g.edge("batch_decision", "endpoint_v2",
           label="hold",
           color=DEC_BORDER, fontcolor=DEC_BORDER,
           style="dashed", arrowhead="vee", constraint="false")

    # v1 path goes straight to merge (single-row "merge")
    g.edge("endpoint_v1", "merge",
           label="single row",
           color=POLL_BORDER, fontcolor=POLL_BORDER,
           style="dashed", arrowhead="vee")

    # ---- Edges: merge -> wechat groups, and writeback to queue ------------
    g.edge("merge", "wechat_groups",
           label="push message",
           color=POLL_BORDER, fontcolor=POLL_BORDER,
           penwidth="1.6", arrowhead="vee")
    g.edge("merge", "queue",
           label="UPDATE sendtime = NOW",
           color=POLL_BORDER, fontcolor=POLL_BORDER,
           style="dotted", arrowhead="vee", constraint="false")

    # ---- Annotation hookups (non-constraining) ----------------------------
    g.edge("wechat_groups", "annot_bridge",
           style="dotted", color=ANNOT_BORDER, arrowhead="none",
           constraint="false")
    g.edge("prod_market", "annot_uptake",
           style="dotted", color=ANNOT_BORDER, arrowhead="none",
           constraint="false")

    pdf, png = render_dot(g, "mbe_d3_wechat_outreach_pipeline", dpi=200)
    register("mbe_d3_wechat_outreach_pipeline", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
