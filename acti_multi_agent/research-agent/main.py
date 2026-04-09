#!/usr/bin/env python3
"""
Research Agent Pipeline — 7-Phase Literature Analysis for PhD Thesis
=====================================================================

Domain: AI data quality / model collapse / synthetic data contamination / data authenticity

Pipeline:
  Phase 1    — Corpus Assembly (OpenAlex + S2 + arXiv + manual imports)
  Phase 2    — Classification (A-J taxonomy via Literature Scanner agent)
  Phase 2.5  — Deep Extraction (7 structured fields per paper)
  Phase 3    — Relationship Graph + Evidence Sufficiency Check
  Phase 3.5  — Narrative Chains (per-beat writing-ready paper ordering)
  Phase 3.7  — Contradiction Map (disagreements for academic honesty)
  Phase 4    — Evidence Inventory + Final Reports

Usage:
  python main.py                        # Run full pipeline (all 7 phases)
  python main.py --phase 1              # Run specific phase
  python main.py --phase 2.5            # Run Phase 2.5 (deep extraction)
  python main.py --phase 3.5 --resume   # Resume from last checkpoint
  python main.py --visualize            # Generate all 7 visualizations
  python main.py --import-file FILE     # Import CSV/BibTeX into data/raw/
  python main.py --demo                 # Architecture overview (no API calls)
  python main.py --status               # Show current pipeline state
"""

from __future__ import annotations

import argparse
import os
import sys
import shutil
import logging

# Ensure src is importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv

from src.utils import setup_logging, load_json
from src.state_manager import (
    load_state, save_state, start_phase, complete_phase,
    get_current_phase, is_phase_complete, PHASE_ORDER,
)
from src.api_client import OpenAlexClient, S2Client, ArxivClient, DEFAULT_MODEL

STATE_PATH = os.path.join(BASE_DIR, "state.json")
LOG_DIR = os.path.join(BASE_DIR, "agent_logs")

# Phase dependency map: phase → list of phases that must be complete first
PHASE_DEPS = {
    "1": [],
    "2": ["1"],
    "2.5": ["2"],
    "3": ["2"],
    "3.5": ["2.5", "3"],
    "3.7": ["2.5", "3"],
    "3.8": ["2"],
    "4": ["3", "3.5", "3.7"],
    "5": ["4"],
}

# Phases that need Anthropic API
NEEDS_ANTHROPIC = {"2", "2.5", "3", "3.5", "3.7", "4", "5"}

# Phases that benefit from S2 client
NEEDS_S2 = {"1", "3", "3.5", "3.8", "4"}


def get_anthropic_client():
    """Initialize Anthropic client."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)
    return Anthropic()


def get_search_clients():
    """Initialize 3-layer search clients: OpenAlex, S2, arXiv."""
    mailto = os.environ.get("OPENALEX_MAILTO", os.environ.get("MAILTO", "user@example.com"))
    oa_key = os.environ.get("OPENALEX_API_KEY")
    oa = OpenAlexClient(mailto=mailto, api_key=oa_key)
    s2_key = os.environ.get("S2_API_KEY")
    s2 = S2Client(api_key=s2_key)
    arxiv = ArxivClient()
    return oa, s2, arxiv


def check_deps(state: dict, phase: str) -> bool:
    """Check if all dependencies for a phase are satisfied."""
    for dep in PHASE_DEPS.get(phase, []):
        if not is_phase_complete(state, dep):
            log.error(f"Phase {phase} requires Phase {dep} to be complete first.")
            return False
    return True


def run_phase(phase: str, state: dict, client, oa, s2, arxiv, resume: bool = False):
    """Dispatch to the appropriate phase module.

    Wraps execution in try/except so that:
    - Fatal errors (wrong key, wrong model, quota) print a clear message and exit
    - Transient errors save state so you can --resume
    """
    from src.api_client import APIKeyMissing, QuotaExhausted, ModelNotFound

    if not check_deps(state, phase):
        return state

    state = start_phase(state, STATE_PATH, phase)

    try:
        if phase == "1":
            from src.phase1_corpus import run_phase1
            state = run_phase1(state, STATE_PATH, BASE_DIR, oa, s2, arxiv)

        elif phase == "2":
            from src.phase2_extraction import run_phase2
            state = run_phase2(state, STATE_PATH, BASE_DIR, client)

        elif phase == "2.5":
            from src.phase2_5_deep import run_phase2_5
            state = run_phase2_5(state, STATE_PATH, BASE_DIR, client)

        elif phase == "3":
            from src.phase3_graph import run_phase3
            state = run_phase3(state, STATE_PATH, BASE_DIR, client, s2)

        elif phase == "3.5":
            from src.phase3_5_narrative import run_phase3_5
            state = run_phase3_5(state, STATE_PATH, BASE_DIR, client, s2)

        elif phase == "3.7":
            from src.phase3_7_contradiction import run_phase3_7
            state = run_phase3_7(state, STATE_PATH, BASE_DIR, client)

        elif phase == "3.8":
            from src.phase3_8_embeddings import run_phase3_8
            state = run_phase3_8(state, STATE_PATH, BASE_DIR, s2)

        elif phase == "4":
            from src.phase4_topics import run_phase4
            state = run_phase4(state, STATE_PATH, BASE_DIR, client, s2)

        elif phase == "5":
            from src.phase5_evaluate import run_phase5
            state = run_phase5(state, STATE_PATH, BASE_DIR, client)

        state = complete_phase(state, STATE_PATH, phase)

    except APIKeyMissing as e:
        log.error(f"\n{'='*60}")
        log.error(f"  ❌ API KEY ERROR in Phase {phase}")
        log.error(f"{'='*60}")
        log.error(f"  {e}")
        log.error(f"  Fix: check ANTHROPIC_API_KEY in .env")
        log.error(f"  State saved — resume with: python main.py --phase {phase} --resume")
        save_state(STATE_PATH, state)
        sys.exit(1)

    except ModelNotFound as e:
        log.error(f"\n{'='*60}")
        log.error(f"  ❌ MODEL NOT FOUND in Phase {phase}")
        log.error(f"{'='*60}")
        log.error(f"  {e}")
        log.error(f"  Fix: check MODEL_FAST / MODEL_DEEP in .env")
        log.error(f"  Current: MODEL_FAST={os.environ.get('MODEL_FAST', 'default')}, "
                   f"MODEL_DEEP={os.environ.get('MODEL_DEEP', 'default')}")
        save_state(STATE_PATH, state)
        sys.exit(1)

    except QuotaExhausted as e:
        log.error(f"\n{'='*60}")
        log.error(f"  ❌ QUOTA EXHAUSTED in Phase {phase}")
        log.error(f"{'='*60}")
        log.error(f"  {e}")
        log.error(f"  State saved — resume later with: python main.py --phase {phase} --resume")
        save_state(STATE_PATH, state)
        sys.exit(1)

    except KeyboardInterrupt:
        log.warning(f"\n  ⚠ Interrupted by user during Phase {phase}")
        log.warning(f"  State saved — resume with: python main.py --phase {phase} --resume")
        save_state(STATE_PATH, state)
        sys.exit(130)

    except Exception as e:
        log.error(f"\n{'='*60}")
        log.error(f"  ❌ UNEXPECTED ERROR in Phase {phase}")
        log.error(f"{'='*60}")
        log.error(f"  {type(e).__name__}: {e}")
        log.error(f"  State saved — resume with: python main.py --phase {phase} --resume")
        save_state(STATE_PATH, state)
        raise  # Re-raise so traceback is visible for debugging

    return state


def run_full_pipeline(state: dict, client, oa, s2, arxiv):
    """Run all phases sequentially."""
    for phase in PHASE_ORDER:
        if is_phase_complete(state, phase):
            log.info(f"Phase {phase} already complete, skipping")
            continue
        log.info(f"\n{'='*60}")
        log.info(f"  PHASE {phase}")
        log.info(f"{'='*60}\n")
        state = run_phase(phase, state, client, oa, s2, arxiv)
    log.info("\nPipeline complete!")
    _print_summary(state)
    return state


def run_auto_loop(state: dict, client, oa, s2, arxiv, max_iterations: int = 5):
    """Auto-loop: run pipeline → Phase 5 evaluate → backtrack → repeat.

    Invariants:
    - Never delete papers (append-only corpus)
    - Never lower overall_score — if a change makes score worse, discard
    - Always save state before and after each iteration
    - Log every action to agent_logs/
    """
    from src.scoring import decide_action, aggregate_reviews
    from src.utils import load_json

    target = float(os.environ.get("TARGET_SCORE", "0.8"))
    log.info(f"Auto-loop: target={target}, max_iterations={max_iterations}")

    for iteration in range(1, max_iterations + 1):
        log.info(f"\n{'#'*60}")
        log.info(f"  AUTO-LOOP ITERATION {iteration}/{max_iterations}")
        log.info(f"{'#'*60}\n")

        # Step 1: Run full pipeline (skips completed phases)
        state = run_full_pipeline(state, client, oa, s2, arxiv)

        # Step 2: Reset Phase 5 for fresh evaluation
        for step in state["phases"].get("5", {}).get("steps", {}):
            state["phases"]["5"]["steps"][step]["status"] = "pending"
        state["phases"]["5"]["status"] = "pending"
        save_state(STATE_PATH, state)

        # Step 3: Run Phase 5 evaluation
        from src.phase5_evaluate import run_phase5
        state = start_phase(state, STATE_PATH, "5")
        state = run_phase5(state, STATE_PATH, BASE_DIR, client, iteration=iteration)
        state = complete_phase(state, STATE_PATH, "5")

        # Step 4: Read evaluation result
        eval_path = os.path.join(BASE_DIR, "analysis", "evaluation_result.json")
        if not os.path.exists(eval_path):
            log.error("Evaluation result not found")
            break

        result = load_json(eval_path)
        action = result.get("action", {})
        act = action.get("action", "done")

        if act == "done":
            log.info(f"\n✅ Target score reached! {action.get('reason', '')}")
            break

        elif act == "human":
            log.info(f"\n🛑 Human review needed: {action.get('reason', '')}")
            log.info("  Fix the issues, then re-run: python main.py --auto --resume")
            break

        elif act == "backtrack":
            target_phase = action.get("target_phase", "3")
            log.info(f"\n🔄 Backtracking to Phase {target_phase}: {action.get('reason', '')}")

            # Reset target phase and all downstream phases
            target_idx = PHASE_ORDER.index(target_phase) if target_phase in PHASE_ORDER else 0
            for p in PHASE_ORDER[target_idx:]:
                if p in state["phases"]:
                    state["phases"][p]["status"] = "pending"
                    for step in state["phases"][p].get("steps", {}):
                        state["phases"][p]["steps"][step]["status"] = "pending"
            save_state(STATE_PATH, state)

    log.info(f"\nAuto-loop finished after {iteration} iteration(s)")
    _print_summary(state)
    return state


def run_visualizations():
    """Generate all 7 visualizations."""
    from src.visualize import run_all_visualizations
    run_all_visualizations(BASE_DIR)


def handle_import(filepath: str):
    """Import a file into data/raw/."""
    raw_dir = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    dest = os.path.join(raw_dir, os.path.basename(filepath))
    shutil.copy2(filepath, dest)
    log.info(f"Imported {filepath} → {dest}")
    log.info("Run Phase 1 to incorporate into corpus.")


def show_status(state: dict):
    """Print current pipeline state."""
    print(f"\nCurrent phase: {state['current_phase']}")
    print(f"Updated: {state.get('updated_at', 'N/A')}\n")

    phase_labels = {
        "1": "Corpus Assembly",
        "2": "Classification (A-J)",
        "2.5": "Deep Extraction",
        "3": "Graph + Evidence Check",
        "3.5": "Narrative Chains",
        "3.7": "Contradiction Map",
        "4": "Evidence Inventory",
    }

    for p_key in PHASE_ORDER:
        p = state["phases"].get(p_key, {})
        status = p.get("status", "pending")
        icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(status, "❓")
        label = phase_labels.get(p_key, "")
        print(f"  Phase {p_key:>3s}: {icon} {status:<12s}  {label}")
        for step_name, step_data in p.get("steps", {}).items():
            s_icon = {"pending": "  ", "in_progress": "→ ", "completed": "✓ "}.get(
                step_data.get("status", "pending"), "  ")
            print(f"    {s_icon}{step_name}: {step_data.get('status', 'pending')}")

    # Check for output files
    print(f"\n  Output files:")
    output_files = [
        "output/evidence_sufficiency.md",
        "output/evidence_inventory.md",
        "output/corpus_by_category.md",
        "output/writing_outline.md",
        "output/contradiction_map.md",
        "output/figures/viz_results.json",
        "analysis/gaps_ranked.json",
        "analysis/narrative_chains.json",
        "analysis/contradictions.json",
        "data/processed/classified.json",
        "data/processed/deep_extracted.json",
    ]
    for f in output_files:
        path = os.path.join(BASE_DIR, f)
        exists = "✅" if os.path.exists(path) else "  "
        print(f"    {exists} {f}")

    stats = state.get("stats", {})
    print(f"\n  API calls — Anthropic: {stats.get('total_api_calls_anthropic', 0)}, "
          f"S2: {stats.get('total_api_calls_s2', 0)}")
    print(f"  Tokens used: {stats.get('total_tokens_used', 0)}")
    print(f"  Est. cost: ${stats.get('estimated_cost_usd', 0):.2f}\n")


def demo_mode():
    """Print architecture overview without API calls."""
    print("\n" + "="*60)
    print("  RESEARCH AGENT PIPELINE v2.0 — 7-PHASE ARCHITECTURE")
    print("="*60)
    print("""
  Goal: Collect targeted evidence to support a 5-beat paper thesis,
  then organize it into writing-ready narrative chains with
  contradiction awareness.

  Paper Thesis:
  Web-scraped training data is experiencing information degradation,
  while physically-verified authentic human social behavioral data
  provides irreplaceable training signals. CampusGo is a running
  platform designed to produce such data.

  5-Beat Evidence Chain:
  ──────────────────────
  Beat 1 (Crisis §2): Model collapse + web pollution + detection fails
    → Categories A, B, C
  Beat 2 (Empirical §4): Web quality measurably declining over time
    → Categories D, H
  Beat 3 (Theory §3): L_auth = λ₁·D_KL + λ₂·D_α + λ₃·(1-TTR_r)
    → Category D
  Beat 4 (Validation §5): Verified social data > web-scraped
    → Categories E, F, I, J
  Beat 5 (Solution §6): CampusGo maps L_auth to platform design
    → Categories A, G

  7-Phase Pipeline:
  ─────────────────
  Phase 1    Corpus Assembly (NO API KEY)
    Layer 1 → OpenAlex: 24 category-tagged queries
    Layer 2 → S2: citation expansion from 5 seed papers
    Layer 3 → arXiv: 9 category-specific queries
    → Deduplicate → Target: 180-220 papers

  Phase 2    Classification (ANTHROPIC_API_KEY)
    → Literature Scanner: classify into A-J (10 categories)
    → Batch 10 papers/call, resumable

  Phase 2.5  Deep Extraction (ANTHROPIC_API_KEY)        ← NEW
    → 7 structured fields per paper: method_type, key_claim,
      methodology, limitation, what_it_does_NOT_address,
      dataset_or_benchmark, theoretical_framework
    → Data foundation for P3.5 and P3.7

  Phase 3    Relationship Graph + Evidence Check
    → NetworkX citation graph + graph metrics
    → Relationship Analyst: refine edges
    → Gap Synthesizer: assess beat sufficiency

  Phase 3.5  Narrative Chains (ANTHROPIC + S2)           ← NEW
    → Full pairwise citation expansion (200 S2 calls)
    → Per-beat narrative spine + paragraph outline
    → Writing-ready Related Work structure

  Phase 3.7  Contradiction Map (ANTHROPIC_API_KEY)       ← NEW
    → Identify disagreements between papers
    → Severity rating: critical / moderate / minor
    → Suggested handling for each contradiction

  Phase 4    Evidence Inventory + Final Reports
    → Structured evidence list per beat
    → 5 output reports (md)

  Visualizations (--visualize):
  ─────────────────────────────
  V1  Category Sunburst (plotly)
  V2  Citation Force Graph (pyvis)
  V3  Beat × Category Heatmap (matplotlib)
  V4  Publication Timeline (plotly)
  V5  Contradiction Graph (networkx)
  V6  Beat Sankey Flow (plotly)
  V7  3D Embedding Cloud (UMAP + plotly)

  6 Specialized Agents:
  ─────────────────────
  1. Literature Scanner    — classifies papers into A-J
  2. Deep Extractor        — extracts 7 structured fields     ← NEW
  3. Relationship Analyst  — builds citation graph edges
  4. Gap Synthesizer       — assesses beat evidence strength
  5. Narrative Analyst     — constructs per-beat story spine   ← NEW
  6. Contradiction Mapper  — finds disagreements               ← NEW

  To run: set ANTHROPIC_API_KEY in .env, then:
    python main.py --phase 1        # Start with corpus assembly
    python main.py                  # Run full pipeline
    python main.py --visualize      # Generate figures
""")
    print("="*60 + "\n")


def _print_summary(state: dict):
    """Print final pipeline summary."""
    stats = state.get("stats", {})
    print(f"\n{'='*60}")
    print(f"  PIPELINE SUMMARY")
    print(f"{'='*60}")
    print(f"  API calls — Anthropic: {stats.get('total_api_calls_anthropic', 0)}, "
          f"S2: {stats.get('total_api_calls_s2', 0)}")
    print(f"  Tokens: {stats.get('total_tokens_used', 0)}")
    print(f"  Est. cost: ${stats.get('estimated_cost_usd', 0):.2f}")
    print(f"\n  Key outputs:")
    key_outputs = [
        "output/evidence_sufficiency.md",
        "output/writing_outline.md",
        "output/contradiction_map.md",
        "output/evidence_inventory.md",
        "output/corpus_by_category.md",
    ]
    for f in key_outputs:
        path = os.path.join(BASE_DIR, f)
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"    {exists} {f}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research Agent Pipeline v3.0")
    parser.add_argument("--phase", type=str,
                        choices=PHASE_ORDER,
                        help="Run a specific phase (1, 2, 2.5, 3, 3.5, 3.7, 3.8, 4, 5)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from last checkpoint")
    parser.add_argument("--visualize", action="store_true",
                        help="Generate all 7 visualizations")
    parser.add_argument("--auto", action="store_true",
                        help="Auto-loop: run pipeline → evaluate → backtrack → repeat until target score")
    parser.add_argument("--max-iterations", type=int, default=5,
                        help="Max iterations for --auto mode (default: 5)")
    parser.add_argument("--target-score", type=float, default=0.8,
                        help="Target overall score for --auto mode (default: 0.8)")
    parser.add_argument("--import-file", dest="import_file", type=str,
                        help="Import CSV/BibTeX file into data/raw/")
    parser.add_argument("--demo", action="store_true",
                        help="Show architecture overview (no API calls)")
    parser.add_argument("--status", action="store_true",
                        help="Show current pipeline state")
    parser.add_argument("--model", type=str, default=None,
                        help="Override model (e.g. claude-opus-4-6)")
    args = parser.parse_args()

    # Load .env — check both research-agent/.env and parent acti_multi_agent/.env
    env_path = os.path.join(BASE_DIR, ".env")
    parent_env = os.path.join(os.path.dirname(BASE_DIR), ".env")
    if os.path.exists(parent_env):
        load_dotenv(parent_env)  # Load parent first (lower priority)
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)  # Local overrides parent

    # Setup logging
    log = setup_logging(LOG_DIR, phase=args.phase)

    # Demo mode
    if args.demo:
        demo_mode()
        sys.exit(0)

    # Import mode
    if args.import_file:
        handle_import(args.import_file)
        sys.exit(0)

    # Load state
    state = load_state(STATE_PATH)

    # Status mode
    if args.status:
        show_status(state)
        sys.exit(0)

    # Visualize mode
    if args.visualize:
        log.info("Generating visualizations")
        run_visualizations()
        sys.exit(0)

    # Override model if specified
    if args.model:
        import src.api_client as ac
        ac.DEFAULT_MODEL = args.model
        log.info(f"Model override: {args.model}")

    # Phase 1 doesn't need Anthropic key — only search APIs (all free, no key)
    # Phase 2+ need Anthropic key for Claude agents
    need_anthropic = args.phase is None or args.phase in NEEDS_ANTHROPIC
    if need_anthropic and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set. Phase 2+ require it.")
        print("Phase 1 works without it: python main.py --phase 1")
        print("Or use --demo for architecture overview.")
        sys.exit(1)

    # Initialize clients
    client = get_anthropic_client() if os.environ.get("ANTHROPIC_API_KEY") else None
    oa, s2, arxiv = get_search_clients()

    # Run
    if args.auto:
        log.info("Running auto-loop mode")
        os.environ["TARGET_SCORE"] = str(args.target_score)
        state = run_auto_loop(state, client, oa, s2, arxiv,
                              max_iterations=args.max_iterations)
    elif args.phase:
        log.info(f"Running Phase {args.phase}" + (" (resume)" if args.resume else ""))
        state = run_phase(args.phase, state, client, oa, s2, arxiv, resume=args.resume)
    else:
        log.info("Running full pipeline (9 phases)")
        state = run_full_pipeline(state, client, oa, s2, arxiv)

    show_status(state)
