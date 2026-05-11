# Unified Figure Style Guide (paper-ready)

All `mbe_*` and `mbse_*` figures must follow this style. Reference
implementation: `scripts/mbe_c1_booking_fanout.py`. The guide below is the
contract every rewrite agent must satisfy.

## 1. Visual identity

- **Engine**: matplotlib only (drop graphviz where the diagram type allows
  matplotlib — graphviz is acceptable only for true ER diagrams or when
  plain rectangles are insufficient).
- **Fonts**: call `setup_mpl()` from `_mbe_helpers`. This sets
  Helvetica → Arial → DejaVu Sans, with editable text in PDF (`fonttype=42`).
- **Color palette** (import from `_mbe_helpers`):
  - `PLATFORM_COLOR` substitute: `#1A5276` (navy — the platform itself)
  - `RIDER_COLOR = "#2980B9"` (blue — passenger / rider lane)
  - `DRIVER_COLOR = "#C0392B"` (red — driver lane)
  - `ACCENT_COLOR` (use literal `#F39C12` orange) for design highlights
  - Neutral text/lines: `#566573` (cool grey)
- **Cards**: `FancyBboxPatch` with `boxstyle="round,pad=0.04"`, white
  facecolor, edgecolor = lane color, linewidth=1.4.
- **Lane bands**: same color as actor, alpha=0.07, edgecolor with
  linewidth=0.8.
- **Arrows**: `FancyArrowPatch` with `arrowstyle="-|>"`, mutation_scale=12.
- **Title**: fontsize=14, bold, pad=14. Optional italic subtitle in
  `#566573` describing the design intent in one sentence.
- **DPI**: 300 for raster (`save_mpl(stem, dpi=300)`).

## 2. Code-language elimination

The figure is for HCI/CHI readers, not engineers. Strip every
implementation reference. Replace as below:

| ❌ Don't say | ✅ Say instead |
|--------------|---------------|
| `controllers/carpooling.controller.js:511-709` | (drop entirely; cite in caption if needed) |
| `INSERT ride_bookings (status='confirmed')` | "Reserve seat" / "Booking record created" |
| `UPDATE rides SET status='full'` | "Mark trip as full" |
| `RIDE_RATING_REMINDER_DELAY_MS = 2*60*60*1000` | "2 hours after trip ends" |
| `ensureRideCarpoolGroupOnBooking(...)` | "Open trip-bound chat" |
| `socketManager.sendNotificationToUser(...)` | "Notify user in real-time" |
| `Postgres 23505 silent swallow` | "(idempotent)" or drop |
| `wxgroup_notice_record` | "WeChat post queue" / "External outreach queue" |
| `@cornell.edu regex` | "Cornell email check" |
| `JWT type='guest'` | "Guest read-only access" |
| `verification_radius` (default 100m) | "venue radius (~100 m)" |
| `is_checkin_period` | "within check-in window" |
| `Haversine RPC calculate_distance` | "Distance check" |
| `point_transactions` table | "Points ledger" |
| `increment_user_points` RPC | "Atomic balance update" (or drop) |
| `PGRST205` / "table does not exist" | "Not yet provisioned in production" |
| Variable names with `_` (e.g., `available_seats`) | natural English ("seats remaining") |
| `narrative_chains.json`, `evidence_inventory.json` | "Narrative chains" / "Evidence inventory" |

## 3. Where snapshot numbers belong

Concrete production numbers (e.g., 184 verified, 16/82 ride pushes, N=19
F5 subset) are **OK to keep in figures** — they are findings, not code.
Only the *engineering machinery* gets stripped.

## 4. Diagram types and how to render them

| Diagram type | Engine | Style notes |
|--------------|--------|-------------|
| Sequence / Activity (with actors) | matplotlib | 3 swim-lanes (actor1 / Platform / actor2), time axis at bottom, cards at temporal positions, arrows between lanes. Same as c1. |
| State machine | matplotlib (preferred) or graphviz | Rounded states, accent color for terminal states, edges labeled with concept-level transitions ("Driver completes trip"), no file:line, no method names |
| ER / Class diagram | graphviz HTML-table nodes acceptable | Keep table names + key columns (this IS the contribution); drop SQL types, drop UUIDs / FK arrowstyles, drop "PGRST205" — replace with "(not yet deployed)" |
| Hub & spoke | matplotlib | Center disc + outer ring of cards; each spoke labeled with concept-level event ("real-time notification") |
| Pipeline (LR phases) | matplotlib | Horizontal cards with accent dividers; backtrack arrow as accent-colored dashed |
| Funnel | matplotlib | Wide-to-narrow horizontal cards with arrows; numeric annotations OK (these are findings) |
| Hierarchy / AHP | matplotlib | Tree layout with rounded boxes; weights as edge labels (`0.25`, `0.20`, ...) — these are findings |
| Matrix / FMEA / Traceability / Verification | matplotlib | imshow with categorical colors; row/column labels in plain English; cell text concept-level |
| Use case | matplotlib | Stick-figure actors + ovals — keep formal but no code references inside ovals |
| Parametric (SysML) | matplotlib | Simplify to "constraint flow": named constraints in rounded boxes connected by arrows; **no constants written out** |

## 5. Subtitle convention

Each figure should carry a one-sentence italic subtitle (in `#566573`)
between the title and the figure body. The subtitle states the **design
intent**, not the mechanism. Examples:

- c1: "Bidirectional rating; the post-trip window is deferred by design
  to remove the in-vehicle rating moment."
- e1: "Eight-phase evidence pipeline; reviewer disagreement triggers
  human-in-loop, not silent override."

## 6. Forbidden visual patterns

- HTML-encoded entities like `&#8804;` (use words: "up to", "at most")
- Multi-line code blocks rendered inline (`lines 593-599\nUPDATE rides...`)
- Footers that say "Per successful booking: 1 ride_bookings row + 6
  notifications rows + ..." — replace with the design-intent subtitle.
- Color legend that explains every shape — readers infer from labels.
- "Honesty note: ..." in red footer — move honesty corrections to the
  main text or caption.

## 7. Verification checklist (every agent must run this)

After rendering, multimodal-Read the PNG and confirm:

1. ☐ No file paths or `:line` references anywhere in the figure.
2. ☐ No SQL keywords (SELECT/INSERT/UPDATE/DELETE), no JS syntax, no
   curly-brace JSON.
3. ☐ No constants spelled out (no `RIDE_RATING_REMINDER_DELAY_MS`, no
   `2*60*60*1000`).
4. ☐ Color palette matches §1.
5. ☐ Title + italic subtitle in place.
6. ☐ Card text reads as English sentences, not pseudocode.
7. ☐ No overlapping cards or text.
8. ☐ Snapshot numbers (e.g., `N=19`, `184 verified`) are kept where
   they're findings, dropped where they're implementation notes.
