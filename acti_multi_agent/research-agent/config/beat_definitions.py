"""Centralized beat definitions — single source of truth for the 6-beat pipeline.

Derived from updated_beat_definitions.json (dual-argument-line thesis structure).
All phase modules import from here instead of maintaining local copies.
"""

# Beat → primary categories
BEAT_CATEGORIES = {
    1: ["A", "B", "C"],      # Collapse + Contamination (line_1)
    2: ["D", "H"],            # Web Drift Measurement (line_1)
    3: ["D", "A"],            # L_auth Bridge (bridge)
    4: ["F", "I", "J"],       # Fine-tuning → Social Reasoning (line_2)
    5: ["F", "I", "J"],       # Contrastive Experiment (line_2)
    6: ["G"],                  # CampusGo Proposal (proposal)
}

# Beat → secondary categories (papers that may appear as supporting evidence)
BEAT_SECONDARY_CATEGORIES = {
    1: [],
    2: ["B", "E"],
    3: ["E", "I"],
    4: ["E"],
    5: ["E", "D"],
    6: ["A", "E", "I"],
}

BEAT_NAMES = {
    1: "Model Collapse and Contamination Risk",
    2: "Partial Measurability of Web Drift",
    3: "L_auth Framework Definition",
    4: "Fine-tuning Data Source Affects Social Reasoning",
    5: "Contrastive Fine-tuning Experiment",
    6: "CampusGo as Design Proposal",
}

# Which argument line each beat belongs to
ARGUMENT_LINES = {
    1: "line_1",
    2: "line_1",
    3: "bridge",
    4: "line_2",
    5: "line_2",
    6: "proposal",
}

# Argument line separation: NEVER use pretraining collapse papers (A) to directly
# support fine-tuning claims (beats 4-5), and vice versa.
LINE_SEPARATION = {
    "line_1": {"forbidden_support_from": ["line_2"]},
    "line_2": {"forbidden_support_from": ["line_1"]},
}

NUM_BEATS = 6

# Per-beat counterevidence that MUST be cited in narrative chains
MUST_CITE_COUNTEREVIDENCE = {
    1: [
        "pi^2/6 pathway: mixed real+synthetic avoids collapse",
        "Self-correcting loops: correction functions stabilize self-consuming training",
        "Curated synthetic data: can optimize preference objectives under strong curation",
    ],
    2: [
        "RefinedWeb/FineWeb: filtered web data still trains strong models",
        "Domain-specific contamination (Wikipedia) does not equal web-wide degradation",
    ],
    3: [],
    4: [
        "RLAIF: AI feedback matches RLHF on summarization and dialogue",
        "AlpacaFarm: simulated feedback 50x cheaper with high agreement",
        "Dromedary: minimal human supervision self-alignment",
        "Zephyr 7B: AI feedback DPO beats LLaMA2-Chat-70B",
        "Social-R1: targeted adversarial training improves social reasoning",
        "Self-Instruct/WizardLM: synthetic instructions work for general instruction-following",
    ],
    5: [],
    6: [],
}

# Per-beat honesty constraints — things the narrative must NOT overclaim
HONESTY_CONSTRAINTS = {
    1: [
        "Do NOT claim all synthetic data is harmful",
        "Do NOT claim web-scale contamination is proven — only domain-specific evidence exists",
        "Do NOT claim detection is impossible — only that it is fragile under adversarial conditions",
    ],
    2: [
        "Do NOT claim web-wide pretraining degradation is demonstrated",
        "Frame as 'rising risk' not 'demonstrated failure'",
        "Explicitly state: no post-2022 web-scale contamination audit exists in the corpus",
    ],
    3: [
        "Do NOT present L_auth as a validated law or discovery",
        "Frame as 'grounded synthesis of existing metric ingredients'",
        "Do NOT claim L_auth is a detection tool — it is a descriptive/predictive framework",
        "Explicitly state that weight calibration is future work",
    ],
    4: [
        "Do NOT claim human data is universally indispensable for alignment",
        "Do NOT claim AI feedback fails on social tasks — corpus lacks direct evidence for this",
        "Frame as 'especially valuable for socially grounded tasks' not 'always necessary'",
    ],
    5: [
        "Frame as 'pilot study' not 'validation'",
        "Use 'initial evidence suggests' not 'demonstrates'",
        "Acknowledge: 3B model may not amplify data quality differences sufficiently",
        "Acknowledge: D1 and D4 co-vary in this design, cannot separate independent contributions",
    ],
    6: [
        "Use proposal verbs: 'motivates' 'suggests' 'points toward' 'frames requirements for'",
        "Do NOT use: 'demonstrates' 'proves' 'validates'",
        "Acknowledge: G-category literature is from adjacent domains, not directly from AI training data collection",
        "Acknowledge: platform effectiveness is untested",
    ],
}

# Narrative verb rules based on citation chain verification
CITATION_VERB_RULES = {
    "verified_citation": "Use 'extends' 'builds on' 'responding to'",
    "no_citation_but_thematically_related": "Use 'in a parallel line of inquiry' 'complementary evidence from' 'independently'",
    "contradicts": "Use 'in contrast' 'challenges' 'narrows the scope of'",
}

# Target paper counts per category
CATEGORY_TARGETS = {
    "A": 30, "B": 17, "C": 12, "D": 22, "E": 22,
    "F": 17, "G": 12, "H": 12, "I": 12, "J": 12,
}
