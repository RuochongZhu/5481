# I Category Audit (Prompt B, pipeline v4.2)

> **Date**: 2026-04-22
> **Auditor**: I-category curator (auto)
> **Scope**: Paper outline v4.2 §2.2 Beat 2 ¶3 — "校园多模块集成设计空间" argument
> **Hard requirement**: ≥3 native closed-community / bounded-scope I papers

---

## 1. Pre-supplement coverage snapshot (from `data/processed/classified.json`)

| # | Year | Title (truncated) | Venue | Native I? |
|---|------|-------------------|-------|-----------|
| 1 | 2024 | Local super apps in the 15-minute city | Frontiers in Sustainable Cities | Borderline — bounded urban scope, but not HCI/CSCW; proxy-ish |
| 2 | 2024 | Persepsi Publik Digitalisasi Layanan Pusaka Kemenag | Da'watuna (communication journal) | No — government digitization, mass-audience |
| 3 | 2026 | SANTER Super-App for Samarinda Smart City (DOI a) | Zenodo preprint | No — smart-city mass platform, non-peer-reviewed venue |
| 4 | 2026 | SANTER Super-App (DOI b, duplicate) | Zenodo preprint | No — duplicate |
| 5 | 2026 | SANTER Super-App (DOI c, duplicate) | Zenodo preprint | No — duplicate |
| 6 | 2026 | NeoPlace: Smart Career Assistant | IEMENTech 2026 | No — engineering demo, not sociotechnical |
| 7 | 2025 | Polri Super App Presisi SKCK Service | Jurnal Teori Riset Adm. Publik | No — public-admin mass platform |

**Pre-supplement native closed-community / HCI-bounded I count: 0 (paper #1 is borderline and alone is insufficient).**

This confirms the Prompt B hypothesis: automated retrieval surfaced mostly mass-market super-app / smart-city government platform papers. Prompt B explicitly says these are **not** native I for CampusRide because they don't match the closed-community bounded scope. Manual supplement is required.

---

## 2. Supplement search & selection

Four directions from Prompt B were searched (WebSearch + Crossref DOI verification). Each candidate below was validated against `https://api.crossref.org/works/<doi>`.

### 2.1 Accepted (appended to `manual_core_inclusions.json::papers[]`)

| # | DOI | Title | Venue | Year | Why native |
|---|-----|-------|-------|------|------------|
| S1 | 10.1145/2675133.2675198 | Dwelling Places in KakaoTalk: Understanding the Roles and Meanings of Chatrooms in Mobile Instant Messengers | CSCW '15 | 2015 | KakaoTalk super-app unit of analysis is **bounded chatrooms** (primary/secondary/tertiary regions) — closed-scope sociotechnical framing inside an integrated platform. HCI/CSCW native. |
| S2 | 10.1177/2056305117703815 | Digital Genealogies: Understanding Social Mobile Media LINE in the Role of Japanese Families | Social Media + Society | 2017 | LINE is a super-app, but this paper studies LINE integration **inside the closed boundary of a family unit** — bounded-community embedded use, not mass-market behaviour. |
| S3 | 10.1145/3313831.3376274 | Please Call the Specialism: Using WeChat to Support Patient Care in China | CHI '20 | 2020 | Nurse-facilitated patient groups inside WeChat — **closed professional-clinic scope**, integrated coordination infrastructure. CHI venue. Directly parallels CampusRide's closed-campus-scope integration argument. |
| S4 | 10.1177/2056305120933285 | LINE as Super App: Platformization in East Asia | Social Media + Society | 2020 | **Theoretical / platform-studies backbone**, not empirical closed-community evidence. Used only to frame super-app platformization so CampusRide's closed-scope can be positioned against it. Explicitly flagged in rationale to avoid category inflation. |

**Post-supplement native-or-theoretical I count: S1 + S2 + S3 (3 native bounded-scope) + S4 (1 theoretical backbone) = 3 native + 1 theory.**

**Hard requirement "≥ 3 native closed-community" — met with S1, S2, S3.**

### 2.2 Rejected candidates (with reasons)

| Candidate | DOI / source | Reject reason |
|-----------|--------------|---------------|
| Azarova, Hazoglou & Aronoff-Spencer "Just Slack it" (2022, New Media & Society, 10.1177/1461444820975723) | Verified | Enterprise collaboration only; Prompt B §2.4 says Slack/Teams research is at best "methodological parallel, not direct precedent". Not closed-community in the campus sense; would inflate I if booked as native. Keep as potential methodology-mirror edge, not manual inclusion. |
| Zhang & Cranshaw "Making Sense of Group Chat" (CSCW 2018, 10.1145/3274465) | Verified | Slack/Flock group-chat tooling — methodological parallel only, not a study of integrated multi-module bounded community. Same reason as above. |
| Lin, Zagalsky, Storey & Serebrenik "Why Developers Are Slacking Off" (CSCW 2016 companion) | Verified short paper | Short / workshop-style paper on software-engineering teams — Prompt A/B exclude workshop shorts, and the scope (developer teams) is not closed-community in CampusRide's sense. |
| Stoeckli et al. "Exploring Affordances of Slack Integrations" (HICSS 2018) | Exists | Enterprise bot-integration study — direct proxy for multi-module platform logic but in mass-enterprise, not closed-community. Methodological parallel only. |
| Pre-supplement papers #2–#7 (Zenodo SANTER / Polri / Kemenag / NeoPlace) | Already classified in corpus | Mass-market smart-city government super-apps or engineering demos — Prompt B §2.4 explicitly excludes these. They remain in corpus for completeness but are **not** counted toward native I. |
| "Local super apps in the 15-minute city" (#1 above) | Already in corpus | Bounded urban scope is closer to native-adjacent, but the venue (Frontiers in Sustainable Cities) is not HCI/CSCW and the framing is urban-sustainability rather than sociotechnical coordination. Keep in corpus but do not count as native-HCI I. |
| Generic "WeChat and civil society" (Harwit 2017) | Exists | Policy/civil-society framing of mass-platform WeChat — not closed-community in the CampusRide sense. Reject. |

### 2.3 Direction-by-direction summary (Prompt B §2.2 list)

| Direction | Result |
|-----------|--------|
| 1. Enterprise all-in-one (Slack, Teams) | No acceptances — Prompt B allows these only as methodological parallel, and we honored that. Several candidates considered and rejected (see 2.2). |
| 2. Higher-ed integrated platforms (Canvas, Blackboard modules) in L@S / CHI | No suitable native peer-reviewed HCI paper surfaced that treats LMS modularity as the sociotechnical unit of analysis. Most hits are comparative/operational literature (ResearchGate systematic reviews, non-HCI venues). Reported as a gap. |
| 3. Closed-community super-apps (KakaoTalk, LINE, bounded WeChat) | **Three acceptances (S1, S2, S3)** — this direction carried the audit. |
| 4. Sociotechnical theory of integrated platforms (Star & Bowker / platform studies / modularity) | **One acceptance (S4)** — Steinberg 2020 as theoretical backbone. Star & Bowker infrastructure classics were considered but kept out of manual inclusions because they predate the super-app discourse; they can still be cited in-text from standing references in Beat 3 / §6. |

### 2.4 Gap signal (for `gaps_ranked.json`, diagnostic only — not paper contribution per §6.3 honesty)

Direction 2 (higher-ed LMS modularity in HCI) returned no native match. This is a genuine under-explored space and should be logged as a pipeline gap signal, but per v4.2 honesty discipline it must **not** be framed in the paper as "we discovered a gap" — only as a scope statement in §6.3 and Beat 7.

---

## 3. Final N and tiered Beat 2 ¶3 wording recommendation

**Final native closed-community I count: N = 3** (S1 KakaoTalk CSCW '15, S2 LINE Families 2017, S3 WeChat Patient Care CHI '20). Plus one theoretical backbone (S4).

Per Prompt B hard requirement, the paper_outline_v4.2 §2.2 Beat 2 ¶3 wording archetype is:

### Tier A — N ≥ 5 (not applicable here)
> "Super-app and integrated community platform research has matured into an **established design space** with documented value propositions (e.g., [S1], [S2], [S3], [extra], [extra]). This literature provides validated primitives for cross-module coordination, enabling us to position CampusRide within a recognized lineage rather than as an isolated design case. Closed-community super-apps in particular demonstrate that bounded-scope integration is not a compromise against mass-market super-apps but a distinct sociotechnical configuration."

### Tier B — N = 3 (**recommended for current state**)
> "Integrated platform research in HCI/CSCW documents an **emerging design space** for closed-community super-apps, with several case studies examining bounded-scope uses of otherwise mass-market platforms (e.g., KakaoTalk chatrooms as dwelling places [S1], LINE inside Japanese families [S2], and WeChat inside nurse-facilitated patient groups [S3]). Platform-studies work on super-app platformization [S4] provides a theoretical backdrop. This literature **indicates** that bounded-scope multi-module coordination is a plausible design target, but a systematic treatment at the campus level is **less developed** — CampusRide contributes one case within this emerging space."
>
> **Verb discipline**: `document`, `indicate`, `emerging design space`, `several case studies`, `less developed`, `one case within`. Avoid `demonstrates`, `established`, `validated`.

### Tier C — N = 2 (fallback; not applicable here, but spec requires)
> "Research on closed-community integration within otherwise mass-market super-apps is **sparse and fragmented**, with only a handful of case studies at the chatroom / family / clinic scope ([best 2 of S1–S3]). We treat this as an **initial inquiry** rather than an established design space, and we frame CampusRide as a exploratory case that may help motivate future systematic work — not as validation of a settled framework. The absence of dedicated campus-scoped multi-module literature is itself a scoping observation."
>
> Adversarial framing mandatory: the thin literature base becomes part of Beat 7 honest-scoping, not hidden.

### Recommended action
Use **Tier B** for the first draft of §2.2 Beat 2 ¶3. Keep Tier C text in a draft comment so that if the E-category curator or query-expansion pass accidentally downgrades the count, the paper can demote wording without restructuring.

---

## 4. Hard-rule compliance checklist

- [x] Each appended entry has `paperId = "doi:<DOI>"` and `category = "I"`.
- [x] Every DOI is Crossref-verified (S1–S4 all returned valid records with matching titles/years/venues).
- [x] Each rationale explicitly states why the paper is **native closed-community / bounded-scope** or, for S4, explicitly flags it as **theoretical backbone, not closed-community proxy**.
- [x] No WeChat / Grab / Gojek **mass-market** business-model papers were counted as native I. The one WeChat paper accepted (S3) is clinic-scoped, not mass-market.
- [x] No Slack / Teams enterprise-collaboration paper was appended; they remain methodological-parallel edges only (§2.2).
- [x] No workshop short papers or preprints appended (Zenodo SANTER entries remain in corpus but are not manual inclusions).
- [x] File conflict safety: `manual_core_inclusions.json::papers[]` was empty at edit time (no concurrent E-curator additions). Entries were appended so future E additions can still be appended to the end.

---

## 5. Next-step hooks

1. After Prompt A (E curator) appends its entries, re-verify `papers[]` does not contain duplicate DOIs (none expected across E vs I, but good hygiene).
2. Re-run Phase 2 classification on the 4 supplemented DOIs so they land in `classified.json` with `primary_category = "I"` and `confidence ≥ 0.8`; set `needs_review = false`.
3. Phase 3.5 narrative chain for Beat 2 must use S1/S3 (HCI/CSCW native) as spine anchors, S2 as supporting bounded-scope case, S4 as theoretical citation — in that order per the tier-B wording above.
4. In Phase 3.7 contradiction scan, S4 (platformization critique) may produce a productive contradiction with S1/S3 (closed-scope case studies) on whether super-apps reduce or amplify coordination frictions — this is a **good** contradiction to preserve for Beat 7 §7.2.
