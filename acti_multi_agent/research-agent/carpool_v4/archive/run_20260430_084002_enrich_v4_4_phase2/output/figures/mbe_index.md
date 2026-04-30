# Model-Based-Engineer Figures — Index

20 figures rendered to serve `output/figures/draft.md`. Each row gives:
the stem, the section/anchor that would best receive it, a one-line caption,
and the exact `\includegraphics` line. PDF is canonical for LaTeX; PNG is
provided alongside for inspection.

Snapshot date for all production data referenced: **2026-04-23** (Supabase
project `bwimyvkwkenrtumsfjzt`).

| # | Stem | Inserts at | Caption (1 line) |
|---|------|------------|------------------|
| 1 | `mbe_a1_stack_layers` | §5.1 \label{fig:mbe-stack} | Deployed stack: Vue/Vite + Express on Railway + 23 controllers / 19 services + Supabase Postgres + Socket.IO/Redis + Resend + WeChat sidecars. |
| 2 | `mbe_a2_module_primitive_matrix` | §5.1 (alongside Table 2) | Module × primitive engagement matrix; symbols from §5.1 Table 2; column-band intensities from F3/F4/F5 survey means. |
| 3 | `mbe_a3_socketio_rooms` | §5.6 (Socket.IO substrate) | Socket.IO room namespacing: hub fans out to `user:{id}`, `activity:{id}`, `thread:{id}`, `ride:{id}` with event names labeled. |
| 4 | `mbe_a4_db_er_core` | §5.10 deployment evidence (or appendix) | Production schema: 18 core tables across 6 domain clusters with FK arrows and 2026-04-23 row counts inline. |
| 5 | `mbe_a5_module_overview_hexagon` | §1 / §5.1 opener | 6 modules orbiting an `.edu` identity core; disc area = primitive engagement; Carpool starred as deep-dive subject. |
| 6 | `mbe_b1_ride_state_machine` | §5.2 carpool overview | Ride + booking state machines; cross-cluster dashed edge marks the seat-recompute that may flip a ride to `full`. |
| 7 | `mbe_b2_activity_state_machine` | §5.4 activities | Activity + participant lifecycles; geo-checkin double-gated by `is_checkin_period` + Haversine distance. |
| 8 | `mbe_b3_marketplace_state_machine` | §5.3 marketplace | Item lifecycle (`active`/`sold`/`removed`) + listing-creation side effects; soft-delete preserves auditability. |
| 9 | `mbe_b4_ride_carpool_chat_lifecycle` | §5.7.5 messaging embedding | Ride-scoped group-chat lifecycle with `chat_expires_at = departure + 1h`; cancellation/reschedule branches dashed. |
| 10 | `mbe_c1_booking_5_effects_fanout` | §5.2 booking side-effects | `bookRide()` 5-side-effect fan-out: ride status, 6 notifications, group-ensure, WeChat record, Socket.IO emit. |
| 11 | `mbe_c2_identity_verification_flow` | §5.7.1 identity | `.edu` identity flow: register → token → Resend → click → JWT, with parallel guest read-only path. |
| 12 | `mbe_c3_rating_2h_delay_flow` | §5.7.3 rating | Rating window timeline (`T_dep + 2h`) + 4-guard upsert flow; flags 3 unimplemented mechanisms. |
| 13 | `mbe_c4_geo_checkin_pipeline` | §5.4 / §5.7.2 safety | 9-stage geo-verified check-in: time window + Haversine + verification radius + forensic trail. |
| 14 | `mbe_d1_messaging_substrate` | §5.6 messaging | DM, group, system messages on shared Socket.IO substrate with `(context_type,id)` cross-module binding. |
| 15 | `mbe_d2_points_award_deduct` | §5.7.4 gamification | Points: 13 sources → `awardPoints` → `point_transactions` + RPC + Socket.IO emit; production reality flag prominent. |
| 16 | `mbe_d3_wechat_outreach_pipeline` | §5.7.5 / §5.10 outreach | WeChat outreach: 3 producers → `wxgroup_notice_record` queue → batch poller → mini-program/H5 link → external groups. |
| 17 | `mbe_e1_research_agent_8phases` | §3.2 / §6.1 pipeline architecture | 8-phase pipeline: Sonnet/Opus tiers, JSON artifacts, P5 5-reviewer + auto-backtrack on score gates. |
| 18 | `mbe_e2_5_reviewer_radial` | §6 reviewer pattern | 5-reviewer eval: wedge angles = weights (25/25/20/15/15); 3-gate backtrack policy. |
| 19 | `mbe_e3_sample_skew_funnel` | §3.1 / §7.2 limits | Three-layer sample skew from N=117 raw → N=111 eligible → F5 anchor at N=19 Driver/Both. |
| 20 | `mbe_e4_registration_cadence` | §5.10 deployment feedback | Soft-launch cadence (Jan 3 / Feb 70 / Mar 111 = 184 users; 170 verified) + WeChat outreach pulse (82 pushes). |

## LaTeX include lines (paste-ready)

```latex
% --- Architecture (mbe_a*) ---
\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_a1_stack_layers.pdf}
  \caption{CampusRide deployed stack (snapshot 2026-04-23). Vue/Vite client → Express on Railway → 23 controllers + 19 services → Supabase Postgres + Storage; Socket.IO with Redis adapter, Resend (email verification), and the WeChat Mini-Program API run as sidecars. Source: \texttt{campusride-backend/src/app.js}.}
  \label{fig:mbe-stack}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_a2_module_primitive_matrix.pdf}
  \caption{Module $\times$ primitive engagement matrix. Symbols from Table~\ref{tab:primitives}; column-band intensities from F3/F4/F5 survey means; the hatched Rating-Fairness column carries the F5 driver-subset signal ($N=19$).}
  \label{fig:mbe-primitive-matrix}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_a3_socketio_rooms.pdf}
  \caption{Socket.IO room namespacing. A JWT-authenticated server hub fans out to four room clusters (\texttt{user:\{id\}}, \texttt{activity:\{id\}}, \texttt{thread:\{id\}}, \texttt{ride:\{id\}}); event names labeled on hub-to-room edges. Source: \texttt{config/socket.js:1-247}.}
  \label{fig:mbe-socket-rooms}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_a4_db_er_core.pdf}
  \caption{Production schema: 18 core tables grouped by domain (Identity, Carpool, Activities, Marketplace, Groups~\&~Messaging, Cross-module). Foreign keys converge on \texttt{users}; row counts are the 2026-04-23 snapshot. The points subsystem is annotated as not deployed (\texttt{point\_rules} 0 rows, \texttt{point\_transactions} returns PGRST205).}
  \label{fig:mbe-db-er}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=0.85\linewidth]{pic/mbe_a5_module_overview_hexagon.pdf}
  \caption{Six modules orbiting an \edudot{} identity core. Disc area is proportional to total primitive engagement (Carpool 6, Marketplace 4, Activities 2, Groups 1, Messages 1); the Points subsystem is rendered as a translucent ring rather than a vertex. Carpool (top, starred) is the deep-dive subject of \S\ref{sec:deep-dive}.}
  \label{fig:mbe-hexagon}
\end{figure}

% --- State machines & lifecycles (mbe_b*) ---
\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_b1_ride_state_machine.pdf}
  \caption{Ride and booking state machines. \texttt{rides.status} (left) and \texttt{ride\_bookings.status} (right); the dashed cross-cluster edge marks the server-side seat recompute that may transition the ride from \texttt{active} to \texttt{full}. Source: \texttt{carpooling.controller.js:511-709}.}
  \label{fig:mbe-ride-sm}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_b2_activity_state_machine.pdf}
  \caption{Activity and participant lifecycles. Activity transitions from \texttt{draft} to \texttt{published} (the gate that opens geo-checkin); \texttt{performCheckin()} is double-gated by \texttt{is\_checkin\_period} (default $\pm 30$~min) and a Haversine distance $\le$ \texttt{verification\_radius} (default 100\,m).}
  \label{fig:mbe-activity-sm}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_b3_marketplace_state_machine.pdf}
  \caption{Marketplace item lifecycle plus listing-creation side effects. Soft-delete (\texttt{status='removed'}) preserves cross-user comment threads and rating history.}
  \label{fig:mbe-marketplace-sm}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_b4_ride_carpool_chat_lifecycle.pdf}
  \caption{Ride-scoped group-chat lifecycle. \texttt{ensureRideCarpoolGroupOnBooking} is called inline from \texttt{bookRide}; idempotent INSERTs handle duplicate-key 23505 silently. Dashed branches: \texttt{cancelBooking}, \texttt{updateRide(departure\_time)}, and post-expiry read-only fallback.}
  \label{fig:mbe-ride-chat}
\end{figure}

% --- Flow & sequence (mbe_c*) ---
\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_c1_booking_5_effects_fanout.pdf}
  \caption{The \texttt{bookRide()} 5-side-effect fan-out. A single \texttt{POST /api/v1/carpooling/rides/:id/book} triggers (1) optional \texttt{rides.status} transition, (2) up to six \texttt{notifications} inserts spanning five categories (with two \texttt{ride\_rating\_reminder} rows scheduled at \texttt{departure+2h} via \texttt{RIDE\_RATING\_REMINDER\_DELAY\_MS}), (3) idempotent group-chat ensure, (4) \texttt{wxgroup\_notice\_record} insert, and (5) Socket.IO emit on \texttt{user:\{driver\_id\}}.}
  \label{fig:mbe-booking-fanout}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=0.9\linewidth]{pic/mbe_c2_identity_verification_flow.pdf}
  \caption{\edudot{} identity verification flow. Registration validates \texttt{@cornell.edu} regex and password policy, persists \texttt{users} with \texttt{verification\_status='pending'}, dispatches a Resend email; the verify link flips \texttt{is\_verified=true} and \texttt{verification\_status='verified'}; login issues a JWT consumed by REST and Socket.IO. Snapshot: 184 users, 100\% \texttt{@cornell.edu}, 170 (92.4\%) verified.}
  \label{fig:mbe-identity}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_c3_rating_2h_delay_flow.pdf}
  \caption{Rating window timeline (top) and submission flow (bottom). The window opens at \texttt{departure\_time + RATING\_READY\_DELAY\_MS} (2\,h); \texttt{createRating} traverses four guards (readiness, membership, role-pairing, self-rating) before \texttt{UPSERT} of \texttt{ratings(trip\_id, rater\_id, ratee\_id)} and the migration-008 trigger that recomputes \texttt{users.avg\_rating}. The side note flags three open design proposals; \texttt{ratings} held 0 rows in the 2026-04-23 snapshot.}
  \label{fig:mbe-rating}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_c4_geo_checkin_pipeline.pdf}
  \caption{Geo-verified activity check-in pipeline (\texttt{activity-checkin.service.js:31-191}). Red dashed edges denote guard rejections (HTTP 403 or distance-exceeded). \texttt{device\_info} and \texttt{ip\_address} captured for forensic trail; the same Haversine primitive is reusable for rideshare pickup verification.}
  \label{fig:mbe-geocheck}
\end{figure}

% --- Cross-module substrates (mbe_d*) ---
\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_d1_messaging_substrate.pdf}
  \caption{Cross-module messaging substrate. Three message tables (\texttt{messages}, \texttt{group\_messages}, \texttt{system\_messages}) share a single Socket.IO transport. DMs bind to ride/marketplace/activity records via \texttt{(context\_type, context\_id)}. The \texttt{messageService.sendMessage} \texttt{REPLY\_REQUIRED} guard limits cold DMs to one message until the recipient replies.}
  \label{fig:mbe-messaging}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_d2_points_award_deduct.pdf}
  \caption{Points award/deduct architecture (\texttt{services/points.service.js:122-236}). Thirteen sources fan in to \texttt{awardPoints}, which writes \texttt{point\_transactions}, calls the \texttt{increment\_user\_points} RPC, and emits a Socket.IO update. Red callout: in production \texttt{point\_rules} has 0 rows and \texttt{point\_transactions} does not exist (REST returns \texttt{PGRST205}); design is implementation-ready but inert.}
  \label{fig:mbe-points}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_d3_wechat_outreach_pipeline.pdf}
  \caption{WeChat group outreach pipeline. Three producers (rideshare 16, marketplace 62, activity 4) enqueue rows into \texttt{wxgroup\_notice\_record} (82 rows total, 2026-01-17 to 2026-04-11). \texttt{wechatLinkService.getBestNoticeLink} tries the mini-program short-link API and falls back to H5; the batch poller dispatches when 3+ rows accrue or the oldest row is $\ge$\,24\,h old.}
  \label{fig:mbe-wechat}
\end{figure*}

% --- Methodology & survey (mbe_e*) ---
\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_e1_research_agent_8phases.pdf}
  \caption{Research-agent 8-phase pipeline. Sonnet handles P1/P2/P2.5/P4 (high-volume); Opus handles P3/P3.5/P3.7/P5 (deep relational and evaluative reasoning). The five-reviewer P5 auto-backtracks (red dashed) when overall $<0.85$ or honesty $<0.80$, routing to the weakest-dimension phase. State invariants and fallback rules apply throughout.}
  \label{fig:mbe-pipeline}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=0.9\linewidth]{pic/mbe_e2_5_reviewer_radial.pdf}
  \caption{Five-reviewer evaluation pattern. Wedge angular spans equal reviewer weights (Narrative 25\%, Coverage 25\%, Gap 20\%, Contradiction 15\%, Honesty 15\%); the right panel shows the multi-condition backtrack policy.}
  \label{fig:mbe-reviewers}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_e3_sample_skew_funnel.pdf}
  \caption{Three-layer sample skew of the formative survey. From $N=117$ raw Qualtrics entries, 6 Survey-Preview rows excluded leaves $N=111$ eligible; concurrent language, role, and completion branchings narrow to the F5 anchor ($N=19$ Driver/Both, with $N=12$ Rider-only control).}
  \label{fig:mbe-skew}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbe_e4_registration_cadence.pdf}
  \caption{Soft-launch acquisition cadence and WeChat outreach pulse, 2026-01-08 to 2026-04-23. Monthly registrations (Jan~3, Feb~70, Mar~111) reach a cumulative 184 (170 verified, 92.4\%); WeChat pushes (62 marketplace + 16 ride + 4 activity = 82) ramp in parallel.}
  \label{fig:mbe-cadence}
\end{figure}
```

## Notes for the maintainer

- All 20 figures live at `output/figures/mbe_*.{pdf,png}` (40 files) and are
  registered as `status: ok` in `output/figures/viz_results.json`.
- Per-stem renderer modules: `scripts/mbe_<stem>.py`. Helpers: `scripts/_mbe_helpers.py`.
- Re-render any figure with: `python3 scripts/render_mbe_figures.py <stem>`,
  or all of them with `python3 scripts/render_mbe_figures.py --all`.
- Path convention in the LaTeX above uses `pic/` (the same prefix the existing
  `q24/q26/q30` survey radars use); adjust to `output/figures/` if your build
  resolves figures differently.
- Existing `q24_tolerance_radar.{pdf,png}`, `q26_motivation_radar.{pdf,png}`,
  `q30_severity_by_distance.{pdf,png}`, and `v1`–`v7` viz files are
  unchanged; the `mbe_` prefix avoids any collision.
