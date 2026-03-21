# Research Agent System Blueprint
## 200-Paper Literature Analysis Pipeline for PhD Topic Determination

**Purpose**: Hand this document to Claude Code for local execution. All tool choices, API endpoints, workflow logic, prompt templates, and bottleneck mitigations are specified below.

**Research Domain**: AI data quality / model collapse / synthetic data contamination / data authenticity — with CampusGo as a potential case study lens.

---

## Part 1: Tool Chain Architecture

### 1.1 Input Layer — Discovery & Search

**Primary tools (by capability tier):**

| Tool | What It Does | Why Use It | API / Access | Cost |
|------|-------------|-----------|--------------|------|
| **Undermind** | Mimics human researcher: iterative keyword + citation + semantic search, adapts as it finds relevant papers. Classifies every paper as highly relevant / related / ignorable. Estimates total relevant papers ("discovery curve"). | Best exhaustive search available. 10x more relevant results than Google Scholar (whitepaper-verified). Finds papers keyword search misses. | Web UI at undermind.ai; no public API yet, export CSV/BibTeX/RIS | $16/mo Pro |
| **OpenAlex** (主力检索) | 2.5亿+ works，完全开放REST API，无需Key。返回title/abstract/citations/concepts/topics。支持filter链式查询、分页、聚合统计。 | 比S2更开放（无认证即可高频调用），数据覆盖更全（含专利、会议、预印本），原生支持institution/concept/topic聚合。只需在请求中加`mailto`参数即可进入"polite pool"（更快响应）。 | `api.openalex.org/works?search={q}&mailto=your@email` | Free |
| **Semantic Scholar** (citation图谱补充) | 200M+ papers，无认证版限速1次/秒。TLDR摘要、citation graph traversal（引用/被引）是S2独有优势。 | OpenAlex的citation关系数据不如S2精确。用S2专门做citation chain expansion（给定paper → 拉references/citations）。不用于批量搜索。 | `api.semanticscholar.org/graph/v1/paper/{id}` — 无需Key，`time.sleep(3)` + 指数退避 | Free |
| **arXiv API** (前沿预印本) | 完全开放，无需Key。返回详尽摘要和元数据。你的研究领域95%+高价值论文首发arXiv。 | 抓最新预印本（OpenAlex/S2收录有1-2周延迟）。先用arXiv扫荡最前沿，再用其他工具补充已发表论文。 | `export.arxiv.org/api/query?search_query={q}&max_results=100` | Free |
| **Elicit** | Semantic search + structured data extraction from papers. Define custom columns (method, finding, limitation, gap) and it extracts from up to 1,000 papers. 99.4% extraction accuracy (VDI/VDE benchmark). | Does 80% of the per-paper analysis work. Exports structured tables directly. | Web UI at elicit.com; no public API. Export CSV. | $12/mo Plus |
| **ResearchRabbit** | Citation network visualization. Input seed papers → expands outward via citation/co-citation. Integrates with Zotero. Acquired by Litmaps. | Best for snowball discovery from known papers. Free, fast, reliable. | Web UI, free tier, Zotero integration | Free |
| **Connected Papers** | Generates visual similarity graph from one seed paper. Shows Prior Works and Derivative Works. | Quick visual of the field landscape around one key paper. | Web UI, 5 free graphs/month | Free |
| **Scite** | Shows whether citations support, contrast, or merely mention a claim. | Essential for understanding debate structure between papers. | Web UI + API (`scite.ai/api`) | $20/mo |

**Programmatic检索引擎三层架构 (无需任何API Key):**

| 层级 | 引擎 | 用途 | 限速策略 |
|------|------|------|---------|
| **Layer 1: OpenAlex** (主力) | 批量语义搜索 + 元数据拉取 + concept聚合 | 加`mailto=`参数进入polite pool (~10次/秒)；否则~1次/秒但仍可用 |
| **Layer 2: S2** (图谱) | 给定paperId → 拉references + citations chain | 无认证1次/秒，脚本中`time.sleep(3)` + 429指数退避 |
| **Layer 3: arXiv** (前沿) | 搜最新预印本（<3个月），抓最前沿论文 | 无限速，但建议`time.sleep(3)`避免被ban |

**本地RAG可选增强 (Phase 2之后):**

| Tool | What It Does | How to Integrate |
|------|-------------|------------------|
| **OpenAlex abstracts + vector embeddings** | 从OpenAlex拉200篇摘要 → `text-embedding-3-large`或`voyage-3`做embedding → 存ChromaDB → 支持语义相似度检索和gap question answering | 成本极低（~$0.02 for 200 abstracts），但只在你需要对corpus做自然语言QA时才值得搭建 |
| **NotebookLM** (Google) | Upload all PDFs → grounded Q&A only from your corpus. No hallucination beyond sources. | Free. Use after collecting papers, for synthesis queries. Cannot search externally. |

### 1.2 Processing Layer — Analysis & Relationship Mapping

**Per-paper analysis (structured extraction):**

| Field to Extract | Tool | Prompt/Method |
|-----------------|------|---------------|
| **Research question** | Elicit custom column | "What is the primary research question?" |
| **Method** | Elicit custom column | "What method/approach is used? (e.g., theoretical proof, simulation, empirical study, survey)" |
| **Key finding** | Elicit custom column | "What is the main result/finding in one sentence?" |
| **Limitation** | Elicit custom column | "What limitations do the authors acknowledge?" |
| **Research gap identified** | Elicit custom column | "What future work or open questions do the authors identify?" |
| **Dataset used** | Elicit custom column | "What dataset(s) or data source(s) are used?" |
| **Theoretical framework** | Elicit custom column | "What theoretical framework or formalism is used?" |

**Cross-paper relationship mapping:**

| Tool | What It Maps | Output Format |
|------|-------------|---------------|
| **Litmaps** | Citation network + temporal evolution. X-axis = year, Y-axis = citation count. Identifies clusters and isolated nodes. | Interactive web graph; export as image/BibTeX |
| **Inciteful** | Multi-seed iterative expansion. Shows "Most Important Papers in the Graph", "Similar papers", "Review papers". Exposes SQL queries for reproducibility. | Web UI, exportable |
| **Connected Papers** | Co-citation similarity graph. Papers closer together share more citation overlap. | Web graph, 5/month free |
| **VOSviewer** | Full bibliometric mapping. Term co-occurrence maps, citation coupling, co-citation networks. Most flexible. Accepts Scopus/WoS/Crossref input. | Standalone Java app, free. Input CSV/BibTeX. |
| **Scite** | Citation context analysis: which papers support vs. contradict each other | Web UI + API |
| **Custom: Claude + Elicit CSV** | After Elicit extraction, feed the full structured CSV to Claude with specific prompts (see Part 3) to identify logical gaps, contradictions, and unexplored intersections. | Claude Code + exported CSV |

### 1.3 Persistence Layer — Long-Running Execution

**The 10-hour problem and solutions:**

The core challenge: Claude Code's context window (~200K tokens) compacts after extended sessions, losing detailed state. Three proven solutions:

**Solution A: Agent Loop Pattern (Carlini approach)**
From Anthropic's own C compiler experiment (16 agents, 2,000 sessions, $20,000):
```bash
#!/bin/bash
# Run in a Docker container, NOT your main machine
while true; do
  COMMIT=$(git rev-parse --short=6 HEAD)
  LOGFILE="agent_logs/agent_${COMMIT}.log"
  claude --dangerously-skip-permissions \
    -p "$(cat AGENT_PROMPT.md)" \
    --model claude-opus-4-6 &> "$LOGFILE"
done
```
The agent reads a task file, does work, commits to git, and the loop restarts with fresh context. State is persisted in files and git, not in the context window.

**Solution B: Agent Teams (Claude Code v2.1.32+, Opus 4.6)**
Multiple Claude instances work in parallel on a shared repo. One acts as team lead, others as specialists. Coordination via git-based mailbox system. Each agent has its own 1M-token context window.

**Solution C: Ruflo Context Autopilot**
Third-party orchestration tool that manages context window automatically — archives, compresses, and restores conversation context. Prevents the "context cliff" where Claude loses early-conversation details.

**Recommended for research pipeline: Solution A + file-based state**
Each loop iteration: read `state.json` → do next task → update `state.json` → commit → restart.

---

## Part 2: Execution Workflow (Step-by-Step)

### Phase 1: Seed Corpus Assembly (Day 1, ~4 hours)

**Step 1.1: Define search queries**

Start with 5 seed papers you already know:
```
1. Shumailov et al. 2024 Nature — model collapse
2. Alemohammad et al. 2024 ICLR — MAD
3. Dohmatob et al. 2024 ICML — tail collapse phase transition
4. Gerstgrasser et al. 2024 arXiv — accumulation principle
5. Briesch et al. 2023 EMNLP — LLM entropy deficit
```

**Step 1.2: Expand via citation network**
- Input all 5 seeds into **ResearchRabbit** → collect forward and backward citations
- Input each seed into **Connected Papers** → capture the similarity clusters
- Run **Undermind** search with: "model collapse training data synthetic contamination entropy degradation data quality authenticity verification" → let it run its full iterative process (~8-10 min)

**Step 1.3: Programmatic三层检索 (全部无需API Key)**

**Layer 1 — OpenAlex 主力批量搜索 (polite pool):**
```python
"""
OpenAlex批量检索 — polite pool模式
只需在请求中加 mailto= 参数即可获得更高频率响应 (~10 req/s)
无需注册、无需Key
"""
import requests, time, json

MAILTO = "your_email@cornell.edu"  # 替换为你的邮箱，进入polite pool
BASE = "https://api.openalex.org/works"

queries = [
    "model collapse generative AI training data",
    "synthetic data contamination language model",
    "AI generated text detection entropy",
    "data provenance verification machine learning",
    "training data quality authentication",
    "information entropy text generation diversity",
    "federated learning data integrity verification",
    "platform design authentic behavioral data",
    "retrieval augmented generation data pollution",
    "self-consuming generative models autophagy",
]

all_papers = {}

for q in queries:
    cursor = "*"
    page = 0
    while cursor:
        params = {
            "search": q,
            "filter": "from_publication_date:2020-01-01,type:article|preprint",
            "select": "id,doi,title,publication_year,cited_by_count,authorships,primary_location,abstract_inverted_index,concepts",
            "sort": "cited_by_count:desc",
            "per_page": 100,
            "cursor": cursor,
            "mailto": MAILTO,
        }
        resp = requests.get(BASE, params=params)
        
        if resp.status_code == 429:
            wait = 2 ** (page + 1)
            print(f"  Rate limited, backing off {wait}s...")
            time.sleep(wait)
            continue
        
        data = resp.json()
        for work in data.get("results", []):
            oa_id = work["id"]
            if oa_id not in all_papers:
                # 还原inverted index为摘要文本
                abstract = ""
                if work.get("abstract_inverted_index"):
                    inv = work["abstract_inverted_index"]
                    word_positions = []
                    for word, positions in inv.items():
                        for pos in positions:
                            word_positions.append((pos, word))
                    word_positions.sort()
                    abstract = " ".join(w for _, w in word_positions)
                
                all_papers[oa_id] = {
                    "openalex_id": oa_id,
                    "doi": work.get("doi"),
                    "title": work.get("title"),
                    "year": work.get("publication_year"),
                    "cited_by_count": work.get("cited_by_count"),
                    "authors": [a["author"]["display_name"] for a in work.get("authorships", [])[:5]],
                    "venue": work.get("primary_location", {}).get("source", {}).get("display_name") if work.get("primary_location") else None,
                    "abstract": abstract,
                    "concepts": [c["display_name"] for c in work.get("concepts", [])[:5]],
                    "query_source": q,
                }
        
        cursor = data.get("meta", {}).get("next_cursor")
        page += 1
        if page >= 3:  # 每个query最多300篇，避免噪声
            break
        time.sleep(0.15)  # polite pool下足够安全
    
    print(f"Query '{q[:40]}...' done. Total unique: {len(all_papers)}")

# 保存
with open("data/raw/openalex_results.json", "w") as f:
    json.dump(list(all_papers.values()), f, indent=2, ensure_ascii=False)

print(f"\nTotal unique papers: {len(all_papers)}")
```

**Layer 2 — Semantic Scholar citation chain expansion (sleep hack):**
```python
"""
S2 citation图谱扩展 — 无需API Key
用途：给定一批paperId，拉取它们的references和citations，发现OpenAlex可能遗漏的关联论文
限速：无认证 1 req/sec，用 time.sleep(3) + 指数退避确保稳定
"""
import requests, time, json

S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"

def s2_get_with_backoff(url, params, max_retries=5):
    """带指数退避的S2请求"""
    for attempt in range(max_retries):
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            wait = 3 * (2 ** attempt)  # 3s, 6s, 12s, 24s, 48s
            print(f"  429 Too Many Requests. Backing off {wait}s (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
        else:
            print(f"  Error {resp.status_code}: {resp.text[:100]}")
            return None
    print(f"  Max retries exceeded for {url}")
    return None

def expand_citations(paper_id, direction="references"):
    """拉取一篇论文的references或citations"""
    fields = "paperId,title,year,citationCount,venue,abstract"
    url = f"{S2_BASE}/{paper_id}/{direction}"
    data = s2_get_with_backoff(url, {"fields": fields, "limit": 100})
    time.sleep(3)  # 核心：每次请求后强制等3秒
    if data:
        return [item.get("citedPaper" if direction == "references" else "citingPaper", {}) 
                for item in data.get("data", [])]
    return []

# 对seed papers和top-cited papers做citation expansion
seed_ids = [
    "603d3f90fc40f79ff51258f0295de3ec5107f73e",  # Shumailov 2024 Nature
    # ... 其他seed paper的S2 paperId
]

citation_papers = {}
for sid in seed_ids:
    for direction in ["references", "citations"]:
        papers = expand_citations(sid, direction)
        for p in papers:
            pid = p.get("paperId")
            if pid and pid not in citation_papers:
                citation_papers[pid] = p
        print(f"  {sid[:12]}... {direction}: found {len(papers)} papers")

with open("data/raw/s2_citation_expansion.json", "w") as f:
    json.dump(list(citation_papers.values()), f, indent=2, ensure_ascii=False)

print(f"\nCitation expansion found {len(citation_papers)} additional papers")
```

**Layer 3 — arXiv 前沿预印本扫荡:**
```python
"""
arXiv API 预印本搜索 — 完全开放，无需Key
用途：抓最前沿的预印本（<6个月），OpenAlex/S2收录有延迟
"""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, time, json

ARXIV_BASE = "http://export.arxiv.org/api/query"

queries = [
    'all:"model collapse" AND all:"training data"',
    'all:"synthetic data" AND all:"generative model" AND all:"contamination"',
    'all:"data authenticity" AND all:"language model"',
    'all:"self-consuming" AND all:"generative"',
    'all:"entropy" AND all:"AI generated text"',
]

arxiv_papers = {}

for q in queries:
    params = urllib.parse.urlencode({
        "search_query": q,
        "start": 0,
        "max_results": 100,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_BASE}?{params}"
    
    response = urllib.request.urlopen(url)
    root = ET.fromstring(response.read())
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    
    for entry in root.findall("atom:entry", ns):
        arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
        if arxiv_id not in arxiv_papers:
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            arxiv_papers[arxiv_id] = {
                "arxiv_id": arxiv_id,
                "title": entry.find("atom:title", ns).text.strip().replace("\n", " "),
                "abstract": entry.find("atom:summary", ns).text.strip().replace("\n", " "),
                "authors": authors[:5],
                "published": entry.find("atom:published", ns).text[:10],
                "categories": [c.attrib["term"] for c in entry.findall("atom:category", ns)],
                "query_source": q,
            }
    
    print(f"arXiv query done. Running total: {len(arxiv_papers)}")
    time.sleep(3)  # arXiv建议间隔3秒

with open("data/raw/arxiv_results.json", "w") as f:
    json.dump(list(arxiv_papers.values()), f, indent=2, ensure_ascii=False)

print(f"\narXiv total: {len(arxiv_papers)} preprints")
```

**Step 1.3.4: 三源合并去重:**
```python
"""
合并 OpenAlex + S2 citation expansion + arXiv → 去重 → unified corpus
去重策略：DOI精确匹配 > 标题Jaccard相似度 > 0.8
"""
import json, re
from collections import defaultdict

def normalize_title(t):
    return re.sub(r'[^a-z0-9\s]', '', t.lower()).split()

def jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa or not sb: return 0
    return len(sa & sb) / len(sa | sb)

# Load all three sources
with open("data/raw/openalex_results.json") as f: oa = json.load(f)
with open("data/raw/s2_citation_expansion.json") as f: s2 = json.load(f)
with open("data/raw/arxiv_results.json") as f: ax = json.load(f)

# Unified schema
corpus = {}
doi_index = {}

def add_paper(paper, source):
    doi = paper.get("doi", "").strip().lower() if paper.get("doi") else None
    title = paper.get("title", "")
    if not title: return
    
    # DOI dedup
    if doi and doi in doi_index:
        return  # already have it
    
    # Title dedup
    norm = normalize_title(title)
    for existing in corpus.values():
        if jaccard(norm, normalize_title(existing["title"])) > 0.8:
            return  # duplicate
    
    uid = f"{source}_{len(corpus)}"
    corpus[uid] = {
        "uid": uid, "source": source,
        "title": title, "doi": doi,
        "year": paper.get("year") or paper.get("publication_year"),
        "authors": paper.get("authors", []),
        "venue": paper.get("venue"),
        "abstract": paper.get("abstract", ""),
        "cited_by_count": paper.get("cited_by_count") or paper.get("citationCount", 0),
        "openalex_id": paper.get("openalex_id"),
        "s2_id": paper.get("paperId"),
        "arxiv_id": paper.get("arxiv_id"),
    }
    if doi: doi_index[doi] = uid

for p in oa: add_paper(p, "openalex")
for p in s2: add_paper(p, "s2")
for p in ax: add_paper(p, "arxiv")

with open("data/processed/corpus_merged.json", "w") as f:
    json.dump(list(corpus.values()), f, indent=2, ensure_ascii=False)

print(f"Merged corpus: {len(corpus)} unique papers")
print(f"  from OpenAlex: {sum(1 for v in corpus.values() if v['source']=='openalex')}")
print(f"  from S2 expansion: {sum(1 for v in corpus.values() if v['source']=='s2')}")
print(f"  from arXiv: {sum(1 for v in corpus.values() if v['source']=='arxiv')}")
```

**Step 1.4: Screen to ~200 papers**
- Use **Elicit** to import the full candidate list
- Filter: relevance > moderate, year ≥ 2020, citationCount > 5 (or year ≥ 2024 for recent)
- Manual review of borderline cases

**Target output**: ~200 papers in a BibTeX/CSV file with title, authors, year, venue, abstract, paperId.

### Phase 2: Structured Extraction (Day 2, ~4 hours)

**Step 2.1: Elicit batch extraction**
- Upload all 200 papers to Elicit
- Define 7 custom extraction columns (see table in 1.2)
- Run extraction → export CSV

**Step 2.2: Scite citation context**
- For the top 50 most-cited papers in your corpus, run Scite queries
- Record: which papers support each other, which contradict, which just mention
- This gives you the "debate structure" of the field

**Step 2.3: Classify papers into categories**
Feed the Elicit CSV to Claude with this prompt:

```
You are analyzing a literature corpus of ~200 papers on AI data quality and model collapse.

Given this CSV of extracted paper data, classify each paper into exactly ONE primary category 
and up to TWO secondary categories from this taxonomy:

PRIMARY CATEGORIES:
A. Model Collapse Theory — papers proving/characterizing model collapse mechanisms
B. Synthetic Data Detection — papers on detecting AI-generated vs human content
C. Data Provenance & Verification — blockchain, federated learning, data integrity
D. Information-Theoretic Analysis — entropy, divergence, distributional analysis of text
E. Platform Design & Data Generation — platforms, systems, or architectures for authentic data
F. Mitigation Strategies — approaches to prevent or reverse model collapse
G. Empirical Measurement — benchmarks, datasets, and empirical studies of data quality

For each paper output:
- paperId
- primary_category (A-G)
- secondary_categories (up to 2, or "none")
- one_sentence_contribution: what this paper uniquely adds
- builds_on: list of paperIds in this corpus that this paper directly builds on
- contradicts: list of paperIds it contradicts or challenges (if any)
- gap_it_leaves: what question this paper does NOT answer
```

### Phase 3: Relationship Graph & Gap Analysis (Day 3, ~6 hours)

**Step 3.1: Build relationship graph**

Using the `builds_on` and `contradicts` fields from Phase 2.3, construct a directed graph:

```python
import networkx as nx
G = nx.DiGraph()
for paper in papers:
    G.add_node(paper['id'], category=paper['primary_category'], 
               title=paper['title'], year=paper['year'])
    for ref in paper['builds_on']:
        G.add_edge(ref, paper['id'], type='builds_on')
    for ref in paper['contradicts']:
        G.add_edge(ref, paper['id'], type='contradicts')

# Find: 
# 1. Papers with high in-degree but low out-degree → foundational papers
# 2. Papers with high out-degree → survey/synthesis papers
# 3. Isolated clusters → disconnected subfields (potential bridging opportunities)
# 4. Category pairs with no edges between them → unexplored intersections
```

**Step 3.2: Identify gaps via category intersection analysis**

Feed the graph structure to Claude:

```
Here is a directed graph of 200 papers classified into categories A-G.

For each pair of categories (A,B), (A,C), ... (F,G):
1. How many papers bridge these two categories?
2. What is the logical connection that SHOULD exist between them?
3. Is there a specific research question that sits at their intersection but has no paper?

Also identify:
- Which papers are "orphans" (no builds_on links to other papers in corpus)?
- Which categories have the least recent papers (potential stale areas)?
- Where does the field disagree? (contradicts edges)
- What is the most-cited gap (most frequently appearing gap_it_leaves)?

Output a ranked list of the top 10 research gaps with:
- Description of the gap
- Which categories it bridges
- Which existing papers are closest to addressing it
- Estimated feasibility (does the methodology exist to address this?)
- How CampusGo's data could contribute (if at all — be honest, say "no connection" if there isn't one)
```

**Step 3.3: Validate gaps against Undermind**
For each of the top 5 gaps, run a targeted Undermind search to confirm no one has addressed it. If a paper exists, downgrade the gap and promote the next candidate.

### Phase 4: Topic Determination & Thesis Framing (Day 3-4)

**Step 4.1: Score candidate topics**

For each validated gap, evaluate:

| Criterion | Weight | Question |
|-----------|--------|----------|
| Novelty | 0.25 | Has this exact question been addressed? (Undermind confirms no) |
| Feasibility | 0.25 | Can you execute this within a PhD timeline with available data/compute? |
| Advisor alignment | 0.20 | Does it fit the research interests of target advisors (Xubo Yue, etc.)? |
| CampusGo relevance | 0.15 | Can CampusGo data actually contribute? (Honest assessment, not forced) |
| Publication potential | 0.15 | Can this produce 2-3 papers at good venues? |

**Step 4.2: Generate thesis statement variants**

For the top 3 scoring topics, Claude generates:
- One-sentence thesis statement
- 3-paragraph research proposal sketch
- Expected contribution to the field
- Methodology outline
- List of 5-8 papers that would form the "direct conversation partners"

---

## Part 3: Prompt Templates for Claude Code Agents

### Agent 1: Literature Scanner
```
SYSTEM: You are a literature analysis agent. You read academic paper metadata
(title, abstract, year, venue, citation count) and make classification decisions.

You NEVER fabricate paper details. If you don't know something, say "unknown".
You cite papers by their paperId only.

Your classification taxonomy:
A. Model Collapse Theory
B. Synthetic Data Detection
C. Data Provenance & Verification
D. Information-Theoretic Analysis
E. Platform Design & Data Generation
F. Mitigation Strategies
G. Empirical Measurement

For each paper, output JSON:
{
  "paperId": "...",
  "primary_category": "A",
  "secondary_categories": ["D"],
  "one_sentence_contribution": "...",
  "builds_on": ["paperId1", "paperId2"],
  "contradicts": [],
  "gap_it_leaves": "..."
}
```

### Agent 2: Relationship Analyst
```
SYSTEM: You analyze relationships between academic papers. You receive a 
structured dataset of papers with their classifications and extracted data.

Your job: identify logical connections, contradictions, and gaps.

Rules:
- A "gap" must be specific enough to be a research question, not a vague direction
- "Contradicts" means the papers reach opposing conclusions on the same question
- "Builds on" means the later paper explicitly uses results/methods from the earlier one
- Be conservative: don't invent connections that aren't supported by the abstracts
- When in doubt, mark as "possibly related" not "builds on"

Output a relationship graph as an edge list with typed edges.
```

### Agent 3: Gap Synthesizer
```
SYSTEM: You synthesize research gaps from a corpus analysis. You receive:
1. A classified paper corpus with per-paper extraction
2. A relationship graph with typed edges
3. Category intersection statistics

Your job: identify the most promising research gaps.

Rules:
- A gap must be at the intersection of at least 2 categories
- A gap must be validated: no existing paper in the corpus addresses it
- Rank gaps by: specificity × novelty × feasibility
- For each gap, identify the 3 closest existing papers (the "conversation partners")
- Be honest about whether CampusGo data is relevant to each gap
- Distinguish between "gap because no one thought of it" (good) and 
  "gap because it's not interesting" (bad) — look at citation patterns for signal
```

---

## Part 4: Bottleneck Analysis & Mitigation Checklist

### Known bottlenecks and fixes:

| # | Bottleneck | Severity | Mitigation |
|---|-----------|----------|------------|
| 1 | **Context window exhaustion** — Claude loses state after ~200K tokens in a long session | Critical | Use Agent Loop Pattern (Part 2). Persist all state in `state.json` and git. Each loop iteration starts fresh with file-based context. |
| 2 | **Elicit extraction quality on niche papers** — extraction columns may return "N/A" for papers outside Elicit's training distribution | Medium | For papers where Elicit fails, fall back to Claude direct PDF analysis. Upload PDF → ask extraction questions directly. Budget ~30 sec per paper. |
| 3 | **Undermind arXiv bias** — Undermind primarily searches Semantic Scholar, which has strong STEM coverage but weaker social science/humanities coverage | Low (for this topic) | Supplement with direct Google Scholar searches for "data authenticity" + "platform design" papers that may appear in HCI or STS venues. |
| 4 | **Citation graph incompleteness** — papers < 6 months old may have zero citation links | Medium | Use Semantic Scholar's "references" field (what the paper cites) rather than "citations" (who cites it) for recent papers. Forward citations lag by 6-12 months. |
| 5 | **Forced CampusGo relevance** — tendency to make every gap about CampusGo whether warranted or not | High | Agent 3 prompt explicitly requires honest assessment. If a gap has "no connection" to CampusGo, say so. Better to have a strong thesis with weak CampusGo tie than a weak thesis with forced CampusGo tie. |
| 6 | **Duplicate papers across tools** — same paper found by Undermind, S2 API, ResearchRabbit, etc. | Low | Deduplicate by DOI (primary) or title similarity (Jaccard > 0.8 on lowercased tokens) as fallback. |
| 7 | **API rate limits** — OpenAlex polite pool: ~10 req/s with mailto; S2无认证: 1 req/s; arXiv: 无硬限但建议3s间隔 | Low | OpenAlex加mailto即可高频。S2用`time.sleep(3)`+指数退避。arXiv加3s间隔。三层引擎互为fallback——任何一个被限速，切换到另一个继续。无需申请任何API Key。 |
| 8 | **Classification consistency** — Claude may classify the same paper differently if asked twice | Medium | Run classification twice with temperature=0. Flag any papers with disagreement for manual review. Use JSON mode for structured output. |
| 9 | **Entropy/divergence computation** — if you want to actually compute D_KL or TTR on CampusGo data, you need sufficient text data | High (if pursuing this) | CampusGo needs significant user-generated text volume. If chat data is sparse, this metric is unreliable. Assess data volume before committing to this angle. |
| 10 | **Advisor alignment blind spot** — gap analysis doesn't account for what target PhD advisors actually care about | High | After gap identification, cross-reference each candidate topic against target advisors' recent publications (last 3 years). Use S2 API to pull their paper list. |
| 11 | **Overreliance on citation-based tools** — citation tools miss very recent papers and papers from adjacent fields that don't cite each other | Medium | Complement citation-based discovery (ResearchRabbit, Connected Papers) with semantic search (Elicit, Undermind) for each identified gap. These two approaches are orthogonal — use both. |
| 12 | **Loop drift** — in long-running agent loops, Claude may gradually shift focus away from the original research question | Medium | Every loop iteration re-reads the original `RESEARCH_QUESTION.md` file and checks progress against `state.json` checklist. Include explicit "Am I still on track?" self-check in the agent prompt. |

### Quality checkpoints:

| After Phase | Check | Pass Criteria |
|------------|-------|---------------|
| Phase 1 | Coverage | ≥ 200 unique papers, ≥ 5 per category (A-G), ≥ 30% from last 2 years |
| Phase 2 | Extraction completeness | < 10% "N/A" on any extraction column; 0 fabricated citations |
| Phase 2 | Classification consistency | < 5% disagreement on double-classification run |
| Phase 3 | Graph connectivity | No category pair with zero edges (would indicate search gap, not research gap) |
| Phase 3 | Gap validation | Every top-5 gap confirmed "not addressed" by targeted Undermind search |
| Phase 4 | Advisor alignment | Every top-3 topic has ≥ 2 points of intersection with a target advisor's work |
| Phase 4 | Honesty check | CampusGo relevance rated honestly for each topic, including "no connection" options |

---

## Part 5: File Structure for Claude Code

```
research-agent/
├── AGENT_PROMPT.md              # Main agent loop prompt (reads state.json, does next task)
├── RESEARCH_QUESTION.md         # Original research direction — never modified by agent
├── state.json                   # Current progress: which phase, which step, what's done
├── config/
│   ├── search_queries.json      # All search queries for S2 API
│   ├── seed_papers.json         # 5 seed papers with paperIds
│   └── advisor_papers.json      # Target advisor publication lists
├── data/
│   ├── raw/
│   │   ├── openalex_results.json    # Layer 1: OpenAlex批量搜索结果
│   │   ├── s2_citation_expansion.json  # Layer 2: S2 citation chain expansion
│   │   ├── arxiv_results.json       # Layer 3: arXiv前沿预印本
│   │   ├── undermind_export.csv     # 手动: Undermind导出
│   │   ├── researchrabbit_export.bib  # 手动: ResearchRabbit导出
│   │   └── elicit_extraction.csv    # 手动: Elicit结构化提取
│   ├── processed/
│   │   ├── corpus_merged.json       # 三源合并去重后的统一语料
│   │   ├── corpus_200.json          # 筛选后的200篇最终语料
│   │   ├── classified.json          # With categories and relationships
│   │   └── relationship_graph.json  # Edge list
│   └── pdfs/                        # Downloaded PDFs for direct analysis
├── analysis/
│   ├── category_stats.json
│   ├── intersection_matrix.json
│   ├── gaps_ranked.json
│   └── candidate_topics.json
├── output/
│   ├── literature_map.html      # Visual relationship graph
│   ├── gap_analysis_report.md
│   └── thesis_proposals.md
└── agent_logs/                  # One log per loop iteration
```

---

## Part 6: Cost & Time Estimate

| Item | Cost | Time |
|------|------|------|
| Undermind Pro (1 month) | $16 | — |
| Elicit Plus (1 month) | $12 | — |
| Claude Pro (you have this) | $20 | — |
| Claude API for agent loops (~50 iterations × ~100K tokens) | ~$15-30 | — |
| OpenAlex API | Free (无需Key，加mailto即polite pool) | — |
| Semantic Scholar API | Free (无需Key，sleep hack) | — |
| arXiv API | Free (完全开放) | — |
| ResearchRabbit / Connected Papers / Litmaps | Free tier | — |
| **Total cost** | **~$63-78** | — |
| Phase 1: Discovery | — | ~4 hours |
| Phase 2: Extraction | — | ~4 hours |
| Phase 3: Analysis | — | ~6 hours |
| Phase 4: Topic selection | — | ~2 hours |
| **Total time** | — | **~16 hours across 3-4 days** |

For the 10-hour continuous run option: use the Agent Loop Pattern (Part 2, Solution A) for Phases 2-3. Budget ~$30-50 in API costs for a full automated run.
