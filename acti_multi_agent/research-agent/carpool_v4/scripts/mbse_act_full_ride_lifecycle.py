"""mbse_act_full_ride_lifecycle — Full activity diagram for createRide -> completeRide.

Single-lane vertical activity diagram (with branches & decisions).  Visual
distinction between deployed-and-exercised (green fill, solid border) and
designed-but-uninstrumented (light grey fill, dashed border) elements.

Source-of-truth:
  campusride-backend/src/controllers/carpooling.controller.js
    createRide  ~ line 60-172
    bookRide    ~ line 511-709
    completeRide ~ line 875-960
  campusride-backend/src/controllers/rating.controller.js
    RATING_READY_DELAY_MS = 2 * 60 * 60 * 1000
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _mbe_helpers import make_digraph, render_dot, register, renderer  # noqa: E402


# Deployed = #2ECC71 fill; designed-only = #ECF0F1 with dashed border
DEPLOYED_FILL = "#ABEBC6"
DEPLOYED_BORDER = "#1E8449"
DESIGNED_FILL = "#ECF0F1"
DESIGNED_BORDER = "#7B7D7D"
DECISION_FILL = "#FCF3CF"
DECISION_BORDER = "#9A7D0A"
DESIGNED_DEC_FILL = "#F2F3F4"
DESIGNED_DEC_BORDER = "#7B7D7D"
ACTION_BORDER = "#1E8449"


@renderer("mbse_act_full_ride_lifecycle")
def render():
    g = make_digraph("mbse_full_ride_lifecycle", rankdir="TB")
    g.attr(
        ranksep="0.45", nodesep="0.45", splines="spline",
        label=(
            "Full ride lifecycle activity diagram  "
            "(createRide -> bookRide -> completeRide)"
        ),
        labelloc="t", fontsize="14",
    )
    g.attr("node", fontsize="10", fontname="Helvetica")
    g.attr("edge", fontsize="9")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def deployed(name, label, shape="box"):
        g.node(name, label,
               shape=shape, style="rounded,filled",
               fillcolor=DEPLOYED_FILL, color=DEPLOYED_BORDER,
               penwidth="1.4")

    def designed(name, label, shape="box"):
        # Dashed outline + grey fill
        style = "rounded,filled,dashed" if shape == "box" else "filled,dashed"
        g.node(name, label,
               shape=shape, style=style,
               fillcolor=DESIGNED_FILL, color=DESIGNED_BORDER,
               penwidth="1.4", fontcolor="#566573")

    def decision(name, label, designed_only=False):
        fc = DESIGNED_DEC_FILL if designed_only else DECISION_FILL
        bc = DESIGNED_DEC_BORDER if designed_only else DECISION_BORDER
        style = "filled,dashed" if designed_only else "filled"
        g.node(name, label,
               shape="diamond", style=style,
               fillcolor=fc, color=bc, penwidth="1.4",
               fontsize="9", height="1.2", width="2.0", fixedsize="true",
               fontcolor="#566573" if designed_only else "#1B2631")

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------
    # Start
    g.node("start", "", shape="circle", style="filled",
           fillcolor="#1B2631", color="#1B2631",
           width="0.30", height="0.30", fixedsize="true")

    deployed("create",
             "Driver: createRide()\nPOST /carpooling/rides")
    deployed("ins_rides", "INSERT rides\n(status='active')")
    deployed("ins_wx",
             "INSERT wxgroup_notice_record\n(WeChat outreach\n– 16 pushes / snapshot)")

    deployed("browse",
             "Riders: search / browse rides\nGET /carpooling/rides")
    deployed("book", "Rider: bookRide()\nPOST .../rides/:id/book")

    decision("dec_seats", "seats > 0?")

    deployed("ins_book",
             "INSERT ride_bookings\n(status='confirmed')")
    deployed("notif_fan",
             "Notification fan-out\n(6 sendNotification +\n6 socket.emit)")
    deployed("ensure_grp",
             "ensureRideCarpoolGroup\nOnBooking(...)\n(auto-create chat)")

    deployed("departure", "Departure time reached")

    deployed("delay_2h",
             "2h delay timer\n(RATING_READY_DELAY_MS\n= 2 * 60 * 60 * 1000 ms)")

    decision("dec_rating", "rating window\nopen?")
    designed("rate_submit",
             "Both submit rating\n(designed; ratings table\nhas 0 rows in production)")
    deployed("rate_skip", "Skip rating")

    decision("dec_sos", "SOS triggered?", designed_only=True)
    designed("sos_fan",
             "High-priority notification\nfan-out + emergency contacts\n(designed; 0 invocations)")

    deployed("complete",
             "Driver: completeRide()\nUPDATE rides\nSET status='completed'")
    deployed("recompute_avg",
             "Recompute users.avg_rating\n(only fires if ratings exist)")

    designed("award_pts",
             "Award points\n(designed; point_rules=0 rows /\npoint_transactions table missing)")

    g.node("end", "", shape="doublecircle", style="filled",
           fillcolor="#1B2631", color="#1B2631",
           width="0.30", height="0.30", fixedsize="true")

    # Booking-failure end (seats == 0)
    designed("book_fail",
             "Reject (400):\n'No seats available'")

    # ------------------------------------------------------------------
    # Edges (main flow)
    # ------------------------------------------------------------------
    g.edge("start", "create", color=DEPLOYED_BORDER)
    g.edge("create", "ins_rides", color=DEPLOYED_BORDER)
    g.edge("ins_rides", "ins_wx", color=DEPLOYED_BORDER)
    g.edge("ins_wx", "browse", color=DEPLOYED_BORDER)
    g.edge("browse", "book", color=DEPLOYED_BORDER)
    g.edge("book", "dec_seats", color=DEPLOYED_BORDER)

    g.edge("dec_seats", "ins_book",
           label="Yes", color=DEPLOYED_BORDER, fontcolor=DEPLOYED_BORDER)
    g.edge("dec_seats", "book_fail",
           label="No", color=DESIGNED_BORDER, fontcolor=DESIGNED_BORDER,
           style="dashed")

    g.edge("ins_book", "notif_fan", color=DEPLOYED_BORDER)
    g.edge("notif_fan", "ensure_grp", color=DEPLOYED_BORDER)
    g.edge("ensure_grp", "departure", color=DEPLOYED_BORDER)
    g.edge("departure", "delay_2h", color=DEPLOYED_BORDER)
    g.edge("delay_2h", "dec_rating", color=DEPLOYED_BORDER)

    g.edge("dec_rating", "rate_submit",
           label="Yes", color=DESIGNED_BORDER, fontcolor=DESIGNED_BORDER,
           style="dashed")
    g.edge("dec_rating", "rate_skip",
           label="No", color=DEPLOYED_BORDER, fontcolor=DEPLOYED_BORDER)

    g.edge("rate_submit", "dec_sos",
           color=DEPLOYED_BORDER, style="dashed")
    g.edge("rate_skip", "dec_sos", color=DEPLOYED_BORDER)

    g.edge("dec_sos", "sos_fan",
           label="Yes", color=DESIGNED_BORDER, fontcolor=DESIGNED_BORDER,
           style="dashed")
    g.edge("dec_sos", "complete",
           label="No", color=DEPLOYED_BORDER, fontcolor=DEPLOYED_BORDER)
    g.edge("sos_fan", "complete",
           color=DESIGNED_BORDER, style="dashed")

    g.edge("complete", "recompute_avg", color=DEPLOYED_BORDER)
    g.edge("recompute_avg", "award_pts",
           color=DESIGNED_BORDER, style="dashed")
    g.edge("award_pts", "end",
           color=DESIGNED_BORDER, style="dashed")

    # Booking-fail goes to end (alternate terminator)
    g.edge("book_fail", "end",
           color=DESIGNED_BORDER, style="dashed", constraint="false")

    # ------------------------------------------------------------------
    # Legend (cluster, off the main flow)
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_legend") as c:
        c.attr(
            label="Legend", style="rounded,filled",
            color="#566573", fillcolor="#FBFCFC",
            fontsize="11", penwidth="1.2", labeljust="l", labelloc="t",
        )
        c.node("legend_dep",
               "Deployed & exercised",
               shape="box", style="rounded,filled",
               fillcolor=DEPLOYED_FILL, color=DEPLOYED_BORDER, penwidth="1.4",
               fontsize="9.5")
        c.node("legend_des",
               "Designed only;\nuninstrumented in production",
               shape="box", style="rounded,filled,dashed",
               fillcolor=DESIGNED_FILL, color=DESIGNED_BORDER, penwidth="1.4",
               fontsize="9.5", fontcolor="#566573")
        c.node("legend_dec",
               "Decision",
               shape="diamond", style="filled",
               fillcolor=DECISION_FILL, color=DECISION_BORDER, penwidth="1.4",
               fontsize="9.5", width="1.6", height="0.9", fixedsize="true")
        c.edge("legend_dep", "legend_des", style="invis")
        c.edge("legend_des", "legend_dec", style="invis")

    # Anchor legend off the main flow without forcing rank
    g.edge("end", "legend_dep", style="invis", constraint="false")

    pdf, png = render_dot(g, "mbse_act_full_ride_lifecycle")
    register("mbse_act_full_ride_lifecycle", "ok", png_path=png)
    return pdf, png


if __name__ == "__main__":
    render()
