# Evidence Sufficiency Report

*Assessment of literature support for each beat of the paper*

---

## Beat 1: Model Collapse and Contamination Risk 🟡 adequate

Supporting papers: 39
Key papers present: The Curse of Recursion: Training on Generated Data Makes Models Forget, AI-generated data contamination erodes pathological variability and diagnostic r, Self-Correcting Self-Consuming Loops for Generative Model Training, Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
Weakness: Good as urgency-setting background, but not as the direct proof base for socially grounded post-training claims. Much of the evidence is recent, fragmented, and often domain-specific; mitigation and generalization across modalities remain underdeveloped.

Evidence chain:
  → Recursive/self-consuming training papers show degradation risk under synthetic contamination
  → Contamination-monitoring and detection papers make training-corpus pollution plausible in practice
  → This supports urgency for provenance-aware collection, not direct validation of Beats 4-5

---

## Beat 2: Web Drift and Partial Measurability 🟡 adequate

Supporting papers: 24
Weakness: The corpus supports only the narrower claim that web drift and AI-content growth are partially measurable in slices of the web. It does not directly prove broad web-scale degradation of training quality, and the D-H connection is especially thin in the graph.

Evidence chain:
  → Measurement papers show AI-content growth or drift can be detected in bounded domains
  → Older retrieval/pollution work shows plausible mechanisms for downstream degradation
  → There is still no strong end-to-end demonstration that the open web as a whole has broadly degraded as a training source

---

## Beat 3: L_auth as Descriptive Framework 🟠 weak

Supporting papers: 27
Key papers present: The Curse of Recursion: Training on Generated Data Makes Models Forget, Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
Key papers MISSING: LIMA: Less Is More for Alignment
Weakness: The corpus can motivate L_auth as a useful organizing lens for fine-tuning data-authenticity effects, but not as a validated law. The underlying D category is very new and weakly integrated with A/E/I, so stage-agnostic or causal claims would be under-supported.

Evidence chain:
  → Collapse and curated-data papers suggest that authenticity and composition matter
  → Recent authenticity/data-composition papers provide a plausible basis for a fine-tuning framework
  → Cross-stage validation and strong causal isolation are missing, so L_auth should be presented as descriptive rather than settled

---

## Beat 4: Provenance Value on Socially Grounded Tasks 🟡 adequate

Supporting papers: 40
Key papers present: Constitutional AI: Harmlessness from AI Feedback
Key papers MISSING: LIMA: Less Is More for Alignment, Self-Instruct: Aligning Language Models with Self-Generated Instructions
Weakness: This is the strongest literature-backed beat, but the claim must stay narrow. The corpus supports that provenance and genuine human interaction data seem especially valuable for socially grounded tasks, while AI feedback can work well on bounded objectives; it does not prove provenance superiority across all post-training settings.

Evidence chain:
  → Well-cited post-training/alignment work shows AI feedback can improve bounded tasks
  → Human-data and socially grounded task papers suggest additional value from real provenance and interaction context
  → The F-J linkage is the clearest connected subthread in the corpus, but direct head-to-head comparisons remain limited

---

## Beat 5: Fixed-Compute Pilot Evidence 🟠 weak

Supporting papers: 40
Key papers present: Constitutional AI: Harmlessness from AI Feedback, Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
Key papers MISSING: LIMA: Less Is More for Alignment, OpenAssistant Conversations — Democratizing Large Language Model Alignment
Weakness: The literature justifies running a fixed-inference-compute pilot, but does not by itself validate strong conclusions from it. The biggest gap is lack of close precedent that cleanly disentangles provenance/data composition from inference-time scaling, chain-of-thought, and model-scale effects on socially grounded tasks.

Evidence chain:
  → Primary-evidence categories motivate a provenance-sensitive post-training hypothesis
  → Adversarial-scope papers show why inference-time compute must be held fixed and discussed explicitly
  → Because the corpus lacks many direct disentangling studies, the pilot should be framed as directional support only

---

## Beat 6: CampusGo as Deployed Provenance Infrastructure 🟡 adequate

Supporting papers: 12
Key papers MISSING: OpenAssistant Conversations — Democratizing Large Language Model Alignment
Weakness: Adequate support exists for presenting CampusGo as a real implementation and deployment contribution. However, deployment demonstrates collection capability and provenance instrumentation, not downstream model improvement; the corpus does not close that gap for you.

Evidence chain:
  → Infrastructure and data-collection papers make a provenance-aware platform contribution legible
  → Secondary links to post-training categories show why such infrastructure matters
  → But implementation evidence should not be converted into a claim of validated model gains without additional downstream results

---

## Beat 7: Competing Explanations and Honest Scoping 🟡 adequate

Supporting papers: 8
Key papers present: Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models, DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, s1: Simple test-time scaling
Key papers MISSING: Self-Instruct: Aligning Language Models with Self-Generated Instructions
Weakness: This beat works if it stays genuinely adversarial. The key alternative mechanisms are present, but the corpus still lacks decisive head-to-head studies against provenance/data-composition effects, so the paper should surface these as real scope limiters rather than try to dismiss them.

Evidence chain:
  → Test-time scaling and reasoning papers show performance can rise without changing training-data authenticity
  → These mechanisms are plausible competitors to the thesis, especially on benchmarked reasoning tasks
  → Honest scoping is therefore well supported, but resolution between mechanisms is not

---

## Overall Assessment
The corpus is sufficient for a cautious paper, not for a maximal claim. Beats 1, 2, 4, 6, and 7 are adequately supported if stated narrowly; Beat 3 is only weakly supported as a descriptive framework; Beat 5 is weak if interpreted beyond directional pilot evidence. The strongest part of the corpus is the thread connecting post-training/alignment evidence to the idea that provenance matters more on socially grounded tasks than on bounded tasks where AI feedback can already work. The weakest part is causal disentangling: the graph is sparse, many papers are isolated and very recent, and there is limited integrated evidence separating data-authenticity effects from inference-time scaling, reasoning prompting, and model size. The paper should therefore avoid claiming that L_auth is a validated law, avoid using motivation beats as direct proof for the main thesis, and keep CampusGo framed as a deployed infrastructure contribution rather than downstream validation.

## Missing Papers (search suggestions)

- **LIMA: Less Is More for Alignment**: Directly relevant to the claim that carefully curated, authentic human data can outperform larger but noisier instruction-tuning mixtures. It would materially strengthen Beats 3-5 by anchoring the data-quality/composition side of the argument with a well-known fine-tuning result.
  Search: `LIMA Less Is More for Alignment high quality human written instruction tuning data quality`
- **OpenAssistant Conversations — Democratizing Large Language Model Alignment**: Likely the most important missing precedent for a deployed human-provenance conversational data pipeline. It would strengthen Beat 6 on infrastructure and also give Beats 4-5 a more concrete socially grounded human-data reference point.
  Search: `OpenAssistant Conversations democratizing large language model alignment human collected dialogue provenance`
- **Self-Instruct: Aligning Language Models with Self-Generated Instructions**: A canonical counterexample showing that synthetic or self-generated instruction data can improve post-training outcomes. It is important not because it supports the thesis, but because it sharpens Beats 4 and 7 by forcing the claim to stay narrow to socially grounded tasks and honest scoping.
  Search: `Self-Instruct aligning language models with self-generated instructions synthetic instruction tuning`

## Strongest Narrative Thread
The Curse of Recursion: Training on Generated Data Makes Models Forget -> Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe -> Constitutional AI: Harmlessness from AI Feedback
