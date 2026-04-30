"""mbe_c4 — Geo-Verified Activity Check-in Pipeline.

Vertical (TB) pipeline for activity check-in flow with location verification.
Source-of-truth:
  campusride-backend/src/services/activity-checkin.service.js:31-191

Pipeline stages (top to bottom):
  1) Client POST request
  2) canUserCheckin guard (line 31)
  3) is_checkin_period time-window guard (Postgres function)
  4) location_verification branch (decision diamond)
  5) calculate_distance Haversine RPC + radius check
  6) INSERT activity_checkins
  7) UPDATE activity_participants
  8) awardPoints -> point_transactions + increment_user_points RPC
  9) PL/pgSQL trigger update_activity_participant_count

Color legend:
  - Service-call: light blue
  - DB INSERT/UPDATE: light green
  - Decision diamond: yellow
  - Guard rejections (red dashed)
  - RPC: orange
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import renderer, make_digraph, render_dot, register  # noqa: E402


# Palette ---------------------------------------------------------------------
SVC_FILL = "#D6EAF8"      # light blue
SVC_BORDER = "#1F618D"

DB_FILL = "#D5F5E3"       # light green
DB_BORDER = "#1E8449"

DEC_FILL = "#FCF3CF"      # yellow
DEC_BORDER = "#B7950B"

RPC_FILL = "#FAE5D3"      # orange
RPC_BORDER = "#B9540B"

REJ_COLOR = "#C0392B"     # red (dashed) — guard rejections

CLIENT_FILL = "#E8DAEF"
CLIENT_BORDER = "#6C3483"

ANNOT_FILL = "#FBFCFC"
ANNOT_BORDER = "#566573"


@renderer("mbe_c4_geo_checkin_pipeline")
def render():
    g = make_digraph("c4_geo_checkin", rankdir="TB")
    g.attr(
        nodesep="0.35", ranksep="0.55", splines="spline",
        label=(
            "Geo-Verified Activity Check-in Pipeline  "
            "(services/activity-checkin.service.js:31-191)"
        ),
        labelloc="t", fontsize="14", fontname="Helvetica-Bold",
    )
    g.attr("node", fontsize="10")
    g.attr("edge", fontsize="9")

    # 1) Client request
    g.node(
        "client",
        label=(
            "<<B>1. Client</B><BR/>"
            "POST /api/v1/activities/checkin<BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "body: { activity_id,<BR/>"
            "  user_location: { latitude, longitude, accuracy } }"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=CLIENT_FILL, color=CLIENT_BORDER, penwidth="1.6",
    )

    # 2) canUserCheckin guard
    g.node(
        "guard_can_checkin",
        label=(
            "<<B>2. canUserCheckin guard</B>"
            "<FONT POINT-SIZE=\"9\"> [line 31]</FONT><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "activity.checkin_enabled = true<BR/>"
            "activity.status IN ('ongoing','published','upcoming')<BR/>"
            "user has activity_participants row<BR/>"
            "user not already checked_in"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=SVC_FILL, color=SVC_BORDER, penwidth="1.4",
    )

    # 3) is_checkin_period (time window) guard
    g.node(
        "guard_time",
        label=(
            "<<B>3. is_checkin_period guard</B>"
            "<FONT POINT-SIZE=\"9\"> [Postgres fn]</FONT><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "checkin_start = start_time - checkin_start_offset (def 30 min)<BR/>"
            "checkin_end   = end_time   + checkin_end_offset   (def 30 min)"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=SVC_FILL, color=SVC_BORDER, penwidth="1.4",
    )

    # 4) Decision diamond — location_verification branch
    g.node(
        "branch_loc",
        label=(
            "4. activity.location_verification ?"
        ),
        shape="diamond", style="filled",
        fillcolor=DEC_FILL, color=DEC_BORDER, penwidth="1.8",
        height="1.0", width="3.0", fixedsize="false",
        margin="0.18",
    )

    # 5) Haversine RPC distance check
    g.node(
        "rpc_distance",
        label=(
            "<<B>5. calculate_distance RPC</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "Supabase RPC (Haversine)<BR/>"
            "calculate_distance(lat1, lon1, lat2, lon2)<BR/>"
            "compare to verification_radius<BR/>"
            "(default 100m, from activity.max_checkin_distance)<BR/>"
            "if distance &gt; radius: error { distance_meters }<BR/>"
            "else: location_verified = true"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=RPC_FILL, color=RPC_BORDER, penwidth="1.6",
    )

    # 6) INSERT activity_checkins
    g.node(
        "db_insert_checkin",
        label=(
            "<<B>6. INSERT activity_checkins</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "(activity_id, user_id, participation_id, checkin_time,<BR/>"
            "user_location JSONB, activity_location JSONB,<BR/>"
            "distance_meters, location_verified, verification_radius,<BR/>"
            "device_info JSONB, ip_address)"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
    )

    # 7) UPDATE activity_participants
    g.node(
        "db_update_part",
        label=(
            "<<B>7. UPDATE activity_participants</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "SET attendance_status='checked_in',<BR/>"
            "checkin_time = NOW(), checked_in = true"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
    )

    # 8) Award points — service + RPC
    g.node(
        "svc_award",
        label=(
            "<<B>8. awardPoints()</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "{ user_id, ruleType: 'activity_checkin', points: 5 }<BR/>"
            "INSERT point_transactions"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=SVC_FILL, color=SVC_BORDER, penwidth="1.4",
    )
    g.node(
        "rpc_increment",
        label=(
            "<<B>increment_user_points RPC</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "atomic balance += 5"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=RPC_FILL, color=RPC_BORDER, penwidth="1.4",
    )

    # 9) Trigger
    g.node(
        "trigger",
        label=(
            "<<B>9. Trigger update_activity_participant_count</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "PL/pgSQL: keeps activities.current_participants in sync<BR/>"
            "(decrement out of 'registered'; no-op increment-side here<BR/>"
            "since user transitioned out, not in)"
            "</FONT>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
    )

    # Reject sink (403)
    g.node(
        "reject_403",
        label="403 Forbidden",
        shape="octagon", style="filled",
        fillcolor="#FADBD8", color=REJ_COLOR, penwidth="1.4",
        fontcolor=REJ_COLOR, fontname="Helvetica-Bold",
    )
    # Reject sink (distance exceeded)
    g.node(
        "reject_distance",
        label=(
            "<<B>error</B><BR/>"
            "<FONT POINT-SIZE=\"9\">"
            "{ distance_meters } returned<BR/>"
            "for client display"
            "</FONT>>"
        ),
        shape="octagon", style="filled",
        fillcolor="#FADBD8", color=REJ_COLOR, penwidth="1.4",
        fontcolor=REJ_COLOR,
    )

    # Side annotations
    g.node(
        "annot_forensic",
        label=(
            "Spoof attempts leave a forensic\\l"
            "trail in device_info + ip_address\\l"
        ),
        shape="note", style="filled",
        fillcolor="#FEF9E7", color=ANNOT_BORDER, fontsize="9",
    )
    g.node(
        "annot_reuse",
        label=(
            "Same Haversine primitive available for\\l"
            "rideshare pickup-point verification\\l"
            "(mbe_c1 reuse)\\l"
        ),
        shape="note", style="filled",
        fillcolor="#FEF9E7", color=ANNOT_BORDER, fontsize="9",
    )

    # Snapshot footer
    g.node(
        "footer",
        label=(
            "<<I>2026-04-23 snapshot: 0 activity_checkins rows; "
            "4 historical activity_registered notifications attest to a "
            "Feb 2026 activity run whose<BR/>transactional rows have since been "
            "cleaned.</I>>"
        ),
        shape="box", style="rounded,filled",
        fillcolor=ANNOT_FILL, color=ANNOT_BORDER, penwidth="1.0",
        fontsize="10", margin="0.18",
    )

    # ---- Edges (main happy path) -------------------------------------------
    g.edge("client", "guard_can_checkin", color=SVC_BORDER, arrowhead="vee")
    g.edge("guard_can_checkin", "guard_time", color=SVC_BORDER, arrowhead="vee")
    g.edge("guard_time", "branch_loc", color=SVC_BORDER, arrowhead="vee")

    # Branch — yes (verify location) -> RPC
    g.edge("branch_loc", "rpc_distance",
           label="true: verify",
           color=DEC_BORDER, fontcolor=DEC_BORDER, arrowhead="vee")
    # Branch — false (skip) -> straight to insert
    g.edge("branch_loc", "db_insert_checkin",
           label="false: skip",
           color=DEC_BORDER, fontcolor=DEC_BORDER,
           style="dashed", arrowhead="vee", constraint="false")

    # RPC -> insert (within radius)
    g.edge("rpc_distance", "db_insert_checkin",
           label="distance <= radius",
           color=RPC_BORDER, fontcolor=RPC_BORDER, arrowhead="vee")

    # Continue main chain
    g.edge("db_insert_checkin", "db_update_part",
           color=DB_BORDER, arrowhead="vee")
    g.edge("db_update_part", "svc_award", color=DB_BORDER, arrowhead="vee")
    g.edge("svc_award", "rpc_increment", color=SVC_BORDER, arrowhead="vee")
    g.edge("rpc_increment", "trigger", color=RPC_BORDER, arrowhead="vee")

    # ---- Reject edges (red dashed) -----------------------------------------
    g.edge("guard_can_checkin", "reject_403",
           label="fail",
           color=REJ_COLOR, fontcolor=REJ_COLOR,
           style="dashed", arrowhead="vee", constraint="false")
    g.edge("guard_time", "reject_403",
           label="out of window",
           color=REJ_COLOR, fontcolor=REJ_COLOR,
           style="dashed", arrowhead="vee", constraint="false")
    g.edge("rpc_distance", "reject_distance",
           label="distance > radius",
           color=REJ_COLOR, fontcolor=REJ_COLOR,
           style="dashed", arrowhead="vee", constraint="false")

    # ---- Side annotations (non-constraint) ---------------------------------
    g.edge("db_insert_checkin", "annot_forensic",
           style="dotted", color=ANNOT_BORDER, arrowhead="none",
           constraint="false")
    g.edge("rpc_distance", "annot_reuse",
           style="dotted", color=ANNOT_BORDER, arrowhead="none",
           constraint="false")

    # Footer anchored below trigger (invisible edge to keep it last)
    g.edge("trigger", "footer", style="invis")

    pdf, png = render_dot(g, "mbe_c4_geo_checkin_pipeline", dpi=300)
    register("mbe_c4_geo_checkin_pipeline", "ok", png_path=png)
    print(f"  pdf -> {pdf}")
    print(f"  png -> {png}")


if __name__ == "__main__":
    render()
