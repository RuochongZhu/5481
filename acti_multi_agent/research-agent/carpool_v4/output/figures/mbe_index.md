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
| 10 | `mbe_c1_booking_fanout` | §5.2 booking side-effects | `bookRide()` 3-branch fan-out (honesty-corrected): ride status, 6 notifications (each bundling 1 DB row + 1 Socket.IO emit), group-chat ensure. |
| 10b | `mbe_c5_createRide_fanout` | §5.2 ride publish + §5.10 outreach evidence | `createRide()` fan-out: rides INSERT + WeChat outreach pipeline (`wxgroup_notice_record` insert; the 16/82 ride pushes correspond to ride creates, not bookings). |
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
  \includegraphics[width=\textwidth]{pic/mbe_c1_booking_fanout.pdf}
  \caption{The \texttt{bookRide()} 3-branch fan-out (honesty-corrected). A single \texttt{POST /api/v1/carpooling/rides/:id/book} triggers (1)~optional \texttt{rides.status} transition to \texttt{full}; (2)~six \texttt{notifications} inserts spanning five categories (with two \texttt{ride\_rating\_reminder} rows scheduled at \texttt{departure+2h} via \texttt{RIDE\_RATING\_REMINDER\_DELAY\_MS}), each of which also emits one Socket.IO event on the recipient's \texttt{user:\{recipient\_id\}} room as a bundled side-effect of \texttt{notification.service.sendNotification}; and (3)~an idempotent \texttt{ride\_carpool} group-chat ensure. The WeChat \texttt{wxgroup\_notice\_record} insert often described alongside booking actually fires on \texttt{createRide}, not \texttt{bookRide} -- see Figure~\ref{fig:mbe-createride-fanout}.}
  \label{fig:mbe-booking-fanout}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbe_c5_createRide_fanout.pdf}
  \caption{The \texttt{createRide()} fan-out. Driver-side ride publication (\texttt{POST /api/v1/carpooling/rides}) (1)~INSERTs into \texttt{rides} with \texttt{status='active'}, and (2)~runs the WeChat outreach pipeline: builds an H5 deep-link, calls \texttt{wechatLinkService.getBestNoticeLink} (mini-program short-link with H5 fallback), formats the notice content via \texttt{simplifyLocation()}, and INSERTs into \texttt{wxgroup\_notice\_record} with \texttt{sendtime=NULL} for the asynchronous batch poller (\texttt{app.js:165-281, 313-328}). The 16 of 82 ride-related rows in the 2026-04-23 \texttt{wxgroup\_notice\_record} snapshot correspond to historical ride publications, not to bookings. Sibling outreach paths in \texttt{marketplace.controller.js:70} (62/82) and \texttt{activity.service.js:147} (4/82) converge on the same queue.}
  \label{fig:mbe-createride-fanout}
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

# MBSE Standardized Diagrams (`mbse_*`) — added v4.4

12 additional figures rendered against the same 2026-04-23 production snapshot.
These follow the standardized MBSE-course diagram types (BDD, IBD, Use Case,
Activity Swimlane, Activity, FFBD, Sequence, Requirements Spec, AHP,
Traceability Matrix, FMEA, Verification Matrix) and supersede the year-old
reference set with v4.4-grounded content.

| # | Stem | Inserts at | Caption (1 line) |
|---|------|------------|------------------|
| M1 | `mbse_bdd_system_context` | §1 intro / §5.1 opener | Block Definition Diagram: «system» CampusRide v4.4 with 5 «actor» blocks + 7 «external system» blocks (Resend, WeChat, Supabase, Railway, TCAT, Google Maps, Uber/Lyft reference). |
| M2 | `mbse_ibd_system_internals` | §5.1 platform overview | Internal Block Diagram: 6 modules (3×2) over 4 substrate bars (.edu identity, Notification + Socket.IO, Supabase + RLS, WeChat outreach), with inter-module port-flows and Points overlay ring. |
| M3 | `mbse_usecase_request_ride` | §5.2 carpool overview opener | Use Case Diagram for carpool capability: 3 actors, 10 priority-coloured ovals, «include»/«extend» dashed connectors, italic call-outs flag designed-but-uninstrumented use cases. |
| M4 | `mbse_act_swimlane_book_ride` | §5.2 booking side-effects | Activity-diagram swimlane (Rider \| System \| Driver) tracing `bookRide()` line-for-line with diamond decisions, fork/join bars, and an honesty note that `wxgroup_notice_record` fires on `createRide` not `bookRide`. |
| M5 | `mbse_act_full_ride_lifecycle` | §5 deep-dive opener | Full activity diagram createRide → bookRide → completeRide. Solid-green = deployed-and-exercised; dashed-grey = designed-but-uninstrumented (rating, SOS, points). |
| M6 | `mbse_ffbd_platform` | §5.1 (after Table 2) | Functional Flow Block Diagram F.1..F.12 platform-wide with OR/AND gates and a dashed feedback loop F.12 → F.1; F.11 (points) flagged with red striped border for the deployment gap. |
| M7 | `mbse_seq_book_ride` | §5.2 booking flow | UML Sequence Diagram bookRide with 6 lifelines (Rider Browser, controller, Postgres, NotificationService, Socket.IO Hub, faded WeChat worker); 2 alt + 1 loop combined fragments. |
| M8 | `mbse_req_spec` | §5.16 HoQ | Requirements specification table R.1–R.12 anchored to HoQ EC1–EC12 with subsystem chip, verification method, and status-tinted (green/yellow/red) row backgrounds + live-evidence trace. |
| M9 | `mbse_ahp_objectives` | §5.16 HoQ | 4-tier AHP hierarchy with 3 criteria (0.50/0.33/0.17), 10 sub-criteria, and 10 composite weights summing to 1.000; bottom stacked-bar ranks priorities. |
| M10 | `mbse_traceability_matrix` | §5.16 HoQ | Requirements (R.1–R.10) × Subsystem (8) traceability matrix with S/V cells, status badges (Active/Specified/Pending), and time-target column. |
| M11 | `mbse_fmea_table` | §5.17 Risk & V&V (new) | FMEA: 12 subsystem failure modes anchored to v4.4, with Severity/Occurrence/Detection gradients and RPN (S×O×D) heat-tinted column. |
| M12 | `mbse_verification_matrix` | §5.17 Risk & V&V (new) | Verification matrix TP.1–TP.12 × OR.1–OR.25 with diagonal `x` plus TP.11 multi-cell inspection coverage and TP.12 pending E2E row. |

## LaTeX include lines (paste-ready, MBSE block)

```latex
% --- MBSE standardized diagrams (mbse_*) ---
\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_bdd_system_context.pdf}
  \caption{Block Definition Diagram: \campusride{} v4.4 system context. The «system» block lists 6 modules and 184 verified users; 5 «actor» blocks (Riders, Drivers, Activity Organizers, Marketplace Sellers, Cornell IT / .edu Domain Authority) and 7 «external system» blocks (Resend, WeChat Mini-Program, Supabase, Railway, TCAT, Google Maps, Uber/Lyft reference) connect via labeled interaction edges. Snapshot 2026-04-23.}
  \label{fig:mbse-bdd}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_ibd_system_internals.pdf}
  \caption{Internal Block Diagram: 6 modules (3$\times$2) over 4 shared substrates (\edudot{} identity, Notification + Socket.IO, Supabase + RLS, WeChat outreach pipeline). Inter-module port-flows: Carpool$\rightarrow$Messages (\texttt{ride\_carpool} group), Marketplace$\rightarrow$WeChat (62 pushes), Activities$\rightarrow$Points (geo-checkin reward, inert in production). Points rendered as a translucent overlay ring per \S\ref{sec:points-overview}.}
  \label{fig:mbse-ibd}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_usecase_request_ride.pdf}
  \caption{Use Case Diagram for the carpool capability. Three actors (Rider, Activity Organizer, Driver), 10 use-case ovals coloured by priority (high / medium / low), and \uml{include} / \uml{extend} connectors mark mandatory sub-flows and condition-gated extensions. Italic call-outs flag designed-but-uninstrumented use cases (rating, points, SOS).}
  \label{fig:mbse-usecase}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_act_swimlane_book_ride.pdf}
  \caption{Activity-diagram swimlane (Rider $\mid$ System $\mid$ Driver) tracing \texttt{bookRide()} \texttt{(carpooling.controller.js:511-709)} line-for-line. Yellow diamonds are decisions; black bars are forks/joins for the parallel notification fan-out. The orange honesty note records that \texttt{wxgroup\_notice\_record} fires on \texttt{createRide}, not on \texttt{bookRide} (\S\ref{sec:carpool-overview} correction).}
  \label{fig:mbse-swimlane}
\end{figure}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_act_full_ride_lifecycle.pdf}
  \caption{Full ride lifecycle activity diagram from \texttt{createRide} $\rightarrow$ \texttt{bookRide} $\rightarrow$ 2\,h delay $\rightarrow$ \texttt{completeRide}. Solid green nodes are deployed-and-exercised; dashed-grey nodes are designed-but-uninstrumented (rating submission, SOS fan-out, points award) per the 2026-04-23 production snapshot.}
  \label{fig:mbse-ride-lifecycle}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_ffbd_platform.pdf}
  \caption{Functional Flow Block Diagram F.1--F.12 for the platform-wide flow, with OR/AND gates and a dashed feedback edge F.12 $\rightarrow$ F.1 closing the continuous-optimization loop. Block F.11 (points) is rendered with a red striped border to flag the production deployment gap (\texttt{point\_rules}\,$=$\,0 rows; \texttt{point\_transactions} table missing).}
  \label{fig:mbse-ffbd}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_seq_book_ride.pdf}
  \caption{UML Sequence Diagram for \texttt{bookRide}. Six lifelines (Rider Browser, \texttt{carpoolingController.bookRide}, Supabase Postgres, NotificationService, Socket.IO Hub, faded WeChat Worker); two \texttt{alt} fragments (seats\,=\,0 $\rightarrow$ 409; last seat $\rightarrow$ \texttt{UPDATE rides SET status='full'}) and one \texttt{loop} fragment over the 6 notification types.}
  \label{fig:mbse-seq}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_req_spec.pdf}
  \caption{Requirements specification R.1--R.12 anchored to HoQ EC1--EC12. Status row backgrounds: green\,=\,Deployed (R.1--R.9, R.11), yellow\,=\,Specified-not-deployed (R.10 points), red\,=\,Pending (R.12 multi-institution whitelist). Live-evidence column traces each row to the 2026-04-23 production snapshot.}
  \label{fig:mbse-req-spec}
\end{figure*}

\begin{figure}[t]\centering
  \includegraphics[width=\linewidth]{pic/mbse_ahp_objectives.pdf}
  \caption{Analytical Hierarchy Process for the v4.4 design objectives. Three top-level criteria (User Experience \& Trust 0.50, Operational Efficiency \& Reach 0.33, Cost-Sharing \& Sustainability 0.17) decompose into 10 sub-criteria with composite weights summing to 1.000. The bottom stacked-bar ranks the 10 composites.}
  \label{fig:mbse-ahp}
\end{figure}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_traceability_matrix.pdf}
  \caption{Requirements $\times$ Subsystem traceability matrix. Rows: 10 requirements R.1--R.10. Columns: 8 subsystems (Auth, Ride-Match, Cost-Split, SOS-Safety, Schedule, Comm/Chat, Suggest-Alt, Monitor/Reward). Filled blue \textbf{S} = satisfies; hollow orange \textbf{V} = verifies. Status badges and time targets in the right margin.}
  \label{fig:mbse-trace}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_fmea_table.pdf}
  \caption{Failure Mode Effects Analysis: 12 v4.4 subsystem failure modes with Severity / Occurrence / Detection (1--5 each) and Risk Priority Number RPN\,$=$\,S$\times$O$\times$D heat-tinted. Highest-risk rows: SOS (RPN 60), Payment integration (48), Auth-email and Ride-match race (16 each), F5-validated rating-fairness retaliation risk (24).}
  \label{fig:mbse-fmea}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_verification_matrix.pdf}
  \caption{Verification matrix: 12 test procedures TP.1--TP.12 (rows) $\times$ 10 originating requirements OR.1--OR.25 (columns) with the diagonal `\texttt{x}' verification pattern. TP.11 (manual snapshot inspection 2026-04-23) covers 6 EC requirements; TP.12 (E2E happy-path browser test) is Pending.}
  \label{fig:mbse-verif}
\end{figure*}
```

## Round-2 additions

Four additional `mbse_*` figures rendered against the same 2026-04-23
production snapshot. They round out the standardized MBSE-course diagram
set with a Deployment Diagram, a class-level Class Diagram, a unified
multi-entity State Machine, and a SysML Parametric Diagram.

| # | Stem | Inserts at | Caption (1 line) |
|---|------|------------|------------------|
| M13 | `mbse_deployment_diagram` | §5.10 deployment-feedback (after Table tab:deployment) | UML Deployment Diagram: 3 «device» nodes (Browser/Mobile, Railway Container, Supabase Cluster) + 3 sidecars (Resend, WeChat, TCAT) with «execution environment», artifacts, and protocol-labelled «communication path» links. |
| M14 | `mbse_class_diagram_db` | §5.1 platform overview (after Figure mbse-ibd-system-internals) | UML Class Diagram: 15 production classes across 6 domain clusters (Identity / Carpool / Activities / Marketplace / Messaging / Cross-module) with multiplicity-labelled associations and a polymorphic-WeChat-notice annotation. |
| M15 | `mbse_state_machine_unified` | §5.2 carpool overview (after the State machine and booking flow paragraph) | Combined UML State Machine: Ride + RideBooking + ride_carpool Group lifecycles on one canvas with dashed cross-entity trigger edges (bookRide may flip Ride to `full` and create the Group; cancelBooking may un-flag `full`; updateRide updates `chat_expires_at`). |
| M16 | `mbse_param_rating_window` | §5.13 sec:dd-rating (after the Implementation paragraph) | SysML Parametric Diagram for the rating-window guard: 3 «constraint» blocks (NotSelfRating ⊕ RoleEligible ⊕ RatingWindowOpen) with binding connectors from value properties + the 7,200,000 ms RATING_READY_DELAY_MS constant; chained outputs feed a Pass / Reject decision. |

## LaTeX include lines (paste-ready, Round-2 block)

```latex
% --- MBSE Round-2 additions (mbse_*) ---
\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_deployment_diagram.pdf}
  \caption{UML Deployment Diagram for \campusride{} v4.4. Three primary \texttt{«device»} nodes (Browser / Mobile, Railway Container, Supabase Cluster) host \texttt{«execution environment»} and \texttt{«artifact»} elements (Vue\,3 + Vite SPA / \texttt{bundle.js}; Node.js\,18 + Express running 23 controllers + 19 services + Socket.IO server; Postgres + RLS with 18 core tables, RLS policies, and the \texttt{increment\_user\_points} / \texttt{calculate\_distance} / \texttt{is\_checkin\_period} RPC functions). Three sidecar \texttt{«device»} nodes (Resend SMTP, WeChat Mini-Program API, TCAT bus schedule API) connect via labelled \texttt{«communication path»} edges (HTTPS REST + WebSocket; Postgres wire / RLS; SMTP via Resend; HTTPS to \texttt{wechatLinkService}). Snapshot 2026-04-23: 184 users, 82 \texttt{wxgroup\_notice\_record} rows, served at \texttt{www.campusgo.college}.}
  \label{fig:mbse-deployment}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_class_diagram_db.pdf}
  \caption{UML Class Diagram for the production database schema (snapshot 2026-04-23). Fifteen core classes are grouped into six domain clusters (Identity, Carpool, Activities, Marketplace, Messaging, Cross-module). Associations carry UML multiplicity labels (\texttt{1}, \texttt{0..1}, \texttt{1..*}, \texttt{0..*}); aggregation ends are marked with open diamonds on the owning side. The polymorphic \texttt{wxgroup\_notice\_record (source\_type, source\_id)} relation to \texttt{Ride}\,/\,\texttt{MarketplaceItem}\,/\,\texttt{Activity} is rendered as an annotated note rather than three near-identical edges to keep the layout legible.}
  \label{fig:mbse-class-db}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_state_machine_unified.pdf}
  \caption{Combined UML State Machine for the three coupled entities of a carpool ride: \texttt{Ride} (\texttt{active}\,$\to$\,\texttt{full}\,$\to$\,\texttt{completed}\,$|$\,\texttt{cancelled}), \texttt{RideBooking} (\texttt{confirmed}\,$\to$\,\texttt{cancelled}), and \texttt{Group(group\_kind='ride\_carpool')} (\texttt{created}\,$\to$\,\texttt{active}\,$\to$\,\texttt{expired}). Within-entity transitions are drawn solid in trigger\,[guard]\,/\,effect form; the dashed cross-cluster edges are the four side-effect couplings: \texttt{bookRide()} may flip the Ride to \texttt{full} and may create the Group; \texttt{cancelBooking()} may unflag \texttt{full} and removes the corresponding \texttt{group\_members} row; \texttt{updateRide(departure\_time)} resets \texttt{Group.chat\_expires\_at}; \texttt{completeRide()} triggers no booking or group transition (the Group expires on its own \texttt{departure + 1h} timer).}
  \label{fig:mbse-state-unified}
\end{figure*}

\begin{figure*}[t]\centering
  \includegraphics[width=\textwidth]{pic/mbse_param_rating_window.pdf}
  \caption{SysML Parametric Diagram for the rating-window guard in \texttt{rating.controller.js::createRating}. Three \texttt{«constraint»} blocks chain in order: \texttt{NotSelfRating} ($\textit{is\_valid}\,\equiv\,\textit{rater\_id}\,\ne\,\textit{ratee\_id}$), \texttt{RoleEligible} (driver--passenger pairing on the trip's \texttt{rides} row), and \texttt{RatingWindowOpen} ($\textit{is\_open}\,\equiv\,(\textit{now}\,-\,\textit{departure\_time})\,\ge\,\textit{delay}$, with delay\,$=$\,\texttt{RATING\_READY\_DELAY\_MS}\,$=$\,2\,h\,$=$\,7{,}200{,}000\,ms). Value properties drawn as small rectangles bind to the constraints via solid connectors with no arrowheads (UML convention). The chained constraint outputs feed a Pass\,/\,Reject decision; in the 2026-04-23 snapshot the \texttt{ratings} table holds zero rows so this guard chain has been exercised zero times in production.}
  \label{fig:mbse-param-rating}
\end{figure*}
```

## Notes for the maintainer

- Original 20 `mbe_*` figures + 12 round-1 `mbse_*` figures + 4 round-2
  `mbse_*` figures live at `output/figures/{mbe,mbse}_*.{pdf,png}`
  (72 files total) and are registered as `status: ok` in
  `output/figures/viz_results.json`.
- Per-stem renderer modules: `scripts/{mbe,mbse}_<stem>.py`. Helpers: `scripts/_mbe_helpers.py`.
- The auto-loader in `scripts/render_mbe_figures.py` now picks up both
  `mbe_*.py` and `mbse_*.py` patterns.
- Re-render any figure with: `python3 scripts/render_mbe_figures.py <stem>`,
  or all of them with `python3 scripts/render_mbe_figures.py --all`.
- Path convention in the LaTeX above uses `pic/` (the same prefix the existing
  `q24/q26/q30` survey radars use); adjust to `output/figures/` if your build
  resolves figures differently.
- Existing `q24_tolerance_radar.{pdf,png}`, `q26_motivation_radar.{pdf,png}`,
  `q30_severity_by_distance.{pdf,png}`, and `v1`–`v7` viz files are
  unchanged; the `mbe_` / `mbse_` prefixes avoid any collision.
