# Research Agent Canonical Standard And Architecture

更新时间：2026-04-11 20:05（America/New_York，完成 telemetry / contradiction 修复与复跑后）

本文件是 `research-agent` 的当前主文档。
它取代并整合以下旧文档中的“现行口径”：

- `README.md`
- `ARCHITECTURE_UPGRADE_NOTES.md`
- `API_CHAIN_SETUP.md`
- `HANDOFF_STATUS_2026-04-09.md`

如果这些文档与本文件冲突，以本文件为准。

## 1. 先看结论

`research-agent` 当前已经重新验证到 Phase `5`，不是“完全不能跑”的状态。
但它也不是一个“已经成熟、可以直接自动给出高可信研究空白或自动闭环决策”的系统。

当前最准确的定义是：

- 它是一个“面向既定 thesis 的证据链整理系统”。
- 它不是一个“开放式自动选题机”。
- `gap` 输出目前只能当诊断信号，不应当当最终研究结论。
- `Phase 5` 当前更像诊断与人审分流层，而不是可以全自动决定下一步的闭环控制器。

当前已复跑并验证完成的 phase：

- Phase `1`
- Phase `2`
- Phase `2.5`
- Phase `3`
- Phase `3.5`
- Phase `3.7`
- Phase `4`
- Phase `5`

当前尚未在本轮复跑中重新验证的 phase：

- Phase `3.8`

## 2. 当前项目目标

### 2.1 主目标

项目的主目标是：

- 收集、清洗、分类并组织文献证据
- 形成一条可审计的 5-beat evidence chain
- 为既定 thesis 提供可追溯的文献底盘、关系图和 narrative scaffold

### 2.2 非主目标

以下内容不再作为当前版本的主验收标准：

- 自动生成 thesis proposals
- 仅靠 graph 自动发现高可信 research gaps
- 仅靠 abstract 级抽取完成 full-text 级结论
- 要求每篇核心论文都必须具备 S2 ID

### 2.3 命名上的历史遗留

代码和文件名里仍保留了一些历史命名，例如：

- `gaps_ranked.json`
- `Gap Synthesizer`
- `score_gaps`

这些名字保留是为了兼容现有代码路径。
在当前标准下，它们的业务含义是：

- 主要承担 beat-level evidence sufficiency 诊断
- 次要承担 gap 提示
- 不代表系统已经具备成熟的 open-ended gap discovery 能力

## 3. 当前生效的标准

本节是“从现在开始应该按什么标准判断系统是否达标”。

### 3.1 系统级标准

系统级标准分成四层：

1. 可运行性：phase 能真正完成，而不是状态文件假完成。
2. 可追溯性：关键产物必须能回溯到 canonical paper identity 和来源层。
3. 证据诚实性：agent 失败、空结果、fallback 结果必须显式暴露，不能伪装成成功。
4. 适用性：输出必须服务于 5-beat thesis 证据链，而不是追求抽象上的“全能研究代理”。

### 3.2 Phase 1 标准

Phase `1` 的目标不是“把所有论文都对齐成 S2”。
Phase `1` 当前的达标标准是：

- `corpus_unified.json` 可重建
- `corpus_200.json` 可重建
- 核心语料有稳定 canonical ID
- DOI、OpenAlex、arXiv 等 source identity 被尽可能保留
- Crossref enrichment 尽可能覆盖 DOI-backed records

不再要求：

- 核心语料里的每篇论文都必须补齐 S2 ID

原因：

- DOI 已经是足够稳定的跨源权威身份
- 批量补 S2 会制造不必要的 `429` 风险

### 3.3 Phase 2 标准

Phase `2` 当前的现实标准不是“几乎没有 `X` 类论文”。
当前更合理的标准是：

- 分类能稳定完成
- 非 `X` 语料可以进入后续 phase
- `X` 和 low-confidence 结果被显式记录

当前分类仍然偏弱，这属于后续优化项，不应假装已经达到高精度标准。

### 3.4 Phase 2.5 标准

Phase `2.5` 当前分两档理解：

- 基线档：abstract-based deep extraction
- 增强档：full-text-based extraction

当前仓库在本轮验证中只达到基线档。
原因：

- `MinerU` 本地未安装
- `GROBID` 尚未接入正式 pipeline

因此当前不能把 `Phase 2.5` 的输出当作 full-text truth。

### 3.5 Phase 3 标准

Phase `3` 当前的达标标准是：

- 关系图可构建
- citation intent enrichment 可运行
- graph metrics 可导出
- agent 失败时不得标记为 completed
- knowledge graph summary 可导出

当前不以“自动识别出很多高质量 gaps”为硬标准。
因为这项能力在现阶段并不稳定。

### 3.6 Phase 3.5 / 3.7 / 4 / 5 标准

当前标准是：

- 先按“失败必须诚实暴露”的契约执行
- 再看内容质量

换句话说，现在优先级是：

- 先避免假完成
- 再提升 narrative / contradiction / evidence inventory 的质量

截至 `2026-04-10`，Phase `3.5 / 3.7 / 4 / 5` 已按这套契约重新验证通过。
这里的“通过”含义是：

- phase 能真实完成
- 输出满足最小 schema
- 不再把局部失败或 error placeholder 记成 completed

这里的“通过”不等于：

- 证据链已经足够强
- thesis 已经被文献充分支撑
- 可以直接据此写出高可信终稿

### 3.7 完成契约

从现在开始，一个 phase step 只有在满足以下条件时才算 completed：

- 核心产物文件已写出
- 产物结构满足最小 schema
- agent 没有以 error placeholder 结束

以下情况不再允许算 completed：

- `notes = "Error: ..."`
- `field_observations.error != null`
- narrative chains 全部是错误占位
- contradiction scan 存在 `scan_errors`
- reviewer results 中任何 reviewer 只返回 `{error: ...}`

当前仓库已经加入了独立 contract 校验层来执行这条规则。

## 4. 当前架构

### 4.1 端到端结构

当前推荐理解方式：

`raw retrieval -> identity normalization -> focused corpus -> classification -> deep extraction -> relationship graph -> knowledge graph -> narrative / contradiction / evidence outputs`

### 4.2 Provider 分层

#### 检索骨架

- `OpenAlex`
- `Semantic Scholar`
- `arXiv`

职责：

- 拉回候选论文
- 提供基础 metadata
- 提供部分 citation graph 能力

#### 身份权威层

- `Crossref`
- DOI normalization
- canonical identity helpers

职责：

- 统一 paper identity
- 补 DOI / publisher / retraction / license 等权威 metadata

#### 引用 fallback 层

- `OpenCitations`

职责：

- 当 S2 不稳定或无 S2 ID 时，提供 DOI-to-DOI fallback

限制：

- 只应作为 fallback
- 不应当作为主 citation graph provider

#### 推理层

- `Anthropic / Claude`
- `OpenAI Responses / GPT-5.4`

当前职责划分：

- Claude：分类、深抽取
- GPT-5.4：关系分析、gap/evidence/narrative 类 reasoning

#### 全文层

- `MinerU`
- `GROBID`

当前状态：

- `GROBID` 已装，本轮未接入 pipeline
- `MinerU` 未装

因此当前系统仍以 abstract-first 为主。

#### 可选增强层

- `Consensus`
- `Nomic`
- 未来可能接的 `scite`

当前状态：

- `Consensus` 有 scaffold，但未启用
- `Nomic` 仍属可选可视化层
- `scite` 尚未集成

### 4.3 Identity Layer

当前内部 identity 契约：

- `paperId` 是内部 canonical ID
- `source_ids` 存放外部来源 ID
- `alias_ids` 存放回查映射

优先级：

1. DOI
2. S2 ID
3. OpenAlex ID
4. arXiv ID
5. title-hash local ID

重要原则：

- 内部 graph 一律用 canonical `paperId`
- 外部 API 调用时，按 provider 取相应 source ID
- 不允许把 OpenAlex URL 直接当成 S2 lookup ID

### 4.4 Graph Layer

当前有两层图：

- `relationship_graph.json`
  - 以 paper-paper 关系为主
- `research_knowledge_graph.json`
  - 包含 paper / category / beat / source / layer / query 等 richer structure

推荐理解：

- `relationship_graph` 负责局部论证关系
- `knowledge_graph` 负责 agent navigation 和 explainability

### 4.5 State Layer

当前 state machine 仍然是 phase-based resumability。
但今后的规则必须是：

- state 只是执行状态
- 不是产物真实性的替代品

也就是说：

- `state.json` 说 completed，不代表内容质量一定达标
- 必须同时检查对应产物

### 4.6 运行稳定性层

本轮新增并验证了一个“运行稳定性层”：

- narrative / contradiction / reviewer / evaluation 现在都有最小 contract 校验
- `full_citation_map.json` 会在加载时正规化成 canonical `paperId`
- `3.5` 和 `3.7` 不再把超大候选集一次性丢给单个 prompt，而是先选高信号子集
- `3.5` 和 `3.7` 在出现截断或 timeout 信号时，会自动改用更紧凑的输入重试
- OpenAI reasoning effort 已下调到更符合当前环境稳定性的档位

## 5. 问题分类与解决路径

### 5.1 架构类问题

这类问题应通过结构重构解决，而不是换模型硬顶。

- phase 完成契约以前不诚实
- identity layer 和 provider 调用边界不够明确
- full-text layer 还没真正接入主链路
- telemetry / stats 没有真实反映 API 调用
- `Phase 5` 当前更适合作为诊断层，不适合作为自动闭环控制层

### 5.2 工具不适用

这类问题的正确解法是换工作方式，而不是继续调同一个工具。

- `OpenCitations` 不适合做主 citation graph provider
- 单次超大 prompt 不适合承担复杂 graph reasoning
- 仅靠 abstract 不适合承担 full-text 级 deep extraction

### 5.3 工具合适但能力不足

这类问题的正确解法是降级、分块、缓存或局部替换。

- `S2` 适合局部 citation / intent enrichment，但不适合大规模 identity 补全
- `Claude` 适合结构化 extraction，但 abstract-only 条件下分类与深抽取效果有限
- `GPT-5.4` 适合 JSON reasoning，但高 effort + 大 prompt 在当前环境下不稳，需要控制上下文和 effort
- `GPT-5.4` 在 `3.5 / 3.7` 这类多论文综合任务上，若不压 prompt，容易出现 timeout、`max_output_tokens` incomplete 或 JSON 截断

### 5.4 标准不合理，需要改目标

这类问题不能靠修 bug 解决，必须先改验收标准。

- 不应要求每篇核心论文都有 S2 ID
- 不应要求图必须很密
- 不应把 `gap discovery` 当当前版本的主成功标准
- 不应把 abstract-based deep extraction 当 full-text truth
- 不应继续沿用“自动 thesis proposal generator”作为主产品定义
- 不应把 `evidence_coverage >= 4/5` 解释成“论文主张已经基本成立”
- 不应把 `Phase 5` 的单次 reviewer 聚合结果当成无需人审的最终裁决

## 6. 当前已验证的真实状态

以下是 `2026-04-11 20:00` 这轮修复后的真实快照。

### 6.1 执行状态

- Phase `1`: completed
- Phase `2`: completed
- Phase `2.5`: completed
- Phase `3`: completed
- Phase `3.5`: completed
- Phase `3.7`: completed
- Phase `3.8`: pending
- Phase `4`: completed
- Phase `5`: completed

这一轮最新快照已经额外包含：

- `3.7` contradiction 输出重组
  - 现在先产出 `review_summary`
  - 再产出 `focus_summary`
  - 再给出 detailed contradictions
- `5` 的 contradiction reviewer 上下文修复
  - 不再直接截断 `contradictions.json` 的前 `3000` 字符
  - 改为吃跨 focus 的结构化摘要
- `api_client.agent_run_json` 容错增强
  - 对轻微截断或不完整 JSON 增加 repair / balanced parse
- `state.json` telemetry 修复
  - phase 结束时会把 usage delta merge 进 stats
  - 状态页不再是 token / API calls 全零

当前 `Lens` 状态：

- 当前 key 已验证可用：`Scholarly Works API` 可用
- 当前 key 未开放：aggregation 相关权限不可用
- 因此当前项目里 `Lens` 的定位仍是“精准补料层”，不是 bulk backbone

### 6.2 语料与分类

- `corpus_200.json`: `168`
- `classified.json`: `168`
- 非 `X` 论文：`163`
- `deep_extracted.json`: `163`

当前类别分布：

- `A: 29`
- `B: 15`
- `C: 19`
- `D: 14`
- `E: 24`
- `F: 17`
- `G: 12`
- `H: 10`
- `I: 12`
- `J: 11`
- `X: 5`

这说明：

- `x_ratio = 0.03`
- `category_balance = 0`
- `avg_fill_rate = 0.924`
- 噪声已经不是当前主瓶颈
- 当前剩余 coverage 缺口主要集中在 `B / D / H / J`

### 6.3 身份、权威 metadata 与图谱

当前 knowledge graph summary：

- `240` nodes
- `1170` edges

当前 `graph_metrics.json`：

- `168` nodes
- `114` edges
- `111` components
- `101` isolated nodes

当前核心语料的权威 metadata 摘要：

- `with DOI = 140`
- `with publisher = 70`
- `retracted_count = 0`

当前图的真实含义仍然是：

- 图比旧版本更诚实
- 稀疏问题依然存在
- 但现在更多是真缺桥，不是假连接

### 6.4 后半段 phase 产物

- `narrative_chains.json`
  - `5` 个 beat 全部有效输出
- `contradictions.json`
  - `37` 条 contradictions
  - `18` 条 `critical`
  - `scan_errors = []`
  - 新增 `review_summary`
  - 新增 `focus_summary`
- `evidence_inventory.json`
  - `5` 个 beat 全部有效输出
- `evaluation_result.json`
  - 已产出最终评分与动作决策

这意味着：

- `3.5` 已稳定在“可写 scaffold”层
- `3.7` 已从“能找到一些矛盾”升级为“能把主要反证按 thesis-limiter 结构组织起来”
- `4` 当前是正常成功，不再依赖 fallback 才能过线
- `5` 当前能稳定完成 reviewer + aggregate，且本轮无 reviewer disagreement

### 6.5 Beat 级支持判断

当前 `gaps_ranked.json` 的 beat judgement 是：

- Beat `1`: `strong` (`63`)
- Beat `2`: `adequate` (`24`)
- Beat `3`: `adequate` (`14`)
- Beat `4`: `adequate` (`64`)
- Beat `5`: `adequate` (`41`)

这意味着：

- Beat `1` 已经能写
- Beat `2` 仍然只能支持“部分可测 / 代理可测”的口径
- Beat `3` 仍然只能支持 `L_auth` 的 grounded synthesis framing
- Beat `4` 可以写“人类数据对某些社会性任务仍重要”，但必须承认 synthetic / AI feedback exceptions
- Beat `5` 仍只能写成 motivated proposal

### 6.6 最新 Phase 5 评分解释

以下分数是 `2026-04-11 20:00` 这轮 `telemetry 修复 + contradiction 结构修复` 之后的最新真实结果，不再沿用之前的 `0.822` 结果。

当前 `Phase 5` 的评分不是“论文质量总分”，而是“这条 evidence-chain pipeline 当前产物的可用性诊断”。

当前结果：

- `overall_score = 0.810`
- `action = done`
- `weakest_dimension = narrative`
- `needs_human_review = false`

各项分数的业务含义：

- `narrative = 0.76`
  - 含义：related-work 骨架已经可写
  - 当前问题：Beat `1` 从 collapse 跳到真实 contamination pressure 的桥仍偏硬
- `contradiction = 0.82`
  - 含义：主要反证、scope limiter、counterevidence 现在已经真正被打捞出来
  - 当前问题：最强反证虽然已被 cataloged，但还需要进一步织进 narrative 主链
- `gap = 0.88`
  - 含义：仍是最强维度，能较稳定地区分 strong / adequate / proposal-only
- `coverage = 0.78`
  - 含义：已经不再阻断验收，但 `D / H / J` 仍偏薄
- `honesty = 0.84`
  - 含义：收口已经明显变诚实
  - 当前问题：Beat `2 / 3 / 5` 仍必须继续保持谨慎口径

### 6.7 Telemetry 当前状态

最新 `state.json` stats：

- `total_api_calls_llm = 34`
- `total_api_calls_openai = 34`
- `total_api_calls_anthropic = 0`
- `total_tokens_input = 120585`
- `total_tokens_output = 168944`
- `total_tokens_used = 289529`
- `estimated_cost_usd = 2.8959`

这说明：

- `LLM` telemetry 已在真实 phase 运行中验证通过
- 最新状态页里 retrieval provider 仍是 `0`
  - 这是因为这轮真实复跑窗口是 `3.7 -> 5`
  - 不是因为 retrieval hook 没接上
- `OpenAlex` / `Lens` 的 usage hook 已通过独立轻量探针验证会记账

### 6.8 这些分数反映出的流程优势与问题

当前流程的优势：

- 已经具备稳定复跑到 `Phase 5` 的能力
- 这次分数是新框架真实跑出来的
- `telemetry` 已经不再是假零
- `contradiction` 已从刚才的 `0.58` 修回 `0.82`
- `Lens` 仍然是有效补料层
- 后半段产物已经建立在 canonical identity 之上
- `avg_fill_rate = 0.924`、`x_ratio = 0.03` 说明数据面已基本可用
- `Phase 5` 当前可以稳定给出无分歧的完成判断

当前流程的核心问题：

- 当前最弱维度已经是 `narrative`，不是 `contradiction`
- Beat `1` 仍要避免从 collapse 直接写成 web-wide contamination 已证实
- `coverage = 0.78` 说明 `D / H / J` 仍有补料空间
- `evidence_coverage = 5/5` 不能被解释成“5 个 beat 都已硬证齐全”
- `Phase 3.8` 依旧未在本轮重新验证
- retrieval telemetry 已验证代码钩子，但还没有在一次新的完整 `Phase 1` 状态页里显示出来

## 7. 文档整合规则

从现在起，建议只按以下顺序读文档：

1. 本文件
2. `README.md`
3. `RESEARCH_QUESTION.md`

其余旧文档的定位：

- `ARCHITECTURE_UPGRADE_NOTES.md`
  - 历史重构记录，不再是现行标准
- `API_CHAIN_SETUP.md`
  - 历史 API 说明，不再是现行架构总述
- `HANDOFF_STATUS_2026-04-09.md`
  - 历史交接纪要，不再是 source of truth

## 8. 需要补充的外部搜索资料

本节不是要求立刻改代码，而是给你一份“如果要补强标准、架构、工具理解，应该优先查什么”。

优先原则：

- 官方文档优先
- 原始论文或 primary source 优先
- 不要先看二手教程

### 8.1 标准类

建议搜索：

1. `systematic literature review evidence sufficiency criteria research gap identification best practices`
   目的：给“证据链是否足够”和“gap 是否可信”建立更合理的验收标准。

2. `paper screening triage relevant uncertain out-of-scope literature review workflow`
   目的：决定是否把 Phase 2 从“硬分类 A-J”改成“两步式：相关性分流 + 主题分类”。

3. `citation graph sparsity acceptable in interdisciplinary literature mapping`
   目的：决定“图很稀疏”到底是系统问题还是领域结构本身。

### 8.2 架构类

建议搜索：

1. `Semantic Scholar API rate limits official docs bulk best practices`
   目的：确认 S2 在当前项目里最合理的调用上限和缓存策略。

2. `OpenAI Responses API incomplete_details max_output_tokens reasoning official`
   目的：确认当前 `status=incomplete` 的最佳处理方式。

3. `Crossref REST API best practices doi metadata enrichment official`
   目的：补强 identity authority 层的标准和限流策略。

4. `GROBID service references doi extraction official docs`
   目的：为后续把 GROBID 真接进 pipeline 做准备。

### 8.3 工具类

建议搜索：

1. `MinerU installation macos python official`
   目的：判断是否值得把 MinerU 装进当前环境。

2. `OpenCitations API references citations reliability limitations official`
   目的：确认它在 fallback 中的边界，不再误当主 provider。

3. `Consensus API quick_search official docs`
   目的：决定 claim verification 层要不要正式启用。

4. `scite API citation statements official`
   目的：如果将来需要 support / contradict / mention stance layer，先确认接法和成本。

5. `SPECTER2 embedding API current official docs Semantic Scholar`
   目的：决定 embeddings 阶段后续是否还值得保留。

## 9. 下一步建议

当前推荐执行顺序是：

1. 先以本文件作为唯一标准和架构入口
2. 后续代码改动都以本文件为验收标准
3. 当前主目标已经达标；下一轮优先从 `narrative` 继续，而不是再回到已经修好的 `contradiction`
4. narrative 的优先改法不是“再堆论文”，而是把 Beat `1 -> 2` 的桥写得更窄、更明确
5. 如果继续补料，优先补 `B / D / H / J`
6. `B` 需要精确补 web-scale / retrieval contamination；`D/H` 需要补 post-2022 drift measurement；`J` 需要补更强的 socially grounded data-composition bridge
7. 需要在未来补做一次新的完整 `Phase 1` 复跑，把 retrieval telemetry 也真正显示到状态页里
8. 再下一步才考虑把 `Phase 2` 改成“相关性分流 + 主题分类”或加入更强 relevance gate
9. `Phase 3.8` 需要补做一次正式验证，避免文档长期遗漏
10. contradiction 层如果要继续提高，应把 curated synthetic success / alignment counterevidence 更集中写入主 stress-test 视角，而不是分散在 side notes

## 10. 一句话版本

`research-agent` 当前应被定义为：

一个以 canonical identity、knowledge graph 和 targeted retrieval 为底盘、面向既定 thesis 的 evidence-chain pipeline；它已经具备稳定复跑到 Phase `5` 的能力，最新标准对齐后整体分数为 `0.822` 并达到当前目标，但主要价值仍是“诚实诊断 thesis 哪些部分缺证据并生成可审计 scaffold”，而不是自动产出可直接提交的研究结论。
