"""Generate an earthquake situation report given a prompt id + variant id."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from .config import GEN_MODEL, PROMPT_DIR, REPORTS_DIR, GEN_TEMPERATURE
from .data_variants import load_variant
from .llm_client import call_generator

log = logging.getLogger("hw_validator")

_PROMPT_FILES = {
    "prompt_a": PROMPT_DIR / "prompt_a_minimal.txt",
    "prompt_b": PROMPT_DIR / "prompt_b_structured.txt",
    "prompt_c": PROMPT_DIR / "prompt_c_enhanced.txt",
}


def load_prompt(prompt_id: str) -> str:
    if prompt_id not in _PROMPT_FILES:
        raise KeyError(f"unknown prompt_id: {prompt_id!r}; choose from {list(_PROMPT_FILES)}")
    return _PROMPT_FILES[prompt_id].read_text(encoding="utf-8").strip()


def _format_user_message(digest: dict[str, Any]) -> str:
    """Format the user message: the data digest as JSON, identical for all prompts."""
    return f"DATA DIGEST (JSON):\n{json.dumps(digest, ensure_ascii=False, indent=2)}\n"


def report_path(prompt_id: str, variant_stem: str) -> Path:
    return REPORTS_DIR / prompt_id / f"{variant_stem}.md"


def generate_report(
    prompt_id: str,
    variant_id: int | str,
    *,
    skip_if_exists: bool = True,
) -> Path:
    """Generate one report. Returns the path to the saved markdown file."""
    digest = load_variant(variant_id)
    variant_stem = digest["meta"]["variant_id"]
    out_path = report_path(prompt_id, variant_stem)
    if skip_if_exists and out_path.exists():
        log.info("skip generation (exists): %s", out_path)
        return out_path

    system_prompt = load_prompt(prompt_id)
    user_message = _format_user_message(digest)

    response = call_generator(system_prompt=system_prompt, user_message=user_message)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(response.text + "\n", encoding="utf-8")

    # Also write a sidecar JSON with provenance
    sidecar = {
        "prompt_id": prompt_id,
        "variant_id": variant_stem,
        "model": response.model,
        "temperature": GEN_TEMPERATURE,
        "usage": response.usage,
    }
    out_path.with_suffix(".json").write_text(
        json.dumps(sidecar, indent=2), encoding="utf-8"
    )
    log.info("generated %s (model=%s, output_tokens=%d)",
             out_path, response.model, response.usage["output_tokens"])
    return out_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m src.report_generator <prompt_id> <variant_index>")
        sys.exit(1)
    p = generate_report(sys.argv[1], int(sys.argv[2]))
    print(f"Wrote: {p}")
    print(p.read_text())
