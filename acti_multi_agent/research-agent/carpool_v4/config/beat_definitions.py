"""Centralized beat definitions for the v4 CampusRide pipeline.

Paper line is:
  motivation -> framework -> primary evidence (survey) -> core contribution
  (multi-module platform with carpool deep-dive) -> adversarial scoping.

Phase modules import this file instead of maintaining local beat/category copies.
See `paper_outline_v4.md` Part 5 and `pipeline_v4_migration_and_config.md`
Part 7 for the alignment table that this module instantiates.
"""

# A-J (10 categories). K has been removed relative to the v3 L_auth taxonomy.
CATEGORY_SEQUENCE = tuple("ABCDEFGHIJ")

# Beat -> primary categories.
# Primary-data beats (4) and artifact beats (6) legitimately have no category
# spine — they use a pseudo-anchor defined in manual_core_inclusions.json.
BEAT_CATEGORIES = {
    1: ["A", "B"],            # §2.1 small-town transport gap
    2: ["C", "D", "I"],       # §2.2 grassroots + integrated platforms
    3: ["E", "F", "G", "H"],  # §2.3 four design primitives
    4: [],                    # §4.1 passenger-side survey (primary_data)
    5: ["F", "H"],            # §4.2 driver tolerance + rating fairness
    6: [],                    # §5  CampusRide platform (artifact)
    7: ["J", "H"],            # §7.2 adversarial scoping
}

# Beat -> secondary categories (papers that may appear as supporting evidence).
BEAT_SECONDARY_CATEGORIES = {
    1: ["B"],
    2: ["B"],
    3: ["B"],
    4: ["F", "H"],
    5: ["J"],
    6: ["E", "F", "G", "H"],
    7: ["B"],
}

BEAT_NAMES = {
    1: "Small-Town Campus Transportation & Coordination Gaps",
    2: "Grassroots Coordination & Integrated Campus Platforms",
    3: "Design Primitives: Identity, Safety, Rating Fairness, Rewards",
    4: "Formative Survey: Passenger-Side WTP & Motivations",
    5: "Formative Survey: Driver-Side Tolerance & Rating-Fairness Asymmetry",
    6: "CampusRide Multi-Module Platform Design with Carpool Deep-Dive",
    7: "Adversarial Scoping: Formalization Risk, Sample Skew, No Deployment",
}

# Canonical runtime argument-line labels.
ARGUMENT_LINES = {
    1: "motivation",
    2: "motivation",
    3: "framework",
    4: "primary",
    5: "primary",
    6: "core_contribution",
    7: "adversarial",
}

# Beats marked as primary_data / artifact are validated leniently by
# phase_contracts.ensure_narrative_chains_valid — they may use a pseudo-anchor
# paperId (prefixed with "local:") and structured internal references in
# their spine rather than real paperIds.
BEAT_TYPES = {
    4: "primary_data",
    6: "artifact",
}

# Motivation papers can frame the problem, but the primary argument line
# (§4.1/§4.2 survey) must stand on its own evidence base. Adversarial
# papers scope rather than directly support the thesis.
LINE_SEPARATION = {
    "motivation": {"forbidden_support_from": ["primary"]},
    "primary": {"forbidden_support_from": ["motivation"]},
    "framework": {"forbidden_support_from": []},
    "core_contribution": {"forbidden_support_from": []},
    "adversarial": {"forbidden_support_from": []},
}

NUM_BEATS = 7

# Per-beat counterevidence that MUST be cited.
# The v4 pipeline concentrates mandatory counterevidence on Beat 7 because
# that is where adversarial scoping literature is expected; other beats may
# cite counterevidence but are not gated on it.
MUST_CITE_COUNTEREVIDENCE = {
    1: [
        "Campus shuttles / public transit can partially substitute for commercial rideshare",
    ],
    2: [
        "Some super-app / integrated-platform literature questions whether formalization preserves grassroots autonomy",
    ],
    3: [
        "Identity verification alone does not address behavioral safety — must be paired with other primitives",
    ],
    4: [],
    5: [
        "Peer rating systems work reasonably in several settings without dedicated fairness mechanisms",
    ],
    6: [
        "Multi-module platform design must acknowledge that deployment is not validation of each module in isolation",
    ],
    7: [
        "Algorithmic management literature (Rosenblat & Stark, Lee et al.) on gig-worker harm from rating systems",
        "Formalization risk: platform-mediated coordination may reproduce commercial rideshare harms",
        ".edu verification does not verify driving competence or prevent malicious behavior",
        "Gamification may produce gaming behavior or crowd out intrinsic motivation",
        "Three-tier sample-skew disclosure: (a) main-sample language skew — 79% Mandarin-native (72/91 who reported native language) limits generalizability to other student populations; (b) driver-subset skew — the F5 rating-fairness asymmetry rests on the Driver/Both subset N=19, which is methodologically preferred to the full-sample mix but still small and requires a dedicated driver-side survey to confirm; (c) completion skew — 44/111 finished (~40% completion rate), so finishers may differ systematically from non-finishers on carpool salience",
    ],
}

# Per-beat honesty constraints: things the narrative must NOT overclaim.
HONESTY_CONSTRAINTS = {
    1: [
        "Frame the small-town rideshare gap as motivated and documented, not empirically quantified at scale",
        "Use 'exists' / 'motivates' / 'is documented'; avoid 'has been proved' / 'is quantified'",
    ],
    2: [
        "Grassroots coordination is well-documented; use 'document' / 'indicate'",
        "Super-app / integrated-platform literature is sparser — frame as 'initial inquiry' not 'established design space'",
        "Do NOT claim CampusRide is the first multi-module campus platform",
    ],
    3: [
        "Present the four design primitives as parallel; do not value-rank them in this beat",
        "Use neutral definitional verbs; the ranking work belongs to Beats 4-6",
    ],
    4: [
        "Descriptive statistics only: no inferential statistics, no t-tests, no p-values, no 'significantly'",
        "Disclose N cohort as 'N=111 eligible / 44 finished' (6 Survey-Preview test responses excluded); report per-item N separately because completion varies by question",
        "Language cohort is disclosed as '79% Mandarin-native (72/91 who reported native language)' — scope-setting, not masked as bias and not marketed as the paper's strength",
        "F6 (Q23 driver willingness, N=33) is reported as descriptive supply-side counts: Ithaca 10/33, short-distance 9/33, long-distance 12/33 Very+Extremely willing; long-distance is highest but this is framed as signal, not as a tested hypothesis",
        "Use 'we observe' / 'reports indicate' / 'median value is'; avoid 'majority think' / 'statistics confirm'",
    ],
    5: [
        "The counterintuitive rating-fairness finding is reported on the Driver/Both subset (N=19) against a Rider-only control subset (N=12); Q24_3 'unfair rating' tolerance is 29.1 in the driver subset versus 22.4 in rider-only, while the other three Q24 items sit at 41.4-52.3 in the driver subset versus 19.6-35.7 in the rider-only control",
        "The subset gap (29.1 unfair-rating vs 41.4-52.3 other-items within the same Driver/Both respondents, a 12.3-23.2 point spread) is the core observation; it resonates with algorithmic management literature (Rosenblat & Stark, Lee et al.), it does NOT replicate it",
        "Rider-only control numbers (35.7 / 19.6 / 22.4 / 33.2) must be reported as methodological justification for the subset split, not hidden because the pattern weakens there",
        "Use 'resonates with' / 'parallels' / 'counterintuitively' / 'limited to the Driver/Both subset (N=19)'; avoid 'confirms' / 'replicates' / 'proves the same phenomenon' and avoid mixing the full-sample N=30 numbers with the subset numbers",
        "Do not over-generalize F5 to all peer rating systems or to professional gig workers",
    ],
    6: [
        "The platform is presented as designed and implemented — not as validated by deployment data",
        "Each design decision in §5.8 must explicitly reference a survey finding (F3/F4/F5), and F5 attribution must go down to the Driver/Both subset (N=19), not the full sample",
        "§5.2 carpool module scope motivation cites F6 (Q23 driver supply willingness: long-distance 12/33 Very+Extremely willing, the highest of the three supply scenarios) as the evidence for prioritizing long-distance carpool as a deep-dive scope",
        "Use 'we designed' / 'motivated by' / 'in response to finding X'; avoid 'effective' / 'successful' / 'proves'",
        "Six-module claim must acknowledge five modules are described at overview level and only carpool is deep-dived",
    ],
    7: [
        "Each adversarial paragraph must cite at least one counterevidence paper — not empty self-criticism",
        "Use 'may reproduce' / 'we acknowledge' / 'scope-limited'; avoid 'we address' / 'we prevent' / 'we solve'",
        "This beat succeeds by honest scoping, not by defending the thesis at all costs",
    ],
}

# Narrative verb rules based on citation chain verification.
CITATION_VERB_RULES = {
    "verified_citation": "Use 'extends' 'builds on' 'responding to'",
    "no_citation_but_thematically_related": "Use 'in a parallel line of inquiry' 'complementary evidence from' 'independently'",
    "contradicts": "Use 'in contrast' 'challenges' 'narrows the scope of'",
}

# Target paper counts per category.
# Rebalanced for v4: C/D/I/J are expected to be thinner at startup and grow
# via Lens targeted supplement (config/lens_queries.json).
CATEGORY_TARGETS = {
    "A": 8,   # Small-town / campus transportation gap
    "B": 10,  # P2P ridesharing & sharing-economy trust
    "C": 8,   # Grassroots / informal coordination platforms
    "D": 8,   # International students digital practices
    "E": 8,   # Identity verification & .edu-scoped platforms
    "F": 10,  # Safety in shared mobility
    "G": 8,   # Gamification in coordination / mobility
    "H": 10,  # Rating & reputation fairness
    "I": 8,   # Integrated community platforms & super-apps
    "J": 10,  # Algorithmic management & platform labor critique
}

# Identifier prefix for pseudo-anchors of primary_data / artifact beats.
LOCAL_ANCHOR_PREFIX = "local:"
