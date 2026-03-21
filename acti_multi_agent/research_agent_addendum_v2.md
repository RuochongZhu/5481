# Research-Agent 优化改造 — 追加修改 V2

> 这份文档是对 `research_agent_optimization_prompt.md` 的补充，不重复已有内容。
> 覆盖：Codex 任务分配、1000篇规模评估、LightRAG 引入、本地 RAG。

---

## A. Codex 任务分配

README 中已有 `run_codex_parallel.py` 跑 6 个独立验证任务。
新增的模块中，以下任务适合交给 Codex（OpenAI）作为**交叉验证**，
不替代 Claude 的主流程，而是作为 second opinion。

### 适合交给 Codex 的任务

| 任务 | 为什么适合 Codex | 实现方式 |
|------|----------------|---------|
| /review-contradiction 的初筛 | 大量 paper pair 预筛选，找候选矛盾对 | Codex 批量跑 claim pair，标记 "可能矛盾" → Claude STORM 辩论只处理候选 |
| /review-coverage 的缺失论文检查 | "这个类别还缺什么 seminal paper" 是纯知识检索任务 | Codex 对每个类别独立检查，输出 missing_papers 列表 |
| /review-gap 的 prior work 搜索 | "有没有人做过这个" 需要广泛搜索能力 | Codex 用 web search 验证 gap 是否已被填补 |
| P2 分类审计 (已有 task 1) | 抽样检查 Claude 分类是否准确 | 保留现有 classification_audit |
| 替代 gaps 生成 (已有 task 6) | 找 Claude pipeline 遗漏的 gap | 保留现有 alternative_gaps |

### 不适合交给 Codex 的任务（必须 Claude）

| 任务 | 为什么必须 Claude | 理由 |
|------|-----------------|------|
| /review-narrative | 需要读完整 narrative_chains.json 并做深度推理 | Opus 级别推理任务 |
| /review-honesty | 需要深度理解 CampusGo 项目细节 | 需要 Claude memory 中的项目上下文 |
| STORM 辩论的裁判 Round 3 | 需要判断辩论质量 | MODEL_DEEP 任务 |
| P3.5 Narrative chain 构建 | 需要理解 200 篇论文间的逻辑关系 | 核心推理任务 |
| DSPy 优化循环 | DSPy 内部调用 Claude API | 框架绑定 |

### 更新 run_codex_parallel.py

在现有 6 个 task 基础上，新增 3 个：

```python
TASKS = {
    # 现有 6 个保留
    1: "classification_audit",
    2: "gap_novelty_check", 
    3: "campusgo_honesty_check",
    4: "methodology_feasibility",
    5: "intersection_validation",
    6: "alternative_gaps",
    
    # 新增 3 个
    7: "contradiction_prescan",      # 预筛矛盾候选对
    8: "coverage_seminal_check",     # 检查 seminal papers 是否缺失
    9: "gap_prior_work_search",      # web search 验证 gap 新颖性
}
```

**Task 7: contradiction_prescan**
```
给 Codex 所有论文的 key_claim 列表（从 extracted.json 提取）。
让它输出所有 "看起来可能矛盾" 的 claim pair。
不需要精确判断——误报没关系，漏报才有问题。
输出: candidate_contradictions.json
→ 然后 Claude 的 STORM 辩论只处理这些候选对（而不是全量 N² 对比）
这能把 STORM 辩论的 API 调用量从 O(N²) 降到 O(K)，K << N²
```

**Task 8: coverage_seminal_check**
```
给 Codex 每个类别(A-J)的名称和描述。
让它列出该领域 "任何 related work 都必须引的 seminal papers"。
对比 classified.json，输出: missing_seminal_papers.json
→ 直接喂给 /review-coverage 的 missing_seminal 字段
```

**Task 9: gap_prior_work_search**
```
给 Codex 你的精确 gap statement。
让它用 web search 尽全力找到一篇已经填补了这个 gap 的论文。
如果找到 → gap_credibility 直接降到 0.2
如果找不到 → 增加 gap 可信度
输出: gap_prior_work_result.json
```

---

## B. 规模评估：从 200 篇到 1000 篇

> 假设你说的 "增多到100篇" 实际指 1000 篇。如果确实是几百篇，
> 当前配置完全够用，以下内容可以推迟到真正需要时再实施。

### B.1 当前配置在 1000 篇时的瓶颈

| 组件 | 200 篇 | 1000 篇 | 瓶颈？ |
|------|--------|---------|--------|
| NetworkX 引用图 | 200 节点 ~1000 边 | 1000 节点 ~10000 边 | ❌ 没问题，NetworkX 轻松处理 10 万节点 |
| S2 API 调用 (引用链) | 200 次 | 1000 次 | ⚠️ 无 key: 100 req/5min，需 50 分钟。有 key: 5 分钟 |
| SPECTER2 embedding | 200 × 768 dim | 1000 × 768 dim | ❌ 没问题，768KB numpy 数组 |
| Claude 分类 (P2) | 20 batch calls | 100 batch calls | ⚠️ 成本从 $2 增到 $10 |
| Claude extraction (P2.5) | 200 calls | 1000 calls | 🔴 成本 $25-50，且耗时 2-3 小时 |
| STORM 辩论 (P3.7) | ~20 候选对 × 3 calls = 60 | ~200 候选对 × 3 calls = 600 | 🔴 需要 Codex prescan 降量 |
| Nomic Atlas 可视化 | 200 点 | 1000 点 | ❌ 免费额度 1M 点 |
| pyvis force graph | 200 节点 | 1000 节点 | ⚠️ 浏览器渲染变慢，需要用 Cosmograph 替代 |
| Reviewer 评分 (P5) | 5 reviewers × 5 beats | 5 reviewers × 5 beats | ❌ 不变，不依赖论文数量 |

**总结：200→1000 的主要问题是 API 成本和时间，不是技术架构。**

### B.2 解决方案

**P2.5 成本问题：** 1000 篇全部做 deep extraction 太贵。改为两阶段：
- 阶段一：只用 abstract 做轻量 extraction（免费，S2 API 已有 TLDR）
- 阶段二：只对 top 200 "核心论文" 做 MinerU + Claude full extraction
- 核心论文判定：citation count > 中位数 OR 被 ≥3 篇同 corpus 论文引用

**STORM 辩论成本问题：** 全量 N² 对比爆炸。用 Codex prescan（Task 7）降到 ~50-100 候选对。

**pyvis 渲染问题：** 1000 节点 pyvis 在浏览器里会卡。两个选择：
- Cosmograph（GPU 渲染，10 万节点也流畅）
- 或 NetworkX 导出 .gexf → Gephi 桌面端渲染

---

## C. 引入 LightRAG（轻量 GraphRAG）

在 200 篇时不需要。在 500+ 篇时**强烈推荐**。
不装微软官方 GraphRAG（太重），装 **LightRAG** 或 **nano-graphrag**。

### C.1 为什么是 LightRAG 而不是 Microsoft GraphRAG

| | Microsoft GraphRAG | LightRAG | nano-graphrag |
|---|---|---|---|
| 代码量 | 重型框架 | 中等 | ~1100 行 |
| 安装 | 复杂配置 | `pip install lightrag-hku` | `pip install nano-graphrag` |
| 默认存储 | 需要配数据库 | NetworkX + JSON (本地) | NetworkX + NanoVectorDB |
| LLM 要求 | GPT-4 级别 | 支持 Ollama 本地 | 支持 Ollama 本地 |
| 适用规模 | 万级文档 | 百~千级 | 百~千级 |
| 你需要它做什么 | 全局主题分析 | 全局主题分析 | 全局主题分析 |

**推荐：先用 nano-graphrag（最轻），不够再升级 LightRAG。**

### C.2 nano-graphrag 集成方案

```python
# src/graphrag_layer.py
from nano_graphrag import GraphRAG, QueryParam

def build_knowledge_graph(corpus_texts: dict[str, str], working_dir: str):
    """
    输入: {paper_id: abstract_or_fulltext} 字典
    构建知识图谱用于全局主题查询
    """
    graph = GraphRAG(
        working_dir=working_dir,
        # 用你已有的 Anthropic API
        best_model_func=your_claude_wrapper,
        cheap_model_func=your_sonnet_wrapper,
    )
    
    for paper_id, text in corpus_texts.items():
        graph.insert(text)
    
    return graph

def query_global_themes(graph, question: str) -> str:
    """全局查询：跨所有论文的主题分析"""
    return graph.query(
        question,
        param=QueryParam(mode="global")
    )

def query_local_entity(graph, question: str) -> str:
    """局部查询：特定实体/概念的细节"""
    return graph.query(
        question, 
        param=QueryParam(mode="local")
    )
```

### C.3 用在哪个 Phase

nano-graphrag 不替代你现有的 NetworkX citation graph，而是**补充语义层**：

| 你的 NetworkX 图 | nano-graphrag 图 |
|----------------|-----------------|
| 节点 = 论文 | 节点 = 概念/实体 (如 "model collapse", "RLHF") |
| 边 = A 引用了 B | 边 = 概念 X 和概念 Y 有关系 (如 "causes", "mitigates") |
| 回答: 谁引用了谁 | 回答: "model collapse 领域的主要辩论是什么" |

**插入位置：P3 之后，P3.5 之前**

```
P3: citation graph (NetworkX) — 谁引用了谁
P3.1 NEW: knowledge graph (nano-graphrag) — 概念之间什么关系  
P3.5: narrative chains (Claude Opus) — 读两个图后推理叙事
```

P3.5 的 Opus 调用现在能同时看到：
1. citation graph 告诉它 "Paper A 引用了 Paper B"
2. knowledge graph 告诉它 "两篇都讨论了 model collapse，但 A 认为它不可避免，B 认为可以通过 accumulation 条件避免"

这让 narrative chain 和 contradiction detection 都更准确。

### C.4 触发条件（不要现在装）

在 AGENT_PROMPT.md 中添加条件：

```markdown
## 何时启用 nano-graphrag
- 如果 corpus > 500 篇 → 启用 nano-graphrag layer
- 如果 /review-narrative 连续 2 次 < 0.5 且 corpus < 500 → 
  可能是语义理解不足，尝试启用
- 如果 corpus ≤ 300 篇且 narrative_score ≥ 0.6 → 不需要
```

---

## D. 本地 RAG 设置

当你的论文全文超过 Claude 的 context window（即使 1M token 也放不下
1000 篇论文的全文），你需要本地 RAG 来做按需检索。

### D.1 最轻量方案：ChromaDB + SPECTER2

```python
# src/local_rag.py
import chromadb
import numpy as np

def build_local_rag(extracted_json: str, embeddings_npy: str):
    """
    用 SPECTER2 embedding + ChromaDB 构建本地 RAG
    """
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_or_create_collection(
        name="research_corpus",
        metadata={"hnsw:space": "cosine"}
    )
    
    # 加载数据
    papers = json.load(open(extracted_json))
    embeddings = np.load(embeddings_npy)
    
    # 插入
    collection.add(
        ids=[p["id"] for p in papers],
        embeddings=embeddings.tolist(),
        documents=[p["abstract"] + " " + p.get("key_claim", "") for p in papers],
        metadatas=[{
            "category": p["category"],
            "beat": p["beat"],
            "year": p["year"],
            "title": p["title"]
        } for p in papers]
    )
    
    return collection

def query_rag(collection, question: str, n_results: int = 10, 
              filter_category: str = None) -> list:
    """
    检索最相关的论文
    """
    where_filter = {"category": filter_category} if filter_category else None
    
    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        where=where_filter
    )
    
    return results
```

### D.2 用在哪里

本地 RAG 服务于两个场景：

**场景 1：Reviewer 评分时的按需检索**
当 /review-gap 需要检查 "有没有人做过类似的工作" 时，
不把 1000 篇 abstract 全塞进 prompt，而是先 RAG 检索 top 10 最相关的，
只把这 10 篇喂给 Claude：

```python
# 在 /review-gap 调用前
relevant = query_rag(collection, gap_statement, n_results=10)
# 只把这 10 篇的 abstract + finding 喂给 Claude 评分
```

**场景 2：STORM 辩论时的证据检索**
辩论 Round 1/2 时，让 debater 能从 corpus 中找到支持自己论点的证据：

```python
# STORM debate Round 1
supporting_evidence = query_rag(
    collection, 
    paper_a["key_claim"], 
    n_results=5,
    filter_category=paper_a["category"]
)
# 把 evidence 附在 debater 的 system prompt 里
```

### D.3 依赖

```
pip install chromadb
```

ChromaDB 是纯 Python，本地文件存储，零配置。不需要 Docker 或外部服务。
SPECTER2 embedding 你在 P3.8 已经算好了，直接复用，不需要额外调 API。

---

## E. LangGraph 评估：什么时候真正需要

### E.1 当前不需要的理由

你的循环逻辑是：
```
while score < 0.8 and iteration < 10:
    weakest = find_weakest()
    if weakest == "coverage": go_back_to_P1()
    elif weakest == "narrative": go_back_to_P3_5()
    ...
```

这是 20 行 Python。LangGraph 解决的是：
- 10+ 个 agent 并行协作
- 复杂的条件分支（if/elif 超过 10 个）
- 需要持久化 state across sessions（你已经有 state.json）
- 需要 human-in-the-loop 中断点（你已经有 disagreement 检测）

### E.2 什么时候需要 LangGraph

当以下任一条件满足时引入：

```markdown
## LangGraph 触发条件
- 循环回退逻辑超过 5 个分支（当前 4 个）
- 需要 P1 和 P3 并行跑（当前是串行）
- 需要多个 Claude Code session 协作（类似 gstack Conductor 模式）
- agent loop 需要跨 session 恢复且 state.json 不够用
```

**如果到了这个阶段，推荐 LangGraph 而非 AutoGen：**
LangGraph 的 state graph 模式更适合你的 "Phase 之间有条件跳转" 结构。
AutoGen 的优势是 multi-agent debate（但你已经用 STORM 模式解决了）。

### E.3 预留接口

即使现在不装 LangGraph，也可以在代码中预留接口，
方便将来迁移。具体做法是把循环逻辑抽象成 `Router` 类：

```python
# src/router.py
class PipelineRouter:
    """
    当前: 纯 Python while/if 实现
    将来: 可以替换为 LangGraph StateGraph
    """
    def decide_next_action(self, scores: dict) -> tuple[str, dict]:
        """
        输入: 当前各维度分数
        输出: (action_name, params)
        """
        if scores["overall_score"] >= 0.8:
            return ("finish", {})
        
        weakest = min(scores, key=lambda k: scores[k] if k != "overall_score" else 1)
        
        routing_table = {
            "evidence_coverage": ("rerun_p1", {"mode": "补搜"}),
            "category_balance": ("rerun_p1", {"mode": "balance"}),
            "narrative_strength": ("rerun_p3_5", {}),
            "contradiction_awareness": ("rerun_p3_7", {}),
            "gap_credibility": ("rerun_p3", {"retry": True}),
        }
        
        return routing_table.get(weakest, ("human_review", {"reason": weakest}))
```

将来如果迁移到 LangGraph，只需要把 `routing_table` 变成 `conditional_edges`，
`PipelineRouter.decide_next_action` 变成 graph node，逻辑完全不变。

---

## F. 更新依赖列表

在 `requirements.txt` 中追加（相比上一份 prompt 新增的）：

```
# 本地 RAG
chromadb

# 轻量 GraphRAG（500+ 篇时启用）
# nano-graphrag          # 取消注释以启用
# lightrag-hku           # 备选，比 nano-graphrag 更完整
```

## G. 更新 .env

```properties
# 新增（追加到已有 .env）

# Codex 新任务
CODEX_TASKS=1,2,3,4,5,6,7,8,9

# 规模阈值
CORPUS_SIZE_THRESHOLD_FOR_GRAPHRAG=500
CORPUS_SIZE_THRESHOLD_FOR_COSMOGRAPH=500

# ChromaDB (本地，不需要外部服务)
CHROMADB_PATH=./data/chromadb
```

---

## H. 执行优先级

这份追加修改不需要全部同时实施。按优先级：

**现在就做（配合上一份 prompt 一起）：**
1. 更新 `run_codex_parallel.py` 加 Task 7/8/9
2. 实现 `src/local_rag.py`（ChromaDB + SPECTER2，10 行代码）
3. 在 AGENT_PROMPT.md 中加入规模触发条件

**500+ 篇论文时做：**
4. 安装 nano-graphrag，实现 `src/graphrag_layer.py`
5. pyvis → Cosmograph 替换
6. P2.5 改为两阶段 extraction

**循环逻辑超过 5 个分支时做：**
7. 抽象 PipelineRouter 类
8. 评估是否迁移到 LangGraph

---

*Generated: 2026-03-21 · 追加修改 V2，配合 research_agent_optimization_prompt.md 使用*
