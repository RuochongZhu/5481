# 本地 AI 风险解决 Prompt 集（Local AI Risk Resolution Prompts）

> **作用**：把 `pipeline_v4_migration_and_config.md` 里 pipeline **自己解决不了**的风险，转化为本地 LLM（Claude Opus 4.7 / GPT-5.4 等）可执行的提示词。本地 AI 可以调取多个 LLM API 层层协作，完成 pipeline 本身做不到的决策性任务。
>
> **使用方式**：这些 prompt 设计为可以直接复制粘贴到你本地的 Claude Code / Cowork / 任何支持 multi-LLM 的执行环境。每个 prompt 都标注了输入、预期输出、建议的 LLM 选型、以及后续串联任务。
>
> **核心哲学**：pipeline 负责**文献组织与诊断**；本地 AI 负责**代码级检查、战略决策、rebuttal 准备**。两者互补。

---

## Part 0. 风险任务分类

根据 pipeline 的能力边界把 7 个风险分成三类：

### A. Pipeline 能自动处理的（2 项，无需本地 AI 介入）
- **风险 4**：C/D/I/J 类文献薄 → `lens_queries.json` 已配置精准补料
- **风险 5**：Beat 7 反证不足 → Phase 3.7 `focus_questions` 已配置

### B. Pipeline 能诊断但需要本地 AI 协助响应的（2 项）
- **风险 3**：三个 contribution 稀释主张 → Phase 5 reviewer 告诉你，本地 AI 帮你决定如何响应
- **风险 6**：Coverage / Contradiction 跷跷板 → 同上

### C. Pipeline 完全碰不到的（3 项，全靠本地 AI）
- **风险 1**：`phase_contracts.py` 在 Beat 4/6 primary-data 时失败
- **风险 2**：v3 旧配置残留污染 v4 运行
- **风险 7**：投稿后审稿人追问 pipeline 本身验证

---

## Part 1. 【Task R1-PreFlight】代码残留污染检测（风险 2）

**场景**：W1 你已经按 `pipeline_v4_migration_and_config.md` Part 2-5 改了 config 和三个 phase 文件里的字符串。但在这种"人工替换字符串"的场景下，**遗漏某处旧 L_auth 引用是非常常见的**——残留字符串会让 pipeline 按旧 thesis 跑，产出错误的 narrative 和 contradiction。

**这个任务 pipeline 做不了**：pipeline 只能按配置跑，不会检测配置里是否有自我矛盾或残留。

**LLM 选型建议**：Claude Opus 4.7（上下文宽、适合跨文件全文扫描）

**Prompt**：

```
你是一个代码一致性检查助手。任务是检测 research-agent pipeline 在从 L_auth
主题迁移到 CampusRide carpool 主题后,是否还有任何 L_auth 残留字符串或概念。

输入材料(附在下面):
1. 新的 thesis 字符串(从 pipeline_v4_migration_and_config.md Part 3.1 复制 THESIS_V4)
2. 新的 Beat 定义 7 条(从 pipeline_v4_migration_and_config.md Part 3.2 复制)
3. 新的 Focus Questions 5 条(从 pipeline_v4_migration_and_config.md Part 4.1 复制)
4. 以下 9 个代码/配置文件的当前内容:
   - src/thesis_v4.py
   - src/phase3_5_narrative.py
   - src/phase3_7_contradiction.py
   - src/phase5_evaluate.py
   - config/search_queries.json
   - config/seed_papers.json
   - config/lens_queries.json
   - config/manual_core_inclusions.json
   - config/manual_exclusions.json

你的任务分三步:

第一步【残留扫描】:
在上述 9 个文件中搜索下列 L_auth 相关字符串或概念。对每一条,报告它在
哪个文件的哪一行出现:
  - "model collapse" / "collapse" (除非明确是 L_auth 之外的 collapse)
  - "synthetic data" / "synthetic contamination"
  - "L_auth" / "D1" / "D2" / "D3" / "D4"
  - "Shumailov" / "Curious Decline" / "π²/6 pathway"
  - "pretraining" / "fine-tuning" 作为论证主线
  - "recursive training"
  - "social reasoning" 作为论点而非工具
  - "thesis:" 后紧跟旧的 5-beat 描述

第二步【概念对齐检查】:
对新的 7 个 Beat(来自输入 2),逐一检查:
  - Beat 主题是否在对应 phase 文件中已出现
  - Beat honesty_note 是否已写入
  - Beat anchor_categories 是否和 config/search_queries.json 里的新 A-J
    一致(如 Beat 1 = A+B)

第三步【输出报告】:
以下面 JSON 格式输出,不要多余文字:

{
  "residual_strings": [
    {"file": "...", "line": N, "text": "...", "severity": "blocking|warning"}
  ],
  "concept_mismatches": [
    {"beat": N, "issue": "...", "file_missing_update": "..."}
  ],
  "ready_to_run_phase1": true | false,
  "blocking_items": ["..."],
  "recommended_fix_order": ["..."]
}

severity 规则:
  - blocking: 会让 pipeline 按错误 thesis 跑
  - warning: 不影响 pipeline 跑,但会让产出文档里出现过时概念

只有 ready_to_run_phase1=true 时才能开始跑 Phase 1。
```

**执行时机**：W1 改完所有配置和字符串之后、跑 `python main.py --phase 1` 之前。

**失败处理**：如果 `ready_to_run_phase1=false`，按 `recommended_fix_order` 逐项修复，再跑一次本 prompt。最多迭代 3 次。

---

## Part 2. 【Task R2-ContractShim】Primary-Data Beat 的伪 Anchor 生成（风险 1）

**场景**：`phase_contracts.py` 的 `ensure_narrative_chains_valid` 要求每个 beat 必须有 `anchor_paper.paperId`。但 Beat 4（乘客侧问卷）和 Beat 6（CampusRide 系统）是 primary data / artifact，没有真实 anchor 论文。

**这个任务 pipeline 做不了**：pipeline 会按契约抛错，不会自己想办法绕过。

**方案**：用本地 AI 生成**结构上合法**的伪 anchor 条目，通过 `manual_core_inclusions.json` 注入，既不改代码，又满足契约。

**LLM 选型建议**：Claude Opus 4.7（需要理解契约结构 + 生成合法 JSON）

**Prompt**：

```
你是一个 research-agent pipeline 的契约适配助手。任务是为两个 primary-data
beat 生成符合 phase_contracts.py 契约的伪 anchor paper 条目。

契约要求(摘录自 phase_contracts.py::ensure_narrative_chains_valid):
  - 每个 beat 必须有 anchor_paper.paperId(非空字符串)
  - 每个 beat 必须有 spine(非空列表)
  - 每个 beat 必须有 paragraph_outline(非空列表)
  - 如果一个 beat 的 error 字段是 "no_papers",允许跳过上述要求——但这会
    触发 narrative_chains 的"全部是占位符"警告

我们有两个"无真实 anchor"的 beat:
  - Beat 4: 乘客侧问卷发现(Passenger-side WTP & Motivations)
           Primary data 源是 Cornell Carpool Survey(N=117,2026)
  - Beat 6: CampusRide 平台设计(六模块 + 拼车 deep-dive)
           Primary artifact 源是 CampusRide 系统文档

你的任务:

第一步【生成伪 Paper 元数据】:
为每个 beat 生成一个伪 paper 条目。使用以下 schema,确保所有字段非空:

{
  "paperId": "<unique canonical ID,以 local: 前缀标记>",
  "title": "<正式的、自描述的标题>",
  "year": 2026,
  "authors": ["<作者列表>"],
  "type": "primary_data" | "system_artifact",
  "doi": null,
  "abstract": "<简洁描述这份 primary data/artifact 是什么、覆盖什么、
               对应到论文哪个 section>",
  "note_for_pipeline": "<告诉下游 agent:这是 primary-data shim,
                          不需要从它检索引用图,只需它作为 beat 的
                          structural anchor>"
}

第二步【填充 spine 和 paragraph_outline】:
对每个 beat,生成:
  - spine: 一个包含 3-5 项的列表,每项是与这份 primary data 相关的
           支撑素材的 paperId 或内部 section reference
  - paragraph_outline: 一个包含 3-4 段的列表,每段一句话描述段落主题

你的 spine 可以引用:
  - 对于 Beat 4: 问卷 finding F1/F3/F4 的 subsection references;H 类
    或 B 类 2-3 篇真实文献作为 contextualizing anchor
  - 对于 Beat 6: 系统各模块的内部 reference;Beat 3 的 design primitive
    回指 2-3 篇

第三步【输出 manual_core_inclusions 补丁】:
输出一个完整的 JSON patch,可以直接 merge 到 config/manual_core_inclusions.json,
使 Beat 4 和 Beat 6 的伪 anchor 被 pipeline 承认为合法 paper。

同时输出一个 Python dict 格式的 paragraph_outline_v4,用于注入到
phase3_5_narrative.py 的 Beat 定义。

输出格式:
=== manual_core_inclusions_patch.json ===
{...}

=== paragraph_outline_v4.py ===
BEAT_4_OUTLINE = [...]
BEAT_6_OUTLINE = [...]

=== verification_check ===
- Beat 4 paperId 是否非空: Y/N
- Beat 4 spine 是否 ≥3 项: Y/N
- Beat 4 paragraph_outline 是否 ≥3 段: Y/N
- Beat 6 paperId 是否非空: Y/N
- Beat 6 spine 是否 ≥3 项: Y/N
- Beat 6 paragraph_outline 是否 ≥3 段: Y/N
- 所有项 Y? ready_to_inject: Y/N
```

**执行时机**：W1 改完 config 之后、跑 Phase 3.5 之前（或者更保险：跑 Phase 1 之前就准备好）。

**验证方式**：跑完 Phase 3.5 后，检查 `narrative_chains.json[3]` 和 `[5]` 是否有正确的 anchor_paper、spine、paragraph_outline 字段，以及 `ensure_narrative_chains_valid` 是否通过。

**失败处理（第二道保险）**：如果 Task R2 的 shim 注入后 Phase 3.5 仍然失败，启动 Task R2-B：

```
接上: Phase 3.5 在注入 primary-data shim 后仍然报 PhaseContractError。
请读取 Phase 3.5 的具体错误信息(我会附在后面),判断:
  (a) 是不是 shim 的 paperId 和 manual_core_inclusions 里的 ID
      不一致? 如果是,给出修复 diff
  (b) 是不是 phase3_5_narrative.py 的 agent prompt 在生成 Beat 4/6
      时遗漏了 anchor_paper 字段? 如果是,给出 prompt 改动建议
  (c) 是否需要放宽 phase_contracts.py 的 primary-data 判断?
      如果是,给出最小改动(只对有 type="primary_data" 标记的 beat
      放宽 anchor_paper 要求,其他 beat 严格校验)

错误信息:
<贴上 Phase 3.5 的错误输出>

输出一个具体的、可执行的修复方案,优先顺序 (a) > (b) > (c)。
```

---

## Part 3. 【Task R3-ContribTriage】三 Contribution 稀释诊断与响应（风险 3）

**场景**：Phase 5 跑完，`reviewer_results.json` 里 `narrative` 分数偏低，评语提到 "unclear primary contribution" 或 "three contributions dilute each other"。

**这个任务 pipeline 能诊断但不能响应**：pipeline reviewer 会标出问题，但降级哪个 contribution、用什么方式降级、是否坚持 full 版——这是战略决策。

**LLM 选型建议**：GPT-5.4（长 reasoning）+ Claude Opus 4.7（写作判断）双 LLM 协作

**Prompt**（给 GPT-5.4 做分析）：

```
你是一个学术论文战略分析助手。我的论文当前有三个 contribution:
  (1) CampusRide 六模块校园平台设计案例
  (2) 拼车模块基于 N=117 问卷的实证 deep-dive
  (3) research-agent pipeline 作为方法论贡献

pipeline 的 Phase 5 reviewer 反馈如下(我会贴上完整 reviewer_results.json):
<贴上 reviewer_results.json 的 narrative reviewer 部分>

你的任务:

第一步【诊断】:
分析 reviewer 到底在不满什么。具体是:
  (a) 三个 contribution 在 Introduction 里没有清晰优先级排序?
  (b) §5 平台章节和 §6 pipeline 章节两个体量大的章节争夺读者注意力?
  (c) Abstract 或标题没有突出单一 primary claim?
  (d) 某个具体 beat 承载了太多 claim?
  (e) 其他?

第二步【方案生成】:
生成三个响应方案,按保留 contribution 的"野心级别"排列:

方案 A (Full preserved): 保留所有三个 contribution。通过哪些具体的写作
手法回应 reviewer?(比如加 "primary contribution is (2),
(1) and (3) are supporting contributions" 这样的明确陈述)

方案 B (Demote #3 to Methodology Note): 把 pipeline 从独立 Section 降级
为 Appendix 或 §3.2 一段话内的方法论注脚。具体改哪些章节?页数如何
重新分配?

方案 C (Split): 把 pipeline 独立出来另写一篇方法论论文(或博客/tech
report),当前论文只做 (1) + (2)。当前论文的哪些章节需要移除或压缩?

对每个方案,给出:
  - 具体改动清单(逐 section)
  - 预期 Phase 5 narrative 分数的变化区间
  - 对投稿档次的影响(CHI full / mid-tier / workshop)
  - 执行代价(改稿时间估计)

第三步【推荐】:
在三个方案中选一个作为 primary recommendation,并给出选择理由。
recommendation 必须考虑我的约束:
  - 1-2 个月交付窗口
  - 已经为三个 contribution 做了前期投入
  - 平台和 pipeline 都是实际做出来的东西
```

**接力任务**（把 GPT-5.4 的分析结果给 Claude，做写作级改动）：

```
你是一个学术论文写作助手。GPT-5.4 刚给出了三个 contribution 稀释问题
的响应方案(贴在下面)。我选择了方案 <A|B|C>。

请按方案要求,生成以下具体改动的草稿:
  - 新的 Abstract 第一句话(突出 primary claim)
  - 新的 Introduction 第 4 段(三 contribution 的排序陈述)
  - <如果是方案 B>: §3.2 的 pipeline methodology note 扩充成能替代原
    §6 大部分内容的紧凑版
  - <如果是方案 C>: §6 需要移除的部分清单;保留的 §3.2 如何重写

方案原文:
<贴上 GPT-5.4 的输出>

输出要有写作纪律:用 paper_outline_v4.md 的 Part 6 诚实性动词表。
```

**执行时机**：Phase 5 第一次跑出 narrative < 0.75 时。

---

## Part 4. 【Task R4-SeesawDetection】Coverage/Contradiction 跷跷板诊断（风险 6）

**场景**：你跑了两轮 Phase 5。第一轮 coverage 低、补料；第二轮补料后 contradiction 又掉下来——这是经典的"改一头崩另一头"跷跷板。

**这个任务 pipeline 能诊断但不能响应**：pipeline 告诉你跷跷板在发生，但"是否该改 thesis scope 而不是继续补料"是判断。

**LLM 选型建议**：Claude Opus 4.7（需要跨 Phase 5 多轮结果分析）

**Prompt**：

```
你是一个 research-agent pipeline 诊断助手。我跑了两轮 Phase 5:

第一轮 reviewer_results:
<贴上第一轮 reviewer_results.json 的摘要分数>
<贴上第一轮 reviewer feedback 文本>

第一轮之后我采取的行动:
<简述:例如"补了 5 篇 D 类国际学生文献">

第二轮 reviewer_results:
<贴上第二轮 reviewer_results.json 的摘要分数>
<贴上第二轮 reviewer feedback 文本>

两轮对比:
  - 某个维度上升: <...>
  - 另一个维度下降: <...>

你的任务:

第一步【判断是不是跷跷板】:
用以下标准判断:
  - 两轮 overall 差距 < 0.05? (小幅波动)
  - 两轮 weakest_dimension 不同?
  - 加权后得分基本没动?
  满足 2 条以上 → 是跷跷板

第二步【根因分析】:
如果是跷跷板,诊断根因属于下列哪一类:
  (a) Thesis 本身 over-scope: claim 太大,无论补什么料都会出现反证
      → 解决方案: 缩小 thesis
  (b) Corpus 某类结构性缺失(比如 J 类 algorithmic management 批评
      文献本身就不多),不是补料能解决的
      → 解决方案: 承认 scope 限制,不再补料
  (c) 不同 reviewer 对同一内容的评分标准不一致(比如 coverage reviewer
      要求细、contradiction reviewer 要求广)
      → 解决方案: 调整 reviewer context
  (d) 真的是 pipeline 内部的奇怪交互,需要看产物详情

对根因最可能的那类,给出具体证据(引用哪个 reviewer 的哪句话)。

第三步【行动方案】:
基于根因,给出**必须跳出跷跷板**的行动方案。方案必须不是"再补料重跑
第三轮"(那会继续跷跷板)。方案必须是:
  - 改 thesis 文字(具体新 thesis)
  - 或改 reviewer context(具体新 PAPER_CONTEXT)
  - 或降低某个 beat 的 honesty_note(具体新 note)
  - 或明确承认某个 contribution 的 scope limitation 在论文里

不可以给"再补 5 篇 J 类文献"这种继续跷跷板的建议。

第四步【风险确认】:
给出这个行动方案的预期 trade-off:
  - 哪个维度会升?
  - 哪个维度会降?(必然有 trade-off)
  - 是否可接受?
```

**执行时机**：Phase 5 连续两轮 overall < 0.80 且 weakest_dimension 交替。

---

## Part 5. 【Task R5-RebuttalPrep】审稿人对 Pipeline 验证的质问预案（风险 7）

**场景**：论文投稿后，审稿人可能问："你把 pipeline 作为 contribution，你如何验证 pipeline 本身的 validity？" 这是 pipeline 跑不完的任务。

**这个任务 pipeline 完全碰不到**：这是 post-submission 的交互问题，pipeline 只负责前期文献。

**LLM 选型建议**：Claude Opus 4.7（擅长 academic rebuttal 风格）

**Prompt**（提前准备 rebuttal pack）：

```
你是一个学术 rebuttal 准备助手。我的论文把 research-agent pipeline 作为
contribution #3,但 pipeline 本身的定位(参见 CURRENT_STATUS_AND_RECOMMENDATIONS.md)
是"evidence-chain organization tool",不是经过验证的 research agent。
这个诚实定位已经写进论文 §3.2 和 §6.3。

但审稿人可能仍然追问:"How do you validate that research-agent actually
works?" 或 "What's your evidence the pipeline is useful beyond your own
paper?"

你的任务是预先准备 rebuttal pack,包含 5 个可能被问的问题和对应回答:

Q1: "How do you validate research-agent?"
    预期回答要点:
    - 我们不 claim 验证了 pipeline 本身
    - 论文的 contribution 是 "pipeline shaped this paper's literature
      synthesis in ways we can audit"
    - §6.2 audit trail 是唯一的 validity evidence
    - Future work: cross-domain deployment + user study

Q2: "Why not compare against human-curated literature review?"
    预期回答要点:
    - 人类 baseline 不是本文目标,是 future work
    - 本文 claim 是工具 assisted 而非 replaced 人类
    - 引用 hybrid approach 文献

Q3: "Why should design research community care about this pipeline
     vs. existing tools like Connected Papers or Elicit?"
    预期回答要点:
    - Pipeline 是 thesis-conditioned,Connected Papers 不是
    - Pipeline 有 contradiction / reviewer diagnostics layer,
      Elicit 不做 adversarial scoping
    - 明确限制: Pipeline 目前只适合 evidence-chain organization,
      不适合 open-ended discovery

Q4: "The sample (N=117, 82% Mandarin) is biased. How can
     you generalize findings?"
    (这虽然是问卷问题,但会连带 pipeline 质问)
    预期回答要点:
    - 本文 scope 明确定义在国际学生小城校园场景
    - 82% Mandarin 是 scope 特征不是 bias 问题
    - §7.2 已承认

Q5: "What if the pipeline's reviewer is just repeating your own
     thesis back at you in a self-confirming loop?"
    这是最尖锐的问题。预期回答要点:
    - Pipeline 的 contradiction_map 专门打捞反证,不是 confirming
    - 本文 §7.2 的 5 个 adversarial scope 直接来自 pipeline,
      这些是我们不可能"希望找到"的反证
    - 引用具体 contradiction case: pipeline 找到哪篇论文让
      我们修改了 §X 的论断

对每个 Q,生成 200-300 词的完整回答,使用 academic rebuttal 风格
(礼貌但不 defensive,承认局限但守住核心 claim)。
```

**执行时机**：W8 投稿前一周，作为 rebuttal 预案。

---

## Part 6. 【Task R6-MetaCheck】两份主文档交叉一致性核查（辅助任务）

**场景**：每次修改 `paper_outline_v4.md` 或 `pipeline_v4_migration_and_config.md`，两份文档可能悄悄脱节。手动对齐太累。

**LLM 选型建议**：任何 long-context LLM

**Prompt**：

```
你是一个文档一致性核查助手。任务是检查以下两份文档是否在 7 个关键维度
上保持同步:

文档 1: paper_outline_v4.md (附在下面)
文档 2: pipeline_v4_migration_and_config.md (附在下面)

核查维度:
  1. 7 个 Beat 的主题、section 映射是否一致
  2. 10 个 category 字母 (A-J) 的主题定义是否一致
  3. 5 个 Focus Question 的编号和主题是否一致
  4. 5 个 Finding (F1-F5) 的含义在两份文档中是否一致
  5. 每个 Beat 的 honesty_note 是否在两份文档中一致
  6. contribution #3 (pipeline) 在 paper outline 里的定位是否与 pipeline
     文档里 §6 的描述一致
  7. 页数汇总是否正确(相加等于声称的总页数)

对每个维度,输出:
  - 状态: ✅ 一致 / ⚠️ 有轻微分歧 / ❌ 冲突
  - 如有分歧: 两份文档的具体差异文字
  - 修复建议: 以哪份为准、另一份改什么

最后输出:
  - 所有维度状态汇总
  - 是否需要触发文档更新(任何 ❌ 都需要)
  - 建议的更新顺序
```

**执行时机**：每次大改完任一主文档后。

---

## Part 7. Prompt 执行顺序总表

按时间顺序排列的任务执行表：

| 时机 | 任务 | 目的 | LLM 建议 |
|------|------|------|---------|
| W1 结束 | R1-PreFlight | 残留检测 | Claude |
| W1 结束 | R2-ContractShim | 伪 anchor 注入 | Claude |
| W3 末（Phase 3.5 跑完） | R2-B（若 R2 不够） | 二次修复 | Claude |
| W5 首轮 Phase 5 后 | R3-ContribTriage | 三 contribution 诊断 | GPT + Claude |
| W5 第二轮 Phase 5 后 | R4-SeesawDetection | 跷跷板判断 | Claude |
| W7 投稿前 | R5-RebuttalPrep | rebuttal 预案 | Claude |
| 每次大改文档后 | R6-MetaCheck | 一致性核查 | Any long-context |

---

## Part 8. 本地 AI 调用技术注意事项

### 8.1 多 LLM 协作的最佳实践

- **GPT-5.4 做长 reasoning**（R3 的诊断）；**Claude Opus 4.7 做写作输出**（R3 的方案撰写）。两者各有所长
- **不要**把所有任务都丢给同一个 LLM——Claude 在 R1 残留检测上比 GPT 细致；GPT 在 R3 战略 reasoning 上比 Claude 有结构性优势
- Prompt 里**明确交接点**：如果一个任务分两步给两个 LLM 做，第一个 LLM 的输出格式要适合第二个 LLM 消费

### 8.2 Context Window 管理

- R1 需要读 9 个文件 → 估计 ~30-60K token，Claude Opus 4.7 够用
- R3 需要读 reviewer_results.json → 估计 ~10K token，任何 LLM 都够
- R6 需要读两份主文档 → 估计 ~40K token

### 8.3 调用链条可以自动化

如果你的 Claude Code / Cowork 环境支持链式调用，可以写一个 `run_risk_check.py` 脚本：

```python
# 伪代码示意
def w1_pre_flight():
    result = call_claude(load_prompt("R1"), files=glob("src/*.py") + glob("config/*.json"))
    if not result["ready_to_run_phase1"]:
        for item in result["blocking_items"]:
            print(f"BLOCKING: {item}")
        return False
    return True

def w3_post_phase35():
    with open("analysis/narrative_chains.json") as f:
        chains = json.load(f)
    if any(c.get("error") for c in chains if c.get("beat") in [4, 6]):
        result = call_claude(load_prompt("R2_B"), context=chains)
        apply_fix(result)
```

### 8.4 失败时的降级路径

- R1 残留检测失败 3 次 → 停下来人工 grep，别让 AI 继续猜
- R2 伪 anchor 两次都过不了契约 → 允许改 `phase_contracts.py` 放宽 primary-data beat 的 anchor 要求（突破"不改代码"原则）
- R3 三个方案你都不满意 → 和导师面谈，AI 给不了这个决策
- R4 跷跷板持续到第 3 轮 → 接受当前分数，停止优化，进入写作 polish

---

## Part 9. 总结

**Pipeline 和本地 AI 的分工边界**：

| 任务类型 | 工具 | 决策权 |
|---------|------|-------|
| 文献检索 + 分类 + narrative 生成 | Pipeline | Pipeline 自主 |
| contradiction 打捞 + reviewer 诊断 | Pipeline | Pipeline 自主 |
| 代码残留检测 | 本地 AI (R1) | 人工验收 |
| 契约 shim 生成 | 本地 AI (R2) | 人工验收 |
| contribution 稀释响应 | 本地 AI (R3) | **人工决策** |
| 跷跷板判断 | 本地 AI (R4) | **人工决策** |
| Rebuttal 预案 | 本地 AI (R5) | 人工定稿 |
| 文档一致性核查 | 本地 AI (R6) | AI 自主 |

**最关键的原则**：本地 AI 是你的**执行助手**和**诊断协作者**，不是决策者。R3、R4 这类决策性任务，AI 生成方案，最终选择由你（或你和导师）做。

---

**文档版本**：v1.0
**创建日期**：2026-04-22
**对齐文档**：`paper_outline_v4.md`、`pipeline_v4_migration_and_config.md`
**执行窗口**：全 8 周覆盖（W1 起至 W8）
