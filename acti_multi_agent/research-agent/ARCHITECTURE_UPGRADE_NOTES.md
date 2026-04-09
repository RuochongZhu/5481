# Architecture Upgrade Notes

更新时间：2026-04-08（本地）

## 1. 这次重构解决的不是“功能缺失”，而是“中间层缺失”

原来的 `research-agent` 能跑通，但架构上有两个明显短板：

- 没有统一的论文身份层，不同来源的同一篇论文会在后续阶段被拆开。
- 没有 persistent graph layer，Phase 3 之后只有临时关系图，没有给后续 agent 提供稳定、可复用、可审计的中间知识层。

这次改动的目标不是再加一个阶段，而是把整个系统从：

`raw papers -> prompt -> outputs`

升级成：

`raw papers -> canonical identity layer -> knowledge graph layer -> wiki/report/json -> downstream agents`

## 2. 借鉴了什么

## 来自 `karpathy/autoresearch`

吸收的不是训练代码本身，而是架构原则：

- 单一优化面：把系统真正需要优化的关键面缩小，而不是每个阶段都各自定义身份和结构。
- 固定中间产物：像 `results.tsv` 那样持续累积、可比较、可回退。
- 让 agent 面向“可审计结构”工作，而不是每轮都从头扫描原始材料。

映射到本项目后，对应成：

- 统一 `paper identity` 作为单一身份层
- 导出 `research_knowledge_graph.json` / `research_knowledge_graph.md` / `knowledge_wiki/`
- 后续对 graph、embedding、narrative 的查询都基于稳定中间层，而不是重新扫 raw corpus

## 来自 `safishamsi/graphify`

吸收的是它的图层设计方法，而不是照搬代码助手技能本身：

- 先提取结构，再导出图，再做报告和 wiki
- 图里不仅放“主实体”，还放 category / query / source / rationale 之类的中间结构节点
- 让 agent 优先读取 graph report / wiki，而不是直接 grep 全量原始文件

映射到本项目后，对应成：

- 不再只保留 paper-paper 边
- 新增 category / beat / source / retrieval layer / query 节点
- 产出可供 agent 文件导航的 `output/knowledge_wiki/index.md`

## 3. 这次已经落地的改动

## 3.1 统一论文身份层

新增文件：

- [src/paper_identity.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/paper_identity.py)

新增能力：

- DOI / OpenAlex / arXiv / S2 统一抽取
- `canonical_id`
- `source_ids`
- `alias_ids`
- `get_s2_lookup_id(...)`
- `build_alias_lookup(...)`

核心原则：

- `paperId` 不再只是“当前来源给的那个 ID”
- `paperId` 现在是内部 canonical ID
- 对外部 API 请求时，单独用 `source_ids.s2` / `source_ids.openalex` / `source_ids.arxiv`

结果：

- 以后 paper-paper 关系、citation expansion、embedding fetch 不再直接依赖原始来源 ID
- 后续阶段不会因为 `paperId` 是 OpenAlex URL 就误判成“不可用于 S2”

## 3.2 dedup 从“合并 metadata”升级为“合并身份”

修改文件：

- [src/dedup.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/dedup.py)

现在 dedup 做的不只是：

- abstract/venue/year/citation 合并

还会做：

- `source_ids` 合并
- `alias_ids` 合并
- dedup 完成后重算 canonical ID

这意味着以后同一篇论文来自 OpenAlex 和 S2 时，不会再只保留一个来源的 ID。

## 3.3 Phase 1 新增“核心语料身份解析”

修改文件：

- [src/phase1_corpus.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase1_corpus.py)

新增逻辑：

- `corpus_unified.json` dedup 完成后，先选 `corpus_200`
- 只对 `corpus_200` 做缺失 S2 identity 的解析
- 优先用 DOI / arXiv 去补 `source_ids.s2`

这样做的原因：

- 不对 4k+ 全量语料做高成本解析
- 只优化真正进入后半段推理和图谱分析的核心语料

## 3.4 新增 persistent knowledge graph layer

新增文件：

- [src/knowledge_base.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/knowledge_base.py)

它导出的不再只是 paper-only graph，而是 richer graph：

- `paper` 节点
- `category` 节点
- `beat` 节点
- `source` 节点
- `layer` 节点
- `query` 节点

关系包括：

- `classified_as`
- `secondary_category`
- `supports_beat`
- `provided_record`
- `retrieved_via`
- `retrieved`
- `builds_on`
- `contradicts`
- `cites`
- `extends`

这个 graph 的目标不是“模拟文献引用数据库”，而是给 agent 一个可导航、可解释的 research map。

## 3.5 Phase 3 现在会导出图层产物

修改文件：

- [src/phase3_graph.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase3_graph.py)

新增导出：

- [data/processed/research_knowledge_graph.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/data/processed/research_knowledge_graph.json)
- [analysis/research_knowledge_graph_summary.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/analysis/research_knowledge_graph_summary.json)
- [output/research_knowledge_graph.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/research_knowledge_graph.md)
- [output/knowledge_wiki/index.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/knowledge_wiki/index.md)

这让 Phase 3 不再只是“算完 metrics 就结束”，而是真正产出一个可复用知识层。

## 3.6 Phase 3.5 / 3.8 不再直接用 `paperId` 调 S2

修改文件：

- [src/phase3_5_narrative.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase3_5_narrative.py)
- [src/phase3_8_embeddings.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase3_8_embeddings.py)

新逻辑：

- 内部 map 一律用 canonical `paperId`
- 对 S2 API 查询一律用 `get_s2_lookup_id(...)`
- S2 返回的 `paperId` 先走 alias lookup，再映射回内部 canonical ID

这一步是后半段图谱质量提升的前置条件。

## 4. 这次重构后的直接结果

在当前已有 fresh run 的基础上，我没有重跑全链路，而是直接用现有 `classified.json` 和 `relationship_graph.json` 重新导出了新图层。

结果：

- 旧 Phase 3 关系图：`168 nodes / 37 edges`
- 新 knowledge graph：`216 nodes / 933 edges`

原因不是“引用边突然变多了”，而是：

- 图里现在加入了 category / beat / query / source / retrieval layer 这些结构节点
- agent 现在可以先沿结构节点导航，再去钻到 paper 节点

这正是 graph knowledge base 的价值。

## 5. 现在这套架构更适合什么

更适合：

- 给另一个 agent / 对话提供稳定上下文层
- 用 wiki 方式让 agent 先读图摘要再下钻
- 后续接 MCP / query_graph / shortest_path 之类工具
- 做持续更新的研究库，而不是一次性批处理

不代表已经完全解决：

- 检索 query 纯度
- S2 解析覆盖率
- 研究 gap 的真实性
- thesis honesty 分数偏低

但它已经把这些问题从“系统性耦合”变成了“局部可优化问题”。

## 6. 下一步最合理的演进

按优先级建议：

1. 把 `research_knowledge_graph.json` 暴露成 query 接口或 MCP server
2. 让后续对话优先读 [output/research_knowledge_graph.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/research_knowledge_graph.md) 和 [output/knowledge_wiki/index.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/knowledge_wiki/index.md)
3. 再回头收紧 `config/search_queries.json`
4. 再做一次从 Phase 1 开始的全量 fresh rerun

## 7. 一句话总结

这次不是给项目“多加一个 graph 功能”，而是把原来散落在各阶段里的结构信息，收束成了一个可持久化、可查询、可审计、可被 agent 消费的中间知识层。
