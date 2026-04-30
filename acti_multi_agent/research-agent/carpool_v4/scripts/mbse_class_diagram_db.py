"""mbse_class_diagram_db - UML Class Diagram for the live database schema.

15 classes drawn as UML record-style boxes (class name in the top
compartment, key attributes in the bottom compartment).  Classes are
grouped into 6 visual clusters by domain:

  Identity        : User
  Carpool         : Ride, RideBooking, Rating
  Activities      : Activity, ActivityParticipant, ActivityCheckin
  Marketplace    : MarketplaceItem
  Messaging       : Group, GroupMember, GroupMessage,
                    Message, MessageParticipant
  Cross-module    : Notification, WxgroupNoticeRecord

Associations between classes carry UML multiplicity labels (1, 0..1,
1..*, 0..*).  Self-loops and inheritance are not used (none of the
production tables inherit from another).  Foreign-key direction is
shown with an open diamond (aggregation) end on the owning side.

Source-of-truth:
  campusride-backend/supabase/migrations/000_initial_schema.sql
  + migrations 005-016 (group / message / activity-checkin / wxgroup tables)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import make_digraph, render_dot, register, renderer  # noqa: E402


# Per-cluster fill palette
IDENTITY_FILL = "#FDEBD0"
IDENTITY_BORDER = "#9C640C"
CARPOOL_FILL = "#D6EAF8"
CARPOOL_BORDER = "#1F618D"
ACT_FILL = "#D5F5E3"
ACT_BORDER = "#1E8449"
MKT_FILL = "#FADBD8"
MKT_BORDER = "#922B21"
MSG_FILL = "#E8DAEF"
MSG_BORDER = "#6C3483"
CROSS_FILL = "#FCF3CF"
CROSS_BORDER = "#9A7D0A"

EDGE_COLOR = "#1B2631"


@renderer("mbse_class_diagram_db")
def render():
    g = make_digraph("mbse_class_diagram_db", rankdir="LR")
    g.attr(
        ranksep="1.20", nodesep="0.55", splines="spline", concentrate="false",
        overlap="false",
        label=(
            "Class Diagram - production database schema (snapshot 2026-04-23)\n"
            "15 core classes across 6 domain clusters; UML associations with multiplicity."
        ),
        labelloc="t", fontsize="14",
    )
    g.attr("node", fontname="Helvetica", fontsize="10")
    g.attr("edge", fontname="Helvetica", fontsize="8.5", color=EDGE_COLOR,
           labeldistance="1.6", labelangle="0",
           labelfloat="false")

    # ------------------------------------------------------------------
    # UML record-style class label builder
    # ------------------------------------------------------------------
    def _esc(s: str) -> str:
        # Escape graphviz record-shape special characters
        return (
            s.replace("\\", "\\\\")
             .replace("<", "\\<").replace(">", "\\>")
             .replace("|", "\\|")
             .replace("{", "\\{").replace("}", "\\}")
             .replace("\"", "\\\"")
        )

    def cls_label(name: str, attrs: list[str]) -> str:
        # Graphviz record shape: '{' = vertical stack, '|' = compartment sep,
        # '\l' = left-align newline within a compartment.
        attr_block = "\\l".join(_esc(a) for a in attrs) + "\\l"
        return "{" + _esc(name) + "|" + attr_block + "}"

    def add_class(g_or_c, key, name, attrs, fill, border):
        g_or_c.node(
            key, cls_label(name, attrs),
            shape="record", style="filled",
            fillcolor=fill, color=border, penwidth="1.6",
            fontsize="10",
        )

    # ------------------------------------------------------------------
    # Cluster 1 - Identity
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_identity") as c:
        c.attr(
            label="Identity", style="rounded,filled",
            color=IDENTITY_BORDER, fillcolor="#FEF9E7",
            fontsize="12", fontcolor=IDENTITY_BORDER, penwidth="1.2",
            labeljust="l",
        )
        add_class(
            c, "User", "User",
            [
                "+ id : UUID",
                "+ email : @cornell.edu",
                "+ university : text",
                "+ is_verified : bool",
                "+ points : int",
                "+ avg_rating : numeric",
            ],
            IDENTITY_FILL, IDENTITY_BORDER,
        )

    # ------------------------------------------------------------------
    # Cluster 2 - Carpool
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_carpool") as c:
        c.attr(
            label="Carpool", style="rounded,filled",
            color=CARPOOL_BORDER, fillcolor="#EBF5FB",
            fontsize="12", fontcolor=CARPOOL_BORDER, penwidth="1.2",
            labeljust="l",
        )
        add_class(
            c, "Ride", "Ride",
            [
                "+ id : UUID",
                "+ driver_id : UUID FK",
                "+ departure_time : ts",
                "+ status : enum",
                "+ total_seats : int",
                "+ price : numeric",
            ],
            CARPOOL_FILL, CARPOOL_BORDER,
        )
        add_class(
            c, "RideBooking", "RideBooking",
            [
                "+ id : UUID",
                "+ ride_id : UUID FK",
                "+ rider_id : UUID FK",
                "+ status : enum",
                "+ payment_status : enum",
            ],
            CARPOOL_FILL, CARPOOL_BORDER,
        )
        add_class(
            c, "Rating", "Rating",
            [
                "+ trip_id : UUID FK",
                "+ rater_id : UUID FK",
                "+ ratee_id : UUID FK",
                "+ score : int (1-5)",
                "+ role_of_rater : enum",
            ],
            CARPOOL_FILL, CARPOOL_BORDER,
        )

    # ------------------------------------------------------------------
    # Cluster 3 - Activities
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_activities") as c:
        c.attr(
            label="Activities", style="rounded,filled",
            color=ACT_BORDER, fillcolor="#EAFAF1",
            fontsize="12", fontcolor=ACT_BORDER, penwidth="1.2",
            labeljust="l",
        )
        add_class(
            c, "Activity", "Activity",
            [
                "+ id : UUID",
                "+ organizer_id : UUID FK",
                "+ location_coord : point",
                "+ status : enum",
                "+ checkin_code : text",
            ],
            ACT_FILL, ACT_BORDER,
        )
        add_class(
            c, "ActivityParticipant", "ActivityParticipant",
            [
                "+ activity_id : UUID FK",
                "+ user_id : UUID FK",
                "+ attendance_status : enum",
                "+ payment_status : enum",
            ],
            ACT_FILL, ACT_BORDER,
        )
        add_class(
            c, "ActivityCheckin", "ActivityCheckin",
            [
                "+ id : UUID",
                "+ participant_id : UUID FK",
                "+ location : point",
                "+ location_verified : bool",
                "+ device_info : json",
            ],
            ACT_FILL, ACT_BORDER,
        )

    # ------------------------------------------------------------------
    # Cluster 4 - Marketplace
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_marketplace") as c:
        c.attr(
            label="Marketplace", style="rounded,filled",
            color=MKT_BORDER, fillcolor="#FDEDEC",
            fontsize="12", fontcolor=MKT_BORDER, penwidth="1.2",
            labeljust="l",
        )
        add_class(
            c, "MarketplaceItem", "MarketplaceItem",
            [
                "+ id : UUID",
                "+ seller_id : UUID FK",
                "+ status : enum",
                "+ price : numeric",
                "+ views_count : int",
            ],
            MKT_FILL, MKT_BORDER,
        )

    # ------------------------------------------------------------------
    # Cluster 5 - Messaging
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_messaging") as c:
        c.attr(
            label="Messaging  (groups + DMs)", style="rounded,filled",
            color=MSG_BORDER, fillcolor="#F4ECF7",
            fontsize="12", fontcolor=MSG_BORDER, penwidth="1.2",
            labeljust="l",
        )
        add_class(
            c, "Group", "Group",
            [
                "+ id : UUID",
                "+ group_kind : enum",
                "+ ride_id : UUID FK?",
                "+ chat_expires_at : ts",
                "+ member_count : int",
            ],
            MSG_FILL, MSG_BORDER,
        )
        add_class(
            c, "GroupMember", "GroupMember",
            [
                "+ group_id : UUID FK",
                "+ user_id : UUID FK",
                "+ role : enum",
            ],
            MSG_FILL, MSG_BORDER,
        )
        add_class(
            c, "GroupMessage", "GroupMessage",
            [
                "+ id : UUID",
                "+ group_id : UUID FK",
                "+ sender_id : UUID FK",
                "+ content : text",
                "+ deleted_at : ts?",
            ],
            MSG_FILL, MSG_BORDER,
        )
        add_class(
            c, "Message", "Message",
            [
                "+ id : UUID",
                "+ sender_id : UUID FK",
                "+ receiver_id : UUID FK",
                "+ context_type : enum",
                "+ context_id : UUID",
                "+ thread_id : UUID",
            ],
            MSG_FILL, MSG_BORDER,
        )
        add_class(
            c, "MessageParticipant", "MessageParticipant",
            [
                "+ message_id : UUID FK",
                "+ user_id : UUID FK",
                "+ is_read : bool",
                "+ archived : bool",
            ],
            MSG_FILL, MSG_BORDER,
        )

    # ------------------------------------------------------------------
    # Cluster 6 - Cross-module
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_crossmod") as c:
        c.attr(
            label="Cross-module", style="rounded,filled",
            color=CROSS_BORDER, fillcolor="#FEF9E7",
            fontsize="12", fontcolor=CROSS_BORDER, penwidth="1.2",
            labeljust="l",
        )
        add_class(
            c, "Notification", "Notification",
            [
                "+ id : UUID",
                "+ recipient_id : UUID FK",
                "+ type : enum",
                "+ priority : enum",
                "+ data : jsonb",
                "+ is_read : bool",
            ],
            CROSS_FILL, CROSS_BORDER,
        )
        add_class(
            c, "WxgroupNoticeRecord", "WxgroupNoticeRecord",
            [
                "+ id : UUID",
                "+ source_type : enum",
                "+ source_id : UUID",
                "+ dispatch_status : enum",
                "+ link_url : text",
            ],
            CROSS_FILL, CROSS_BORDER,
        )

    # ------------------------------------------------------------------
    # Associations (UML labelled edges with multiplicity)
    # arrowhead = "odiamond" expresses aggregation (the "owning" side)
    # ------------------------------------------------------------------
    def assoc(src, dst, lbl, *, src_mult="", dst_mult="",
              owner="src", style="solid", color=EDGE_COLOR):
        head = "odiamond" if owner == "dst" else "vee"
        tail = "odiamond" if owner == "src" else "none"
        g.edge(
            src, dst, label=lbl,
            taillabel=src_mult, headlabel=dst_mult,
            arrowhead=head, arrowtail=tail, dir="both",
            style=style, color=color, fontcolor=color,
            penwidth="1.1", labeldistance="2.4", labelangle="22",
        )

    # User <-> Ride (driver)
    assoc("User", "Ride", "drives",
          src_mult="1", dst_mult="0..*", owner="src")
    # User <-> RideBooking (rider)
    assoc("User", "RideBooking", "books",
          src_mult="1", dst_mult="0..*", owner="src")
    # Ride <-> RideBooking
    assoc("Ride", "RideBooking", "has",
          src_mult="1", dst_mult="0..*", owner="src")
    # Ride <-> Rating (trip_id)
    assoc("Ride", "Rating", "yields",
          src_mult="1", dst_mult="0..*", owner="src")
    # User <-> Rating (rater + ratee, summarised as one association)
    assoc("User", "Rating", "rates / is rated",
          src_mult="2", dst_mult="0..*", owner="src")

    # User <-> Activity
    assoc("User", "Activity", "organises",
          src_mult="1", dst_mult="0..*", owner="src")
    # Activity <-> ActivityParticipant
    assoc("Activity", "ActivityParticipant", "registers",
          src_mult="1", dst_mult="0..*", owner="src")
    # User -> ActivityParticipant omitted to reduce User-as-hub clutter
    # (User-Activity participation is transitive via Activity-ActivityParticipant).
    # ActivityParticipant <-> ActivityCheckin
    assoc("ActivityParticipant", "ActivityCheckin", "checks in",
          src_mult="1", dst_mult="0..*", owner="src")

    # User <-> MarketplaceItem
    assoc("User", "MarketplaceItem", "lists",
          src_mult="1", dst_mult="0..*", owner="src")

    # Group <-> GroupMember
    assoc("Group", "GroupMember", "contains",
          src_mult="1", dst_mult="0..*", owner="src")
    # User <-> GroupMember
    assoc("User", "GroupMember", "member of",
          src_mult="1", dst_mult="0..*", owner="src")
    # Group <-> GroupMessage
    assoc("Group", "GroupMessage", "carries",
          src_mult="1", dst_mult="0..*", owner="src")
    # User -> GroupMessage (sender) intentionally omitted to reduce
    # User-as-hub clutter; "member of" already records the User-Group relation.
    # Ride <-> Group (ride_carpool kind)
    assoc("Ride", "Group", "spawns ride_carpool",
          src_mult="1", dst_mult="0..1", owner="src",
          style="dashed", color="#7D6608")

    # Message + MessageParticipant
    assoc("User", "Message", "sends DM",
          src_mult="1", dst_mult="0..*", owner="src")
    assoc("Message", "MessageParticipant", "addressed to",
          src_mult="1", dst_mult="1..*", owner="src")
    # User -> MessageParticipant omitted (is_read flag is the only payload;
    # transitive via Message.sender_id keeps the diagram less crowded).

    # Notification (recipient = User)
    assoc("User", "Notification", "receives",
          src_mult="1", dst_mult="0..*", owner="src")

    # Wxgroup notice references source rows polymorphically via
    # (source_type, source_id).  Render a single annotated note instead
    # of three near-identical dashed edges (which would crowd the layout).
    g.node(
        "wx_note",
        "polymorphic association:\n"
        "(source_type, source_id) -> Ride / MarketplaceItem / Activity\n"
        "snapshot 2026-04-23: 16 ride / 62 mkt / 4 act = 82",
        shape="note", style="filled", fillcolor="#FEF9E7",
        color=CROSS_BORDER, fontcolor=CROSS_BORDER, fontsize="9",
    )
    g.edge("WxgroupNoticeRecord", "wx_note",
           style="dashed", color=CROSS_BORDER, arrowhead="none",
           constraint="false")

    pdf, png = render_dot(g, "mbse_class_diagram_db")
    register("mbse_class_diagram_db", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
