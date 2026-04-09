# Evidence Inventory by Beat

## Beat 1: Crisis Exists

The crisis was first established by Shumailov et al. (2024) who proved models degrade when trained recursively on synthetic data. This was confirmed across language models by the 'Curse of Recursion' paper and extended to image generation by Alemohammad et al. Martinez et al. documented how this creates a real-world contamination loop as AI content floods the internet. However, Dohmatob et al. provide important skepticism about whether the crisis is as severe as claimed.

- **Shumailov et al. 2024**
  Role: Establishes the core phenomenon
  Finding: Models lose performance when trained on AI-generated data recursively
- **Shumailov et al. 2023**
  Role: Confirms model degradation through forgetting
  Finding: Recursive training causes catastrophic forgetting of original data distribution
- **Martinez et al. 2023**
  Role: Documents the contamination feedback loop
  Finding: AI-generated content increasingly pollutes internet training data
- **Alemohammad et al. 2023**
  Role: Demonstrates autophagous collapse in image models
  Finding: Model Autophagy Disorder (MAD) occurs across modalities
- **Dohmatob et al. 2025**
  Role: Provides critical counter-perspective
  Finding: Argues collapse narrative may be overblown or misunderstood

Remaining gaps:
  ⚠ Quantification of actual web contamination rates
  ⚠ Real-world impact measurements beyond lab settings

---

## Beat 2: Empirical Evidence

Empirical validation comes from multiple angles: Guo et al. provide comprehensive experiments showing collapse is conditional on data curation quality. Bertrand et al. identify specific iteration thresholds where instability emerges. Dohmatob et al. connect the phenomenon to fundamental changes in scaling laws. Cuconasu et al. demonstrate that architectural choices like noise injection can mitigate effects.

- **Guo et al. 2024**
  Role: Comprehensive experimental validation
  Finding: Models collapse under some conditions but can thrive with proper curation
- **Bertrand et al. 2023**
  Role: Stability analysis across iterations
  Finding: Identifies critical instability thresholds in iterative retraining
- **Dohmatob et al. 2024**
  Role: Connects collapse to neural scaling laws
  Finding: Model collapse fundamentally alters scaling law behavior
- **Cuconasu et al. 2024**
  Role: Shows noise can prevent collapse in specific architectures
  Finding: Controlled noise injection improves robustness against synthetic data

Remaining gaps:
  ⚠ Long-term studies beyond 10-20 iterations
  ⚠ Cross-architecture comparisons
  ⚠ Different data mixture ratios

---

## Beat 3: Theoretical Framework

The theoretical understanding centers on Seddik et al.'s thermodynamic framework showing models trend toward maximum entropy. However, Padmanabhan et al. prove that with careful curation, self-consumption can actually optimize for human preferences. Gerstgrasser et al. provide the key theoretical result that accumulating real data alongside synthetic can break the recursion curse.

- **Seddik et al. 2024**
  Role: Provides thermodynamic analogy and mathematical framework
  Finding: Models approach maximum entropy state in closed loops
- **Padmanabhan et al. 2024**
  Role: Theoretical proof of conditions for beneficial self-consumption
  Finding: With proper curation, self-consumption can optimize preferences
- **Gerstgrasser et al. 2024**
  Role: Theoretical conditions for avoiding collapse
  Finding: Accumulation of real data can prevent collapse under specific conditions

Remaining gaps:
  ⚠ Unified mathematical framework across all modalities
  ⚠ Precise threshold calculations for safe synthetic ratios

---

## Beat 4: Novel Experiments

Key experiments should validate Shumailov's variance tracking formula across different architectures and test Guo's optimal mixture ratios in real-world scenarios.

- **Shumailov et al. 2024**
  Role: Proposes variance tracking experiments
  Finding: Variance formula Var(X_j^n) = σ²(1+n/M) predicts collapse
- **Guo et al. 2024**
  Role: Tests different data mixture strategies
  Finding: Specific mixture ratios can maintain model quality

Remaining gaps:
  ⚠ Need experiments on frontier models
  ⚠ Cross-modal collapse testing
  ⚠ Real-world deployment studies

---

## Beat 5: Solutions and Future Work

Solutions emerge on three fronts: Gerstgrasser et al. show data accumulation strategies work, Padmanabhan et al. demonstrate curation can turn the problem into an optimization opportunity, and Cuconasu et al. provide architectural solutions through noise injection. Together these suggest a multi-pronged approach to preventing collapse.

- **Gerstgrasser et al. 2024**
  Role: Primary solution: data accumulation strategy
  Finding: Accumulating real data prevents collapse
- **Padmanabhan et al. 2024**
  Role: Curation as optimization opportunity
  Finding: Proper curation turns bug into feature
- **Cuconasu et al. 2024**
  Role: Architectural solution through noise
  Finding: Controlled noise injection prevents collapse

Remaining gaps:
  ⚠ Implementation guidelines for practitioners
  ⚠ Computational cost analysis of solutions
  ⚠ Long-term effectiveness validation

---

## Suggested Paper Structure

- section_1_crisis: ~15 papers, 4-5 pages
- section_2_empirical: ~8 papers, 3-4 pages
- section_3_theory: ~10 papers, 4-5 pages
- section_4_experiment: ~5 papers, 3-4 pages
- section_5_solution: ~8 papers, 4-5 pages