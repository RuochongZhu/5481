"""Phase 3.5: Narrative Chain Construction — per-beat writing-ready paper ordering."""

from __future__ import annotations

import json
import logging
import os
import re

from .api_client import (
    BRAIN_PHASE3_NARRATIVE,
    OpenCitationsClient,
    S2Client,
    S2_FIELDS,
    agent_run,
)
from .paper_identity import build_alias_lookup, canonicalize_paper_ref, extract_source_ids, get_s2_lookup_id
from .phase_contracts import ensure_narrative_chains_valid
from .prompts import NARRATIVE_ANALYST
from .state_manager import complete_step, is_step_complete, save_state
from .utils import atomic_write_json, load_json, filter_active_papers

log = logging.getLogger("research_agent")

# Import centralized beat definitions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.beat_definitions import (
    BEAT_CATEGORIES, BEAT_NAMES, ARGUMENT_LINES, NUM_BEATS,
    MUST_CITE_COUNTEREVIDENCE, HONESTY_CONSTRAINTS, CITATION_VERB_RULES,
)

BEAT_PRIORITY_PAPERS = {
    1: [
        "doi:10.1038/s41586-024-07566-y",
        "doi:10.52591/lxai202312101",
        "doi:10.48550/arxiv.2311.16822",
        "doi:10.48550/arxiv.2406.07515",
        "doi:10.48550/arxiv.2402.07043",
        "doi:10.48550/arxiv.2602.16136",
        "doi:10.48550/arxiv.2303.13408",
    ],
    2: [
        "doi:10.1145/3590152",
        "doi:10.1145/3442381.3450048",
        "doi:10.48550/arxiv.2406.17557",
    ],
    3: [
        "doi:10.1075/sl.22034.oh",
        "doi:10.3390/e22040394",
        "doi:10.1103/rxxz-lk3n",
        "doi:10.18653/v1/2024.findings-naacl.228",
    ],
    4: [
        "doi:10.18653/v1/d19-1454",
        "doi:10.18653/v1/2022.emnlp-main.248",
        "doi:10.48550/arxiv.2305.11206",
        "doi:10.48550/arxiv.2212.08073",
        "doi:10.48550/arxiv.2303.17548",
        "doi:10.48550/arxiv.2305.18290",
        "doi:10.48550/arxiv.2309.00267",
    ],
    5: [
        "doi:10.18653/v1/d19-1454",
        "doi:10.48550/arxiv.2305.11206",
        "doi:10.48550/arxiv.2305.18290",
        "doi:10.48550/arxiv.2305.14387",
        "doi:10.48550/arxiv.2309.00267",
        "doi:10.48550/arxiv.2310.16944",
        "doi:10.18653/v1/2022.emnlp-main.248",
    ],
    6: [
        "doi:10.48550/arxiv.2404.12691",
        "doi:10.48550/arxiv.2304.07327",
        "doi:10.1145/3774904.3792955",
        "doi:10.1145/3770762.3772602",
        "doi:10.1145/2632048.2632054",
        "doi:10.1007/s00779-005-0046-3",
        "doi:10.5334/cstp.303",
        "doi:10.1017/aap.2022.33",
    ],
    7: [
        "doi:10.48550/arxiv.2408.03314",
        "doi:10.48550/arxiv.2201.11903",
        "doi:10.48550/arxiv.2203.11171",
        "doi:10.48550/arxiv.2001.08361",
        "doi:10.48550/arxiv.2501.12948",
        "doi:10.48550/arxiv.2501.19393",
    ],
}

BEAT_DEEMPHASIZED_PAPERS = {
    1: {
        "doi:10.31234/osf.io/83k9r",
        "doi:10.31234/osf.io/83k9r_v1",
        "doi:10.22555/pjets.v12i1.1077",
        "doi:10.1111/cobi.70138",
    },
}

BEAT_NARRATIVE_GUIDANCE = {
    1: (
        "Beat 1 must read as a three-step chain: (1) recursive synthetic reuse / collapse risk, "
        "(2) partial but still incomplete contamination-pressure evidence in information environments, "
        "(3) detector fragility and the limits of reactive filtering. Prefer a category-A anchor such as "
        "Nature 2024 collapse or go-MAD style work. Do not use perception / labeling papers as proof of "
        "web-scale contamination; if they appear, keep them as downstream social consequences or supporting context. "
        "Before any category-B bridge, insert one explicit scope-limiting step or transition that says the literature "
        "mostly proves indiscriminate recursive reuse risk, not universal synthetic-data failure; papers like Beyond Model "
        "Collapse or A Tale of Tails can serve this limiting step. If category-B evidence is still thin, say so explicitly "
        "instead of forcing a strong bridge. "
        "MUST cite counterevidence: pi^2/6 pathway (mixed real+synthetic avoids collapse), self-correcting loops, "
        "curated synthetic data success cases."
    ),
    2: (
        "Beat 2 should progress from measurement proxies to longitudinal web observations to crawl-curation practice. "
        "Keep the conclusion narrow: measurable drift is partial and indirect, not decisive proof of web-wide contamination. "
        "MUST cite counterevidence: RefinedWeb/FineWeb show filtered web data still trains strong models. "
        "Explicitly state: no post-2022 web-scale contamination audit exists in the corpus."
    ),
    3: (
        "Beat 3 defines L_auth as a fine-tuning-focused descriptive framework with four dimensions: "
        "Provenance Ratio (D1), Lexical Diversity (D2), Entropy (D3), Social Behavioral Diversity (D4). "
        "D1 and D4 are design-level inputs; D2 and D3 are measurable emergent outcomes. "
        "End on scope limits: L_auth is a synthesis of metric ingredients for post-training data composition, not a validated standalone law or stage-agnostic result. "
        "Weight calibration is explicitly future work."
    ),
    4: (
        "Beat 4 belongs to the primary post-training evidence line. Its evidence base is independent of Beat 1's "
        "collapse mechanism. Do NOT use pretraining collapse papers to support fine-tuning claims. "
        "Balance human-data value against bounded synthetic success cases (RLAIF, AlpacaFarm, Zephyr). "
        "The defensible claim is narrower: human data appears especially valuable for socially grounded tasks, "
        "not that it universally dominates. "
        "MUST cite counterevidence: RLAIF matches RLHF on summarization, AlpacaFarm 50x cheaper, "
        "Zephyr 7B beats LLaMA2-Chat-70B with AI feedback DPO."
    ),
    5: (
        "Beat 5 is the contrastive fine-tuning experiment. Frame as 'pilot study' not 'validation'. "
        "Use 'initial evidence suggests' not 'demonstrates'. "
        "Acknowledge: 3B model may not amplify data quality differences sufficiently. "
        "Acknowledge: D1 and D4 co-vary in this design, cannot separate independent contributions. "
        "This beat shares categories F, I, J with Beat 4 but focuses on experimental methodology. "
        "Treat LIMA as a cross-beat anchor, not unique proof for Beat 5: in Beat 4 it motivates why post-training "
        "data quality matters, while in Beat 5 it only justifies the plausibility of a provenance-sensitive contrast. "
        "Explicitly state that the pilot holds inference-time compute fixed because self-consistency, structured "
        "chain-of-thought, and DEL-ToM-style inference-time scaling are live rival explanations that the paper "
        "cannot apportion away after the fact."
    ),
    6: (
        "Beat 6 should present CampusGo as a deployed provenance-aware core contribution, not merely a proposal. "
        "ANCHOR-CONTRIBUTION RELATIONSHIP: Longpre et al. (2024) is the problem-diagnosis anchor, not the solution itself. "
        "CampusGo should be framed as one concrete operationalization of authenticity, consent, and provenance requirements "
        "for post-training social-reasoning data, not as fulfillment of the entire agenda or as validated downstream impact. "
        "Use platform and provenance precedents to frame the implementation and governance requirements, "
        "but do not claim CampusGo or any platform solution is validated as improving downstream model performance. "
        "Acknowledge: G-category literature is from adjacent domains (citizen science, biomedicine, "
        "Indigenous data governance), not directly from AI training data collection."
    ),
    7: (
        "Beat 7 is adversarial scoping. Build a short chain around competing mechanisms such as inference-time scaling, "
        "test-time compute, chain-of-thought, extended thinking, and model scale. The beat should succeed by narrowing "
        "the thesis to fixed-compute data-composition effects where appropriate, not by dismissing these alternatives."
    ),
}

MANUAL_VERIFIED_PROGRESSIONS = {
    ("doi:10.48550/arxiv.2305.18290", "doi:10.48550/arxiv.2305.14387"):
        "Verified by check_citations.py: AlpacaFarm cites DPO.",
    ("doi:10.48550/arxiv.2305.18290", "doi:10.48550/arxiv.2310.16944"):
        "Verified by check_citations.py: Zephyr cites DPO.",
}

STRUCTURED_BEAT_SPECS = {
    4: {
        "anchor": "doi:10.48550/arxiv.2305.11206",
        "spine": [
            "doi:10.18653/v1/2022.emnlp-main.248",
            "doi:10.48550/arxiv.2305.11206",
            "doi:10.48550/arxiv.2303.17548",
            "doi:10.48550/arxiv.2305.18290",
            "doi:10.48550/arxiv.2309.00267",
        ],
        "roles": {
            "doi:10.18653/v1/2022.emnlp-main.248":
                "Establishes why social reasoning is the right downstream target: even strong LLMs lag on mental-state and norm-sensitive tasks, so this capability cannot be assumed from pretraining alone.",
            "doi:10.48550/arxiv.2305.11206":
                "Anchor paper for Beat 4: LIMA shows that a small, carefully curated human-authored set can drive large alignment gains, making data provenance a high-leverage post-training variable.",
            "doi:10.48550/arxiv.2303.17548":
                "Shows that post-training data source changes socially meaningful outputs, not just generic helpfulness: instruction tuning shifts whose opinions the model appears to reflect.",
            "doi:10.48550/arxiv.2305.18290":
                "Provides the clean methodological hinge: DPO simplifies preference optimization so feedback-source comparisons become more interpretable than full RLHF stacks.",
            "doi:10.48550/arxiv.2309.00267":
                "Provides required counterevidence: AI feedback can match RLHF on bounded dialogue and summarization tasks, so the claim must stay narrower than universal human-data superiority.",
        },
        "transitions": {
            ("doi:10.18653/v1/2022.emnlp-main.248", "doi:10.48550/arxiv.2305.11206"):
                "Once social reasoning is established as a persistent weak spot, the next question is whether carefully curated post-training data can move that behavior more efficiently than scale alone.",
            ("doi:10.48550/arxiv.2305.11206", "doi:10.48550/arxiv.2303.17548"):
                "After LIMA makes curation a plausible treatment variable, the literature asks whether provenance alters socially meaningful outputs rather than only general chat quality.",
            ("doi:10.48550/arxiv.2303.17548", "doi:10.48550/arxiv.2305.18290"):
                "If provenance affects social judgments, then the optimization pipeline itself matters, which is why later work isolates a simpler preference-learning objective.",
            ("doi:10.48550/arxiv.2305.18290", "doi:10.48550/arxiv.2309.00267"):
                "With a simpler alignment method in place, the strongest counterclaim is that AI-generated preference signals may substitute for human judgments on bounded tasks.",
        },
        "paragraphs": [
            {
                "topic": "Social reasoning remains a distinct post-training weak spot",
                "papers": [
                    "doi:10.18653/v1/d19-1454",
                    "doi:10.18653/v1/2022.emnlp-main.248",
                ],
                "opening_sentence": "The fine-tuning line should begin from task sensitivity, not from collapse theory: social commonsense and theory-of-mind style reasoning remain meaningfully weaker than generic instruction following.",
            },
            {
                "topic": "Curated human data and provenance shape socially meaningful behavior",
                "papers": [
                    "doi:10.48550/arxiv.2304.07327",
                    "doi:10.48550/arxiv.2305.11206",
                    "doi:10.48550/arxiv.2303.17548",
                ],
                "opening_sentence": "Against that backdrop, human conversational corpora and curated instruction sets make data provenance concrete, and LIMA plus opinion-shift evidence show that source quality affects socially meaningful outputs.",
            },
            {
                "topic": "Methodological hinge plus bounded-task counterevidence",
                "papers": [
                    "doi:10.48550/arxiv.2305.18290",
                    "doi:10.48550/arxiv.2305.14387",
                    "doi:10.48550/arxiv.2309.00267",
                    "doi:10.48550/arxiv.2310.16944",
                ],
                "opening_sentence": "The honest conclusion comes only after the counterexamples: DPO makes source comparisons cleaner, but AlpacaFarm, RLAIF, and Zephyr all show that synthetic or AI-feedback pipelines can succeed on bounded alignment objectives.",
            },
        ],
        "supporting": [
            {
                "paperId": "doi:10.18653/v1/d19-1454",
                "attached_to_spine_paper": "doi:10.18653/v1/2022.emnlp-main.248",
                "role": "Benchmark anchor showing that social interaction reasoning remains far below human performance.",
            },
            {
                "paperId": "doi:10.48550/arxiv.2304.07327",
                "attached_to_spine_paper": "doi:10.48550/arxiv.2305.11206",
                "role": "Human-generated conversation corpus that makes post-training provenance concrete rather than hypothetical.",
            },
            {
                "paperId": "doi:10.48550/arxiv.2305.14387",
                "attached_to_spine_paper": "doi:10.48550/arxiv.2305.18290",
                "role": "Low-cost simulated-feedback baseline that narrows any claim of uniquely human preference data.",
            },
            {
                "paperId": "doi:10.48550/arxiv.2310.16944",
                "attached_to_spine_paper": "doi:10.48550/arxiv.2309.00267",
                "role": "Additional counterevidence that AI-feedback distillation can be highly competitive on general chat alignment.",
            },
        ],
        "writing_notes":
            "Keep Beat 4 clearly separate from collapse literature. The defensible chain is: social reasoning is a real post-training weak spot; curated human data can be disproportionately high leverage; provenance changes socially meaningful outputs; and bounded-task counterevidence prevents any universal claim that human data always wins. The final sentence of the beat should explicitly narrow the thesis to socially grounded, norm-sensitive behavior rather than alignment overall.",
    },
    5: {
        "anchor": "doi:10.48550/arxiv.2305.11206",
        "spine": [
            "doi:10.18653/v1/d19-1454",
            "doi:10.48550/arxiv.2305.11206",
            "doi:10.48550/arxiv.2305.18290",
            "doi:10.48550/arxiv.2310.16944",
        ],
        "roles": {
            "doi:10.18653/v1/d19-1454":
                "Establishes Social IQa as a demanding evaluation target, which is why the pilot uses social reasoning rather than only generic chat benchmarks.",
            "doi:10.48550/arxiv.2305.11206":
                "Anchor paper for Beat 5: LIMA is the clearest precedent that data quality and curation can matter enough to justify a provenance-sensitive fine-tuning contrast.",
            "doi:10.48550/arxiv.2305.18290":
                "Defines the pilot's methodological hinge: DPO keeps the optimization recipe simple enough that differences between data conditions remain interpretable.",
            "doi:10.48550/arxiv.2310.16944":
                "Provides the strongest competitive synthetic baseline: AI-feedback distillation can produce strong chat alignment, which is why the pilot must be framed as a directional test rather than a foregone human-data victory.",
        },
        "transitions": {
            ("doi:10.18653/v1/d19-1454", "doi:10.48550/arxiv.2305.11206"):
                "Because the benchmark is intentionally socially grounded, the next step is a precedent showing that carefully curated fine-tuning data can materially change behavior.",
            ("doi:10.48550/arxiv.2305.11206", "doi:10.48550/arxiv.2305.18290"):
                "Once data quality is treated as the intervention, the method must stay simple enough that condition-to-condition differences remain interpretable.",
            ("doi:10.48550/arxiv.2305.18290", "doi:10.48550/arxiv.2310.16944"):
                "With a controlled preference objective in place, the strongest next baseline is Zephyr, which applies AI-feedback distillation on top of a DPO-style alignment recipe while still leaving inference-time compute fixed so rival decoding explanations can be named explicitly later.",
        },
        "paragraphs": [
            {
                "topic": "Why the pilot uses social reasoning as its evaluation target",
                "papers": [
                    "doi:10.18653/v1/d19-1454",
                    "doi:10.18653/v1/2022.emnlp-main.248",
                ],
                "opening_sentence": "The experiment beat should begin by justifying the evaluation target: social reasoning remains difficult enough that small changes in data provenance are more likely to surface here than on generic chat benchmarks.",
            },
            {
                "topic": "Why a provenance-sensitive contrast is methodologically plausible",
                "papers": [
                    "doi:10.48550/arxiv.2305.11206",
                    "doi:10.48550/arxiv.2305.18290",
                    "doi:10.48550/arxiv.2305.14387",
                ],
                "opening_sentence": "LIMA motivates the treatment variable, DPO keeps the comparison interpretable, and AlpacaFarm shows why a synthetic baseline is methodologically reasonable even if it is not the same as socially grounded human data.",
            },
            {
                "topic": "Why the outcome must be framed as directional rather than validated",
                "papers": [
                    "doi:10.48550/arxiv.2309.00267",
                    "doi:10.48550/arxiv.2310.16944",
                ],
                "opening_sentence": "The strongest existing counterevidence comes from bounded alignment tasks: RLAIF and Zephyr show that AI feedback can already be highly competitive, which is why the present experiment can only offer directional evidence on social reasoning rather than full validation.",
            },
        ],
        "supporting": [
            {
                "paperId": "doi:10.18653/v1/2022.emnlp-main.248",
                "attached_to_spine_paper": "doi:10.18653/v1/d19-1454",
                "role": "Broader theory-of-mind benchmark evidence showing that social reasoning deficits persist in strong LLMs.",
            },
            {
                "paperId": "doi:10.48550/arxiv.2305.14387",
                "attached_to_spine_paper": "doi:10.48550/arxiv.2305.18290",
                "role": "Low-cost simulated-feedback baseline that makes a non-human comparison arm realistic for pilot studies.",
            },
            {
                "paperId": "doi:10.48550/arxiv.2309.00267",
                "attached_to_spine_paper": "doi:10.48550/arxiv.2310.16944",
                "role": "Bounded-task counterevidence showing AI feedback can already match RLHF in dialogue and summarization.",
            },
        ],
        "writing_notes":
            "Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. Handle LIMA explicitly as a cross-beat paper: in Beat 4 it supports the broader claim that curation matters, while in Beat 5 it only motivates why a provenance-sensitive intervention is worth testing. State explicitly that the pilot fixes inference-time compute, prompt/interface conditions, and retrieval usage precisely because self-consistency, structured CoT, and DEL-ToM-style inference-time scaling are live rival explanations; the corpus does not let the paper apportion causal weight among those mechanisms after the fact. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.",
    },
    6: {
        "anchor": "doi:10.48550/arxiv.2404.12691",
        "spine": [
            "doi:10.1007/s00779-005-0046-3",
            "doi:10.1145/2632048.2632054",
            "doi:10.48550/arxiv.2404.12691",
            "doi:10.48550/arxiv.2304.07327",
            "doi:10.1017/aap.2022.33",
        ],
        "roles": {
            "doi:10.1007/s00779-005-0046-3":
                "Provides the broad feasibility precedent: mobile sensing can capture rich human behavioral traces over time.",
            "doi:10.1145/2632048.2632054":
                "Narrows that feasibility claim into the university setting by showing that continuous smartphone sensing can characterize student behavior in a campus environment.",
            "doi:10.48550/arxiv.2404.12691":
                "Anchor paper for Beat 6: AI data authenticity, consent, and provenance are currently fragmented, so a deployed CampusGo-style collection platform needs these requirements baked in from the start.",
            "doi:10.48550/arxiv.2304.07327":
                "Provides the bridge from collection to downstream use: intentionally gathered human conversations can become alignment corpora, so a CampusGo-style platform is not just sensing infrastructure but a potential data-generation pathway.",
            "doi:10.1017/aap.2022.33":
                "Adds the stewardship boundary: contributors must remain stakeholders in how sensitive data are curated and reused, which keeps CampusGo deployed-but-scoped rather than extractive or overclaimed.",
        },
        "transitions": {
            ("doi:10.1007/s00779-005-0046-3", "doi:10.1145/2632048.2632054"):
                "A general sensing precedent becomes relevant only after it is narrowed into a campus-specific behavioral setting.",
            ("doi:10.1145/2632048.2632054", "doi:10.48550/arxiv.2404.12691"):
                "Once campus collection looks feasible, the key question becomes not sensing alone but how authenticity, consent, and provenance should be represented for AI use.",
            ("doi:10.48550/arxiv.2404.12691", "doi:10.48550/arxiv.2304.07327"):
                "Once provenance requirements are explicit, the next question is whether intentionally collected human interaction data can actually flow into alignment pipelines; OpenAssistant provides that bridge.",
            ("doi:10.48550/arxiv.2304.07327", "doi:10.1017/aap.2022.33"):
                "A usable human-data pipeline is still not enough unless contributors remain visible as ongoing stakeholders in reuse and curation decisions.",
        },
        "paragraphs": [
            {
                "topic": "Campus-situated collection is technically plausible",
                "papers": [
                    "doi:10.1007/s00779-005-0046-3",
                    "doi:10.1145/2632048.2632054",
                ],
                "opening_sentence": "The beat should start with implementation feasibility only: adjacent mobile-sensing work shows that campus-scale behavioral collection is technically plausible, not that deployment alone proves model-training value.",
            },
            {
                "topic": "AI-specific provenance requirements define the proposal core",
                "papers": [
                    "doi:10.48550/arxiv.2404.12691",
                    "doi:10.48550/arxiv.2304.07327",
                    "doi:10.3389/fclim.2021.637037",
                ],
                "opening_sentence": "What turns simple sensing into a defensible proposal is the provenance layer plus a downstream use case: authenticity, consent, and governance must be designed together, and OpenAssistant shows that intentionally collected human conversations can in fact become alignment data.",
            },
            {
                "topic": "Stewardship requirements keep CampusGo deployed but carefully scoped",
                "papers": [
                    "doi:10.5334/cstp.303",
                    "doi:10.1017/aap.2022.33",
                ],
                "opening_sentence": "The final move is a scope limit: stewardship principles show why CampusGo can be presented as a deployed provenance-aware platform, but not as a validated intervention for downstream model gains.",
            },
        ],
        "supporting": [
            {
                "paperId": "doi:10.3389/fclim.2021.637037",
                "attached_to_spine_paper": "doi:10.1017/aap.2022.33",
                "role": "Power-sensitive governance lens reinforcing that open-data defaults are insufficient for contributor-originated data.",
            },
            {
                "paperId": "doi:10.5334/cstp.303",
                "attached_to_spine_paper": "doi:10.1017/aap.2022.33",
                "role": "Operational reminder that documentation, interoperability, and reuse norms often break before raw data collection does.",
            },
        ],
        "writing_notes":
            "Beat 6 should read as deployed requirements engineering, not downstream validation. Longpre et al. (2024) is the diagnosis anchor that names the broken properties of present AI data pipelines; CampusGo is positioned as one concrete operationalization of those requirements for socially grounded post-training data, not as proof that the full authenticity agenda is solved. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a deployed system would need to satisfy.",
    },
}


def run_phase3_5(state: dict, state_path: str, base_dir: str, client,
                 s2: S2Client | None = None) -> dict:
    """Orchestrate Phase 3.5: narrative chain construction per beat."""
    proc_dir = os.path.join(base_dir, "data", "processed")
    analysis_dir = os.path.join(base_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    classified_path = os.path.join(proc_dir, "classified.json")
    if not os.path.exists(classified_path):
        log.error("classified.json not found. Run Phase 2 first.")
        return state

    classified = filter_active_papers(load_json(classified_path))
    log.info(f"Phase 3.5: building narrative chains for {len(classified)} papers")

    # Load verified citation chains from check_citations.py if available
    verified_chains_path = os.path.join(base_dir, "citation_chains.json")
    verified_chains = {}
    if os.path.exists(verified_chains_path):
        verified_data = load_json(verified_chains_path)
        for edge in verified_data.get("edges", []):
            src = edge.get("from", "")
            tgt = edge.get("to", "")
            if src and tgt:
                verified_chains.setdefault(src, []).append(tgt)
        log.info(f"Loaded {len(verified_data.get('edges', []))} verified citation edges from citation_chains.json")

    # Step 1: Expand citation graph (full pairwise references)
    if not is_step_complete(state, "3.5", "citation_expansion"):
        log.info("=== Phase 3.5.1: Full citation expansion ===")
        citation_map = _expand_full_citations(classified, s2, proc_dir)
        state = complete_step(state, state_path, "3.5", "citation_expansion", {
            "papers_expanded": len(citation_map),
        })
    else:
        citation_map = _load_normalized_citation_map(classified, proc_dir)
        log.info(f"Citation map loaded: {len(citation_map)} papers")

    # Step 2: Build narrative chains per beat
    if not is_step_complete(state, "3.5", "narrative_chains"):
        log.info("=== Phase 3.5.2: Narrative chain construction ===")
        chains = _build_narrative_chains(client, classified, citation_map)
        atomic_write_json(os.path.join(analysis_dir, "narrative_chains.json"), chains)
        ensure_narrative_chains_valid(chains)
        state = complete_step(state, state_path, "3.5", "narrative_chains", {
            "beats_processed": len(chains),
        })
    else:
        chains = load_json(os.path.join(analysis_dir, "narrative_chains.json"))

    # Step 3: Generate writing-ready outline
    if not is_step_complete(state, "3.5", "writing_outline"):
        log.info("=== Phase 3.5.3: Writing outline generation ===")
        _generate_writing_outline(chains, classified, os.path.join(base_dir, "output"))
        state = complete_step(state, state_path, "3.5", "writing_outline")

    return state


def _expand_full_citations(classified: list[dict], s2: S2Client | None,
                           proc_dir: str) -> dict:
    """For each paper in corpus, fetch its references list from S2.

    This builds a full directed citation graph: paper → [papers it cites].
    Only tracks citations within our corpus (internal edges).
    """
    cite_path = os.path.join(proc_dir, "full_citation_map.json")

    # Load existing progress
    citation_map = _load_normalized_citation_map(classified, proc_dir)

    if s2 is None:
        log.warning("No S2 client — skipping citation expansion, using existing edges only")
        return citation_map

    oc_token = os.environ.get("OPENCITATIONS_ACCESS_TOKEN") or None
    oc = OpenCitationsClient(access_token=oc_token)

    # Build set of all paper IDs in corpus for filtering
    corpus_ids = {p["paperId"] for p in classified}
    alias_lookup = build_alias_lookup(classified)

    # Only expand papers we haven't done yet
    to_expand = [
        p for p in classified
        if p["paperId"] not in citation_map
        and (get_s2_lookup_id(p) or extract_source_ids(p).get("doi"))
    ]

    log.info(f"Expanding citations for {len(to_expand)} papers ({len(citation_map)} already done)")

    for i, p in enumerate(to_expand):
        pid = p["paperId"]
        s2_pid = get_s2_lookup_id(p)
        paper_doi = extract_source_ids(p).get("doi")
        internal_refs = []
        try:
            if s2 is not None and s2_pid:
                refs = s2.get_references(s2_pid, limit=200, fields="paperId")
                ref_ids = [
                    canonicalize_paper_ref(r.get("paperId", ""), alias_lookup)
                    for r in refs
                    if r.get("paperId")
                ]
                # Only keep references that are in our corpus
                internal_refs = sorted({rid for rid in ref_ids if rid in corpus_ids})
            if not internal_refs and paper_doi:
                internal_refs = _expand_with_opencitations(oc, paper_doi, corpus_ids, alias_lookup)
            citation_map[pid] = internal_refs
            if (i + 1) % 20 == 0:
                log.info(f"  Expanded {i+1}/{len(to_expand)} papers")
                atomic_write_json(cite_path, citation_map)
        except Exception as e:
            log.warning(f"  Failed to expand {pid} via S2: {e}")
            if paper_doi:
                citation_map[pid] = _expand_with_opencitations(oc, paper_doi, corpus_ids, alias_lookup)
            else:
                citation_map[pid] = []

    atomic_write_json(cite_path, citation_map)
    total_edges = sum(len(v) for v in citation_map.values())
    log.info(f"Full citation map: {len(citation_map)} papers, {total_edges} internal edges")
    return citation_map


def _load_normalized_citation_map(classified: list[dict], proc_dir: str) -> dict[str, list[str]]:
    """Load legacy citation maps and rewrite them onto canonical paper IDs."""
    cite_path = os.path.join(proc_dir, "full_citation_map.json")
    if not os.path.exists(cite_path):
        return {}

    raw_map = load_json(cite_path)
    if not isinstance(raw_map, dict):
        return {}

    alias_lookup = build_alias_lookup(classified)
    corpus_ids = {p["paperId"] for p in classified}
    normalized: dict[str, list[str]] = {}
    changed = False

    for raw_key, raw_refs in raw_map.items():
        canonical_key = canonicalize_paper_ref(raw_key, alias_lookup)
        if canonical_key is None or canonical_key not in corpus_ids:
            changed = True
            continue

        refs = raw_refs if isinstance(raw_refs, list) else []
        canonical_refs = []
        for ref in refs:
            canonical_ref = canonicalize_paper_ref(ref, alias_lookup)
            if canonical_ref and canonical_ref in corpus_ids and canonical_ref != canonical_key:
                canonical_refs.append(canonical_ref)
            elif ref:
                changed = True

        merged = sorted(set(normalized.get(canonical_key, []) + canonical_refs))
        if merged != canonical_refs or raw_key != canonical_key:
            changed = True
        normalized[canonical_key] = merged

    if changed:
        atomic_write_json(cite_path, normalized)
        log.info("Normalized legacy full_citation_map.json to canonical paper IDs")

    return normalized


def _extract_dois_from_oc_field(value: str) -> list[str]:
    if not value:
        return []
    return re.findall(r"doi:([^\s;]+)", value, flags=re.I)


def _expand_with_opencitations(oc: OpenCitationsClient, doi: str, corpus_ids: set[str],
                               alias_lookup: dict[str, str]) -> list[str]:
    """Fallback DOI-to-DOI reference expansion via OpenCitations."""
    try:
        refs = oc.get_references(doi)
    except Exception as e:
        log.debug(f"  OpenCitations fallback failed for DOI {doi}: {e}")
        return []

    internal_refs = set()
    for row in refs:
        for cited_doi in _extract_dois_from_oc_field(row.get("cited", "")):
            canonical = canonicalize_paper_ref(cited_doi.lower(), alias_lookup)
            if canonical in corpus_ids:
                internal_refs.add(canonical)
            else:
                canonical = canonicalize_paper_ref(f"doi:{cited_doi.lower()}", alias_lookup)
                if canonical in corpus_ids:
                    internal_refs.add(canonical)
    return sorted(internal_refs)


def _build_narrative_chains(client, classified: list[dict],
                            citation_map: dict) -> list[dict]:
    """For each beat, use NARRATIVE_ANALYST to construct the narrative chain."""
    chains = []

    for beat_num, categories in BEAT_CATEGORIES.items():
        beat_name = BEAT_NAMES[beat_num]
        log.info(f"  Beat {beat_num} ({beat_name}): categories {categories}")

        # Collect papers for this beat
        beat_papers = [
            p for p in classified
            if p.get("primary_category") in categories
            or any(c in categories for c in p.get("secondary_categories", []))
        ]

        if not beat_papers:
            log.warning(f"  No papers for Beat {beat_num}, skipping")
            chains.append({"beat": beat_num, "beat_name": beat_name,
                           "error": "no_papers", "spine": [], "supporting": []})
            continue

        try:
            selected_papers = _select_narrative_input_papers(beat_num, beat_papers, categories)
            citation_edges = _collect_beat_citation_edges(selected_papers, citation_map)
            papers_input = _format_beat_papers(selected_papers, citation_edges)
            result = _run_narrative_agent(
                client,
                beat_num,
                beat_name,
                categories,
                beat_papers,
                selected_papers,
                citation_map,
                papers_input,
            )
            result = _apply_structured_refinement(
                beat_num,
                result,
                selected_papers,
                citation_map,
            )
            result = _normalize_spine_metadata(result)
            result["beat"] = beat_num
            result["beat_name"] = beat_name
            result["paper_count"] = len(beat_papers)
            result["input_paper_count"] = len(selected_papers)
            chains.append(result)
            spine_len = len(result.get("spine", []))
            log.info(f"  Beat {beat_num}: spine={spine_len} papers, "
                     f"supporting={len(result.get('supporting', []))} papers")
        except Exception as e:
            log.error(f"  Beat {beat_num} narrative failed: {e}")
            chains.append({"beat": beat_num, "beat_name": beat_name,
                           "error": str(e), "spine": [], "supporting": []})

    return chains


def _select_narrative_input_papers(beat_num: int, beat_papers: list[dict], categories: list[str],
                                   max_total: int = 24, per_category: int = 8) -> list[dict]:
    """Keep narrative prompts compact while preserving category coverage."""
    by_id = {}
    selected = []
    papers_by_id = {p["paperId"]: p for p in beat_papers}
    deemphasized = BEAT_DEEMPHASIZED_PAPERS.get(beat_num, set())

    def _ranked(items: list[dict]) -> list[dict]:
        return sorted(
            items,
            key=lambda x: (x.get("citationCount", 0), x.get("year", 0)),
            reverse=True,
        )

    def _try_add(paper: dict) -> bool:
        if len(selected) >= max_total:
            return False
        pid = paper["paperId"]
        if pid in by_id:
            return False
        by_id[pid] = paper
        selected.append(paper)
        return True

    for pid in BEAT_PRIORITY_PAPERS.get(beat_num, []):
        paper = papers_by_id.get(pid)
        if paper is not None:
            _try_add(paper)

    for category in categories:
        primary_papers = _ranked([
            p for p in beat_papers
            if p.get("primary_category") == category and p["paperId"] not in deemphasized
        ])
        secondary_papers = _ranked([
            p for p in beat_papers
            if p.get("primary_category") != category
            and category in p.get("secondary_categories", [])
            and p["paperId"] not in deemphasized
        ])
        added_for_category = 0
        for pool in (primary_papers, secondary_papers):
            for paper in pool:
                if added_for_category >= per_category or len(selected) >= max_total:
                    break
                if _try_add(paper):
                    added_for_category += 1
            if added_for_category >= per_category or len(selected) >= max_total:
                break

    if len(selected) < max_total:
        ranked = _ranked([p for p in beat_papers if p["paperId"] not in deemphasized])
        for paper in ranked:
            _try_add(paper)
            if len(selected) >= max_total:
                break

    if len(selected) < max_total and deemphasized:
        for paper in _ranked([p for p in beat_papers if p["paperId"] in deemphasized]):
            _try_add(paper)
            if len(selected) >= max_total:
                break

    selected.sort(key=lambda x: (x.get("year", 0), x.get("citationCount", 0)))
    return selected[:max_total]


def _collect_beat_citation_edges(beat_papers: list[dict], citation_map: dict) -> list[dict]:
    beat_ids = {p["paperId"] for p in beat_papers}
    citation_edges = []
    for paper in beat_papers:
        pid = paper["paperId"]
        for ref_id in citation_map.get(pid, []):
            if ref_id in beat_ids:
                citation_edges.append({"from": pid, "to": ref_id})
    return citation_edges


def _looks_like_truncation_error(error: Exception) -> bool:
    text = str(error).lower()
    return (
        "unterminated string" in text
        or "max_output_tokens" in text
        or "missing output text" in text
        or "incomplete" in text
        or "expecting ',' delimiter" in text
    )


def _run_narrative_agent(client, beat_num: int, beat_name: str, categories: list[str],
                         beat_papers: list[dict], selected_papers: list[dict],
                         citation_map: dict,
                         papers_input: str) -> dict:
    beat_guidance = BEAT_NARRATIVE_GUIDANCE.get(beat_num, "")
    argument_line = ARGUMENT_LINES.get(beat_num, "unknown")
    selected_by_id = {p["paperId"]: p for p in selected_papers}
    priority_titles = [
        f"{pid} :: {selected_by_id[pid].get('title', '')}"
        for pid in BEAT_PRIORITY_PAPERS.get(beat_num, [])
        if pid in selected_by_id
    ]
    priority_hint = (
        "Priority anchors to consider: "
        + " | ".join(priority_titles)
        if priority_titles else
        "Priority anchors to consider: none explicitly seeded for this beat."
    )

    # Argument line separation constraint
    line_warning = ""
    if argument_line == "primary":
        line_warning = (
            "\nCRITICAL CONSTRAINT: This beat belongs to the primary evidence line. "
            "Do NOT use motivation papers as direct support for the post-training claim. "
            "The primary line must stand on its own evidence base.\n"
        )
    elif argument_line == "motivation":
        line_warning = (
            "\nCRITICAL CONSTRAINT: This beat is motivation only. "
            "Do NOT present it as the direct evidence base for the primary post-training claim.\n"
        )

    # Honesty constraints
    honesty = HONESTY_CONSTRAINTS.get(beat_num, [])
    honesty_block = ""
    if honesty:
        honesty_block = "\nHonesty constraints for this beat:\n" + "\n".join(f"- {h}" for h in honesty) + "\n"

    task = (
        f"Construct the narrative chain for Beat {beat_num}: {beat_name}.\n"
        f"Argument line: {argument_line}\n\n"
        f"This beat covers categories {categories} and has {len(beat_papers)} candidate papers. "
        f"You are seeing the top {len(selected_papers)} papers selected for signal density.\n"
        f"Beat-specific guidance: {beat_guidance}\n"
        f"{line_warning}"
        f"{honesty_block}"
        f"{priority_hint}\n"
        f"If a required category is thin, make that weakness explicit in the chain instead of forcing a strong bridge.\n"
        f"Use at most 6 spine papers and at most 12 supporting papers.\n\n"
        f"{papers_input}"
    )
    try:
        raw = agent_run(
            client,
            role=NARRATIVE_ANALYST,
            model=BRAIN_PHASE3_NARRATIVE,
            task=task,
            max_tokens=8192,
        )
        result = _parse_json_object(raw)
        _ensure_narrative_beat_valid(result)
        return result
    except Exception as e:
        compact_papers = selected_papers[:16]
        compact_edges = _collect_beat_citation_edges(compact_papers, citation_map)
        compact_input = _format_beat_papers(compact_papers, compact_edges)
        compact_task = (
            f"Construct the narrative chain for Beat {beat_num}: {beat_name}.\n\n"
            f"This beat covers categories {categories}. The first attempt overflowed, so use this compact set "
            f"of {len(compact_papers)} papers only. Be concise.\n"
            f"Beat-specific guidance: {beat_guidance}\n"
            f"{priority_hint}\n"
            f"If a required category is thin, represent it as a limitation or supporting bridge, not a forced proof.\n"
            f"Use at most 5 spine papers and at most 8 supporting papers.\n\n"
            f"{compact_input}"
        )
        log.warning("  Beat %s retrying with compact narrative input (%s papers)", beat_num, len(compact_papers))
        try:
            raw = agent_run(
                client,
                role=NARRATIVE_ANALYST,
                model=BRAIN_PHASE3_NARRATIVE,
                task=compact_task,
                max_tokens=8192,
            )
            result = _parse_json_object(raw)
            _ensure_narrative_beat_valid(result)
            return result
        except Exception as second_error:
            log.error("  Beat %s using fallback narrative chain: %s", beat_num, second_error)
            return _fallback_narrative_chain(
                beat_num,
                beat_name,
                categories,
                beat_papers,
                selected_papers,
                error=second_error,
            )


def _apply_structured_refinement(beat_num: int, result: dict, selected_papers: list[dict],
                                 citation_map: dict[str, list[str]]) -> dict:
    """Tighten weak late-line beats into shorter, more inspectable chains."""
    spec = STRUCTURED_BEAT_SPECS.get(beat_num)
    if not spec:
        return result

    selected_by_id = {p["paperId"]: p for p in selected_papers}
    ranked_ids = [
        p["paperId"]
        for p in sorted(
            selected_papers,
            key=lambda x: (x.get("citationCount", 0), x.get("year", 0)),
            reverse=True,
        )
    ]

    spine_ids = [pid for pid in spec.get("spine", []) if pid in selected_by_id]
    target_spine_len = max(3, len(spec.get("spine", [])))
    for pid in [item.get("paperId", "") for item in result.get("spine", [])] + ranked_ids:
        if pid and pid in selected_by_id and pid not in spine_ids and len(spine_ids) < target_spine_len:
            spine_ids.append(pid)

    if len(spine_ids) < 3:
        return result

    anchor_id = spec.get("anchor")
    if anchor_id not in selected_by_id:
        anchor_id = result.get("anchor_paper", {}).get("paperId", "")
    if anchor_id and anchor_id not in spine_ids and anchor_id in selected_by_id:
        spine_ids = spine_ids[:1] + [anchor_id] + [pid for pid in spine_ids[1:] if pid != anchor_id]
        spine_ids = spine_ids[:target_spine_len]
    if not anchor_id:
        anchor_id = spine_ids[0]

    existing_anchor = result.get("anchor_paper", {}) or {}
    anchor_why = existing_anchor.get("why", "")
    if existing_anchor.get("paperId") != anchor_id or not anchor_why:
        anchor_why = spec.get("roles", {}).get(anchor_id, "Structured anchor selected for clearer narrative inspection.")

    spine = []
    for idx, pid in enumerate(spine_ids, start=1):
        next_id = spine_ids[idx] if idx < len(spine_ids) else ""
        transition = spec.get("transitions", {}).get((pid, next_id), "")
        ordering_basis, ordering_note, ordering_summary = _describe_ordering_basis(pid, next_id, citation_map)
        if transition and ordering_summary:
            transition = f"{transition} [{ordering_summary}]"
        item = {
            "paperId": pid,
            "position": idx,
            "role_in_narrative": spec.get("roles", {}).get(pid, f"Structured Beat {beat_num} spine paper."),
            "transition_to_next": transition,
        }
        if next_id:
            item["ordering_basis"] = ordering_basis
            item["ordering_note"] = ordering_note
        spine.append(item)

    supporting = []
    seen_support = set()
    for item in spec.get("supporting", []):
        pid = item.get("paperId", "")
        if pid in selected_by_id and pid not in spine_ids and pid not in seen_support:
            supporting.append(dict(item))
            seen_support.add(pid)
    for item in result.get("supporting", []):
        pid = item.get("paperId", "")
        if pid in selected_by_id and pid not in spine_ids and pid not in seen_support and len(supporting) < 8:
            supporting.append(item)
            seen_support.add(pid)

    paragraphs = []
    for idx, para in enumerate(spec.get("paragraphs", []), start=1):
        paper_ids = [pid for pid in para.get("papers", []) if pid in selected_by_id]
        if not paper_ids:
            continue
        paragraphs.append({
            "paragraph": idx,
            "topic": para.get("topic", f"Beat {beat_num} paragraph {idx}"),
            "papers": paper_ids,
            "opening_sentence": para.get("opening_sentence", ""),
        })

    refined = dict(result)
    refined["anchor_paper"] = {"paperId": anchor_id, "why": anchor_why}
    refined["spine"] = spine
    refined["supporting"] = supporting
    if paragraphs:
        refined["paragraph_outline"] = paragraphs
    refined["writing_notes"] = spec.get("writing_notes", result.get("writing_notes", ""))
    refined["structured_refinement"] = True
    return refined


def _describe_ordering_basis(current_id: str, next_id: str,
                             citation_map: dict[str, list[str]]) -> tuple[str, str, str]:
    if not next_id:
        return "", "", ""

    if current_id in citation_map.get(next_id, []):
        note = f"Verified citation order: {next_id} cites {current_id}."
        return "verified_citation", note, "verified citation order"

    manual_note = MANUAL_VERIFIED_PROGRESSIONS.get((current_id, next_id))
    if manual_note:
        return "verified_citation", manual_note, "verified citation order"

    if next_id in citation_map.get(current_id, []):
        note = (
            "Direct internal citation runs in the opposite direction, so this sequence is kept as "
            "thematic progression rather than strict citation order."
        )
        return "thematic_progression", note, "thematic progression; direct citation runs in the opposite direction"

    note = (
        "No direct internal citation edge was found; order is justified by the argument progression "
        "rather than by a verified citation chain."
    )
    return "thematic_progression", note, "thematic progression; no verified internal citation edge"


def _ensure_narrative_beat_valid(result: dict) -> dict:
    if not isinstance(result, dict):
        raise ValueError("narrative beat result is not an object")

    anchor = result.get("anchor_paper")
    if not isinstance(anchor, dict) or not anchor.get("paperId"):
        raise ValueError("narrative beat missing anchor_paper.paperId")

    spine = result.get("spine")
    if not isinstance(spine, list) or not spine:
        raise ValueError("narrative beat missing non-empty spine")

    paragraphs = result.get("paragraph_outline")
    if not isinstance(paragraphs, list) or not paragraphs:
        raise ValueError("narrative beat missing non-empty paragraph_outline")

    return result


def _normalize_spine_metadata(result: dict) -> dict:
    """Ensure each spine item has explicit ordering/transition metadata for reviewers."""
    if not isinstance(result, dict):
        return result

    spine = result.get("spine")
    if not isinstance(spine, list):
        return result

    normalized = []
    total = len(spine)
    for idx, item in enumerate(spine, start=1):
        if not isinstance(item, dict):
            continue
        fixed = dict(item)
        next_exists = idx < total
        if next_exists:
            fixed.setdefault("ordering_basis", "thematic_progression")
            fixed.setdefault(
                "ordering_note",
                "Order is justified by the argument progression rather than a verified internal citation chain.",
            )
            fixed.setdefault(
                "transition_to_next",
                "The next paper narrows, extends, or qualifies this claim while keeping the beat within its supported scope.",
            )
        else:
            fixed.setdefault("transition_to_next", "")
        normalized.append(fixed)

    result["spine"] = normalized
    return result


def _fallback_narrative_chain(beat_num: int, beat_name: str, categories: list[str],
                              beat_papers: list[dict], selected_papers: list[dict],
                              error: Exception) -> dict:
    """Build a conservative, contract-compliant narrative chain."""
    selected_by_id = {p["paperId"]: p for p in selected_papers}
    ranked = sorted(
        selected_papers,
        key=lambda x: (x.get("citationCount", 0), x.get("year", 0)),
        reverse=True,
    )

    anchor = None
    for pid in BEAT_PRIORITY_PAPERS.get(beat_num, []):
        if pid in selected_by_id:
            anchor = selected_by_id[pid]
            break
    if anchor is None:
        anchor = ranked[0] if ranked else (beat_papers[0] if beat_papers else {})

    spine_ids = []

    def _push(paper_id: str):
        if paper_id and paper_id not in spine_ids and len(spine_ids) < 6:
            spine_ids.append(paper_id)

    _push(anchor.get("paperId", ""))
    for category in categories:
        primary = sorted(
            [p for p in selected_papers if p.get("primary_category") == category],
            key=lambda x: (x.get("citationCount", 0), x.get("year", 0)),
            reverse=True,
        )
        if primary:
            _push(primary[0]["paperId"])
    for paper in ranked:
        _push(paper["paperId"])

    spine_papers = [selected_by_id[pid] for pid in spine_ids if pid in selected_by_id]
    supporting_papers = [p for p in ranked if p["paperId"] not in spine_ids][:8]

    spine = []
    for idx, paper in enumerate(spine_papers, start=1):
        role = "Anchor / framing paper" if idx == 1 else f"Extends Beat {beat_num} through category {paper.get('primary_category', 'X')}"
        transition = (
            "The next paper narrows or extends the claim while keeping the beat within its supported scope."
            if idx < len(spine_papers) else
            ""
        )
        spine.append({
            "paperId": paper.get("paperId", ""),
            "position": idx,
            "role_in_narrative": role,
            "transition_to_next": transition,
        })

    paragraphs = []
    groups = [
        ("Foundation and strongest anchors", spine_papers[: max(1, min(2, len(spine_papers)))]),
        ("Bridge evidence and scope limits", spine_papers[2:4] if len(spine_papers) > 2 else supporting_papers[:2]),
        ("Implications, tensions, and cautious takeaways", spine_papers[4:] if len(spine_papers) > 4 else supporting_papers[2:5]),
    ]
    para_num = 1
    for topic, papers in groups:
        papers = [p for p in papers if p]
        if not papers:
            continue
        paragraphs.append({
            "paragraph": para_num,
            "topic": topic,
            "papers": [p.get("paperId", "") for p in papers],
            "opening_sentence": (
                f"This paragraph organizes Beat {beat_num} conservatively after a narrative parse failure, "
                "prioritizing the strongest directly relevant anchors."
            ),
        })
        para_num += 1

    supporting = [
        {
            "paperId": p.get("paperId", ""),
            "attached_to_spine_paper": anchor.get("paperId", ""),
            "role": f"Fallback supporting context from category {p.get('primary_category', 'X')}.",
        }
        for p in supporting_papers
    ]

    guidance = BEAT_NARRATIVE_GUIDANCE.get(beat_num, "")
    return {
        "anchor_paper": {
            "paperId": anchor.get("paperId", ""),
            "why": f"Fallback anchor selected from the highest-signal seeded paper after narrative parse failure ({error}).",
        },
        "spine": spine,
        "supporting": supporting,
        "paragraph_outline": paragraphs,
        "writing_notes": (
            "Conservative fallback narrative chain generated after model JSON validation failed. "
            f"{guidance}"
        ).strip(),
        "fallback_warning": str(error),
    }

def _parse_json_object(raw: str) -> dict:
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

    raise last_error or ValueError("Narrative output did not contain a valid JSON object")


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


def _format_beat_papers(papers: list[dict], citation_edges: list[dict]) -> str:
    """Format papers and citation edges for the NARRATIVE_ANALYST."""
    lines = ["## Papers\n"]
    for p in sorted(papers, key=lambda x: x.get("year", 0)):
        lines.append(
            f"paperId: {p['paperId']}\n"
            f"title: {p.get('title', 'N/A')}\n"
            f"year: {p.get('year', 'N/A')}\n"
            f"category: {p.get('primary_category', 'X')}\n"
            f"key_claim: {p.get('key_claim', p.get('one_sentence_contribution', 'N/A'))}\n"
            f"method_type: {p.get('method_type', 'N/A')}\n"
            f"citations: {p.get('citationCount', 0)}\n"
            f"---"
        )

    if citation_edges:
        lines.append(f"\n## Citation Edges ({len(citation_edges)} internal edges)\n")
        for e in citation_edges[:60]:
            lines.append(f"{e['from']} → {e['to']}")

    return "\n".join(lines)


def _generate_writing_outline(chains: list[dict], classified: list[dict],
                               output_dir: str):
    """Generate a human-readable writing outline from narrative chains."""
    os.makedirs(output_dir, exist_ok=True)
    by_id = {p["paperId"]: p for p in classified}

    lines = ["# Related Work Writing Outline\n"]
    lines.append("*Auto-generated narrative structure for each beat*\n\n---\n")

    for chain in chains:
        beat = chain.get("beat", "?")
        name = chain.get("beat_name", "")
        lines.append(f"## Beat {beat}: {name}\n")

        if chain.get("error"):
            lines.append(f"⚠ Error: {chain['error']}\n\n---\n")
            continue

        # Anchor paper
        anchor = chain.get("anchor_paper", {})
        if anchor:
            pid = anchor.get("paperId", "")
            p = by_id.get(pid, {})
            lines.append(f"**Anchor paper**: {p.get('title', pid)}")
            lines.append(f"  Why: {anchor.get('why', 'N/A')}\n")

        # Spine
        spine = chain.get("spine", [])
        if spine:
            lines.append(f"**Narrative spine** ({len(spine)} papers):\n")
            for s in spine:
                pid = s.get("paperId", "")
                p = by_id.get(pid, {})
                title = p.get("title", pid)[:70]
                lines.append(f"  {s.get('position', '?')}. [{p.get('year', '?')}] {title}")
                lines.append(f"     Role: {s.get('role_in_narrative', 'N/A')}")
                if s.get("ordering_basis"):
                    lines.append(f"     Basis: {s['ordering_basis']}")
                if s.get("ordering_note"):
                    lines.append(f"     Note: {s['ordering_note']}")
                if s.get("transition_to_next"):
                    lines.append(f"     → {s['transition_to_next']}")
            lines.append("")

        # Paragraph outline
        paras = chain.get("paragraph_outline", [])
        if paras:
            lines.append("**Paragraph structure**:\n")
            for para in paras:
                lines.append(f"  ¶{para.get('paragraph', '?')}: {para.get('topic', '')}")
                if para.get("opening_sentence"):
                    lines.append(f"    Opening: \"{para['opening_sentence']}\"")
                paper_ids = para.get("papers", [])
                for pid in paper_ids:
                    p = by_id.get(pid, {})
                    lines.append(f"    - {p.get('title', pid)[:60]} ({p.get('year', '?')})")
            lines.append("")

        # Writing notes
        notes = chain.get("writing_notes", "")
        if notes:
            lines.append(f"**Writing notes**: {notes}\n")

        lines.append("---\n")

    outline_path = os.path.join(output_dir, "writing_outline.md")
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Writing outline: {outline_path}")
