# Evidence Inventory by Beat

## Beat 1: Crisis Exists

The best-supported part of the paper is the claim that recursive use of synthetic data can damage future models. MAD introduces the self-consuming loop, the Nature paper establishes collapse theoretically and empirically, and A Tale of Tails explains why the damage is structurally about tail erosion rather than a narrow benchmark artifact. The LLM-specific self-consumption paper makes the problem directly relevant to language models. Detector-evasion papers then show that once synthetic text enters the wild, reactive filtering is unreliable. The chain is therefore close to complete for 'collapse is real' and 'reactive detection fails,' but it still breaks on the missing middle claim about how much polluted web data exists at scale.

- **LXAI 2023**
  Role: Foundational statement of recursive self-training failure
  Finding: Shows autophagous training loops amplify bias and degrade model quality over generations even when the first synthetic generation appears usable.
- **Nature 2024**
  Role: Strongest combined theoretical and empirical proof that model collapse is real
  Finding: Demonstrates that recursive training causes irreversible loss of information, especially in distribution tails, with deterioration accumulating over generations.
- **arXiv 2024**
  Role: Explains the mechanism of collapse as tail-loss and a scaling-law shift
  Finding: Argues collapse is not just performance drift but a systematic reduction in support coverage that changes effective scaling behavior.
- **Key paper present in sufficiency analysis; bibliographic details not provided in source bundle**
  Role: Extends the collapse concern from image-style generative settings to LLM self-consumption
  Finding: Provides direct relevance to language models by showing they are also vulnerable when trained on their own outputs.
- **Missing key paper identified in sufficiency analysis**
  Role: Missing anchor paper reinforcing recursive forgetting
  Finding: Would strengthen the claim that repeated exposure to generated data causes forgetting rather than harmless averaging.
- **arXiv 2023**
  Role: Shows reactive filtering is brittle
  Finding: Demonstrates that paraphrasing can defeat AI-text detectors and watermarks, limiting post hoc filtering as a stand-alone defense.
- **2024**
  Role: Independent confirmation that detector-based defenses fail under light edits
  Finding: Shows simple manipulations materially reduce detector accuracy, implying large volumes of synthetic text can pass into downstream corpora undetected.

Remaining gaps:
  ⚠ A web-scale prevalence study of AI-generated text is still missing, so the paper cannot yet show that contamination is already large enough online to make collapse a present crisis rather than a plausible risk.
  ⚠ Need the missing recursive-forgetting anchor ('The Curse of Recursion') to strengthen the claim that the effect is robust across formulations.
  ⚠ Need better bridge evidence linking detector failure to actual corpus contamination rates in real crawls.

---

## Beat 2: Web Quality Declines Over Time

This beat is currently the weakest empirical link. The collapse literature explains why increasing synthetic contamination would degrade web quality, and the detector-evasion literature explains why that contamination may be hard to measure. But the corpus lacks the paper that actually measures web-scale prevalence and lacks the longitudinal crawl study needed to show deterioration over time. As a result, the current chain supports 'decline is plausible and may be hard to observe,' not 'decline has been demonstrated longitudinally.'

- **Missing key paper identified in sufficiency analysis**
  Role: Most important missing anchor for measuring web pollution directly
  Finding: Would quantify the fraction of web-scale data that is AI-generated and provide the empirical base for any time-trend claim.
- **Explicitly identified as missing in sufficiency analysis**
  Role: Critical missing temporal evidence
  Finding: Would be the direct evidence required to show decline over time rather than static contamination.
- **Nature 2024**
  Role: Explains why rising contamination would matter if it is occurring
  Finding: Establishes that increasing synthetic share in training data can produce cumulative information loss.
- **arXiv 2024**
  Role: Supplies the expected signature of declining quality
  Finding: Suggests quality decline should appear as reduced tail diversity and altered scaling, offering measurable consequences for polluted corpora.
- **arXiv 2023**
  Role: Explains why observed pollution may be underestimated
  Finding: If paraphrase defeats detectors, then simple detector-based prevalence estimates may miss contaminated text and understate the trend.
- **2024**
  Role: Corroborates measurement difficulty
  Finding: Shows that even lightweight editing changes detector outcomes, complicating longitudinal measurement based on surface-form detection alone.

Remaining gaps:
  ⚠ Need a direct web-scale prevalence paper, ideally with reproducible estimates across major corpora.
  ⚠ Need a longitudinal Common Crawl or equivalent study that tracks AI-generated fraction and quality metrics over multiple time points.
  ⚠ Need operational definitions of 'quality decline' beyond detector scores, such as entropy, novelty, source diversity, or tail coverage.
  ⚠ Need bridge evidence connecting measured synthetic share to downstream losses in corpus usefulness.

---

## Beat 3: L_auth Theory and Novelty

The theoretical beat should argue that what matters is not merely whether text looks human, but whether it contributes irreducible information, novelty, and support coverage that future learners need. The entropy and sufficiency classics are the missing formal base. The collapse papers then motivate why such a construct matters: recursive data replaces diverse support with averaged, self-similar samples, especially harming tails. The homogenization papers provide conceptual language for the same phenomenon in LLM outputs. Right now the corpus can gesture at this theory, but it cannot yet present L_auth as a rigorously grounded construct.

- **Missing key paper identified in sufficiency analysis**
  Role: Missing classical foundation for defining novelty and information content
  Finding: Would ground L_auth in formal information measures rather than ad hoc quality heuristics.
- **Missing key paper identified in sufficiency analysis**
  Role: Missing classical foundation for what information is preserved by a statistic or proxy
  Finding: Would justify an L_auth metric as preserving the aspects of data needed for learning while discarding surface cues.
- **arXiv 2024**
  Role: Links theory to the claim that novelty lives in the tails
  Finding: Provides a natural motivation for defining L_auth around support coverage and tail preservation rather than average fluency.
- **Nature 2024**
  Role: Connects information-theoretic loss to recursive training
  Finding: Shows that synthetic recursion destroys information generation by generation, motivating a formal metric for retained informational value.
- **2025**
  Role: Provides a conceptual bridge from averaging to novelty loss
  Finding: Argues LLM outputs tend toward homogenization, supporting the idea that human-authored data contains harder-to-reproduce variation.
- **JCR 2025**
  Role: Applies the homogenization/collapse logic to a domain setting
  Finding: Frames generative systems as pushing outputs toward a democratization-average trap, offering a domain-relevant intuition for why L_auth should reward original variation.
- **LXAI 2023**
  Role: Supplies an early analytical basis for why recursive averages are dangerous
  Finding: Shows how self-consumption can reinforce bias and erase less-frequent information, consistent with a novelty-sensitive theory.

Remaining gaps:
  ⚠ Need the classical information-theoretic anchors to make L_auth mathematically credible.
  ⚠ Need a clear formal definition of L_auth and how it differs from entropy, perplexity, detector score, and provenance labels.
  ⚠ Need proofs or at least propositions showing when L_auth decreases under recursive generation.
  ⚠ Need empirical validation that L_auth predicts downstream utility better than standard detector-based measures.

---

## Beat 4: Experiment: Measuring Recursive Pollution Better Than Detectors

The experimental beat should convert the paper's critique into a direct test: create datasets with increasing synthetic contamination, apply paraphrase/editing stressors that defeat standard detectors, and compare whether L_auth-style novelty or information metrics track degradation earlier and more robustly than provenance detectors. The collapse papers define the expected direction of harm, the detector papers define the adversarial setup, and the mitigation papers define meaningful comparison arms. The result would let the paper claim not only that the problem exists, but that its proposed measure is operationally better than current reactive tools.

- **arXiv 2023**
  Role: Justifies an experimental baseline that detectors are insufficient
  Finding: Shows that a strong experiment must include paraphrase and editing because detector-only benchmarks are too easy.
- **2024**
  Role: Provides practical perturbations for a stress test
  Finding: Demonstrates realistic low-effort manipulations that should be included when testing whether L_auth is more robust than detectors.
- **Nature 2024**
  Role: Supplies the target phenomenon the experiment should recover
  Finding: Predicts monotonic loss as recursive contamination rises, giving the experiment a theoretically expected direction of effect.
- **arXiv 2024**
  Role: Suggests what to measure beyond accuracy
  Finding: Indicates the experiment should track tail coverage, diversity, and scaling behavior rather than only average benchmark scores.
- **arXiv 2024**
  Role: Provides a mitigation-aware comparator condition
  Finding: Argues synthetic data can be useful under reinforcement-style filtering, so the experiment should compare naive recursion with curated or reinforced pipelines.
- **arXiv 2024**
  Role: Motivates self-correction as an ablation arm
  Finding: Introduces mechanisms intended to stabilize self-consuming loops, useful as a competing intervention in the experiment.
- **arXiv 2024**
  Role: Provides a high-quality curation condition for experimental comparison
  Finding: Suggests carefully curated synthetic data may avoid some failure modes, so L_auth should be tested on both uncurated and curated recursion regimes.

Remaining gaps:
  ⚠ No paper in the current corpus appears to run this exact head-to-head experiment, so this beat remains mostly a proposal.
  ⚠ Need a gold-standard dataset with known contamination proportions and controlled recursion depth.
  ⚠ Need pre-registered evaluation metrics linking measurement to downstream training utility, not just detection accuracy.
  ⚠ Need domain coverage beyond generic web text to show robustness across education, code, science, and consumer text.

---

## Beat 5: Solution: How to Avoid or Mitigate Collapse

The solution literature supports a measured, not fatalistic, conclusion: collapse is a real risk, but it is not inevitable. The strongest mitigations all preserve contact with high-quality nonrecursive data or add strong curation, reinforcement, or self-correction before synthetic outputs reenter training. Retrieval-based provenance can help on the ingestion side, but the detector-evasion results imply that reactive filtering alone is insufficient. The most defensible solution beat therefore recommends a layered strategy: maintain real-data anchors, prioritize curation over volume, use provenance/retrieval where possible, and evaluate corpus health with intrinsic novelty or information measures rather than detector confidence alone.

- **arXiv 2024**
  Role: Primary solution paper for using synthetic data safely
  Finding: Argues that synthetic data need not cause collapse if filtered or reinforced with quality signals rather than naively recycled.
- **arXiv 2024**
  Role: Theoretical argument for curated self-consumption
  Finding: Shows that carefully curated synthetic loops can converge toward desirable objectives instead of collapsing.
- **arXiv 2024**
  Role: Algorithmic mitigation proposal
  Finding: Introduces self-correction mechanisms designed to stabilize recursive training and prevent quality decay.
- **arXiv 2024**
  Role: Mathematical mitigation result
  Finding: Proves that mixing real data with synthetic data under appropriate conditions can avoid collapse, emphasizing the importance of preserving a nontrivial real-data stream.
- **arXiv 2023**
  Role: Best available practical defense on the ingestion side
  Finding: Suggests retrieval/provenance-style approaches may outperform pure detectors when policing synthetic contamination.
- **Nature 2024**
  Role: Problem-defining baseline that solutions must beat
  Finding: Provides the failure benchmark against which any mitigation strategy must be evaluated.

Remaining gaps:
  ⚠ Current solution papers mostly address training pipelines, not web-scale governance of polluted public corpora.
  ⚠ Need evidence that proposed mitigations work for LLM-scale text ecosystems, not only controlled synthetic-loop settings.
  ⚠ Need cost-benefit analysis comparing curation, provenance, retrieval, and real-data acquisition.
  ⚠ Need policy or platform mechanisms for preserving human-authored high-novelty data sources over time.

---

## Suggested Paper Structure

- section_1_crisis: ~7 papers, 4-5 pages
- section_2_empirical: ~6 papers, 3-4 pages
- section_3_theory: ~7 papers, 3-4 pages
- section_4_experiment: ~7 papers, 4-5 pages
- section_5_solution: ~6 papers, 3-4 pages