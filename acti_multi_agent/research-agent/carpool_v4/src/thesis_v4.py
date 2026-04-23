"""Shared v4 thesis constant.

Injected into prompts.py, phase3_5_narrative.py, phase3_7_contradiction.py,
scoring.py so every agent in the pipeline sees the same CampusRide thesis
statement. See pipeline_v4_migration_and_config.md Part 3.1 for origin.
"""

THESIS_V4 = """
Commercial ridesharing services (Uber/Lyft) underserve small-town
university settings, producing a multi-faceted coordination gap that
extends beyond transportation — to marketplace, activities, groups, and
other peer interactions (Beat 1). In this gap, students — especially
international students from messaging-app-centric cultures — have
self-organized grassroots coordination via WeChat/WhatsApp groups across
multiple domains; existing super-app and integrated-platform literature
provides partial but incomplete design guidance for this setting
(Beat 2). Four design primitives — institutional identity verification,
safety infrastructure, rating fairness, and gamification — emerge from
the literature as candidates for formalizing such grassroots practice
(Beat 3). A formative survey (N=111 eligible / 44 finished, after
excluding 6 Survey-Preview test responses) on carpooling reveals high
willingness-to-pay uplift for real-time location sharing, .edu
verification, and emergency SOS (F3 means 69.1 / 67.3 / 63.5 on a
0-100 scale), with financial motivations dominating and gamification as
a secondary motivator (Beat 4); it also surfaces a counterintuitive
rating-fairness asymmetry within the Driver/Both subgroup (N=19),
where tolerance for unfair ratings (29.1) is 12.3-23.2 points lower
than tolerance for late passengers, route changes, or destination
changes (41.4-52.3) — a gap that does not appear in the Rider-only
control subset (N=12) (Beat 5). We designed and implemented CampusRide,
a multi-module identity-verified campus platform comprising carpool,
marketplace, activities, groups, messaging, and points modules; the
carpool module is developed in depth to operationalize the four
primitives in response to the survey findings, with long-distance
routes (F6: 12/33 drivers Very+Extremely willing on Q23, the highest of
three supply scenarios) as the priority scope for §5.2 (Beat 6). We
acknowledge that platform-mediated formalization may reproduce
algorithmic management harms documented in commercial rideshare; the
sample skew (79% Mandarin-native among the 91 respondents who reported
native language, i.e. 72/91) and the driver-subset reliance (F5 rests
on N=19) scope generalizability; no deployment evaluation is provided
(Beat 7 — adversarial).
""".strip()


# Compact single-line version for prompts that need brevity.
THESIS_V4_SHORT = (
    "Small-town university ridesharing is underserved by Uber/Lyft, producing a "
    "multi-domain coordination gap. International students already coordinate "
    "informally via WeChat/WhatsApp groups. CampusRide formalizes this with a "
    "multi-module identity-verified campus platform; a carpool deep-dive "
    "operationalizes four design primitives (institutional identity, safety, "
    "rating fairness, gamification) against a formative survey with N=111 "
    "eligible / 44 finished respondents, a counterintuitive rating-fairness "
    "asymmetry observed within the Driver/Both subgroup (N=19), and a "
    "long-distance driver-supply preference (F6). "
    "The research-agent pipeline supporting this synthesis is itself the paper's "
    "third contribution. Adversarial scoping acknowledges platform-mediated "
    "rideshare harms, a 79% Mandarin-native language cohort (72/91 who "
    "reported native language), the driver subgroup (N=19) on which F5 "
    "rests, and absence of deployment evaluation."
)


# Paper-level contribution claims referenced by reviewer prompts.
CONTRIBUTIONS = [
    "(1) CampusRide — an identity-verified multi-module campus platform "
    "(carpool, marketplace, activities, groups, messaging, points).",
    "(2) Deep-dive case on the carpool module grounded in a formative survey "
    "(N=111 eligible / 44 finished) with transferable design findings, "
    "including a counterintuitive rating-fairness asymmetry observed within "
    "the driver subgroup (N=19).",
    "(3) research-agent — a thesis-conditioned evidence pipeline that shaped "
    "this paper's literature synthesis and adversarial scoping.",
]
