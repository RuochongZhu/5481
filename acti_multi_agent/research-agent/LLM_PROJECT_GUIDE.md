# CampusRide LLM Project Guide

This document is the single-file onboarding guide for humans and LLMs. It is intended to give an accurate mental model of the current codebase, the active development directory, the main product features, the runtime architecture, and the places where the repository still contains legacy or misleading material.

## 1. One-Screen Summary

- Project name: `CampusRide`
- Product type: campus community platform combining rideshare, marketplace, activities, groups, messaging, points, and notifications
- Current active code line: `integration-local-localhost/`
- Frontend: Vue 3 + Vite + Pinia + Ant Design Vue + Tailwind CSS
- Backend: Node.js + Express + Supabase + Socket.IO + Resend
- Local default ports:
  - Frontend dev server: `5173`
  - Backend API server: `3001`
- Main external services:
  - Supabase for database and auth-related data access
  - Google Maps for location features
  - Resend for transactional email
  - WeChat-related env vars exist for mini-program linking and optional auth flows

## 2. Which Directory Is The Real Project

This repository is not a clean single-app repo. It contains multiple snapshots, backups, and generated notes.

Use this as the source of truth:

- Active frontend + backend: `integration-local-localhost/`

Treat these as reference-only unless explicitly needed:

- `integration-production/`
  Production-oriented snapshot/reference copy
- `integration_backup_local_1.2.9/`
  Historical backup
- Root-level summary files such as `COMPLETE_SUMMARY.md`, `EXECUTION_SUMMARY.md`, `QUICK_REFERENCE.md`
  Many are task-specific notes, not canonical architecture docs

## 3. Product Scope

CampusRide is a campus-focused social utility platform. The project is broader than “rideshare”; it is a multi-module app with overlapping social and transactional features.

Major functional areas:

- Authentication and account lifecycle
  - Register, login, guest login, email verification, password reset, token refresh
- Rideshare / carpool
  - Create rides, browse rides, booking-related operations, ratings
- Marketplace
  - Post items, browse listings, comments, favorites, item messaging
- Activities
  - Create activities, browse activity feed, detail pages, registration, history, check-in
- Groups and social graph
  - Group maps, group detail, friend-related APIs, visibility/location features, thoughts/posts
- Messaging and notifications
  - Direct messages, system messages, unread counts, socket-based real-time updates
- Gamification
  - Points, transactions, leaderboard, engagement rewards
- Admin and announcements
  - Admin routes/views and announcement APIs
- Compliance/legal pages
  - Terms, privacy, cookies, disclosures, carpool disclaimer

## 4. High-Level Architecture

The project is a split frontend/backend web application.

### Frontend

- Location: `integration-local-localhost/src/`
- Stack:
  - Vue 3
  - Vue Router
  - Pinia
  - Axios
  - Ant Design Vue
  - Tailwind CSS
  - Socket.IO client
  - Google Maps JS API
- Dev server:
  - Vite on `5173` by default
- API strategy:
  - Axios instance uses `VITE_API_BASE_URL` or falls back to `http://localhost:3001`
  - API helper then appends `/api/v1`
- Auth strategy:
  - JWT access token in `localStorage`
  - Refresh token flow handled in Axios response interceptor
  - Public auth pages are protected from accidental redirect loops during token expiry

### Backend

- Location: `integration-local-localhost/campusride-backend/src/`
- Stack:
  - Node.js
  - Express
  - Socket.IO
  - Supabase JS client
  - JWT
  - Resend
  - Swagger
- Default bind:
  - Host `0.0.0.0`
  - Port `3001`
- API namespace:
  - `/api/v1/*`
- Real-time:
  - Socket.IO attaches to the same HTTP server as the API
- Data/services:
  - Supabase is the primary persistence layer
  - Optional Redis env vars exist but Redis is not core to normal local startup

### External Integrations

- Supabase
  - Primary database access and admin queries
- Google Maps
  - Used in rideshare and map/group/activity experiences
- Resend
  - Email verification and password reset
- WeChat
  - URL link / mini-program related support is present in backend services and auth flow

## 5. Actual Code Layout

Canonical project tree:

```text
CampusRide/
├── README.md
├── LLM_PROJECT_GUIDE.md
├── integration-local-localhost/
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/
│   │   ├── stores/
│   │   ├── views/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── utils/
│   │   └── assets/
│   ├── docs/
│   └── campusride-backend/
│       ├── package.json
│       ├── .env.example
│       ├── src/
│       │   ├── server.js
│       │   ├── app.js
│       │   ├── routes/
│       │   ├── controllers/
│       │   ├── services/
│       │   ├── middleware/
│       │   ├── config/
│       │   └── utils/
│       ├── database/
│       └── tests/
├── integration-production/
└── integration_backup_local_1.2.9/
```

## 6. Frontend Mental Model

### Frontend Entry Points

- `src/main.js`
  - Creates app
  - installs router, Pinia, Ant Design Vue
  - initializes auth state
  - installs app recovery behavior after long inactivity
- `src/App.vue`
  - wraps page content with shared `HeaderComponent` and `FooterComponent`
  - hides layout chrome for routes that set `meta.hideNavigation`

### Frontend State

Current top-level Pinia stores:

- `src/stores/auth.js`
- `src/stores/activity.js`
- `src/stores/message.js`

Operationally important stores:

- `auth.js`
  - user session and auth initialization
- `message.js`
  - threads, unread counts, message selection, real-time message UX
- `activity.js`
  - activity-related shared state

### Frontend Routes

The current router is more expansive than some older docs suggest.

Primary routes include:

- Public/auth:
  - `/login`
  - `/register`
  - `/verify-email/:token`
  - `/resend-verification`
  - `/forgot-password`
  - `/reset-password/:token`
- Main product:
  - `/rideshare`
  - `/rideshare/:id`
  - `/activities`
  - `/activities/create`
  - `/activities/history`
  - `/activities/:id`
  - `/marketplace`
  - `/marketplace/:id`
  - `/marketplace/my-items`
  - `/marketplace/favorites`
  - `/leaderboard`
  - `/groups`
  - `/groups/:id`
  - `/messages`
  - `/profile/:userId`
  - `/admin`
- Misc/public:
  - `/terms`
  - `/privacy`
  - `/cookies`
  - `/carpool-disclaimer`
  - `/disclosures`
  - `/test-avatar`

Important note:

- The route names and actual paths use `rideshare`, not just `carpooling`
- The app title string in router metadata says `CampusGo` in many places, which suggests partial rebranding or legacy naming still in code

### Frontend Views Inventory

Main views currently present include:

- `LoginView.vue`
- `RegisterView.vue`
- `EmailVerificationView.vue`
- `ForgotPasswordView.vue`
- `ResetPasswordView.vue`
- `RideshareView.vue`
- `ActivitiesView.vue`
- `CreateActivityView.vue`
- `ActivityDetailView.vue`
- `ParticipationHistoryView.vue`
- `MarketplaceView.vue`
- `MyMarketplaceItems.vue`
- `MyFavoritesView.vue`
- `LeaderboardView.vue`
- `GroupMapView.vue`
- `GroupDetailView.vue`
- `MessagesView.vue`
- `UserProfileView.vue`
- `AdminView.vue`
- legal-policy related views

## 7. Backend Mental Model

### Backend Entry Points

- `src/server.js`
  - validates required env vars
  - starts HTTP server
  - initializes Socket.IO
  - can trigger optional DB init/sample data
  - starts cleanup service unless disabled
- `src/app.js`
  - builds Express app
  - sets trust proxy
  - installs helmet, cors, rate limiting, parsers, morgan
  - mounts all route groups
  - exposes Swagger at `/api-docs`

### Backend Route Groups

Mounted route families include:

- `/api/v1/health`
- `/api/v1/auth`
- `/api/v1/users`
- `/api/v1/leaderboard`
- `/api/v1/notifications`
- `/api/v1/points`
- `/api/v1/activities`
- `/api/v1/rideshare`
- `/api/v1/marketplace`
- `/api/v1/groups`
- `/api/v1/thoughts`
- `/api/v1/visibility`
- `/api/v1/carpooling`
- `/api/v1/messages`
- `/api/v1/upload`
- `/api/v1/ratings`
- `/api/v1/friends`
- `/api/v1/admin`
- `/api/v1/announcements`
- `/api/v1/webhook`

There is also a check-in route file mounted directly under `/api/v1`, so some activity check-in paths are not nested in the same way as the main activity router.

### Backend Controller Domains

Controller coverage shows the backend supports more than the shortest README summary:

- auth
- user and user profile
- rideshare and carpooling
- marketplace and marketplace comments
- activities, activity comments, activity chat, activity check-in
- groups
- friends
- thoughts
- visibility
- messages and system messages
- notifications
- points
- leaderboard
- ratings
- uploads
- admin
- announcements

### Backend Real-Time Layer

Socket.IO responsibilities currently include:

- JWT-based socket authentication
- guest user socket support
- online/offline presence broadcast
- activity room join/leave
- message thread room join/leave
- typing indicators
- real-time notification/message fanout

Main socket room patterns:

- `user:{userId}`
- `activity:{activityId}`
- `thread:{threadId}`

## 8. Data And Persistence Model

The persistent backend uses Supabase as the main data layer. Based on docs and code shape, major table domains include:

- users
- rides / ride bookings
- marketplace items / favorites / comments
- groups / members
- thoughts
- visibility
- activities / participants / check-ins / comments / chats
- notifications
- messages and system-message-related records
- points and leaderboard-related tables
- ratings
- announcement / webhook-supporting tables

This repo contains multiple migration and data-maintenance scripts, but the migration story is not centralized in one obvious modern folder. Expect operational scripts to be spread between:

- `campusride-backend/database/`
- root/backend helper scripts such as `run-*.js`, `*.mjs`, and shell helpers

## 9. Runtime And Environment Variables

### Frontend

Minimal frontend env from `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:3001
```

Also used in code:

- `VITE_GOOGLE_MAPS_API_KEY`
- `VITE_APP_STALE_RELOAD_MS`
- optional `VITE_HOST`

Important behavior:

- The Axios client expects `VITE_API_BASE_URL` to be the backend origin, not the `/api/v1` path
- It then appends `/api/v1` internally
- Socket connections in `MessagesView.vue` derive the socket host from that same base URL

### Backend

Key backend env vars:

```env
NODE_ENV=development
PORT=3001
FRONTEND_URL=http://localhost:5173
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...
JWT_SECRET=...
JWT_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
RESEND_API_KEY=...
RESEND_FROM_EMAIL=...
RESEND_FROM_NAME=Campus Ride
```

Additional optional env families exist for:

- `DATABASE_URL`
- `REDIS_URL`
- `BIND_HOST`
- `INIT_DATABASE`
- `CREATE_SAMPLE_DATA`
- `ENABLE_CLEANUP_SERVICE`
- WeChat integration:
  - `WECHAT_APPID`
  - `WECHAT_APPSECRET`
  - `WECHAT_MINI_WEBVIEW_PATH`
  - `WECHAT_MINI_WEBVIEW_QUERY_KEY`
  - `WECHAT_MINI_ENV_VERSION`
  - `DISABLE_WECHAT_FEATURES`
  - `DISABLE_WECHAT_AUTH`

## 10. How To Run Locally

### Frontend

```bash
cd integration-local-localhost
npm install
npm run dev
```

Expected local URL:

- `http://127.0.0.1:5173`

### Backend

```bash
cd integration-local-localhost/campusride-backend
npm install
npm run dev
```

Expected local URL:

- `http://localhost:3001`
- Swagger: `http://localhost:3001/api-docs`

### Combined

At repo root there are helper scripts such as:

- `server-manager.sh`
- `start-services.sh`

These are convenience wrappers, not the cleanest source of architecture truth.

## 11. What Makes This Repo Confusing

If an LLM gets confused in this repo, it will usually be because of one of these issues:

- Multiple parallel app snapshots exist in the same repository
- Several markdown files are task reports, not enduring documentation
- Some docs still refer to an old `integration/` directory that is no longer the active path
- There are mixed naming conventions:
  - `CampusRide`
  - `CampusGo`
  - `rideshare`
  - `carpooling`
- Some backend integrations look optional in one place and mandatory in another
- There are backup files such as `.vue.backup` that should not be treated as current implementation

## 12. Known Documentation Drift

Important mismatches to remember:

- Current active directory is `integration-local-localhost/`, not `integration/`
- Frontend dev port in current Vite config is `5173`, not `3000`
- Root `README.md` is the best short overview, but some internal doc links still point to old paths
- `docs/PROJECT_SUMMARY.md` is broad but partly stale
- `docs/ARCHITECTURE_OVERVIEW.md` is useful for conceptual architecture, but not a fully trustworthy source for current route and directory details

## 13. Best Reading Order For An LLM

If an LLM needs to quickly orient itself in the actual code, use this order:

1. Read this file: `LLM_PROJECT_GUIDE.md`
2. Read root `README.md`
3. Read frontend router:
   - `integration-local-localhost/src/router/index.js`
4. Read frontend API layer:
   - `integration-local-localhost/src/utils/api.js`
5. Read backend app/bootstrap:
   - `integration-local-localhost/campusride-backend/src/app.js`
   - `integration-local-localhost/campusride-backend/src/server.js`
6. Read the relevant frontend store or view for the feature being changed
7. Read the matching backend route + controller pair

## 14. Best Interpretation Of The Product

The best short description of this codebase is:

`CampusRide` is a multi-module campus platform centered on student coordination and community activity. It combines rideshare, marketplace, events, groups, messaging, notifications, and point-based engagement in a Vue 3 + Express + Supabase architecture with real-time updates over Socket.IO.

## 15. Practical Guidance For Future Contributors Or LLMs

- Do new work inside `integration-local-localhost/` unless explicitly targeting another snapshot
- Verify routes and env defaults from code, not from older markdown docs
- Be careful with naming drift between “rideshare” and “carpooling”
- Check both frontend route names and backend route mounts before assuming endpoint names
- Treat root-level summary docs as historical context, not authoritative system design
- When documenting the project elsewhere, point readers to this file first
