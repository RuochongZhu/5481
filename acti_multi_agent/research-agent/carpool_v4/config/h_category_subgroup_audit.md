# H-Category Subgroup Audit (Prompt E, v4.2)

> Scope: H-subgroup / H-amateur manual inclusions added to `config/manual_core_inclusions.json::papers[]` to support the driver-subset rating-fairness finding (F5) in paper outline v4.2 §4.2 Beat 5 and §5.8.3.
>
> Driving claims (from pipeline_v4.2_modification_guide.md Part 3):
>
> - **X1**: Rating sensitivity differs between active drivers and passive raters (asymmetric, not symmetric).
> - **X2**: Amateur / occasional drivers (NOT professional gig workers) also show rating anxiety — rating anxiety is not a product of full-time platform-labor bargaining alone.
> - **X3**: Defensive methodology citation for reporting a descriptive rating finding on a small subset (N=19).

All DOIs below validated against `https://api.crossref.org/works/<DOI>` (HTTP 200, matching title + authors + year).

---

## Accepted Papers by Direction

### Direction 1 — X1 (two-sided rating asymmetry, driver vs passenger perspective)

**1 paper accepted.**

| # | DOI | Citation | Venue | Year | Secondary label | Claim |
|---|-----|----------|-------|------|-----------------|-------|
| 1 | `10.1287/mksc.2021.1311` | Fradkin, Grewal & Holtz, "Reciprocity and Unveiling in Two-Sided Reputation Systems: Evidence from an Experiment on Airbnb" | Marketing Science | 2021 | `H-subgroup` | X1 |

**Routing**: §4.2 Beat 5 ¶3 (asymmetry anchor) + §5.8.3 (design rationale for the reveal-window / dispute-window decision).

**Why it is a legitimate asymmetry citation, with scoping note**:
- Airbnb field experiment manipulates *when* each side's rating becomes visible. The treatment (hidden until both submit) reduced retaliation and reciprocation and lowered ratings — direct causal evidence that the two sides of a peer marketplace behave asymmetrically toward the rating system, and that architectural choices change that asymmetry.
- **Framing caveat (required by Prompt E)**: this is an econ/marketplace "fairness" framing — not HCI's design-research framing. We cite strictly for the asymmetry mechanism (reveal-timing → behavior change), not for normative fairness claims. Beat 5 ¶3 wording should reference "two-sided reveal-timing asymmetry documented in marketplace studies" rather than importing the econ fairness vocabulary wholesale.

---

### Direction 2 — X2 (amateur / non-professional / P2P carpool driver rating experience)

**2 papers accepted — native match achieved (NOT zero native).**

| # | DOI | Citation | Venue | Year | Secondary label | Claim |
|---|-----|----------|-------|------|-----------------|-------|
| 2 | `10.1007/s10606-022-09461-4` | Neifer, Bossauer, Pakusch, Boehm & Lawo, "Trust-Building in Peer-to-Peer Carsharing: Design Case Study for Algorithm-Based Reputation Systems" | Computer Supported Cooperative Work (CSCW) | 2023 | `H-amateur` | X2 |
| 3 | `10.1016/j.jclepro.2025.144661` | Hartl, Penz & Schuessler, "Creating a Trusting Environment in the Sharing Economy: Unpacking Mechanisms for Trust-Building Used by Peer-to-Peer Carpooling Platforms" | Journal of Cleaner Production | 2025 | `H-amateur` | X2 |

**Routing**: §4.2 Beat 5 ¶3 (amateur-driver extension) + §7.2 Beat 7 ¶2 (scoping), and Neifer specifically into §5.8.3 (rating-system design with fairness consideration).

**Why these are legitimately "amateur / peer driver" and NOT professional-gig-worker papers**:
- Neifer et al. 2023 (CSCW): participants are *private car owners* on Turo/Getaround-style platforms sharing their own vehicles with strangers. Explicitly studies how these owners experience biased/fake ratings. HCI/CSCW venue, native to the design-research community CampusRide is in dialogue with.
- Hartl, Penz & Schuessler 2025 (JCP): studies BlaBlaCar, Oszkar, Zego, Carpul — all P2P carpool platforms where drivers are not professional wage workers. Mixed-method (qualitative cross-platform comparison + N=163 laboratory experiment). Directly documents that review/rating systems have **different consequences for car owners vs non-car-owners** and **for more vs less experienced users** — a structural parallel to our Driver/Both vs Rider-only subset split, making it a particularly load-bearing citation for the X2 extension.

**Hard rule compliance**: Neither Neifer et al. nor Hartl et al. study professional gig labor. Rosenblat & Stark (2016) and Lee et al. (2015) — the existing H-category anchors — stay in the corpus for Beat 5 ¶1 framing and Beat 7 ¶1 (Formalization Risk), but the *X2 extension* in Beat 5 ¶3 is now supported by native amateur-driver literature, not by stretching professional-gig-worker papers.

---

### Direction 3 — X3 (small-sample rating methodology / robustness defense)

**1 paper accepted.**

| # | DOI | Citation | Venue | Year | Secondary label | Claim |
|---|-----|----------|-------|------|-----------------|-------|
| 4 | `10.1145/2858036.2858498` | Kelly Caine, "Local Standards for Sample Size at CHI" | CHI 2016 | 2016 | `H-subgroup` | X3 |

**Routing**: §4.2 Beat 5 ¶2 (subset-selection methodological justification) + §7.2 Beat 7 ¶2 (Sample Skew disclosure).

**Why it is a legitimate methodology-defense citation**:
- Systematic analysis of *all* CHI 2014 papers. Documents that CHI sample sizes range from 1 to 916,000, with a **modal value of N=12**, and that accepted distributions vary by study type. This is the canonical local-standards reference in the HCI community.
- Provides a citable basis for reporting a descriptive rating finding on N=19 (Driver/Both subset) without implying inferential claims. Caine's data shows our N=19 is above the CHI modal sample size, which directly supports the §4.2 ¶2 subset-justification argument that the N=19 choice is methodologically principled, not a convenience cut.

---

## Summary Counts

| Direction | Accepted | Target | Hard-fail threshold | Status |
|-----------|----------|--------|---------------------|--------|
| 1 (X1) | 1 | ≥ 1 | — | pass |
| 2 (X2) | 2 | ≥ 1 (hard-fail = 0) | 0 | **pass (native match, not zero)** |
| 3 (X3) | 1 | ≥ 1 | — | pass |
| **Total** | **4** | | | |

**Secondary-label distribution**: `H-subgroup` ×2 (Fradkin 2021, Caine 2016); `H-amateur` ×2 (Neifer 2023, Hartl 2025).

---

## Direction 2 Explicit Outcome Statement

**Direction 2 returned NATIVE MATCH (non-zero).** Two papers directly address peer-to-peer amateur-driver rating experience without reverting to professional-gig-worker literature:

1. Neifer et al. 2023 (CSCW, HCI venue, Turo/Getaround-style private owners).
2. Hartl, Penz & Schuessler 2025 (Journal of Cleaner Production, BlaBlaCar + three other P2P carpool platforms, includes N=163 lab experiment on trust-building mechanisms with car-owner vs non-owner split).

Because Direction 2 is non-zero, the **outline's fallback wording in §4.2 Beat 5 ¶3** ("We extend this concern from professional gig work to an amateur driver context *without direct literature precedent*") is **NOT** required. The stronger wording is justified — cite Neifer 2023 and Hartl et al. 2025 as direct precedent for amateur-driver rating concerns and frame the extension as "resonates with a small but growing P2P-carpool literature."

No entry needs to be added to `gaps_ranked.json` for Direction 2.

---

## Rejected Candidates

| Candidate | Why considered | Rejection reason |
|-----------|---------------|------------------|
| Rosenblat & Stark 2016 (IJoC), "Algorithmic Labor and Information Asymmetries" | Classic H-category anchor, touches rating anxiety | NOT H-subgroup / H-amateur — studies professional Uber drivers. Stays as Beat 5 ¶1 framing and Beat 7 ¶1 anchor, but does NOT support X2. Keeping this paper out of the H-subgroup label set enforces the Prompt E hard rule. |
| Lee, Kusbit, Metsky & Dabbish 2015 (CHI), "Working with Machines" | Driver-side algorithmic management | Same as Rosenblat & Stark: professional Uber/Lyft labor, not amateur. Valid H anchor, invalid as X2 support. Not relabeled. |
| Lauterbach, Truong, Shah & Adamic 2009 (CSE/SocialCom), "Surfing a Web of Trust: Reputation and Reciprocity on CouchSurfing.com" (`10.1109/cse.2009.345`) | CouchSurfing peer-to-peer trust and reciprocity — structurally adjacent to peer driver rating | CouchSurfing is not carpool-adjacent (hospitality exchange, no driver role); reciprocity evidence is interesting but weaker than the Fradkin Airbnb field experiment for X1 and off-topic for X2. Not included to keep the H-subgroup label set tightly load-bearing. Could be added later as a Beat 3 supporting cite if needed, not as H-subgroup. |
| Farajallah, Hammond & Pénard 2019 (Information Economics and Policy), "What Drives Pricing Behavior in Peer-to-Peer Markets? Evidence from BlaBlaCar" (`10.1016/j.infoecopol.2019.01.002`) | BlaBlaCar empirical study, relevant P2P setting | Focus is on pricing behavior and ethnicity-driven discrimination, not directly on driver rating anxiety or reveal-timing asymmetry. Would also duplicate the P2P-carpool slot better filled by Hartl et al. 2025 (which directly compares trust-building mechanisms and has the owner-vs-non-owner split paralleling our subset split). Not included. |
| Bellotti, Ambard, Turner, Gossmann, Demková & Carroll 2015 (CHI), "A Muddle of Models of Motivation for Using Peer-to-Peer Economy Systems" (`10.1145/2702123.2702272`) | Native CHI paper on P2P motivations | About motivational mismatch between providers and users, not rating anxiety specifically. Strong paper but off-target for X1/X2. Candidate for Beat 2 or Beat 3 general-P2P support if later needed, not H-subgroup. |
| Wutich, Beresford & Bernard 2024 (International Journal of Qualitative Methods), "Sample Sizes for 10 Types of Qualitative Data Analysis" (`10.1177/16094069241296206`) | Broad sample-size guidance | Valid methodology reference but not HCI-venue. Caine 2016 (CHI) is a stronger local-standards citation for our HCI paper and targets §4.2 ¶2 more directly. Caine chosen over Wutich. |

---

## Impact on Beat 5 ¶2 / ¶3 Wording (Feedback to Outline)

### §4.2 Beat 5 ¶2 (subset-selection methodological justification)

Recommended additions to the existing wording:

- Cite **Caine 2016** in the sentence "We do not perform inferential statistics; N=19 is small but the subset-level observation is meaningful." Specifically: "The modal sample size in CHI-published work is N=12 (Caine 2016); our N=19 descriptive observation is within the CHI local-standards distribution for formative design research, and we report it as descriptive rather than inferential."

### §4.2 Beat 5 ¶3 (literature dialogue)

Outline's *current* hedged language: "若 Prompt E 方向 2 无适配文献：降级措辞为 'We extend this concern from professional gig work to an amateur driver context without direct literature precedent'."

**Recommended upgrade** (because Direction 2 is non-zero):

- Replace the fallback hedge with the stronger form: "Rating anxiety is not a product of professional-labor bargaining alone — a small but growing P2P-carpool literature (Neifer et al. 2023; Hartl, Penz & Schuessler 2025) documents similar concerns in amateur-driver settings, and our Driver/Both subset observation resonates with this emerging pattern."
- Keep the `resonates with / parallels` verb discipline. Do **not** escalate to `confirms` or `replicates` — Neifer's N=16 interviews + N=12 evaluation and Hartl et al.'s four-platform qualitative + N=163 lab experiment are supporting evidence, not a confirmatory replication of our survey.
- Add the Fradkin, Grewal & Holtz 2021 citation with an explicit HCI-vs-econ framing caveat: "Platform-side marketplace studies (Fradkin, Grewal & Holtz 2021) further document that the two sides of a peer marketplace respond asymmetrically to rating-system architecture, though those studies use an econ fairness framing distinct from HCI's."

### §5.8.3 (Rating System with Fairness Consideration)

- Use Fradkin et al. 2021 to justify the reveal-window / dispute-window design decision (their treatment condition hides feedback until both submit).
- Use Neifer et al. 2023 to frame the algorithmic-scoring choice as a design pattern already being explored in CSCW for amateur P2P drivers.

### §7.2 Beat 7 ¶2 (Sample Skew)

- Use Caine 2016 to frame "N=19 is small but within CHI local standards for descriptive / formative work" rather than as an apologetic caveat. This strengthens the `scope-limited` verb discipline without softening the honest acknowledgement.

---

## Phase 3 Edge Requirements (Pipeline Hook)

Per pipeline_v4.2 Prompt D §5.2 "H-subgroup special processing":

- The four papers added above must have `CONCEPTUAL_OVERLAP` edges with `weight=1.0` to `evidence_inventory[4]` (F5, the driver-subset rating-fairness finding) when Phase 3 is re-run.
- Specifically:
  - Fradkin 2021 ↔ F5: asymmetric rating behavior mechanism.
  - Neifer 2023 ↔ F5: amateur peer driver rating concerns.
  - Hartl et al. 2025 ↔ F5: P2P-carpool owner-vs-non-owner trust-building split (structural parallel to Driver/Both vs Rider-only).
  - Caine 2016 ↔ F5: methodological validity of the N=19 descriptive observation.

---

**Audit produced**: 2026-04-22
**Audit author role**: H-subgroup curator (Prompt E)
**Aligned document**: `paper_outline_v4.2.md` (§4.2 Beat 5, §5.8.3, §7.2 Beat 7)
