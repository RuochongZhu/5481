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
    BEAT_CATEGORIES, BEAT_SECONDARY_CATEGORIES, BEAT_NAMES, ARGUMENT_LINES,
    NUM_BEATS, BEAT_TYPES, MUST_CITE_COUNTEREVIDENCE, HONESTY_CONSTRAINTS,
    CITATION_VERB_RULES, LOCAL_ANCHOR_PREFIX,
)


_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load_primary_anchors() -> dict[int, dict]:
    """Load Beat 4/6 pseudo-anchor metadata from manual_core_inclusions.json.

    Returns a dict mapping beat_num -> primary anchor entry. For primary_data
    and artifact beats that have no literature category, the pseudo-anchor is
    injected into the narrative chain so phase_contracts.ensure_narrative_chains_valid
    succeeds. See config/manual_core_inclusions.json::primary_anchors.
    """
    path = os.path.join(_PROJECT_ROOT, "config", "manual_core_inclusions.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as fh:
            data = json.load(fh)
    except Exception:  # pragma: no cover - misformatted config
        return {}
    out: dict[int, dict] = {}
    for anchor in data.get("primary_anchors", []):
        if not isinstance(anchor, dict):
            continue
        for beat in anchor.get("supports_beats", []):
            if isinstance(beat, int) and beat not in out:
                out[beat] = anchor
    return out

# Per-beat prioritized paperIds used to up-weight important literature in
# narrative-chain agent prompts. Empty at v4 W1 start; populate after Phase 1
# once the corpus has real DOIs for the v4 beat anchors.
BEAT_PRIORITY_PAPERS: dict[int, list[str]] = {
    1: [],
    2: [],
    3: [],
    4: [],  # primary_data beat uses local:CornellCarpoolSurvey2026
    5: [],
    6: [],  # artifact beat uses local:CampusRideSystem2026
    7: [],
}

# Per-beat paperIds that should be down-weighted in narrative chains (e.g.
# off-topic survey hits). Empty at v4 W1 start.
BEAT_DEEMPHASIZED_PAPERS: dict[int, set[str]] = {}

BEAT_NARRATIVE_GUIDANCE = {
    1: (
        "Beat 1 motivates §2.1: commercial ridesharing (Uber/Lyft) underserves small-town university "
        "settings in both pricing and availability, and the small-town coordination gap extends beyond "
        "transportation to marketplace, activities, and peer interactions. Use Category A (small-town / "
        "campus transport gap) as the anchor; Category B (P2P rideshare / sharing-economy trust) supports "
        "the 'why peer / campus-scoped platforms are worth designing' bridge. "
        "Use verbs: exists, motivates, is documented. AVOID: has been proved, is quantified, "
        "definitively shows. Preview finding F1 (Uber perceived expensive 28/32; availability issues 23/32) "
        "at the end of the first paragraph only as a teaser — the full finding belongs to Beat 4 (§4.1)."
    ),
    2: (
        "Beat 2 motivates §2.2: this is the paper's longest related-work subsection because it carries "
        "the double argument — grassroots coordination + multi-module platform. Build a four-paragraph "
        "chain: (1) international students already self-organize carpool coordination via WeChat/WhatsApp "
        "(Category C+D, anchor Sawyer & Chen or equivalent), (2) this coordination extends beyond carpool "
        "to marketplace / activities / help-seeking — a single social channel carrying multi-domain "
        "coordination (Category C+D), (3) super-app / integrated-platform literature (Category I) gives "
        "partial but incomplete guidance for campus scope, (4) transition to Beat 3 design primitives. "
        "Preview finding F2 (17/72 Mandarin vs 1/15 English used WeChat groups for carpool) at end of "
        "paragraph 1. "
        "Use verbs: document, indicate, suggest. For super-app literature use 'initial inquiry' not "
        "'established design space'. AVOID: the first multi-module campus platform, demonstrates a design space."
    ),
    3: (
        "Beat 3 defines §2.3: four design primitives distilled from literature — (1) institutional "
        "identity (E: .edu / campus scope), (2) safety infrastructure (F: real-time location + SOS), "
        "(3) rating fairness (H: peer reputation + algorithmic management concerns), (4) rewards / "
        "gamification (G). Each primitive is one paragraph with one classic citation + one recent (2022+) "
        "citation. Present the four as PARALLEL; do NOT value-rank them here — Beats 4/5/6 do the ranking. "
        "Identity primitive (¶1) wording is TIERED against Category E manual-inclusion count and MUST NOT "
        "jump tiers: if E native N>=5 say 'mature literature specialized here to institutional and .edu-scoped "
        "contexts'; if E native N=3-4 say 'moderate precedent — a well-studied trust signal in sharing "
        "economy, with institutional/.edu scoping discussed case-by-case in HCI/CSCW, though systematic "
        "treatment is less developed'; if E native N<3 say 'under-investigated primitive — while identity "
        "verification has an established literature in broader sharing economy contexts, .edu-scoped identity "
        "as a distinct trust primitive has received limited systematic treatment, and we position this paper "
        "as one case within that under-investigated space' (i.e. scope disclosure, not a coverage failure). "
        "Use neutral definitional verbs: we distill, we propose, commonly discussed. AVOID: the canonical "
        "framework, validated primitives."
    ),
    4: (
        "Beat 4 is §4.1 passenger-side survey findings (primary_data). The anchor is the pseudo-anchor "
        "local:CornellCarpoolSurvey2026. The spine references findings (F1/F3/F4/F6) and section labels, "
        "not paperIds. Narrative: (1) recap N cohort — N=111 eligible / 44 finished (6 Survey-Preview test "
        "responses excluded) and 79% Mandarin-native among the 91 respondents who reported native language "
        "(72/91), with per-item N reported separately because completion varies by question; (2) transport-gap "
        "quantification F1 — Uber pricing perceived too high 28/32, Uber availability problematic 23/32; "
        "(3) WTP safety-feature ranking F3 — all seven items >=50 on the 0-100 scale, with means 69.1 "
        "(Real-Time Location Sharing), 67.3 (.edu school-email verification), 63.5 (Emergency SOS), 60.5 "
        "(driver experience visibility), 55.4 (auto trip-sharing with emergency contacts), 54.9 (driver "
        "social connections), 50.9 (interior car photos); (4) motivation structure F4 — financial dominant, "
        "gamification secondary, social and environmental also present; (5) F6 preview of Q23 driver supply "
        "willingness (N=33) — Ithaca 10/33, short-distance 9/33, long-distance 12/33 Very+Extremely willing, "
        "long-distance is the highest supply scenario at 36% and feeds §5.2 carpool-module scope motivation "
        "(Beat 6). "
        "NO inferential statistics, NO p-values, NO 'significantly'. Use: we observe, reports indicate, "
        "median value is. Disclose 79% Mandarin-native (72/91) as scope, not as bias and not as a selling point."
    ),
    5: (
        "Beat 5 is §4.2 driver-side tolerance + the counterintuitive rating-fairness asymmetry. v4.2 "
        "MAJOR REVISION: the finding is NO LONGER reported on the full N=30 sample. It is reported on "
        "the Driver/Both subset (N=19, self-reported travel role Driver or Both) against a Rider-only "
        "control subset (N=12). Using the full mixed sample dilutes real drivers' experience-anchored "
        "answers with riders' hypothetical answers to 'as a driver, how tolerant would you be'. "
        "The anchor is Rosenblat & Stark 2016 (or closest algorithmic management anchor in Category H/J). "
        "Narrative: "
        "(1) Driver/Both subset (N=19) four-dimensional tolerance on the 0-100 scale — late passenger "
        "(Q24_1) 47.2, destination change (Q24_2) 41.4, unfair rating (Q24_3) 29.1, non-standard route "
        "(Q24_4) 52.3; unfair rating (29.1) is 12.3-23.2 points below the other three (41.4-52.3) — this "
        "is the core counterintuitive observation: the thing drivers least tolerate is not passenger "
        "misbehavior but unfairness from the rating system itself. "
        "(2) Rider-only control subset (N=12) numbers MUST BE REPORTED in the same paragraph as "
        "methodological justification for the subset split: 35.7 / 19.6 / 22.4 / 33.2 on Q24_1 / Q24_2 / "
        "Q24_3 / Q24_4. In the rider-only control the pattern is weak — 'unfair rating' 22.4 is not "
        "distinctively low and is actually higher than 'destination change' 19.6 — which is exactly why "
        "the full-sample mix washed the pattern out, and why reporting on the Driver/Both subset is the "
        "methodologically honest choice. Do NOT hide these control numbers because the pattern weakens; "
        "the weakening IS the justification. "
        "(3) Contextualize with algorithmic management literature (Rosenblat & Stark, Lee et al.); "
        "frame as 'resonates with' / 'parallels' at smaller, amateur-driver campus scale, NOT "
        "'replicates' or 'confirms'. Explicitly note that the literature covers professional gig "
        "workers, and whether amateur/occasional-driver rating anxiety is isomorphic is an open "
        "question the paper raises rather than answers. "
        "Spine: F+H papers (including H-subgroup for amateur drivers) as contextualizing frame; J can "
        "support the adversarial framing into Beat 7. "
        "Attribution MUST go to 'Driver/Both subset (N=19)' — never drop the subset label, never mix "
        "with full-sample N=30 numbers. AVOID: proves, confirms, validates the same phenomenon, "
        "replicates Rosenblat & Stark."
    ),
    6: (
        "Beat 6 is §5 CampusRide platform (artifact). The anchor is the pseudo-anchor "
        "local:CampusRideSystem2026. The spine references module names ('module:carpool', 'module:marketplace', "
        "etc.) and finding keys ('finding:F3', 'finding:F4', 'finding:F5', 'finding:F6'), not real paperIds. "
        "Narrative: (1) §5.1 platform overview with 6-module x 4-primitive matrix; (2) §5.2 carpool module "
        "scope — cite F6 (Q23 driver supply willingness, N=33: Ithaca 10/33, short-distance 9/33, "
        "long-distance 12/33 Very+Extremely willing) as the evidence for prioritizing long-distance carpool "
        "as the deep-dive scope, because long-distance is the highest supply scenario at 36%; (3) §5.2-5.7 "
        "remaining modules get one subsection each at overview level; (4) §5.8 carpool deep-dive with four "
        "design decisions (identity, safety, rating fairness, gamification) each explicitly motivated by a "
        "survey finding — identity ties to F3 mean 67.3 / median 79; safety ties to F3 Real-Time Location "
        "69.1 and SOS 63.5; rating fairness ties to F5 Driver/Both-subset (N=19) 29.1 versus same-subset "
        "41.4-52.3 on the other three Q24 items; gamification ties to F4. F5 attribution MUST stay at the "
        "Driver/Both subset level — never smear F5 back onto the full sample. "
        "Use: we designed, we implemented, motivated by, in response to finding X. AVOID: effective, "
        "successful, proves, validates. Acknowledge: no deployment data; six-module claim acknowledges "
        "only carpool is deep-dived."
    ),
    7: (
        "Beat 7 is §7.2 adversarial scoping — the honesty anchor. Five paragraphs, each citing at least "
        "one counterevidence paper (Category J primarily, H secondarily): "
        "(1) formalization risk — platform-mediated coordination may reproduce algorithmic management "
        "harms (Rosenblat & Stark, Lee et al.); "
        "(2) sample skew — THREE-TIER disclosure is required and none of the three may be suppressed: "
        "(a) main-sample language skew — 79% Mandarin-native (72/91 who reported native language) limits "
        "generalizability, with English-native respondents at 15/91 (16%) leaving any claim about them "
        "highly uncertain; (b) driver-subset skew — the F5 rating-fairness asymmetry rests on the "
        "Driver/Both subset N=19, which is methodologically preferred to the full-sample mix (see §4.2 "
        "¶2 justification) but still very small and requires a dedicated driver-side survey to confirm; "
        "(c) completion skew — 44/111 finished (~40% completion rate), so finishers may differ "
        "systematically from non-finishers on carpool salience; "
        "(3) no deployment evaluation — the four design decisions are not compared in real-world use; "
        "(4) .edu scope boundary — identity verification does NOT verify driving competence, behavior, "
        "or platform governance; "
        "(5) gamification risk — cross-module points may induce gaming / fake trips. "
        "Use: may reproduce, we acknowledge, scope-limited. AVOID: we address, we prevent, we solve. "
        "This beat succeeds by honest scoping, not by defending the thesis at all costs."
    ),
}

# Known-good pairwise progressions verified out-of-band. Empty at v4 W1 start;
# populate via check_citations.py once v4 seed papers are fetched.
MANUAL_VERIFIED_PROGRESSIONS: dict[tuple[str, str], str] = {}

# STRUCTURED_BEAT_SPECS is empty at v4 W1 start. The v4 pipeline handles
# Beats 4 and 6 (primary_data / artifact) via _build_primary_anchor_chain;
# literature beats (1,2,3,5,7) are refined by the LLM agent output alone.
# Populate this dict post-W3 only if a specific literature beat needs extra
# structural tightening beyond what the agent produces.
STRUCTURED_BEAT_SPECS: dict[int, dict] = {}


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


_BEAT4_SPINE_KEYS = [
    ("finding:F1", "Uber pricing perceived expensive (28/32) and availability issues (23/32)"),
    ("finding:F3", "Safety-feature WTP ranking: real-time location 69.1, .edu 67.3, SOS 63.5 (F3 means on 0-100 scale)"),
    ("finding:F4", "Motivation structure: financial 63.6, gamification 48.3, social 45.6, environmental 44.5"),
    ("finding:F6", "Driver supply willingness (Q23): long-distance 12/33 Very+Extremely willing (highest), Ithaca 10/33, short 9/33"),
]

_BEAT4_PARAGRAPHS = [
    {
        "paragraph": 1,
        "topic": "Methodology recap and scope disclosure",
        "papers": ["finding:F1"],
        "opening_sentence": "The formative survey yielded N=111 eligible respondents and N=44 who finished the full instrument (6 Survey-Preview test rows excluded); 79% of respondents who reported native language were Mandarin-native (72/91), which we disclose as scope rather than mask as bias.",
    },
    {
        "paragraph": 2,
        "topic": "Quantified transport gap and WTP for safety / identity features",
        "papers": ["finding:F1", "finding:F3"],
        "opening_sentence": "Passengers report Uber as expensive (28/32) and often unavailable (23/32); across seven asked-for features, all cross the 50 mean-WTP threshold, with real-time location (mean 69.1 / median 76), .edu verification (mean 67.3 / median 79), and emergency SOS (mean 63.5 / median 64) as the top three.",
    },
    {
        "paragraph": 3,
        "topic": "Motivation structure + driver supply willingness (F6)",
        "papers": ["finding:F4", "finding:F6"],
        "opening_sentence": "Passenger motivation splits into two tiers — financial at 63.6 then gamification / social / environmental clustered at 48.3 / 45.6 / 44.5 — while driver supply willingness (F6, N=33) favours long-distance trips (12/33 Very+Extremely willing) over in-Ithaca (10/33) and short-distance (9/33), directly informing the carpool module's long-distance scope priority in §5.2.",
    },
]

_BEAT6_SPINE_KEYS = [
    ("module:carpool", "Carpool module — deep-dive with four design decisions"),
    ("module:marketplace", "Marketplace module — .edu-scoped P2P trading with bidirectional rating"),
    ("module:activities", "Activities module — cross-cultural event organization and check-in"),
    ("module:groups", "Groups module — interest and geo groups with group-map discovery"),
    ("module:messages", "Messages module — cross-module embedded communication layer"),
    ("module:points", "Points module — cross-module gamification meta-layer, deliberately auxiliary"),
]

_BEAT6_PARAGRAPHS = [
    {
        "paragraph": 1,
        "topic": "Platform overview and the 6-module x 4-primitive design matrix",
        "papers": ["module:carpool", "module:marketplace", "module:activities", "module:groups", "module:messages", "module:points"],
        "opening_sentence": "CampusRide is a Vue 3 + Express + Supabase + Socket.IO platform integrating six modules (carpool, marketplace, activities, groups, messaging, points) that share four design primitives from Beat 3.",
    },
    {
        "paragraph": 2,
        "topic": "Six-module overview with cross-module design primitive reuse + F6 long-distance scope",
        "papers": ["module:marketplace", "module:activities", "module:groups", "module:messages", "module:points", "finding:F6"],
        "opening_sentence": "Each module reuses the platform's shared .edu identity layer and messaging infrastructure; only carpool fully exercises all four primitives at maximum intensity, which — combined with F6's long-distance driver-supply willingness (12/33 highest) — is why we select carpool, with long-distance trips as its priority scope, for deep-dive analysis.",
    },
    {
        "paragraph": 3,
        "topic": "Carpool deep-dive: four design decisions motivated by survey findings F3/F4/F5/F6",
        "papers": ["module:carpool", "finding:F3", "finding:F4", "finding:F5", "finding:F6"],
        "opening_sentence": "The carpool deep-dive operationalizes four design decisions motivated by survey findings: .edu identity verification (F3), safety skeleton with real-time location and SOS (F3), bidirectional rating with Driver/Both-subset fairness consideration (F5, N=19), and gamification kept as a secondary incentive (F4); F6's long-distance driver-supply preference anchors §5.2's carpool scope choice.",
    },
]


def _build_primary_anchor_chain(beat_num: int, beat_name: str,
                                anchor: dict, context_papers: list[dict]) -> dict:
    """Construct a narrative_chain for a primary_data / artifact beat.

    Uses the pseudo-anchor from manual_core_inclusions.primary_anchors and
    section / finding / module keys in the spine. Context papers from
    BEAT_SECONDARY_CATEGORIES enter as supporting entries.
    """
    beat_type = BEAT_TYPES.get(beat_num, "primary_data")
    anchor_id = anchor.get("paperId", f"{LOCAL_ANCHOR_PREFIX}Beat{beat_num}Anchor")
    anchor_title = anchor.get("title", f"Primary anchor for Beat {beat_num}")

    if beat_num == 4:
        spine_keys = _BEAT4_SPINE_KEYS
        paragraphs = _BEAT4_PARAGRAPHS
        why = (
            "Formative Cornell Carpool Survey (N=111 eligible / 44 finished, 6 Survey-Preview "
            "test rows excluded) is the primary-data source grounding passenger-side WTP and "
            "motivation findings (F1/F3/F4) plus driver supply willingness (F6, N=33). It is a "
            "pseudo-anchor because it is grey literature contributed by the authors, not a "
            "retrieved peer-reviewed paper."
        )
    elif beat_num == 6:
        spine_keys = _BEAT6_SPINE_KEYS
        paragraphs = _BEAT6_PARAGRAPHS
        why = (
            "CampusRide multi-module platform is the artifact anchor for the core contribution. "
            "It is a pseudo-anchor because the system itself is the evidence, not a peer-reviewed "
            "paper about it; the system is described via its implementation documentation."
        )
    else:
        spine_keys = [(f"local:Beat{beat_num}_anchor", anchor_title)]
        paragraphs = [{
            "paragraph": 1,
            "topic": anchor_title,
            "papers": [anchor_id],
            "opening_sentence": anchor.get("abstract", "")[:240],
        }]
        why = anchor.get("note_for_pipeline", "Pseudo-anchor for primary-data / artifact beat.")

    spine = [
        {
            "paperId": anchor_id,
            "position": 1,
            "role_in_narrative": f"Pseudo-anchor for {beat_type} beat: {anchor_title}.",
            "ordering_basis": "thematic_progression",
            "ordering_note": "Primary-data / artifact beat: spine entries are internal finding or module keys rather than citation-ordered paperIds.",
            "transition_to_next": "Subsequent entries walk through the findings / modules that belong to this beat.",
        }
    ]
    for idx, (key, label) in enumerate(spine_keys, start=2):
        spine.append({
            "paperId": key,
            "position": idx,
            "role_in_narrative": label,
            "ordering_basis": "thematic_progression",
            "ordering_note": "Internal section / finding / module reference (not a citation).",
            "transition_to_next": "",
        })
    if spine:
        spine[-1]["transition_to_next"] = ""

    # Context papers from secondary categories become supporting references.
    ranked_context = sorted(
        context_papers,
        key=lambda x: (x.get("citationCount", 0), x.get("year", 0)),
        reverse=True,
    )[:10]
    supporting = [
        {
            "paperId": p.get("paperId", ""),
            "attached_to_spine_paper": anchor_id,
            "role": f"Contextualizing reference from category {p.get('primary_category', 'X')}: {p.get('title', '')[:80]}",
        }
        for p in ranked_context
        if p.get("paperId")
    ]

    return {
        "beat": beat_num,
        "beat_name": beat_name,
        "argument_line": ARGUMENT_LINES.get(beat_num, "unknown"),
        "beat_type": beat_type,
        "anchor_paper": {
            "paperId": anchor_id,
            "why": why,
        },
        "spine": spine,
        "supporting": supporting,
        "paragraph_outline": paragraphs,
        "writing_notes": (
            BEAT_NARRATIVE_GUIDANCE.get(beat_num, "")
            + " (Primary-data / artifact beat: chain assembled from manual_core_inclusions.primary_anchors; "
              "contextualizing literature is listed as supporting rather than spine.)"
        ),
    }


def _build_narrative_chains(client, classified: list[dict],
                            citation_map: dict) -> list[dict]:
    """For each beat, use NARRATIVE_ANALYST to construct the narrative chain."""
    chains = []
    primary_anchors = _load_primary_anchors()

    for beat_num, categories in BEAT_CATEGORIES.items():
        beat_name = BEAT_NAMES[beat_num]
        log.info(f"  Beat {beat_num} ({beat_name}): categories {categories}")

        # Primary-data / artifact beats bypass the LLM chain path and use the
        # pseudo-anchor from manual_core_inclusions.json. Their spine references
        # contextualizing papers from BEAT_SECONDARY_CATEGORIES and finding /
        # module keys (see BEAT_NARRATIVE_GUIDANCE for Beats 4 and 6).
        beat_type = BEAT_TYPES.get(beat_num)
        if beat_type in {"primary_data", "artifact"}:
            context_cats = BEAT_SECONDARY_CATEGORIES.get(beat_num, [])
            context_papers = [
                p for p in classified
                if p.get("primary_category") in context_cats
                or any(c in context_cats for c in p.get("secondary_categories", []))
            ]
            anchor = primary_anchors.get(beat_num, {})
            chains.append(_build_primary_anchor_chain(beat_num, beat_name, anchor, context_papers))
            log.info(
                "  Beat %s populated with pseudo-anchor %s for %s beat (context papers=%d)",
                beat_num, anchor.get("paperId", "?"), beat_type, len(context_papers),
            )
            continue

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
