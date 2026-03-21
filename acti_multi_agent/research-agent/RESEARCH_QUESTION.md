# Research Direction — Evidence Chain for Vibe Research

## Paper Thesis

Web-scraped training data is experiencing information degradation (tail collapse, entropy decline, diversity loss), while physically-verified authentic human social behavioral data provides irreplaceable training signals for social intelligence and human alignment. CampusGo is a running platform designed according to these principles.

## Research Strategy

**NOT**: Open-ended gap exploration → generate thesis proposals
**BUT**: Targeted evidence collection → support predetermined thesis

## 5-Beat Evidence Chain

### Beat 1: Crisis Exists (Literature Review)
**Goal**: Prove model collapse + web pollution is real and urgent
**Evidence needed**: 180-220 papers in 7 categories (A-G)
**Output**: Structured literature review proving the problem

### Beat 2: Empirical Evidence (Data Analysis)
**Goal**: Show web content quality is declining over time
**Evidence needed**: Temporal trends in entropy/TTR from 5 data sources
**Output**: Plots showing degradation + statistical significance

### Beat 3: Theoretical Framework (L_auth)
**Goal**: Formalize "authenticity loss" as computable metrics
**Evidence needed**: Information theory tools, novelty check
**Output**: L_auth = λ₁·D_KL + λ₂·D_α + λ₃·(1-TTR_r)

### Beat 4: Validation Experiment
**Goal**: Prove verified social data improves social reasoning tasks
**Evidence needed**: Fine-tune comparison (web vs filtered vs verified)
**Output**: Statistical proof that condition C > condition A

### Beat 5: CampusGo as Solution
**Goal**: Map L_auth framework to platform design decisions
**Evidence needed**: CampusGo data metrics, design rationale
**Output**: Feature → metric mapping, Gerstgrasser accumulation proof

## Key Differences from Original Pipeline

| Original | New (Vibe Research) |
|----------|---------------------|
| Find gaps → generate topics | Collect evidence → support thesis |
| 200 papers, broad search | 180-220 papers, 7 targeted categories |
| Gap Synthesizer finds unknowns | Literature proves known crisis |
| CampusGo relevance uncertain | CampusGo is the designed solution |
| 4 phases (corpus → gaps → topics) | 5 beats (crisis → data → theory → experiment → solution) |

## What Stays the Same

- Phase 1 search infrastructure (OpenAlex + S2 + arXiv)
- Classification into categories (now A-G aligned with beats)
- Codex cross-validation for quality control
- State machine for resumability

## What Changes

- Search queries: 7 category-specific query sets (from prompt.md)
- Classification: papers assigned to A-G based on beat contribution
- No "gap synthesis" — instead "evidence sufficiency check"
- Output: Not thesis proposals, but evidence inventory per beat
