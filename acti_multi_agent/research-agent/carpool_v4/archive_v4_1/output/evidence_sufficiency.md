# Evidence Sufficiency Report

*Assessment of literature support for each beat of the paper*

---

## Beat 1: Small-Town Campus Transportation & Coordination Gaps 🟡 adequate

Supporting papers: 25
Key papers present: Examining network governance of multimodal integration: A comparative study of r
Key papers MISSING: Direct campus-specific study of rideshare scarcity in rural or small-town universities
Weakness: The corpus can motivate a narrower claim that rural/small-town mobility systems are coordination-heavy and often imperfect, with general peer-platform trust frictions layered on top. It does not directly establish that small-town university students are underserved by commercial ridesharing or that campus populations specifically compensate through peer coordination.

Evidence chain:
  → A papers show small-town/rural transit integration and governance challenges.
  → B papers show trust and participation frictions in sharing platforms.
  → Together they motivate the problem setting, but they are background motivation rather than direct proof of a campus rideshare gap.

---

## Beat 2: Grassroots Coordination and Integrated Campus Platforms 🟠 weak

Supporting papers: 18
Key papers MISSING: Direct study of WeChat or WhatsApp transport coordination among international students on campus, Integrated campus platform or campus super-app case study with service coordination functions
Weakness: This beat is only partially supported. C suggests messaging apps can enable community coordination in adjacent contexts, and D supports the broader importance of international-student support networks, but the leap to transport-specific self-organization is thin. I appears sparse, very recent, and weakly connected, so the move from grassroots chat groups to a multi-module campus platform remains more an informed inquiry than a well-established literature line.

Evidence chain:
  → C papers indicate messaging platforms can support community coordination, but mostly outside mobility-specific campus use.
  → D papers establish international students as a population with distinctive support and adjustment needs.
  → I papers only weakly support the integrated-platform move, so this beat supports a plausible premise, not a settled empirical claim.

---

## Beat 3: Four Design Primitives: Identity, Safety, Rating Fairness, Rewards 🟠 weak

Supporting papers: 16
Key papers present: Trust and reputation in the sharing economy: The role of personal photos in Airb, Fulfillment of the Work Games: Warehouse Workers' Experiences with Algorithmic M
Key papers MISSING: Institutional identity verification as a trust mechanism in closed-community sharing platforms, Two-sided rating fairness study for peer mobility or carpool platforms
Weakness: The framework has partial support, but the four primitives are not equally grounded. Identity verification appears especially under-supported as a direct literature line, safety evidence is thin, and the fairness and gamification literatures do not integrate into a coherent shared framework in this corpus. This means the primitives work better as defensible design proposals than as fully literature-derived necessities.

Evidence chain:
  → General trust/reputation work supports the need for trust signals beyond anonymous interaction.
  → Available safety, fairness, and gamification papers provide adjacent justification for individual primitives.
  → Because the corpus is highly disconnected and one core primitive lacks clear direct backing, the beat supports a plausible framework, not a strongly consolidated one.

---

## Beat 4: Passenger-Side WTP and Motivations 🟡 adequate

Supporting papers: 9
Key papers MISSING: Campus-specific willingness-to-pay study for student ridesharing or carpooling
Weakness: This beat is supported primarily by the paper's own formative survey, which is appropriate for a descriptive findings beat. The limitation is scope: the sample is skewed and 82% Mandarin-native, so the evidence should be framed as formative design input for a specific campus subpopulation rather than general student demand.

Evidence chain:
  → The N=117 survey directly reports passenger willingness-to-pay and stated motivations.
  → Safety and rewards literature provides only contextual interpretation, not the proof line.
  → The beat is sufficient for descriptive formative claims within the surveyed population, not for broader generalization.

---

## Beat 5: Driver-Side Tolerance and Rating-Fairness Asymmetry 🟠 weak

Supporting papers: 9
Key papers present: Not all algorithmic controls are equal: the double-edged impact of algorithmic c, Algorithmic Control and Psychological Risk in Digitally Managed Public Transport
Key papers MISSING: Driver participation study in peer carpool or campus ridesharing systems, Direct study of rating asymmetry or reputational unfairness in peer mobility platforms
Weakness: The survey's driver-side finding is intriguing but fragile. With only N=30 drivers, the rating-unfairness tolerance result can be used as a design signal or hypothesis, not a general behavioral conclusion. The algorithmic-management literature helps explain why this asymmetry matters, but it does not validate the specific magnitude or prevalence in a campus carpool context.

Evidence chain:
  → The survey provides the direct observation of driver-side tolerance and perceived asymmetry.
  → Algorithmic management papers explain why ratings and controls can create psychological and behavioral distortions.
  → Because the driver subsample is small and context-specific, the beat supports a cautionary design implication rather than a broadly generalizable empirical claim.

---

## Beat 6: CampusRide Multi-Module Platform and Carpool Deep-Dive 🟡 adequate

Supporting papers: 16
Key papers present: Trust and reputation in the sharing economy: The role of personal photos in Airb, Not all algorithmic controls are equal: the double-edged impact of algorithmic c
Key papers MISSING: Deployment evaluation of a campus ridesharing or campus mobility platform, Implementation case of an integrated campus platform spanning multiple student coordination modules
Weakness: The beat is sufficient to support that CampusRide was designed and implemented as an artifact, and that its carpool decisions are traceable to survey findings. It is not sufficient to support effectiveness, adoption, safety improvement, or sustainability claims, because no deployment evaluation is provided. The integrated multi-module framing is also more novel than corpus-backed.

Evidence chain:
  → The artifact exists and the carpool module operationalizes the stated design primitives.
  → Survey findings provide a visible rationale for design decisions such as identity, safety, ratings, and rewards.
  → Without live deployment or user outcome data, the evidence supports design rationale and implementation, not platform success.

---

## Beat 7: Adversarial Scoping 🟢 strong

Supporting papers: 25
Key papers present: Fulfillment of the Work Games: Warehouse Workers' Experiences with Algorithmic M, Not all algorithmic controls are equal: the double-edged impact of algorithmic c, Algorithmic Control and Psychological Risk in Digitally Managed Public Transport
Key papers MISSING: Higher-education-specific critique of algorithmic governance in closed-community mobility platforms
Weakness: This beat is well supported as a limitation section, though most of the external critique comes from labor, logistics, and public-transport domains rather than campus carpooling specifically. That is acceptable here because the point is not to prove failure, but to honestly delimit how formalization, ratings, incentives, and platform control can introduce new harms.

Evidence chain:
  → Algorithmic management literature establishes that ratings, incentives, and digitally mediated control can create genuine harms.
  → Gamification-related critique makes reward design a real risk rather than a harmless engagement feature.
  → Combined with the paper's own admissions about skewed sampling, no deployment, and .edu scope, the adversarial scoping is credible and appropriately cautionary.

---

## Overall Assessment
The corpus is sufficient for a careful, narrow paper: it can motivate the problem setting, justify several design concerns, contextualize a formative survey, and strongly support an honest adversarial-scoping section. It is not sufficient for stronger claims that small-town campuses are definitively underserved by commercial rideshare in a documented, campus-specific way, nor that international students are already using WeChat/WhatsApp for transport coordination at scale, nor that the four design primitives emerge as a fully established framework from prior work. The biggest structural issue is fragmentation: 88 papers produce only 19 edges, with 72 components and 66 isolated nodes, so the literature base is broad but not integrated. The paper is best supported as a formative design-and-implementation contribution with explicit scope limits, not as a validated deployment or a settled general theory of campus mobility platforms.

## Missing Papers (search suggestions)

- **Direct study of rideshare scarcity and student coping in rural or small-town university settings**: Beat 1 currently relies on rural transit and general platform-trust motivation. A direct campus study would substantiate the claimed commercial rideshare gap rather than merely motivate it.
  Search: `Search: rural university campus rideshare availability student transportation gap small town`
- **Study of WeChat or WhatsApp transportation coordination among international students on campus**: Beat 2 needs evidence for mobility/logistics coordination specifically, not just community support, identity, or information exchange through messaging apps.
  Search: `Search: WeChat WhatsApp international students transportation coordination campus ride sharing`
- **Institutional identity verification as a trust mechanism in closed-community sharing platforms**: Beat 3's identity-verification primitive is central to the artifact but lacks a clear direct literature anchor in the corpus. This would connect university affiliation or verified institutional status to trust, safety, and participation.
  Search: `Search: institutional verification trust closed community marketplace university email verified platform`

## Strongest Narrative Thread
Trust and reputation in the sharing economy: The role of personal photos in Airb -> Not all algorithmic controls are equal: the double-edged impact of algorithmic c -> Fulfillment of the Work Games: Warehouse Workers' Experiences with Algorithmic M
