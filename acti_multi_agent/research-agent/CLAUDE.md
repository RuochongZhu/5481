# Research Agent — CLAUDE.md

> Claude Code reads this file on every session start. It defines quality gates,
> role isolation rules, and invariants for the research-agent pipeline.

## Project Overview

PhD literature analysis pipeline for AI data quality / model collapse / data authenticity.
9-phase pipeline with 5-reviewer evaluation loop and auto-backtrack.
7-beat paper structure:
- motivation (Beats 1-2)
- framework (Beat 3)
- primary (Beats 4-5)
- core_contribution (Beat 6)
- adversarial (Beat 7)

## Beat Structure (7 beats)

| Beat | Title | Argument Line | Categories |
|------|-------|---------------|------------|
| 1 | Model Collapse and Contamination Risk | motivation | A, B, C |
| 2 | Partial Measurability of Web Drift | motivation | D, H |
| 3 | L_auth Framework Definition | framework | D, A |
| 4 | Fine-tuning Data Source Affects Social Reasoning | primary | F, I, J |
| 5 | Contrastive Fine-tuning Experiment | primary | F, I, J |
| 6 | CampusGo as Deployed Core Contribution | core_contribution | G |
| 7 | Competing Explanations and Honest Scoping | adversarial | K |

CRITICAL:
- Motivation beats frame urgency but do not directly prove the primary post-training claim.
- Primary beats cannot rely on collapse papers as direct support.
- Beat 6 may acknowledge deployment, but not validated downstream model gains.
- Beat 7 must surface genuine competing mechanisms such as inference-time scaling.

## Quality Gates (Hooks)

### Before any classification (P2) API call:
- 每篇论文必须且只能分到 A-K 中的一个主类别
- confidence 低于 0.6 时标注 needs_review=true
- 绝对不允许发明新类别或跳过论文
- 如果 abstract 为空或少于 50 词，标注 incomplete=true，不分类

### Before any deep extraction (P2.5) API call:
- 如果 MinerU markdown 存在，优先使用 markdown 而非 abstract
- 7 个字段必须全部输出，缺失字段用 "not_stated" 填充
- key_claim 必须是可证伪的陈述，不能是模糊描述

### Before any narrative chain (P3.5) API call:
- 每个 beat 的 spine 必须按 citation 时间顺序排列
- 每篇论文只能出现在一个 beat 的 spine 或 supporting 中
- anchor paper 必须是该 beat 引用量最高的论文之一
- primary 的 beat 不能用 motivation 论文作为直接支撑
- adversarial beat 的成功标准是诚实界定范围，而不是替 thesis 辩护

### Before any contradiction scan (P3.7) API call:
- 只标记真正的分歧，不标记互补发现
- 每个矛盾必须有双方的具体证据
- severity 必须是 critical / moderate / minor 之一
- competing_mechanism 允许用于 Beat 7
- 每个矛盾必须标注所属 argument_line

### After Phase 5 evaluation:
- 如果 overall_score < 0.85，自动回退到最弱维度对应的 phase
- 如果 honesty_score < 0.80，即使 overall 达标也回退到 Phase 4
- Category K active paper count < 3 时不能判定 done
- Category K contradiction focus 没有足够证据时不能判定 done
- 任一关键分析产物里仍有 fallback placeholder 时不能判定 done
- 如果 reviewer 分歧 > 0.3，暂停等待人工确认
- 永远不删除论文（append-only corpus）

## Role Isolation (gstack pattern)

5 个 reviewer 各自只关心一个维度，互不干涉：

| Reviewer | 关注点 | 权重 | Slash Command |
|----------|--------|------|---------------|
| Narrative | 叙事逻辑流 | 25% | /review-narrative |
| Coverage | 类别覆盖完整性 | 25% | /review-coverage |
| Gap | 研究空白可信度 | 20% | /review-gap |
| Contradiction | 矛盾处理诚实度 | 15% | /review-contradiction |
| Honesty | 过度论断与范围控制 | 15% | /review-honesty |

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
