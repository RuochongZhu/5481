"""mbe_b3 — Marketplace Item Lifecycle + Side Effects.

A state machine for `marketplace_items.status` (active / sold / removed)
plus a right-side cluster of side-effects fired on listing creation:
  (a) wxgroup_notice_record insert with mini-program/H5 link
  (b) aggregate counters (views_count, favorites_count)
  (c) companion threads (marketplace_comments, parent_id self, soft-delete)
  (d) cross-module DM (messages with context_type='marketplace')

Source: §5.3 of the draft + migrations 004_marketplace_schema.sql,
005_marketplace_comments.sql, 005_wxgroup_notice_record.sql in
integration-production/campusride-backend/database/migrations/.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# State colors per spec
STATE_COLORS = {
    "active":  {"fill": "#D5F5E3", "border": "#1E8449"},   # green
    "sold":    {"fill": "#E8DAEF", "border": "#6C3483"},   # purple
    "removed": {"fill": "#D5DBDB", "border": "#566573"},   # grey
}

# Side-effect cluster colors (warm peach to differentiate from state cluster)
SIDE_FILL = "#FEF9E7"
SIDE_BORDER = "#B9770E"


@renderer("mbe_b3_marketplace_state_machine")
def render():
    g = make_digraph("b3_marketplace_state_machine", rankdir="LR")
    g.attr(
        nodesep="0.45", ranksep="1.0", splines="spline",
        label=("Marketplace Item Lifecycle + Listing-Creation Side Effects"
               "  (marketplace_items.status; migrations 004 / 005)"),
        labelloc="t", fontsize="13", fontname="Helvetica-Bold",
    )

    # ----- Main cluster: state machine ------------------------------------
    with g.subgraph(name="cluster_states") as c:
        c.attr(
            label=(
                "Item state machine (marketplace_items.status)\\n"
                "snapshot 2026-04-23: 15 items total -- ALL status='removed'\\l"
                "12 aggregate views, 0 favorites, 0 marketplace_comments rows\\l"
                "soft-delete preserves auditability for ratings + cross-user threads\\l"
            ),
            style="rounded,filled",
            fillcolor="#F8F9F9",
            color="#34495E",
            penwidth="1.6",
            fontname="Helvetica-Bold",
            fontsize="11",
            margin="14",
        )

        # [start] pseudo-node
        c.node(
            "start",
            label="[start]",
            shape="circle",
            style="filled",
            fillcolor="black",
            fontcolor="white",
            fontname="Helvetica-Bold",
            fontsize="10",
            width="0.35", height="0.35", fixedsize="true",
        )

        # active state
        c.node(
            "active",
            label=("<<B>active</B><BR/>"
                   "<FONT POINT-SIZE=\"10\">status = 'active'</FONT><BR/>"
                   "<FONT POINT-SIZE=\"9\">[004:16]</FONT>>"),
            shape="box", style="rounded,filled",
            fillcolor=STATE_COLORS["active"]["fill"],
            color=STATE_COLORS["active"]["border"],
            penwidth="2.0",
        )

        # sold state (final, double border via peripheries)
        c.node(
            "sold",
            label=("<<B>sold</B><BR/>"
                   "<FONT POINT-SIZE=\"10\">status = 'sold'  (final)</FONT><BR/>"
                   "<FONT POINT-SIZE=\"9\">manual today; buyer-side context absent</FONT>>"),
            shape="box", style="rounded,filled",
            fillcolor=STATE_COLORS["sold"]["fill"],
            color=STATE_COLORS["sold"]["border"],
            peripheries="2",
            penwidth="2.0",
        )

        # removed state (final, soft-delete)
        c.node(
            "removed",
            label=("<<B>removed</B><BR/>"
                   "<FONT POINT-SIZE=\"10\">status = 'removed'  (final, soft-delete)</FONT><BR/>"
                   "<FONT POINT-SIZE=\"9\">row preserved; FKs to ratings/threads remain valid</FONT>>"),
            shape="box", style="rounded,filled",
            fillcolor=STATE_COLORS["removed"]["fill"],
            color=STATE_COLORS["removed"]["border"],
            peripheries="2",
            penwidth="2.0",
        )

        # transitions
        c.edge("start", "active",
               label=("createListing()\\n"
                      "+ fires side-effects (right cluster)"),
               color=STATE_COLORS["active"]["border"],
               fontcolor=STATE_COLORS["active"]["border"],
               penwidth="1.8", fontsize="10", arrowsize="0.9")
        c.edge("active", "sold",
               label="markSold()\\n(currently manual)",
               color=STATE_COLORS["sold"]["border"],
               fontcolor=STATE_COLORS["sold"]["border"],
               penwidth="1.6", fontsize="10", arrowsize="0.9")
        c.edge("active", "removed",
               label="deleteListing()\\nsoft-delete (status='removed')",
               color=STATE_COLORS["removed"]["border"],
               fontcolor=STATE_COLORS["removed"]["border"],
               penwidth="1.6", fontsize="10", arrowsize="0.9")

    # ----- Right cluster: side effects on listing creation ----------------
    with g.subgraph(name="cluster_side_effects") as s:
        s.attr(
            label=("Cross-module reuse: side effects on listing creation\\l"
                   "(active state spawns these on createListing())\\l"),
            style="rounded,filled",
            fillcolor=SIDE_FILL,
            color=SIDE_BORDER,
            penwidth="2.0",
            fontname="Helvetica-Bold",
            fontsize="11",
            margin="14",
        )

        # (a) wxgroup_notice_record insert
        s.node(
            "se_a",
            label=(
                "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
                "<TR><TD ALIGN=\"LEFT\"><B>(a) wxgroup_notice_record insert</B></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
                "[migration 005_wxgroup_notice_record.sql]"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
                "formatted: &quot;&#20108;&#25163;&#19978;&#26032; &lt;title&gt; + short link&quot;"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
                "link = wechatLinkService.getBestNoticeLink:<BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;1) try mini-program short link<BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;2) fallback to H5 URL"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\" BGCOLOR=\"#FCF3CF\"><FONT POINT-SIZE=\"9\">"
                "snapshot: <B>62 / 82</B> rows are marketplace pushes"
                "</FONT></TD></TR>"
                "</TABLE>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=SIDE_BORDER, penwidth="1.4",
        )

        # (b) aggregate counters
        s.node(
            "se_b",
            label=(
                "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
                "<TR><TD ALIGN=\"LEFT\"><B>(b) aggregate counters</B></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
                "[004:17-18]"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
                "marketplace_items.views_count++<BR ALIGN=\"LEFT\"/>"
                "marketplace_items.favorites_count <BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;on marketplace_item_favorites insert"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\" BGCOLOR=\"#FCF3CF\"><FONT POINT-SIZE=\"9\">"
                "snapshot: 12 views, 0 favorites"
                "</FONT></TD></TR>"
                "</TABLE>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=SIDE_BORDER, penwidth="1.4",
        )

        # (c) companion threads
        s.node(
            "se_c",
            label=(
                "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
                "<TR><TD ALIGN=\"LEFT\"><B>(c) companion threads</B></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
                "[migration 005_marketplace_comments.sql]"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
                "marketplace_comments table:<BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;parent_id -&gt; self  (threading)<BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;is_deleted  (soft-delete)"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\" BGCOLOR=\"#FCF3CF\"><FONT POINT-SIZE=\"9\">"
                "snapshot: 0 rows"
                "</FONT></TD></TR>"
                "</TABLE>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=SIDE_BORDER, penwidth="1.4",
        )

        # (d) cross-module DM
        s.node(
            "se_d",
            label=(
                "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
                "<TR><TD ALIGN=\"LEFT\"><B>(d) cross-module DM</B></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
                "[messages table; context_*]"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"10\">"
                "&quot;Contact seller&quot; -&gt; messages thread<BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;context_type = 'marketplace'<BR ALIGN=\"LEFT\"/>"
                "&nbsp;&nbsp;context_id   = &lt;item_id&gt;"
                "</FONT></TD></TR>"
                "<TR><TD ALIGN=\"LEFT\" BGCOLOR=\"#FCF3CF\"><FONT POINT-SIZE=\"9\">"
                "soft-delete keeps thread linkable post-removal"
                "</FONT></TD></TR>"
                "</TABLE>>"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=SIDE_BORDER, penwidth="1.4",
        )

        # Stack vertically inside the cluster
        s.edge("se_a", "se_b", style="invis")
        s.edge("se_b", "se_c", style="invis")
        s.edge("se_c", "se_d", style="invis")

    # ----- Active -> side-effect cluster edges ----------------------------
    edge_kw = dict(color=SIDE_BORDER, fontcolor=SIDE_BORDER,
                   penwidth="1.4", fontsize="9",
                   arrowhead="vee", arrowsize="0.8",
                   style="dashed")
    g.edge("active", "se_a", label="(a) push notice", **edge_kw)
    g.edge("active", "se_b", label="(b) init counters", **edge_kw)
    g.edge("active", "se_c", label="(c) thread root", **edge_kw)
    g.edge("active", "se_d", label="(d) DM context", **edge_kw)

    pdf, png = render_dot(g, "mbe_b3_marketplace_state_machine", dpi=300)
    register("mbe_b3_marketplace_state_machine", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
