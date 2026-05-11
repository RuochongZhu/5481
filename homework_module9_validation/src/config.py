"""Project-wide configuration constants."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv


def _load_env() -> Path:
    here = Path(__file__).resolve().parent.parent
    candidates = [
        here / ".env",
        here.parent / "acti_multi_agent" / "research-agent" / "carpool_v4" / ".env",
        here.parent / "acti_multi_agent" / "research-agent" / ".env",
    ]
    for path in candidates:
        if path.exists():
            load_dotenv(path, override=False)
            return path
    raise FileNotFoundError(
        f"No .env file found. Searched: {[str(p) for p in candidates]}"
    )


ENV_PATH: Final[Path] = _load_env()
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

# Model selection (hard-coded for reproducibility; the homework compares prompts,
# not models, so we hold the model constant). Override via env if needed.
# Sonnet-4.6 is used for both roles to keep cost reasonable and isolate the
# prompt as the only varying factor across generation runs.
GEN_MODEL: Final[str] = os.getenv("HOMEWORK_GEN_MODEL", "claude-sonnet-4-6")
REVIEW_MODEL: Final[str] = os.getenv("HOMEWORK_REVIEW_MODEL", "claude-sonnet-4-6")

# Sampling temperatures
GEN_TEMPERATURE: Final[float] = float(os.getenv("GEN_TEMPERATURE", "0.7"))
REVIEW_TEMPERATURE: Final[float] = float(os.getenv("REVIEW_TEMPERATURE", "0.0"))

# Token budgets
GEN_MAX_TOKENS: Final[int] = 1500
REVIEW_MAX_TOKENS: Final[int] = 2048

# Sample size
N_VARIANTS: Final[int] = int(os.getenv("N_VARIANTS", "12"))

# Prompt IDs
PROMPT_IDS: Final[tuple[str, str, str]] = ("prompt_a", "prompt_b", "prompt_c")
PROMPT_LABELS: Final[dict[str, str]] = {
    "prompt_a": "A: Minimal",
    "prompt_b": "B: Structured",
    "prompt_c": "C: Enhanced",
}

# Reviewer IDs + display names
REVIEWER_IDS: Final[tuple[str, ...]] = (
    "factual_grounding",
    "operational_actionability",
    "communication_clarity",
    "calibrated_uncertainty",
    "completeness_compliance",
)

REVIEWER_PERSONAS: Final[dict[str, str]] = {
    "factual_grounding": "Data Integrity Auditor",
    "operational_actionability": "Emergency Response Coordinator",
    "communication_clarity": "Public Information Officer",
    "calibrated_uncertainty": "Skeptical Science Editor",
    "completeness_compliance": "Editor-in-Chief",
}

REVIEW_WEIGHTS: Final[dict[str, float]] = {
    "factual_grounding":         0.30,
    "operational_actionability": 0.20,
    "communication_clarity":     0.15,
    "calibrated_uncertainty":    0.20,
    "completeness_compliance":   0.15,
}
assert abs(sum(REVIEW_WEIGHTS.values()) - 1.0) < 1e-9, "weights must sum to 1.0"

# Score key names inside reviewer JSON responses
SCORE_KEY: Final[str] = "score_0_10"
CHECKLIST_KEY: Final[str] = "checklist"

# Paths
PROMPT_DIR: Final[Path] = PROJECT_ROOT / "prompts"
REVIEWER_PROMPT_DIR: Final[Path] = PROMPT_DIR / "reviewers"
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
VARIANT_DIR: Final[Path] = DATA_DIR / "variants"
SEED_DIGEST_PATH: Final[Path] = DATA_DIR / "seed_digest.json"

OUTPUT_DIR: Final[Path] = PROJECT_ROOT / "outputs"
REPORTS_DIR: Final[Path] = OUTPUT_DIR / "generated_reports"
REVIEWER_SCORES_DIR: Final[Path] = OUTPUT_DIR / "reviewer_scores"
RESULTS_DIR: Final[Path] = OUTPUT_DIR / "results"
FIGURES_DIR: Final[Path] = OUTPUT_DIR / "figures"

# API retry settings
MAX_RETRIES: Final[int] = 4
BASE_BACKOFF_SEC: Final[float] = 1.5

# Concurrency for the reviewer panel (per report)
REVIEWER_CONCURRENCY: Final[int] = 5
# Concurrency for the outer loop over (prompt, variant)
REPORT_CONCURRENCY: Final[int] = 3
