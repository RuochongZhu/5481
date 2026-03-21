#!/usr/bin/env python3
"""
Codex Parallel Cross-Validation
================================
Spawns local `codex exec` processes for independent cross-validation.
Uses codex CLI config (~/.codex/config.toml) by default (ppchat proxy).
Falls back to direct OpenAI if codex fails — reads OPENAI_API_KEY from .env.

Usage:
  python run_codex_parallel.py                 # Run all 6 tasks
  python run_codex_parallel.py --tasks 1,3     # Run specific tasks
  python run_codex_parallel.py --list          # List tasks
  python run_codex_parallel.py --max-parallel 2
"""

import argparse
import json
import os
import re
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "processed"
ANALYSIS_DIR = BASE_DIR / "analysis"
OUTPUT_DIR = BASE_DIR / "output" / "codex_validation"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _extract_json(text: str):
    match = re.search(r'```(?:json)?\s*\n?(.*?)```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    for ch in ('[', '{'):
        idx = text.find(ch)
        if idx >= 0:
            try:
                return json.loads(text[idx:])
            except json.JSONDecodeError:
                pass
    return None


# ---------------------------------------------------------------------------
# Fallback: direct OpenAI API call when codex CLI is down
# ---------------------------------------------------------------------------

def _call_openai_direct(prompt: str) -> str:
    """Call OpenAI API directly using OPENAI_API_KEY from env."""
    import urllib.request
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return '{"error": "OPENAI_API_KEY not set, cannot fallback"}'

    body = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Task runner
# ---------------------------------------------------------------------------

def run_codex_task(task: dict, output_dir: Path) -> dict:
    """Run via codex CLI. If codex fails, fallback to direct OpenAI."""
    task_id, name, prompt = task["id"], task["name"], task["prompt"]
    output_file = output_dir / f"task_{task_id}_{name}.json"
    print(f"  [{task_id}] Starting: {name}")
    start = time.time()

    stdout, backend = "", "codex"
    try:
        result = subprocess.run(
            ["codex", "exec", "--sandbox", "danger-full-access", prompt],
            capture_output=True, text=True, timeout=300, cwd=str(BASE_DIR),
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or not stdout:
            raise RuntimeError(f"codex returned {result.returncode}")
    except Exception as e:
        print(f"  [{task_id}] Codex failed ({e}), falling back to OpenAI direct")
        backend = "openai_direct"
        try:
            stdout = _call_openai_direct(prompt)
        except Exception as e2:
            stdout = json.dumps({"error": str(e2)})
            backend = "failed"

    elapsed = round(time.time() - start, 1)
    parsed = _extract_json(stdout)
    output_data = {
        "task_id": task_id, "name": name, "backend": backend,
        "status": "success" if parsed else "parse_error",
        "elapsed_sec": elapsed,
        "output": parsed if parsed else stdout[:2000],
    }
    output_file.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [{task_id}] Done: {name} ({elapsed}s, {backend})")
    return output_data


# ---------------------------------------------------------------------------
# Task definitions
# ---------------------------------------------------------------------------

def build_tasks() -> list[dict]:
    classified = _load_json(DATA_DIR / "classified.json")
    gaps = _load_json(ANALYSIS_DIR / "gaps_ranked.json")
    metrics = _load_json(ANALYSIS_DIR / "graph_metrics.json")
    matrix = _load_json(ANALYSIS_DIR / "intersection_matrix.json")

    cat_dist = {}
    for p in (classified if isinstance(classified, list) else []):
        cat_dist[p.get("primary_category", "X")] = cat_dist.get(p.get("primary_category", "X"), 0) + 1

    top20 = sorted((classified if isinstance(classified, list) else []),
                    key=lambda p: p.get("citationCount", 0), reverse=True)[:20]
    top20_str = "\n".join(
        f"- [{p.get('year')}] {p.get('title','?')[:80]} (cat={p.get('primary_category')}, cites={p.get('citationCount',0)})"
        for p in top20)

    gaps_list = gaps.get("gaps", []) if isinstance(gaps, dict) else []
    gaps_str = "\n".join(
        f"#{g['rank']}: {g.get('research_question', g.get('description',''))[:120]} "
        f"(cats={g.get('bridges_categories')}, score={g.get('score')}, campusgo={g.get('campusgo_relevance')})"
        for g in gaps_list)

    return [
        {"id": 1, "name": "classification_audit",
         "description": "Audit top 20 papers for misclassifications",
         "prompt": f"You are a research methodology auditor. Review these paper classifications (A-G taxonomy).\n\nCategories: {json.dumps(cat_dist)}\n\nTop 20 papers:\n{top20_str}\n\nFor each, verify the primary_category. Output JSON array of corrections or [{{'status':'all_correct'}}]."},

        {"id": 2, "name": "gap_novelty_check",
         "description": "Verify gaps are genuinely novel",
         "prompt": f"You are a research gap validator. Assess novelty of each gap.\n\nGaps:\n{gaps_str}\n\nFor each: rate 'confirmed_novel', 'partially_addressed', or 'already_exists'. Name closest existing work if any.\n\nOutput JSON: [{{'rank':1, 'novelty_verdict':'...', 'closest_work':'...', 'reasoning':'...'}}]"},

        {"id": 3, "name": "campusgo_honesty_check",
         "description": "Independent CampusGo relevance assessment",
         "prompt": f"You are an independent reviewer. CampusGo is a campus activity web/mobile app (Vue3+Node+Supabase) with GPS check-in, QR codes, star ratings, chat, 7 activity categories. It is NOT an IoT platform, NOT federated learning, NOT edge computing.\n\nGaps:\n{gaps_str}\n\nRate each: 'genuine' (features directly relate), 'stretch' (needs reframing), 'forced' (dishonest).\n\nOutput JSON: [{{'rank':1, 'campusgo_assessment':'forced', 'reason':'...'}}]"},

        {"id": 4, "name": "methodology_feasibility",
         "description": "PhD feasibility of top 3 proposals",
         "prompt": f"You are a PhD committee member. Evaluate top 3 gaps for PhD feasibility.\n\nGaps:\n{gaps_str}\n\nFor top 3: timeline, resources, datasets, risks, publication venues.\n\nOutput JSON: [{{'rank':1, 'phd_feasible':true, 'timeline':'3-4y', 'biggest_risk':'...', 'venues':['...']}}]"},

        {"id": 5, "name": "intersection_validation",
         "description": "Validate category intersection matrix",
         "prompt": f"You are a bibliometric analyst. Validate this intersection matrix.\n\nMatrix: {json.dumps(matrix)}\nMetrics: {json.dumps(metrics)}\nCategories: {json.dumps(cat_dist)}\n\nAre sparse pairs genuinely underexplored or corpus artifacts? Which pairs should have more connections?\n\nOutput JSON: {{'sparse_valid':[...], 'expected_connections':[...], 'recommendations':'...'}}"},

        {"id": 6, "name": "alternative_gaps",
         "description": "Generate gaps the pipeline missed",
         "prompt": f"You are a senior AI researcher (data quality / model collapse). Current gaps:\n{gaps_str}\n\nCategories: {json.dumps(cat_dist)}\n\nGenerate 5 ALTERNATIVE gaps NOT in the list. Each must bridge 2+ categories and be a specific PhD question. Assess CampusGo relevance honestly (it's a campus activity web app with GPS/QR/ratings/chat).\n\nOutput JSON: [{{'rank':1, 'research_question':'...', 'bridges':['A','D'], 'campusgo':'genuine|stretch|forced', 'reason':'...'}}]"},
    ]


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge_results(output_dir: Path) -> dict:
    results = {}
    for f in sorted(output_dir.glob("task_*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        results[data["name"]] = data

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "total_tasks": len(results),
        "successful": sum(1 for r in results.values() if r.get("status") == "success"),
        "tasks": results,
    }
    (output_dir / "validation_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport: {output_dir / 'validation_report.json'}")
    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Codex Cross-Validation")
    parser.add_argument("--tasks", type=str, help="Task IDs (e.g. 1,3,5)")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--max-parallel", type=int, default=4)
    parser.add_argument("--merge-only", action="store_true")
    args = parser.parse_args()

    from dotenv import load_dotenv
    for p in [BASE_DIR.parent / ".env", BASE_DIR / ".env"]:
        if p.exists():
            load_dotenv(p, override=True)

    tasks = build_tasks()

    if args.list:
        for t in tasks:
            print(f"  [{t['id']}] {t['name']}: {t['description']}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.merge_only:
        merge_results(OUTPUT_DIR)
        return

    if args.tasks:
        ids = {int(x) for x in args.tasks.split(",")}
        tasks = [t for t in tasks if t["id"] in ids]

    print(f"\n{len(tasks)} tasks, max {args.max_parallel} parallel\n")

    with ProcessPoolExecutor(max_workers=args.max_parallel) as pool:
        futures = {pool.submit(run_codex_task, t, OUTPUT_DIR): t for t in tasks}
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                t = futures[f]
                print(f"  [{t['id']}] Exception: {e}")

    report = merge_results(OUTPUT_DIR)
    print(f"\nDone: {report['successful']}/{report['total_tasks']} successful")


if __name__ == "__main__":
    main()
