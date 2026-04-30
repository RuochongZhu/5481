"""mbe_c2 — `.edu` Identity Verification Flow.

Sequence/flow diagram of the registration -> email-verification -> JWT issuance
pipeline, plus the parallel guest-token branch consumed by Socket.IO.

Source-of-truth:
  campusride-backend/src/controllers/auth.controller.js:35-178
  campusride-backend/src/config/socket.js:44
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_mbe_figures import renderer  # noqa: E402
from _mbe_helpers import make_digraph, render_dot, register  # noqa: E402


# Palette per spec
CLIENT_FILL = "#FCF3CF"     # yellow
SERVER_FILL = "#D6EAF8"     # light blue
DB_FILL     = "#A9DFBF"     # green
EMAIL_FILL  = "#F5CBA7"     # orange
NOTE_FILL   = "#FDEBD0"
GUEST_FILL  = "#E8DAEF"

CLIENT_BORDER = "#9A7D0A"
SERVER_BORDER = "#1F618D"
DB_BORDER     = "#196F3D"
EMAIL_BORDER  = "#A04000"
GUEST_BORDER  = "#6C3483"
GUARD_COLOR   = "#922B21"   # italic red-tinted


@renderer("mbe_c2_identity_verification_flow")
def render():
    g = make_digraph("c2_identity_flow", rankdir="TB")
    g.attr(
        ranksep="0.55", nodesep="0.45", splines="spline",
        label=(
            "`.edu` Identity Verification Flow  "
            "(auth.controller.js:35-178, config/socket.js:44)"
        ),
        labelloc="t", fontsize="14",
    )
    g.attr("node", fontsize="11")
    g.attr("edge", fontsize="10")

    # =====================================================================
    # MAIN FLOW cluster (left/center, top-to-bottom)
    # =====================================================================
    with g.subgraph(name="cluster_main") as c:
        c.attr(
            label="Main flow: register -> verify -> login -> JWT",
            style="rounded", color=SERVER_BORDER,
            fontsize="12", penwidth="1.2",
        )

        # 1. Client register
        c.node(
            "n1_client_register",
            ("CLIENT\nPOST /api/v1/auth/register\n"
             "{ email, password, first_name,\n"
             "  last_name, student_id }"),
            shape="box", style="rounded,filled",
            fillcolor=CLIENT_FILL, color=CLIENT_BORDER, penwidth="1.4",
        )

        # 2. Validation node (server)
        c.node(
            "n2_validate",
            ("SERVER  validate()\n"
             "email regex: must end @cornell.edu\n"
             "password: >=8 chars, >=1 upper,\n"
             ">=1 lower, >=1 digit"),
            shape="box", style="rounded,filled",
            fillcolor=SERVER_FILL, color=SERVER_BORDER, penwidth="1.4",
        )

        # 3. Generate token
        c.node(
            "n3_token",
            ("SERVER  generate verification token\n"
             "email_verification_token = crypto.random()\n"
             "email_verification_expires = now + 24h"),
            shape="box", style="rounded,filled",
            fillcolor=SERVER_FILL, color=SERVER_BORDER, penwidth="1.4",
        )

        # 4. DB insert
        c.node(
            "n4_db_insert",
            ("DB  INSERT INTO users\n"
             "is_verified = false\n"
             "verification_status = 'pending'"),
            shape="cylinder", style="filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )

        # 6. Award points (between insert and email click)
        c.node(
            "n6_points",
            ("SERVER  awardPoints('registration')  +10\n"
             "INSERT point_transactions\n"
             "(production point_rules has 0 rows ->\n"
             "this is currently a no-op in deploy)"),
            shape="box", style="rounded,filled",
            fillcolor=SERVER_FILL, color=SERVER_BORDER, penwidth="1.2",
        )

        # 7. Email click
        c.node(
            "n7_click",
            ("CLIENT (email link)\n"
             "GET /api/v1/auth/verify?token=<...>"),
            shape="box", style="rounded,filled",
            fillcolor=CLIENT_FILL, color=CLIENT_BORDER, penwidth="1.4",
        )

        # 8. Validate token + expiry
        c.node(
            "n8_validate_token",
            ("SERVER  verifyEmail()\n"
             "lookup token, check expiry"),
            shape="box", style="rounded,filled",
            fillcolor=SERVER_FILL, color=SERVER_BORDER, penwidth="1.4",
        )

        # 9. DB update verified
        c.node(
            "n9_db_update",
            ("DB  UPDATE users\n"
             "is_verified = true\n"
             "verification_status = 'verified'\n"
             "email_verification_token = NULL"),
            shape="cylinder", style="filled",
            fillcolor=DB_FILL, color=DB_BORDER, penwidth="1.4",
        )

        # 10. Login
        c.node(
            "n10_login",
            ("CLIENT  POST /api/v1/auth/login\n"
             "SERVER  bcrypt.compare(password)\n"
             "+ guard: is_verified == true"),
            shape="box", style="rounded,filled",
            fillcolor=SERVER_FILL, color=SERVER_BORDER, penwidth="1.4",
        )

        # 11. Issue JWT
        c.node(
            "n11_jwt",
            ("SERVER  jwt.sign(\n"
             "  { userId, type: 'user' },\n"
             "  JWT_SECRET, HS256, 7d )"),
            shape="box", style="rounded,filled",
            fillcolor=SERVER_FILL, color=SERVER_BORDER, penwidth="1.4",
        )

        # 12. Authenticated calls
        c.node(
            "n12_authn",
            ("CLIENT  authenticated calls\n"
             "REST: Authorization: Bearer <jwt>\n"
             "Socket.IO: handshake.auth.token"),
            shape="box", style="rounded,filled",
            fillcolor=CLIENT_FILL, color=CLIENT_BORDER, penwidth="1.4",
        )

        # Edges with guard labels (italic red-tinted)
        c.edge(
            "n1_client_register", "n2_validate",
            label="<<i>guard: HTTPS, body parsed</i>>",
            fontcolor=GUARD_COLOR, color=SERVER_BORDER,
        )
        c.edge(
            "n2_validate", "n3_token",
            label=("<<i>guard: email ~ /@cornell\\.edu$/<br/>"
                   "AND pwd matches policy</i>>"),
            fontcolor=GUARD_COLOR, color=SERVER_BORDER,
        )
        c.edge(
            "n3_token", "n4_db_insert",
            label="persist user row",
            color=DB_BORDER, fontcolor=DB_BORDER,
        )
        c.edge(
            "n4_db_insert", "n6_points",
            label="post-insert hook",
            color=SERVER_BORDER, fontcolor=SERVER_BORDER,
        )
        c.edge(
            "n6_points", "n7_click",
            label=("<<i>guard: user clicks within<br/>"
                   "email_verification_expires (24h)</i>>"),
            style="dashed",
            fontcolor=GUARD_COLOR, color=CLIENT_BORDER,
        )
        c.edge(
            "n7_click", "n8_validate_token",
            color=SERVER_BORDER,
        )
        c.edge(
            "n8_validate_token", "n9_db_update",
            label=("<<i>guard: token matches<br/>"
                   "AND now &lt; expires</i>>"),
            fontcolor=GUARD_COLOR, color=DB_BORDER,
        )
        c.edge(
            "n9_db_update", "n10_login",
            label="user can now log in",
            color=SERVER_BORDER, fontcolor=SERVER_BORDER,
        )
        c.edge(
            "n10_login", "n11_jwt",
            label=("<<i>guard: bcrypt match<br/>"
                   "AND is_verified == true</i>>"),
            fontcolor=GUARD_COLOR, color=SERVER_BORDER,
        )
        c.edge(
            "n11_jwt", "n12_authn",
            label="return token to client",
            color=SERVER_BORDER, fontcolor=SERVER_BORDER,
        )

    # =====================================================================
    # PARALLEL email branch (off step 4)
    # =====================================================================
    g.node(
        "n5_email",
        ("EMAIL SERVICE (Resend)\n"
         "sendVerificationEmail(\n"
         "  email, token )\n"
         "subject: 'Verify your Cornell email'"),
        shape="box", style="rounded,filled",
        fillcolor=EMAIL_FILL, color=EMAIL_BORDER, penwidth="1.4",
    )
    g.edge(
        "n4_db_insert", "n5_email",
        label="parallel branch\n(fire-and-forget)",
        style="dashed", color=EMAIL_BORDER, fontcolor=EMAIL_BORDER,
        constraint="false",
    )
    # Email service hands off to user mailbox -> click
    g.edge(
        "n5_email", "n7_click",
        label="user opens link",
        style="dashed", color=EMAIL_BORDER, fontcolor=EMAIL_BORDER,
        constraint="false",
    )

    # =====================================================================
    # GUEST cluster (right side, dashed)
    # =====================================================================
    with g.subgraph(name="cluster_guest") as gc:
        gc.attr(
            label="Guest token branch (read-only)",
            style="dashed,rounded", color=GUEST_BORDER,
            fillcolor="#FBF5FE", fontsize="12", penwidth="1.4",
        )

        gc.node(
            "g1_client",
            ("CLIENT  open read-only view\n"
             "(no .edu account)"),
            shape="box", style="rounded,filled",
            fillcolor=CLIENT_FILL, color=CLIENT_BORDER, penwidth="1.4",
        )
        gc.node(
            "g2_jwt",
            ("SERVER  jwt.sign(\n"
             "  { userId: 'guest',\n"
             "    type: 'guest' },\n"
             "  JWT_SECRET, HS256 )\n"
             "limited scope"),
            shape="box", style="rounded,filled",
            fillcolor=GUEST_FILL, color=GUEST_BORDER, penwidth="1.4",
        )
        gc.node(
            "g3_socket",
            ("Socket.IO middleware\n"
             "(config/socket.js:44)\n"
             "accepts BOTH user + guest tokens;\n"
             "guests restricted to read-only events"),
            shape="note", style="filled",
            fillcolor=NOTE_FILL, color=GUEST_BORDER,
            fontcolor=GUEST_BORDER, fontsize="9",
        )

        gc.edge(
            "g1_client", "g2_jwt",
            label="GET /api/v1/auth/guest",
            color=GUEST_BORDER, fontcolor=GUEST_BORDER,
        )
        gc.edge(
            "g2_jwt", "g3_socket",
            label="handshake.auth.token",
            style="dashed",
            color=GUEST_BORDER, fontcolor=GUEST_BORDER,
        )

    # Cross-link: both flows feed Socket.IO middleware
    g.edge(
        "n12_authn", "g3_socket",
        label="user JWT also accepted",
        style="dotted", color="#566573", fontcolor="#566573",
        constraint="false",
    )

    # =====================================================================
    # Snapshot footer (legend node)
    # =====================================================================
    g.node(
        "snapshot",
        ("Production snapshot (2026-04):\n"
         "184 users registered  |  100% @cornell.edu  |  170 verified (92.4%)\n"
         "2-tier verification model collapses to 1-tier in practice:\n"
         "no manual-review queue is wired up."),
        shape="note", style="filled",
        fillcolor="#FEF9E7", color="#7D6608", fontcolor="#7D6608",
        fontsize="10",
    )
    g.edge(
        "n12_authn", "snapshot",
        style="invis", constraint="true",
    )

    pdf, png = render_dot(g, "mbe_c2_identity_verification_flow")
    register("mbe_c2_identity_verification_flow", "ok", png_path=png)
    return pdf, png
