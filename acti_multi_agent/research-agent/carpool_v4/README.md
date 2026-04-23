# carpool_v4 — Research-Agent Pipeline v4 (CampusRide)

v4 pipeline workspace for the **CampusRide** HCI design-case paper. Adapted
from the L_auth v3 research-agent pipeline (preserved in the parent directory
`../`). The 8-phase architecture is unchanged; what changed is the thesis,
the 7-beat topic mapping, the A-J category taxonomy, the 5 focus questions,
and the reviewer evaluation context.

## Quick Orientation

- Paper outline: `../paper_outline_v4.md`
- Migration spec (what changed vs L_auth): `../pipeline_v4_migration_and_config.md`
- Local-AI risk prompts (R1-R6): `../local_ai_risk_resolution_prompts.md`
- Project constraints (quality gates, verb discipline): `CLAUDE.md`
- Thesis constant: `src/thesis_v4.py`
- Beat / category / argument-line source of truth: `config/beat_definitions.py`

## Running

```bash
cd carpool_v4

# One-time W1 setup
cp ../.env .env          # reuse API keys
python main.py --status  # verify clean state

# Phase 1: corpus assembly (W1)
python main.py --phase 1

# All phases sequentially
python main.py

# Auto-loop: pipeline + eval + backtrack until target score
python main.py --auto

# Resume from last checkpoint
python main.py --phase 2.5 --resume
```

## Key v4 Changes vs. L_auth

- Thesis: CampusRide multi-module campus platform with carpool deep-dive, not AI
  training data authenticity. See `src/thesis_v4.py`.
- Categories: A-J (10 categories). K (competing mechanisms) has been removed.
- Beat mapping: sections §2.1, §2.2, §2.3, §4.1, §4.2, §5, §7.2.
- Beats 4 and 6 are primary_data and artifact respectively; they use
  pseudo-anchors (`local:CornellCarpoolSurvey2026`, `local:CampusRideSystem2026`)
  in `config/manual_core_inclusions.json::primary_anchors`. `phase_contracts.py`
  has been minimally relaxed to allow pseudo-anchors for these beats.
- 5 reviewer prompts in `src/scoring.py::REVIEWER_PROMPTS` were rewritten;
  `PAPER_CONTEXT_V4` is injected at the top of every reviewer context.
- 5 focus questions (F1 Gap, F2 Grassroots, F3 .edu, F4 Rating, F5 Gamification)
  in `src/phase3_7_contradiction.py::CONTRADICTION_FOCUS_CONFIGS`.

Old L_auth pipeline remains untouched in the parent directory for reference.
