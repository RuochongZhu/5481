"""Phase 4: Evidence Inventory & Final Report Generation."""

from __future__ import annotations

import json
import logging
import os
import re

from .api_client import agent_run, BRAIN_PHASE4_EVIDENCE, S2Client
from .phase_contracts import ensure_evidence_inventory_valid
from .prompts import TOPIC_SCORER
from .state_manager import complete_step, is_step_complete
from .utils import atomic_write_json, load_json

log = logging.getLogger("research_agent")

# Import centralized beat definitions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.beat_definitions import BEAT_CATEGORIES as _BEAT_CATS, BEAT_NAMES as _BEAT_NAMES, NUM_BEATS

BEAT_CATEGORY_HINTS = _BEAT_CATS

BEAT_TITLES = _BEAT_NAMES


def run_phase4(state: dict, state_path: str, base_dir: str, client,
               s2: S2Client | None = None) -> dict:
    """Orchestrate Phase 4: evidence inventory + final report."""
    analysis_dir = os.path.join(base_dir, "analysis")
    output_dir = os.path.join(base_dir, "output")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)

    evidence_path = os.path.join(analysis_dir, "gaps_ranked.json")
    narrative_path = os.path.join(analysis_dir, "narrative_chains.json")
    classified_path = os.path.join(proc_dir, "classified.json")

    if not os.path.exists(evidence_path):
        log.error("gaps_ranked.json not found. Run Phase 3 first.")
        return state

    evidence = load_json(evidence_path)
    narrative_chains = load_json(narrative_path) if os.path.exists(narrative_path) else []
    classified = load_json(classified_path) if os.path.exists(classified_path) else []

    # Step 1: Generate evidence inventory per beat
    if not is_step_complete(state, 4, "score_gaps"):
        log.info("=== Phase 4.1: Evidence inventory ===")
        inventory = _build_evidence_inventory(client, evidence, classified, narrative_chains)
        atomic_write_json(os.path.join(analysis_dir, "evidence_inventory.json"), inventory)
        ensure_evidence_inventory_valid(inventory)
        state = complete_step(state, state_path, 4, "score_gaps")
    else:
        inventory = load_json(os.path.join(analysis_dir, "evidence_inventory.json"))
        ensure_evidence_inventory_valid(inventory)

    # Step 2: Skip advisor alignment (not relevant for evidence chain)
    if not is_step_complete(state, 4, "advisor_alignment"):
        log.info("=== Phase 4.2: Skipped (not applicable) ===")
        state = complete_step(state, state_path, 4, "advisor_alignment")

    # Step 3: Skip thesis generation (thesis is predetermined)
    if not is_step_complete(state, 4, "thesis_generation"):
        log.info("=== Phase 4.3: Skipped (thesis predetermined) ===")
        state = complete_step(state, state_path, 4, "thesis_generation")

    # Step 4: Final report
    if not is_step_complete(state, 4, "final_report"):
        log.info("=== Phase 4.4: Generate final reports ===")
        _generate_evidence_report(base_dir, evidence, inventory, classified, output_dir)
        state = complete_step(state, state_path, 4, "final_report")

    return state


def _build_evidence_inventory(client, evidence: dict, classified: list[dict],
                              narrative_chains: list[dict] | None = None) -> dict:
    """Use TOPIC_SCORER agent to generate structured evidence inventory per beat."""
    beats = evidence.get("beats", [])
    beats_summary = json.dumps(beats, indent=2, ensure_ascii=False)[:3000] if beats else "No beat analysis available"

    # Build per-category paper lists for the agent
    by_cat = {}
    for p in classified:
        cat = p.get("primary_category", "X")
        if cat == "X":
            continue
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append({
            "paperId": p.get("paperId", ""),
            "title": p.get("title", "")[:80],
            "year": p.get("year", 0),
            "citationCount": p.get("citationCount", 0),
            "one_sentence_contribution": p.get("one_sentence_contribution", "")[:100],
        })

    # Sort each category by citations, take top 10
    cat_summaries = {}
    for cat, papers in by_cat.items():
        papers.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
        cat_summaries[cat] = papers[:10]

    task = (
        f"Generate a structured evidence inventory for a 6-beat research paper.\n\n"
        f"## Evidence Sufficiency Analysis\n{beats_summary}\n\n"
        f"## Top Papers by Category\n{json.dumps(cat_summaries, indent=2, ensure_ascii=False)[:4000]}\n\n"
        f"For each beat, identify the 5-8 most important papers and the logical chain connecting them."
    )

    try:
        raw = agent_run(client, role=TOPIC_SCORER, task=task, model=BRAIN_PHASE4_EVIDENCE, max_tokens=8192)
        result = _parse_json_object(raw)
        result = _ground_evidence_inventory(result, evidence, classified)
        ensure_evidence_inventory_valid(result)
        log.info("Evidence inventory generated")
        return result
    except Exception as first_error:
        log.warning(f"Evidence inventory retrying with compact context: {first_error}")
        retry_task = _compact_inventory_task(beats, cat_summaries)
        retry_role = (
            TOPIC_SCORER
            + "\nReturn minified JSON only. No prose, no markdown, no trailing commentary. "
              "The JSON must contain exactly 6 evidence_inventory entries and a non-empty suggested_paper_outline object."
        )
        try:
            raw = agent_run(client, role=retry_role, task=retry_task, model=BRAIN_PHASE4_EVIDENCE, max_tokens=4096)
            result = _parse_json_object(raw)
            result = _ground_evidence_inventory(result, evidence, classified)
            ensure_evidence_inventory_valid(result)
            log.info("Evidence inventory generated after compact retry")
            return result
        except Exception as second_error:
            log.error(f"Evidence inventory failed after retry: {second_error}")
            return _fallback_evidence_inventory(evidence, classified, second_error, narrative_chains)


def _compact_inventory_task(beats: list[dict], cat_summaries: dict) -> str:
    """Build a shorter retry prompt that still preserves beat/category coverage."""
    slim_categories = {
        cat: [
            {
                "paperId": p.get("paperId", ""),
                "title": p.get("title", "")[:60],
                "year": p.get("year", 0),
                "citationCount": p.get("citationCount", 0),
            }
            for p in papers[:5]
        ]
        for cat, papers in cat_summaries.items()
    }
    return (
        "Generate a contract-compliant evidence inventory for exactly 6 beats.\n"
        f"Beat analysis: {json.dumps(beats, ensure_ascii=False)[:1500]}\n"
        f"Top papers by category: {json.dumps(slim_categories, ensure_ascii=False)[:2500]}\n"
        "Each beat must include non-empty core_papers and a concise narrative."
    )


def _fallback_evidence_inventory(evidence: dict, classified: list[dict], error: Exception,
                                 narrative_chains: list[dict] | None = None) -> dict:
    """Return a conservative, contract-compliant inventory from classified metadata."""
    by_id = {paper.get("paperId", ""): paper for paper in classified if paper.get("paperId")}
    by_cat: dict[str, list[dict]] = {}
    for paper in classified:
        cat = paper.get("primary_category", "X")
        if cat == "X":
            continue
        by_cat.setdefault(cat, []).append(paper)
    for papers in by_cat.values():
        papers.sort(key=lambda x: x.get("citationCount", 0) or 0, reverse=True)

    evidence_beats = {
        int(b.get("beat", idx)): b
        for idx, b in enumerate(evidence.get("beats", []), start=1)
        if isinstance(b, dict) and str(b.get("beat", idx)).isdigit()
    }
    chain_by_beat = {
        int(chain.get("beat", 0)): chain
        for chain in (narrative_chains or [])
        if isinstance(chain, dict) and str(chain.get("beat", 0)).isdigit()
    }

    inventory = []
    for beat in range(1, NUM_BEATS + 1):
        selected = []
        seen = set()
        chain = chain_by_beat.get(beat, {})

        for item in chain.get("spine", []) or []:
            if not isinstance(item, dict):
                continue
            pid = item.get("paperId", "")
            paper = by_id.get(pid)
            if not paper or pid in seen:
                continue
            selected.append({
                "paperId": pid,
                "title": paper.get("title", ""),
                "role": item.get("role_in_narrative") or f"Structured spine paper for Beat {beat}",
                "key_finding": str(
                    paper.get("key_claim")
                    or paper.get("one_sentence_contribution")
                    or paper.get("abstract", "")[:120]
                    or "Narrative-driven fallback candidate."
                )[:180],
                "citation_note": _citation_note(paper),
            })
            seen.add(pid)
            if len(selected) >= 5:
                break

        for item in chain.get("supporting", []) or []:
            if len(selected) >= 5:
                break
            if not isinstance(item, dict):
                continue
            pid = item.get("paperId", "")
            paper = by_id.get(pid)
            if not paper or pid in seen:
                continue
            selected.append({
                "paperId": pid,
                "title": paper.get("title", ""),
                "role": item.get("role") or f"Structured supporting paper for Beat {beat}",
                "key_finding": str(
                    paper.get("key_claim")
                    or paper.get("one_sentence_contribution")
                    or paper.get("abstract", "")[:120]
                    or "Narrative-driven fallback candidate."
                )[:180],
                "citation_note": _citation_note(paper),
            })
            seen.add(pid)

        for cat in BEAT_CATEGORY_HINTS.get(beat, []):
            for paper in by_cat.get(cat, []):
                pid = paper.get("paperId", "")
                if pid in seen:
                    continue
                selected.append(_paper_inventory_item(paper, beat, cat))
                seen.add(pid)
                if len(selected) >= 5:
                    break
            if len(selected) >= 5:
                break

        if not selected:
            selected.append({
                "paperId": f"fallback:beat-{beat}:no-paper",
                "title": "No candidate paper found",
                "role": f"Fallback placeholder for Beat {beat}",
                "key_finding": "No classified paper was available for this beat; rerun retrieval before using this beat in prose.",
                "citation_note": "No usable citation",
            })

        beat_info = evidence_beats.get(beat, {})
        remaining_gaps = [
            f"Fallback generated after evidence inventory parse failure: {error}",
        ]
        weakness = beat_info.get("weakness")
        if weakness:
            remaining_gaps.append(str(weakness))

        inventory.append({
            "beat": beat,
            "title": beat_info.get("name") or BEAT_TITLES[beat],
            "core_papers": selected,
            "narrative": chain.get("writing_notes") or (
                "Conservative fallback inventory aligned to narrative chains and classified metadata. "
                "Use these papers as candidates, not as a polished evidence chain."
            ),
            "remaining_gaps": remaining_gaps,
        })

    outline = {
        f"section_{beat}_{BEAT_TITLES[beat].lower().replace(' ', '_')}": {
            "papers": len(inventory[beat - 1]["core_papers"]),
            "pages": "TBD",
            "note": "fallback inventory; revise after successful Phase 4 retry",
        }
        for beat in range(1, NUM_BEATS + 1)
    }
    return {
        "evidence_inventory": inventory,
        "suggested_paper_outline": outline,
        "fallback_warning": f"Evidence inventory retry failed: {error}",
    }


def _ground_evidence_inventory(result: dict, evidence: dict, classified: list[dict]) -> dict:
    """Replace hallucinated inventory entries with actual corpus-grounded papers."""
    if not isinstance(result, dict):
        return result

    inventory = result.get("evidence_inventory")
    if not isinstance(inventory, list):
        return result

    by_id = {p.get("paperId", ""): p for p in classified if p.get("paperId")}
    by_title = {
        _normalize_title(p.get("title", "")): p
        for p in classified
        if p.get("title")
    }
    by_cat: dict[str, list[dict]] = {}
    for paper in classified:
        cat = paper.get("primary_category", "X")
        if cat == "X":
            continue
        by_cat.setdefault(cat, []).append(paper)
    for papers in by_cat.values():
        papers.sort(key=lambda x: x.get("citationCount", 0) or 0, reverse=True)

    evidence_beats = {
        int(item.get("beat", idx)): item
        for idx, item in enumerate(evidence.get("beats", []), start=1)
        if isinstance(item, dict) and str(item.get("beat", idx)).isdigit()
    }

    grounded_inventory = []
    for beat_entry in inventory:
        if not isinstance(beat_entry, dict):
            continue
        beat = int(beat_entry.get("beat", 0) or 0)
        allowed_cats = list(BEAT_CATEGORY_HINTS.get(beat, []))
        grounded_core = []
        seen_ids = set()

        for item in beat_entry.get("core_papers", []) or []:
            if not isinstance(item, dict):
                continue
            paper = None
            pid = item.get("paperId", "")
            title = item.get("title", "")
            if pid in by_id:
                paper = by_id[pid]
            elif title:
                paper = by_title.get(_normalize_title(title))

            if not paper:
                continue

            paper_id = paper.get("paperId", "")
            if not paper_id or paper_id in seen_ids:
                continue

            grounded_core.append({
                "paperId": paper_id,
                "title": paper.get("title", title),
                "role": item.get("role") or f"Supports Beat {beat} via category {paper.get('primary_category', 'X')}",
                "key_finding": str(
                    item.get("key_finding")
                    or paper.get("key_claim")
                    or paper.get("one_sentence_contribution")
                    or paper.get("abstract", "")[:180]
                    or "Corpus-grounded candidate paper."
                )[:180],
                "citation_note": (
                    item.get("citation_note")
                    if item.get("citation_note") and "unknown" not in str(item.get("citation_note")).lower()
                    else _citation_note(paper)
                ),
            })
            seen_ids.add(paper_id)

        if len(grounded_core) < 5:
            for cat in allowed_cats:
                for paper in by_cat.get(cat, []):
                    paper_id = paper.get("paperId", "")
                    if not paper_id or paper_id in seen_ids:
                        continue
                    grounded_core.append(_paper_inventory_item(paper, beat, cat))
                    seen_ids.add(paper_id)
                    if len(grounded_core) >= 5:
                        break
                if len(grounded_core) >= 5:
                    break

        if not grounded_core:
            grounded_core.append({
                "paperId": f"fallback:beat-{beat}:no-paper",
                "title": "No candidate paper found",
                "role": f"Fallback placeholder for Beat {beat}",
                "key_finding": "No classified paper was available for this beat; rerun retrieval before using this beat in prose.",
                "citation_note": "No usable citation",
            })

        beat_info = evidence_beats.get(beat, {})
        grounded_inventory.append({
            "beat": beat,
            "title": beat_entry.get("title") or beat_info.get("name") or BEAT_TITLES.get(beat, f"Beat {beat}"),
            "argument_line": beat_entry.get("argument_line"),
            "core_papers": grounded_core[:8],
            "narrative": beat_entry.get("narrative") or (
                "Grounded evidence inventory synthesized from actual corpus papers."
            ),
            "remaining_gaps": beat_entry.get("remaining_gaps", []),
        })

    result["evidence_inventory"] = grounded_inventory
    return result


def _normalize_title(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())


def _paper_inventory_item(paper: dict, beat: int, category: str) -> dict:
    contribution = (
        paper.get("key_claim")
        or paper.get("one_sentence_contribution")
        or paper.get("abstract", "")[:120]
        or "Use as a conservative candidate; verify before citing."
    )
    return {
        "paperId": paper.get("paperId", ""),
        "title": paper.get("title", ""),
        "role": f"Supports Beat {beat} via category {category}",
        "key_finding": str(contribution)[:180],
        "citation_note": _citation_note(paper),
    }


def _citation_note(paper: dict) -> str:
    authors = paper.get("authors") or []
    if authors and isinstance(authors[0], dict):
        first_author = authors[0].get("name", "")
    elif authors:
        first_author = str(authors[0])
    else:
        first_author = "Unknown author"
    year = paper.get("year", "?")
    return f"{first_author} et al. {year}"


def _parse_json_object(raw: str) -> dict:
    """Parse model output with small JSON repair attempts."""
    text = raw.strip()
    match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    first_brace = min(
        [idx for idx in (text.find("{"), text.find("[")) if idx != -1],
        default=-1,
    )
    if first_brace != -1:
        text = text[first_brace:]

    candidates = []
    for candidate in (text, _extract_balanced_json(text), _trim_to_last_json_closer(text)):
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    last_error = None
    for candidate in candidates:
        for repaired in (candidate, _close_unbalanced_json(candidate)):
            if not repaired:
                continue
            try:
                parsed = json.loads(repaired)
                if isinstance(parsed, dict):
                    return parsed
            except Exception as e:
                last_error = e

    raise last_error or ValueError("Model output did not contain a valid JSON object")


def _extract_balanced_json(text: str) -> str:
    if not text:
        return ""
    start = next((i for i, ch in enumerate(text) if ch in "[{"), -1)
    if start == -1:
        return ""

    stack = []
    in_string = False
    escape = False
    for i, ch in enumerate(text[start:], start):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}":
            if not stack or ch != stack[-1]:
                return ""
            stack.pop()
            if not stack:
                return text[start:i + 1]
    return ""


def _trim_to_last_json_closer(text: str) -> str:
    last = max(text.rfind("}"), text.rfind("]"))
    return text[:last + 1] if last != -1 else ""


def _close_unbalanced_json(text: str) -> str:
    if not text:
        return ""

    stack = []
    in_string = False
    escape = False
    for ch in text:
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}":
            if stack and ch == stack[-1]:
                stack.pop()

    repaired = text
    if in_string:
        repaired += '"'
    if stack:
        repaired += "".join(reversed(stack))
    return repaired


def _generate_evidence_report(base_dir: str, evidence: dict, inventory: dict,
                               classified: list[dict], output_dir: str):
    """Write human-readable evidence reports."""

    # --- Report 1: Evidence Sufficiency ---
    lines = ["# Evidence Sufficiency Report\n"]
    lines.append("*Assessment of literature support for each beat of the paper*\n\n---\n")

    beats = evidence.get("beats", [])
    for b in beats:
        status_icon = {"strong": "🟢", "adequate": "🟡", "weak": "🟠", "critical_gap": "🔴"}.get(
            b.get("status", ""), "❓")
        lines.append(f"## Beat {b.get('beat', '?')}: {b.get('name', '')} {status_icon} {b.get('status', '')}\n")
        lines.append(f"Supporting papers: {b.get('supporting_papers', '?')}")
        if b.get("key_papers_present"):
            lines.append(f"Key papers present: {', '.join(b['key_papers_present'])}")
        if b.get("key_papers_missing"):
            lines.append(f"Key papers MISSING: {', '.join(b['key_papers_missing'])}")
        if b.get("weakness"):
            lines.append(f"Weakness: {b['weakness']}")
        if b.get("evidence_chain"):
            lines.append(f"\nEvidence chain:")
            for step in b["evidence_chain"]:
                lines.append(f"  → {step}")
        lines.append("\n---\n")

    overall = evidence.get("overall_assessment", "")
    if overall:
        lines.append(f"## Overall Assessment\n{overall}\n")

    missing = evidence.get("missing_papers", [])
    if missing:
        lines.append("## Missing Papers (search suggestions)\n")
        for m in missing:
            lines.append(f"- **{m.get('title', '?')}**: {m.get('why_needed', '')}")
            if m.get("search_suggestion"):
                lines.append(f"  Search: `{m['search_suggestion']}`")
        lines.append("")

    thread = evidence.get("strongest_narrative_thread", [])
    if thread:
        lines.append(f"## Strongest Narrative Thread\n{' → '.join(thread)}\n")

    report_path = os.path.join(output_dir, "evidence_sufficiency.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Evidence sufficiency report: {report_path}")

    # --- Report 2: Evidence Inventory ---
    inv_lines = ["# Evidence Inventory by Beat\n"]
    inv_items = inventory.get("evidence_inventory", [])
    for item in inv_items:
        inv_lines.append(f"## Beat {item.get('beat', '?')}: {item.get('title', '')}\n")
        if item.get("narrative"):
            inv_lines.append(f"{item['narrative']}\n")
        for p in item.get("core_papers", []):
            inv_lines.append(f"- **{p.get('citation_note', p.get('title', '?'))}**")
            inv_lines.append(f"  Role: {p.get('role', '')}")
            inv_lines.append(f"  Finding: {p.get('key_finding', '')}")
        if item.get("remaining_gaps"):
            inv_lines.append(f"\nRemaining gaps:")
            for g in item["remaining_gaps"]:
                inv_lines.append(f"  ⚠ {g}")
        inv_lines.append("\n---\n")

    outline = inventory.get("suggested_paper_outline", {})
    if outline:
        inv_lines.append("## Suggested Paper Structure\n")
        for section, info in outline.items():
            inv_lines.append(f"- {section}: ~{info.get('papers', '?')} papers, {info.get('pages', '?')} pages")

    inv_path = os.path.join(output_dir, "evidence_inventory.md")
    with open(inv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(inv_lines))
    log.info(f"Evidence inventory: {inv_path}")

    # --- Report 3: Category summary (quick reference) ---
    cat_lines = ["# Paper Corpus by Category\n"]
    by_cat = {}
    for p in classified:
        cat = p.get("primary_category", "X")
        if cat == "X":
            continue
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(p)

    cat_names = {
        "A": "Model Collapse Theory", "B": "Web Data Pollution & Scale",
        "C": "Detection & Reactive Limits", "D": "Information Theory + Text Quality",
        "E": "Data Quality & Curation", "F": "Human Data Value & RLHF",
        "G": "Platform & Provenance Design", "H": "Temporal Web Quality Measurement",
        "I": "Social Reasoning Benchmarks", "J": "Fine-tune Data Composition Ablation",
    }
    for cat in sorted(by_cat):
        papers = sorted(by_cat[cat], key=lambda x: x.get("citationCount", 0), reverse=True)
        cat_lines.append(f"## {cat}: {cat_names.get(cat, '')} ({len(papers)} papers)\n")
        for p in papers[:15]:
            cat_lines.append(
                f"- [{p.get('year', '?')}] {p.get('title', '?')[:80]} "
                f"(cites={p.get('citationCount', 0)})"
            )
            if p.get("one_sentence_contribution"):
                cat_lines.append(f"  → {p['one_sentence_contribution'][:100]}")
        if len(papers) > 15:
            cat_lines.append(f"  ... and {len(papers) - 15} more")
        cat_lines.append("")

    cat_path = os.path.join(output_dir, "corpus_by_category.md")
    with open(cat_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cat_lines))
    log.info(f"Corpus by category: {cat_path}")

    _generate_related_work_draft(base_dir, classified, output_dir)
    _generate_reference_list(base_dir, classified, output_dir)


def _generate_related_work_draft(base_dir: str, classified: list[dict], output_dir: str):
    """Generate a readable related-work prose draft from narrative chains."""
    analysis_dir = os.path.join(base_dir, "analysis")
    chains_path = os.path.join(analysis_dir, "narrative_chains.json")
    if not os.path.exists(chains_path):
        return

    chains = load_json(chains_path)
    if not isinstance(chains, list):
        return

    by_id = {p["paperId"]: p for p in classified}
    lines = ["# Related Work Draft\n"]
    lines.append("*Auto-generated prose draft built from narrative chains. Treat as a draft scaffold, not a final polished section.*\n")

    for chain in chains:
        if not isinstance(chain, dict) or chain.get("error"):
            continue
        beat = chain.get("beat", "?")
        beat_name = chain.get("beat_name", f"Beat {beat}")
        lines.append(f"\n## Beat {beat}: {beat_name}\n")

        anchor = chain.get("anchor_paper", {})
        anchor_id = anchor.get("paperId")
        anchor_label = _paper_short_citation(by_id.get(anchor_id, {})) if anchor_id in by_id else anchor_id
        if anchor_label:
            lines.append(f"Anchor paper: {anchor_label}.")
            if anchor.get("why"):
                lines.append(anchor["why"])
                lines.append("")

        for para in chain.get("paragraph_outline", []):
            if not isinstance(para, dict):
                continue
            opening = (para.get("opening_sentence") or "").strip()
            paper_ids = para.get("papers", []) or []
            cited = [_paper_short_citation(by_id[pid]) for pid in paper_ids if pid in by_id]
            support = ""
            if cited:
                support = " Key sources: " + "; ".join(cited) + "."
            paragraph = (opening + support).strip()
            if paragraph:
                lines.append(paragraph)
                lines.append("")

        notes = (chain.get("writing_notes") or "").strip()
        if notes:
            lines.append(f"Writing note: {notes}\n")

    draft_path = os.path.join(output_dir, "related_work_draft.md")
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    log.info(f"Related work draft: {draft_path}")


def _generate_reference_list(base_dir: str, classified: list[dict], output_dir: str):
    """Generate a references list for papers used in narrative chains."""
    analysis_dir = os.path.join(base_dir, "analysis")
    chains_path = os.path.join(analysis_dir, "narrative_chains.json")
    if not os.path.exists(chains_path):
        return

    chains = load_json(chains_path)
    if not isinstance(chains, list):
        return

    by_id = {p["paperId"]: p for p in classified}
    ordered_ids = []
    seen = set()
    for chain in chains:
        if not isinstance(chain, dict):
            continue
        for pid in _iter_chain_paper_ids(chain):
            if pid in by_id and pid not in seen:
                seen.add(pid)
                ordered_ids.append(pid)

    papers = [by_id[pid] for pid in ordered_ids]
    papers.sort(key=lambda p: ((p.get("year") or 0), (p.get("title") or "").lower()))

    lines = ["# Related Work References\n"]
    lines.append(f"*Selected references used in `narrative_chains.json` and `writing_outline.md`. Total: {len(papers)}.*\n")

    for idx, paper in enumerate(papers, start=1):
        authors = _paper_authors_text(paper)
        year = paper.get("year", "n.d.")
        title = (paper.get("title") or "Untitled").strip()
        venue = (paper.get("venue") or paper.get("journal") or "").strip()
        pid = paper.get("paperId", "")
        doi = ((paper.get("source_ids") or {}).get("doi") or paper.get("doi") or "").strip()
        arxiv = ((paper.get("source_ids") or {}).get("arxiv") or "").strip()

        ref = f"{idx}. {authors} ({year}). {title}."
        if venue:
            ref += f" {venue}."
        ref += f" `{pid}`"
        if doi:
            ref += f" DOI: `{doi}`"
        elif arxiv:
            ref += f" arXiv: `{arxiv}`"
        lines.append(ref)

    ref_path = os.path.join(output_dir, "related_work_references.md")
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    log.info(f"Related work references: {ref_path}")


def _iter_chain_paper_ids(chain: dict):
    anchor = chain.get("anchor_paper", {})
    anchor_id = anchor.get("paperId")
    if anchor_id:
        yield anchor_id

    for item in chain.get("spine", []) or []:
        pid = item.get("paperId")
        if pid:
            yield pid

    for item in chain.get("supporting", []) or []:
        pid = item.get("paperId")
        if pid:
            yield pid

    for para in chain.get("paragraph_outline", []) or []:
        for pid in para.get("papers", []) or []:
            if pid:
                yield pid


def _paper_short_citation(paper: dict) -> str:
    if not paper:
        return ""
    author = _paper_first_author(paper) or "Unknown"
    year = paper.get("year", "n.d.")
    title = (paper.get("title") or "Untitled").strip()
    return f"{author} et al. ({year}), {title}"


def _paper_authors_text(paper: dict) -> str:
    authors = paper.get("authors") or []
    names = []
    for author in authors[:5]:
        if isinstance(author, dict):
            name = author.get("name")
        else:
            name = str(author)
        if name:
            names.append(name.strip())
    if not names:
        first = _paper_first_author(paper)
        return first if first else "Unknown author"
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} et al."


def _paper_first_author(paper: dict) -> str:
    authors = paper.get("authors") or []
    if not authors:
        return ""
    first = authors[0]
    if isinstance(first, dict):
        return (first.get("name") or "").strip()
    return str(first).strip()
