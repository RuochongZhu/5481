# Research-Agent Pipeline v4 改造规范

> **作用**：按 `paper_outline_v4.md` 反推的 pipeline 具体改造规格。每一条改造都服务于大纲中某个 beat、某个 section、某个 finding。两份文档通过 `paper_outline_v4.md` 的 Part 6（Beat ↔ Pipeline 对应表）保持同步。
>
> **范围约束**：
> - **不改代码**：`main.py`、`state_manager.py`、`phase_contracts.py`、`api_client.py`、`utils.py`、`scoring.py` 一行不动
> - **改配置**：`config/*.json` 全部替换为 carpool + multi-module 主题
> - **改 prompt 内嵌字符串**：`phase3_5_narrative.py` / `phase3_7_contradiction.py` / `phase5_evaluate.py` 里硬编码的 thesis、beat_definitions、focus_questions、reviewer context
> - **state 迁移**：L_auth 时代的 `state.json` 和产物在切到新分支后重置
>
> **pipeline 硬约束摘要**（来自 `phase_contracts.py`）：
> - 7 个 beat 必须存在
> - 5 个 reviewer 维度必须各自给分（narrative / contradiction / gap / coverage / honesty）
> - action 必须是 `done / backtrack / human` 之一
> - 每个 narrative beat 必须有 `anchor_paper` + `spine` + `paragraph_outline`
> - evidence_inventory 每个 beat 必须有 `core_papers`（非空）

---

## Part 1. Git 迁移前置（你已决定，只做 reference）

你说已经决定了 git 策略。这里不做建议，只列一次迁移必须做的**5 个动作**，方便你写迁移脚本时参考：

1. 当前分支（假设是 `main` 或 `l_auth_v3`）打 tag `l_auth_v3_final_snapshot`，保留所有 L_auth 成果
2. 归档 `data/processed/`、`analysis/`、`output/`、`state.json` 到 `archive/l_auth_v3/`
3. 新分支（`carpool_v4` 或继续 `main`）从干净环境开始：重建空的 `data/processed/`、`analysis/`、`output/`；删除或重置 `state.json`
4. `config/*.json` 替换为下面 Part 2 的新内容
5. 三个 phase 文件里的 prompt 字符串替换为 Part 3、Part 4、Part 5 的内容

---

## Part 2. Config 层改造

### 2.1 `config/search_queries.json`

**新 A-J 10 类分类**（X 保留给 irrelevant，pipeline 原生约定）。每类 3-4 query，总 query 数 ~30-32。

对齐大纲的哪个 beat：

- A + B → Beat 1
- C + D + I → Beat 2
- E + F + G + H → Beat 3
- J → Beat 7

```json
{
  "version": "v4.0",
  "thesis_reference": "small-town campus multi-module platform with carpool deep-dive",
  "categories": {
    "A": {
      "name": "Small-town / Campus Transportation Gap",
      "supports_beats": [1],
      "queries": [
        "small town university rideshare transportation gap",
        "college campus Uber Lyft availability pricing",
        "rural student transportation access",
        "campus mobility underserved populations"
      ]
    },
    "B": {
      "name": "Peer-to-Peer Ridesharing & Sharing Economy Trust",
      "supports_beats": [1, 3],
      "queries": [
        "peer-to-peer ridesharing trust empirical",
        "sharing economy identity verification signals",
        "Airbnb Uber trust reputation systems",
        "stranger trust online platform economy"
      ]
    },
    "C": {
      "name": "Grassroots / Informal Coordination Platforms",
      "supports_beats": [2],
      "queries": [
        "WeChat group coordination informal community",
        "WhatsApp ridesharing self-organized",
        "messaging app community coordination",
        "informal digital infrastructure self-organized"
      ]
    },
    "D": {
      "name": "International Students Digital Practices US Universities",
      "supports_beats": [2],
      "queries": [
        "Chinese international students WeChat US university",
        "international student digital acculturation American campus",
        "international student mobility practice United States",
        "immigrant student community digital platform"
      ]
    },
    "E": {
      "name": "Identity Verification & .edu-Scoped Platforms",
      "supports_beats": [3, 6],
      "queries": [
        "campus scoped platform identity verification",
        "dot edu email verification trust signal",
        "closed community online identity design",
        "institutional verification online platform"
      ]
    },
    "F": {
      "name": "Safety in Shared Mobility",
      "supports_beats": [3, 6],
      "queries": [
        "rideshare safety real-time location sharing",
        "SOS emergency button mobility app design",
        "women safety rideshare peer transport",
        "shared mobility risk mitigation design"
      ]
    },
    "G": {
      "name": "Gamification in Coordination / Mobility",
      "supports_beats": [3, 6],
      "queries": [
        "gamification carpooling points incentive",
        "mobility app rewards behavioral change",
        "gamification sustainable transport motivation",
        "point system coordination platform"
      ]
    },
    "H": {
      "name": "Rating & Reputation System Design & Fairness",
      "supports_beats": [3, 5, 6, 7],
      "queries": [
        "rideshare rating system fairness driver",
        "peer reputation algorithmic management",
        "rating system bias platform mediated work",
        "peer feedback design fairness online platform"
      ]
    },
    "I": {
      "name": "Integrated Community Platforms & Super-Apps",
      "supports_beats": [2, 6],
      "queries": [
        "super app integrated community platform",
        "multi-module platform community design",
        "campus one-stop platform student",
        "closed community integrated services"
      ]
    },
    "J": {
      "name": "Algorithmic Management & Platform Labor Critique (Adversarial)",
      "supports_beats": [7],
      "queries": [
        "algorithmic management gig worker rating",
        "platform labor algorithmic control critique",
        "rideshare driver precarity platform",
        "algorithmic opacity worker wellbeing"
      ]
    }
  }
}
```

### 2.2 `config/seed_papers.json`

5 篇带 DOI 的 seed paper，每篇对应 1-2 个 beat。Phase 1 citation graph 从这 5 篇扩展。

> **注**：DOI 需要你在实际执行时用 Semantic Scholar 或 Google Scholar 核实最准确的版本。下面给出的是 citation key 参考。

```json
{
  "version": "v4.0",
  "seeds": [
    {
      "citation_key": "ShaheenCohen2019",
      "title": "Shared Mobility: Current Practices and Guiding Principles (or the latest Shaheen & Cohen shared mobility review)",
      "doi_placeholder": "TODO: verify DOI",
      "supports_beats": [1],
      "category": "A"
    },
    {
      "citation_key": "ErtFleischerMagen2016",
      "title": "Trust and reputation in the sharing economy: The role of personal photos in Airbnb",
      "doi": "10.1016/j.tourman.2016.01.013",
      "supports_beats": [3],
      "category": "B"
    },
    {
      "citation_key": "SawyerChen2012OrEquivalent",
      "title": "International students WeChat community coordination (to be verified)",
      "doi_placeholder": "TODO: verify or swap for closest equivalent",
      "supports_beats": [2],
      "category": "C"
    },
    {
      "citation_key": "RosenblatStark2016",
      "title": "Algorithmic Labor and Information Asymmetries: A Case Study of Uber's Drivers",
      "doi": "10.2139/ssrn.2686227",
      "supports_beats": [5, 7],
      "category": "H"
    },
    {
      "citation_key": "KoivistoHamari2019",
      "title": "The rise of motivational information systems: A review of gamification research",
      "doi": "10.1016/j.ijinfomgt.2018.10.013",
      "supports_beats": [3, 6],
      "category": "G"
    }
  ]
}
```

**执行注意**：W1 开始 Phase 1 前，这 5 个 DOI 必须全部验证真实并且在 Semantic Scholar 能查到——否则 Phase 1 的 citation graph 扩展会失败。

### 2.3 `config/lens_queries.json`

Lens 做**精准补料**，不做 bulk backbone。对应大纲中 coverage 最可能薄弱的 C/D/I/J 类：

```json
{
  "version": "v4.0",
  "purpose": "Lens targeted supplement for thin categories (C/D/I/J)",
  "queries": [
    {
      "query": "international students digital coordination US university 2020..2025",
      "target_category": "D",
      "max_results": 30
    },
    {
      "query": "WeChat group community coordination informal platform 2018..2025",
      "target_category": "C",
      "max_results": 30
    },
    {
      "query": "super app integrated community platform campus 2020..2025",
      "target_category": "I",
      "max_results": 25
    },
    {
      "query": "algorithmic management gig worker rating fairness 2018..2025",
      "target_category": "J",
      "max_results": 25
    }
  ]
}
```

### 2.4 `config/manual_core_inclusions.json`

强制收入的非检索条目——这些 pipeline 单靠检索通常找不到：

```json
{
  "version": "v4.0",
  "inclusions": [
    {
      "citation_key": "CornellCarpoolSurvey2026",
      "type": "primary_data",
      "title": "Cornell Carpool System Survey (Ruochong et al., 2026)",
      "n_respondents": 117,
      "supports_beats": [4, 5],
      "note": "Primary data for §3.1 and §3.2; treat as grey literature in classification"
    },
    {
      "citation_key": "CampusRideSystem2026",
      "type": "artifact",
      "title": "CampusRide Multi-Module Platform Technical Documentation",
      "supports_beats": [6],
      "note": "System artifact reference for §4"
    },
    {
      "citation_key": "ResearchAgentPipeline2026",
      "type": "method",
      "title": "Research-Agent: A Thesis-Conditioned Evidence Pipeline",
      "supports_section": "3.0.2",
      "note": "Methodology contribution, reference in §3.0.2 and Appendix B"
    }
  ]
}
```

### 2.5 `config/manual_exclusions.json`

明确排除：

```json
{
  "version": "v4.0",
  "exclusion_rules": [
    "pure autonomous vehicle technology without human coordination aspect",
    "pure transportation economics modeling without user/design perspective",
    "traffic flow optimization without social coordination aspect",
    "ridesharing pricing algorithm papers with no user experience dimension",
    "deep learning based demand prediction without design implication"
  ]
}
```

### 2.6 `config/manual_category_overrides.json`

用于 Phase 2 分类错误时的补丁。W2 跑完 Phase 2 后用 disagreements 文件定位具体该打补丁的论文。**W1 初始为空**：

```json
{
  "version": "v4.0",
  "overrides": {}
}
```

---

## Part 3. Phase 3.5 (Narrative Chains) 的 Prompt 改造

### 3.1 Thesis 字符串（全 pipeline 共享）

下面这段 thesis 字符串要**注入 `phase3_5_narrative.py`、`phase3_7_contradiction.py`、`phase5_evaluate.py` 三个文件**作为 shared constant。建议做法：在 `src/` 下新建 `thesis_v4.py` 统一托管：

```python
# src/thesis_v4.py

THESIS_V4 = """
Commercial ridesharing services (Uber/Lyft) underserve small-town
university settings, producing a multi-faceted coordination gap that
extends beyond transportation — to marketplace, activities, groups, and
other peer interactions (Beat 1). In this gap, students — especially
international students from messaging-app-centric cultures — have
self-organized grassroots coordination via WeChat/WhatsApp groups across
multiple domains; existing super-app and integrated-platform literature
provides partial but incomplete design guidance for this setting
(Beat 2). Four design primitives — institutional identity verification,
safety infrastructure, rating fairness, and gamification — emerge from
the literature as candidates for formalizing such grassroots practice
(Beat 3). A formative survey (N=117) on carpooling reveals high
willingness-to-pay uplift for .edu verification, real-time location
sharing, and emergency SOS, with financial motivations dominating and
gamification as a secondary motivator (Beat 4), and surfaces a
counterintuitive driver sensitivity to unfair ratings that exceeds
tolerance for late passengers or route changes (Beat 5). We designed and
implemented CampusRide, a multi-module identity-verified campus platform
comprising carpool, marketplace, activities, groups, messaging, and
points modules; the carpool module is developed in depth to
operationalize the four primitives in response to the survey findings
(Beat 6). We acknowledge that platform-mediated formalization may
reproduce algorithmic management harms documented in commercial
rideshare; the sample skew (82% Mandarin-native respondents) scopes
generalizability; no deployment evaluation is provided (Beat 7 —
adversarial).
"""
```

### 3.2 `phase3_5_narrative.py` 的 Beat 定义替换

找到 `BEAT_DEFINITIONS` 或类似的硬编码结构，替换为 7 个 beat 的新定义。每个 beat 必须指定 anchor category、spine categories、key finding reference：

```python
# 片段示意，实际代码需按原文件结构对齐

BEAT_DEFINITIONS_V4 = [
    {
        "beat": 1,
        "beat_name": "Small-town campus transportation and coordination gaps",
        "paper_section": "2.1",
        "anchor_categories": ["A"],
        "spine_categories": ["A", "B"],
        "target_paper_count": 4,
        "honesty_note": "Gap exists and is motivated by literature, but is not systematically quantified at scale",
        "narrative_verb_discipline": "use 'exists', 'motivates', 'is documented in'; avoid 'has been proved'"
    },
    {
        "beat": 2,
        "beat_name": "Grassroots coordination among international students and integrated campus platforms",
        "paper_section": "2.2",
        "anchor_categories": ["C", "D"],
        "spine_categories": ["C", "D", "I"],
        "target_paper_count": 6,
        "honesty_note": "Grassroots practice is well-documented; integrated platform literature is sparser and should be framed as 'initial inquiry' not 'established design space'",
        "narrative_verb_discipline": "use 'document', 'indicate'; when citing super-app literature, use 'suggest' not 'demonstrate'"
    },
    {
        "beat": 3,
        "beat_name": "Design primitives: identity, safety, rating fairness, rewards",
        "paper_section": "2.3",
        "anchor_categories": ["E", "H"],
        "spine_categories": ["E", "F", "G", "H"],
        "target_paper_count": 5,
        "honesty_note": "Present four primitives as parallel; do not value-rank them in this beat",
        "narrative_verb_discipline": "neutral definitional verbs"
    },
    {
        "beat": 4,
        "beat_name": "Formative survey: passenger-side WTP and motivations",
        "paper_section": "3.1",
        "anchor_categories": [],
        "spine_categories": [],
        "primary_data_ref": "CornellCarpoolSurvey2026",
        "target_paper_count": 0,
        "honesty_note": "Descriptive statistics only; N per item must be reported; 82% Mandarin disclosed as scope",
        "narrative_verb_discipline": "descriptive, no inferential claims"
    },
    {
        "beat": 5,
        "beat_name": "Formative survey: driver-side tolerance and the rating-fairness asymmetry",
        "paper_section": "3.2",
        "anchor_categories": ["H"],
        "spine_categories": ["F", "H"],
        "primary_data_ref": "CornellCarpoolSurvey2026",
        "target_paper_count": 2,
        "honesty_note": "Counterintuitive finding (rating-unfairness tolerance 26.6) should be contextualized with algorithmic management literature but not over-generalized",
        "narrative_verb_discipline": "tentative; 'suggests', 'resonates with'"
    },
    {
        "beat": 6,
        "beat_name": "CampusRide multi-module system design with carpool deep-dive",
        "paper_section": "4",
        "anchor_categories": [],
        "spine_categories": [],
        "primary_artifact_ref": "CampusRideSystem2026",
        "target_paper_count": 0,
        "honesty_note": "No deployment data. Design decisions must explicitly reference survey findings (F3-F5). .edu verification does not verify driving competence — state this limit inline",
        "narrative_verb_discipline": "'we designed'; avoid 'effectively', 'successfully'"
    },
    {
        "beat": 7,
        "beat_name": "Adversarial scoping: formalization risk, sample skew, no deployment, scope of .edu",
        "paper_section": "5.2",
        "anchor_categories": ["J", "H"],
        "spine_categories": ["H", "J"],
        "target_paper_count": 5,
        "honesty_note": "Each adversarial paragraph must cite at least one counterevidence paper. This beat is the honesty anchor of the paper.",
        "narrative_verb_discipline": "acknowledgment verbs; 'may reproduce', 'we do not claim', 'scope-limited'"
    }
]
```

### 3.3 Beat 4 / Beat 6 的特殊处理

Beat 4 和 Beat 6 的 `anchor_categories` 为空、`spine_categories` 为空。pipeline 原生 flow 可能会在 `ensure_narrative_chains_valid` 处抱怨"missing valid anchor_paper.paperId"。

**最小 workaround**（改 prompt，不改 contract 代码）：
- Beat 4：让 narrative agent 使用 `CornellCarpoolSurvey2026` 作为伪 anchor（通过 `manual_core_inclusions.json` 注入这个 citation key，并在分类时 override 为某个合适类别比如 `primary_data`）。如果这个方法对 `ensure_narrative_chains_valid` 的字段校验仍然不过，**backup 方案**是让 Beat 4 引用 1 篇最近的 rideshare motivation survey 作为伪 anchor，真正内容由 `paragraph_outline` 承载
- Beat 6：同理，`CampusRideSystem2026` 作伪 anchor

**建议的 decision**：如果 W3 跑 Phase 3.5 时 Beat 4/6 报错，先尝试伪 anchor，仍不过就在 prompt 里加 `"treat as primary-data beat, paragraph_outline carries all content"` 的 instruction。**只有在这两种都不过才考虑改 `phase_contracts.py` 放宽 primary-data beats 的 anchor 要求**——但这会突破"不改代码"的纪律，需要谨慎。

---

## Part 4. Phase 3.7 (Contradiction Map) 的 Prompt 改造

### 4.1 Focus Questions 替换

找到 `FOCUS_QUESTIONS` 或等价结构，替换为新 5 个 focus：

```python
FOCUS_QUESTIONS_V4 = [
    {
        "focus_id": "F1",
        "name": "Gap vs. Substitute",
        "target_beats": [1],
        "thesis_claim_under_test": "Commercial rideshare underserves small-town university settings",
        "adversarial_prompt": (
            "Search for literature indicating commercial rideshare services "
            "(Uber/Lyft) do NOT significantly underperform in small-town "
            "or university settings, or that existing substitutes (campus "
            "shuttles, taxi, public transit) adequately fill the gap. "
            "Identify at least 3 pieces of counterevidence if available."
        ),
        "expected_category_focus": ["A", "B"]
    },
    {
        "focus_id": "F2",
        "name": "Grassroots Legitimacy",
        "target_beats": [2],
        "thesis_claim_under_test": "Grassroots WeChat/WhatsApp coordination requires formalization",
        "adversarial_prompt": (
            "Search for literature arguing that grassroots / informal "
            "coordination platforms are ALREADY ADEQUATE and do not need "
            "formalization, or that formalization causes loss of community "
            "autonomy or trust. Identify ≥3 counterevidence pieces."
        ),
        "expected_category_focus": ["C", "D"]
    },
    {
        "focus_id": "F3",
        "name": ".edu as Trust Primitive",
        "target_beats": [3, 6],
        "thesis_claim_under_test": "Institutional .edu identity verification provides meaningful trust uplift",
        "adversarial_prompt": (
            "Search for literature, case studies, or incident reports where "
            "institutional identity verification (e.g., .edu email, campus "
            "card) FAILED to prevent fraud, harassment, or unsafe behavior. "
            "Also: literature arguing identity verification merely shifts "
            "risk rather than reducing it. Identify ≥3 counterevidence."
        ),
        "expected_category_focus": ["E", "F"]
    },
    {
        "focus_id": "F4",
        "name": "Rating Fairness as Independent Design Concern",
        "target_beats": [5, 6],
        "thesis_claim_under_test": "Driver sensitivity to unfair ratings requires dedicated fairness design",
        "adversarial_prompt": (
            "Search for literature arguing peer rating systems in rideshare "
            "work adequately WITHOUT dedicated fairness mechanisms, or that "
            "rating-fairness concerns are either overstated or better "
            "addressed by stronger identity signals alone. Identify ≥3 "
            "counterevidence pieces."
        ),
        "expected_category_focus": ["H"]
    },
    {
        "focus_id": "F5",
        "name": "Gamification Risk",
        "target_beats": [3, 6],
        "thesis_claim_under_test": "Gamification serves as a legitimate secondary incentive for carpooling",
        "adversarial_prompt": (
            "Search for literature documenting that gamification in "
            "mobility / coordination contexts produces unintended effects: "
            "crowding out of intrinsic motivation, gaming behavior, "
            "quality degradation, or equity concerns. Identify ≥3 "
            "counterevidence pieces."
        ),
        "expected_category_focus": ["G", "J"]
    }
]
```

### 4.2 Contradiction 输出结构保持不变

`phase3_7_contradiction.py` 产出的 `contradictions.json` 的 schema（`review_summary` + `focus_summary` + `contradictions[]`）**不用改**——`phase_contracts.py` 对此有明确校验，动了也白动。

### 4.3 Contradiction 打捞的 target 数量

pipeline 当前产出 `total_found = 37` / `critical_count = 18`（来自 docs 快照）。**carpool 主题初期**，合理期望：

- `total_found` ≥ 15
- `critical_count` ≥ 5
- 每个 focus 有 ≥2 条 contradiction

低于这个水位线，pipeline 诊断上 `contradiction=0.60` 以下，这时候要回 W1 补 J 类和 H 类文献。

---

## Part 5. Phase 5 (Evaluation) 的 Reviewer Context 改造

### 5.1 PAPER_CONTEXT 注入点

找到 5 个 reviewer 的 system prompt 构造点（通常在 `phase5_evaluate.py` 的一组 `build_reviewer_prompt` 或类似函数里），**在每个 reviewer system prompt 的开头注入**以下 context：

```python
PAPER_CONTEXT_V4 = """
EVALUATION CONTEXT — READ BEFORE SCORING:

This is a 10-page design case study paper for a mid-tier HCI conference
or extended workshop submission. It has THREE contribution claims:

(1) CampusRide — an identity-verified multi-module campus platform
(2) A deep-dive case on the carpool module, grounded in an N=117
    formative survey
(3) research-agent — a thesis-conditioned evidence pipeline supporting
    the literature synthesis

Evaluate accordingly, not as a PhD-length empirical paper:

- NOVELTY BAR: A well-scoped design case with survey-informed evidence
  and honest framing IS sufficient. Controlled experiments and
  deployment evaluation are NOT required.

- EVIDENCE BAR: N=117 formative survey (N≤33 on individual ordinal
  items) is a reasonable formative-stage sample. Do NOT apply
  inferential-statistics standards. No t-tests or p-values are expected
  or appropriate.

- SAMPLE SKEW: 82% Mandarin-native respondents is DISCLOSED as a
  scope-setting property. Evaluate whether the paper scopes its claims
  accordingly — NOT whether the sample is demographically balanced.

- MULTI-MODULE SCOPE: The paper claims a multi-module platform design
  but goes deep only on carpool. This is a deliberate scoping choice.
  Other modules are described at overview level. Evaluate whether the
  carpool deep-dive transferability-argument for other modules is
  honest — NOT whether each module is independently validated.

- METHODOLOGY CONTRIBUTION: The research-agent pipeline is presented as
  a methodology tool used by this paper, not as a stand-alone validated
  research agent. Do NOT evaluate the pipeline itself — evaluate how
  the paper uses it and whether its use is honestly framed.

- VERB DISCIPLINE: The paper is expected to use 'motivates',
  'suggests', 'informs', 'scopes' rather than 'proves', 'validates',
  'demonstrates'. Do NOT penalize the paper for cautious verbs; DO
  penalize over-claiming verbs.
"""
```

### 5.2 Reviewer 分数预期 & 回溯行为

5 个 reviewer 的期望表现区间（W5 跑 Phase 5 后对照）：

| 维度 | 期望区间 | 低于该区间的含义 & 应对 |
|------|---------|-----------------------|
| narrative | 0.70-0.85 | < 0.70：段落过渡硬、7 beat 跳跃。重写 `writing_outline.md` 后重跑 Phase 3.5 |
| contradiction | 0.75-0.90 | < 0.75：Beat 7 反证不足、Focus Question 未充分回应。补 J/H 类文献回 Phase 1 |
| gap | 0.75-0.90 | < 0.75：某 beat 主张超出文献支撑。**降级口径**而不是补料 |
| coverage | 0.70-0.85 | < 0.70：某类文献薄。回 Phase 1 补 Lens queries |
| honesty | 0.80-0.95 | < 0.80：有 over-claiming。做一轮 verb-sweep：把 proves/demonstrates 换成 motivates/suggests |

### 5.3 Action 决策

- `done`：`overall ≥ 0.80` 且 `honesty ≥ 0.80` → 写作阶段完成，进入 polish
- `backtrack`：`overall < 0.80` 且有明确 weakest dimension → 按 5.2 表处理
- `human`：`honesty < 0.70` 或同维度连续两轮回溯仍不升 → 停下来找导师

---

## Part 6. Pipeline 改造的 W1 启动动作清单

W1 周内必须完成（按顺序执行）：

1. **【git】** 按你的策略切好分支，旧产物归档，新分支的工作目录清空 `data/processed/`、`analysis/`、`output/`、删除 `state.json`
2. **【config】** 按 Part 2 写完 6 个 `config/*.json`；`seed_papers.json` 的 5 个 DOI 全部在 Semantic Scholar 验证
3. **【code string edit】** 新建 `src/thesis_v4.py` 承载 `THESIS_V4` 常量
4. **【code string edit】** 在 `phase3_5_narrative.py` 替换 `BEAT_DEFINITIONS`（Part 3.2）
5. **【code string edit】** 在 `phase3_7_contradiction.py` 替换 `FOCUS_QUESTIONS`（Part 4.1）
6. **【code string edit】** 在 `phase5_evaluate.py` 所有 reviewer system prompt 里注入 `PAPER_CONTEXT_V4`（Part 5.1）
7. **【state】** `python main.py --status` 确认是新分支的干净状态
8. **【smoke test】** `python main.py --phase 1`，跑 corpus assembly；跑完后检查 `corpus_unified.json` 是否有 ≥ 120 篇、每类至少 8 篇（J 和 I 类可以略少）

### W1 后的 pipeline run 时间表

| 周次 | Pipeline run | 检查点 |
|------|-------------|-------|
| W1 | Phase 1 | `corpus_unified.json` ≥ 120 篇；10 个类别都非空 |
| W2 | Phase 2 | `classified.json` 的 X 类比例 < 10%；C/D/I/J 类各 ≥ 5 篇 |
| W2 | Phase 2.5 | `deep_extracted.json` `avg_fill_rate` > 0.85 |
| W3 | Phase 3 | `gaps_ranked.json` 7 个 beat 都至少 adequate；Beat 4/6 会因为无文献而显示 "primary data beat"，这是正常 |
| W3 | Phase 3.5 | `narrative_chains.json` 7 个 beat 全部有 spine + paragraph_outline |
| W4 | Phase 3.7 | `contradictions.json` total ≥ 15, critical ≥ 5 |
| W4 | Phase 4 | `evidence_inventory.json` 7 个 beat 都有 core_papers |
| W5 | Phase 5 | `evaluation_result.json` overall ≥ 0.75, honesty ≥ 0.75, action = done/backtrack-actionable |

---

## Part 7. Beat ↔ Pipeline ↔ Finding 的完整对齐表（最终一致性检查）

这张表是**本文档和 `paper_outline_v4.md` 的共享主键**。两份文档的所有条目都应该能在这张表上找到自己的位置。

| Beat | 论文 Section | Pipeline 类别 | Seed Paper | Focus Q | Reviewer Caveat | Finding 引用 |
|------|-------------|--------------|-----------|---------|-----------------|-------------|
| 1 | §2.1 | A + B | ShaheenCohen2019 | F1 | honesty: no "empirically quantified" | F1 (preview) |
| 2 | §2.2 | C + D + I | SawyerChen 或等价 | F2 | coverage: C/D 必须补料 | F2 |
| 3 | §2.3 | E + F + G + H | ErtFleischerMagen2016 + KoivistoHamari2019 | — | narrative: 4 primitive 并列 | — |
| 4 | §3.1 | — (primary data) | CornellCarpoolSurvey2026 | — | honesty: no inferential stats | F1, F3, F4 |
| 5 | §3.2 | H + F | RosenblatStark2016 | F4 | gap: 不过度泛化 F5 | F5 |
| 6 | §4 | — (artifact) | CampusRideSystem2026 | F3, F5 | honesty: no "effective" 等 | F3, F4, F5 |
| 7 | §5.2 | J + H | RosenblatStark2016 | 所有 | contradiction: ≥5 critical | — |

**文档一致性校验规则**：如果你修改了 `paper_outline_v4.md` 里某个 beat 的 anchor 或 spine，同步修改本文件 Part 2（config）、Part 3（beat definition）、Part 7（对齐表）。反之亦然。

---

## Part 8. 已知风险 & 应对

| 风险 | 触发信号 | 应对 |
|------|---------|------|
| Beat 4/6 作为 primary-data/artifact beat 在 `ensure_narrative_chains_valid` 处失败 | Phase 3.5 抛 `PhaseContractError: missing valid anchor_paper.paperId` | 先尝试 Part 3.3 的伪 anchor 方案；不过关才考虑改 contract 代码 |
| 7 beat 与 pipeline v3 的 7 beat 冲突（旧 beat definition 残留） | Phase 3.5 输出 7 个 beat 但主题混淆 | 确认 `phase3_5_narrative.py` 的 `BEAT_DEFINITIONS` 确实替换为 v4；检查 `thesis_v4.py` 引入 |
| 三个 contribution 超出 reviewer 期望稀释单一贡献 | Phase 5 narrative < 0.70 且评语提到 "unclear primary contribution" | 把 research-agent 作为 contribution 降级：从 Part 0.2 的 (3) 移到 "methodology note"，或接受 Compact v4-A 的 tight framing |
| C/D 类文献过薄导致 Beat 2 只能引 2-3 篇 | Phase 2 分类后 C 类 < 5, D 类 < 5 | Lens 补料（已在 Part 2.3 准备），扩展 C/D queries |
| Beat 7 contradiction 打捞不足 | `contradictions.json` critical < 5 | 强化 Part 4.1 的 adversarial_prompt，或在 `manual_core_inclusions.json` 手动塞 3-5 篇 Rosenblat/Lee 等 algorithmic management critique |
| 反馈回路：reviewer 扣 coverage 分 → 补料 → 补料后 contradiction 又不足 | 连续两轮 Phase 5 跷跷板 | 停下来，回到 thesis statement 检查是否 overreach。通常 thesis 表述比 corpus 更容易改 |
| pipeline methodology 写进论文后审稿人要求验证 pipeline 本身 | 审稿意见："how do you validate research-agent?" | 准备 rebuttal: pipeline 是 internal tool，论文不 claim pipeline 本身的 validity；§3.0.2 已明确定位 |

---

## Part 9. 两份文档的同步规则

为保持 `paper_outline_v4.md` 和本文件的一致性，遵守：

- **主键是 Part 7 的对齐表**。任何修改都必须从这张表出发
- **单向改动禁止**。改一份文档时必须同步检查另一份
- **版本号同步**：两份文档共享一个版本号（v4.0、v4.1...）
- **破坏性改动清单**：如果要做下列改动，两份文档必须同时更新：
  - 任何 beat 的 paper_section 映射（如 Beat 2 从 §2.2 改到 §2.3）
  - 任何 category 重命名（A-J 的字母 + name）
  - 任何 contribution claim 的增删
  - 任何 finding (F1-F5) 的 beat 归属

---

**文档版本**：v4.0
**创建日期**：2026-04-22
**对齐文档**：`paper_outline_v4.md`
**契合 pipeline 版本**：research-agent 8-phase, `phase_contracts.py` 7-beat 硬约束不动
