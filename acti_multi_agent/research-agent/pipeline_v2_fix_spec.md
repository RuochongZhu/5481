# Pipeline v2 Fix Spec
# Target: acti_multi_agent/research-agent/
# Context: After successful v2 migration (score 0.853, 7 beats, Category K added)
# Goal: Fix 7 identified issues before manuscript drafting

---

## Priority Overview

| Priority | Issue | Blocks Writing? |
|---|---|---|
| P0 | Beat 1 missing `Curse of Recursion` linkage (data bug) | Yes |
| P0 | Beat 7 under-supported (only 5 papers, missing foundational CoT/test-time-compute) | Yes |
| P1 | Beat 4 missing Constitutional AI (canonical RLAIF reference) | Partially |
| P1 | Category K has duplicate entries (SymbCoT ×2, Polar Questions ×2) | No, but messy |
| P2 | X category 2 papers unresolved | No |
| P2 | Beat 6 anchor awkward (Longpre is problem-statement, not solution) | No |
| P3 | LIMA is anchor for both Beat 4 and Beat 5 (narrative overlap risk) | No |

---

## P0-1: Fix Beat 1 ↔ Curse of Recursion Linkage Bug

### Symptom
- `evidence_sufficiency.md` Beat 1 reports: `Key papers MISSING: The Curse of Recursion`
- But `corpus_by_category.md` Category A includes it (paperId: `s2:155aec5cff650263a4c71136f97570611d1bba7a`)
- `related_work_draft.md` Beat 1 spine paragraph 1 DOES cite it
- `writing_outline.md` Beat 1 lists it as spine position 1

**The paper is in the corpus and used in the narrative, but the sufficiency check can't find it.**

### Root Cause Hypothesis
The sufficiency check in `phase3_graph` or `phase4_topics` likely matches `key_papers_present` by title string. The title string in evaluation may be truncated or formatted differently than the one in classified.json. Specifically:
- Stored title: `"The Curse of Recursion: Training on Generated Data Makes Models Forget"`
- Possible matcher: looking for the full title via substring, but hitting a column-width truncation in the intermediate JSON

### Fix
1. Open `analysis/evidence_inventory.json`. Locate Beat 1 entry. Check if `core_papers[].paperId` array includes `s2:155aec5cff650263a4c71136f97570611d1bba7a`. If yes → bug is in sufficiency rendering; if no → bug is in beat-paper assignment.

2. Open `src/phase4_topics.py` (or whichever module generates `evidence_sufficiency.md`). Find the function that computes `key_papers_missing`. It likely does something like:

```python
required_key_papers = {"The Curse of Recursion", "AI models collapse", ...}
present = {p["title"] for p in beat_papers}
missing = required_key_papers - present
```

Change the matching from exact string to substring + case-insensitive:

```python
def title_match(required_title, paper_title):
    return required_title.lower() in paper_title.lower()

missing = [r for r in required_key_papers 
           if not any(title_match(r, p["title"]) for p in beat_papers)]
```

3. Alternatively, match by paperId rather than title — paperIds are canonical, titles are not. If the pipeline tracks required-papers by ID somewhere, prefer that path.

4. Re-run Phase 4 only: `python main.py --phase 4 --resume`

### Verification
After rerun, `evidence_sufficiency.md` Beat 1 should no longer list "The Curse of Recursion" under `Key papers MISSING`.

---

## P0-2: Supplement Beat 7 with Foundational Test-Time-Compute Papers

### Symptom
Beat 7 currently has only 5 supporting papers. `evidence_sufficiency.md` flags this as `🟠 weak` and explicitly lists two missing anchors:
- Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters (Snell et al. 2024)
- Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al. 2022)

Without these, Beat 7 cannot credibly argue that test-time scaling is a genuine competing mechanism — the corpus lacks the foundational papers.

### Fix
Add the following papers to Category K via targeted retrieval. Run Phase 1 corpus addition:

**Mandatory additions (2 papers):**

```
Paper 1:
  Title: Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
  Authors: Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar
  Year: 2024
  arXiv: 2408.03314
  Target category: K (primary)
  Role in Beat 7: Provides the strongest general-purpose evidence that test-time compute can substitute for training scale. Critical anchor for scoping claim.

Paper 2:
  Title: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
  Authors: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou
  Year: 2022
  arXiv: 2201.11903
  Target category: K (primary)
  Role in Beat 7: Canonical CoT foundation. Must be cited when framing test-time reasoning as a competing mechanism.
```

**Strongly recommended additions (3 papers, to bring Beat 7 support to ~10):**

```
Paper 3:
  Title: OpenAI o1 System Card (or "Learning to Reason with LLMs")
  Source: OpenAI technical report, September 2024
  URL: https://openai.com/index/learning-to-reason-with-llms/
  Target category: K
  Role: Industry-scale evidence that extended inference-time reasoning substantially improves reasoning benchmarks. Cite the system card; independent third-party evaluations if available.

Paper 4:
  Title: DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
  Authors: DeepSeek-AI et al.
  Year: 2025
  arXiv: 2501.12948
  Target category: K
  Role: Open-weight replication of o1-style reasoning. Important because it rules out "o1 is proprietary magic" — the mechanism is reproducible.

Paper 5:
  Title: s1: Simple test-time scaling
  Authors: Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, et al.
  Year: 2025
  arXiv: 2501.19393
  Target category: K
  Role: Shows test-time scaling works with just 1000 curated examples — directly relevant to L_auth's data-composition vs compute-scaling comparison.
```

### Implementation

**Option A: Manual CSV import** (fastest):

Create `data/raw/beat7_supplement.csv` with columns: `paperId,title,authors,year,venue,abstract,doi,arxiv_id,target_category`.

Run: `python main.py --import-file data/raw/beat7_supplement.csv`

Then: `python main.py --phase 1 --resume` to ingest into corpus.

Then: `python main.py --phase 2 --resume` to run classifier. The classifier should assign these to K given their abstracts.

**Option B: Targeted retrieval via API**:

In `config/beat_definitions.py`, Beat 7 `search_queries` are already defined. Run a targeted corpus expansion:

```python
# Temporary script: scripts/expand_beat7.py
from src.api_client import OpenAlexClient, S2Client
queries = [
    "test-time compute scaling LLM social reasoning",
    "chain-of-thought prompting elicits reasoning Wei 2022",
    "o1 DeepSeek R1 reasoning benchmark",
    "s1 simple test-time scaling 2025",
]
# Fetch top-5 per query, merge into data/processed/corpus_unified.json
```

Then re-run Phase 2 classification.

**Option C** (if you trust the classifier): modify `phase1_corpus.py` to prioritize Beat 7 queries in the next retrieval pass. Less precise but fully automated.

### Verification
- Category K should have ≥8 papers (currently 5, adding 2 mandatory gets 7, +3 recommended gets 10).
- Beat 7 `supporting_papers` in `evidence_sufficiency.md` should be ≥8.
- `evidence_sufficiency.md` Beat 7 status should change from `🟠 weak` to `🟡 adequate`.

---

## P1-1: Add Constitutional AI to Beat 4

### Symptom
`evidence_sufficiency.md` Beat 4 lists missing: `Constitutional AI: Harmlessness from AI Feedback`. This is the canonical RLAIF paper — without it, the counter-evidence argument in Beat 4 (that AI feedback works on bounded tasks) is weaker than it should be.

### Fix
Add to Category F:

```
Title: Constitutional AI: Harmlessness from AI Feedback
Authors: Yuntao Bai, Saurav Kadavath, Sandipan Kundu, et al. (Anthropic)
Year: 2022
arXiv: 2212.08073
Target category: F (primary)
Role in Beat 4: Canonical RLAIF paper. Required as counterevidence for the claim that human data is always necessary for alignment. Should be cited alongside RLAIF (Lee 2023), AlpacaFarm (Dubois 2023), Zephyr (Tunstall 2023).
```

Add via same mechanism as P0-2 (CSV import or API retrieval). Category F already has 16 papers so this just makes the counter-evidence cluster more complete.

---

## P1-2: Deduplicate Category K Entries

### Symptom
From `corpus_by_category.md` Category K:
- `Faithful Logical Reasoning via Symbolic Chain-of-Thought` appears twice (ACL + arXiv versions, different cites=29 vs cites=1)
- From `related_work_references.md`, same issue: entries 40 and 41 are duplicates

Similarly in `related_work_references.md` entries 65 and 66: `Relevant answers to polar questions` (preprint + journal versions).

### Fix
These are not true duplicates in the academic sense — they are different published versions of the same work. Pipeline should mark one as canonical and flag the other:

1. Open `data/processed/classified.json`. For each duplicate pair:
   - Keep the more formally published version as canonical (ACL version of SymbCoT, Phil Trans B version of Polar Questions)
   - Mark the preprint with:
```json
{
  "duplicate_of": "<canonical_paperId>",
  "duplicate_reason": "preprint version; canonical version available"
}
```

2. In `src/phase3_graph.py` (or wherever beat-paper counts are computed), add a filter:
```python
def active_papers(papers):
    return [p for p in papers if not p.get("duplicate_of") and not p.get("v2_pruned")]
```
Use `active_papers()` when counting support for beats, to avoid double-counting.

3. In `src/phase3_5_narrative.py` (narrative construction), only include canonical version in spine. Duplicates can be listed in `supporting` with a note, or omitted.

4. Re-run from Phase 3: `python main.py --phase 3 --resume`

### Verification
- `corpus_by_category.md` Category K should list each title once (or clearly mark duplicates)
- Beat 7 `supporting_papers` count should not double-count these
- Writing outline for Beat 7 should cite ACL/journal versions, not preprints

---

## P2-1: Resolve X-Category Papers

### Symptom
`evaluation_report.md` shows `X papers: 2, X ratio: 0.015`. These are papers the classifier couldn't fit into A–K.

### Fix
Identify them:
```bash
jq '.[] | select(.primary_category == "X") | {paperId, title}' data/processed/classified.json
```

For each X paper, one of three actions:
- **Reclassify** if the classifier missed a valid category (manually set `primary_category` and re-run Phase 3)
- **Prune** if the paper is genuinely off-topic (add `"v2_pruned": true, "v2_prune_reason": "X category, no thesis relevance"`)
- **Keep as X** if borderline; ensures honest reporting of noise in corpus

This is a quick manual review; should take under 15 minutes for 2 papers.

---

## P2-2: Clarify Beat 6 Anchor Framing

### Symptom
Beat 6 anchor is Longpre (2024) "Position: Data Authenticity, Consent, & Provenance for AI are all broken". This paper states the problem; CampusGo is your solution. The anchor-to-contribution relationship is slightly inverted.

### Fix
Do not change the anchor selection — Longpre is still the best-fitting paper in the corpus. Instead, modify the Beat 6 writing note to make the positioning explicit.

In `analysis/narrative_chains.json` → Beat 6 → `writing_notes`, prepend:

```
ANCHOR-CONTRIBUTION RELATIONSHIP: Longpre et al. (2024) enumerates the broken 
properties of AI data pipelines (authenticity, consent, provenance). CampusGo 
is positioned as ONE concrete operationalization of these requirements for 
post-training social-reasoning data — not a fulfillment of the full agenda, 
and not validated against alternative designs. The anchor names the problem; 
CampusGo offers a partial, deployed response.
```

Then re-run Phase 3.5 to regenerate `related_work_draft.md` and `writing_outline.md` with the updated note:
```
python main.py --phase 3.5 --resume
```

---

## P3: Differentiate LIMA's Role Across Beats 4 and 5

### Symptom
LIMA is anchor for both Beat 4 (provenance affects social reasoning) and Beat 5 (pilot experiment design). Without explicit differentiation, the writing could repeat the same LIMA argument twice.

### Fix
In `analysis/narrative_chains.json` → Beat 5 → `writing_notes`, append:

```
LIMA CROSS-BEAT HANDLING: LIMA is already introduced in Beat 4 as evidence that 
curated human data has disproportionate leverage on alignment. In Beat 5, 
reference Beat 4's treatment explicitly and pivot to the METHODOLOGICAL angle: 
LIMA demonstrates that pilot-scale (1000-example) curation can produce 
measurable behavioral differences, justifying a 300-500-dialogue contrastive 
design as methodologically plausible. Do NOT re-argue the "data quality matters" 
point — that is Beat 4's job.
```

Re-run Phase 3.5 as in P2-2.

---

## Execution Sequence

```
Step 1: Fix Beat 1 bug (P0-1)
  → Edit src/phase4_topics.py string matching logic
  → Rerun: python main.py --phase 4 --resume
  → Verify: evidence_sufficiency.md no longer flags Curse of Recursion missing

Step 2: Add Beat 7 papers (P0-2)
  → Prepare CSV or API script with 5 papers (2 mandatory + 3 recommended)
  → Import: python main.py --import-file data/raw/beat7_supplement.csv
  → Rerun Phase 1: python main.py --phase 1 --resume
  → Rerun Phase 2 for new papers only
  → Continue downstream phases

Step 3: Add Constitutional AI (P1-1)
  → Append to same CSV or separate import
  → Already covered by Step 2 rerun

Step 4: Deduplicate K (P1-2)
  → Edit classified.json to flag duplicates
  → Modify phase3_graph.py to filter duplicates
  → Rerun: python main.py --phase 3 --resume

Step 5: Resolve X-category (P2-1)
  → Manual review of 2 papers
  → Edit classified.json
  → Rerun: python main.py --phase 3 --resume (combined with Step 4)

Step 6: Update writing notes for Beats 5 and 6 (P2-2, P3)
  → Edit narrative_chains.json
  → Rerun Phase 3.5: python main.py --phase 3.5 --resume

Step 7: Regenerate final outputs
  → python main.py --phase 4 --resume
  → python main.py --phase 5 --resume

Step 8: Verify all fixes
  → Check evidence_sufficiency.md: no P0 flags remain
  → Check evaluation_report.md: score should stay ≥ 0.85, Beat 7 should move to adequate
  → Check corpus_by_category.md: K has ≥ 8 papers, no visible duplicates
```

---

## Expected Post-Fix State

| Metric | Current | After Fix | Target |
|---|---|---|---|
| Total papers | 133 | 138-141 | ≥130 |
| Category K count | 5 | 8-10 | ≥8 |
| Beat 7 support | 5 (weak) | 8-10 (adequate) | ≥8 |
| Beat 1 status | adequate (with false missing flag) | adequate (clean) | adequate |
| X papers | 2 | 0-2 | manage-able |
| Duplicates in K | 2 pairs | 0 pairs (flagged) | 0 active duplicates |
| Overall score | 0.853 | 0.85-0.87 | ≥0.85 |

---

## Invariants (Do Not Change)

1. **Do not re-run Phase 1 from scratch** — only --resume to add new papers
2. **Do not delete papers** — duplicates and X-category get flagged, not removed
3. **Do not modify beat definitions** — Beat 7 is already correctly defined; issue is corpus population
4. **Do not lower honesty constraints** — the 0.88 honesty score is hard-won; preserve it
5. **Do not change pruning decisions from v1→v2** — those were intentional scope decisions
