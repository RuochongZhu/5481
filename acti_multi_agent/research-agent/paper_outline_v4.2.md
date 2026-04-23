# CampusRide Paper Outline v4.2 (Full Long Version)

> **作用**：在 research-agent pipeline 的 7-beat 硬约束下，承载三个 contribution 主线的 **12–15 页 mid-tier conference / 扩展期刊版**大纲。Compact 短版已移除。
>
> 三个 contribution 主线：
> ① CampusRide 作为 identity-verified **六模块**校园平台的设计案例（每模块单独一小节）
> ② 拼车模块作为深度实证案例（基于 N=44 finished / 问卷）
> ③ research-agent 作为 thesis-conditioned 文献综述的方法论贡献（**独立成节**）
>
> **约束**：pipeline `phase_contracts.py` 硬性要求 7 个 beat。论文 section 结构必须一一对应。
>
> **v4.2 vs v4.1 主要变动**（见本文末 Part 7 改动清单）：
> - 问卷真实数据核对后，N 口径从 "117/50" 修正为 "111 eligible / 44 finished"（去掉 6 条 Survey Preview 测试响应）
> - 母语比例从 "82% Mandarin" 修正为 "79% of respondents who reported native language (72/91)"
> - Finding F1 数字微调（29/33 → 28/32）
> - Finding F3 数字微调（±1.5 范围内与最终 CSV 同步）
> - **Finding F5 重大改动**：从全样本 (N=30) 改为 Driver/Both 子集 (N=19)，rating-fairness asymmetry 在子集上显著强化
> - **新增 Finding F6**：司机对空座提供的意愿梯度（Q23_1/2/3），长途 Very/Extremely willing = 12/33 (36%) 最高
> - Beat 5 / §4.2 整段重写（见 Part 2）
> - Part 5 对齐表新增 `min_edges_per_chain` 硬指标
> - §6.2 Audit Trail 新增 negative audit 段落
> - Beat 3 ¶1 Identity primitive 改为档位化措辞（依据 E 类 manual inclusion 数量）
> - Beat 7 §7.2 Sample Skew 加入 N=19 driver 子集披露

---

## Part 0. 论文基本信息

### 0.1 候选标题

- **主候选**：*"CampusRide: An Identity-Verified Multi-Module Campus Platform with a Deep-Dive Case on Small-Town Carpooling — Supported by a Thesis-Conditioned Evidence Pipeline"*
- **短版**：*"CampusRide: Designing an Identity-Verified Multi-Module Campus Platform, with a Carpool Deep-Dive and a Methodology Contribution"*
- **方法论强调版**：*"From Grassroots Practice to Platform Design: A Six-Module Campus Case with Survey-Informed Carpool Evidence and an Auditable Literature Pipeline"*

建议主候选作为投稿标题。三个 contribution 都出现在副标题里，不偷懒。

### 0.2 Contribution Claims（写进 Introduction）

```
本文提出三个贡献：
(1) 一个 identity-verified 六模块校园平台 CampusRide 的设计案例，
    覆盖拼车、二手市场、活动、群组、消息、积分六个模块，
    展示了在单一 .edu 身份层和跨模块设计原语上如何构建校园场景
    的协调基础设施；
(2) 基于 N=111 eligible / 44 finished 前期问卷的拼车模块深度实证分析，
    揭示了三个可迁移的设计发现——.edu 身份验证作为信任原语、国际学生
    群体的草根协调实践、以及司机子群体（N=19）对评分公平性的反直觉
    敏感；
(3) research-agent，一个 thesis-conditioned 八阶段 evidence
    pipeline，在可审计流程下支撑本文的文献综述，并作为 design
    research 社区可复用的方法论工具。
```

### 0.3 目标投稿

- 主目标：CHI full paper、CSCW full paper、DIS full paper、或 IEEE/ACM 扩展期刊
- 备选：NordiCHI、HCII、International Journal of Human-Computer Studies
- 不适合：workshop short paper、LBW、poster

---

## Part 1. 完整论文结构总览

### 1.1 Section 级结构（12–15 页）

| Section | 内容 | 页数 | 对应 beat |
|---------|------|------|----------|
| **§1 Introduction** | 动机 + 三 contribution 声明 | 1.0 | — |
| **§2 Related Work** | 三条文献线 | 2.5 | Beat 1–3 |
| §2.1 | Small-town campus transportation & coordination gaps | 0.7 | Beat 1 |
| §2.2 | Grassroots coordination + integrated campus platforms | 1.0 | Beat 2 |
| §2.3 | Design primitives: identity, safety, rating, rewards | 0.8 | Beat 3 |
| **§3 Methodology** | 问卷 + pipeline 两种方法 | 1.0 | — |
| §3.1 | Formative survey protocol | 0.5 | — |
| §3.2 | Literature synthesis via research-agent | 0.5 | — |
| **§4 Formative Survey Findings** | 问卷结果 | 2.0 | Beat 4–5 |
| §4.1 | Passenger-side WTP and motivations | 1.1 | Beat 4 |
| §4.2 | Driver-subset tolerance & the rating-fairness asymmetry | 0.9 | Beat 5 |
| **§5 CampusRide Platform Design** | 六模块平台 + 拼车 deep-dive | 3.5 | Beat 6 |
| §5.1 | Platform overview & shared design primitives | 0.8 | Beat 6 |
| §5.2–5.7 | Six modules, one subsection each | 1.5 | Beat 6 |
| §5.8 | Carpool deep-dive (four design decisions) | 1.2 | Beat 6 |
| **§6 Research-Agent Pipeline as Methodology Contribution** | 独立 contribution 章节 | 1.5 | — |
| §6.1 | Architecture & 8-phase flow | 0.6 | — |
| §6.2 | Audit trail: how the pipeline shaped this paper (含 negative audit) | 0.6 | — |
| §6.3 | Scope & honest limitations of the pipeline | 0.3 | — |
| **§7 Discussion** | 反思 + 限制 | 1.5 | Beat 7 |
| §7.1 | General reflections on platform design | 0.6 | — |
| §7.2 | Adversarial scoping & limitations | 0.9 | Beat 7 |
| **§8 Conclusion** | | 0.4 | — |
| **References** | | 1.2 | — |
| **正文合计** | | **~13.5** | |
| **含参考文献合计** | | **~14.7** | |

**体量落在 12–15 页区间**，符合 CHI/CSCW full paper 或扩展期刊常见上限。

### 1.2 7-Beat ↔ Section 对应表（pipeline 接口）

| Beat | 论文 Section | 主题 | Pipeline 产物映射 |
|------|-------------|------|-------------------|
| **Beat 1** | §2.1 | 小城校园交通 + 协调缺口 | `narrative_chains[0]`、A+B 类 |
| **Beat 2** | §2.2 | 草根协调 + 集成平台文献 | `narrative_chains[1]`、C+D+I 类 |
| **Beat 3** | §2.3 | 四个 design primitive | `narrative_chains[2]`、E+F+G+H 类 |
| **Beat 4** | §4.1 | 乘客侧 WTP + 动机 + 驾驶者供给意愿 | `evidence_inventory[3]` + 问卷 |
| **Beat 5** | §4.2 | 司机子群体容忍度 + 反直觉发现 | `evidence_inventory[4]` + 问卷 + **H-subgroup** |
| **Beat 6** | §5 (全) | 六模块平台 + 拼车 deep-dive | `evidence_inventory[5]` + 系统文档 |
| **Beat 7** | §7.2 | 对抗性 scoping + 限制 | `contradictions.json` + J 类 |

注意：**§6 Research-Agent Pipeline 不占 beat slot**——它是方法论章节，不是证据链中的一环。pipeline 作为 contribution 通过 §3.2 和 §6 两处共同呈现。

### 1.3 Finding 总表（v4.2 更新）

| Finding | 内容 | 来源题目 | 数字 | 出现段落 |
|---------|------|---------|------|---------|
| **F1** | Uber 定价偏贵 / 可用性问题 | Q16、Q23 (availability) | 28/32 偏贵、23/32 可用性问题 | §2.1 preview、§4.1 ¶2 |
| **F2** | Mandarin 受访者用 WeChat 找拼车显著多于 English | Q15 × Q35 | 17/72 Mandarin vs 1/15 English；或在 Q15 应答者中 17/21 vs 1/2 | §2.2 ¶1 |
| **F3** | 7 项安全特性 WTP 全部 ≥50% | Q20_1–Q20_7 | 69.1 / 67.3 / 63.5 / 60.5 / 55.4 / 54.9 / 50.9 | §4.1 ¶3 |
| **F4** | 动机双梯队，财务 > 游戏化/社交/环保 | Q26_1–Q26_4 | 63.6 / 48.3 / 45.6 / 44.5 | §4.1 ¶4 |
| **F5** | 司机子集对评分不公正容忍度低于其他三类问题 | Q24_1–Q24_4，限 Driver/Both (N=19) | 47.2 / 41.4 / **29.1** / 52.3 | §4.2 ¶1、§5.8.3 |
| **F6** | 驾驶者长途空座提供意愿最高 | Q23_1–Q23_3，N=33 | Ithaca 10/33、短途 9/33、长途 **12/33** Very+Extremely willing | §5.2 引用 |

---

## Part 2. 每个 Beat 的详细内容

### Beat 1 | §2.1 Small-Town Campus Transportation & Coordination Gaps（0.7 页）

**角色**：动机的上半段——场景缺口存在。

**Anchor paper**：Shaheen & Cohen shared mobility 综述类（或等价的小城 rideshare 缺口文献）

**Spine (4–5 篇)**：
- 小城 / 大学 rideshare 服务覆盖文献
- 大学生出行可达性 / food / social coordination 需求文献
- 通用分享经济 (sharing economy) 在小城的局限文献
- （可选）Ithaca / Cornell 本地交通分析 grey literature

**要讲的事**（两段）：
- ¶1：主流商业 rideshare (Uber/Lyft) 在小城校园情境下存在结构性服务缺口——pricing 和 availability 两个维度。文献里有若干实证但不系统
- ¶2：**关键承上启下**——这个缺口不只是拼车问题。学生群体在出行、二手交易、活动组织、日常社交等**多个面向**都面临协调摩擦，这些摩擦共同构成一个"campus coordination gap"。**为 Beat 2 的多模块平台论证铺垫**

**Finding 引用**：F1（Uber 感知贵 28/32、可用性 23/32）——放在第 1 段结尾作 preview

**诚实纪律**：
- 允许说：`exists` / `is documented` / `motivates`
- 禁止说：`has been empirically proved at scale` / `quantified`

### Beat 2 | §2.2 Grassroots Coordination + Integrated Campus Platforms（1.0 页）

**角色**：动机的下半段——既存实践 + 多模块平台的文献基础。**这一 beat 承载双论证线，是全文最长的 Related Work 子节**。

**Anchor paper**：Sawyer & Chen 类国际学生 WeChat 研究

**Spine (7–8 篇)**：
- C 类 3 篇：WeChat/WhatsApp 群协调、self-organized 社区平台
- D 类 2 篇：国际学生 US 大学数字实践
- I 类 2–3 篇：super-app / integrated community platform 文献（见 pipeline v4.2 Prompt B 补强）

**要讲的事**（四段）：

- ¶1：国际学生已自发通过通讯软件群组协调拼车——这是**非正式基础设施** (informal infrastructure) 存在的最直接证据。F2 preview 放这里。
  - **F2 精确表述**：在 72 位以 Mandarin Chinese 为母语的受访者中，17 位报告通过 WeChat/WhatsApp 群组寻找拼车伙伴；对照组 15 位 English 母语受访者中仅 1 位。考虑到问卷逻辑跳转使得 Q15（找拼车途径）的实际应答子集较小（Mandarin 21/72、English 2/15），在应答者内部该比例为 17/21 对 1/2。无论采用哪个分母，方向一致、强度显著
- ¶2：这类协调**不限于拼车**。同一 WeChat 群里也在做二手交易、活动召集、信息共享、应急求助。学生群体已在多域协调中依赖**单一社交通道**。这是"多模块平台"合法性的**经验锚点**
- ¶3：**文献层面**，super-app / integrated community platform 研究指出集成设计的价值（引 I 类 1–2 篇）。**此处措辞依据 pipeline Prompt B 的 I 类 audit 输出档位化**：
  - 若 I 类 native N≥5：`an established design space with documented value propositions`
  - 若 I 类 native N=3–4：`an emerging design space with several case studies`
  - 若 I 类 native N<3：`an initial inquiry with fragmented precedent`
  
  大多数现有 super-app 文献聚焦大众市场（微信、Grab、Gojek 等）或一般社区平台。**针对校园 + 封闭 scope 的多模块集成研究尚不成熟**——这是 CampusRide 的设计空间
- ¶4：过渡到 Beat 3：要把上述草根实践形式化，需要什么 design primitive？下一节回答

**Finding 引用**：F2（含双分母披露）放在 ¶1

**诚实纪律**：
- 草根协调文献较稳——可以用 `document` / `indicate`
- I 类 super-app 文献档位化措辞见上
- 不宣称 CampusRide 是"第一个"多模块校园平台

### Beat 3 | §2.3 Design Primitives: Identity, Safety, Rating Fairness, Rewards（0.8 页）

**角色**：框架——从文献中提炼出四个 design primitive，为 §5 的系统设计预铺轨道。

**Anchor paper**：Ert, Fleischer & Magen 2016 Airbnb trust（或 Resnick & Zeckhauser reputation systems）

**Spine (6–8 篇)**：
- E 类 2 篇：`.edu` / campus-scoped identity verification（依赖 pipeline Prompt A manual inclusion 的结果）
- F 类 2 篇：shared mobility safety、real-time location、SOS
- G 类 1–2 篇：gamification in coordination / mobility
- H 类 2 篇：peer rating、algorithmic management、rating fairness（其中 H-subgroup 文献为 Beat 5 专设，见 Prompt E）

**要讲的事**（四段，每 primitive 一段）：

- ¶1 **Identity primitive**（档位化措辞，依据 Prompt A 的 E 类 manual inclusion 结果）：
  - 若 E 类 native N≥5：`Identity verification in sharing economy has a mature literature, specialized here to institutional and .edu-scoped contexts, where closed-community scoping demonstrably reduces stranger-coordination costs`
  - 若 E 类 native N=3–4：`Identity verification is a well-studied trust signal in sharing economy; institutional identity scoping (with .edu as one instance) has been discussed in case-by-case terms in HCI/CSCW literature, though a systematic treatment is less developed`
  - 若 E 类 native N<3 （即当前 v4.1 状态）：`While identity verification has an established literature in broader sharing economy contexts, .edu-scoped identity as a distinct trust primitive has received limited systematic treatment. We position this paper's treatment as one case within this under-investigated space`——**此时 E 类稀薄从 coverage 缺陷翻译为 contribution 的一部分**
- ¶2 **Safety primitive**：shared mobility 中的主动安全设计——实时位置共享、SOS、emergency contact。文献显示这些 feature 对用户 trust 的提升
- ¶3 **Rating-fairness primitive**：peer rating 作为 reputation 机制的长处与 algorithmic management 批评带出的公平性问题。引 Rosenblat & Stark、Lee et al. 等经典文献。**此处需要和 Beat 5 的 driver-subgroup finding 对话**——现有 rating fairness 文献主要覆盖职业 gig worker，amateur / occasional driver 的 rating anxiety 是否同构是本文追问的问题之一（见 pipeline Prompt E 引入的 H-subgroup 文献）
- ¶4 **Rewards/gamification primitive**：积分激励在 coordination / mobility 中的应用 + 对内在动机挤出的 risk（引 Koivisto & Hamari、Deterding 等）

**Finding 引用**：无——pure 文献

**诚实纪律**：
- 四 primitive **并列**，不在这一 beat 做价值排序。**Beat 4/5 的经验发现 + Beat 6 的设计决策才承担排序工作**
- 每个 primitive 至少 1 篇经典引用 + 1 篇最新（2022+）引用
- Identity primitive 措辞严格依 Prompt A audit 档位，不向上越档

### Beat 4 | §4.1 Formative Survey: Passenger-Side WTP & Motivations（1.1 页）

**角色**：核心实证 I——乘客视角的需求、痛点、WTP、动机，并附司机供给意愿前置。

**Anchor paper**：无（primary data）

**Supporting**：问卷数据 + Beat 3 design primitives 的回指

**要讲的事**（四段 + 表/图）：

- ¶1 (recap)：问卷 methodology 放 §3.1，这里只 recap——N=111 eligible / 44 finished（排除 6 条 Survey Preview 测试响应）；79% of respondents who reported native language are Mandarin Chinese (72/91)；本节报告每题完成响应者子集，N 每题报告
- ¶2 (交通缺口量化)：F1 数字表或 bar chart——Uber pricing 偏贵 28/32 (Slightly + Much higher)、availability 问题 23/32 (Somewhat difficult + Moderate + Very difficult)
- ¶3 (WTP 安全特性排序)：F3 完整表（所有 N=30–31）：
  - Real-Time Location Sharing：mean 69.1（median 76）
  - School email verification (.edu)：mean 67.3（median 79）
  - Emergency SOS button：mean 63.5（median 64）
  - Driver's driving experience visibility：mean 60.5（median 60）
  - Automatic trip-sharing with emergency contacts：mean 55.4（median 52）
  - Driver's social connections display：mean 54.9（median 60）
  - Interior car photos：mean 50.9（median 52）
  
  **全部 7 项 mean ≥50% 且 top-4 的 median ≥60%**，是一个强 observation，值得强调
- ¶4 (动机结构)：F4 motivation bar——splitting fuel costs 63.6、platform rewards 48.3、social expansion 45.6、environmental impact 44.5。**双梯队动机**（财务显著高于其他三项的持平梯队）作为 Beat 6 积分模块辅助化设计的依据

**表/图**：1 张 WTP 排序表 + 1 张 motivation bar chart

**Finding 引用**：F1、F3、F4 全量

**诚实纪律**：
- **不做任何 inferential statistics**（no t-test、no p-value、no 显著性声明）
- 承认 79% Mandarin 母语的 scope-setting 性质——**不当 bias 遮掩，也不当论文卖点**
- 所有 mean / median 必须标注 N，不得裸数字

### Beat 5 | §4.2 Formative Survey: Driver-Subset Tolerance & the Rating-Fairness Asymmetry（0.9 页）

**角色**：核心实证 II。**论文最有辨识度的 counterintuitive finding 所在**。

**v4.2 重大修订**：本节从"全样本 tolerance (N=30)"改为"**Driver/Both 子集 tolerance (N=19) + Rider-only 子集对照 (N=12)**"。此修订由真实数据核查推动：rating-fairness asymmetry 只在 driver 子集内清晰存在，在 rider 子集内不成立。使用全样本会让乘客对假设性情境的回答稀释掉真司机的真实偏好。

**Anchor paper**：Rosenblat & Stark 2016；本 beat 需要补强 H-subgroup 文献（见 pipeline Prompt E）

**Spine**：
- H 类经典 rating fairness 文献 1–2 篇（Rosenblat & Stark、Lee et al.）
- **H-subgroup 1 篇**：driver vs passenger perspective 的非对称 rating 研究（Prompt E 方向 1）
- **H-amateur 1 篇**：非职业 / 偶发司机的 rating 经验文献（Prompt E 方向 2）
- F 类 rideshare driver experience 1 篇

**要讲的事**（三段 + 一张对比图）：

- ¶1 (子集说明 + 核心 finding)：
  
  在 44 完整响应中，Q3 (travel role) 自我报告为 Driver (N=23) 或 Both (N=22) 的受访者合并为 Driver/Both 子集，Rider-only 为对照子集。Q24_1–Q24_4 四项容忍度在两子集内的对比如下（全部为 0–100 评分，值越大越容忍）：
  
  | 容忍项 | **Driver/Both (N=19)** | Rider-only (N=12) | 差值 |
  |-------|----------------------|-----------------|------|
  | 乘客迟到 10 分钟 (Q24_1) | 47.2 | 35.7 | +11.5 |
  | 乘客临时改目的地 (Q24_2) | 41.4 | 19.6 | +21.8 |
  | **乘客给出不公平评分 (Q24_3)** | **29.1** | 22.4 | +6.7 |
  | 乘客要求非标准路线 (Q24_4) | 52.3 | 33.2 | +19.1 |
  
  在 Driver/Both 子集内，"不公平评分"容忍度 29.1 显著低于其他三项（41.4–52.3），gap 范围 12.3–23.2 分。同一受访者对乘客行为问题的容忍度显著高于对评分系统本身不公的容忍度。**这是本文的核心 counterintuitive observation：司机最难忍的不是乘客行为失当，而是来自评分系统本身的不公平**

- ¶2 (子集选择的 methodological justification)：
  
  我们选择仅在 Driver/Both 子集报告 F5，而非使用全样本 N=30 的两个理由：
  1. Q24 问题语义为"作为司机对以下情境的容忍度"。Rider-only 受访者回答此题时必然是**假设性作答**——他们没有实际驾驶经验来校准评分。混合报告会用假设性回答稀释真司机的经验回答
  2. 实证对照支持这一选择：Rider-only 子集中同一个 pattern **弱很多**（"不公平评分" 22.4 甚至高于"改目的地" 19.6），说明该 pattern 对 driver-like 经验锚定
  
  承认代价：N=19 小。我们不做 inferential statistics，仅作 descriptive observation。本 finding 需要更大规模 driver 专项调查来验证
- ¶3 (文献对话)：
  
  Rosenblat & Stark 等 algorithmic management 研究早已指出职业 gig worker 对平台评分的焦虑。我们的 finding 在**校园 peer carpool 这一更小规模、更高信任、非职业**的情境下**resonates with this concern**。这指向两个关键外推：
  1. 即使有 `.edu` 身份验证这类强信任信号，**评分系统本身的公平性仍是独立的、不可替代的 design concern**
  2. Rating anxiety **不是职业劳动议价的独有产物**；amateur / occasional driver 也表现出类似敏感（引 H-amateur 文献，若 Prompt E 方向 2 有结果）
  
  **若 Prompt E 方向 2 无适配文献**：降级措辞为 `We extend this concern from professional gig work to an amateur driver context without direct literature precedent; this extension itself is a limitation we acknowledge in §7.2`

**关键图表**：**3×4 tolerance 对比图**（本文最具辨识度的 figure）
- 横轴：四个容忍项（迟到 / 改目的地 / 不公平评分 / 改路线）
- 纵轴：0–100 容忍度
- 三组柱：全样本 N=30 / Driver/Both N=19 / Rider-only N=12
- 重点 annotate：Driver/Both 子集上"不公平评分"柱显著低于同子集其他三项
- Legend (English)：Full Sample (N=30) / Driver Subset (N=19) / Rider Subset (N=12)

**Finding 引用**：F5（driver 子集版本）

**诚实纪律**：
- 不把 F5 过度泛化到所有 peer rating 系统
- N=19 的子集 observation，需要更大规模验证
- 用 `resonates with` / `parallels` 而不是 `confirms` / `replicates`
- 明确 disclose 子集切分决策和代价
- Rider-only 子集对照数字必须报告，不得因为对 pattern 弱而隐藏——它恰恰是 methodological 合理性的支撑

### Beat 6 | §5 CampusRide Platform Design（3.5 页，全文最大章节）

**角色**：核心贡献——六模块平台的设计案例 + 拼车模块的深度设计。

这一 section 分三层：§5.1 platform overview、§5.2–5.7 六模块各一小节、§5.8 拼车深度。

#### §5.1 Platform Overview & Shared Design Primitives（0.8 页）

- ¶1：CampusRide 架构——Vue 3 + Express + Supabase + Socket.IO 一句话技术栈。**一张架构图**（占 0.4 页）展示 6 个模块 + 共享的 auth / identity / messaging / points 四层基础设施。Figure legend 用 English
- ¶2：**共享 design primitive 矩阵**——6 模块 × 4 primitive 的小表格：
  - Carpool：Identity ✓ / Safety ✓✓ / Rating ✓✓ / Rewards ✓
  - Marketplace：Identity ✓ / Safety ✓ / Rating ✓ / Rewards ✓
  - Activities：Identity ✓ / Safety ○ / Rating ○ / Rewards ✓
  - Groups：Identity ✓ / Safety ○ / Rating ○ / Rewards ○
  - Messages：Identity ✓ / Safety ○ / Rating ○ / Rewards ○
  - Points：(cross-module meta-module)
- ¶3：过渡——`.edu` 身份层是所有模块的共同准入；积分模块是跨模块 meta-layer；拼车的 safety + rating 是最密集的 primitive 使用，因此深度案例选拼车

#### §5.2 Carpool Module (overview)（0.25 页）

- 功能定位：校园内部 / 短途 / 长途 三类距离拼车匹配
- 用到的 primitive：四个全用到
- 关键用户场景：Ithaca 内通勤、去 NYC/Boston 长途返家
- **F6 引用 (v4.2 新增)**：司机供给意愿数据 (Q23_1–Q23_3)——在 33 位回答 Q23 系列的受访者中，Very willing + Extremely willing 的比例为 Ithaca 内 10/33 (30%)、短途 9/33 (27%)、**长途 12/33 (36%)**。长途场景司机供给意愿最高，直接支撑本模块对"长途返家"作为重点场景的设计选择
- 详细设计决策在 §5.8

#### §5.3 Marketplace Module（0.25 页）

- 功能定位：校园内部 P2P 二手交易
- 用到的 primitive：Identity（强）、Rating（买卖双向）、Rewards（发帖 + 交易奖励）
- 关键设计决策：`.edu` 验证作为买卖双方准入、面对面交易 optional 位置共享
- 和拼车的设计原语复用点：同一 identity + rating + messaging 层

#### §5.4 Activities Module（0.25 页）

- 功能定位：校园活动发布 + 报名 + 签到
- 用到的 primitive：Identity、Rewards（参与积分）
- 关键设计决策：跨文化活动（引用 F2 的国际学生背景）作为平台特色场景；签到系统和积分联动

#### §5.5 Groups Module（0.2 页）

- 功能定位：兴趣群组 / 地理群组 / 群组地图
- 用到的 primitive：Identity、Rewards
- 关键设计决策：群组发现机制、群组地图可视化作为 social discovery layer

#### §5.6 Messages Module（0.2 页）

- 功能定位：DM、系统消息、群消息（Socket.IO 实时）
- 用到的 primitive：Identity
- 关键设计决策：消息和其他模块的嵌入（拼车路上自动建群、市场交易自带消息通道、活动自带群聊）。**这一嵌入是多模块集成的核心机制**

#### §5.7 Points Module (Cross-Module Gamification)（0.2 页）

- 功能定位：跨模块 meta-layer
- 用到的 primitive：Rewards（自身）
- 关键设计决策：积分如何从哪些行为累积；跨模块通用消费点数；**F4 的"辅助动机"定位**让积分刻意**不**主导经济激励

#### §5.8 Carpool Deep-Dive: Four Design Decisions（1.2 页）

**角色**：论文最具设计反思性的子节。从 Beat 4/5 的 finding 直接推出四个设计决策。

##### §5.8.1 Identity Verification (0.3 页)
- 设计决策：`.edu` 验证作为注册 gating + profile 持续展示的 trust signal
- 证据支撑：F3 的 mean 67.3 / median 79（WTP uplift 的 top-2）
- 实现简述：注册流程、验证机制、在 driver/passenger profile 中的展示方式
- 局限承认：`.edu` 只验证身份，不验证驾驶能力、不防止行为失当

##### §5.8.2 Safety Skeleton (0.3 页)
- 设计决策：实时位置共享 + SOS 按钮作为行程进行中的两个主动安全层
- 证据支撑：F3 的 Real-Time Location mean 69.1（top-1）、SOS mean 63.5（top-3）
- 实现简述：Socket.IO 的 thread 房间机制；SOS 的短路径（一键联系紧急联系人）
- 局限承认：位置共享对隐私的 trade-off；SOS 的响应链条依赖校外资源

##### §5.8.3 Rating System with Fairness Consideration (0.35 页) — **论文最具创新性的设计段落**
- 设计决策：
  - 双向评分（乘客 ↔ 司机对称）
  - 评分理由必填
  - 评分公开前的异议窗口（例如 24 小时）
  - 跨行程的评分趋势保护——单次异常评分不决定司机总体标签
- 证据支撑：F5 driver 子集的 29.1（vs 同子集其他三项 41.4–52.3），明确 attribute 到 Driver/Both subset (N=19)
- 对话 algorithmic management 文献：我们的设计是否真的缓解了那种焦虑？**承认本文无部署数据可以验证**，作为 future work
- 局限承认：异议窗口可能被操纵；跨行程保护可能减慢对真正问题司机的识别；N=19 子集限制设计决策的经验底盘

##### §5.8.4 Gamification as Secondary Incentive (0.25 页)
- 设计决策：积分作为辅助激励，不主导经济动机
- 证据支撑：F4 的 48.3（gamification 第二梯队）
- 实现简述：拼车积分与跨模块积分池联通
- 局限承认：积分机制可能诱导 gaming behavior（见 Beat 7 讨论）

**Finding 回指汇总**：F3 × 3 次、F4 × 1 次、F5 × 1 次、F6 × 1 次（在 §5.2）——六次 finding 回指使 §5 每个核心设计都有经验依据

**诚实纪律**：
- 避免 `effective` / `successfully` / `proves`
- 允许 `we designed` / `we implemented` / `motivated by` / `in response to finding X`
- F5 的 attribution 必须到 subset 层级，不得混淆为全样本

### Beat 7 | §7.2 Adversarial Scoping & Limitations（0.9 页）

**角色**：全篇的诚实性锚点。**这一 beat 对 pipeline contradiction reviewer 评分至关重要**。

**Anchor paper**：Rosenblat & Stark、Lee et al. 或其他 algorithmic management 批评

**Spine**：`contradictions.json` 打捞出的 5 个 focus + H-subgroup 文献对 N=19 子集的方法论讨论

**要讲的事**（五段 adversarial scoping）：

- ¶1 (Formalization Risk)：形式化草根实践可能复制商业 rideshare 的 algorithmic management harm。我们的 rating fairness 设计是**响应**而非**解决**这一风险
- ¶2 (Sample Skew，v4.2 扩展)：
  - 主样本偏态：79% Mandarin 母语样本偏态限制 findings 泛化性。English 母语学生 N=15，对他们的任何判断（包括"他们不用微信群"）都有较大不确定性
  - **子集偏态 (v4.2 新增)**：F5 的核心 observation 基于 Driver/Both 子集 N=19。我们认为这个 subset 选择在方法论上优于使用全样本（见 §4.2 ¶2 justification），但 N=19 本身仍然非常小。该 finding 需要专项 driver 调查验证
  - 完成率偏态：问卷 44/111 完成（~40%），完成者可能在某些维度（如对拼车议题的关注度）与未完成者系统性不同
- ¶3 (No Deployment Evaluation)：本文 stop 在设计案例阶段，未提供部署数据。四个 design decision 之间的相对效力未在 real-world 中被比较
- ¶4 (Scope Boundary of `.edu`)：身份验证解决身份问题，不解决行为问题——不验证驾驶能力、不阻止恶意行为、不替代平台治理。若 Prompt A 的 E 类 manual inclusion 不足，进一步承认："our treatment of .edu as a trust primitive operates in a literature space with limited direct precedent"
- ¶5 (Gamification Risk)：跨模块积分系统可能在某些模块（比如拼车）产生 gaming behavior（刷积分、虚假行程）。本文没有数据评估这一风险

**诚实纪律**：
- 每段引 1 篇相关反证文献，不空泛自省
- 这一 beat 主动求 pipeline contradiction reviewer 打高分——写完跑一遍 Phase 5 看这里 honesty 分
- Sample skew 的三层披露（主样本 / 子集 / 完成率）不得合并，reviewer 容易以此扣 honesty 分

---

## Part 3. 非 Beat Section 的内容

### §1 Introduction（1.0 页）

**四段结构 + 三 contribution bullet**：
- ¶1 (Hook)：小城校园 + 国际学生 + 草根协调的三重交叉场景——用 Cornell/Ithaca 作为 representative case
- ¶2 (Gap + Practice)：Beat 1 + Beat 2 的 teaser。"交通不只是交通"是承接全文的钩子
- ¶3 (Approach)：三件事——N=111 eligible / 44 finished 前期问卷 + CampusRide 六模块平台（拼车 deep-dive）+ research-agent pipeline 支撑文献综述
- ¶4 (Contribution)：Part 0.2 的三 bullet

### §3 Methodology（1.0 页）

两个小节，各 0.5 页。

#### §3.1 Formative Survey Protocol（0.5 页）

- 招募方式、平台（Qualtrics）、时间段
- 同意声明的原文引用（一两句）
- **N 的精确披露 (v4.2 修订)**：问卷平台原始记录 N=117，其中 6 条 Status='Survey Preview' 为研究者内部测试响应已排除。有效受访者 N=111 进入问卷、N=44 完成全部问题
- **母语分布披露 (v4.2 修订)**：在报告母语的 91 位受访者中，72 位（79%）为 Mandarin Chinese 母语、15 位（16%）为 English 母语、其他 4 位（5%）。**此比例作为 scope 披露，不作为偏见解释**
- **角色分布披露**：Q3 自我报告 Rider N=56、Driver N=23、Both N=22、未报告 N=10。Beat 5 专门使用 Driver + Both 子集 (N=45 中的 N=19 完整应答 Q24)
- 问题设计的 7 大模块简述（demographics / travel patterns / pain points / Uber perception / safety WTP / motivations / driver tolerance）
- 本文分析立场：descriptive only；每项 finding 标注具体的 N

#### §3.2 Literature Synthesis via Research-Agent（0.5 页）

这是 contribution #3 的第一次出现（第二次在 §6 展开）。两段：

- ¶1：本文 Related Work 和 Adversarial Scoping 的文献底盘由 research-agent pipeline 支撑。pipeline 是 8 阶段 thesis-conditioned evidence chain（从语料装配 → 分类 → 深抽取 → 关系图 → narrative → contradiction → evidence inventory → reviewer diagnostics）
- ¶2：pipeline 对本论文的直接价值——**可审计的反证打捞**（§7.2）和 **evidence sufficiency diagnostics**。详细架构和应用在 §6 展开；完整实现开源在 `<repo URL>`

**诚实纪律**（继承自 pipeline `CURRENT_STATUS_AND_RECOMMENDATIONS.md`）：
- 不声称 pipeline 自动生成论文
- 不声称 pipeline 提供 open-ended gap discovery
- 表述为 `evidence-chain organization tool` 而不是 `research agent`

### §6 Research-Agent Pipeline as Methodology Contribution（1.5 页）

这是 contribution #3 的主场章节。

#### §6.1 Architecture & 8-Phase Flow（0.6 页）

- ¶1：pipeline 总架构——provider 分层（OpenAlex + S2 + arXiv + Lens + Crossref）、推理层（Claude + GPT）、identity 层（DOI canonical ID）、state machine（phase-based resumability）、契约层（`phase_contracts.py`）
- ¶2：8 阶段功能一句话总结
  - Phase 1 Corpus Assembly
  - Phase 2 Classification (A–J taxonomy)
  - Phase 2.5 Deep Extraction
  - Phase 3 Relationship Graph + Evidence Sufficiency
  - Phase 3.5 Narrative Chains
  - Phase 3.7 Contradiction Map
  - Phase 4 Evidence Inventory
  - Phase 5 Five-Reviewer Evaluation
- **一张图**：8 阶段流水线示意（0.25 页）。Figure legend 用 English

#### §6.2 Audit Trail: How the Pipeline Shaped This Paper（0.6 页）

**这是 §6 最有说服力的一段**——用本文自己作为 case study 展示 pipeline 的 operational value。**v4.2 新增 negative audit 段以平衡 positive instances**。

- ¶1 (Positive audit)：具体审计追溯——Section 2 的 anchor papers 来自 `narrative_chains.json`；§7.2 的 5 个 adversarial scope 直接映射 pipeline `contradictions.json` 的 5 个 focus；§5 的 finding 回指次数由 `evidence_inventory.json` 检查覆盖
- ¶2 (Positive audit)：Phase 5 reviewer feedback 对本文的修改历程——具体列 1–2 个 reviewer iteration（比如"初稿 honesty 分 0.72，reviewer 指出 §5.8 有 `effective` 表述，改为 `designed to address` 后升至 0.84"）
- ¶3 **(Negative audit，v4.2 新增)**：pipeline 也有给出误导信号或漏抓的情况，本小段公开披露两个具体实例以 balance：
  - (a) Phase 2 自动分类把 3 篇 proxy-level 论文标为 E 类 native `.edu` 文献。人工审查 (Prompt A audit) 降级为 proxy，并手工补入真正 native E 类论文的 DOI（具体做法参考公开 repo 的 `config/e_category_audit.md`）。这暴露了 automated classification 在 niche category 上的 limitation
  - (b) 问卷核对阶段发现，初版 evidence_inventory[4] (F5) 报告基于全样本 N=30 的 tolerance 数字。经子集分析后修订为 Driver/Both N=19，pipeline 当前版本不自动对 survey 做 subset sensitivity analysis——这是 pipeline 支持的 scope 边界，不是 bug。在未来 pipeline 迭代中会增加 primary-data 子集健壮性检查
- ¶4 (Positive audit)：可复现性声明——pipeline 和本文的全部 config、`state.json`、各阶段产物都开源，包括 Prompt A/B/E 的 audit 记录

#### §6.3 Scope & Honest Limitations of the Pipeline（0.3 页）

- 一段明确说清楚 pipeline **不是**什么：
  - 不是 open-ended research agent
  - 不是 automated thesis generator
  - 不是 gap discovery tool（`gaps_ranked.json` 是诊断信号不是结论）
  - 仅 abstract-first，不做 full-text truth extraction
  - 不对 primary survey data 做子集稳健性检查（需人工介入）
- 给出对后续使用者的建议（参考 `CURRENT_STATUS_AND_RECOMMENDATIONS.md` 第 5–6 节）

### §7.1 General Discussion（0.6 页）

三段：
- ¶1 (From Grassroots to Formal)：反思 `.edu` 验证作为介于商业 app 和草根群之间的第三种信任架构
- ¶2 (Cross-Module Transferability)：拼车模块的设计原语如何在 marketplace / activities / groups 中再利用。指向"模块共享设计原语"的 methodological claim
- ¶3 (Pipeline-Assisted Design Research)：反思 research-agent 在本研究中的角色——让文献综述 auditable，contradiction reviewer 推动 §7.2 adversarial scoping 的深度；同时承认 pipeline 的 niche category 和 primary-data sensitivity 的 limitation（接 §6.2 ¶3 的 negative audit）

### §8 Conclusion（0.4 页）

四句话：
- 小城校园存在多面向协调缺口，国际学生草根实践给出具体形态
- CampusRide 把这些实践形式化为六模块 identity-verified 平台
- 拼车模块的深度案例展示了四个设计原语如何从 survey findings 推到实现，其中 driver-subset rating-fairness observation 作为核心 counterintuitive 发现
- research-agent pipeline 作为可复用方法论工具开源，供 design research 社区使用

---

## Part 4. 页数最终汇总

| 分组 | 页数 |
|------|------|
| §1 Introduction | 1.0 |
| §2 Related Work (Beat 1–3) | 2.5 |
| §3 Methodology | 1.0 |
| §4 Formative Findings (Beat 4–5) | 2.0 |
| §5 Platform Design (Beat 6) | 3.5 |
| §6 Pipeline Methodology | 1.5 |
| §7 Discussion (含 Beat 7) | 1.5 |
| §8 Conclusion | 0.4 |
| **正文小计** | **13.4** |
| References | 1.2 |
| **总计** | **14.6 页** |

Appendix 不计入正文（多数期刊在 page limit 外）：
- Appendix A：问卷全文 + 同意声明
- Appendix B：research-agent pipeline 完整架构图 + 每阶段接口
- Appendix C：完整 N 每题报告 + 所有交叉表（含 Driver/Both 与 Rider-only 子集的完整四维 tolerance）
- Appendix D：pipeline 审计追溯完整日志（含 Prompt A/B/E 的 audit 输出）

---

## Part 5. 每个 Beat 与 Pipeline 产物的精确对应（对齐表）

这张表是本大纲和 `pipeline_v4.2_modification_guide.md` 的**共享主键**。

**v4.2 新增列**：`min_edges_per_chain` —— narrative_chain 内支撑论文之间的最少 edge 数，作为 Phase 3 relationship graph 的硬指标。

| Beat | 论文 Section | Pipeline 类别 | narrative_chains 索引 | contradictions focus | reviewer 约束点 | Finding 引用 | `min_edges_per_chain` |
|------|-------------|--------------|--------------------|--------------------|---------------|-------------|---------------------|
| 1 | §2.1 | A + B | [0] | F1 (Gap vs. Substitute) | honesty: 不写成 empirically quantified | F1 (preview) | 8 |
| 2 | §2.2 | C + D + I | [1] | F2 (Grassroots Legitimacy) | coverage: C/D/I 类必须补料（Prompt B）| F2 | 8 |
| 3 | §2.3 | E + F + G + H | [2] | 无专属 focus | narrative: 四 primitive 并列；E 类档位化措辞（Prompt A）| — | 8 |
| 4 | §4.1 | — (primary data) | [3] | 无 | honesty: no inferential stats | F1、F3、F4、F6 | 5 |
| 5 | §4.2 | H + **H-subgroup** + F（对话） | [4] | F5 (Rating Fairness) | gap: 不过度泛化 F5；子集 N=19 必须披露 | F5 (driver 子集) | 8 |
| 6 | §5 (全) | — (artifact) | [5] | F3 (.edu), F5 (Gamification) | honesty: no "effective" | F3、F4、F5、F6 | 5 |
| 7 | §7.2 | J + H + **H-subgroup** | [6] | 所有 5 focus | contradiction: ≥5 critical | — | 6 |

**总 edge 下限**：∑ min_edges_per_chain = 48 条。加上跨 chain 的 bridge edge（Prompt D 产出的 CONCEPTUAL_OVERLAP 等），总 edge 数目标 ≥ 80。

---

## Part 6. 诚实性纪律总表（写作时必守）

| Section | 允许的动词 | 禁止的动词 | v4.2 新增约束 |
|---------|-----------|-----------|-------------|
| §2.1 Beat 1 | exists, motivates, is documented, points to | has been proved, is quantified, definitively shows | — |
| §2.2 Beat 2 | document, indicate, suggest；for I 类：档位化措辞 | demonstrates, establishes design space, the first multi-module campus platform | I 类措辞严格依 Prompt B audit 档位 |
| §2.3 Beat 3 | we propose, we distill, commonly discussed；Identity primitive：档位化措辞 | the canonical framework, validated primitives | **Identity primitive 严格依 Prompt A audit 档位，不得越档** |
| §4.1 Beat 4 | we observe, reports indicate, median value is, N=X responses | majority think, statistics confirm, significantly | 每 finding 标注 N |
| §4.2 Beat 5 | resonates with, parallels, counterintuitively；**limited to Driver/Both subset (N=19)** | confirms, replicates, proves the same phenomenon；全样本混合报告 | **子集切分决策必须 justify，Rider 对照必须报告** |
| §5 Beat 6 | we designed, motivated by, in response to, implementation | effective, successful, proves, validates | F5 attribution 到 subset 层级 |
| §6 Pipeline | evidence-chain organization tool, audit trail；**negative audit** | research agent, automated discovery, validated pipeline | **§6.2 必须含 negative instance** |
| §7.2 Beat 7 | may reproduce, we acknowledge, scope-limited | we address, we prevent, we solve | **三层 sample skew 分开披露** |

---

## Part 7. v4.1 → v4.2 改动清单

### 7.1 数据口径类改动

| 项目 | v4.1 | v4.2 |
|------|------|------|
| 总 N 口径 | "117/50" | "111 eligible / 44 finished" |
| 母语分母 | "82% Mandarin" | "79% of respondents who reported native language (72/91)" |
| F1 pricing | 29/33 | 28/32 |
| F1 availability | 24/33 | 23/32 |
| F3 数字 | 70.1/65.9/64.4/61.4/54.7/54.2/51.5 | 69.1/67.3/63.5/60.5/55.4/54.9/50.9（排序不变）|
| F5 基础样本 | 全样本 N=30 | Driver/Both 子集 N=19 + Rider-only 对照 N=12 |
| F2 分母说明 | 只报 17/72 vs 1/15 | 17/72 vs 1/15 + Q15 应答子集 17/21 vs 1/2 双披露 |

### 7.2 结构类改动

| 项目 | v4.1 | v4.2 |
|------|------|------|
| Finding 总数 | F1–F5 | F1–F6（新增 F6：Q23_1/2/3 司机空座意愿）|
| Beat 5 标题 | Driver-Side Tolerance | Driver-**Subset** Tolerance |
| Beat 5 图表 | 1 张 4 维 bar chart | 1 张 3×4 全样本/driver/rider 对比图 |
| §6.2 段落数 | 3（全 positive）| 4（¶1 positive / ¶2 positive / **¶3 negative** / ¶4 positive）|
| §7.2 ¶2 Sample Skew | 单层 | **三层**（主样本 / 子集 / 完成率）|
| Part 5 对齐表 | 7 列 | **8 列**（新增 min_edges_per_chain）|
| Identity primitive 措辞 | 平摊表述 | **档位化**，依 Prompt A audit 输出 |
| I 类 primitive 措辞 | 平摊表述 | **档位化**，依 Prompt B audit 输出 |

### 7.3 Pipeline 侧对应改动（详见 `pipeline_v4.2_modification_guide.md`）

- Prompt A：E 类 manual inclusion（≥4 篇 native `.edu` 文献）
- Prompt B：I 类核查与补强
- **Prompt E（v4.2 新增）**：H 类细分，支撑 driver-subgroup 的 X1/X2 claims
- Prompt C：query expansion（corpus +40–60%）
- Prompt D：edge extraction 提升（含 H-subgroup 与 F5 evidence 的强 edge）
- Phase 4 F5 evidence_inventory 改为双子集报告
- §6.2 的 negative audit 需要 pipeline 端提供 audit bundle

### 7.4 未改动事项（继承 v4.1）

- 三个 contribution 主线不变
- 候选标题不变
- 目标投稿不变（CHI/CSCW/DIS full paper 或扩展期刊）
- §5 六模块结构不变
- §5.8 四个设计决策不变（只在 §5.8.3 加子集 attribution）
- 7-Beat ↔ Section 对应不变
- 页数分配微调（§4.1 从 1.2 降到 1.1，§4.2 从 0.8 升到 0.9），总体 13.4 页不变

---

**文档版本**：v4.2 (Full Long only)
**创建日期**：2026-04-22
**对齐 pipeline**：research-agent 8-phase, `phase_contracts.py` 7-beat 硬约束
**对齐 pipeline 指南**：`pipeline_v4.2_modification_guide.md`
**上游数据**：Cornell_Carpool_System_Survey_April_21__2026_22_55.csv（问卷真实数据核对已完成）
**取代**：`paper_outline_v4.md` (v4.1)
