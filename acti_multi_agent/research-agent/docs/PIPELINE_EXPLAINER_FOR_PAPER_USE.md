# research-agent 管线讲解与论文使用说明

更新时间：2026-04-11 20:05（America/New_York）

## 1. 一句话先说清

`research-agent` 现在最准确的定位，不是“自动找研究空白并自动写论文”的全能代理，而是一个**围绕既定 thesis 组织文献证据链**的多阶段管线。

它做的核心事情是：

- 把多源检索拉回来的论文统一成可追踪语料
- 按 A-J taxonomy 做 thesis-conditioned 分类
- 抽取每篇论文对当前论题真正有用的 claim / limitation / method 信息
- 组织成 narrative、contradiction、evidence inventory、reviewer diagnostics
- 给你一个“可写、可审计、可防过度主张”的论文底盘

它不做的事情是：

- 不可靠地自动提出全新 thesis
- 不可靠地自动发现开放式 research gap
- 不把 abstract 级抽取伪装成 full-text truth
- 不把 Phase 5 分数伪装成“论文已经成立”

## 2. 大局图

端到端可以理解为：

`检索与补料 -> 身份统一 -> 分类 -> 深抽取 -> 关系图/知识图 -> narrative -> contradiction -> evidence inventory -> reviewer 评分 -> 写作产物`

系统的三类输入：

- 研究目标输入
  - 固定 thesis / 5-beat argument
  - A-J taxonomy
- 检索控制输入
  - `config/search_queries.json`
  - `config/seed_papers.json`
  - `config/lens_queries.json`
  - `config/manual_core_inclusions.json`
  - `config/manual_exclusions.json`
  - `config/manual_category_overrides.json`
- 环境与 provider 输入
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `LENS_API_KEY`
  - 以及 OpenAlex / Crossref / OpenCitations / arXiv 等 provider

系统的三类输出：

- 机器可消费的中间结果
  - `data/processed/*.json`
  - `analysis/*.json`
- 人可直接阅读的写作产物
  - `output/related_work_draft.md`
  - `output/related_work_references.md`
  - `output/writing_outline.md`
  - `output/evidence_inventory.md`
  - `output/contradiction_map.md`
  - `output/evaluation_report.md`
- 流程状态与运行统计
  - `state.json`

## 3. 核心架构

### 3.1 编排层

- `main.py`
  - 负责 phase 调度、rerun invalidation、状态输出、phase 结束后的 usage flush
- `state.json`
  - 记录 phase / step 状态、当前 phase、stats
- `src/state_manager.py`
  - 负责 state 初始化、迁移、保存、usage merge

### 3.2 provider 层

- 检索骨架
  - `OpenAlex`
  - `Semantic Scholar`
  - `arXiv`
- 精准补料层
  - `Lens Scholarly Works API`
- 身份权威层
  - DOI normalization
  - `Crossref`
- 引用 fallback 层
  - `OpenCitations`

### 3.3 推理层

- `Claude`
  - 主要做分类、深抽取
- `GPT-5.4`
  - 主要做关系分析、gap/evidence 诊断、narrative、contradiction、reviewers

### 3.4 约束层

- `src/phase_contracts.py`
  - 负责 schema / 失败占位校验
- `src/api_client.py`
  - 统一 API 调用、JSON 解析、fallback、telemetry 记账

### 3.5 产物层

- `analysis/`
  - 面向 pipeline 诊断与后续 phase
- `output/`
  - 面向人读、面向写论文

## 4. 每个 Phase 是什么

| Phase | 核心模块 | 主要输入 | 主要输出 | 作用 | 下游怎么用 |
|---|---|---|---|---|---|
| `1` | `src/phase1_corpus.py` | query、seed、manual inclusion/exclusion、provider API | `data/raw/*`、`data/processed/corpus_unified.json`、`corpus_200.json` | 拉论文、去重、统一 identity、形成候选语料 | 给 `2` 分类和后续全部 phase 作为统一语料底盘 |
| `2` | `src/phase2_extraction.py` | `corpus_200.json` | `data/processed/classified.json` | 把论文压到 A-J taxonomy，并保留 contribution / gap / confidence | 决定每篇论文进入哪个 beat、哪类证据链 |
| `2.5` | `src/phase2_5_deep.py` | `classified.json`、abstract、可选全文 | `data/processed/deep_extracted.json` | 抽 key claim / method / limitation / benchmark 等结构化字段 | 给 narrative、contradiction、gap、evidence inventory 使用 |
| `3` | `src/phase3_graph.py` | `classified.json`、deep extraction、citation map | `analysis/graph_metrics.json`、`relationship_analysis.json`、`gaps_ranked.json`、知识图摘要 | 建关系图、算图指标、做 beat-level evidence sufficiency 诊断 | 给 `3.5`、`4`、`5` 提供结构化上下文 |
| `3.5` | `src/phase3_5_narrative.py` | 分类、深抽取、graph/gap 结果 | `analysis/narrative_chains.json`、`output/writing_outline.md` | 把论文组织成 5-beat related-work scaffold | 给 `4` 写 evidence inventory，也给你写正文 |
| `3.7` | `src/phase3_7_contradiction.py` | 分类、深抽取、priority papers、focus questions | `analysis/contradictions.json`、`output/contradiction_map.md` | 强制打捞 thesis 的反证、scope tension、counterevidence | 给 Phase `5` honesty/contradiction reviewer，也给正文中的 limitations / related work counterargument |
| `3.8` | embeddings 阶段 | 当前语料 | embedding 产物 | 语义相似度补充层 | 当前轮未重验，非主路径 |
| `4` | `src/phase4_topics.py` | narrative、gap、contradiction、classified | `analysis/evidence_inventory.json`、`output/evidence_inventory.md`、`output/related_work_draft.md`、`related_work_references.md` | 形成 beat 级 conversation partners、草稿、参考文献清单 | 是你写综述正文最直接的中间台阶 |
| `5` | `src/phase5_evaluate.py`、`src/scoring.py` | 全部 analysis/output 产物 | `analysis/reviewer_results.json`、`analysis/evaluation_result.json`、`output/evaluation_report.md` | 对 narrative / contradiction / gap / coverage / honesty 五维做诊断 | 帮你决定哪里能写、哪里必须收口、哪里要补文献 |

## 5. 这些 Phase 彼此如何交互

### 5.1 数据流

- Phase `1` 先把“能用的语料池”定下来
- Phase `2` 决定每篇论文属于哪类证据
- Phase `2.5` 决定后面 reasoning 看到的是“结构化 claim”而不是杂乱 abstract
- Phase `3` 负责把“论文列表”变成“有关系、有 beat 诊断的证据网络”
- Phase `3.5` 负责“怎么讲”
- Phase `3.7` 负责“不能只讲支持，还要讲反证”
- Phase `4` 负责“把 narrative 和 contradiction 收束成可写材料”
- Phase `5` 负责“诊断这套材料是不是还在过度主张”

### 5.2 控制流

- `main.py` 按 phase 顺序运行
- 当上游 phase 被重跑时，下游产物会被失效化，避免吃旧缓存
- 每个 phase 完成前都要过 contract 校验
- phase 结束后会把 usage delta merge 到 `state.json`

### 5.3 为什么要有 `3.5 / 3.7 / 4 / 5`

如果只有检索、分类、图谱，这套系统仍然只是“找文献的工具”。

真正让它变成论文工作流的是：

- `3.5`
  - 把文献变成章节逻辑
- `3.7`
  - 把文献变成 honest related work，而不是单边辩护
- `4`
  - 把逻辑和反证变成可写材料
- `5`
  - 把“感觉能写”变成可解释诊断

## 6. 当前技术路径

当前真正生效的技术路径是：

- 检索主骨架
  - `OpenAlex + Semantic Scholar + arXiv`
- 精准补料
  - `Lens`
  - 不是 bulk backbone，而是 targeted supplement
- identity 策略
  - 以 DOI / canonical ID 为主
  - S2 ID 不再要求全覆盖
- reasoning 分工
  - Claude 负责 extraction-heavy 任务
  - GPT-5.4 负责 reasoning-heavy 任务
- extraction 路线
  - 当前仍是 abstract-first
  - `GROBID` / `MinerU` 不是当前生产主路径
- contradiction 路线
  - 先按 focus question 打捞
  - 再生成 `review_summary + focus_summary + detailed contradictions`
  - Phase `5` 的 contradiction reviewer 现在吃的是结构化摘要，不再吃被截断的原始长 JSON
- telemetry 路线
  - API client 实时累计 usage
  - phase 结束时 flush 到 `state.json`
  - LLM token/call 已在真实 phase 运行中验证
  - `OpenAlex` / `Lens` usage hook 也已通过独立轻量探针验证

## 7. 当前达到的效果

### 7.1 最新验证结果

截至 `2026-04-11 20:00` 的最新完整验证：

- 已完成：`1 / 2 / 2.5 / 3 / 3.5 / 3.7 / 4 / 5`
- 未重验：`3.8`

最新 `Phase 5` 评分：

- `overall = 0.810`
- `narrative = 0.76`
- `contradiction = 0.82`
- `gap = 0.88`
- `coverage = 0.78`
- `honesty = 0.84`
- `action = done`
- `needs_human_review = false`

当前数据面：

- `classified = 168`
- `non-X = 163`
- `x_ratio = 0.03`
- `avg_fill_rate = 0.924`

当前 contradiction 面：

- `total_found = 37`
- `critical_count = 18`
- `scan_errors = []`

当前 telemetry 状态页：

- `total_api_calls_llm = 34`
- `total_api_calls_openai = 34`
- `total_tokens_input = 120585`
- `total_tokens_output = 168944`
- `total_tokens_used = 289529`
- `estimated_cost_usd = 2.8959`

注意：

- 最新状态页里 retrieval 调用仍显示 `0`
  - 这是因为这次真实复跑窗口是 `3.7 -> 5`
  - 不是因为 retrieval telemetry 代码没接上
  - `OpenAlex` / `Lens` hook 已通过独立探针验证会记账

### 7.2 当前强项

- 系统已经能稳定跑到 Phase `5`
- 证据链已经不是“假完成”
- `contradiction` 现在不再只盯住 collapse 主张，也能显式拉出 filtered web、synthetic alignment、AI feedback 等 counterevidence
- `gap` 维度已经能稳定做“支持到哪一步”的诊断
- `x_ratio` 很低，语料噪声已明显下降
- `related_work_draft.md`、`writing_outline.md`、`related_work_references.md` 已经能直接支持写作

### 7.3 当前主要问题

- 最弱维度已经不是 contradiction，而是 narrative
  - 主要问题是 Beat `1` 从 collapse 跳到真实 web contamination pressure 的桥还偏硬
- `coverage` 虽然过线，但 `D / H / J` 仍偏薄
- Beat `2` 仍然不能写成“开放 web 已被 AI 内容确定性大规模退化”
- Beat `3` 仍然只能把 `L_auth` 写成 grounded synthesis，而不是已验证的新理论
- Beat `5` 仍然只能写成 motivated design proposal，而不是 literature-proven solution

## 8. 五个分数分别是什么意思

| 维度 | 它在评什么 | 高分意味着什么 | 当前分数在说什么 |
|---|---|---|---|
| `narrative` | 5-beat 链条是不是可读、可写、过渡自然 | 章节骨架已经接近可写综述 | `0.76` 说明主链可用，但 Beat `1 -> 2` 的桥仍要收口 |
| `contradiction` | 是否把最强反证和 scope limiter 真拉出来了 | 不是单边辩护，而是能诚实处理 counterevidence | `0.82` 说明核心反证已经被打捞出来，但还要继续把它们织进 narrative 主链 |
| `gap` | 是否诚实区分“已支持 / 部分支持 / 只能提案” | 不会把弱支持伪装成 novelty | `0.88` 是当前最稳定强项 |
| `coverage` | 类别和 beat 的料够不够 | 各 section 都有足够 conversation partners | `0.78` 说明能写，但 `D / H / J` 仍有明显补料空间 |
| `honesty` | 有没有过度主张 | final 写法不会越过 corpus 的实际支持边界 | `0.84` 说明口径已明显变诚实，但 Beat `2/3/5` 仍必须谨慎措辞 |

## 9. 你写论文时应该怎么用

### 9.1 不要直接把系统当成“自动成稿器”

最合理的用法是：

- 它负责给你证据底盘、章节骨架、反证清单、参考文献清单
- 你负责最后的论证口径、段落组织、措辞收口、主张边界

### 9.2 具体怎么用每份产物

- `output/evaluation_report.md`
  - 先看总分、最弱维度、当前还能不能继续强写
- `analysis/reviewer_results.json`
  - 直接看 reviewer 对每个维度的文字诊断，这是最重要的“写作约束”
- `output/writing_outline.md`
  - 用来定 5-beat 的章节骨架
- `output/related_work_draft.md`
  - 用来拿 paragraph scaffold 和 anchor papers
  - 不建议整段照抄，只建议改写、压缩、重组
- `output/evidence_inventory.md`
  - 用来选每个 beat 的核心 conversation partners
- `output/contradiction_map.md`
  - 用来写 limitations、counterargument、scope condition
- `output/related_work_references.md`
  - 用来准备文献列表和引用核对
- `analysis/gaps_ranked.json`
  - 用来决定哪些 beat 只能写“部分支持”

### 9.3 一个最省事的写法

建议按这个顺序写：

1. 先看 `analysis/reviewer_results.json`
   - 把 reviewer 明确禁止你过度主张的地方先记下来
2. 再看 `output/writing_outline.md`
   - 先定 5-beat 结构
3. 再看 `output/evidence_inventory.md`
   - 每个 beat 选 4-7 篇主文献
4. 再看 `output/related_work_draft.md`
   - 参考它的 paragraph scaffold 重写正文
5. 最后用 `output/contradiction_map.md`
   - 给每个关键 section 补一段 honest limitation / counterevidence

### 9.4 写作时必须保留的口径

- Beat `1`
  - 可以强写 recursive reuse / collapse 风险
  - 不要强写成“开放 web 已被证实全面污染”
- Beat `2`
  - 只能写“部分可测、代理可测、直接因果证据仍有限”
- Beat `3`
  - 只能写 `L_auth` 是 grounded synthesis
- Beat `4`
  - 必须承认 synthetic instruction / AI feedback 在某些任务上确实有效
- Beat `5`
  - 只能写 motivated design proposal

## 10. 你现在最该看哪些文件

如果你现在就开始写论文，建议按以下顺序打开：

1. `CURRENT_STATUS_AND_RECOMMENDATIONS.md`
2. `analysis/reviewer_results.json`
3. `output/evaluation_report.md`
4. `output/writing_outline.md`
5. `output/evidence_inventory.md`
6. `output/related_work_draft.md`
7. `output/contradiction_map.md`
8. `output/related_work_references.md`

## 11. 最后的判断

当前这套系统已经达到“可作为论文综述与 related work 底盘”的程度，但还没有达到“你可以完全不判断、直接照单全收”的程度。

最现实的结论是：

- 它已经足够帮你省掉大部分检索、整理、分组、反证打捞工作
- 它已经足够帮你把 thesis 收口到一个诚实可写的版本
- 它还不能替你做最后的学术判断
