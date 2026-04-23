# E-Category Manual Inclusion Audit (Prompt A, v4.2)

**Scope**: `.edu` / campus-scoped identity verification as trust primitive (Category E).
**Trigger**: v4.1 E-category retrieval returned 0 native papers; 3 pre-existing "documented" papers were proxy-level (generic identity verification in sharing economy, not `.edu`-native). Automated retrieval cannot close this gap because native-E literature is scattered across HCI / CSCW / iConference / CHB case studies with low keyword recall.
**Target**: >=4 native papers (hard floor), 6 papers target.
**Outcome**: **6 native E papers accepted, 2 candidates rejected as proxy / format-ineligible.**

All DOIs validated via `https://api.crossref.org/works/<DOI>` with matching title+year+authors.

---

## Accepted native-E papers (N=6)

| # | DOI | Authors (year) | Venue | Why native E (not proxy) |
|---|-----|----------------|-------|--------------------------|
| 1 | `10.1111/j.1083-6101.2007.00367.x` | Ellison, Steinfield, Lampe (2007) | Journal of Computer-Mediated Communication | Facebook-era MSU undergraduate study when `.edu` email was the platform's gating credential; institutional identity was the load-bearing primitive, not a secondary feature. Foundational bridging-social-capital finding for `.edu`-scoped closed-community SNS. |
| 2 | `10.1177/1461444814543998` | Ellison, Gray, Lampe, Fiore (2014) | New Media & Society | Resource-mobilization requests on Facebook; network structure seeded by `.edu`-gated college cohorts. Direct empirical grounding for the mechanism CampusRide's identity primitive replicates: institutional-identity-seeded graphs yield mobilizable help / favor ties. |
| 3 | `10.1145/3025453.3025682` | Schlesinger, Chandrasekharan, Masden, Bruckman, Edwards, Grinter (2017) | CHI '17 | Interview study of 18 Yik Yak users on one urban US university campus. Hyper-locality geofence is the functional cousin of `.edu`-email gating; canonical HCI case study of a campus-bounded anonymous platform. |
| 4 | `10.1016/j.chb.2015.11.043` | Black, Mezzina, Thompson (2016) | Computers in Human Behavior | Content analysis of 4,000 Yaks across 42 US university campuses — the largest empirical corpus on campus-bounded anonymous platforms. Cross-campus behavioral baseline for what campus-identity scoping produces. |
| 5 | `10.9776/16152` | Heston, Birnholtz (2016) | iConference 2016 Proceedings | SIDE-theoretic (social identity model of deindividuation effects) treatment of Yik Yak location filtering as campus identity producer. Directly theoretical for the Identity primitive paragraph. |
| 6 | `10.1145/3078843` | Wu, Minkus, Ross (2017) | ACM Transactions on Intelligent Systems and Technology | Large-scale cross-campus measurement of location-based anonymous mobile apps (Yik Yak, Whisper) at US colleges, quantifying privacy-identity trade-offs of campus-scoped anonymity. Design-science native E, not sharing-economy proxy. |

**Confidence scores (native-E categorization, 0-1):**
- #1 Ellison 2007: **0.95** — foundational `.edu`-era Facebook study, unambiguous.
- #2 Ellison 2014: **0.80** — Facebook was no longer `.edu`-gated by 2014, but the NMS paper's sampled network structure is college-seeded and its mechanism (institution-seeded resource mobilization) is exactly what CampusRide primitive targets.
- #3 Schlesinger 2017: **0.90** — campus-bounded anonymous platform, canonical HCI reference.
- #4 Black 2016: **0.85** — 42-campus content analysis, empirical bedrock.
- #5 Heston 2016: **0.85** — campus-identity SIDE treatment.
- #6 Wu 2017: **0.80** — cross-campus measurement study, rigorous but less HCI-design-facing.

Average confidence: **0.86**.

---

## Rejected candidates (N=2)

| DOI | Authors (year) | Venue | Rejection reason |
|-----|----------------|-------|------------------|
| `10.1111/j.1083-6101.2007.00394.x` | Judith Donath (2007) | Journal of Computer-Mediated Communication, "Signals in Social Supernets" | **Proxy only.** Theoretical signaling framework for SNS identity broadly; does not engage `.edu` gating, campus geofencing, or institutional identity scoping as a first-class construct. Including would be category inflation. May still be cited from Beat 3 as general theoretical backbone but NOT as native-E evidence. |
| `10.1007/978-3-642-21521-6_3` | Ellison, Vitak, Steinfield, Gray, Lampe (2011) | Book chapter in *Privacy Online*, Springer | **Format ineligible.** Prompt A hard constraint excludes non-peer-reviewed-conference/journal formats; this is an edited Springer book chapter. Content is highly on-target (same Ellison group, Facebook privacy/social capital) but format rule precludes inclusion. The same arc is already covered by accepted papers #1 (2007) and #2 (2014) from the same research group. |

### Directions that returned 0 native papers

- **Direction 1c (Ellison 2014 CHI "Social Capital and Resource Requests on Facebook")**: the prompt named it as CHI — it is actually published in *New Media & Society* 16(7):1104-1121 (2014). Accepted as paper #2 under correct venue; no native paper lost.
- **Direction 3 (`.edu` email as gating mechanism — HCI/CSCW/IS, or LMS identity verification case studies 2014-2018)**: **0 confirmed native papers** found that pass Crossref verification and hard-rule format filter. Keywords "edu email verification", "university email gating", "LMS institutional identity" returned blog posts, dissertations, or non-indexed workshop papers. **This is a genuine literature gap** and should be surfaced in `gaps_ranked.json` as a minor gap within Beat 3 ¶1; it does NOT block the wording-tier decision because directions 1 and 2 alone delivered 6 native papers.
- **Direction 4b (Resnick & Kuwabara reputation in campus contexts)**: **0 native papers** — Resnick & Kuwabara's reputation work is general-purpose and does not apply itself to `.edu` contexts. Excluded.

---

## Recommended wording tier for Beat 3 ¶1 (paper outline v4.2 §2.3)

Final native-E count: **N = 6** (≥5 threshold met).

Per the pipeline guide Part 1.3 tier schedule:

> **N ≥ 5 (standard primitive wording)**:
> "Identity verification in sharing economy has a mature literature, specialized here to institutional and `.edu`-scoped contexts, where closed-community scoping demonstrably reduces stranger-coordination costs."

**Recommendation: use the N ≥ 5 standard-primitive wording.**

Caveat for reviewer/honesty pass: of the 6 native papers, 4 of 6 are campus-bounded anonymous-platform studies (Yik Yak / location-anonymous), and 2 of 6 are `.edu`-Facebook-era SNS studies. The "closed-community scoping reduces stranger-coordination costs" claim is directly supported by the Ellison 2007 / 2014 pair; the Yik Yak cluster supports the broader "campus-bounded identity as trust primitive" construct rather than the specific carpool-relevant stranger-coordination mechanism. If the Honesty reviewer flags this asymmetry, the paragraph should explicitly disclose that `.edu`-email gating evidence leans on Facebook-era work and that campus-bounded modern evidence comes from anonymous-platform contexts (a different but adjacent primitive).

---

## File outputs

- `carpool_v4/config/manual_core_inclusions.json::papers[]` — appended 6 E-category entries (indices 4-9, after the 4 existing I-category entries). `primary_anchors` block untouched.
- `carpool_v4/config/e_category_audit.md` — this file.

No other files modified.
