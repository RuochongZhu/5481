"""mbe_d1 — Cross-Module Messaging Substrate.

Three messaging surfaces (DM, group, system) sit on top of a shared Socket.IO
substrate. A right-side cluster shows how DMs are bound to other modules
(rides, marketplace, activities) via the (context_type, context_id) pair.

Source-of-truth:
  campusride-backend/src/services/messageService.js  (REPLY_REQUIRED guard)
  campusride-backend/src/controllers/messages.controller.js
  campusride-backend/src/controllers/groupMessages.controller.js
  campusride-backend/migrations/010_group_moderation.sql
  campusride-backend/src/config/socket.js  (rooms / events)
  draft §5.7 messaging
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import renderer, make_digraph, render_dot, register  # noqa: E402


# ---- palette --------------------------------------------------------------
DM_FILL = "#D6EAF8"          # light blue
DM_BORDER = "#1F618D"

GROUP_FILL = "#D5F5E3"       # light green
GROUP_BORDER = "#1E8449"

SYS_FILL = "#FCF3CF"         # light yellow
SYS_BORDER = "#B7950B"

SUBSTRATE_FILL = "#34495E"   # dark grey
SUBSTRATE_BORDER = "#1A252F"
SUBSTRATE_FONT = "white"

CTX_FILL = "#E8DAEF"         # light purple
CTX_BORDER = "#6C3483"

GUARD_FILL = "#FAE5D3"       # light orange — REPLY_REQUIRED callout
GUARD_BORDER = "#CA6F1E"

FOOTER_FILL = "#FDFEFE"
FOOTER_BORDER = "#566573"


@renderer("mbe_d1_messaging_substrate")
def render():
    g = make_digraph("d1_messaging_substrate", rankdir="TB")
    g.attr(
        ranksep="0.85", nodesep="0.55", splines="spline",
        label=(
            "Cross-module messaging substrate — three surfaces share one "
            "Socket.IO transport;\nDMs bind to other modules via "
            "(context_type, context_id).  "
            "[messageService.js / groupMessages.controller.js / socket.js, "
            "draft §5.7]"
        ),
        labelloc="t", fontsize="13", fontname="Helvetica-Bold",
    )
    g.attr("node", fontsize="10")
    g.attr("edge", fontsize="9")

    # ------------------------------------------------------------------
    # Top tier — three surface boxes (HTML-like tables for column lists)
    # ------------------------------------------------------------------
    dm_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD ALIGN=\"CENTER\"><B>messages  (DM)</B></TD></TR>"
        "<TR><TD ALIGN=\"CENTER\"><FONT POINT-SIZE=\"9\">"
        "snapshot: <B>22 rows</B></FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<B>columns:</B><BR ALIGN=\"LEFT\"/>"
        "id, sender_id&#8594;users, receiver_id&#8594;users,<BR ALIGN=\"LEFT\"/>"
        "thread_id, subject (2-255), content (1-2000),<BR ALIGN=\"LEFT\"/>"
        "message_type {general | activity_inquiry |<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;activity_update | support},<BR ALIGN=\"LEFT\"/>"
        "<B>context_type</B>, <B>context_id</B>,<BR ALIGN=\"LEFT\"/>"
        "priority, reply_to<BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<B>companion:</B> message_participants (8 rows)<BR ALIGN=\"LEFT\"/>"
        "&#8594; per-side read / archive state<BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "dm",
        label=dm_label,
        shape="box", style="rounded,filled",
        fillcolor=DM_FILL, color=DM_BORDER, penwidth="1.6",
    )

    group_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD ALIGN=\"CENTER\"><B>group_messages</B></TD></TR>"
        "<TR><TD ALIGN=\"CENTER\"><FONT POINT-SIZE=\"9\">"
        "snapshot: <B>2 rows</B> across 5 community groups</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<B>columns:</B><BR ALIGN=\"LEFT\"/>"
        "id, group_id&#8594;groups, sender_id,<BR ALIGN=\"LEFT\"/>"
        "content (CHECK 1-2000),<BR ALIGN=\"LEFT\"/>"
        "message_type {text | image | file},<BR ALIGN=\"LEFT\"/>"
        "deleted_at  (soft-delete)<BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<B>RLS:</B> SELECT only to current group_members;<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;INSERT only when auth.uid() = sender_id<BR ALIGN=\"LEFT\"/>"
        "<B>moderation</B> (migration 010):<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;group_muted_users,<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;group_message_deletions<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;<I>NOT inherited by ride_carpool groups</I><BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "grp",
        label=group_label,
        shape="box", style="rounded,filled",
        fillcolor=GROUP_FILL, color=GROUP_BORDER, penwidth="1.6",
    )

    sys_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD ALIGN=\"CENTER\"><B>system_messages</B></TD></TR>"
        "<TR><TD ALIGN=\"CENTER\"><FONT POINT-SIZE=\"9\">"
        "snapshot: <B>10 rows</B>; all sender_type='user',<BR ALIGN=\"CENTER\"/>"
        "all message_type='feedback'</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<B>columns:</B><BR ALIGN=\"LEFT\"/>"
        "id, user_id, sender_type {admin | user},<BR ALIGN=\"LEFT\"/>"
        "is_pinned, message_type<BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<I>In production: 0 admin announcements;</I><BR ALIGN=\"LEFT\"/>"
        "<I>the 'user' subsurface is the de-facto</I><BR ALIGN=\"LEFT\"/>"
        "<I>feedback channel.</I><BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "sys",
        label=sys_label,
        shape="box", style="rounded,filled",
        fillcolor=SYS_FILL, color=SYS_BORDER, penwidth="1.6",
    )

    # Pin the three surfaces to the same rank (top tier)
    with g.subgraph() as top:
        top.attr(rank="same")
        top.node("dm")
        top.node("grp")
        top.node("sys")

    # ------------------------------------------------------------------
    # REPLY_REQUIRED guard callout — attached to the DM box
    # ------------------------------------------------------------------
    guard_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD ALIGN=\"CENTER\"><B>Guard: REPLY_REQUIRED</B></TD></TR>"
        "<TR><TD ALIGN=\"CENTER\"><FONT POINT-SIZE=\"9\">"
        "messageService.sendMessage()</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "first DM to a recipient with no prior thread<BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;&#8594; 1 message allowed;<BR ALIGN=\"LEFT\"/>"
        "subsequent messages refused with <B>403</B><BR ALIGN=\"LEFT\"/>"
        "&nbsp;&nbsp;until recipient replies once.<BR ALIGN=\"LEFT\"/>"
        "<I>Light-touch first-message friction analog.</I><BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "guard",
        label=guard_label,
        shape="note", style="filled",
        fillcolor=GUARD_FILL, color=GUARD_BORDER, penwidth="1.4",
        fontcolor="#7E5109",
    )
    g.edge(
        "dm", "guard",
        label="enforced on INSERT",
        style="dashed", color=GUARD_BORDER, fontcolor=GUARD_BORDER,
        arrowhead="none", constraint="false", minlen="1",
    )

    # ------------------------------------------------------------------
    # Bottom tier — shared Socket.IO substrate
    # ------------------------------------------------------------------
    substrate_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD><FONT COLOR=\"white\"><B>Shared Socket.IO substrate</B>"
        "</FONT></TD></TR>"
        "<TR><TD><FONT COLOR=\"white\" POINT-SIZE=\"9\">"
        "[campusride-backend/src/config/socket.js — see mbe_a3]"
        "</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT COLOR=\"white\" POINT-SIZE=\"9\">"
        "<B>Rooms:</B> user:{userId} &nbsp;&nbsp; "
        "activity:{activityId} &nbsp;&nbsp; thread:{threadId}"
        "<BR ALIGN=\"LEFT\"/>"
        "<B>Events:</B> notification &nbsp; new_message &nbsp; "
        "typing_indicator &nbsp; online_users<BR ALIGN=\"LEFT\"/>"
        "<B>Auth:</B> JWT on connect; type='guest' &#8594; "
        "read-only token<BR ALIGN=\"LEFT\"/>"
        "<I>All three surfaces share the typing-indicator + "
        "online-presence affordances.</I><BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "substrate",
        label=substrate_label,
        shape="box", style="filled,bold",
        fillcolor=SUBSTRATE_FILL, color=SUBSTRATE_BORDER, penwidth="2.4",
        fontcolor=SUBSTRATE_FONT, margin="0.22",
    )

    # Surface <-> substrate edges (Socket.IO emit, both directions)
    g.edge(
        "dm", "substrate",
        label="emit new_message\n(thread:{threadId})",
        color=DM_BORDER, fontcolor=DM_BORDER, dir="both",
        arrowhead="vee", arrowtail="vee", penwidth="1.4",
    )
    g.edge(
        "grp", "substrate",
        label="emit new_message\n(thread:{groupThreadId})",
        color=GROUP_BORDER, fontcolor=GROUP_BORDER, dir="both",
        arrowhead="vee", arrowtail="vee", penwidth="1.4",
    )
    g.edge(
        "sys", "substrate",
        label="emit notification\n(user:{userId})",
        color=SYS_BORDER, fontcolor="#7D6608", dir="both",
        arrowhead="vee", arrowtail="vee", penwidth="1.4",
    )

    # ------------------------------------------------------------------
    # Right-side cluster — Cross-module context binding (3 examples)
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_context") as c:
        c.attr(
            label="Cross-module context binding\\n"
                  "(messages.context_type, messages.context_id)",
            style="rounded,filled",
            fillcolor=CTX_FILL, color=CTX_BORDER, penwidth="1.8",
            fontname="Helvetica-Bold", fontsize="11",
            fontcolor="#4A235A",
            margin="14",
        )
        c.node(
            "ctx_ride",
            label=(
                "context_type='ride'\n"
                "context_id = <ride_id>\n"
                "DMs originated from a ride card\n"
                "(driver / passenger side-channel)"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=CTX_BORDER, penwidth="1.2",
            fontsize="10",
        )
        c.node(
            "ctx_market",
            label=(
                "context_type='marketplace'\n"
                "context_id = <item_id>\n"
                "'Contact seller' button -> DM thread\n"
                "(62/82 wxgroup_notice rows are\n"
                " marketplace-originated; cf. mbe_b3)"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=CTX_BORDER, penwidth="1.2",
            fontsize="10",
        )
        c.node(
            "ctx_activity",
            label=(
                "context_type='activity'\n"
                "context_id = <activity_id>\n"
                "DMs from activity card\n"
                "(message_type='activity_inquiry'\n"
                " | 'activity_update')"
            ),
            shape="box", style="rounded,filled",
            fillcolor="white", color=CTX_BORDER, penwidth="1.2",
            fontsize="10",
        )

    # DM <-> context cluster (context_type/context_id binding)
    g.edge(
        "dm", "ctx_ride",
        label="(context_type, context_id)",
        color=CTX_BORDER, fontcolor=CTX_BORDER, dir="both",
        arrowhead="vee", arrowtail="vee", penwidth="1.2",
        constraint="false", minlen="2",
    )
    g.edge(
        "dm", "ctx_market",
        color=CTX_BORDER, dir="both",
        arrowhead="vee", arrowtail="vee", penwidth="1.2",
        constraint="false", minlen="2",
    )
    g.edge(
        "dm", "ctx_activity",
        color=CTX_BORDER, dir="both",
        arrowhead="vee", arrowtail="vee", penwidth="1.2",
        constraint="false", minlen="2",
    )

    # ------------------------------------------------------------------
    # Bottom annotation (snapshot footer)
    # ------------------------------------------------------------------
    g.node(
        "footer",
        label=(
            "<<i>Snapshot: 22 DMs concentrated in the "
            "2026-02-05 to 2026-02-28 burst; "
            "18 message_reply notifications attest to that burst. "
            "All DMs is_read=true.</i>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=FOOTER_FILL, color=FOOTER_BORDER, penwidth="1.0",
        fontsize="10",
    )
    g.edge("substrate", "footer", style="invis", constraint="true")

    pdf, png = render_dot(g, "mbe_d1_messaging_substrate", dpi=300)
    register("mbe_d1_messaging_substrate", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")
    return pdf, png


if __name__ == "__main__":
    render()
