"""STORM-style 3-round debate for contradiction verification.

Uses Claude fast for debaters and GPT-5.4 xhigh for the judge.
No external framework — just 3 API calls per contradiction candidate.
"""

from __future__ import annotations

import logging
from .api_client import BRAIN_FAST, BRAIN_GPT_XHIGH, agent_run

log = logging.getLogger("research_agent")


def storm_debate(client, paper_a: dict, paper_b: dict) -> dict:
    """3-round debate to determine if two papers genuinely contradict.

    Round 1: Author A defends their finding against Paper B
    Round 2: Author B attacks Paper A's finding
    Round 3: Neutral judge decides if this is a genuine contradiction

    Returns: {"is_genuine": bool, "verdict": str, "strength": str, "rounds": [...]}
    """
    finding_a = paper_a.get("key_claim", paper_a.get("one_sentence_contribution", ""))
    finding_b = paper_b.get("key_claim", paper_b.get("one_sentence_contribution", ""))
    title_a = paper_a.get("title", "Paper A")[:80]
    title_b = paper_b.get("title", "Paper B")[:80]
    method_a = paper_a.get("methodology", "not specified")
    method_b = paper_b.get("methodology", "not specified")

    rounds = []

    # Round 1: Author A defends
    log.debug(f"  Debate R1: {title_a[:40]} defends")
    try:
        r1 = agent_run(
            client,
            role=(
                f"You are the author of '{title_a}'. "
                "Defend your finding against the opposing paper's claim. "
                "Be specific, cite your methodology, and explain why your result is more reliable. "
                "Keep response under 200 words."
            ),
            task=(
                f"Your finding: {finding_a}\n"
                f"Your methodology: {method_a}\n\n"
                f"Opposing paper '{title_b}' claims: {finding_b}\n"
                f"Their methodology: {method_b}\n\n"
                f"Defend your position."
            ),
            model=BRAIN_FAST,
            max_tokens=512,
        )
        rounds.append({"round": 1, "role": "defender_a", "text": r1})
    except Exception as e:
        log.warning(f"  Debate R1 failed: {e}")
        rounds.append({"round": 1, "role": "defender_a", "error": str(e)})
        r1 = "Defense unavailable."

    # Round 2: Author B attacks
    log.debug(f"  Debate R2: {title_b[:40]} attacks")
    try:
        r2 = agent_run(
            client,
            role=(
                f"You are the author of '{title_b}'. "
                "Attack the opposing paper's finding. Point out methodological weaknesses, "
                "scope limitations, or flawed assumptions. "
                "Keep response under 200 words."
            ),
            task=(
                f"Your finding: {finding_b}\n"
                f"Your methodology: {method_b}\n\n"
                f"Opposing paper '{title_a}' claims: {finding_a}\n"
                f"Their defense: {r1[:500]}\n\n"
                f"Attack their position."
            ),
            model=BRAIN_FAST,
            max_tokens=512,
        )
        rounds.append({"round": 2, "role": "attacker_b", "text": r2})
    except Exception as e:
        log.warning(f"  Debate R2 failed: {e}")
        rounds.append({"round": 2, "role": "attacker_b", "error": str(e)})
        r2 = "Attack unavailable."

    # Round 3: Neutral judge (GPT-5.4 xhigh)
    log.debug("  Debate R3: Judge decides")
    try:
        r3 = agent_run(
            client,
            role=(
                "You are a neutral senior reviewer judging a debate between two papers. "
                "Decide: is this a GENUINE contradiction, a SCOPE disagreement (both correct "
                "under different conditions), or NOT a real contradiction? "
                "Output exactly one line: GENUINE | SCOPE | NOT_REAL "
                "followed by a one-sentence explanation. Then rate strength: strong | moderate | weak."
            ),
            task=(
                f"Paper A: '{title_a}'\n"
                f"Claim: {finding_a}\n"
                f"Defense: {r1[:400]}\n\n"
                f"Paper B: '{title_b}'\n"
                f"Claim: {finding_b}\n"
                f"Attack: {r2[:400]}\n\n"
                f"Is this a genuine contradiction? Rate its strength."
            ),
            model=BRAIN_GPT_XHIGH,
            max_tokens=256,
        )
        rounds.append({"round": 3, "role": "judge", "text": r3})
    except Exception as e:
        log.warning(f"  Debate R3 failed: {e}")
        rounds.append({"round": 3, "role": "judge", "error": str(e)})
        r3 = "GENUINE moderate — judge unavailable, defaulting to genuine"

    # Parse judge verdict
    verdict_text = r3.strip().upper()
    is_genuine = "GENUINE" in verdict_text and "NOT_REAL" not in verdict_text
    is_scope = "SCOPE" in verdict_text

    if "STRONG" in verdict_text:
        strength = "strong"
    elif "WEAK" in verdict_text:
        strength = "weak"
    else:
        strength = "moderate"

    if is_scope:
        verdict_type = "scope_disagreement"
    elif is_genuine:
        verdict_type = "genuine_contradiction"
    else:
        verdict_type = "not_real"

    return {
        "paper_a": paper_a.get("paperId", ""),
        "paper_b": paper_b.get("paperId", ""),
        "is_genuine": is_genuine or is_scope,
        "verdict_type": verdict_type,
        "strength": strength,
        "judge_text": r3[:300],
        "rounds": rounds,
    }


def batch_debate(client, candidate_pairs: list[tuple[dict, dict]],
                 max_debates: int = 20) -> list[dict]:
    """Run STORM debates on a batch of candidate contradiction pairs.

    Returns only genuine/scope contradictions (filters out not_real).
    """
    results = []
    total = min(len(candidate_pairs), max_debates)
    log.info(f"  Running {total} STORM debates")

    for i, (pa, pb) in enumerate(candidate_pairs[:max_debates]):
        log.info(f"  Debate {i+1}/{total}: "
                 f"{pa.get('title', '?')[:30]} vs {pb.get('title', '?')[:30]}")
        result = storm_debate(client, pa, pb)
        if result["is_genuine"]:
            results.append(result)
            log.info(f"    → {result['verdict_type']} ({result['strength']})")
        else:
            log.info(f"    → not_real, discarded")

    log.info(f"  Debates complete: {len(results)}/{total} genuine contradictions")
    return results
