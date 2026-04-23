# CampusRide Paper Outline v4.1 (Full Long Version)

> **作用**：在 research-agent pipeline 的 7-beat 硬约束下，承载三个 contribution 主线的 **12-15 页 mid-tier conference / 扩展期刊版** 大纲。Compact 短版已移除。
>
> 三个 contribution 主线：
> ① CampusRide 作为 identity-verified **六模块** 校园平台的设计案例（每模块单独一小节）
> ② 拼车模块作为深度实证案例（基于 N=117 问卷）
> ③ research-agent 作为 thesis-conditioned 文献综述的方法论贡献（**独立成节**）
>
> **约束**：pipeline `phase_contracts.py` 硬性要求 7 个 beat。论文 section 结构必须一一对应。

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
(2) 基于 N=117 前期问卷的拼车模块深度实证分析，揭示了三个可迁移
    的设计发现——.edu 身份验证作为信任原语、国际学生群体的草根
    协调实践、以及司机对评分公平性的反直觉敏感；
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

### 1.1 Section 级结构（12-15 页）

| Section | 内容 | 页数 | 对应 beat |
|---------|------|------|----------|
| **§1 Introduction** | 动机 + 三 contribution 声明 | 1.0 | — |
| **§2 Related Work** | 三条文献线 | 2.5 | Beat 1-3 |
| §2.1 | Small-town campus transportation & coordination gaps | 0.7 | Beat 1 |
| §2.2 | Grassroots coordination + integrated campus platforms | 1.0 | Beat 2 |
| §2.3 | Design primitives: identity, safety, rating, rewards | 0.8 | Beat 3 |
| **§3 Methodology** | 问卷 + pipeline 两种方法 | 1.0 | — |
| §3.1 | Formative survey protocol | 0.5 | — |
| §3.2 | Literature synthesis via research-agent | 0.5 | — |
| **§4 Formative Survey Findings** | 问卷结果 | 2.0 | Beat 4-5 |
| §4.1 | Passenger-side WTP and motivations | 1.2 | Beat 4 |
| §4.2 | Driver-side tolerance & the rating-fairness asymmetry | 0.8 | Beat 5 |
| **§5 CampusRide Platform Design** | 六模块平台 + 拼车 deep-dive | 3.5 | Beat 6 |
| §5.1 | Platform overview & shared design primitives | 0.8 | Beat 6 |
| §5.2-5.7 | Six modules, one subsection each | 1.5 | Beat 6 |
| §5.8 | Carpool deep-dive (four design decisions) | 1.2 | Beat 6 |
| **§6 Research-Agent Pipeline as Methodology Contribution** | 独立 contribution 章节 | 1.5 | — |
| §6.1 | Architecture & 8-phase flow | 0.6 | — |
| §6.2 | Audit trail: how the pipeline shaped this paper | 0.6 | — |
| §6.3 | Scope & honest limitations of the pipeline | 0.3 | — |
| **§7 Discussion** | 反思 + 限制 | 1.5 | Beat 7 |
| §7.1 | General reflections on platform design | 0.6 | — |
| §7.2 | Adversarial scoping & limitations | 0.9 | Beat 7 |
| **§8 Conclusion** | | 0.4 | — |
| **References** | | 1.2 | — |
| **正文合计** | | **~13.5** | |
| **含参考文献合计** | | **~14.7** | |

**体量落在 12-15 页区间**，符合 CHI/CSCW full paper 或扩展期刊常见上限。

### 1.2 7-Beat ↔ Section 对应表（pipeline 接口）

| Beat | 论文 Section | 主题 | Pipeline 产物映射 |
|------|-------------|------|-------------------|
| **Beat 1** | §2.1 | 小城校园交通 + 协调缺口 | `narrative_chains[0]`、A+B 类 |
| **Beat 2** | §2.2 | 草根协调 + 集成平台文献 | `narrative_chains[1]`、C+D+I 类 |
| **Beat 3** | §2.3 | 四个 design primitive | `narrative_chains[2]`、E+F+G+H 类 |
| **Beat 4** | §4.1 | 乘客侧 WTP + 动机 | `evidence_inventory[3]` + 问卷 |
| **Beat 5** | §4.2 | 司机侧容忍度 + 反直觉发现 | `evidence_inventory[4]` + 问卷 |
| **Beat 6** | §5 (全) | 六模块平台 + 拼车 deep-dive | `evidence_inventory[5]` + 系统文档 |
| **Beat 7** | §7.2 | 对抗性 scoping + 限制 | `contradictions.json` + J 类 |

注意：**§6 Research-Agent Pipeline 不占 beat slot**——它是方法论章节，不是证据链中的一环。pipeline 作为 contribution 通过 §3.2 和 §6 两处共同呈现。

---

## Part 2. 每个 Beat 的详细内容

### Beat 1 | §2.1 Small-Town Campus Transportation & Coordination Gaps（0.7 页）

**角色**：动机的上半段——场景缺口存在。

**Anchor paper**：Shaheen & Cohen shared mobility 综述类（或等价的小城 rideshare 缺口文献）

**Spine (4-5 篇)**：
- 小城 / 大学 rideshare 服务覆盖文献
- 大学生出行可达性 / food / social coordination 需求文献
- 通用分享经济 (sharing economy) 在小城的局限文献
- （可选）Ithaca / Cornell 本地交通分析 grey literature

**要讲的事**（两段）：
- ¶1：主流商业 rideshare (Uber/Lyft) 在小城校园情境下存在结构性服务缺口——pricing 和 availability 两个维度。文献里有若干实证但不系统
- ¶2：**关键承上启下**——这个缺口不只是拼车问题。学生群体在出行、二手交易、活动组织、日常社交等**多个面向**都面临协调摩擦，这些摩擦共同构成一个"campus coordination gap"。**为 Beat 2 的多模块平台论证铺垫**

**Finding 引用**：F1（Uber 感知贵 29/33、可用性 24/33）——放在第 1 段结尾作 preview

**诚实纪律**：
- 允许说：`exists` / `is documented` / `motivates`
- 禁止说：`has been empirically proved at scale` / `quantified`

### Beat 2 | §2.2 Grassroots Coordination + Integrated Campus Platforms（1.0 页）

**角色**：动机的下半段——既存实践 + 多模块平台的文献基础。**这一 beat 承载双论证线，是全文最长的 Related Work 子节**。

**Anchor paper**：Sawyer & Chen 类国际学生 WeChat 研究

**Spine (7-8 篇)**：
- C 类 3 篇：WeChat/WhatsApp 群协调、self-organized 社区平台
- D 类 2 篇：国际学生 US 大学数字实践
- I 类 2-3 篇：super-app / integrated community platform 文献

**要讲的事**（四段）：
- ¶1：国际学生已自发通过通讯软件群组协调拼车——这是**非正式基础设施** (informal infrastructure) 存在的最直接证据。F2 preview 放这里
- ¶2：这类协调**不限于拼车**。同一 WeChat 群里也在做二手交易、活动召集、信息共享、应急求助。学生群体已在多域协调中依赖**单一社交通道**。这是"多模块平台"合法性的**经验锚点**
- ¶3：**文献层面**，super-app / integrated community platform 研究指出集成设计的价值（引 I 类 1-2 篇）。但这些文献多聚焦大众市场（微信、Grab、Gojek 等）或一般社区平台。**针对校园 + 封闭 scope 的多模块集成研究尚不成熟**——这是 CampusRide 的设计空间
- ¶4：过渡到 Beat 3：要把上述草根实践形式化，需要什么 design primitive？下一节回答

**Finding 引用**：F2（17/72 Mandarin vs 1/15 English 通过微信找拼车）放在 ¶1 末

**诚实纪律**：
- 草根协调文献较稳——可以用 `document` / `indicate`
- I 类 super-app 文献若薄，¶3 必须降级为 `initial inquiry` 而不是 `established design space`
- 不宣称 CampusRide 是"第一个"多模块校园平台

### Beat 3 | §2.3 Design Primitives: Identity, Safety, Rating Fairness, Rewards（0.8 页）

**角色**：框架——从文献中提炼出四个 design primitive，为 §5 的系统设计预铺轨道。

**Anchor paper**：Ert, Fleischer & Magen 2016 Airbnb trust（或 Resnick & Zeckhauser reputation systems）

**Spine (6-8 篇)**：
- E 类 2 篇：`.edu` / campus-scoped identity verification
- F 类 2 篇：shared mobility safety、real-time location、SOS
- G 类 1-2 篇：gamification in coordination / mobility
- H 类 2 篇：peer rating、algorithmic management、rating fairness

**要讲的事**（四段，每 primitive 一段）：

- ¶1 **Identity primitive**：身份验证在分享经济中的经典作用，特化到 institutional / `.edu` scoping。在封闭社区下可以降低陌生人协调成本
- ¶2 **Safety primitive**：shared mobility 中的主动安全设计——实时位置共享、SOS、emergency contact。文献显示这些 feature 对用户 trust 的提升
- ¶3 **Rating-fairness primitive**：peer rating 作为 reputation 机制的长处与 algorithmic management 批评带出的公平性问题。引 Rosenblat & Stark、Lee et al. 等
- ¶4 **Rewards/gamification primitive**：积分激励在 coordination / mobility 中的应用 + 对内在动机挤出的 risk（引 Koivisto & Hamari、Deterding 等）

**Finding 引用**：无——pure 文献

**诚实纪律**：
- 四 primitive **并列**，不在这一 beat 做价值排序。**Beat 4/5 的经验发现 + Beat 6 的设计决策才承担排序工作**
- 每个 primitive 至少 1 篇经典引用 + 1 篇最新（2022+）引用

### Beat 4 | §4.1 Formative Survey: Passenger-Side WTP & Motivations（1.2 页）

**角色**：核心实证 I——乘客视角的需求、痛点、WTP、动机。

**Anchor paper**：无（primary data）

**Supporting**：问卷数据 + Beat 3 design primitives 的回指

**要讲的事**（四段 + 表/图）：

- ¶1 (recap)：问卷 methodology 放 §3.1，这里只 recap——N=117 启动、50 完整；82% Mandarin 母语；本节报告每题完成响应者子集，N 每题报告
- ¶2 (交通缺口量化)：F1 数字表或 bar chart——Uber pricing 29/33 偏贵、availability 24/33 问题
- ¶3 (WTP 安全特性排序)：F3 完整表——实时位置 70.1%、`.edu` 65.9%、SOS 64.4%、driver experience 61.4%、auto trip-sharing 54.7%、social connections 54.2%、interior photos 51.5%。**全部 7 项 ≥50%** 是一个强 observation，值得强调
- ¶4 (动机结构)：F4 motivation bar——财务 63.6、游戏化 48.3、社交 45.6、环保 44.5。**双梯队动机**作为 Beat 6 积分模块辅助化设计的依据

**表/图**：1 张 WTP 排序表 + 1 张 motivation bar chart

**Finding 引用**：F1、F3、F4 全量

**诚实纪律**：
- **不做任何 inferential statistics**（no t-test、no p-value、no 显著性声明）
- 承认 82% Mandarin 母语的 scope-setting 性质——**不当 bias 遮掩，也不当论文卖点**

### Beat 5 | §4.2 Formative Survey: Driver-Side Tolerance & the Rating-Fairness Asymmetry（0.8 页）

**角色**：核心实证 II。**论文最有辨识度的 counterintuitive finding 所在**。

**Anchor paper**：Rosenblat & Stark 2016

**Spine**：H 类 rating fairness 文献 1-2 篇 + F 类 rideshare driver experience 1 篇

**要讲的事**（两段 + 表/图）：

- ¶1 (司机容忍四象限)：Q24 数据——迟到 42.7、改路线 44.8、改目的地 33.0、**不公平评分 26.6**。关键 observation：司机最难忍的不是乘客行为失当，而是来自评分系统本身的不公平
- ¶2 (解读 & 文献对话)：Rosenblat & Stark 等 algorithmic management 研究早已指出 gig worker 对平台评分的焦虑。我们的 finding 在**校园 peer carpool 这一更小规模、更高信任**的情境下**复现了这一焦虑**。这指向：即使有 `.edu` 身份验证这类强信任信号，**评分系统本身的公平性仍是独立的、不可替代的 design concern**

**表/图**：1 张 4 维 tolerance bar chart，把 26.6 明显低于其他三项画出来

**Finding 引用**：F5

**诚实纪律**：
- 不把 F5 过度泛化到所有 peer rating 系统
- N=30 的样本上的 observation，需要更大规模验证
- 用 `resonates with` / `parallels` 而不是 `confirms`

### Beat 6 | §5 CampusRide Platform Design（3.5 页，全文最大章节）

**角色**：核心贡献——六模块平台的设计案例 + 拼车模块的深度设计。

这一 section 分三层：§5.1 platform overview、§5.2-5.7 六模块各一小节、§5.8 拼车深度。

#### §5.1 Platform Overview & Shared Design Primitives（0.8 页）

- ¶1：CampusRide 架构——Vue 3 + Express + Supabase + Socket.IO 一句话技术栈。**一张架构图**（占 0.4 页）展示 6 个模块 + 共享的 auth / identity / messaging / points 四层基础设施
- ¶2：**共享 design primitive 矩阵**——6 模块 × 4 primitive 的小表格：
  - 拼车：Identity ✓ / Safety ✓✓ / Rating ✓✓ / Rewards ✓
  - 二手市场：Identity ✓ / Safety ✓ / Rating ✓ / Rewards ✓
  - 活动：Identity ✓ / Safety ○ / Rating ○ / Rewards ✓
  - 群组：Identity ✓ / Safety ○ / Rating ○ / Rewards ○
  - 消息：Identity ✓ / Safety ○ / Rating ○ / Rewards ○
  - 积分：(跨模块 meta-module)
- ¶3：过渡——`.edu` 身份层是所有模块的共同准入；积分模块是跨模块 meta-layer；拼车的 safety + rating 是最密集的 primitive 使用，因此深度案例选拼车

#### §5.2 Carpool Module (overview)（0.25 页）

- 功能定位：校园内部 / 短途 / 长途 三类距离拼车匹配
- 用到的 primitive：四个全用到
- 关键用户场景：Ithaca 内通勤、去 NYC/Boston 长途返家
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
- 证据支撑：F3 的 65.9% WTP uplift（median 79%）
- 实现简述：注册流程、验证机制、在 driver/passenger profile 中的展示方式
- 局限承认：`.edu` 只验证身份，不验证驾驶能力、不防止行为失当

##### §5.8.2 Safety Skeleton (0.3 页)
- 设计决策：实时位置共享 + SOS 按钮作为行程进行中的两个主动安全层
- 证据支撑：F3 的 70.1% + 64.4% WTP uplift
- 实现简述：Socket.IO 的 thread 房间机制；SOS 的短路径（一键联系紧急联系人）
- 局限承认：位置共享对隐私的 trade-off；SOS 的响应链条依赖校外资源

##### §5.8.3 Rating System with Fairness Consideration (0.35 页) — **论文最具创新性的设计段落**
- 设计决策：
  - 双向评分（乘客 ↔ 司机对称）
  - 评分理由必填
  - 评分公开前的异议窗口（例如 24 小时）
  - 跨行程的评分趋势保护——单次异常评分不决定司机总体标签
- 证据支撑：F5 的 26.6 vs 其他 33-45 的显著低容忍
- 对话 algorithmic management 文献：我们的设计是否真的缓解了那种焦虑？**承认本文无部署数据可以验证**，作为 future work
- 局限承认：异议窗口可能被操纵；跨行程保护可能减慢对真正问题司机的识别

##### §5.8.4 Gamification as Secondary Incentive (0.25 页)
- 设计决策：积分作为辅助激励，不主导经济动机
- 证据支撑：F4 的 48.3（gamification 第二梯队）
- 实现简述：拼车积分与跨模块积分池联通
- 局限承认：积分机制可能诱导 gaming behavior（见 Beat 7 讨论）

**Finding 回指汇总**：F3 × 3 次、F4 × 1 次、F5 × 1 次——五次 finding 回指使 §5.8 每个小节都有经验依据

**诚实纪律**：
- 避免 `effective` / `successfully` / `proves`
- 允许 `we designed` / `we implemented` / `motivated by` / `in response to finding X`

### Beat 7 | §7.2 Adversarial Scoping & Limitations（0.9 页）

**角色**：全篇的诚实性锚点。**这一 beat 对 pipeline contradiction reviewer 评分至关重要**。

**Anchor paper**：Rosenblat & Stark、Lee et al. 或其他 algorithmic management 批评

**Spine**：`contradictions.json` 打捞出的 5 个 focus

**要讲的事**（五段 adversarial scoping）：

- ¶1 (Formalization Risk)：形式化草根实践可能复制商业 rideshare 的 algorithmic management harm。我们的 rating fairness 设计是**响应**而非**解决**这一风险
- ¶2 (Sample Skew)：82% Mandarin 母语样本偏态限制 findings 泛化性。英语母语学生 N=15，对他们的任何判断（包括"他们不用微信群"）都有较大不确定性
- ¶3 (No Deployment Evaluation)：本文 stop 在设计案例阶段，未提供部署数据。四个 design decision 之间的相对效力未在 real-world 中被比较
- ¶4 (Scope Boundary of `.edu`)：身份验证解决身份问题，不解决行为问题——不验证驾驶能力、不阻止恶意行为、不替代平台治理
- ¶5 (Gamification Risk)：跨模块积分系统可能在某些模块（比如拼车）产生 gaming behavior（刷积分、虚假行程）。本文没有数据评估这一风险

**诚实纪律**：
- 每段引 1 篇相关反证文献，不空泛自省
- 这一 beat 主动求 pipeline contradiction reviewer 打高分——写完跑一遍 Phase 5 看这里 honesty 分

---

## Part 3. 非 Beat Section 的内容

### §1 Introduction（1.0 页）

**四段结构 + 三 contribution bullet**：
- ¶1 (Hook)：小城校园 + 国际学生 + 草根协调的三重交叉场景——用 Cornell/Ithaca 作为 representative case
- ¶2 (Gap + Practice)：Beat 1 + Beat 2 的 teaser。"交通不只是交通"是承接全文的钩子
- ¶3 (Approach)：三件事——N=117 前期问卷 + CampusRide 六模块平台（拼车 deep-dive）+ research-agent pipeline 支撑文献综述
- ¶4 (Contribution)：Part 0.2 的三 bullet

### §3 Methodology（1.0 页）

两个小节，各 0.5 页。

#### §3.1 Formative Survey Protocol（0.5 页）

- 招募方式、平台（Qualtrics）、时间段
- 同意声明的原文引用（一两句）
- N=117 启动、50 完整的 breakdown
- **82% Mandarin 母语 scope disclosure**（disclose as scope, not bias）
- 问题设计的 7 大模块简述（demographics / travel patterns / pain points / Uber perception / safety WTP / motivations / driver tolerance）
- 本文分析立场：descriptive only

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
  - Phase 2 Classification (A-J taxonomy)
  - Phase 2.5 Deep Extraction
  - Phase 3 Relationship Graph + Evidence Sufficiency
  - Phase 3.5 Narrative Chains
  - Phase 3.7 Contradiction Map
  - Phase 4 Evidence Inventory
  - Phase 5 Five-Reviewer Evaluation
- **一张图**：8 阶段流水线示意（0.25 页）

#### §6.2 Audit Trail: How the Pipeline Shaped This Paper（0.6 页）

**这是 §6 最有说服力的一段**——用本文自己作为 case study 展示 pipeline 的 operational value。

- ¶1：具体审计追溯——Section 2 的 anchor papers 来自 `narrative_chains.json`；§7.2 的 5 个 adversarial scope 直接映射 pipeline `contradictions.json` 的 5 个 focus；§5 的 finding 回指次数由 `evidence_inventory.json` 检查覆盖
- ¶2：Phase 5 reviewer feedback 对本文的修改历程——具体列 1-2 个 reviewer iteration（比如"初稿 honesty 分 0.72，reviewer 指出 §5.8 有 `effective` 表述，改为 `designed to address` 后升至 0.84"）
- ¶3：可复现性声明——pipeline 和本文的全部 config、`state.json`、各阶段产物都开源

#### §6.3 Scope & Honest Limitations of the Pipeline（0.3 页）

- 一段明确说清楚 pipeline **不是**什么：
  - 不是 open-ended research agent
  - 不是 automated thesis generator
  - 不是 gap discovery tool（`gaps_ranked.json` 是诊断信号不是结论）
  - 仅 abstract-first，不做 full-text truth extraction
- 给出对后续使用者的建议（参考 `CURRENT_STATUS_AND_RECOMMENDATIONS.md` 第 5-6 节）

### §7.1 General Discussion（0.6 页）

三段：
- ¶1 (From Grassroots to Formal)：反思 `.edu` 验证作为介于商业 app 和草根群之间的第三种信任架构
- ¶2 (Cross-Module Transferability)：拼车模块的设计原语如何在 marketplace / activities / groups 中再利用。指向"模块共享设计原语"的 methodological claim
- ¶3 (Pipeline-Assisted Design Research)：反思 research-agent 在本研究中的角色——让文献综述 auditable，contradiction reviewer 推动 §7.2 adversarial scoping 的深度

### §8 Conclusion（0.4 页）

四句话：
- 小城校园存在多面向协调缺口，国际学生草根实践给出具体形态
- CampusRide 把这些实践形式化为六模块 identity-verified 平台
- 拼车模块的深度案例展示了四个设计原语如何从 survey findings 推到实现
- research-agent pipeline 作为可复用方法论工具开源，供 design research 社区使用

---

## Part 4. 页数最终汇总

| 分组 | 页数 |
|------|------|
| §1 Introduction | 1.0 |
| §2 Related Work (Beat 1-3) | 2.5 |
| §3 Methodology | 1.0 |
| §4 Formative Findings (Beat 4-5) | 2.0 |
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
- Appendix C：完整 N 每题报告 + 所有交叉表
- Appendix D：pipeline 审计追溯完整日志

---

## Part 5. 每个 Beat 与 Pipeline 产物的精确对应（对齐表）

这张表是本大纲和 `pipeline_v4_migration_and_config.md` 的**共享主键**。

| Beat | 论文 Section | Pipeline 类别 | narrative_chains 索引 | contradictions focus | reviewer 约束点 | Finding 引用 |
|------|-------------|--------------|--------------------|--------------------|---------------|-------------|
| 1 | §2.1 | A + B | [0] | F1 (Gap vs. Substitute) | honesty: 不写成 empirically quantified | F1 (preview) |
| 2 | §2.2 | C + D + I | [1] | F2 (Grassroots Legitimacy) | coverage: C/D/I 类必须补料 | F2 |
| 3 | §2.3 | E + F + G + H | [2] | 无专属 focus | narrative: 四 primitive 并列 | — |
| 4 | §4.1 | — (primary data) | [3] | 无 | honesty: no inferential stats | F1, F3, F4 |
| 5 | §4.2 | H + F（对话） | [4] | F4 (Rating Fairness) | gap: 不过度泛化 F5 | F5 |
| 6 | §5 (全) | — (artifact) | [5] | F3 (.edu), F5 (Gamification) | honesty: no "effective" | F3, F4, F5 |
| 7 | §7.2 | J + H | [6] | 所有 5 focus | contradiction: ≥5 critical | — |

---

## Part 6. 诚实性纪律总表（写作时必守）

| Section | 允许的动词 | 禁止的动词 |
|---------|-----------|-----------|
| §2.1 Beat 1 | exists, motivates, is documented, points to | has been proved, is quantified, definitively shows |
| §2.2 Beat 2 | document, indicate, suggest; for super-app: `initial inquiry` | demonstrates, establishes design space, the first multi-module campus platform |
| §2.3 Beat 3 | we propose, we distill, commonly discussed | the canonical framework, validated primitives |
| §4.1 Beat 4 | we observe, reports indicate, median value is | majority think, statistics confirm, significantly |
| §4.2 Beat 5 | resonates with, parallels, counterintuitively | confirms, replicates, proves the same phenomenon |
| §5 Beat 6 | we designed, motivated by, in response to, implementation | effective, successful, proves, validates |
| §6 Pipeline | evidence-chain organization tool, audit trail | research agent, automated discovery, validated pipeline |
| §7.2 Beat 7 | may reproduce, we acknowledge, scope-limited | we address, we prevent, we solve |

---

**文档版本**：v4.1 (Full Long only)
**创建日期**：2026-04-22
**对齐 pipeline**：research-agent 8-phase, `phase_contracts.py` 7-beat 硬约束
**下游对齐文档**：`pipeline_v4_migration_and_config.md`、`local_ai_risk_resolution_prompts.md`
