# Research Agent 当前问题与建议

更新时间：2026-04-08（本地）  
范围：`/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent`

## 1. 当前结论

这套 `research-agent` 现在已经可以完整跑通，从 Phase 1 一直到 Phase 5 都已完成，说明项目已经脱离“环境坏了 / API 不通 / 根本跑不起来”的状态。

但它目前还没有达到“高质量 research agent”的水平。更准确地说：

- 它已经具备“自动收集文献、分类、做深抽取、组织 narrative、生成矛盾图”的能力。
- 它还不具备“高可信度地发现研究空白、稳定构建引用网络、支撑严谨 thesis 论证”的能力。

本次 fresh run 的最终评分见 [output/evaluation_report.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/evaluation_report.md)：

- `Overall score = 0.630`
- `narrative = 0.70`
- `contradiction = 0.80`
- `gap = 0.70`
- `coverage = 0.60`
- `honesty = 0.30`

系统自己的结论也是：`Action: human`，需要人工复核后再继续。

## 2. 这次 fresh run 的关键事实

### 2.1 流程状态

- Phase 1：完成
- Phase 2：完成
- Phase 2.5：完成
- Phase 3：完成
- Phase 3.5：完成
- Phase 3.7：完成
- Phase 3.8：完成
- Phase 4：完成
- Phase 5：完成

状态文件： [state.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/state.json)

### 2.2 当前语料规模

- 分类总数：`168`
- 非 `X` 论文数：`116`
- 被打到 `X` 的论文数：`52`

分类分布：

- `A: 16`
- `B: 2`
- `C: 19`
- `D: 7`
- `E: 25`
- `F: 16`
- `G: 5`
- `H: 4`
- `I: 13`
- `J: 9`
- `X: 52`

这说明 Phase 1 拉回来的候选里噪声不低，尤其 `B / H / G / D / J` 这些类偏弱。

### 2.3 图谱与引用结果

- Phase 3 初始图谱：`168 nodes / 22 edges`
- 关系分析后：`25 edges`
- 连通分量：`145`
- 孤立点：`135`

这是一个明显偏稀疏的图。

Phase 3.5 的全量引文扩展结果：

- 引文扩展论文数：`110`
- 内部引用边：`3`

文件： [data/processed/full_citation_map.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/data/processed/full_citation_map.json)

这个结果已经足够说明：当前系统的“图谱能力”不是没有，而是被 ID 对齐问题和检索纯度问题严重限制了。

### 2.4 Embedding 结果

- SPECTER2 成功嵌入的论文只有 `3` 篇
- 向量形状：`(3, 768)`

文件： [data/processed/specter_embeddings.npy](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/data/processed/specter_embeddings.npy)

这说明跨数据源的论文身份没有统一好，导致后续 embedding / 相似度 / 聚类几乎没有发挥出来。

### 2.5 输出文件已经可用

核心输出都已生成：

- [output/evidence_sufficiency.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/evidence_sufficiency.md)
- [output/writing_outline.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/writing_outline.md)
- [output/contradiction_map.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/contradiction_map.md)
- [output/evidence_inventory.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/evidence_inventory.md)
- [output/corpus_by_category.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/output/corpus_by_category.md)

分析产物：

- [analysis/gaps_ranked.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/analysis/gaps_ranked.json)
- [analysis/narrative_chains.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/analysis/narrative_chains.json)
- [analysis/contradictions.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/analysis/contradictions.json)

## 3. 现在最主要的问题

## 问题 1：前端检索能跑，但候选语料纯度不够

表现：

- `168` 篇里有 `52` 篇最终被分类为 `X`
- `B` 类只有 `2` 篇，`H` 只有 `4` 篇，`G` 只有 `5` 篇
- Beat 2 和 Beat 5 被评为 `critical_gap`

这意味着当前 Phase 1 不是真的把目标研究空间打满了，而是“拉了一批量很大但纯度一般的候选”，再靠 Phase 2 硬筛。

最典型的受害类：

- `B`：容易混入环境污染、contamination 之类不相关论文
- `H`：web quality / temporal decline 查询过宽，缺少真正的长期测量工作
- `J`：LoRA / ablation 查询会混入泛 adapter 论文
- `G`：平台设计和真实数据采集框架相关论文明显不足

对应配置文件： [config/search_queries.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/config/search_queries.json)

## 问题 2：跨源 `paperId` 没有统一，后半段能力被直接打折

这是当前最关键的技术问题。

现在项目里混用了三种身份：

- Semantic Scholar `paperId`
- OpenAlex work URL，例如 `https://openalex.org/W...`
- `arxiv:...`

Phase 3.5 和 Phase 3.8 会把这些 ID 直接拿去请求 S2，结果就是：

- 大量 OpenAlex ID 在 S2 侧直接 `404`
- 可扩展引用关系非常少
- 可取 embedding 的论文只有 `3` 篇

这不是论文本身没有引用关系，而是系统没有先做 ID 解析和统一。

高风险文件：

- [src/phase3_5_narrative.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase3_5_narrative.py)
- [src/phase3_graph.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase3_graph.py)
- [src/phase3_8_embeddings.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/phase3_8_embeddings.py)
- [src/dedup.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/dedup.py)

## 问题 3：后半段 narrative 能生成，但 graph-based gap discovery 仍然偏弱

表现：

- Narrative chains 能出 5 个 beat
- Contradiction map 能找到 `25` 条矛盾
- 但 Phase 3 的 gap synthesizer 识别出的 graph-based research gaps 是 `0`
- 图谱总体仍然稀疏，无法支撑真正强的“结构性空白发现”

这说明当前系统更擅长：

- 给定主题后组织相关工作
- 给定主题后挖论文间张力

但还不擅长：

- 自动从图谱中长出可信的 research gap

## 问题 4：`honesty` 维度很低，说明自动输出和真实证据之间还有错配风险

Phase 5 的最弱项不是 narrative，也不是 contradiction，而是 `honesty = 0.30`。

这通常意味着：

- 有些叙事是“能说通”，但证据底盘不够硬
- 某些类别里的论文虽然被分进来了，但不一定真是该命题下的核心证据
- 某些“缺失论文”其实是系统自己没检索到，不是领域里不存在

这也是为什么系统最终要求 `human review`。

## 4. API 和环境现状

## 已验证可用

- `OpenAlex`：可用
- `arXiv`：可用
- `Semantic Scholar`：带 key 可用，但会触发 `429`
- `OpenAI`：可用
- `Nomic`：可用
- `Anthropic REST`：可用

## 需要注意

### Anthropic

当前环境里，Anthropic Python SDK 直接调用会被拦：

- 现象：`PermissionDeniedError: Your request was blocked`
- 处理：已在 [src/api_client.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/api_client.py) 增加 REST fallback

所以现在 Anthropic 不是“不能用”，而是“SDK 路径有问题，REST 路径能用”。

### Semantic Scholar

不是没用到，实际上用到了，而且对 Phase 1 / 3 / 3.5 / 3.8 都很重要。  
当前问题不是 key 无效，而是：

- 速率限制会出现 `429`
- 很多论文没有先被解析为 S2 兼容 ID，导致请求质量差

### scite

当前项目里没有接入 scite。  
也就是说，即使你有会员，目前这套代码并不会调用 scite 的任何能力。

## 5. 从 thesis / research 价值角度看，这个系统现在适合做什么

现在适合：

- 快速搭建 related work 初稿
- 整理主题分块
- 找潜在矛盾论文对
- 生成第一版 evidence inventory
- 辅助你回忆项目结构、恢复上下文、快速重启文献管线

现在不适合直接拿来：

- 自动得出高可信研究空白结论
- 作为最终文献综述定稿依据
- 依赖引用图来证明理论链条严密
- 依赖 embedding 结果做深入聚类分析

## 6. 我建议的改进顺序

## 第一优先级：先修 ID 规范化

目标：让 OpenAlex / S2 / arXiv 统一到可追踪、可扩展的内部主键体系。

建议做法：

- 在 dedup 后给每篇论文保存统一结构：
  - `paperId`
  - `s2_paper_id`
  - `openalex_id`
  - `arxiv_id`
  - `doi`
- 后续凡是调用 S2 的地方，优先用 `s2_paper_id`
- 对 OpenAlex / arXiv 论文增加解析步骤，先查到可用的 S2 ID 再进入 Phase 3.5 / 3.8

不先做这个，后面 graph、embedding、citation expansion 都会继续失真。

## 第二优先级：重写检索查询，特别是 `B / H / J / G`

目标：减少 Phase 2 的无效筛除，直接提升语料纯度。

优先改这些类：

- `B`：明确限制为 AI-generated text / synthetic text pollution / detector robustness
- `H`：明确限制为 longitudinal web quality / Common Crawl quality drift / temporal degradation
- `J`：限制为 social reasoning / data composition / ablation / adaptation，不要泛化到所有 LoRA
- `G`：增加 platform design / verified data collection / human-in-the-loop data pipeline / social data collection systems

对应文件： [config/search_queries.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/config/search_queries.json)

## 第三优先级：在 Phase 1 或 Phase 2 之间加一个 relevance gate

建议在进入 Phase 2 前增加一层轻量过滤：

- 关键词黑名单
- 域外主题剔除
- 对 `B/H/J/G` 做更严格的短文本相关性判别

这样可以降低：

- `X` 比例过高
- Beat evidence 虚高
- 后面 honesty 评分偏低

## 第四优先级：补缺失的领域种子论文

当前系统自己已经指出缺口，尤其是：

- model collapse foundational papers
- empirical web decline measurement
- information theory foundations
- platform design / social data collection frameworks

建议把这些 paper 直接补进：

- [config/seed_papers.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/config/seed_papers.json)

靠纯搜索去捞这些关键论文，稳定性不如直接加种子。

## 第五优先级：再跑一次完整 fresh run

顺序建议：

1. 修 ID 规范化
2. 调整 search queries
3. 补 seed papers
4. 清理状态并 archive 当前输出
5. 从 Phase 1 重跑到 Phase 5

我预期这样做之后，最明显会改善的是：

- `X` 比例下降
- `B/H/G` 覆盖提升
- citation map 边数明显增加
- embedding 可用论文数大幅提升
- `honesty` 分数回升

## 7. 最实际的下一步建议

如果只做一件事，先做这个：

- 修跨源 ID 规范化

如果做两件事，顺序是：

1. 修 ID 规范化
2. 收紧 `search_queries.json`

如果要追求下一轮分数提升，而不是只要“能跑”，这两个是必须做的，不是可选优化。

## 8. 一句话结论

这个项目现在已经从“坏掉的半成品”恢复成“能完整执行的 research pipeline”了；但它的上限目前被两件事卡住：

- 前端检索纯度不够
- 后端跨源 ID 没统一

不先解决这两个问题，继续加模型、加 API、加 reviewer，收益都不会高。
