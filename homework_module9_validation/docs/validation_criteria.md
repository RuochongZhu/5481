# Validation Criteria

## Overview

The validation system evaluates AI-generated earthquake situation reports across
**5 customized dimensions**, each scored by a distinct AI reviewer persona on a
0-10 scale anchored to a 5-item binary checklist. The dimension scores combine
into a single weighted composite (range 0-10).

## Full rubric table

| # | Dimension | Persona | What it measures | Scale | Weight |
|---|-----------|---------|------------------|-------|--------|
| 1 | **Factual Grounding** | Data Integrity Auditor | All numeric claims trace to source data; no invented places/events; no unsupported predictions | 0-10 anchored to a 5-item checklist | 30% |
| 2 | **Operational Actionability** | Emergency Response Coordinator | Concrete decision-support: named regions, recommended actions, monitoring guidance, next-step priorities | 0-10 anchored to a 5-item checklist | 20% |
| 3 | **Communication Clarity** | Public Information Officer | Inverted-pyramid structure, plain language, scannable formatting, no filler/redundancy | 0-10 anchored to a 5-item checklist | 15% |
| 4 | **Calibrated Uncertainty** | Skeptical Science Editor | Appropriate hedging, acknowledges data limits, no false precision, no pseudo-predictions | 0-10 anchored to a 5-item checklist | 20% |
| 5 | **Completeness Compliance** | Editor-in-Chief | Required sections present and substantive: exec summary, key signals, risk watch, data caveats, recommended actions | 0-10 anchored to a 5-item checklist | 15% |

Weights are encoded in `src/config.py::REVIEW_WEIGHTS` and sum to 1.0 (validated at import).

**Composite = Σ (dimension_score × weight)**

## Per-dimension checklist details

Each reviewer evaluates **5 binary pass/fail items** specific to its dimension.
A passing checklist score floor for each band is built into the prompt:

| Score | Checklist count | Meaning |
|-------|-----------------|---------|
| 9-10  | 5 pass          | Dimension is exemplary |
| 7-8   | 4 pass          | Minor issue, otherwise sound |
| 5-6   | 3 pass          | Mixed: notable strength + notable weakness |
| 3-4   | 1-2 pass        | Failing on this dimension |
| 0-2   | 0 pass          | Severely deficient |

### Factual Grounding (Data Integrity Auditor)
1. `all_event_counts_traceable` — all numeric counts in the report appear in the digest's summary or are derivable from sample_events
2. `all_places_in_digest` — every place name cited appears in `digest.sample_events[*].place` or `digest.summary.top_regions`
3. `magnitudes_within_data_range` — any magnitude cited falls within the digest's [min, max] and is supported by a specific sample event
4. `no_unsupported_predictions` — the report does NOT predict specific future earthquakes (date / location / magnitude); general monitoring framing is allowed
5. `no_invented_metadata` — depth ranges, tsunami flags, dates all match the digest

### Operational Actionability (Emergency Response Coordinator)
1. `names_specific_regions` — names ≥3 specific regions, not "various regions"
2. `gives_quantified_signals` — at least one risk signal is quantified with a number
3. `concrete_monitoring_priorities` — risk-watch content names specific watch items
4. `decision_grade_recommendations` — at least one explicit action a coordinator could take in 24h
5. `prioritization_visible` — distinguishes high-priority from low-priority signals

### Communication Clarity (Public Information Officer)
1. `inverted_pyramid_structure` — leads with the most important takeaway
2. `clear_section_structure` — clearly labeled section headings
3. `plain_language` — technical jargon avoided or briefly explained
4. `scannable_formatting` — bullets/lists where appropriate; no wall-of-text
5. `no_filler_or_redundancy` — no boilerplate phrases, no repetition

### Calibrated Uncertainty (Skeptical Science Editor)
1. `appropriate_hedging` — hedged language ("suggests", "indicates") when warranted
2. `acknowledges_data_limits` — explicit caveat about data source, window, threshold
3. `no_false_precision` — no invented precision (e.g., "60% probability of M5+ in 48h")
4. `no_pseudo_predictions` — does not assert a specific future earthquake will occur
5. `distinguishes_signal_from_noise` — explains WHY an area is high-risk (clustering, magnitude, plate boundary)

### Completeness Compliance (Editor-in-Chief)
1. `has_executive_summary` — 2-4 sentence opening / labeled summary
2. `has_key_signals_section` — ≥3 specific signal items in a list / section
3. `has_risk_watch_section` — "next 7 days" / "watch list" framed as monitoring
4. `has_data_caveats_section` — explicit data-caveat / data-limitation section
5. `has_recommended_actions` — ≥2 specific actions in a labeled section

## How this differs from the LAB's Likert scales

The LAB (`lab_ai_reporter.py`) generates reports but does NOT validate them with
multiple criteria or run statistical comparisons. The Module 9 LAB
`LAB_ai_quality_control.md` (referenced in the homework prompt) uses a single
1-5 Likert scale per dimension. Our system departs from both as follows:

| Feature                          | LAB Likert (single rater)                       | This system (5-reviewer panel)                              |
|----------------------------------|-------------------------------------------------|--------------------------------------------------------------|
| **Raters per report**            | 1                                               | 5 (one per dimension)                                        |
| **Scale**                        | 1-5 Likert                                       | 0-10 anchored to a 5-item binary checklist + qualitative   |
| **Persona**                      | none (generic AI rater)                          | each dimension has a distinct domain persona                 |
| **Auditability**                 | one number, no justification                    | each item produces evidence quotes and specific criticisms   |
| **Score combination**            | unweighted mean                                  | weighted composite (factual carries more weight)             |
| **JSON schema**                  | unstructured text                                | strict JSON, validated by parser with repair fallback        |
| **Bias mitigation**              | single rater drifts                              | role-isolated reviewers, each pinned to one dimension only   |
| **Reproducibility**              | depends on rater wording                         | binary checklist items reduce inter-rater drift              |
| **Score interpretability**       | "what does 3/5 mean?"                            | 3 of 5 checklist items passed -> tied to specific failures   |
| **Cross-validation across runs** | n/a                                              | reviewers run at temperature 0 -> deterministic              |

## Reviewer prompt structure

Each of the 5 reviewer prompts has 3 sections (mirroring `PAPER_CONTEXT_V4`
injection in carpool_v4):

1. **Shared evaluation context** (`prompts/_shared_context.txt`) — what an
   earthquake situation report is, who reads it, what evidence standards apply.
   This is injected into every reviewer to keep yardsticks consistent.

2. **Persona-specific role** — e.g., "You are the DATA INTEGRITY AUDITOR. Your
   job — and only job — is to verify that..."

3. **Dimension-specific rubric** — 5 binary checklist items + scoring guidance +
   strict JSON output schema with named keys.

## Reviewer output schema

```json
{
  "dimension": "factual_grounding",
  "persona": "Data Integrity Auditor",
  "score_0_10": 7.5,
  "checklist": {
    "all_event_counts_traceable": true,
    "all_places_in_digest": true,
    "magnitudes_within_data_range": false,
    "no_unsupported_predictions": true,
    "no_invented_metadata": true
  },
  "checklist_count": 4,
  "evidence_quotes": ["quote from report supporting an item", "..."],
  "criticisms": ["specific failure 1", "..."],
  "would_publish": "yes" | "no" | "conditional"
}
```

`src/reviewer.py::_parse_reviewer_json` validates this schema and clips scores
to [0, 10]. A JSON-repair fallback handles the common LLM error of splitting a
quoted string into two adjacent quote-spans glued by an em-dash.

## Aggregation

```python
composite = sum(score[d] * weight[d] for d in dimensions)
```

The composite is the primary outcome variable for the ANOVA in
`statistical_analysis.py`. Per-dimension scores are analyzed secondarily
(per-dimension ANOVA with Bonferroni-corrected α = 0.01).
