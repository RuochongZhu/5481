# Pipeline Upgrade Run Log — 2026-04-12/13

## What Was Done

Upgraded pipeline from 5-beat linear structure to 6-beat dual-argument-line structure:
- Line 1 (pretraining risk): Beat 1 (Collapse A,B,C) + Beat 2 (Web Drift D,H)
- Bridge: Beat 3 (L_auth D,A)
- Line 2 (fine-tuning experimental): Beat 4 (Social Reasoning F,I,J) + Beat 5 (Experiment F,I,J)
- Proposal: Beat 6 (CampusGo G)

## Files Modified (14 files)

- `config/beat_definitions.py` — NEW: centralized beat config
- `src/prompts.py` — 4 agent prompts updated to 6-beat
- `src/scoring.py` — 6-beat scoring, honesty minimum, raised thresholds
- `src/phase3_5_narrative.py` — 6-beat narrative, argument line separation, citation_chains.json integration
- `src/phase3_7_contradiction.py` — corrected beat attributions, argument line imports
- `src/phase4_topics.py` — 6-beat evidence inventory
- `src/phase3_graph.py` — 6-beat BEAT_REQUIREMENTS
- `src/knowledge_base.py` — 6-beat categories
- `src/phase_contracts.py` — accepts 5 or 6 beats, auto-fixes malformed contradictions
- `src/phase5_evaluate.py` — evidence coverage /6
- `src/visualize.py` — 6-beat heatmap labels
- `main.py` — target score, demo mode, status display, arg handling fix
- `.env` — TARGET_SCORE, HONESTY_MIN
- `CLAUDE.md` — documents new structure

## Pipeline Run Results (32 evaluations total)

### Best scores achieved (across all runs):
- Overall: 0.822 (old 5-beat), 0.75 (new 6-beat with GPT-5.4)
- Narrative: 0.84 (old), 0.72 (new 6-beat, Anthropic fallback)
- Contradiction: 0.87
- Gap: 0.81
- Coverage: 0.89 (old), 0.78 (new)
- Honesty: 0.86

### Current state (latest evaluation):
- Overall: 0.65 (narrative reviewer dragging it down)
- Narrative: 0.40 (GPT-5.4 is very strict on Beat 2)
- Contradiction: 0.82
- Gap: 0.58
- Coverage: 0.73
- Honesty: 0.86

## Issues Encountered

1. **check_citations.py crash** — `refs_data.get("data", [])` returned None for some S2 responses. Fixed with `or []` fallback.

2. **Malformed contradiction entries** — LLM occasionally produces contradictions with missing `paper_b.paperId`. Happened twice. Fixed by adding auto-cleanup in `ensure_contradictions_valid()`.

3. **OpenAI quota exhaustion** — GPT-5.4 quota ran out mid-run. All LLM calls fell back to Anthropic REST. Scores during fallback period were more stable (0.72-0.73 range) but lower ceiling.

4. **Phase 4 evidence inventory** — GPT-5.4 medium effort consistently hits max_output_tokens on the full 6-beat inventory prompt. Falls back to low effort or Anthropic. Sometimes produces only 3-4 beats instead of 6.

5. **TARGET_SCORE arg override bug** — `main.py --auto` was overriding `.env` TARGET_SCORE with the arg default (0.85). Fixed by making the arg default `None` and only setting env if explicitly provided.

6. **Narrative reviewer structural complaint** — GPT-5.4 narrative reviewer consistently scores Beat 2 (Web Drift) as the weakest link. Core issue: only 18 papers in D+H categories, H has only 9 papers. The reviewer wants stronger temporal/web-drift anchors and more explicit limitation-admitting language. This is a corpus limitation, not a pipeline bug.

7. **S2 429 rate limiting** — Frequent 429 responses during citation expansion. Handled by existing backoff logic (3s delay). 5 papers failed to expand due to NoneType responses.

## Actionable Next Steps

1. **Supplement H-category papers** — Run targeted Phase 1 search for temporal web quality measurement papers to strengthen Beat 2
2. **Re-run with full quota** — Once both OpenAI and Anthropic quotas are fresh, a clean run should score higher
3. **Consider adjusting narrative reviewer prompt** — The GPT-5.4 narrative reviewer may be too strict for a 6-beat structure where some beats (2, 5, 6) are intentionally weaker/proposal-framed
