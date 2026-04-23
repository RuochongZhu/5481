"""Consensus API claim-check integration for Phase 5 reviewer context."""

from __future__ import annotations

import logging
import os

from .api_client import ConsensusClient
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")


def run_consensus_claim_checks(base_dir: str) -> dict:
    """Run lightweight claim verification searches and save a reviewer-ready summary."""
    api_key = os.environ.get("CONSENSUS_API_KEY", "").strip()
    analysis_dir = os.path.join(base_dir, "analysis")
    config_path = os.path.join(base_dir, "config", "consensus_claims.json")
    output_path = os.path.join(analysis_dir, "consensus_claim_checks.json")

    if not api_key:
        result = {
            "enabled": False,
            "provider": "consensus",
            "reason": "CONSENSUS_API_KEY not set",
            "claims": [],
        }
        atomic_write_json(output_path, result)
        return result

    claims_cfg = load_json(config_path) if os.path.exists(config_path) else {}
    claims = claims_cfg.get("claims", []) if isinstance(claims_cfg, dict) else []
    if not claims:
        result = {
            "enabled": False,
            "provider": "consensus",
            "reason": "No claims configured",
            "claims": [],
        }
        atomic_write_json(output_path, result)
        return result

    client = ConsensusClient(api_key=api_key)
    checks = []

    for item in claims:
        claim = (item.get("claim") or "").strip()
        if not claim:
            continue
        try:
            raw = client.quick_search(
                claim,
                limit=int(os.environ.get("CONSENSUS_SEARCH_LIMIT", "8")),
            )
            summary = client.summarize_quick_search(raw)
            checks.append({
                "id": item.get("id", ""),
                "purpose": item.get("purpose", ""),
                "claim": claim,
                "search_summary": summary,
                "raw": raw,
            })
            log.info(
                "Consensus check '%s': %s hits",
                item.get("id", claim[:40]),
                summary.get("result_count", 0),
            )
        except Exception as e:
            log.warning("Consensus check failed for '%s': %s", item.get("id", claim[:40]), e)
            checks.append({
                "id": item.get("id", ""),
                "purpose": item.get("purpose", ""),
                "claim": claim,
                "error": str(e),
            })

    result = {
        "enabled": True,
        "provider": "consensus",
        "claim_count": len(checks),
        "claims": checks,
    }
    atomic_write_json(output_path, result)
    return result
