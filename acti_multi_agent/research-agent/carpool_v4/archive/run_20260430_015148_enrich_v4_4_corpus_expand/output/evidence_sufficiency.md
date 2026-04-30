# Evidence Sufficiency Report

*Assessment of literature support for each beat of the paper*

---

## Beat 1: Small-Town Campus Transportation & Coordination Gaps 🟡 adequate

Supporting papers: 19
Key papers present: Taking the Pulse of US College Campuses with Location-Based Anonymous Mobile App, The Benefits of Facebook “Friends:” Social Capital and College Students’ Use of
Key papers MISSING: Direct study of transportation insecurity or transit deserts in small-town university settings, Direct study of informal peer ride coordination on rural or small-town campuses
Weakness: The corpus can motivate a campus coordination problem, but only indirectly supports the specific small-town university ridesharing gap. Category A appears to establish transportation/access friction, while much of B is trust-oriented and not transport-specific. This is sufficient for background framing, not for proving that a campus carpool platform is the needed remedy.

Evidence chain:
  → A papers indicate transportation or access gaps affecting campus contexts.
  → B papers explain why coordination among semi-strangers is hard, but they do not directly document small-town campus ridesharing failure.

---

## Beat 2: Grassroots Coordination and Integrated Campus Platforms 🟠 weak

Supporting papers: 16
Key papers present: The Benefits of Facebook “Friends:” Social Capital and College Students’ Use of, Taking the Pulse of US College Campuses with Location-Based Anonymous Mobile App
Key papers MISSING: Direct study of WeChat/WhatsApp-based transportation coordination among international students in university towns, Case study of integrated campus or super-app style student platforms spanning multiple daily-life services
Weakness: This beat is the thinnest motivation link. The corpus supports the narrower claim that students and migrant/international communities use digital social platforms for coordination and support, and that campus digital platforms can host multiple functions. It does not directly establish that international students in small-town universities self-organize ride coordination across domains via WeChat/WhatsApp. The C-D-I literature is sparse, siloed, and mostly adjacent rather than on-point.

Evidence chain:
  → C papers show messaging apps can support grassroots coordination, but mostly outside campus mobility.
  → D papers concern international students, but per the gap notes they do not directly address WeChat-based on-campus mobility coordination.
  → I papers suggest integrated platform possibilities, but the literature is sparse and functions more as design inspiration than empirical proof.

---

## Beat 3: Four Design Primitives: Identity, Safety, Rating Fairness, Rewards 🟡 adequate

Supporting papers: 26
Key papers present: Trust and reputation in the sharing economy: The role of personal photos in Airb, Trust and power in Airbnb’s digital rating and reputation system, Factors influencing trust and behavioral intention to use Airbnb service innovat
Key papers MISSING: Direct study of institutionally verified trust mechanisms in closed campus peer-to-peer mobility platforms, Direct study comparing rating fairness and safety perceptions in campus-scoped ridesharing communities
Weakness: The corpus can justify the four primitives as a parallel design framework, but mostly by stitching together adjacent literatures. Trust/reputation is the strongest sub-thread; campus-scoped institutional verification and closed-community fairness are notably underdeveloped. The literature is sufficient to motivate the primitives individually, not to show that this exact four-part bundle is established best practice for campus ridesharing.

Evidence chain:
  → E and B provide general trust and identity-signal rationale.
  → G and related platform studies help motivate rewards/gamification and engagement design.
  → H and adjacent reputation papers motivate rating fairness concerns, though mostly from non-campus contexts.

---

## Beat 4: Primary Survey: Passenger WTP, Motivations, and Driver Supply Willingness 🟡 adequate

Supporting papers: 10
Key papers present: Trust and power in Airbnb’s digital rating and reputation system, Factors influencing trust and behavioral intention to use Airbnb service innovat
Key papers MISSING: Benchmark study of campus ridesharing willingness-to-pay and adoption in small-town universities
Weakness: This beat is supported primarily by the formative survey itself, not by the corpus. As descriptive formative evidence, it is sufficient if tightly scoped to the respondents who finished the survey. It should not be generalized to the broader campus population because of the completion rate, language skew, and lack of deployment or revealed-behavior data. F6 is reportable as a sample-specific gradient: long-distance willingness is highest at 12/33 on Q23.

Evidence chain:
  → The N=111 eligible / 44 finished survey directly supports descriptive claims about this sample’s rider motivations and WTP.
  → Q23 provides a directly observed driver willingness gradient, with long-distance willingness highest within the three tiers.
  → F and H papers serve only as contextualizers for why safety/fairness may matter; they do not prove the survey findings.

---

## Beat 5: Driver-Subset Tolerance and Rating-Fairness Asymmetry 🟠 weak

Supporting papers: 22
Key papers present: Trust and power in Airbnb’s digital rating and reputation system, Trust and reputation in the sharing economy: The role of personal photos in Airb
Key papers MISSING: Algorithmic Labor and Information Asymmetries: A Case Study of Uber’s Drivers, Direct driver-side study of reputation-system fairness in peer ridesharing or campus mobility settings
Weakness: This is an interesting exploratory finding, not a stable empirical conclusion. The N=19 Driver/Both subgroup can support reporting the observed asymmetry within the sample, and the Rider-only control N=12 helps justify that the pattern is subgroup-specific rather than a survey artifact. But the subgroup is too small for generalization, and the literature resonance comes mostly from broader platform reputation and algorithmic-management work rather than campus carpool evidence.

Evidence chain:
  → The survey shows lower tolerance for rating unfairness in the N=19 Driver/Both subgroup than for the other three design concerns.
  → The N=12 Rider-only control helps support the methodological claim that the effect is subgroup-specific.
  → J and reputation papers explain why asymmetric exposure to ratings can matter, but they do not independently validate the observed subgroup pattern.

---

## Beat 6: CampusRide Multi-Module Platform and Carpool Deep-Dive 🟡 adequate

Supporting papers: 26
Key papers present: Taking the Pulse of US College Campuses with Location-Based Anonymous Mobile App, Trust and reputation in the sharing economy: The role of personal photos in Airb, Trust and power in Airbnb’s digital rating and reputation system
Key papers MISSING: Deployment or usability evaluation study of an integrated campus mobility platform, Comparative design case of a verified campus super-app with transportation, marketplace, and community modules
Weakness: The beat is sufficient as an artifact contribution: a designed and implemented platform with a carpool module grounded in formative findings. It is not sufficient as an effectiveness claim. The corpus supports design rationale for individual features, and the survey links F3-F6 to specific carpool decisions, but there is no deployment evaluation, no behavioral validation, and little literature showing that an integrated multi-module campus platform outperforms narrower tools.

Evidence chain:
  → Beat 4 provides formative inputs for the carpool module’s design decisions.
  → E/F/G/H contextualize why identity verification, safety, fairness, and rewards are plausible design choices.
  → The implementation itself substantiates that CampusRide was built, but not that it works in practice or improves outcomes.

---

## Beat 7: Adversarial Scoping 🟡 adequate

Supporting papers: 17
Key papers present: Trust and power in Airbnb’s digital rating and reputation system, Trust and reputation in the sharing economy: The role of personal photos in Airb
Key papers MISSING: Algorithmic Labor and Information Asymmetries: A Case Study of Uber’s Drivers, Working with Machines: The Impact of Algorithmic and Data-Driven Management on Human Workers, Direct study of gamification-related pressure or over-participation harms in mobility platforms
Weakness: This beat works when framed as a real limitation section. The available critique literature is enough to justify concern that formalization can reproduce rating pressure, behavioral nudging, and platform control harms. It also supports honest acknowledgement of the sample’s three-layer skew and the absence of deployment evidence. The main weakness is that the corpus seems stronger on general platform/reputation critique than on campus-specific manifestations of those harms.

Evidence chain:
  → J provides the main adversarial lens on platformization and algorithmic-management risk.
  → H and reputation papers reinforce that ratings and trust systems can create asymmetries rather than merely solve trust problems.
  → The paper’s own sample composition and lack of deployment evaluation independently justify narrow scoping.

---

## Overall Assessment
The corpus is sufficient for a cautious, well-scoped paper, but not for a broad causal or generalizable thesis. Beats 1, 3, 4, 6, and 7 are supportable if phrased narrowly: there is a motivating campus coordination problem, the four design primitives are plausible, the survey offers formative descriptive evidence for this sample, CampusRide is a real artifact grounded in those findings, and there are genuine platformization risks that bound the contribution. Beat 2 is the main literature weakness because the leap from grassroots messaging use and international-student digital practices to multi-domain WeChat/WhatsApp ride coordination in small-town campuses is only weakly supported. Beat 5 is the main empirical weakness because the rating-fairness asymmetry is an exploratory subgroup observation with N=19, not a general finding. The strongest version of the paper is therefore: small-town campuses have coordination frictions; international students already rely on informal digital community infrastructures; CampusRide formalizes that pattern into an identity-verified campus artifact; the carpool module is grounded in formative survey results; and formalization brings real fairness and management risks that the paper openly scopes.

## Missing Papers (search suggestions)

- **Direct study of WeChat/WhatsApp-based ride coordination among international students in university towns**: This would directly support Beat 2 instead of forcing an inference from general messaging-app coordination and international-student adaptation literature.
  Search: `Search for: WeChat international students transportation coordination campus, WhatsApp ride sharing university international students, Chinese students WeChat mobility campus`
- **Direct study of transportation insecurity or peer ridesharing in small-town/rural university settings**: This would strengthen Beat 1 by documenting the exact mobility gap the paper claims, and would reduce reliance on more general campus or urban transport framing.
  Search: `Search for: rural university transportation insecurity, small-town campus mobility gap, college student ridesharing rural campus, university transit desert`
- **Algorithmic Labor and Information Asymmetries: A Case Study of Uber’s Drivers**: This is a foundational paper for Beats 5 and 7 because it gives a strong theoretical basis for why rating systems and platform formalization can create asymmetric pressure and control, especially on drivers.
  Search: `Search for: Rosenblat Stark 2016 algorithmic labor information asymmetries Uber drivers`

## Strongest Narrative Thread
The Benefits of Facebook “Friends:” Social Capital and College Students’ Use of -> Taking the Pulse of US College Campuses with Location-Based Anonymous Mobile App -> Trust and power in Airbnb’s digital rating and reputation system
