"""Phase 3.8: SPECTER2 Embedding Fetch — get 768-dim vectors from S2 API."""

import logging
import os
import numpy as np

from .api_client import S2Client
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")


def run_phase3_8(state: dict, state_path: str, base_dir: str,
                 s2: S2Client | None = None) -> dict:
    """Fetch SPECTER2 embeddings for all classified papers."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(proc_dir, exist_ok=True)

    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = load_json(classified_path)
    log.info(f"Phase 3.8: fetching SPECTER2 embeddings for {len(classified)} papers")

    if not is_step_complete(state, "3.8", "fetch_embeddings"):
        log.info("=== Phase 3.8.1: Fetch SPECTER2 embeddings ===")
        embedded_count = _fetch_specter_embeddings(classified, s2, proc_dir)
        state = complete_step(state, state_path, "3.8", "fetch_embeddings", {
            "papers_embedded": embedded_count,
        })
    else:
        log.info("SPECTER2 embeddings already fetched")

    return state


def _fetch_specter_embeddings(classified: list[dict], s2: S2Client | None,
                               proc_dir: str) -> int:
    """Fetch SPECTER2 768-dim embeddings via S2 API fields=embedding.specter_v2."""
    emb_path = os.path.join(proc_dir, "specter_embeddings.npy")
    meta_path = os.path.join(proc_dir, "specter_metadata.json")

    if s2 is None:
        log.warning("No S2 client — cannot fetch embeddings")
        return 0

    # Filter to papers with S2-compatible IDs (not OpenAlex URLs)
    s2_papers = [p for p in classified
                 if p.get("paperId")
                 and not p["paperId"].startswith("https://openalex.org/")
                 and not p["paperId"].startswith("arxiv:")]

    log.info(f"  {len(s2_papers)} papers have S2-compatible IDs")

    embeddings = []
    metadata = []
    failed = 0

    for i, p in enumerate(s2_papers):
        pid = p["paperId"]
        try:
            result = s2._get(
                f"https://api.semanticscholar.org/graph/v1/paper/{pid}",
                {"fields": "embedding.specter_v2"}
            )
            emb = result.get("embedding", {}).get("vector")
            if emb and len(emb) == 768:
                embeddings.append(emb)
                metadata.append({
                    "paperId": pid,
                    "title": p.get("title", "")[:80],
                    "year": p.get("year", 0),
                    "category": p.get("primary_category", "X"),
                    "citationCount": p.get("citationCount", 0),
                })
            else:
                failed += 1
        except Exception as e:
            failed += 1
            if (i + 1) % 50 == 0:
                log.warning(f"  Failed {pid}: {e}")

        if (i + 1) % 20 == 0:
            log.info(f"  Fetched {i+1}/{len(s2_papers)} ({len(embeddings)} ok, {failed} failed)")

    if embeddings:
        arr = np.array(embeddings, dtype=np.float32)
        np.save(emb_path, arr)
        atomic_write_json(meta_path, metadata)
        log.info(f"SPECTER2 embeddings: {arr.shape} saved to {emb_path}")
    else:
        log.warning("No embeddings fetched")

    return len(embeddings)
