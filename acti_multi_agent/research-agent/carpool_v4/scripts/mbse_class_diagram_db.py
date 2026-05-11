"""mbse_class_diagram_db - Class diagram of the production database schema.

Fifteen classes drawn as Graphviz HTML-table nodes, grouped into six
domain clusters: Identity, Carpool, Activities, Marketplace, Messaging,
and Cross-module. Each class shows its name and the key columns that
are load-bearing for the design — primary keys are bold "id", foreign
keys are italic and read in natural English ("driver -> users"). SQL
types (UUID, text, JSONB), engineering-only fields, and database
internals are stripped for HCI/CHI readers.

Style: per `_mbe_style_guide.md` §4 (ER / class diagram row), graphviz
HTML-table nodes are acceptable for true class / ER diagrams. Strong
precedent: `mbe_a4_db_er_core.py` — this figure matches its conventions.
The points ledger and the wxgroup notice queue are annotated with the
design-language phrase "not yet provisioned in production".
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import make_digraph, render_dot, register, renderer  # noqa: E402


# Per-cluster header colors (light pastel fill + matching dark border)
CLUSTERS = {
    "identity":    {"fill": "#D6EAF8", "border": "#1F618D", "label": "Identity"},
    "carpool":     {"fill": "#FADBD8", "border": "#922B21", "label": "Carpool"},
    "activities":  {"fill": "#D5F5E3", "border": "#1E8449", "label": "Activities"},
    "marketplace": {"fill": "#FAE5D3", "border": "#B9770E", "label": "Marketplace"},
    "messaging":   {"fill": "#E8DAEF", "border": "#6C3483", "label": "Messaging"},
    "cross":       {"fill": "#FCF3CF", "border": "#9A7D0A", "label": "Cross-module"},
}

# Navy edge color (per style guide)
EDGE_COLOR = "#1A5276"


def _row(text: str, port: str | None = None, italic: bool = False,
         bold: bool = False, color: str | None = None) -> str:
    """Build one HTML <TR><TD>...</TD></TR> row of a class node."""
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


def _class_node(name: str, columns: list[tuple[str, str, str]],
                fill: str, border: str) -> str:
    """Return an HTML-like label for a class.

    columns: list of (port, text, role) where role in {pk, fk, self_fk, col, note}.
    """
    header = (
        f'<TR><TD BGCOLOR="{fill}" ALIGN="CENTER">'
        f'<B>{name}</B></TD></TR>'
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


@renderer("mbse_class_diagram_db")
def render():
    g = make_digraph("mbse_class_diagram_db", rankdir="TB")
    g.attr(splines="spline", nodesep="0.45", ranksep="0.8", concentrate="false",
           label=("CampusRide class diagram — 15 classes across six domain "
                  "clusters (snapshot 2026-04-23)"),
           labelloc="t", fontsize="14")
    g.attr("node", shape="plaintext", style="", fontname="Helvetica",
           fontsize="10")

    # ---------- Identity cluster ----------
    cl = CLUSTERS["identity"]
    with g.subgraph(name="cluster_identity") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("User", _class_node(
            "User",
            [
                ("id",   "id",                              "pk"),
                (None,   "email (Cornell address)",         "col"),
                (None,   "university",                      "col"),
                (None,   "verified status",                 "col"),
                (None,   "average rating",                  "col"),
                (None,   "points balance",                  "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Carpool cluster ----------
    cl = CLUSTERS["carpool"]
    with g.subgraph(name="cluster_carpool") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("Ride", _class_node(
            "Ride",
            [
                ("id",     "id",                                          "pk"),
                ("driver", "driver &#8594; users",                          "fk"),
                (None,     "departure time",                              "col"),
                (None,     "seats remaining",                             "col"),
                (None,     "status (active / full / completed / cancelled)", "col"),
                (None,     "fare per seat",                               "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("RideBooking", _class_node(
            "RideBooking",
            [
                ("id",     "id",                              "pk"),
                ("ride",   "ride &#8594; rides",                   "fk"),
                ("rider",  "rider &#8594; users",                  "fk"),
                (None,     "status (confirmed / cancelled)",  "col"),
                (None,     "payment status",                  "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("Rating", _class_node(
            "Rating",
            [
                ("id",     "id",                              "pk"),
                ("trip",   "trip &#8594; rides",                   "fk"),
                ("rater",  "rater &#8594; users",                  "fk"),
                ("ratee",  "ratee &#8594; users",                  "fk"),
                (None,     "rater role (driver / passenger)", "col"),
                (None,     "score (1-5)",                     "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Activities cluster ----------
    cl = CLUSTERS["activities"]
    with g.subgraph(name="cluster_activities") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("Activity", _class_node(
            "Activity",
            [
                ("id",     "id",                                          "pk"),
                ("org",    "organizer &#8594; users",                          "fk"),
                (None,     "venue coordinates",                           "col"),
                (None,     "status (draft / published / ongoing / done)", "col"),
                (None,     "check-in code",                               "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("ActivityParticipant", _class_node(
            "ActivityParticipant",
            [
                ("id",   "id",                          "pk"),
                ("act",  "activity &#8594; activities",      "fk"),
                ("usr",  "user &#8594; users",               "fk"),
                (None,   "attendance status",           "col"),
                (None,   "payment status",              "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("ActivityCheckin", _class_node(
            "ActivityCheckin",
            [
                ("id",   "id",                          "pk"),
                ("part", "participant &#8594; participants", "fk"),
                (None,   "distance to venue",           "col"),
                (None,   "location verified",           "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Marketplace cluster ----------
    cl = CLUSTERS["marketplace"]
    with g.subgraph(name="cluster_marketplace") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("MarketplaceItem", _class_node(
            "MarketplaceItem",
            [
                ("id",     "id",                                  "pk"),
                ("seller", "seller &#8594; users",                     "fk"),
                (None,     "status (active / sold / removed)",    "col"),
                (None,     "price",                               "col"),
                (None,     "view count",                          "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Messaging cluster ----------
    cl = CLUSTERS["messaging"]
    with g.subgraph(name="cluster_messaging") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("Group", _class_node(
            "Group",
            [
                ("id",       "id",                                       "pk"),
                ("creator",  "creator &#8594; users",                         "fk"),
                (None,       "kind (community / ride-bound)",            "col"),
                ("ride",     "ride &#8594; rides (null for community)",       "fk"),
                (None,       "chat expires at",                          "col"),
                (None,       "member count",                             "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("GroupMember", _class_node(
            "GroupMember",
            [
                ("id",     "id",                       "pk"),
                ("group",  "group &#8594; groups",          "fk"),
                ("usr",    "user &#8594; users",            "fk"),
                (None,     "role",                     "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("GroupMessage", _class_node(
            "GroupMessage",
            [
                ("id",     "id",                       "pk"),
                ("group",  "group &#8594; groups",          "fk"),
                ("send",   "sender &#8594; users",          "fk"),
                (None,     "content",                  "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("Message", _class_node(
            "Message",
            [
                ("id",     "id",                       "pk"),
                ("send",   "sender &#8594; users",          "fk"),
                ("recv",   "receiver &#8594; users",        "fk"),
                (None,     "thread",                   "col"),
                (None,     "context (type, id)",       "col"),
                (None,     "message type",             "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("MessageParticipant", _class_node(
            "MessageParticipant",
            [
                ("id",   "id",                          "pk"),
                ("msg",  "message &#8594; messages",         "fk"),
                ("usr",  "user &#8594; users",               "fk"),
                (None,   "read flag",                   "col"),
                (None,   "archived flag",               "col"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Cross-module cluster ----------
    cl = CLUSTERS["cross"]
    with g.subgraph(name="cluster_cross") as c:
        c.attr(label=cl["label"], style="rounded,filled",
               color=cl["border"], fillcolor=cl["fill"], penwidth="1.4",
               fontsize="12")
        c.node("Notification", _class_node(
            "Notification",
            [
                ("id",   "id",                          "pk"),
                ("usr",  "recipient &#8594; users",          "fk"),
                (None,   "type",                        "col"),
                (None,   "priority",                    "col"),
                (None,   "payload",                     "col"),
                (None,   "read flag",                   "col"),
            ],
            fill=cl["fill"], border=cl["border"]))
        c.node("WxgroupNoticeRecord", _class_node(
            "WxgroupNoticeRecord",
            [
                ("id",   "id",                                       "pk"),
                (None,   "source kind (ride / item / activity)",     "col"),
                (None,   "source reference",                         "col"),
                (None,   "dispatch status",                          "col"),
                (None,   "external link",                            "col"),
                (None,   "not yet provisioned in production",        "note"),
            ],
            fill=cl["fill"], border=cl["border"]))

    # ---------- Association edges ----------
    # Color edges by parent cluster so the diagram reads as colored bundles
    # rather than a navy spaghetti. User-as-hub edges share the Identity
    # navy; intra-cluster edges share the cluster border color.
    edge_attrs = {"arrowhead": "crow", "arrowtail": "none", "dir": "both",
                  "penwidth": "1.0"}

    def fk(child: str, child_port: str, parent: str, parent_port: str = "id",
           style: str | None = None, color: str = EDGE_COLOR,
           label: str | None = None):
        attrs = dict(edge_attrs)
        attrs["color"] = color
        if style:
            attrs["style"] = style
        if label:
            attrs["label"] = label
            attrs["fontsize"] = "9"
            attrs["fontcolor"] = color
        g.edge(f"{child}:{child_port}", f"{parent}:{parent_port}", **attrs)

    # Identity hub - User is referenced by everyone (navy bundle)
    USR = CLUSTERS["identity"]["border"]
    fk("Ride", "driver", "User", color=USR)
    fk("RideBooking", "rider", "User", color=USR)
    fk("Rating", "rater", "User", color=USR)
    fk("Rating", "ratee", "User", color=USR)
    fk("Activity", "org", "User", color=USR)
    fk("ActivityParticipant", "usr", "User", color=USR)
    fk("MarketplaceItem", "seller", "User", color=USR)
    fk("Group", "creator", "User", color=USR)
    fk("GroupMember", "usr", "User", color=USR)
    fk("GroupMessage", "send", "User", color=USR)
    fk("Message", "send", "User", color=USR)
    fk("Message", "recv", "User", color=USR)
    fk("MessageParticipant", "usr", "User", color=USR)
    fk("Notification", "usr", "User", color=USR)

    # Carpool internal links (red bundle)
    CAR = CLUSTERS["carpool"]["border"]
    fk("RideBooking", "ride", "Ride", color=CAR)
    fk("Rating", "trip", "Ride", color=CAR)
    fk("Group", "ride", "Ride", color=CAR, style="dashed",
       label="ride-bound only")

    # Activities internal links (green bundle)
    ACT = CLUSTERS["activities"]["border"]
    fk("ActivityParticipant", "act", "Activity", color=ACT)
    fk("ActivityCheckin", "part", "ActivityParticipant", color=ACT)

    # Messaging internal links (purple bundle)
    MSG = CLUSTERS["messaging"]["border"]
    fk("GroupMember", "group", "Group", color=MSG)
    fk("GroupMessage", "group", "Group", color=MSG)
    fk("MessageParticipant", "msg", "Message", color=MSG)

    pdf, png = render_dot(g, "mbse_class_diagram_db", dpi=300)
    register("mbse_class_diagram_db", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
