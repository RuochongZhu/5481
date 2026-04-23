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
(Beat 3). A formative survey (N=117) on carpooling reveals high
willingness-to-pay uplift for .edu verification, real-time location
sharing, and emergency SOS, with financial motivations dominating and
gamification as a secondary motivator (Beat 4), and surfaces a
counterintuitive driver sensitivity to unfair ratings that exceeds
tolerance for late passengers or route changes (Beat 5). We designed and
implemented CampusRide, a multi-module identity-verified campus platform
comprising carpool, marketplace, activities, groups, messaging, and
points modules; the carpool module is developed in depth to
operationalize the four primitives in response to the survey findings
(Beat 6). We acknowledge that platform-mediated formalization may
reproduce algorithmic management harms documented in commercial
rideshare; the sample skew (82% Mandarin-native respondents) scopes
generalizability; no deployment evaluation is provided (Beat 7 —
adversarial).
""".strip()


# Compact single-line version for prompts that need brevity.
THESIS_V4_SHORT = (
    "Small-town university ridesharing is underserved by Uber/Lyft, producing a "
    "multi-domain coordination gap. International students already coordinate "
    "informally via WeChat/WhatsApp groups. CampusRide formalizes this with a "
    "multi-module identity-verified campus platform; a carpool deep-dive "
    "operationalizes four design primitives (institutional identity, safety, "
    "rating fairness, gamification) against a formative N=117 survey. "
    "The research-agent pipeline supporting this synthesis is itself the paper's "
    "third contribution. Adversarial scoping acknowledges platform-mediated "
    "rideshare harms, Mandarin-native sample skew, and absence of deployment "
    "evaluation."
)


# Paper-level contribution claims referenced by reviewer prompts.
CONTRIBUTIONS = [
    "(1) CampusRide — an identity-verified multi-module campus platform "
    "(carpool, marketplace, activities, groups, messaging, points).",
    "(2) Deep-dive case on the carpool module grounded in an N=117 formative "
    "survey with three transferable design findings.",
    "(3) research-agent — a thesis-conditioned evidence pipeline that shaped "
    "this paper's literature synthesis and adversarial scoping.",
]
