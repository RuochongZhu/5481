"""Centralized beat definitions: runtime source of truth for the v2 pipeline.

The paper is now organized as motivation -> framework -> primary evidence ->
core contribution -> adversarial scoping. Phase modules should import this file
instead of maintaining local beat/category copies.
"""

CATEGORY_SEQUENCE = tuple("ABCDEFGHIJK")

# Beat -> primary categories
BEAT_CATEGORIES = {
    1: ["A", "B", "C"],       # Background motivation: collapse + contamination risk
    2: ["D", "H"],            # Background motivation: web drift measurement
    3: ["D", "A"],            # Fine-tuning-focused L_auth framework
    4: ["F", "I", "J"],       # Primary evidence: provenance and social reasoning
    5: ["F", "I", "J"],       # Primary evidence: fixed-compute pilot experiment
    6: ["G"],                 # Core contribution: deployed CampusGo platform
    7: ["K"],                 # Adversarial scoping: competing mechanisms
}

# Beat -> secondary categories (papers that may appear as supporting evidence)
BEAT_SECONDARY_CATEGORIES = {
    1: [],
    2: ["B", "E"],
    3: ["E", "I"],
    4: ["E", "K"],
    5: ["E", "D", "K"],
    6: ["E", "I", "J"],
    7: ["I", "J"],
}

BEAT_NAMES = {
    1: "Model Collapse and Contamination Risk",
    2: "Partial Measurability of Web Drift",
    3: "L_auth Framework Definition",
    4: "Fine-tuning Data Source Affects Social Reasoning",
    5: "Contrastive Fine-tuning Experiment",
    6: "CampusGo as Deployed Core Contribution",
    7: "Competing Explanations and Honest Scoping",
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

# Motivation papers can frame the problem, but the primary post-training claim
# must stand on its own evidence base. Adversarial papers scope rather than
# directly support the thesis.
LINE_SEPARATION = {
    "motivation": {"forbidden_support_from": ["primary"]},
    "primary": {"forbidden_support_from": ["motivation"]},
    "framework": {"forbidden_support_from": []},
    "core_contribution": {"forbidden_support_from": []},
    "adversarial": {"forbidden_support_from": []},
}

NUM_BEATS = 7

# Per-beat counterevidence that MUST be cited in narrative chains.
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
    3: [
        "Pretraining operationalization is future work, not a current stage-agnostic validation",
    ],
    4: [
        "RLAIF: AI feedback matches RLHF on summarization and dialogue",
        "AlpacaFarm: simulated feedback 50x cheaper with high agreement",
        "Dromedary: minimal human supervision self-alignment",
        "Zephyr 7B: AI feedback DPO beats LLaMA2-Chat-70B",
        "Social-R1: targeted adversarial training improves social reasoning",
        "Self-Instruct/WizardLM: synthetic instructions work for general instruction-following",
    ],
    5: [
        "Inference-time scaling and model scale may explain gains even when data provenance is controlled",
        "DPO/preference-learning variants may be needed to separate data effects from optimization effects",
    ],
    6: [
        "CampusGo deployment does not by itself validate downstream model-performance gains",
    ],
    7: [
        "Inference-time scaling, chain-of-thought, test-time compute, and model scale can improve reasoning without changing training-data composition",
    ],
}

# Per-beat honesty constraints: things the narrative must NOT overclaim.
HONESTY_CONSTRAINTS = {
    1: [
        "Do NOT claim all synthetic data is harmful",
        "Do NOT treat pretraining collapse as an independent proof line for the post-training thesis",
        "Do NOT claim web-scale contamination is proven -- only domain-specific evidence exists",
        "Do NOT claim detection is impossible -- only that it is fragile under adversarial conditions",
    ],
    2: [
        "Do NOT claim web-wide pretraining degradation is demonstrated",
        "Frame as background motivation and rising risk, not demonstrated failure",
        "Explicitly state: no post-2022 web-scale contamination audit exists in the corpus",
    ],
    3: [
        "Do NOT present L_auth as a validated law or discovery",
        "Frame L_auth as a descriptive framework for fine-tuning data-authenticity effects",
        "Do NOT claim stage-agnostic validation; pretraining operationalization is future work",
        "Do NOT claim L_auth is a detection tool",
        "Explicitly state that weight calibration is future work",
    ],
    4: [
        "Do NOT claim human data is universally indispensable for alignment",
        "Do NOT claim AI feedback fails on social tasks -- corpus lacks direct evidence for this",
        "Frame as especially valuable for socially grounded tasks, not always necessary",
    ],
    5: [
        "Frame as pilot study at fixed inference-time compute, not complete validation",
        "Use 'initial evidence suggests' not 'demonstrates'",
        "Acknowledge: 3B model may not amplify data quality differences sufficiently",
        "Acknowledge: D1 and D4 co-vary in this design, cannot separate independent contributions",
        "Acknowledge: inference-time scaling remains a competing explanation outside the fixed-compute setup",
    ],
    6: [
        "CampusGo may be presented as deployed/open-source infrastructure, not as validated downstream training efficacy",
        "Do NOT use: 'proves' or 'validates model improvement'",
        "Acknowledge: platform effectiveness for model training remains untested",
        "Acknowledge: provenance and consent are design contributions, not evidence that every collected datum is high-value",
    ],
    7: [
        "Do NOT dismiss inference-time scaling",
        "Present competing mechanisms as genuine scope limiters",
        "If evidence shows strong social-reasoning gains from inference-time scaling alone, narrow L_auth to data-composition effects at fixed compute",
        "Beat 7 succeeds by honest scoping, not by defending the thesis at all costs",
    ],
}

# Narrative verb rules based on citation chain verification.
CITATION_VERB_RULES = {
    "verified_citation": "Use 'extends' 'builds on' 'responding to'",
    "no_citation_but_thematically_related": "Use 'in a parallel line of inquiry' 'complementary evidence from' 'independently'",
    "contradicts": "Use 'in contrast' 'challenges' 'narrows the scope of'",
}

# Target paper counts per category after demoting motivation beats and adding K.
CATEGORY_TARGETS = {
    "A": 8,
    "B": 17,
    "C": 5,
    "D": 22,
    "E": 10,
    "F": 17,
    "G": 12,
    "H": 12,
    "I": 12,
    "J": 12,
    "K": 8,
}
