"""mbe_a3 — Socket.IO Room Namespacing.

Hub-and-spoke: server hub on the left, four room clusters on the right
(user / activity / thread / ride). Edges labeled with event names.

Source: campusride-backend/src/config/socket.js:1-247.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# Distinct fillcolors per room cluster (keep readable on light bg).
ROOM_STYLES = {
    "user": {
        "fill": "#FDEBD0",      # warm peach
        "border": "#B9770E",
        "title": "user:{userId} -- personal/notification room",
        "annot": "sendNotificationToUser()  [socket.js:184]",
    },
    "activity": {
        "fill": "#D5F5E3",      # mint
        "border": "#1E8449",
        "title": "activity:{activityId} -- activity live chat",
        "annot": "sendNotificationToActivity()  [socket.js:190]\\l"
                 "client emits join_activity   [socket.js:124]\\l",
    },
    "thread": {
        "fill": "#D6EAF8",      # sky
        "border": "#1F618D",
        "title": "thread:{threadId} -- DM and group typing",
        "annot": "sendMessageToThread()  [socket.js:211]\\l"
                 "client emits join_message_thread  [socket.js:139]\\l"
                 "typing_indicator broadcast excludes sender  [socket.js:151-158]\\l",
    },
    "ride": {
        "fill": "#FADBD8",      # rose
        "border": "#922B21",
        "title": "ride:{rideId} -- ride-scoped (implicit)",
        "annot": "sendRideshareUpdate()  [socket.js:201]",
    },
}


def _add_room(g, key: str, events: list[tuple[str, str]]) -> str:
    """Add a room cluster. events = [(node_id, label), ...].

    Returns the cluster's representative node-id (the "title card") so the
    server hub can connect into the cluster.
    """
    style = ROOM_STYLES[key]
    cname = f"cluster_{key}"
    title_id = f"{key}_title"
    with g.subgraph(name=cname) as c:
        c.attr(
            label=f"{style['title']}\\n\\n{style['annot']}",
            style="rounded,filled",
            fillcolor=style["fill"],
            color=style["border"],
            penwidth="2.0",
            fontname="Helvetica-Bold",
            fontsize="11",
            margin="14",
        )
        # An invisible anchor so we can route hub -> cluster cleanly.
        c.node(
            title_id,
            label=f"room\\n{style['title'].split(' -- ')[0]}",
            shape="folder",
            style="filled,bold",
            fillcolor="white",
            color=style["border"],
            fontname="Helvetica-Bold",
            fontsize="11",
        )
        for node_id, label in events:
            c.node(
                node_id,
                label=label,
                shape="box",
                style="rounded,filled",
                fillcolor="white",
                color=style["border"],
                fontname="Helvetica",
                fontsize="10",
            )
            c.edge(title_id, node_id,
                   color=style["border"], penwidth="1.0",
                   arrowhead="vee", arrowsize="0.7")
    return title_id


@renderer("mbe_a3_socketio_rooms")
def render():
    g = make_digraph("a3_socketio_rooms", rankdir="LR")
    g.attr(nodesep="0.35", ranksep="1.1", splines="spline",
           label="Socket.IO Room Namespacing  (campusride-backend/src/config/socket.js)",
           labelloc="t", fontsize="13", fontname="Helvetica-Bold")

    # --- Server hub --------------------------------------------------------
    hub_label = (
        "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"2\">"
        "<TR><TD><B>Socket.IO Server</B></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"10\">SocketManager (singleton)</FONT></TD></TR>"
        "<TR><TD><FONT POINT-SIZE=\"9\">[socket.js:5-244]</FONT></TD></TR>"
        "<TR><TD ALIGN=\"LEFT\"><FONT POINT-SIZE=\"9\">"
        "<B>Auth (mandatory):</B><BR ALIGN=\"LEFT\"/>"
        "&#8226; JWT via handshake.auth.token<BR ALIGN=\"LEFT\"/>"
        "&#8226; type='guest' -&gt; read-only<BR ALIGN=\"LEFT\"/>"
        "&#8226; Redis adapter (multi-instance)<BR ALIGN=\"LEFT\"/>"
        "</FONT></TD></TR>"
        "</TABLE>>"
    )
    g.node(
        "hub",
        label=hub_label,
        shape="box",
        style="filled,bold",
        fillcolor="#2C3E50",
        fontcolor="white",
        color="#1A252F",
        penwidth="2.5",
        margin="0.18",
    )

    # --- Client (left of hub, drives connection auth) ---------------------
    g.node(
        "client",
        label="Client\\n(handshake.auth.token)",
        shape="component",
        style="filled",
        fillcolor="#ECF0F1",
        color="#7F8C8D",
        fontsize="10",
    )
    g.edge("client", "hub",
           label="connect + JWT",
           fontsize="9", color="#7F8C8D",
           style="dashed", arrowhead="normal")

    # --- 4 room clusters ---------------------------------------------------
    user_anchor = _add_room(g, "user", [
        ("evt_notification", "notification"),
        ("evt_user_online", "user_online"),
        ("evt_user_offline", "user_offline"),
        ("evt_online_users", "online_users"),
    ])
    activity_anchor = _add_room(g, "activity", [
        ("evt_activity_notification", "activity_notification"),
        ("evt_activity_message", "activity_message"),
        ("evt_join_activity", "join_activity (in)"),
    ])
    thread_anchor = _add_room(g, "thread", [
        ("evt_new_message", "new_message"),
        ("evt_typing_indicator", "typing_indicator\\n(broadcast excl. sender)"),
        ("evt_join_message_thread", "join_message_thread (in)"),
    ])
    ride_anchor = _add_room(g, "ride", [
        ("evt_rideshare_update", "rideshare_update"),
    ])

    # --- Hub -> room edges with the primary event/label -------------------
    edge_specs = [
        (user_anchor,     "emit  notification\\n(to user:{userId})",        "#B9770E"),
        (activity_anchor, "emit  activity_notification\\n(to activity:{id})", "#1E8449"),
        (thread_anchor,   "emit  new_message / typing_indicator\\n(to thread:{id})", "#1F618D"),
        (ride_anchor,     "emit  rideshare_update\\n(to ride:{rideId})",     "#922B21"),
    ]
    for tgt, lbl, col in edge_specs:
        g.edge("hub", tgt,
               label=lbl,
               color=col, fontcolor=col,
               penwidth="1.6", fontsize="10",
               arrowhead="normal", arrowsize="0.9")

    pdf, png = render_dot(g, "mbe_a3_socketio_rooms", dpi=300)
    register("mbe_a3_socketio_rooms", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
