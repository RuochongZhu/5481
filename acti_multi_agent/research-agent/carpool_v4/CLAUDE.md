# Research Agent — CLAUDE.md (v4.2 CampusRide)

> Claude Code reads this file on every session start. It defines quality gates,
> role isolation rules, and invariants for the **v4.2 CampusRide** research-agent
> pipeline. Previous L_auth thesis state is archived in `../` (parent dir).
> v4.1 artifacts are superseded by v4.2 updates described below.

## Project Overview

HCI design-case literature analysis pipeline for the **CampusRide** paper.
9-phase pipeline with 5-reviewer evaluation loop and auto-backtrack.
7-beat paper structure, 3-contribution claim:

Three contribution claims (carried through Abstract, Introduction §1, §5, §6):
1. CampusRide — identity-verified multi-module campus platform
2. Carpool module deep-dive grounded in a formative survey (N=111 eligible / 44 finished; driver subgroup N=19 carries the F5 rating-fairness asymmetry)
3. research-agent — thesis-conditioned evidence pipeline as methodology

## v4.1 → v4.2 changes (summary)

- Survey cohort corrected: "117 / 50" → "111 eligible / 44 finished" (6 Survey-Preview test rows excluded).
- Language cohort corrected: "82% Mandarin" → "79% Mandarin-native (72/91 who reported native language)".
- F1 numbers: 29/32 → 28/32, 24/33 → 23/32. F3 means updated to 69.1 / 67.3 / 63.5 / 60.5 / 55.4 / 54.9 / 50.9.
- **F5 MAJOR**: now reported on the Driver/Both subset (N=19) with a Rider-only control subset (N=12). Full-sample N=30 is an outdated v4.1 artifact — flag it.
- **F6 NEW**: Q23 driver supply willingness (N=33). Long-distance 12/33 Very+Extremely willing = highest.
- E / I / H-subgroup categories populated via manual_core_inclusions (Prompt A/B/E audits under `config/*_audit.md`).
- Phase 3 relationship graph emits 4 new edge types: `conceptual_overlap`, `methodological_mirror`, `temporal_succession`, `contradiction`.
- §6.2 Audit Trail must include a negative-audit paragraph (pipeline limitations explicitly disclosed).

## Beat Structure (7 beats, sections §2.1–§7.2)

| Beat | § | Title | Argument Line | Categories |
|------|---|-------|---------------|------------|
| 1 | §2.1 | Small-Town Campus Transportation & Coordination Gaps | motivation | A, B |
| 2 | §2.2 | Grassroots Coordination & Integrated Campus Platforms | motivation | C, D, I |
| 3 | §2.3 | Design Primitives: Identity, Safety, Rating Fairness, Rewards | framework | E, F, G, H |
| 4 | §4.1 | Formative Survey: Passenger-Side WTP & Motivations (+ F6 supply) | primary | *(primary_data)* |
| 5 | §4.2 | Formative Survey: Driver-Subset Tolerance & Rating-Fairness Asymmetry | primary | F, H, H-subgroup |
| 6 | §5 | CampusRide Multi-Module Platform Design with Carpool Deep-Dive | core_contribution | *(artifact)* |
| 7 | §7.2 | Adversarial Scoping: 3-Tier Sample Skew, Formalization, No Deployment | adversarial | J, H, H-subgroup |

CRITICAL:
- Motivation beats (1-2) frame urgency but do not directly prove the primary survey findings.
- Primary beats (4-5) present formative survey results — NO inferential statistics.
- Beat 6 describes a designed and implemented artifact but does NOT claim deployment validation.
- Beat 7 must surface algorithmic management critique as genuine scope limiters.
- Beats 4 and 6 are primary_data / artifact — they use pseudo-anchors (`local:CornellCarpoolSurvey2026`, `local:CampusRideSystem2026`) from `config/manual_core_inclusions.json::primary_anchors`.

## Category Taxonomy (A-J, 10 categories)

| Cat | Name |
|-----|------|
| A | Small-town / Campus Transportation Gap |
| B | Peer-to-Peer Ridesharing & Sharing-Economy Trust |
| C | Grassroots / Informal Coordination Platforms |
| D | International Students Digital Practices US Universities |
| E | Identity Verification & .edu-Scoped Platforms |
| F | Safety in Shared Mobility |
| G | Gamification in Coordination / Mobility |
| H | Rating & Reputation System Design & Fairness |
| I | Integrated Community Platforms & Super-Apps |
| J | Algorithmic Management & Platform Labor Critique (adversarial) |

K from the prior L_auth run has been removed. Do NOT expect K coverage anywhere.

## Quality Gates (Hooks)

### Before any classification (P2) API call:
- 每篇论文必须且只能分到 A-J 中的一个主类别
- confidence 低于 0.6 时标注 needs_review=true
- 绝对不允许发明新类别或跳过论文
- 如果 abstract 为空或少于 50 词，标注 incomplete=true，不分类

### Before any deep extraction (P2.5) API call:
- 如果 MinerU markdown 存在，优先使用 markdown 而非 abstract
- 7 个字段必须全部输出，缺失字段用 "not_stated" 填充
- key_claim 必须是可证伪的陈述，不能是模糊描述

### Before any narrative chain (P3.5) API call:
- 每个 beat 的 spine 必须按 citation 时间顺序排列（除 Beat 4/6 primary_data/artifact）
- 每篇论文只能出现在一个 beat 的 spine 或 supporting 中
- anchor paper 必须是该 beat 引用量最高的论文之一（除 Beat 4/6）
- Beat 4/6 使用 `local:` 前缀伪 anchor，其 spine 可引用 `finding:F1..F5` 或 `module:carpool..points`
- primary 的 beat (4/5) 不能用 motivation 论文作为直接支撑
- Beat 6 各设计决策必须明确回指某个 survey finding (F3/F4/F5)
- adversarial beat (7) 必须引用至少一篇反证文献，不空泛自省
- Beat 7 的成功标准是诚实界定范围，而不是替 thesis 辩护

### Before any contradiction scan (P3.7) API call:
- 只标记真正的分歧，不标记互补发现
- 每个矛盾必须有双方的具体证据
- severity 必须是 critical / moderate / minor 之一
- competing_mechanism 允许用于 Beat 7
- 每个矛盾必须标注所属 argument_line
- Focus Questions: F1 Gap/Substitute, F2 Grassroots Legitimacy, F3 .edu Trust Primitive, F4 Rating Fairness, F5 Gamification Risk

### After Phase 5 evaluation:
- 如果 overall_score < 0.85，自动回退到最弱维度对应的 phase
- 如果 honesty_score < 0.80，即使 overall 达标也回退到 Phase 4
- Category J active paper count < 3 时不能判定 done
- Category J (adversarial) contradiction focus 没有足够证据时不能判定 done
- 任一关键分析产物里仍有 fallback placeholder 时不能判定 done
- 如果 reviewer 分歧 > 0.3，暂停等待人工确认
- 永远不删除论文（append-only corpus）

## Verb Discipline (per-section)

| Section | 允许 | 禁止 |
|---------|------|------|
| §2.1 Beat 1 | exists, motivates, is documented, points to | has been proved, is quantified, definitively shows |
| §2.2 Beat 2 | document, indicate, suggest; for super-app: initial inquiry | demonstrates, establishes design space, the first multi-module campus platform |
| §2.3 Beat 3 | we propose, we distill, commonly discussed | the canonical framework, validated primitives |
| §4.1 Beat 4 | we observe, reports indicate, median value is | majority think, statistics confirm, significantly |
| §4.2 Beat 5 | resonates with, parallels, counterintuitively | confirms, replicates, proves the same phenomenon |
| §5 Beat 6 | we designed, motivated by, in response to, implementation | effective, successful, proves, validates |
| §6 Pipeline | evidence-chain organization tool, audit trail | research agent, automated discovery, validated pipeline |
| §7.2 Beat 7 | may reproduce, we acknowledge, scope-limited | we address, we prevent, we solve |

## Role Isolation (5-reviewer pattern)

5 个 reviewer 各自只关心一个维度，互不干涉：

| Reviewer | 关注点 | 权重 | Slash Command |
|----------|--------|------|---------------|
| Narrative | 叙事逻辑流 | 25% | /review-narrative |
| Coverage | 类别覆盖完整性 | 25% | /review-coverage |
| Gap | 研究空白可信度 | 20% | /review-gap |
| Contradiction | 矛盾处理诚实度 | 15% | /review-contradiction |
| Honesty | 过度论断与范围控制 | 15% | /review-honesty |

每个 reviewer 的 context 都注入 `scoring.PAPER_CONTEXT_V4`（三 contribution 说明 + 证据标准 + 动词纪律）。

## Model Tiering

- MODEL_FAST (Sonnet): P1, P2, P2.5 — 高频批量调用
- MODEL_DEEP (Opus): P3.5, P3.7, P5 — 低频深度推理

## Invariants

- Corpus is append-only: never delete papers from classified.json
- v2_pruned / pruned papers must be explicitly filtered by downstream phases
- State is always saved before and after each phase
- Every API error is caught and classified (APIKeyMissing / ModelNotFound / QuotaExhausted)
- Pipeline is fully resumable via --resume flag
- results.tsv tracks every auto-loop iteration
- Thesis is defined in `src/thesis_v4.py::THESIS_V4`; any change flows through all agent prompts

## Reference Documents

- `../paper_outline_v4.md` — Full 12-15 page paper outline
- `../pipeline_v4_migration_and_config.md` — v4 migration specification
- `../local_ai_risk_resolution_prompts.md` — Local-AI prompts for R1-R6 risk tasks
