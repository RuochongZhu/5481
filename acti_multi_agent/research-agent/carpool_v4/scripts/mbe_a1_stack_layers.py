"""mbe_a1 — CampusRide Stack Layers Architecture.

A 4-tier layered architecture diagram (+ sidecar) showing the deployed
CampusRide system: Vue client, Express API gateway, services/controllers,
and Supabase data tier, with WeChat / Resend / Socket.IO sidecars.

Source-of-truth: integration-production/campusride-backend/src/app.js,
package.json, supabase project bwimyvkwkenrtumsfjzt (snapshot 2026-04-23).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# Tier fill colors (light pastels for easy distinction)
CLIENT_FILL = "#D6EAF8"   # light blue
GATEWAY_FILL = "#D5F5E3"  # light green
SERVICE_FILL = "#FAE5D3"  # light orange
DATA_FILL = "#E8DAEF"     # light purple
SIDECAR_FILL = "#FCF3CF"  # light yellow

CLIENT_BORDER = "#2874A6"
GATEWAY_BORDER = "#229954"
SERVICE_BORDER = "#CA6F1E"
DATA_BORDER = "#7D3C98"
SIDECAR_BORDER = "#B7950B"


@renderer("mbe_a1_stack_layers")
def render():
    g = make_digraph("a1_stack_layers", rankdir="TB")
    g.attr(ranksep="1.0", nodesep="0.5", splines="spline",
           compound="true", newrank="true",
           label="CampusRide deployed stack (snapshot 2026-04-23)",
           labelloc="t", fontsize="14")
    g.attr("node", fontsize="10")

    # ---------- Client tier ----------
    with g.subgraph(name="cluster_client") as c:
        c.attr(label="Client tier  (browser / WeChat mini-program webview)",
               style="rounded,filled", color=CLIENT_BORDER,
               fillcolor=CLIENT_FILL, fontsize="12", penwidth="1.4",
               rank="same")
        c.node("client_web",
               "Vue 3.5.12 SPA\nVite 5.4 build\nAnt Design Vue 4.2\nTailwindCSS",
               fillcolor="#FFFFFF", color=CLIENT_BORDER)
        c.node("client_socket",
               "Socket.IO-client 4.8\n(WS, JWT in handshake.auth)",
               fillcolor="#FFFFFF", color=CLIENT_BORDER)
        c.node("client_wechat",
               "WeChat mini-program\nwebview shell",
               fillcolor="#FFFFFF", color=CLIENT_BORDER)

    # ---------- API gateway tier ----------
    with g.subgraph(name="cluster_gateway") as c:
        c.attr(label="API gateway tier  (Railway)",
               style="rounded,filled", color=GATEWAY_BORDER,
               fillcolor=GATEWAY_FILL, fontsize="12", penwidth="1.4",
               rank="same")
        c.node("gw_express",
               "Express 5.1 on Node.js\nmounts /api/v1/*\nhelmet + cors + rate-limit",
               fillcolor="#FFFFFF", color=GATEWAY_BORDER)
        c.node("gw_io",
               "Socket.IO server\n(authenticated rooms)",
               fillcolor="#FFFFFF", color=GATEWAY_BORDER)

    # ---------- Service layer ----------
    with g.subgraph(name="cluster_service") as c:
        c.attr(label="Service layer  (23 controllers + 19 services)",
               style="rounded,filled", color=SERVICE_BORDER,
               fillcolor=SERVICE_FILL, fontsize="12", penwidth="1.4")

        # Controllers cluster (same rank inside)
        with c.subgraph(name="cluster_controllers") as cc:
            cc.attr(label="Controllers (key)",
                    style="rounded,dashed", color=SERVICE_BORDER,
                    fillcolor="#FFF7E6", fontsize="11", rank="same")
            cc.node("ctrl_auth", "auth.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cc.node("ctrl_carpool",
                    "carpooling.controller\nPOST /rides/:id/book\n(booking entrypoint)",
                    fillcolor="#FFE9C9", color=SERVICE_BORDER, penwidth="1.6")
            cc.node("ctrl_activity", "activity.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cc.node("ctrl_marketplace", "marketplace.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cc.node("ctrl_group", "group.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cc.node("ctrl_message", "message.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cc.node("ctrl_points", "points.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cc.node("ctrl_rating", "rating.controller",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)

        # Services cluster (same rank inside)
        with c.subgraph(name="cluster_services") as cs:
            cs.attr(label="Services (key)",
                    style="rounded,dashed", color=SERVICE_BORDER,
                    fillcolor="#FFF7E6", fontsize="11", rank="same")
            cs.node("svc_notif", "notification.service",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cs.node("svc_points", "points.service",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cs.node("svc_rcg", "rideCarpoolGroup.service",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cs.node("svc_checkin", "activity-checkin.service",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cs.node("svc_wxlink", "wechat-link.service",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)
            cs.node("svc_msg", "messageService",
                    fillcolor="#FFFFFF", color=SERVICE_BORDER)

    # ---------- Data tier ----------
    with g.subgraph(name="cluster_data") as c:
        c.attr(label="Data tier  (Supabase project bwimyvkwkenrtumsfjzt)",
               style="rounded,filled", color=DATA_BORDER,
               fillcolor=DATA_FILL, fontsize="12", penwidth="1.4",
               rank="same")
        c.node("db_pg",
               "Supabase Postgres\n"
               "users=184  rides=0  ratings=0\n"
               "marketplace_items=15  groups=5\n"
               "messages=22  notifications=54\n"
               "wxgroup_notice_record=82\n"
               "RPC: increment_user_points,\ncalculate_distance",
               fillcolor="#FFFFFF", color=DATA_BORDER)
        c.node("db_storage",
               "Supabase Storage\n(avatars, listing images)",
               fillcolor="#FFFFFF", color=DATA_BORDER)

    # ---------- Sidecar / external (right column) ----------
    with g.subgraph(name="cluster_sidecar") as c:
        c.attr(label="Sidecar / external (right column)",
               style="rounded,filled", color=SIDECAR_BORDER,
               fillcolor=SIDECAR_FILL, fontsize="12", penwidth="1.4")
        c.node("sc_redis",
               "Redis adapter\n(Socket.IO multi-instance pub/sub)",
               fillcolor="#FFFFFF", color=SIDECAR_BORDER)
        c.node("sc_resend",
               "Resend\n(email verification)",
               fillcolor="#FFFFFF", color=SIDECAR_BORDER)
        c.node("sc_wxapi",
               "WeChat Mini-Program API\n(short link + H5 fallback)",
               fillcolor="#FFFFFF", color=SIDECAR_BORDER)
        c.node("sc_poller",
               "WeChat group notice\nbatch poller (cron)",
               fillcolor="#FFFFFF", color=SIDECAR_BORDER)
        # Vertical stack within sidecar — visible structural edges
        c.edge("sc_redis", "sc_resend", style="invis", weight="10")
        c.edge("sc_resend", "sc_wxapi", style="invis", weight="10")
        c.edge("sc_wxapi", "sc_poller", style="invis", weight="10")

    # ---------- Cross-tier edges ----------
    # Client -> Gateway
    g.edge("client_web", "gw_express",
           label="HTTPS REST\nAuthorization: Bearer <JWT>",
           color=CLIENT_BORDER, fontcolor=CLIENT_BORDER)
    g.edge("client_socket", "gw_io",
           label="WebSocket\nhandshake.auth.token",
           color=CLIENT_BORDER, fontcolor=CLIENT_BORDER, style="dashed")
    g.edge("client_wechat", "gw_express",
           label="HTTPS (webview)",
           color=CLIENT_BORDER, fontcolor=CLIENT_BORDER, style="dotted")

    # Gateway -> Service layer
    g.edge("gw_express", "ctrl_carpool",
           label="route mount\n/api/v1/*",
           color=GATEWAY_BORDER, fontcolor=GATEWAY_BORDER)
    g.edge("gw_io", "svc_notif",
           label="emit",
           color=GATEWAY_BORDER, fontcolor=GATEWAY_BORDER, style="dashed")

    # Controllers -> Services (representative wiring)
    g.edge("ctrl_carpool", "svc_rcg", color=SERVICE_BORDER)
    g.edge("ctrl_carpool", "svc_points", color=SERVICE_BORDER)
    g.edge("ctrl_activity", "svc_checkin", color=SERVICE_BORDER)
    g.edge("ctrl_message", "svc_msg", color=SERVICE_BORDER)
    g.edge("ctrl_points", "svc_points", color=SERVICE_BORDER)
    g.edge("ctrl_group", "svc_wxlink", color=SERVICE_BORDER)
    g.edge("ctrl_rating", "svc_notif", color=SERVICE_BORDER)
    g.edge("ctrl_auth", "svc_notif", color=SERVICE_BORDER, style="dotted")

    # Services -> Data tier
    g.edge("svc_rcg", "db_pg",
           label="Supabase JS\n(REST + RPC)",
           color=DATA_BORDER, fontcolor=DATA_BORDER)
    g.edge("svc_points", "db_pg",
           label="rpc(increment_user_points)",
           color=DATA_BORDER, fontcolor=DATA_BORDER)
    g.edge("svc_msg", "db_pg", color=DATA_BORDER)
    g.edge("svc_checkin", "db_pg",
           label="rpc(calculate_distance)",
           color=DATA_BORDER, fontcolor=DATA_BORDER)
    g.edge("svc_notif", "db_pg", color=DATA_BORDER, style="dashed")
    g.edge("ctrl_marketplace", "db_storage",
           label="signed uploads",
           color=DATA_BORDER, fontcolor=DATA_BORDER, style="dashed")

    # Services -> Sidecar / external (constraint=false so sidecar can float right)
    g.edge("gw_io", "sc_redis",
           label="adapter",
           color=SIDECAR_BORDER, fontcolor=SIDECAR_BORDER, style="dashed",
           constraint="false")
    g.edge("svc_notif", "sc_resend",
           label="sendVerificationEmail",
           color=SIDECAR_BORDER, fontcolor=SIDECAR_BORDER,
           constraint="false")
    g.edge("svc_wxlink", "sc_wxapi",
           label="getBestNoticeLink",
           color=SIDECAR_BORDER, fontcolor=SIDECAR_BORDER,
           constraint="false")

    # Poller pulls from data tier
    g.edge("sc_poller", "db_pg",
           label="SELECT wxgroup_notice_record\nWHERE sendtime IS NULL",
           color=SIDECAR_BORDER, fontcolor=SIDECAR_BORDER, dir="back",
           style="dashed", constraint="false")
    g.edge("sc_poller", "sc_wxapi",
           label="dispatch",
           color=SIDECAR_BORDER, fontcolor=SIDECAR_BORDER, style="dashed",
           constraint="false")

    # ---- Same-rank pins to align sidecar column horizontally with main col ----
    # The sidecar should sit visually on the right. We pin each sidecar node
    # to the same rank as a corresponding node in the main column.
    with g.subgraph() as r:
        r.attr(rank="same")
        r.node("gw_express")
        r.node("sc_redis")
    with g.subgraph() as r:
        r.attr(rank="same")
        r.node("ctrl_carpool")
        r.node("sc_resend")
    with g.subgraph() as r:
        r.attr(rank="same")
        r.node("svc_rcg")
        r.node("sc_wxapi")
    with g.subgraph() as r:
        r.attr(rank="same")
        r.node("db_pg")
        r.node("sc_poller")


    pdf, png = render_dot(g, "mbe_a1_stack_layers")
    register("mbe_a1_stack_layers", "ok", png_path=png)
    return pdf, png
