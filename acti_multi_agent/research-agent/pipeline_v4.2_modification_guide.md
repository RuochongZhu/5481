# Research-Agent Pipeline v4.2 修改指南

> **作用**：把 pipeline 对齐到 paper outline v4.2。核心改动由问卷真实数据揭示的 driver 子集 rating-fairness asymmetry 触发（新增 F6），并叠加 v4.1 遗留的 E 类真空、I 类未核实、edge 密度偏低三个结构性问题。
>
> **对齐文档**：`paper_outline_v4.2.md`
>
> **执行方式**：本文档中五条提示词（Prompt A–E）按顺序由本地 AI 执行，每条独立。每条提示词后附**验收标准**和**失败模式**。
>
> **版本**：v4.2
> **创建日期**：2026-04-22

---

## Part 0. 执行概览

### 0.1 修改动机（三来源）

1. **来自 v4.1 遗留**：E 类完全空（3 篇 proxy-level 不算 native）、I 类未核实、edge 密度偏低。
2. **来自问卷真实数据**：driver 子集 (N≈19) 的 rating-fairness asymmetry 比全样本更强，论文 Beat 5 升级为核心发现，触发 H 类细分补强。
3. **来自大纲结构调整**：Part 5 对齐表新增 `min_edges_per_chain` 硬指标，倒逼 edge extraction。

### 0.2 执行顺序（固定）

```
A (E 类 manual)  →  B (I 类核查)  →  E (H 类细分)  →  C (query expansion)  →  D (edge extraction)
   ↑                                                 ↑
   解决 coverage 硬洞                                 解决 density 问题
```

**为什么是这个顺序**：
- A、B、E 动论文池本身 → 先跑，避免后续重跑浪费预算
- C 扩 query 是全类别扫描，需要在 manual inclusions 进入后跑，避免重复手工 vs 自动
- D 必须最后跑，因为它处理的是"已确定的 corpus 之间"的关系，池还在变动时跑是无效劳动

### 0.3 总 API 预算估算

| Prompt | 估算调用 | 估算成本（USD） | 预计时长 |
|--------|---------|---------------|---------|
| A | ~40 次 Crossref/OpenAlex 查询 + 15 次 LLM 审核 | $2–4 | 30–60 分钟 |
| B | ~30 次检索 + 10 次 LLM 审核 | $1.5–3 | 30 分钟 |
| E | ~50 次检索 + 20 次 LLM 审核 | $3–5 | 45 分钟 |
| C | 视 query 扩展倍数，~200–400 次 API | $15–30 | 1–2 小时 |
| D | 全量 edge extraction，~N² / 2 对比较 | $20–40 | 2–4 小时 |
| **合计** | | **$40–80** | **4–8 小时** |

### 0.4 验收总闸（跑完 D 之后检查）

| 指标 | v4.1 当前 | v4.2 目标 | 硬失败阈值 |
|------|----------|----------|-----------|
| E 类 native 论文数 | 0 | ≥ 4 | < 3 |
| I 类 native 论文数 | 未核实 | ≥ 3 | < 2 |
| H 类细分 driver-subgroup 文献 | 0 | ≥ 2 | 0 |
| Total corpus 增长 | base | +40–60% | +20% 以下 |
| 平均每篇 outgoing edge | 未测 | ≥ 4 | < 3 |
| Chain 内 edge 数（每条）| 未测 | ≥ 8 | < 6 |
| CONTRADICTION edge 总数 | 未知 | ≥ 15 | < 10 |
| Phase 5 reviewer coverage 分 | 未知 | ≥ 0.85 | < 0.75 |

---

## Part 1. Prompt A — E 类 Manual Inclusion

### 1.1 背景

E 类 = `.edu` / campus-scoped identity verification as trust primitive。

automated retrieval 返回 0 篇 native。现有 3 篇被 pipeline 打成 `documented` 的是 proxy-level（不是 .edu 原生研究，只是身份验证的一般性讨论）。继续推 retrieval pipeline 不会变好——这不是 pipeline bug，是 retrieval target 本身不存在于 automated discoverable 集合里。**E 类文献散落在 HCI / CSCW / EDM / Social Computing 的 case study 里，关键词召回率极低**。

手工 DOI 挖掘是唯一路径。

### 1.2 完整提示词

````
任务：为 research-agent pipeline 的 config/manual_core_inclusions.json::papers[]
补充 E 类（.edu / campus-scoped identity verification as trust primitive）
的真实原生文献 DOI，至少 4 篇，目标 6 篇。

当前问题：E 类 retrieval 为 0，现有 3 篇是 proxy-level（非 .edu 原生）。
继续跑 automated retrieval 无效，因为 E 类文献多以 case study 形式散落在
HCI / CSCW / EDM 会议，关键词召回率极低。

检索方向（按优先级）：

1. Nicole B. Ellison 团队关于大学 .edu 平台的早期研究：
   - 2007 JCMC "Benefits of Facebook 'friends': Social Capital and
     College Students' Use of Online Social Network Sites"
     （college students + SNS 身份）
   - 2011 New Media & Society "Negotiating Privacy Concerns and Social
     Capital Needs in a Social Media Environment"
   - 2014 CHI "Social Capital and Resource Requests on Facebook"
   请返回 DOI 并在 rationale 字段说明为什么对 .edu-scoped identity 相关。

2. 校园专属匿名 / 半匿名平台研究（Yik Yak、Juicy Campus、College ACB）：
   - Black, Mezzina, Thompson 等关于 Yik Yak 的 CHI/CSCW 论文
   - Schlesinger, Edwards, Grinter 2017（关于 race / identity on Yik Yak）
   - 任何 2014–2018 关于 campus-bounded anonymous platforms 的实证研究

3. 大学邮箱作为 gating 机制的论文：
   - 搜索 "edu email" "university email verification" "campus-bounded"
     "institutional identity" + HCI/CSCW/CHI/IS venue
   - 教育科技领域的 LMS 身份验证相关 case study

4. 邻域 trust primitive 的 .edu-adjacent 论文：
   - Donath 身份与 signaling 理论（可作为理论底盘）
   - Resnick & Kuwabara 关于 reputation system 的经典，若在大学情境应用过

输出格式（追加到 manual_core_inclusions.json::papers[]）：
[
  {
    "doi": "10.xxxx/xxxxx",
    "title": "论文标题",
    "authors": ["姓, 名"],
    "year": 2007,
    "venue": "JCMC",
    "category": "E",
    "rationale": "为什么算 E 类而非 proxy；具体引到大纲哪一段（Beat 3 ¶1）",
    "manual_inclusion_reason": "E category retrieval returned 0 native papers;
                                 this paper is cited explicitly in paper outline
                                 v4.2 §2.3 as anchor for identity primitive"
  }
]

硬约束：
- 每篇论文必须通过 Crossref 或 OpenAlex 校验 DOI 有效，不接受猜测 DOI
- 只接受 peer-reviewed 会议 / 期刊，不接受 arXiv preprint 和 workshop short paper
- 每篇必须在 rationale 里明确说为什么是 "native E" 而不是 proxy
- 若某方向找不到真正 native 文献，明确报告"方向 X 无 native 文献"，
  不得用 proxy 凑数

同时产出一份 short audit note 写入 config/e_category_audit.md，说明：
- 哪些候选论文被考察过但被拒（及拒绝理由）
- 最终塞入的论文的类别归属信心分（0-1）
- 对 Beat 3 ¶1 措辞的建议：若只凑到 N 篇 native，¶1 应该用多强的表述
  - 若 N≥5：标准 primitive 措辞
  - 若 N=3–4：降级为 "institutional identity scoping with .edu as one instance"
  - 若 N<3：标注为 "under-investigated primitive"，变成论文动机的一部分
````

### 1.3 验收标准

| 检查项 | 通过标准 |
|-------|---------|
| manual_core_inclusions.json 追加条目数 | ≥ 4（硬失败 <3）|
| 每条 rationale 明确说为什么 native | 100% |
| DOI 通过 Crossref/OpenAlex 校验 | 100%，无效 DOI 立即剔除 |
| e_category_audit.md 的措辞建议分档 | 必须给出 N=3–4/N=5+/N<3 三档 |
| 被拒绝候选的拒绝理由明确 | 每个拒绝候选至少一句话说为什么 |

### 1.4 失败模式

1. **"找不到 native 但不敢报告零"**：若四个方向都 0 命中，不得伪造或降标准。直接报告"E 类无 native literature available"，触发**大纲升级**：把 E 类文献稀薄作为论文 contribution 的一部分（"under-investigated primitive"）。
2. **DOI 猜测**：任何未经 Crossref/OpenAlex 验证的 DOI 一律拒绝。LLM 容易编造看似合理的 DOI（特别是 2007 年之前的老文章），必须 verify。
3. **类别 inflation**：把 proxy-level 再次塞进来并打 E 标签，只为满足数量。rationale 字段要明确抗拒这种动作。

---

## Part 2. Prompt B — I 类核查与补强

### 2.1 背景

I 类 = super-app / integrated community platform。

Beat 2 ¶3 的论证（"校园多模块集成设计空间"）依赖 I 类。v4.1 诚实纪律说"若 I 类薄，¶3 降级为 initial inquiry"——这是事后补救。v4.2 要先验证 I 类实际覆盖，再决定 ¶3 措辞档位。

### 2.2 完整提示词

````
任务：检查 I 类（integrated community platform / super-app）retrieval 结果
是否足够支撑论文大纲 §2.2 ¶3 的"校园多模块集成设计空间"论证。若不足，
走和 E 类相同的 manual inclusion 流程。

检查标准（按大纲要求）：
- 至少 3 篇原生（非 proxy）integrated platform 论文
- 其中至少 1 篇聚焦 closed-community 或 bounded-scope，不能全是大众市场
  super-app（微信 / Grab / Gojek）
- 至少 1 篇在 HCI / CSCW venue，与 design research 社区对话

若不满足上述标准，按优先级挖 DOI：

1. 校园 / 工作场景的多模块平台 HCI 研究：
   - 任何关于 enterprise all-in-one platform（Slack + integration）的 CSCW 研究
   - 关于 higher-ed platforms (Canvas、Blackboard 扩展模块化) 的 learning at scale
     / L@S 研究
   - 校友 / 学生自建 integrated tool 的 case study

2. Super-app 文献中接近 closed-community 的：
   - 韩国 KakaoTalk 的封闭社交圈研究
   - 日本 LINE 的 bounded-community 模块研究
   - 印度 / 东南亚 bounded-user super-app 的 HCI 研究

3. Sociotechnical 理论底盘：
   - infrastructure studies (Star, Bowker) 视角下的 integrated platform 论文
   - platform studies 视角下的 modularity 讨论

输出格式和硬约束同提示词 A，但 category 字段 = "I"。

额外产出 config/i_category_audit.md，回答一个问题：
"若 I 类最终只有 N 篇 native 文献，Beat 2 ¶3 的 claim 应该用多强的措辞？
 给出 N=2 / N=3 / N=5 三档的具体措辞建议。"

硬约束：
- 大众市场 super-app（WeChat / Grab / Gojek）的一般性研究不算 native I 类，
  因为它们和 CampusRide 的 closed-community 封闭 scope 不对应
- 若方向 1 完全无结果，这本身是重要信号——把"校园多模块集成"作为
  under-theorized space 写入 gaps_ranked.json（但不得在论文里作为
  contribution 主卖点，违反 §6.3 诚实纪律）
````

### 2.3 验收标准

| 检查项 | 通过标准 |
|-------|---------|
| 现有 I 类 retrieval 覆盖核查 | 必须 explicit 报告当前 N |
| 若 N < 3，manual 补到 ≥ 3 | hard requirement |
| closed-community 聚焦论文 ≥ 1 篇 | hard requirement |
| HCI/CSCW venue 论文 ≥ 1 篇 | hard requirement |
| i_category_audit.md 三档措辞建议 | 必须给出 |

### 2.4 失败模式

1. **大众 super-app 伪装成 I 类**：WeChat / Grab / Gojek 的论文**不是** native I 类，因为 CampusRide 是 bounded-scope 校园平台，不是大众市场产品。rationale 要明确抗拒这种 inflation。
2. **enterprise collaboration 文献被当成 I 类**：Slack / Microsoft Teams 的集成研究与 campus multi-module 有相似性但不完全对应。允许引用但必须在 rationale 里说明"methodological parallel, not direct precedent"。

---

## Part 3. Prompt E — H 类细分：Driver Subgroup Sensitivity

### 3.1 背景（v4.2 新增）

问卷真实数据显示：

| 容忍项 | Driver/Both 子集 (N=19) | Rider-only 子集 (N=12) |
|-------|----------------------|---------------------|
| 迟到 | 47.2 | 35.7 |
| 改目的地 | 41.4 | 19.6 |
| **不公平评分** | **29.1** | 22.4 |
| 改路线 | 52.3 | 33.2 |

rating-fairness asymmetry 只在 driver 子集内显著存在。论文 Beat 5 升级为"**driver subgroup-specific** rating-fairness finding"。这要求 H 类文献能支撑两条更细颗粒的 claim：

- **Claim X1**：Rating sensitivity 在 active drivers vs passive raters 之间有差异，不是对称现象
- **Claim X2**：Amateur / occasional drivers（不是职业 gig worker）也会表现出 rating anxiety

当前 H 类文献（Rosenblat & Stark、Lee et al.）聚焦 Uber/Lyft **全职** gig worker，无法直接支撑 X2。必须补强。

### 3.2 完整提示词

````
任务：问卷子集分析揭示 rating-fairness asymmetry 只在 Driver/Both 子集
(N=19) 成立，Rider-only 子集 (N=12) 不成立。论文 Beat 5 要以此作为
核心 finding，但需要 H 类（peer rating / algorithmic management）文献
支撑以下两条更细颗粒的 claim：

Claim X1: "Rating sensitivity 在 active drivers vs passive raters 之间
          是有差异的，不是对称现象"
Claim X2: "Amateur / occasional drivers (not professional gig workers)
          也会表现出 rating anxiety——这不是全职劳动议价的产物"

当前 H 类文献（Rosenblat & Stark、Lee et al.）主要聚焦 Uber/Lyft 全职
司机，无法直接支撑 X2。需要检索并补充以下方向文献，每个方向 1–2 篇：

方向 1（支撑 X1）：区分 driver vs passenger perspective 的 rating 研究
- 搜索 "two-sided rating asymmetry" / "driver vs passenger rating bias"
- Platform-side literature 比 labor-side literature 更可能涵盖这个区分
- 可查 Fradkin, Grewal, Holtz 等做 marketplace trust 的经济学文献（谨慎
  引——经济学框架和 HCI 框架对 "fairness" 定义不同）

方向 2（支撑 X2）：非职业 / 兼职 / 偶发司机的 rating 经验
- 搜索 "occasional drivers" "part-time rideshare" "peer-to-peer ride"
  + rating / fairness
- BlaBlaCar 相关 peer-to-peer carpool 研究（不是职业 gig）特别相关
- 搜索 Facebook 共乘群 / Meetup 类 informal mobility coordination 的
  rating 研究

方向 3（防御性 scoping）：rating asymmetry 在小样本下的 robustness
- 搜索 "small sample rating study" + methodology discussion
- 目的：为 Beat 7 "Sample Skew" adversarial 段提供防御文献
- 非 strict 相关，引 1 篇即可

硬约束：
- 所有检索结果经 relevance 审核后，rationale 字段必须明确说：
  "supports claim X1 / X2 / X3 because ..."
- 若某方向找不到真正相关的文献，明确报告"方向 N: no suitable match"，
  不用邻域文献硬凑
- 若方向 2 确实找不到 P2P carpool 的 rating 文献，这本身是个 gap，
  记入 pipeline 的 gaps_ranked.json（诊断信号，但不写进论文作为
  "我们发现了 gap"——这违反 §6.3 的诚实纪律）

输出：
- 追加到 manual_core_inclusions.json::papers[] 格式同提示词 A
- 新增 config/h_category_subgroup_audit.md：三个方向的检索结果 +
  rationale + 每篇文献如何被 cite 到 Beat 5 / §5.8.3 / Beat 7 的
  具体段落

额外动作（重要）：
这次 manual inclusion 的条目，在 category 字段除了主类别 "H"，还需要加
secondary label "H-subgroup" 或 "H-amateur"，以便 pipeline 的 Phase 2.5
deep extraction 能识别出"这些是为支撑 X1/X2 专门引入的"，在后续 Phase 3
relationship graph 里，这些论文需要和 F5 evidence inventory 建立
强 edge（weight=1.0）。
````

### 3.3 验收标准

| 检查项 | 通过标准 |
|-------|---------|
| 方向 1 文献数 | ≥ 1 |
| 方向 2 文献数 | ≥ 1（硬失败 = 0，因 X2 完全无文献支撑会削弱 Beat 5）|
| 方向 3 文献数 | ≥ 1 |
| secondary label "H-subgroup" 标记 | 100% |
| 每篇 rationale 明确 supports X1/X2/X3 | 100% |
| 若方向 2 = 0，gaps_ranked.json 对应条目 | 必须写入 |

### 3.4 失败模式

1. **把全职 gig worker 文献伪装成 amateur driver 文献**：这是最容易犯的错——Rosenblat & Stark、Lee et al. 看起来和 "driver rating anxiety" 话题相关，但它们讨论的是**职业** gig worker，不能直接支撑 X2。rationale 必须 explicit 区分。
2. **方向 2 完全真空但继续推 pipeline**：若 P2P carpool 的 rating 文献真的不存在（很可能的情况），必须停下来告诉大纲端，这会影响 Beat 5 ¶2 的措辞。v4.2 大纲已预留"即便缺 X2 支撑文献"的 fallback 措辞档，但 pipeline 必须 explicit 报告这个缺失。

---

## Part 4. Prompt C — Retrieval Query Expansion

### 4.1 背景

Phase 1 Corpus Assembly 的 query strategy 偏窄。总论文量和跨类别 edge density 都不足。这一步提升总量 + 创造跨类别桥接，为 Phase 3 的 edge extraction 铺料。

**注意**：必须在 A、B、E 完成之后跑。因为 manual inclusions 也会影响 C 的去重逻辑。

### 4.2 完整提示词

````
任务：Phase 1 Corpus Assembly 的 query strategy 目前偏窄，总论文量和
cross-category edge density 都不足。做一次 query expansion pass，目标
将总 corpus 从当前量级提升 40–60%（但不牺牲类别相关性）。

执行步骤：

1. 打开 config/retrieval_queries.json（或等价 query config 文件），导出
   当前每个类别（A–J）的所有 query string。

2. 对每个类别做以下扩展：
   a) 同义词替换：从 anchor paper 的 keywords field 抽取 top-5 non-query
      terms，组成新 query。例：若 H 类原 query 是 "rating fairness gig
      worker"，anchor paper keyword 里有 "algorithmic management"、
      "platform labor"、"worker voice"，则生成三条新 query。
   b) 跨类别桥接 query：生成显式跨类别组合 query，例：
      - "international student AND rideshare" (C × F)
      - "campus identity AND peer rating" (E × H)
      - "gamification AND shared mobility" (G × F)
      - "peer-to-peer carpool AND rating"   (F × H，为 X2 支撑)
      - "institutional identity AND trust primitive" (E × 通用)
      这些 query 的结果允许被多个类别同时吸收（pipeline 已有 multi-label
      support），是 edge density 提升的主要来源。
   c) 时间窗口拓展：当前若 2019–2024，扩到 2014–2025；对 H 类和 C 类
      尤其重要（经典文献都在更早时间段）。对 E 类可扩到 2007–2025，
      因为 Ellison 团队的 .edu 文献多在 2007–2014 时段。

3. 重新跑 Phase 1，将新增论文 flag 为 query_expansion_batch_{date}。

4. 跑一次 Phase 2 classification，但对这批新论文设置 stricter threshold：
   相关性分 < 0.7 的直接丢弃（expansion 不等于降质量）。

5. 产出报告 reports/query_expansion_report.md：
   - 每类别新增论文数
   - 跨类别 multi-label 论文数（这是 edge 的温床）
   - 拒绝率（质量 gatekeeping 证据）
   - 新增论文里有多少是 manual inclusion 能替代的（避免重复劳动）

硬约束：
- 不得降低 Phase 2 classification 的 relevance threshold 去硬凑数量
- 跨类别 bridge query 必须是"两类别的 legitimate intersection"，不得虚构
  关系（例："rideshare AND education" 就不是 legitimate，因为两者语义没有
  自然交集）
- 新 query 总数上限 = 当前 query 数 × 2，避免 API 预算爆炸
- 和 A/B/E 引入的 manual inclusions 做 DOI 级去重，不得重复
````

### 4.3 验收标准

| 检查项 | 通过标准 |
|-------|---------|
| 总 corpus 增长 | +40–60%（硬失败 <20%）|
| 跨类别 multi-label 论文 | ≥ 15 篇（edge 温床）|
| Phase 2 拒绝率 | 10–30%（太低说明质量闸没开，太高说明 query 不精）|
| 新 query 总数 | ≤ 原 query 数 × 2 |
| 和 manual inclusions DOI 去重 | 0 重复 |

### 4.4 失败模式

1. **为凑数量放宽 relevance threshold**：v4.1 诊断报告里已经指出 pipeline 有过"降阈值硬凑"倾向。v4.2 必须严守 0.7 threshold。
2. **bridge query 虚构交叉**：LLM 容易生成语义上不合理的跨类别组合（"rideshare AND education"）。每条 bridge query 必须人工或 second-pass LLM 审核 legitimacy。

---

## Part 5. Prompt D — Edge Extraction 提升

### 5.1 背景

v4.1 诊断：relationship graph edge density 偏低，Phase 5 coverage 分上不去。

问题不在论文数（A/B/E/C 已解决），而在 extraction prompt 太保守——只抓了显式 citation relation，没抓 conceptual / methodological / contradictory / temporal relation。

**必须最后跑**——在 A/B/E/C 全部完成、corpus 稳定后。

### 5.2 完整提示词

````
任务：Phase 3 Relationship Graph 当前 edge density 偏低。问题不在论文数，
而在 extraction prompt 太保守——只抓了显式 citation relation，没抓
conceptual / methodological / contradictory relation。

修改 Phase 3 的 edge extraction prompt，加入以下四类 edge：

1. CONCEPTUAL_OVERLAP edge：
   两篇论文讨论同一 design primitive 或同一 sociotechnical phenomenon，
   但来自不同 category 或 venue。例：一篇 E 类 .edu identity 论文和一篇
   H 类 peer rating 论文都讨论"institutional scaffold of trust"，算一条
   CONCEPTUAL_OVERLAP edge。

2. METHODOLOGICAL_MIRROR edge：
   两篇论文用相似方法（formative survey + design case、qualitative
   interview + system build），即使研究主题不同也算一条 edge，
   weight=0.5。这对 §3 Methodology 的文献支撑很关键。

3. CONTRADICTION edge（已有但可能被 underused）：
   检查现有 contradictions.json，把每个 focus 的支撑论文两两连
   CONTRADICTION edge，确保 contradiction map 在 relationship graph 里
   有 visible footprint。

4. TEMPORAL_SUCCESSION edge：
   A 论文（2015）提出 concept X，B 论文（2022）批评 / 扩展 concept X，
   即使 B 不显式引 A，也算 TEMPORAL_SUCCESSION edge。这对 Beat 3 和
   Beat 7 的 "algorithmic management 批评谱系"非常重要。

修改后的 extraction prompt 结构（伪代码）：

For each pair (paper_i, paper_j) where i < j in same or related category:
  - Check CITATION edge (existing logic)
  - Check CONCEPTUAL_OVERLAP: shared keywords >= 3 AND shared
    sociotechnical frame
  - Check METHODOLOGICAL_MIRROR: both have "formative survey" OR
    both have "design case study" OR both have "system + evaluation"
  - Check CONTRADICTION: if both appear in same contradictions.json focus
  - Check TEMPORAL_SUCCESSION: year diff >= 3 AND one keyword in other's
    abstract

Target metric：
- 平均每篇论文 >= 4 条 outgoing edge
- 每个 narrative_chain 支撑论文之间 >= 8 条 edge（对应大纲 Part 5 新增
  min_edges_per_chain 指标）
- CONTRADICTION edge 总数 >= 15（对应 Beat 7 的 5 focus × 3 edges）

H-subgroup 特殊处理：
- A/B/E 里标记为 "H-subgroup" 的 manual inclusions，和 Phase 4
  evidence_inventory[4]（F5 的证据清单）之间必须建立强 CONCEPTUAL_OVERLAP
  edge（weight=1.0）。这一条 edge 是 Beat 5 driver-subgroup finding 的
  文献锚，不能漏。

输出：
- 更新后的 relationship_graph.json
- 一份 edge density diff report：每类 edge 增加多少，哪些 chain 的密度
  从 X 提升到 Y
- 抽样 10 条新生成的 edge 人工审查，report 误判率

硬约束：
- 不得为凑数量而降低 edge semantic 质量——每条 new edge 必须能用一句话
  解释关系
- CONCEPTUAL_OVERLAP 的 "shared keyword >= 3" 不接受 stopword 或泛义词
  （如 "user"、"study"、"design"），必须是领域特定术语
- 保留旧版 relationship_graph.json 做 A/B 比较（命名为
  relationship_graph_v4.1_backup.json）
````

### 5.3 验收标准

| 检查项 | 通过标准 |
|-------|---------|
| 平均每篇 outgoing edge | ≥ 4（硬失败 <3）|
| 每条 chain 内 edge | ≥ 8（硬失败 <6）|
| CONTRADICTION edge 总数 | ≥ 15（硬失败 <10）|
| H-subgroup 与 F5 evidence 的强 edge | 必须存在 |
| 抽样 10 条 edge 误判率 | ≤ 20%（硬失败 >30%）|
| 备份文件存在 | relationship_graph_v4.1_backup.json |

### 5.4 失败模式

1. **CONCEPTUAL_OVERLAP 的 keyword 匹配被 stopword 污染**：如果把 "user"、"study"、"system" 算作 shared keyword，会产生大量虚假 edge。必须用领域特定术语过滤。
2. **TEMPORAL_SUCCESSION 把无关旧论文连到新论文**：时间差 ≥ 3 年是必要条件但不充分，还必须有 keyword 重叠。
3. **不跑备份就直接改**：如果 extraction 出问题需要回滚，没有 v4.1 backup 会非常痛苦。备份是硬要求。

---

## Part 6. 每个 Prompt 的产出应该如何注入 Paper

这张表说明 pipeline 产出到 paper outline v4.2 的具体映射。跑完每个 Prompt 后用这张表检查是否真的让论文支撑变硬。

| Prompt | 产出 | 对应 paper 段落 | 验证方式 |
|--------|-----|---------------|---------|
| A | E 类 manual inclusions + e_category_audit.md | §2.3 Beat 3 ¶1 Identity primitive | §2.3 ¶1 至少 2 篇 E 类 citation |
| A | 若 E 类 N<3 的 fallback 建议 | §2.3 ¶1 措辞档位选择 | 看 audit.md 的 N 区间推荐措辞 |
| B | I 类 manual inclusions + i_category_audit.md | §2.2 Beat 2 ¶3 integrated platform 论证 | §2.2 ¶3 至少 2 篇 I 类 citation |
| E | H-subgroup manual inclusions | §4.2 Beat 5 ¶2（driver 子集 finding）、§5.8.3 | §4.2 ¶2 至少 1 篇支撑 X2 citation |
| C | 总 corpus +40–60%、multi-label 论文 | 全论文 References 分布 | Reference 总数、类别分布 |
| D | relationship_graph.json 增强 | §6.1 图示、§6.2 audit trail | Phase 5 coverage 分 ≥ 0.85 |

---

## Part 7. Pipeline 跑完之后的整合步骤

跑完 A–E 之后，按以下顺序执行最后的整合：

### 7.1 重新跑 Phase 2.5 Deep Extraction

对所有 manual inclusions（A、B、E 引入的）和 query expansion 引入的新论文做 deep extraction，抽取：
- key findings
- methodology
- design implications
- limitations

### 7.2 重新跑 Phase 3.5 Narrative Chains

基于新的 corpus 和新的 edge graph，regenerate narrative chains [0]–[6]（对应 Beat 1–7）。重点检查 chain[2]（Beat 3）和 chain[4]（Beat 5）——这是受 v4.2 改动影响最大的两条。

### 7.3 重新跑 Phase 3.7 Contradiction Map

新引入的 H-subgroup 文献可能在 contradictions 上和现有 Rosenblat & Stark 类文献冲突（他们假设职业 gig worker，新文献谈 amateur），这是**好的冲突**——Beat 7 ¶5 的 Gamification Risk 段落可以吸收。

### 7.4 重新跑 Phase 4 Evidence Inventory

evidence_inventory[4]（F5）必须从"全样本 tolerance"改为"driver 子集 tolerance (N=19) + rider 子集对照 (N=12)"。这是 pipeline 端对应大纲 Beat 5 改动的镜像。

### 7.5 重新跑 Phase 5 Five-Reviewer Evaluation

所有五个 reviewer（honesty / coverage / contradiction / gap / precision）分数重新跑。**目标分数**：

| Reviewer | v4.1 基线（估计）| v4.2 目标 |
|----------|---------------|----------|
| Honesty | 0.80 | ≥ 0.85 |
| Coverage | 0.70（因 E 类真空） | ≥ 0.85 |
| Contradiction | 0.75 | ≥ 0.85 |
| Gap | 0.70 | ≥ 0.80 |
| Precision | 0.80 | ≥ 0.85 |

### 7.6 产出最终的 audit bundle

把以下文件打包为 `pipeline_v4.2_audit_bundle.zip`：
- state.json（pipeline 最终状态）
- phase_outputs/*.json（所有阶段产物）
- config/manual_core_inclusions.json（含 A/B/E 新增）
- config/*_audit.md（E/I/H 三份 audit 记录）
- reports/query_expansion_report.md
- reports/edge_density_diff_report.md
- reports/phase5_reviewer_final_scores.json

这个 bundle 是论文 §6.2 Audit Trail 的数据基础，也是开源发布给 design research 社区复现的完整包。

---

## Part 8. 诚实性纪律（跑 pipeline 时必守）

| 行动 | 允许 | 禁止 |
|------|-----|------|
| manual inclusion 的 rationale | 明确说为什么 native、引到哪一段 | 用 "seems relevant"、"appears to support" 之类模糊 |
| 类别归属 | 主 + secondary label | 类别 inflation（proxy 打成 native）|
| DOI 验证 | Crossref/OpenAlex 双验证 | 猜测 DOI、未验证接受 |
| 找不到文献 | 明确报告 "no suitable match" | 降标准硬凑 |
| Phase 5 分数 | 真实分数，包括低分 | 为达标 inflation |
| audit.md 的拒绝候选 | 列出并说理由 | 悄悄丢弃 |
| gaps_ranked.json | 诊断信号 | 在论文里当 contribution 吹 |

---

## Part 9. 失败与回滚

若跑到任何一步发现：

- A 产出 <2 篇 native → **停止 B/E/C/D**，告知大纲端走"E 类 under-investigated primitive"升级路径（见 paper_outline_v4.2.md Beat 3 fallback 档位）
- E 方向 2（amateur driver 文献）= 0 → **继续跑 C/D 但标注 Beat 5 ¶2 需要用 weakest fallback 档位**（只引 Rosenblat & Stark 类，但 explicit 说 "we extend this concern to a new population (amateur drivers) without direct literature precedent"）
- D 抽样误判率 > 30% → **回滚到 relationship_graph_v4.1_backup.json**，debug extraction prompt

---

## 附录：v4.1 → v4.2 改动清单

| 项目 | v4.1 | v4.2 |
|------|------|------|
| Prompt 数量 | 4（A/B/C/D）| 5（A/B/**E**/C/D）|
| 新增 prompt E | — | H 类细分补强 |
| 新增 evidence 处理 | — | Phase 4 F5 改为双子集 |
| 新增 secondary label | — | "H-subgroup"、"H-amateur" |
| 新增 edge 要求 | — | H-subgroup 与 F5 强 edge |
| Phase 5 目标 coverage | 未定 | ≥ 0.85 |
| audit bundle | 未定 | 硬要求 |

---

**文档版本**：v4.2
**创建日期**：2026-04-22
**对齐文档**：`paper_outline_v4.2.md`
**上游输入**：v4.1 pipeline 诊断报告 + Cornell_Carpool_System_Survey_April_21__2026_22_55.csv 真实数据分析
