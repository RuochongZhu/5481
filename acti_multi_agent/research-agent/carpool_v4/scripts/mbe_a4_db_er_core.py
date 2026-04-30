"""mbe_a4 — Database ER diagram (Core 18 tables, snapshot 2026-04-23).

HTML-like Graphviz nodes for each production table. Foreign-key edges
shown child -> parent with crow's-foot on the many-side. Tables grouped
into clusters by domain. Snapshot row counts appear in each header.

Source-of-truth: integration-production/campusride-backend/database/
migrations/{000,005,006,007,008,009,010,011}_*.sql.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# Per-cluster header colors (light pastel fill + matching dark border)
CLUSTERS = {
    "identity":    {"fill": "#D6EAF8", "border": "#1F618D", "label": "Identity"},
    "carpool":     {"fill": "#FADBD8", "border": "#922B21", "label": "Carpool"},
    "activities":  {"fill": "#D5F5E3", "border": "#1E8449", "label": "Activities"},
    "marketplace": {"fill": "#FAE5D3", "border": "#B9770E", "label": "Marketplace"},
    "messaging":   {"fill": "#E8DAEF", "border": "#6C3483", "label": "Groups & Messaging"},
    "cross":       {"fill": "#FCF3CF", "border": "#9A7D0A", "label": "Cross-module"},
}


def _row(text: str, port: str | None = None, italic: bool = False,
         bold: bool = False, color: str | None = None) -> str:
    """Build one HTML <TR><TD>...</TD></TR> row of a table node."""
    inner = text
    if italic:
        inner = f"<I>{inner}</I>"
    if bold:
        inner = f"<B>{inner}</B>"
    port_attr = f' PORT="{port}"' if port else ""
    color_attr = f' BGCOLOR="{color}"' if color else ""
    return (
        f'<TR><TD ALIGN="LEFT"{port_attr}{color_attr}>{inner}</TD></TR>'
    )


def _table_node(name: str, count: str, columns: list[tuple[str, str, str]],
                fill: str, border: str) -> str:
    """Return an HTML-like label for a table.

    columns: list of (port, text, role) where role in {pk, fk, self_fk, col, note}.
    """
    header = (
        f'<TR><TD BGCOLOR="{fill}" ALIGN="CENTER">'
        f'<B>{name}</B> &nbsp;<FONT POINT-SIZE="9">'
        f'(n={count})</FONT></TD></TR>'
    )
    body = []
    for port, text, role in columns:
        if role == "pk":
            body.append(_row(text, port=port, bold=True))
        elif role in ("fk", "self_fk"):
            body.append(_row(text, port=port, italic=True))
        elif role == "note":
            body.append(_row(f'<FONT POINT-SIZE="9" COLOR="#7B241C">{text}</FONT>',
                             port=port))
        else:
            body.append(_row(text, port=port))
    table = (
        f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3" '
        f'COLOR="{border}">'
        + header + "".join(body) +
        "</TABLE>>"
    )
    return table


@renderer("mbe_a4_db_er_core")
def render():
    g = make_digraph("a4_db_er_core", rankdir="TB")
    g.attr(splines="spline", nodesep="0.35", ranksep="0.7", concentrate="false",
           label=("CampusRide production schema — 18 core tables "
                  "(snapshot 2026-04-23)"),
           labelloc="t", fontsize="14")
    g.attr("node", shape="plaintext", style="", fontname="Helvetica",
           fontsize="10")

    # ---------- Identity cluster ----------
    cl = CLUSTERS["identity"]
    with g.subgraph(name="cluster_identity") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("users", _table_node(
            "users", "184",
            [
                ("id",    "id : uuid",                "pk"),
                (None,    "email",                    "col"),
                (None,    "university",               "col"),
                (None,    "is_verified",              "col"),
                (None,    "verification_status",      "col"),
                (None,    "avg_rating, total_ratings", "col"),
                (None,    "points",                   "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Carpool cluster ----------
    cl = CLUSTERS["carpool"]
    with g.subgraph(name="cluster_carpool") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("rides", _table_node(
            "rides", "0",
            [
                ("id",        "id : uuid",                                 "pk"),
                ("driver",    "driver_id &#8594; users",                   "fk"),
                (None,        "departure_time",                            "col"),
                (None,        "available_seats",                           "col"),
                (None,        "status (active/full/completed/cancelled)",  "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("ride_bookings", _table_node(
            "ride_bookings", "0",
            [
                ("id",     "id : uuid",                              "pk"),
                ("ride",   "ride_id &#8594; rides",                  "fk"),
                ("pax",    "passenger_id &#8594; users",             "fk"),
                (None,     "status (confirmed/cancelled)",           "col"),
                (None,     "seats_booked",                           "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("ratings", _table_node(
            "ratings", "0",
            [
                ("id",     "id : uuid",                       "pk"),
                ("trip",   "trip_id &#8594; rides",           "fk"),
                ("rater",  "rater_id &#8594; users",          "fk"),
                ("ratee",  "ratee_id &#8594; users",          "fk"),
                (None,     "role_of_rater (driver/passenger)", "col"),
                (None,     "score : 1..5",                    "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Activities cluster ----------
    cl = CLUSTERS["activities"]
    with g.subgraph(name="cluster_activities") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("activities", _table_node(
            "activities", "0",
            [
                ("id",     "id : uuid",                                       "pk"),
                ("org",    "organizer_id &#8594; users",                      "fk"),
                ("group",  "group_id &#8594; groups",                         "fk"),
                (None,     "status (draft/published/ongoing/completed/...)",  "col"),
                (None,     "checkin_enabled",                                 "col"),
                (None,     "location_coordinates",                            "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("activity_participants", _table_node(
            "activity_participants", "0",
            [
                ("id",   "id : uuid",                              "pk"),
                ("act",  "activity_id &#8594; activities",         "fk"),
                ("usr",  "user_id &#8594; users",                  "fk"),
                (None,   "attendance_status",                      "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("activity_checkins", _table_node(
            "activity_checkins", "0",
            [
                ("id",   "id : uuid",                              "pk"),
                ("act",  "activity_id &#8594; activities",         "fk"),
                ("usr",  "user_id &#8594; users",                  "fk"),
                (None,   "distance_meters",                        "col"),
                (None,   "location_verified",                      "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("activity_chat_messages", _table_node(
            "activity_chat_messages", "0",
            [
                ("id",   "id : uuid",                              "pk"),
                ("act",  "activity_id &#8594; activities",         "fk"),
                ("usr",  "user_id &#8594; users",                  "fk"),
                (None,   "content",                                "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Marketplace cluster ----------
    cl = CLUSTERS["marketplace"]
    with g.subgraph(name="cluster_marketplace") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("marketplace_items", _table_node(
            "marketplace_items", "15",
            [
                ("id",     "id : uuid",                            "pk"),
                ("seller", "seller_id &#8594; users",              "fk"),
                (None,     "status (active/sold/removed)",         "col"),
                (None,     "views_count",                          "col"),
                (None,     "favorites_count",                      "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("marketplace_comments", _table_node(
            "marketplace_comments", "0",
            [
                ("id",      "id : uuid",                                 "pk"),
                ("item",    "item_id &#8594; marketplace_items",         "fk"),
                ("usr",     "user_id &#8594; users",                     "fk"),
                ("parent",  "parent_id &#8594; (self)",                  "self_fk"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Groups & Messaging cluster ----------
    cl = CLUSTERS["messaging"]
    with g.subgraph(name="cluster_messaging") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("groups", _table_node(
            "groups", "5",
            [
                ("id",       "id : uuid",                                 "pk"),
                ("creator",  "creator_id &#8594; users",                  "fk"),
                (None,       "group_kind (community/ride_carpool)",       "col"),
                ("ride",     "ride_id &#8594; rides (NULL community)",    "fk"),
                (None,       "chat_expires_at",                           "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("group_members", _table_node(
            "group_members", "10",
            [
                ("id",     "id : uuid",                          "pk"),
                ("group",  "group_id &#8594; groups",            "fk"),
                ("usr",    "user_id &#8594; users",              "fk"),
                (None,     "role",                               "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("group_messages", _table_node(
            "group_messages", "2",
            [
                ("id",     "id : uuid",                                "pk"),
                ("group",  "group_id &#8594; groups",                  "fk"),
                (None,     "sender_id (= auth.uid)",                   "col"),
                (None,     "content",                                  "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("messages", _table_node(
            "messages", "22",
            [
                ("id",     "id : uuid",                       "pk"),
                ("send",   "sender_id &#8594; users",         "fk"),
                ("recv",   "receiver_id &#8594; users",       "fk"),
                (None,     "thread_id",                       "col"),
                (None,     "context_type, context_id",        "col"),
                (None,     "message_type",                    "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("system_messages", _table_node(
            "system_messages", "10",
            [
                ("id",   "id : uuid",                       "pk"),
                ("usr",  "user_id &#8594; users",           "fk"),
                (None,   "sender_type (admin/user)",        "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Cross-module cluster ----------
    cl = CLUSTERS["cross"]
    with g.subgraph(name="cluster_cross") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("notifications", _table_node(
            "notifications", "54",
            [
                ("id",   "id : uuid",                       "pk"),
                ("usr",  "user_id &#8594; users",           "fk"),
                (None,   "type",                            "col"),
                (None,   "data : JSONB",                    "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("point_rules", _table_node(
            "point_rules", "0",
            [
                (None, "(NOT MIGRATED in production)", "note"),
                (None, "schema deferred",              "note"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("point_transactions", _table_node(
            "point_transactions", "&mdash;",
            [
                (None, "(table does not exist)",       "note"),
                (None, "REST returns PGRST205",        "note"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("wxgroup_notice_record", _table_node(
            "wxgroup_notice_record", "82",
            [
                ("id",   "id : uuid",                                "pk"),
                (None,   "content",                                  "col"),
                (None,   "sendtime",                                 "col"),
                (None,   "62 marketplace + 16 ride + 4 activity",    "note"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Foreign-key edges ----------
    # crow on the many-side (child); plain on the one-side (parent).
    edge_attrs = {"arrowhead": "crow", "arrowtail": "none", "dir": "both",
                  "color": "#34495E", "penwidth": "1.0"}

    def fk(child: str, child_port: str, parent: str, parent_port: str = "id",
           style: str | None = None, color: str | None = None,
           label: str | None = None):
        attrs = dict(edge_attrs)
        if style:
            attrs["style"] = style
        if color:
            attrs["color"] = color
        if label:
            attrs["label"] = label
            attrs["fontsize"] = "9"
            attrs["fontcolor"] = attrs["color"]
        g.edge(f"{child}:{child_port}", f"{parent}:{parent_port}", **attrs)

    # Identity links (users is the hub — color-code these so the hub doesn't get cluttered)
    USR = "#1F618D"
    fk("rides", "driver", "users", color=USR)
    fk("ride_bookings", "pax", "users", color=USR)
    fk("ratings", "rater", "users", color=USR)
    fk("ratings", "ratee", "users", color=USR)
    fk("activities", "org", "users", color=USR)
    fk("activity_participants", "usr", "users", color=USR)
    fk("activity_checkins", "usr", "users", color=USR)
    fk("activity_chat_messages", "usr", "users", color=USR)
    fk("marketplace_items", "seller", "users", color=USR)
    fk("marketplace_comments", "usr", "users", color=USR)
    fk("groups", "creator", "users", color=USR)
    fk("group_members", "usr", "users", color=USR)
    fk("messages", "send", "users", color=USR)
    fk("messages", "recv", "users", color=USR)
    fk("system_messages", "usr", "users", color=USR)
    fk("notifications", "usr", "users", color=USR)

    # Carpool links
    CAR = "#922B21"
    fk("ride_bookings", "ride", "rides", color=CAR)
    fk("ratings", "trip", "rides", color=CAR)
    fk("groups", "ride", "rides", color=CAR, style="dashed",
       label="NULL for community")

    # Activities links
    ACT = "#1E8449"
    fk("activity_participants", "act", "activities", color=ACT)
    fk("activity_checkins", "act", "activities", color=ACT)
    fk("activity_chat_messages", "act", "activities", color=ACT)
    fk("activities", "group", "groups", color=ACT, style="dashed")

    # Marketplace links
    MKT = "#B9770E"
    fk("marketplace_comments", "item", "marketplace_items", color=MKT)
    # Self-FK (parent_id) on comments for threading
    g.edge("marketplace_comments:parent", "marketplace_comments:id",
           arrowhead="crow", dir="both", color=MKT, style="dotted",
           label="thread", fontsize="9", fontcolor=MKT)

    # Groups & messaging links
    MSG = "#6C3483"
    fk("group_members", "group", "groups", color=MSG)
    fk("group_messages", "group", "groups", color=MSG)

    pdf, png = render_dot(g, "mbe_a4_db_er_core", dpi=300)
    register("mbe_a4_db_er_core", "ok", png_path=png)
    return pdf, png
