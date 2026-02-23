#!/usr/bin/env python3
"""
SYSEN 5381 Lab: AI-Powered Data Reporter (Earthquake API)

Pipeline:
1) Query this project's earthquake API (Flask endpoint -> USGS provider)
2) Process/aggregate results into a compact JSON digest
3) Send digest to a local AI model (Ollama) to generate a report
4) Write reports + artifacts to disk for submission

Run:
  1) Start the local API server:
       python3 -m app.main
  2) In another terminal, run:
       python3 lab_ai_reporter.py

Env:
  - EARTHQUAKE_API_URL (optional, default: http://127.0.0.1:8000/api/v1/earthquakes)
  - OLLAMA_HOST (optional, default: http://127.0.0.1:11434)
  - OLLAMA_MODEL (optional, default: llama3.2:1b)
  - REPORT_OUTPUT_DIR (optional, default: reports)
"""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

API_URL = os.getenv("EARTHQUAKE_API_URL", "http://127.0.0.1:8000/api/v1/earthquakes")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
OUTPUT_DIR = Path(os.getenv("REPORT_OUTPUT_DIR", "reports"))

# Prompt iteration artifacts (so you can screenshot the final output and show iteration)
PROMPT_V1 = """You are a data reporter.
Given earthquake summary data, write a short plain-language summary in 6 bullet points.
Focus on: event count, magnitude range, high-risk signals, and what to monitor next.
"""

PROMPT_V2 = """You are an earthquake desk reporter writing for non-technical readers.
Return markdown with these sections:
1) Executive Summary (2-3 sentences)
2) Key Observations (4 bullets)
3) Risk Watch (3 bullets)
4) Data Caveat (1 sentence)
Keep it concise and actionable.
"""

PROMPT_FINAL = """You are an AI seismic reporter.
Use ONLY the provided data. Do not invent facts.
Write concise markdown in this exact structure:
# Earthquake Situation Report
## Executive Summary
(2-3 sentences)
## Top Signals
(4 bullet points)
## Risk Watch (Next 7 Days)
(3 bullet points)
## Data Caveats
(2 bullet points)
## Recommended Monitoring Actions
(numbered list of 3 items)
"""


def fetch_project_earthquake_data(*, days: int = 30, min_magnitude: float = 4.0, limit: int = 150) -> dict[str, Any]:
    """Call the existing local API endpoint from this project."""
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days)

    params = {
        "provider": "usgs",
        "starttime": start_date.isoformat(),
        "endtime": end_date.isoformat(),
        "minmagnitude": min_magnitude,
        "limit": limit,
        "orderby": "time",
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if "events" not in payload:
        raise ValueError("API payload missing 'events'. Start server with: python3 -m app.main")

    return payload


def _parse_iso_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def build_data_digest(payload: dict[str, Any], *, sample_size: int = 30) -> dict[str, Any]:
    """Reduce data size and add useful aggregates for AI prompting."""
    events = payload.get("events", [])
    magnitudes = [e.get("magnitude") for e in events if isinstance(e.get("magnitude"), (int, float))]

    region_counts: Counter[str] = Counter()
    daily_counts: Counter[str] = Counter()

    for event in events:
        place = event.get("place") or "Unknown"
        # A simple heuristic: keep the part after " of " as a region label.
        region = place.split(" of ")[-1].strip()
        region_counts[region] += 1

        dt = _parse_iso_utc(event.get("time"))
        if dt:
            daily_counts[dt.date().isoformat()] += 1

    simplified_events: list[dict[str, Any]] = []
    for event in events[:sample_size]:
        simplified_events.append(
            {
                "time": event.get("time"),
                "magnitude": event.get("magnitude"),
                "place": event.get("place"),
                "depth_km": event.get("depth_km"),
                "tsunami": event.get("tsunami"),
            }
        )

    return {
        "meta": payload.get("meta", {}),
        "summary": {
            "event_count": len(events),
            "max_magnitude": max(magnitudes) if magnitudes else None,
            "min_magnitude": min(magnitudes) if magnitudes else None,
            "avg_magnitude": round(sum(magnitudes) / len(magnitudes), 2) if magnitudes else None,
            "top_regions": region_counts.most_common(5),
            "daily_counts": dict(sorted(daily_counts.items())),
        },
        "sample_events": simplified_events,
    }


def make_prompt(instruction: str, digest: dict[str, Any]) -> str:
    return f"""{instruction}

DATA (JSON):
{json.dumps(digest, ensure_ascii=False, indent=2)}
"""


def query_ollama(prompt: str) -> str:
    # Ollama local API: https://github.com/ollama/ollama/blob/main/docs/api.md
    url = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
    body = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(url, json=body, timeout=120)
    response.raise_for_status()
    payload = response.json()
    text = payload.get("response", "")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Ollama returned an empty response.")
    return text.strip()


def query_llm(prompt: str) -> str:
    """Use local Ollama for fully local lab execution."""
    return query_ollama(prompt)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_pipeline() -> None:
    payload = fetch_project_earthquake_data()
    digest = build_data_digest(payload)

    _write_text(OUTPUT_DIR / "earthquake_data_digest.json", json.dumps(digest, ensure_ascii=False, indent=2))

    prompts = {
        "prompt_v1": make_prompt(PROMPT_V1, digest),
        "prompt_v2": make_prompt(PROMPT_V2, digest),
        "prompt_final": make_prompt(PROMPT_FINAL, digest),
    }

    for name, prompt in prompts.items():
        report_md = query_llm(prompt)
        _write_text(OUTPUT_DIR / f"{name}_report.md", report_md)

    description = (
        "I queried the project's USGS earthquake API, aggregated results into a compact JSON digest, and then "
        "used local Ollama to generate a markdown situation report. I iterated from a simple 6-bullet prompt to a "
        "fixed-section report prompt to improve structure and actionability, and saved each iteration plus the "
        "final report to files for submission screenshots."
    )
    _write_text(OUTPUT_DIR / "submission_description.txt", description)

    print("✅ Done. Generated files:")
    for path in sorted(OUTPUT_DIR.glob("*")):
        print(f"- {path}")


if __name__ == "__main__":
    run_pipeline()
