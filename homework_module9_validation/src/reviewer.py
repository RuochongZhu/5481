"""Single-reviewer evaluation: persona + rubric + strict JSON parsing."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from .config import (
    CHECKLIST_KEY,
    PROMPT_DIR,
    REVIEWER_IDS,
    REVIEWER_PROMPT_DIR,
    REVIEWER_SCORES_DIR,
    REVIEW_MODEL,
    REVIEW_TEMPERATURE,
    SCORE_KEY,
)
from .data_variants import load_variant
from .llm_client import call_reviewer

log = logging.getLogger("hw_validator")

_SHARED_CONTEXT_PATH = PROMPT_DIR / "_shared_context.txt"


def _shared_context() -> str:
    return _SHARED_CONTEXT_PATH.read_text(encoding="utf-8").strip()


def _reviewer_prompt(reviewer_id: str) -> str:
    if reviewer_id not in REVIEWER_IDS:
        raise KeyError(f"unknown reviewer_id: {reviewer_id!r}; choose from {REVIEWER_IDS}")
    path = REVIEWER_PROMPT_DIR / f"{reviewer_id}.txt"
    return path.read_text(encoding="utf-8").strip()


def build_system_prompt(reviewer_id: str) -> str:
    return _shared_context() + "\n\n" + _reviewer_prompt(reviewer_id)


def build_user_message(digest: dict[str, Any], report_md: str) -> str:
    return (
        "SOURCE DIGEST (the data the report was supposed to summarize):\n"
        "```json\n"
        f"{json.dumps(digest, ensure_ascii=False, indent=2)}\n"
        "```\n\n"
        "GENERATED REPORT (markdown, evaluate this):\n"
        "```markdown\n"
        f"{report_md.rstrip()}\n"
        "```\n\n"
        "Now produce your evaluation as STRICT JSON per the schema."
    )


# ---------------------------------------------------------------------------
# Strict JSON parser with repair fallback (patterned after carpool_v4 scoring.py)
# ---------------------------------------------------------------------------

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json_block(text: str) -> str:
    """Pull the first JSON-shaped block out of LLM text."""
    m = _JSON_FENCE_RE.search(text)
    if m:
        return m.group(1)
    m = _JSON_OBJECT_RE.search(text)
    if m:
        return m.group(0)
    return text.strip()


def _coerce_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        return v.strip().lower() in {"true", "1", "yes", "y", "pass"}
    return False


def _repair_inner_quotes(text: str) -> str:
    """Repair the common LLM failure: `"A" — text "..." with stray `"` before delimiter.

    The LLM occasionally produces list elements like:
        "quote text" — explanation",
    which is two quoted spans glued by an em-dash with one stray close-quote.
    We detect: `"<A>" <em-dash|hyphen> <unquoted text> " <delimiter>` and merge
    into a single well-formed JSON string `"<A> — <unquoted text>" <delimiter>`.

    The separator MUST be an em-dash (—) or ASCII hyphen (-), NOT a colon, so this
    pattern cannot match a key-value pair like `"key": "value"`.
    """
    pattern = re.compile(
        r'"([^"\n]+?)"\s*([—\-])\s*([^"\n]+?)"(\s*[,\]\}])'
    )
    cur = text
    for _ in range(8):
        new = pattern.sub(r'"\1 \2 \3"\4', cur)
        if new == cur:
            break
        cur = new
    return cur


def _parse_reviewer_json(raw: str, reviewer_id: str) -> dict[str, Any]:
    """Parse JSON from raw LLM text; return a sanitized dict."""
    block = _extract_json_block(raw)
    try:
        data = json.loads(block)
    except json.JSONDecodeError:
        # Repair pass 1: drop trailing commas
        block_fixed = re.sub(r",\s*([\}\]])", r"\1", block)
        # Repair pass 2: merge accidental split-quote spans
        block_fixed = _repair_inner_quotes(block_fixed)
        try:
            data = json.loads(block_fixed)
        except json.JSONDecodeError as e:
            log.warning("JSON parse failed for %s: %s; raw[:200]=%r",
                        reviewer_id, e, raw[:200])
            return {
                "dimension": reviewer_id,
                "persona": "UNKNOWN",
                SCORE_KEY: 0.0,
                CHECKLIST_KEY: {},
                "checklist_count": 0,
                "evidence_quotes": [],
                "criticisms": [f"JSON parse failure: {e}"],
                "would_publish": "no",
                "_parse_status": "failed",
                "_raw": raw,
            }

    # Sanitize
    out: dict[str, Any] = dict(data)
    out["dimension"] = reviewer_id
    out.setdefault("persona", "UNKNOWN")

    # Score
    score = out.get(SCORE_KEY)
    try:
        score_f = float(score)
    except (TypeError, ValueError):
        score_f = 0.0
    score_f = max(0.0, min(10.0, score_f))
    out[SCORE_KEY] = score_f

    # Checklist
    checklist = out.get(CHECKLIST_KEY) or {}
    if not isinstance(checklist, dict):
        checklist = {}
    coerced = {k: _coerce_bool(v) for k, v in checklist.items()}
    out[CHECKLIST_KEY] = coerced
    out["checklist_count"] = int(sum(1 for v in coerced.values() if v))

    # Lists
    for key in ("evidence_quotes", "criticisms"):
        v = out.get(key, [])
        if isinstance(v, str):
            v = [v]
        elif not isinstance(v, list):
            v = []
        out[key] = v[:10]

    out.setdefault("would_publish", "conditional")
    out["_parse_status"] = "ok"
    return out


# ---------------------------------------------------------------------------
# Run a single reviewer
# ---------------------------------------------------------------------------

def run_reviewer(
    reviewer_id: str,
    *,
    digest: dict[str, Any],
    report_md: str,
) -> dict[str, Any]:
    system_prompt = build_system_prompt(reviewer_id)
    user_message = build_user_message(digest, report_md)
    response = call_reviewer(system_prompt=system_prompt, user_message=user_message)
    parsed = _parse_reviewer_json(response.text, reviewer_id)
    parsed["_model"] = response.model
    parsed["_temperature"] = REVIEW_TEMPERATURE
    parsed["_usage"] = response.usage
    return parsed


def score_path(prompt_id: str, variant_stem: str, reviewer_id: str) -> Path:
    return REVIEWER_SCORES_DIR / f"{prompt_id}__{variant_stem}__{reviewer_id}.json"


def review_report_file(
    reviewer_id: str,
    *,
    prompt_id: str,
    variant_id: int | str,
    report_path: Path,
    skip_if_exists: bool = True,
) -> Path:
    """Run one reviewer, save result JSON to disk, return its path."""
    digest = load_variant(variant_id)
    variant_stem = digest["meta"]["variant_id"]
    out_path = score_path(prompt_id, variant_stem, reviewer_id)
    if skip_if_exists and out_path.exists():
        log.info("skip review (exists): %s", out_path)
        return out_path

    report_md = report_path.read_text(encoding="utf-8")
    result = run_reviewer(reviewer_id, digest=digest, report_md=report_md)
    result["_prompt_id"] = prompt_id
    result["_variant_id"] = variant_stem
    result["_reviewer_id"] = reviewer_id

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    log.info("scored %s/%s by %s -> %.1f",
             prompt_id, variant_stem, reviewer_id, result[SCORE_KEY])
    return out_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python -m src.reviewer <reviewer_id> <prompt_id> <variant_index>")
        sys.exit(1)
    rev = sys.argv[1]
    pid = sys.argv[2]
    vid = int(sys.argv[3])
    from .report_generator import report_path as _rp
    digest = load_variant(vid)
    p = _rp(pid, digest["meta"]["variant_id"])
    if not p.exists():
        print(f"Report does not exist: {p}; generate it first.")
        sys.exit(1)
    out = review_report_file(rev, prompt_id=pid, variant_id=vid, report_path=p,
                              skip_if_exists=False)
    print(f"Wrote {out}")
    print(out.read_text())
