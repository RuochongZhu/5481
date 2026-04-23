"""State machine: load/save/transition state.json for pipeline resumability."""

from __future__ import annotations

import copy
import os
import logging
from datetime import datetime, timezone
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

def _initial_stats() -> dict:
    return {
        "total_api_calls_llm": 0,
        "total_api_calls_anthropic": 0,
        "total_api_calls_openai": 0,
        "total_api_calls_s2": 0,
        "total_api_calls_openalex": 0,
        "total_api_calls_lens": 0,
        "total_api_calls_crossref": 0,
        "total_api_calls_opencitations": 0,
        "total_api_calls_arxiv": 0,
        "total_tokens_input": 0,
        "total_tokens_output": 0,
        "total_tokens_used": 0,
        "estimated_cost_usd": 0.0,
    }


INITIAL_STATE = {
    "version": "3.3",
    "created_at": None,
    "updated_at": None,
    "current_phase": 1,
    "phases": {
        "1": {
            "status": "pending",
            "steps": {
                "openalex_search": {"status": "pending", "queries_completed": 0, "papers_found": 0},
                "lens_search": {"status": "pending", "queries_completed": 0, "papers_found": 0},
                "s2_citation_expansion": {"status": "pending", "seeds_processed": 0, "papers_added": 0},
                "arxiv_search": {"status": "pending", "papers_found": 0},
                "manual_import": {"status": "pending", "files_imported": [], "papers_added": 0},
                "dedup_and_merge": {"status": "pending", "total_before": 0, "total_after": 0},
                "pdf_download": {"status": "pending", "attempted": 0, "downloaded": 0, "skipped": 0},
            },
            "quality_check": {"total_papers": 0, "passed": False},
        },
        "2": {
            "status": "pending",
            "steps": {
                "classification": {"status": "pending", "papers_classified": 0, "total_papers": 0, "last_batch_index": 0},
                "consistency_check": {"status": "pending", "disagreement_count": 0, "disagreement_rate": 0.0},
            },
            "quality_check": {"na_rate": 0.0, "disagreement_rate": 0.0, "passed": False},
        },
        "2.5": {
            "status": "pending",
            "steps": {
                "grobid_parse": {
                    "status": "pending",
                    "papers_considered": 0,
                    "parsed": 0,
                    "missing_pdf": 0,
                    "failed": 0,
                },
                "mineru_convert": {"status": "pending", "converted": 0},
                "deep_extraction": {"status": "pending", "papers_extracted": 0, "last_batch_index": 0},
                "merge_deep": {"status": "pending"},
            },
        },
        "3": {
            "status": "pending",
            "steps": {
                "build_graph": {"status": "pending"},
                "citation_intent": {"status": "pending", "edges_enriched": 0},
                "compute_metrics": {"status": "pending"},
                "intersection_matrix": {"status": "pending"},
                "relationship_analysis": {"status": "pending"},
                "gap_synthesis": {"status": "pending"},
            },
            "quality_check": {"passed": False},
        },
        "3.5": {
            "status": "pending",
            "steps": {
                "citation_expansion": {"status": "pending", "papers_expanded": 0},
                "narrative_chains": {"status": "pending", "beats_processed": 0},
                "writing_outline": {"status": "pending"},
            },
        },
        "3.7": {
            "status": "pending",
            "steps": {
                "contradiction_scan": {"status": "pending", "contradictions_found": 0},
                "contradiction_report": {"status": "pending"},
            },
        },
        "3.8": {
            "status": "pending",
            "steps": {
                "fetch_embeddings": {"status": "pending", "papers_embedded": 0},
            },
        },
        "4": {
            "status": "pending",
            "steps": {
                "score_gaps": {"status": "pending"},
                "advisor_alignment": {"status": "pending"},
                "thesis_generation": {"status": "pending"},
                "final_report": {"status": "pending"},
            },
        },
        "5": {
            "status": "pending",
            "steps": {
                "data_scores": {"status": "pending"},
                "reviewer_eval": {"status": "pending"},
                "aggregate": {"status": "pending"},
                "eval_report": {"status": "pending"},
            },
        },
    },
    "stats": _initial_stats(),
}

# Ordered list of all phases for sequential execution
PHASE_ORDER = ["1", "2", "2.5", "3", "3.5", "3.7", "3.8", "4", "5"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state(state_path: str) -> dict:
    """Load state.json or create initial state if missing."""
    if os.path.exists(state_path):
        state = load_json(state_path)
        # Migrate v1 → v2 if needed
        state = migrate_state(state)
        log.info(f"Loaded state: phase {state['current_phase']}")
        return state
    state = {**INITIAL_STATE, "created_at": _now(), "updated_at": _now()}
    save_state(state_path, state)
    log.info("Created initial state.json")
    return state


def save_state(state_path: str, state: dict) -> None:
    """Atomic save of state.json."""
    state["updated_at"] = _now()
    atomic_write_json(state_path, state)


def update_step(state: dict, phase: int | str, step: str, updates: dict) -> dict:
    """Update a specific step within a phase."""
    p = str(phase)
    state["phases"][p]["steps"][step].update(updates)
    return state


def complete_step(state: dict, state_path: str, phase: int | str, step: str, updates: dict | None = None) -> dict:
    """Mark a step as completed and save."""
    p = str(phase)
    if updates:
        state["phases"][p]["steps"][step].update(updates)
    state["phases"][p]["steps"][step]["status"] = "completed"
    save_state(state_path, state)
    log.info(f"Phase {phase} step '{step}' completed")
    return state


def start_phase(state: dict, state_path: str, phase: int | str) -> dict:
    """Mark a phase as in_progress."""
    p = str(phase)
    state["phases"][p]["status"] = "in_progress"
    state["current_phase"] = p
    save_state(state_path, state)
    log.info(f"Phase {phase} started")
    return state


def complete_phase(state: dict, state_path: str, phase: int | str) -> dict:
    """Mark a phase as completed."""
    p = str(phase)
    state["phases"][p]["status"] = "completed"
    save_state(state_path, state)
    log.info(f"Phase {phase} completed")
    return state


def get_current_phase(state: dict) -> str:
    """Return the earliest incomplete phase key."""
    for p in PHASE_ORDER:
        if state["phases"].get(p, {}).get("status") != "completed":
            return p
    return PHASE_ORDER[-1]


def is_phase_complete(state: dict, phase: int | str) -> bool:
    return state["phases"].get(str(phase), {}).get("status") == "completed"


def is_step_complete(state: dict, phase: int | str, step: str) -> bool:
    p = str(phase)
    return state["phases"].get(p, {}).get("steps", {}).get(step, {}).get("status") == "completed"


def reset_phase_tree(state: dict, state_path: str, start_phase: int | str) -> dict:
    """Reset a phase and all downstream phases back to initial defaults."""
    start = str(start_phase)
    if start not in PHASE_ORDER:
        return state

    start_idx = PHASE_ORDER.index(start)
    for phase in PHASE_ORDER[start_idx:]:
        state["phases"][phase]["status"] = "pending"
        state["phases"][phase]["steps"] = copy.deepcopy(INITIAL_STATE["phases"][phase]["steps"])
        if "quality_check" in INITIAL_STATE["phases"][phase]:
            state["phases"][phase]["quality_check"] = copy.deepcopy(
                INITIAL_STATE["phases"][phase]["quality_check"]
            )
        elif "quality_check" in state["phases"][phase]:
            state["phases"][phase].pop("quality_check", None)

    state["current_phase"] = start
    save_state(state_path, state)
    log.info(f"Reset phase {start} and downstream phases to pending")
    return state


def migrate_state(state: dict) -> dict:
    """Migrate older state versions by adding missing phase/step entries."""
    version = state.get("version", "1.0")
    for p_key in PHASE_ORDER:
        if p_key not in state["phases"]:
            state["phases"][p_key] = {
                "status": "pending",
                "steps": {
                    k: dict(v) for k, v in INITIAL_STATE["phases"][p_key]["steps"].items()
                },
            }
            if "quality_check" in INITIAL_STATE["phases"][p_key]:
                state["phases"][p_key]["quality_check"] = dict(
                    INITIAL_STATE["phases"][p_key]["quality_check"]
                )
        else:
            # Add missing steps within existing phases
            for step_key, step_val in INITIAL_STATE["phases"][p_key]["steps"].items():
                if step_key not in state["phases"][p_key].get("steps", {}):
                    state["phases"][p_key].setdefault("steps", {})[step_key] = dict(step_val)

    stats = state.setdefault("stats", {})
    for key, value in _initial_stats().items():
        stats.setdefault(key, value)

    state["version"] = "3.3"
    return state


def bump_stats(state: dict, anthropic_calls: int = 0, s2_calls: int = 0, tokens: int = 0):
    """Increment API usage counters."""
    state["stats"]["total_api_calls_anthropic"] += anthropic_calls
    state["stats"]["total_api_calls_s2"] += s2_calls
    state["stats"]["total_tokens_used"] += tokens
    # Rough cost estimate: $3/M input + $15/M output for Sonnet, assume 50/50 split
    state["stats"]["estimated_cost_usd"] = round(state["stats"]["total_tokens_used"] * 9e-6, 2)


def merge_usage_delta(state: dict, usage_delta: dict | None):
    """Merge provider-level runtime telemetry into persistent state."""
    if not usage_delta:
        return state

    stats = state.setdefault("stats", {})
    for key, default in _initial_stats().items():
        stats.setdefault(key, default)

    call_key_map = {
        "anthropic": "total_api_calls_anthropic",
        "openai": "total_api_calls_openai",
        "s2": "total_api_calls_s2",
        "openalex": "total_api_calls_openalex",
        "lens": "total_api_calls_lens",
        "crossref": "total_api_calls_crossref",
        "opencitations": "total_api_calls_opencitations",
        "arxiv": "total_api_calls_arxiv",
    }

    llm_calls = 0
    for provider, stat_key in call_key_map.items():
        calls = int(usage_delta.get("api_calls", {}).get(provider, 0) or 0)
        if calls:
            stats[stat_key] += calls
            if provider in {"anthropic", "openai"}:
                llm_calls += calls

    stats["total_api_calls_llm"] += llm_calls

    input_tokens = int(usage_delta.get("tokens", {}).get("input", 0) or 0)
    output_tokens = int(usage_delta.get("tokens", {}).get("output", 0) or 0)
    total_tokens = int(usage_delta.get("tokens", {}).get("total", input_tokens + output_tokens) or 0)

    stats["total_tokens_input"] += input_tokens
    stats["total_tokens_output"] += output_tokens
    stats["total_tokens_used"] += total_tokens
    stats["estimated_cost_usd"] = round(
        stats.get("estimated_cost_usd", 0.0) + float(usage_delta.get("estimated_cost_usd", 0.0) or 0.0),
        4,
    )
    return state
