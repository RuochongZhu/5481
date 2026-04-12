# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## Executive Summary

1. When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) → Can verifier-like correction substitute for fresh human data in self-consuming training loops?
   Handling: State that unverified recursive reuse is risky, but verifier-guided or correction-guided synthetic pipelines are a live exception. Emphasize that such methods depend on access to a trustworthy correction signal, which may itself require human grounding. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.
2. Is web pollution detectable? (pollution scale vs detection limits) → Are retrieval-based detectors robust against paraphrased AI-generated text?
   Handling: Explicitly distinguish closed-output matching from adversarially transformed text. Say retrieval helps under specific assumptions, but is not a universal defense against web pollution or obfuscation.
3. How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? → Are humans fundamentally necessary in the alignment loop, or can self-alignment largely remove them?
   Handling: State explicitly that the literature is split on whether benchmark-level alignment can be automated. Distinguish operational alignment on narrow assistant tasks from normative grounding and ongoing human oversight. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
4. How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) → Is temporally increasing AI contamination enough to conclude that major live-web knowledge sources are already degraded for training?
   Handling: Acknowledge Wikipedia as strong source-specific temporal evidence of contamination while noting that corpus-level training harm remains unproven because filtered broad-web mixtures still perform well. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
5. Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) → Can AI-generated feedback substitute for human preference data in alignment?
   Handling: Explicitly concede that AI feedback can substitute for human feedback on bounded alignment benchmarks. Then state that our claim is about residual value in socially grounded or harder-to-verify settings, not about denying RLAIF's success on summarization/dialogue. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
6. Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? → Does AI pollution of the web necessarily make web-derived data unusable?
   Handling: Separate web-index retrieval from pretraining-corpus construction. State that AI pollution is clearly harmful for some retrieval settings, but FineWeb shows this does not generalize to all filtered web-derived training corpora. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

## Focus Coverage

- [A, E] When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) (count=5)
  Representative: Can verifier-like correction substitute for fresh human data in self-consuming training loops?
- [B, C] Is web pollution detectable? (pollution scale vs detection limits) (count=6)
  Representative: Are retrieval-based detectors robust against paraphrased AI-generated text?
- [F, J] How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? (count=5)
  Representative: Are humans fundamentally necessary in the alignment loop, or can self-alignment largely remove them?
- [D, H] How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) (count=5)
  Representative: Is temporally increasing AI contamination enough to conclude that major live-web knowledge sources are already degraded for training?
- [E, F] Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) (count=5)
  Representative: Can AI-generated feedback substitute for human preference data in alignment?
- [B, E, H] Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? (count=4)
  Representative: Does AI pollution of the web necessarily make web-derived data unusable?
- [I, J] Does data composition matter for social reasoning? (benchmarks vs ablation) (count=4)
  Representative: Are current social-reasoning failures mostly evidence of a fundamental capability limit, or can targeted data composition substantially repair them?

---

## C4: 🔴 CRITICAL — direct_contradiction

**Question**: Can verifier-like correction substitute for fresh human data in self-consuming training loops?

**Paper A**: Self-Consuming Generative Models go MAD
  Claim: Without fresh real data, degradation is inevitable.
  Evidence: "Without enough fresh real data in each generation... inevitably suffer MAD"

**Paper B**: Self-Correcting Self-Consuming Loops for Generative Model Training
  Claim: An explicit correction/verification mechanism can stabilize self-consuming loops.
  Evidence: "Introducing a correction function that maps data points to be more likely under the true distribution makes self-consuming generative training loops exponentially more stable"

**Relevance to thesis**: This is the strongest pro-verification counterexample. It supports your qualified claim that verifier-screened synthetic data may still work in narrower settings, while also showing that 'inevitable collapse' is too strong.
**Beat affected**: 4
**Suggested handling**: State that unverified recursive reuse is risky, but verifier-guided or correction-guided synthetic pipelines are a live exception. Emphasize that such methods depend on access to a trustworthy correction signal, which may itself require human grounding. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Are retrieval-based detectors robust against paraphrased AI-generated text?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Retrieval-based detection is an effective and scalable defense even when paraphrasing defeats current detectors.
  Evidence: An 11B paraphraser easily evades current detectors, but retrieval-based detection is reported as effective and scalable.

**Paper B**: Can AI-Generated Text be Reliably Detected?
  Claim: Recursive paraphrasing attacks can break retrieval-based AI-text detectors and increase false positives.
  Evidence: The paper reports attacks that break watermarking, neural, zero-shot, and retrieval-based detectors.

**Relevance to thesis**: Directly narrows any claim that retrieval solves detectability: some retrieval setups work, but robustness collapses under stronger adversarial paraphrasing.
**Beat affected**: 4
**Suggested handling**: Explicitly distinguish closed-output matching from adversarially transformed text. Say retrieval helps under specific assumptions, but is not a universal defense against web pollution or obfuscation.

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Are humans fundamentally necessary in the alignment loop, or can self-alignment largely remove them?

**Paper A**: Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Hum
  Claim: Principle-driven self-alignment can align LLMs to human values with minimal human supervision.
  Evidence: Key claim says Dromedary is built 'with minimal human supervision' and 'almost no human annotation'.

**Paper B**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Successful RL is fundamentally human-in-the-loop, so human-centric approaches are essential rather than optional.
  Evidence: Key claim says RL is 'fundamentally a human-in-the-loop paradigm' and human-centric methods are key.

**Relevance to thesis**: This is the clearest challenge to any strong claim that authentic human supervision remains indispensable: one paper says alignment can be mostly automated, the other says humans are foundational.
**Beat affected**: 4
**Suggested handling**: State explicitly that the literature is split on whether benchmark-level alignment can be automated. Distinguish operational alignment on narrow assistant tasks from normative grounding and ongoing human oversight. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Is temporally increasing AI contamination enough to conclude that major live-web knowledge sources are already degraded for training?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: AI contamination in a major web knowledge source is rising measurably over time.
  Evidence: Finds AI-generated content in newly created Wikipedia pages has markedly increased since GPT-3.5, providing lower bounds on contamination.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Filtered web data alone remains highly effective for pretraining.
  Evidence: Shows properly filtered and deduplicated web data only can significantly outperform models trained on curated corpora like The Pile.

**Relevance to thesis**: This weakens any strong Beat 2 claim that observed contamination automatically implies broad usable-web degradation.
**Beat affected**: 2
**Suggested handling**: Acknowledge Wikipedia as strong source-specific temporal evidence of contamination while noting that corpus-level training harm remains unproven because filtered broad-web mixtures still perform well. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Can AI-generated feedback substitute for human preference data in alignment?

**Paper A**: 10.1613/jair.1.15348
  Claim: Successful RL should remain fundamentally human-in-the-loop; human-centric approaches are key and underprioritized.
  Evidence: Survey/position paper states RL is 'fundamentally a human-in-the-loop paradigm' and that human-centric methods are essential.

**Paper B**: 10.48550/arxiv.2309.00267
  Claim: AI feedback can replace human feedback on important alignment tasks with comparable results.
  Evidence: RLAIF achieves performance comparable to RLHF on summarization and dialogue, including self-improvement when the labeler is the same model as the policy.

**Relevance to thesis**: This is the strongest counterevidence to any broad claim that human feedback is generally indispensable. It forces the thesis to be narrower: human data may remain most valuable where preferences are socially grounded, hard to simulate, or distribution-shifting.
**Beat affected**: 4
**Suggested handling**: Explicitly concede that AI feedback can substitute for human feedback on bounded alignment benchmarks. Then state that our claim is about residual value in socially grounded or harder-to-verify settings, not about denying RLAIF's success on summarization/dialogue. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Does AI pollution of the web necessarily make web-derived data unusable?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: Heavy AI-generated contamination causes retrieval collapse by eroding source diversity and enabling adversarial infiltration, although LLM rankers are more resilient.
  Evidence: At 67% pool contamination, source diversity erodes; BM25 admits 19-24% adversarial document infiltration.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: A very large filtered and deduplicated CommonCrawl corpus can still improve LLM pretraining quality relative to other open datasets.
  Evidence: FineWeb uses 96 CommonCrawl snapshots with systematic filtering/deduplication and reports better-performing LLMs than other open pretraining datasets.

**Relevance to thesis**: This is a core scope limiter: live retrieval over a polluted web can fail even while carefully constructed static web corpora remain highly effective for pretraining.
**Beat affected**: 4
**Suggested handling**: Separate web-index retrieval from pretraining-corpus construction. State that AI pollution is clearly harmful for some retrieval settings, but FineWeb shows this does not generalize to all filtered web-derived training corpora. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Are current social-reasoning failures mostly evidence of a fundamental capability limit, or can targeted data composition substantially repair them?

**Paper A**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Targeted social-reasoning training matters: adversarial hard examples plus reinforcement learning from verifiable feedback significantly improve social reasoning robustness.
  Evidence: "training with adversarial hard examples via reinforcement learning from verifiable feedback significantly improves social reasoning robustness"

**Paper B**: Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large L
  Claim: LLMs show limited, non-robust Theory-of-Mind and rely on shallow heuristics rather than generalized social reasoning.
  Evidence: "limited and non-robust Theory of Mind abilities, relying on shallow heuristics rather than generalized social reasoning, as shown by failures on adversarial examples"

**Relevance to thesis**: Most direct tension for the thesis: benchmark weakness alone cannot be read as proof that social reasoning is unreachable; targeted training data can improve it. This weakens any overstrong claim that only authentic human data can help.
**Beat affected**: 4
**Suggested handling**: Explicitly separate zero-shot benchmark evidence from post-training intervention evidence. Say that untuned LLMs are fragile on social benchmarks, but targeted hard-example training can improve robustness; the open question is how far those gains generalize beyond the trained distribution. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — direct_contradiction

**Question**: Do watermark-based provenance signals make AI-generated text reliably detectable?

**Paper A**: A Watermark for Large Language Models
  Claim: A watermark can be embedded with negligible quality loss and detected efficiently from short text spans without model access.
  Evidence: The paper presents efficient detection of watermarked text without needing API or parameter access.

**Paper B**: Can AI-Generated Text be Reliably Detected?
  Claim: Recursive paraphrasing attacks can break watermark-based detection.
  Evidence: Watermarking is explicitly listed among the detector classes broken by the reported attacks.

**Relevance to thesis**: This weakens any simple provenance-based argument that AI pollution is straightforward to detect after redistribution or rewriting.
**Beat affected**: 4
**Suggested handling**: Present watermarking as a cooperative provenance tool for compliant ecosystems, not as a reliable detector once content is transformed or laundered through paraphrase.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Is fresh real/human data necessary in every generation, or can curation make self-consuming loops viable?

**Paper A**: Self-Consuming Generative Models go MAD
  Claim: Without sufficient fresh real data each generation, self-consuming models inevitably degrade.
  Evidence: "Without enough fresh real data in each generation... inevitably suffer Model Autophagy Disorder (MAD), losing either quality or diversity"

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Under curated selection, self-consuming synthetic loops can still improve with respect to human preferences.
  Evidence: "curated data provably optimize human preferences" and "increase expected reward"

**Relevance to thesis**: This is the strongest pro-curation counterexample to a blanket 'fresh human data is required' story. It narrows the thesis to open-ended fidelity and social grounding, not all downstream objectives.
**Beat affected**: 4
**Suggested handling**: Acknowledge that 'fresh human data required' is too strong. Reframe as: fresh human data appears important for diversity/tail retention and socially grounded signals, whereas curated synthetic data may suffice for narrower preference-optimization regimes. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C3: 🔴 CRITICAL — scope_disagreement

**Question**: Can recursive use of synthetic data avoid collapse if it remains anchored to real data?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive use of synthetic data causes collapse and tail loss.
  Evidence: "model-generated content in training causes irreversible model collapse"

**Paper B**: Universality of the $π^2/6$ Pathway in Avoiding Model Collapse
  Claim: A mixed real+synthetic regime can avoid collapse across generations.
  Evidence: "augmenting real data with synthetic data across generations universally preserves a fraction π²/6 of statistical efficiency, avoiding model collapse regardless of the specific model family"

**Relevance to thesis**: Undermines any unconditional collapse claim. The defensible thesis is about risk under contamination/recursive reuse, not impossibility when a persistent real-data anchor remains.
**Beat affected**: 4
**Suggested handling**: Distinguish discard-style recursive retraining from anchored augmentation. Note that collapse results are strongest when synthetic data replace rather than complement real data; mixed regimes are a major counterexample. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Can retrieval remain a scalable defense once the web itself is polluted with AI-generated content?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Retrieval-based detection is effective and scalable.
  Evidence: The paper frames retrieval as a scalable defense after classifier-style detectors are evaded.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: Heavy AI pollution causes retrieval collapse: source diversity erodes at 67% contamination, and BM25 permits 19-24% adversarial infiltration.
  Evidence: The study finds large contamination-driven degradation in retrieval quality, while noting only partial resilience from LLM rankers.

**Relevance to thesis**: This supports our caution that open-web defenses may fail exactly when pollution becomes widespread, but it also shows retrieval can still help in cleaner or more controlled settings.
**Beat affected**: 4
**Suggested handling**: Separate provider-side provenance retrieval from open-web retrieval. Acknowledge that retrieval can work with trusted reference corpora, but web-scale retrieval degrades as pollution rises.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Is substantial human supervision necessary to align LLMs to human values?

**Paper A**: 10.1613/jair.1.15348
  Claim: Human participation is central to successful RL systems and should not be minimized away.
  Evidence: The survey argues that human-centric approaches are key to successful RL and have not been adequately prioritized.

**Paper B**: 10.48550/arxiv.2305.03047
  Claim: LLMs can be aligned with minimal human supervision using principle-driven self-alignment.
  Evidence: The paper claims Dromedary can be aligned 'from scratch' with almost no human annotation via principle-driven self-alignment.

**Relevance to thesis**: This directly narrows the space in which we can argue human data remains uniquely valuable. If minimal-supervision self-alignment works, our thesis cannot treat human annotation as universally required for alignment.
**Beat affected**: 4
**Suggested handling**: Acknowledge self-alignment as serious counterevidence. Frame the thesis around cases where principle-driven self-alignment may be weak: contested norms, minority perspectives, high-stakes behavioral calibration, and tasks requiring authentic human interaction traces. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — scope_disagreement

**Question**: Can simulated or AI-generated feedback stand in for human feedback during development of learning-from-feedback methods?

**Paper A**: 10.1613/jair.1.15348
  Claim: Human-centered interaction remains a core requirement for robust RL and alignment.
  Evidence: The survey treats RL as inherently human-in-the-loop and argues human-centric approaches are indispensable.

**Paper B**: 10.48550/arxiv.2305.14387
  Claim: LLM-generated feedback can proxy for human judgments cheaply and with high agreement in simulation.
  Evidence: AlpacaFarm reports a simulation framework using LLM-generated feedback that is 50x cheaper than crowdworkers while maintaining high agreement with human evaluations.

**Relevance to thesis**: This weakens a blanket argument for ongoing human data collection in feedback pipelines. It suggests humans may be most valuable for final validation or harder domains, not necessarily for every iteration of method development.
**Beat affected**: 4
**Suggested handling**: Treat AlpacaFarm as real counterevidence, then immediately note its stated scope limits: relatively simple single-turn instructions and human validation from only 13 crowdworkers. Use that to justify a narrower claim about where human data still matters. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Can AI feedback substitute for human feedback in aligning models to human preferences?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: AI feedback can match human feedback on key alignment tasks.
  Evidence: RLAIF is reported as 'comparable to RLHF across summarization and dialogue tasks,' even when the AI labeler is the same model as the policy.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Instruction tuning does not reliably align models to real human opinion distributions and may amplify bias.
  Evidence: The paper finds 'substantial misalignment with US demographic group opinions' and says instruct-tuning may 'distort opinion distributions'.

**Relevance to thesis**: Directly supports a narrowed version of the thesis: AI feedback may replace humans on utility benchmarks, but not on socially grounded preference representation.
**Beat affected**: 4
**Suggested handling**: Acknowledge that AI feedback is strong for benchmarked summarization/dialogue optimization, but note that this does not imply faithful alignment to diverse human populations or subjective value distributions. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — scope_disagreement

**Question**: Can synthetic instruction data replace human-authored supervision across all alignment objectives?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Self-generated synthetic instructions can substantially improve instruction following without human-written instructions.
  Evidence: Self-Instruct reports a 33% improvement on SUPER-NI 'without relying on human-written instructions'.

**Paper B**: BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dat
  Claim: Nuanced safety alignment benefits from large human-preference datasets with separate helpfulness and harmlessness labels.
  Evidence: BeaverTails introduces 333,963 QA pairs with distinct human annotations for helpfulness and harmlessness to enable safety alignment.

**Relevance to thesis**: This narrows any blanket anti-synthetic claim: synthetic data can replace humans for generic instruction-following, while human-authored supervision remains salient for safety-sensitive and norm-laden objectives.
**Beat affected**: 4
**Suggested handling**: Write that synthetic instruction tuning is effective for general instruction-following tasks, but safety alignment appears to need richer, explicitly human-labeled signals than generic self-generated instruction data provides. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — scope_disagreement

**Question**: Is web-origin data itself the problem, or only low-quality/junk variants of it?

**Paper A**: LLMs Can Get "Brain Rot"!
  Claim: Continual pre-training on junk social media data causes persistent declines in reasoning, safety, and long-context understanding.
  Evidence: Controlled continual pre-training on junk social media induces multifaceted decline that resists large-scale post-hoc tuning.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Filtered and deduplicated web-only data can outperform curated corpora in pretraining.
  Evidence: RefinedWeb reports strong gains from web-only training over curated-corpus baselines.

**Relevance to thesis**: Strongly narrows the thesis: the literature does not support 'web data harms quality' in general; decline appears tied to junky or poorly controlled web inputs, not web provenance alone.
**Beat affected**: 4
**Suggested handling**: Avoid blanket language about web data. Contrast junk-social-media continual pretraining with filtered web-only corpora, and argue that source quality and pipeline design mediate outcomes. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: If we optimize training data for social reasoning, do the core deficits disappear or just move to harder settings?

**Paper A**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Social reasoning robustness can be materially improved through targeted adversarial social-training data.
  Evidence: "significantly improves social reasoning robustness"

**Paper B**: CoMMET: To What Extent Can LLMs Perform Theory of Mind Tasks?
  Claim: Even with modern LLMs, broader multimodal and multi-turn Theory-of-Mind evaluation still reveals major deficits.
  Evidence: "revealing significant LLM deficits" on a "multimodal, multi-turn evaluation covering all ATOMS mental states and moral reasoning"

**Relevance to thesis**: This narrows the thesis rather than overturning it: data composition clearly matters, but gains from text-centric hard-example training may not transfer to richer socially situated settings.
**Beat affected**: 4
**Suggested handling**: Acknowledge that data composition can improve social reasoning on targeted distributions, while emphasizing that broader multimodal and interactive benchmarks still show substantial failure modes. Position socially grounded data as a candidate for closing that transfer gap, not as a proven necessity. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — methodological_tension

**Question**: Does curated synthetic data avert collapse, or does it only optimize a narrower objective?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive training on model-generated data leads to irreversible collapse of the underlying data distribution.
  Evidence: "indiscriminate use of model-generated content... causes irreversible model collapse where tails of the original distribution disappear"

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Curated self-consuming loops can improve aligned performance even when training data are synthetic.
  Evidence: "data curation in self-consuming generative model loops provably increases expected reward and collapses reward variance"

**Relevance to thesis**: Directly constrains any broad anti-synthetic claim: curated synthetic data may fail to preserve rare human-distributional structure while still succeeding on preference/reward objectives.
**Beat affected**: 4
**Suggested handling**: Explicitly separate two notions of success in Related Work: preserving the human data distribution versus optimizing a verifier/reward model. State that curated synthetic data can substitute in alignment-style, bounded objective settings, but not necessarily for retaining long-tail socially grounded behavior. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C1: 🔴 CRITICAL — methodological_tension

**Question**: Do intrinsic diversity metrics provide strong evidence that live-web drift is already causing practical training degradation?

**Paper A**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Recursive training on synthetic text causes measurable degradation across generations.
  Evidence: Reports a consistent decline in lexical, syntactic, and semantic diversity across generations of synthetic retraining.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: Modern multi-snapshot filtered web data still trains stronger models.
  Evidence: FineWeb uses 96 CommonCrawl snapshots with filtering/deduplication and yields better-performing LLMs than other open pretraining datasets.

**Relevance to thesis**: Directly limits Beat 2: metric decline is real in recursive synthetic loops, but that does not by itself show present-day live-web corpora are broadly degrading model quality.
**Beat affected**: 2
**Suggested handling**: State explicitly that diversity metrics are an early-warning signal for recursive reuse, not yet decisive proof of web-wide pretraining decline; contrast controlled synthetic-loop experiments with filtered open-web training results. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🔴 CRITICAL — implicit_tension

**Question**: Do documented crawl-quality pathologies show that scraped web data is already materially degraded as a training source?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: Large web crawls contain substantial quality and contamination problems.
  Evidence: Documents machine-generated text, benchmark contamination, patents, social biases, and disproportionate exclusion of minority voices in C4.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Those problems do not prevent web-only corpora from outperforming curated mixtures when processing is improved.
  Evidence: RefinedWeb argues filtered and deduplicated web data alone significantly outperforms curated corpora.

**Relevance to thesis**: This is a core tension for Beat 2: contamination and skew are real, yet practical model performance can remain strong after aggressive filtering.
**Beat affected**: 2
**Suggested handling**: Do not equate 'documented corpus pathology' with 'observed training failure.' Say that degradation evidence depends heavily on the data-construction pipeline and the evaluation criterion. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Are high detector accuracy numbers enough to claim reliable real-world detection?

**Paper A**: Distinguishing Reality from AI: Approaches for Detecting Synthetic Content
  Claim: Hybrid multimodal detection approaches achieve up to 92% accuracy, outperforming single-modality methods.
  Evidence: The survey highlights top-line gains from combining modalities.

**Paper B**: Simple techniques to bypass GenAI text detectors: implications for inclusive edu
  Claim: Simple post-processing manipulations reduce GenAI text detector accuracy by 17.4%, making them unreliable for academic-integrity enforcement.
  Evidence: The study reports sizable accuracy drops across six major detectors under simple bypass techniques.

**Relevance to thesis**: This narrows blanket skepticism: some hybrid systems look strong on benchmarks, but it also reinforces that deployed text-only detection is brittle under light editing.
**Beat affected**: 4
**Suggested handling**: Do not cite benchmark accuracy as proof of robust detection. Note the scope gap between multimodal lab performance and adversarial, text-only, real-world use.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Do successful prevalence studies in bounded domains show that web-scale AI pollution is readily detectable?

**Paper A**: AI See What You Did There – The Prevalence of LLM-Generated Answers in MOOC Resp
  Claim: AI-generated answers are highly prevalent in MOOC submissions and can be identified through textual analysis metrics over 4,045 responses.
  Evidence: The paper reports high prevalence and identifiability within a constrained educational corpus.

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: General detectability is highly contingent on domain, generator, and detector, making universal detection difficult.
  Evidence: The survey emphasizes strong dependence on domain and method rather than stable cross-context detectability.

**Relevance to thesis**: This matters for honesty in framing: positive detection in a narrow classroom setting is not evidence that open-web contamination can be measured reliably at scale.
**Beat affected**: 4
**Suggested handling**: Use MOOC results only as domain-specific prevalence evidence. Avoid extrapolating them to web-wide pollution or general detector reliability.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Do longitudinal temporal measurements establish broad web degradation, or only degradation within specific genres?

**Paper A**: WWW - Privacy Policies over Time: Curation and Analysis of a Million-Document Da
  Claim: A web genre becomes worse over time on readability and ambiguity measures.
  Evidence: Shows privacy policies are becoming longer, harder to read, and more ambiguous over time, while underreporting third parties and tracking.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: Aggregate filtered web snapshots remain an excellent training source.
  Evidence: FineWeb aggregates 96 CommonCrawl snapshots and still produces better-performing LLMs than other open datasets.

**Relevance to thesis**: This narrows Beat 2 by showing that clear temporal degradation in one institutional genre does not automatically imply overall web-text degradation for pretraining.
**Beat affected**: 2
**Suggested handling**: Use privacy-policy studies as domain-specific evidence of live-web drift, but avoid generalizing from genre deterioration to whole-web training collapse. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Does direct longitudinal evidence of worsening web content imply that current crawl mixtures are degrading overall?

**Paper A**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Claim: Over 25 years, privacy policies have drifted toward more intrusive and opaque content.
  Evidence: Finds increasing use of location data, implicitly collected data, and sharing with unnamed third parties from 1996 to 2021.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Even without curated sources, processed web data can be highly competitive.
  Evidence: RefinedWeb reports web-data-only pretraining significantly outperforms curated-corpus baselines.

**Relevance to thesis**: Again limits how far Beat 2 can go: measurable temporal deterioration exists, but its relevance to general pretraining quality is not settled.
**Beat affected**: 2
**Suggested handling**: Present this as a boundary condition: some live-web subdomains demonstrably worsen over time, yet broad pretraining utility may persist after selection and cleanup. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Is explicit RLHF the crucial ingredient for alignment, or can simpler preference-optimization methods achieve the same result?

**Paper A**: 10.1613/jair.1.15348
  Claim: Alignment should be understood through a human-in-the-loop RL lens, with human-centric RL as a core paradigm.
  Evidence: The survey positions RL itself as fundamentally human-in-the-loop and central to successful systems.

**Paper B**: 10.48550/arxiv.2305.18290
  Claim: The RLHF optimization stage can be removed without losing performance.
  Evidence: DPO uses a simple cross-entropy objective and reports matching or exceeding RLHF performance without reinforcement learning.

**Relevance to thesis**: This does not show human data is unnecessary, but it does undermine any claim that the RLHF machinery itself is where human value resides. It shifts the argument toward the source and content of preferences rather than the RL algorithm.
**Beat affected**: 4
**Suggested handling**: State clearly that recent work separates human preference information from the PPO-style RLHF pipeline. Our paper should argue about when authentic human signals matter, not imply that online RLHF is always required. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — methodological_tension

**Question**: Do alignment gains require full RLHF pipelines, or can lightweight ranking-based optimization suffice once preference signals exist?

**Paper A**: 10.1613/jair.1.15348
  Claim: Human-in-the-loop RL remains a central conceptual model for successful alignment.
  Evidence: The survey emphasizes human-centric RL as fundamental rather than incidental.

**Paper B**: 10.48550/arxiv.2304.05302
  Claim: A simpler ranking-based objective can match PPO-style RLHF alignment performance.
  Evidence: RRHF aligns models by ranking sampled responses with conditional log-probabilities and reports performance comparable to PPO while being simpler to train and scale.

**Relevance to thesis**: Like DPO, RRHF narrows where human data is plausibly indispensable. It suggests that once preference information exists, heavy RLHF infrastructure may not be necessary.
**Beat affected**: 4
**Suggested handling**: Mention RRHF alongside DPO as evidence that the field is collapsing the optimization stack around preference learning. Then clarify that our thesis concerns the provenance and groundedness of preference data, not a defense of complex RLHF pipelines. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Does a preference-optimization stage materially improve alignment, or is it brittle and dependent on data-collection details?

**Paper A**: Zephyr: Direct Distillation of LM Alignment
  Claim: AI-feedback preference distillation can produce very strong alignment gains cheaply and simply.
  Evidence: Zephyr claims a 7B model aligned with AI-feedback DPO can outperform LLaMA2-Chat-70B on MT-Bench without PPO.

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: Even with human feedback data, RLHF may fail to consistently improve over SFT.
  Evidence: OpenAssistant notes RLHF 'did not uniformly improve over SFT models,' likely due reward-model training on human-generated rather than model-generated messages.

**Relevance to thesis**: The disagreement is not only about human vs AI feedback; it also shows that conclusions depend heavily on pipeline design and evaluation choice. This weakens simple generalizations from either camp.
**Beat affected**: 4
**Suggested handling**: Frame this as a methodological split: preference optimization can look highly effective under some data/evaluation setups, but brittle under others. Avoid treating any single alignment recipe as settled. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — implicit_tension

**Question**: Is provenance the main bottleneck, or can aggressive data-quality engineering offset lack of fresh human collection?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Synthetic recursive reuse destroys important low-frequency structure in the training distribution.
  Evidence: "tails of the original distribution disappear due to compounding statistical and functional approximation errors"

**Paper B**: Yi: Open Foundation Models by 01.AI
  Claim: Careful curation can dominate scale and architecture in practice.
  Evidence: "data quality engineering rather than architectural innovation" and "smaller models on higher-quality data outperform larger models on lower-quality data"

**Relevance to thesis**: Indirectly weakens any simple provenance-first story by showing that curation quality can outweigh raw scale on benchmark performance, even if this does not specifically validate synthetic substitution.
**Beat affected**: 4
**Suggested handling**: Use this as a boundary-setting citation: curation clearly matters a great deal for mainstream LM performance, but that does not resolve whether curated synthetic data preserves socially grounded, behaviorally authentic, long-tail human signals. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Do current detection methods justify strong claims that AI content is already dominating the web?

**Paper A**: The Dead Internet Theory: Investigating the Rise of AI-Generated Content and Bot
  Claim: The Dead Internet Theory is substantiated by growing evidence that bots and AI-generated content increasingly dominate online interactions.
  Evidence: The paper claims growing evidence for AI/bot dominance fundamentally altering the internet's structure.

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Universal detection is highly challenging because detectability depends on generation method, domain, and detection approach.
  Evidence: The survey concludes detectability varies across interacting factors and general detection remains difficult.

**Relevance to thesis**: This creates a scale-estimation problem: broad claims about web domination may outrun what current detectors can actually verify.
**Beat affected**: 4
**Suggested handling**: Treat web-domination claims as suggestive rather than settled. Emphasize that scale estimates remain uncertain without auditable provenance or stronger measurement methods.

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Does rising AI-generated content in major web knowledge sources prove downstream quality decline for filtered web corpora?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: AI-generated content in newly created Wikipedia pages has increased markedly since GPT-3.5, establishing lower bounds on contamination in a major source.
  Evidence: Study finds a marked post-GPT-3.5 increase in AI-generated newly created Wikipedia pages.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: Despite web-scale noise, systematic filtering and deduplication still yield a stronger pretraining corpus.
  Evidence: FineWeb's filtered 15-trillion-token dataset produces better-performing LLMs than other open pretraining datasets.

**Relevance to thesis**: This blocks an overly linear argument from contamination prevalence to quality decline: contamination can be rising in important sources without implying that all filtered web corpora are already low-value.
**Beat affected**: 4
**Suggested handling**: Use Wikipedia contamination as provenance-risk evidence, but do not treat prevalence estimates as direct causal evidence of pretraining-quality collapse; explicitly say filtering pipelines may buffer some of this contamination. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — implicit_tension

**Question**: Do documented CommonCrawl flaws preclude competitive downstream performance in other modalities?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: CommonCrawl-derived C4 has notable contamination and bias problems.
  Evidence: C4 analysis identifies machine-generated text, benchmark contamination, and socially skewed filtering effects.

**Paper B**: Demystifying CLIP Data
  Claim: Careful metadata-driven curation and balancing of raw CommonCrawl can outperform a strong proprietary dataset in vision-language pretraining.
  Evidence: MetaCLIP's curated CommonCrawl-derived data outperforms CLIP's proprietary data source.

**Relevance to thesis**: This extends the scope limiter beyond text-only LLMs: documented web-corpus flaws are real, but they do not make web-derived data noncompetitive once curation is strong.
**Beat affected**: 4
**Suggested handling**: Acknowledge documentation papers as governance and bias warnings, then note that multimodal evidence also shows rehabilitated CommonCrawl can remain high-performing. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🟡 MODERATE — implicit_tension

**Question**: Can high-quality synthetic conversation data replace human-origin data for socially competent behavior?

**Paper A**: Enhancing Chat Language Models by Scaling High-quality Instructional Conversatio
  Claim: Large-scale, diverse, high-quality synthetic instructional conversations substantially improve chat-model performance without human queries.
  Evidence: "Scaling diverse, high-quality synthetic instructional conversation data (UltraChat) significantly improves open-source chat language models without requiring human queries"

**Paper B**: Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large L
  Claim: Strong chat behavior does not imply robust social reasoning; LLMs still fail adversarial Theory-of-Mind stress tests.
  Evidence: "LLMs exhibit limited and non-robust Theory of Mind abilities" and fail on adversarial examples

**Relevance to thesis**: Important tension for any claim favoring socially grounded human data: synthetic conversation data can clearly improve general chat quality, but benchmark evidence suggests those gains do not automatically become robust social reasoning.
**Beat affected**: 4
**Suggested handling**: Write that synthetic dialogue data is effective for broad instruction/chat performance, but current evidence does not show that it substitutes for socially grounded data on adversarial social reasoning. Avoid claiming synthetic data is uniformly inadequate; say its success is task-dependent. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Does careful curation of a very small dataset suffice for social intelligence, or only for superficial alignment?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: A tiny set of 1,000 carefully curated examples can yield competitive aligned behavior, supporting the Superficial Alignment Hypothesis.
  Evidence: "Fine-tuning a 65B LLaMA model on only 1,000 carefully curated examples without RLHF produces competitive performance"

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: Scaling and generic pretrained competence are not enough for social intelligence; GPT-3 still lags humans by over 30% on mental-state reasoning tasks.
  Evidence: "GPT-3 models lag behind humans by over 30% on social intelligence tasks and struggle with mental state reasoning"

**Relevance to thesis**: This is a real but indirect tension: curation can strongly affect generic alignment behavior, yet that should not be conflated with genuine social reasoning. It supports a narrower thesis that composition matters, while warning against overinterpreting chat-style gains.
**Beat affected**: 4
**Suggested handling**: Use this pair to distinguish alignment/helpfulness from social reasoning. State that small, curated datasets can produce impressive conversational alignment, but benchmark evidence shows that such gains do not establish Theory-of-Mind competence. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟢 MINOR — implicit_tension

**Question**: Is large-scale synthetic instruction generation the main route to reducing human supervision, or can a very small curated human set do as well?

**Paper A**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: Scaling synthetic, increasingly complex instructions is an effective substitute for manual instruction authoring.
  Evidence: WizardLM says Evol-Instruct rewrites instructions with LLMs and the resulting data lets WizardLM outperform Alpaca and Vicuna.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: A tiny set of carefully curated human examples can be enough for competitive alignment without RLHF.
  Evidence: LIMA reports competitive performance from only 1,000 curated examples and argues for a 'Superficial Alignment Hypothesis'.

**Relevance to thesis**: These papers do not directly conflict on whether human supervision can be reduced, but they disagree on the best mechanism: synthetic scale versus small, high-quality human curation.
**Beat affected**: 4
**Suggested handling**: Mention that open-alignment work diverges on whether gains come mainly from synthetic scaling or from a small amount of high-quality human-authored data; this matters for how much human collection CampusGo would need to justify. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---


## Summary

Total contradictions: 34
Critical (must address): 20

## Thesis Risk Assessments

- The main risk to the thesis is overstatement. Several papers provide credible counterexamples showing that collapse is not universal: curated synthetic loops can improve preference reward, verifier/correction functions can stabilize self-consuming training, and mixed real+synthetic regimes can avoid collapse in theory. The thesis remains defensible only if framed narrowly: uncurated or weakly anchored recursive reuse is risky, while curated or verifier-screened synthetic data may substitute in bounded objectives but is not yet shown to preserve full human distributional richness or socially grounded behavioral signals.
- The strongest risk to our thesis is overclaiming detectability at web scale. The literature does not support a simple story that AI pollution can be cleanly measured or filtered out: classifier-style detectors are brittle, watermarking fails under paraphrase, and even retrieval-based defenses split sharply between controlled/provider-side settings and polluted open-web settings. At the same time, some papers do show workable detection or provenance signals in bounded conditions, so we should not imply detection is impossible. The honest position is narrower: web pollution is plausibly serious, but measuring or excluding it at web scale remains method-limited and assumption-sensitive.
- Beat 2 is supportable only in a qualified form. The evidence for measurable drift or degradation is strongest when it is direct and localized: temporal audits of privacy policies, contamination growth in Wikipedia, and corpus audits like C4. But the strongest counterweight is practical: FineWeb and RefinedWeb show that large-scale filtered web mixtures still produce very strong models. So the literature supports saying that live-web contamination and drift are measurable and increasingly salient, not that they have already produced a clear, general, corpus-wide pretraining degradation visible in downstream performance.
- Risk is significant. The selected F papers provide real counterevidence to any broad thesis that human feedback is generally required for alignment: RLAIF and AlpacaFarm show AI-feedback can work well on bounded tasks, and DPO/RRHF show the RLHF pipeline itself is often not necessary once preference information exists. The defensible version of the thesis is narrower: human data remains especially valuable where preferences are socially grounded, difficult to simulate, normatively contested, or require authentic interaction traces rather than benchmark-style proxy judgments.
- High-profile papers in this set make it untenable to claim that human-authored supervision is broadly necessary for instruction following or benchmarked preference optimization. Self-Instruct, WizardLM, RLAIF, Zephyr, and Dromedary all provide evidence that synthetic instructions, AI feedback, or self-alignment can substantially reduce human supervision in bounded settings. The safer, more defensible thesis is
- High risk if the paper states or implies a blanket contamination-to-quality-decline law for web data. RefinedWeb, FineWeb, and MetaCLIP all show that aggressively filtered, deduplicated, or otherwise engineered web corpora can outperform curated or proprietary alternatives. The safer thesis is narrower: unfiltered, recursively reused, junk, or heavily AI-polluted web data creates serious risks, but documentation and filtering can partially preserve or recover training value, even though bias, benchmark contamination, and minority-voice exclusion may persist.
- The main risk is overstating benchmark failures as evidence that socially grounded human data is uniquely necessary. Among these papers, the strongest direct challenge is Social-R1, which shows that targeted social-data construction can materially improve robustness. At the same time, the benchmark papers remain strong evidence that generic instruction tuning, chat optimization, and untargeted scaling do not reliably produce robust social reasoning, especially in adversarial, multimodal, multi-turn, or embodied settings. The safest thesis is therefore: data composition clearly matters for social reasoning, but current successes are narrow and do not yet invalidate the need for more authentic socially grounded data.

## Unresolved Tensions

- Do curated synthetic loops preserve rare human behaviors, or only optimize whatever the reward/verifier measures?
- How much persistent real data is enough to prevent collapse in practice, beyond the theoretical mixed-data results?
- Are correction/verification mechanisms realistic at scale, or do they smuggle in human grounding through reward models, filters, or correction oracles?
- Do curation successes on standard pretraining benchmarks transfer to socially grounded tasks where authenticity and long-tail variation matter most?
- Whether provider-side retrieval/provenance systems can scale across firms and privacy constraints without becoming unusable or incomplete.
- How robust LLM-ranker resilience remains as contamination rises beyond the reported BM25-focused retrieval-collapse settings.
- How to estimate true web-scale AI pollution when prevalence studies are domain-bounded and many detectors are vulnerable to paraphrase or light post-editing.
- Whether hybrid multimodal detectors retain their reported advantage under realistic adversarial transformations rather than static benchmark conditions.
- Whether diversity-style intrinsic metrics are predictive of downstream degradation on real open-web corpora rather than only in controlled recursive-synthetic settings.
- Whether source-specific contamination findings such as Wikipedia lower bounds extrapolate to CommonCrawl-scale training mixtures.
- Whether filtering and deduplication are merely masking accumulating web degradation at current scales or can robustly offset it over time.
- How much temporal drift in narrow but important genres like privacy policies should count as evidence about the overall quality of the live web for language-model pretraining.
- None of the strongest AI-feedback success papers directly test tasks requiring lived experience, minority viewpoints, longitudinal social behavior, or other authentic human-grounded signals.
- RLAIF and AlpacaFarm are strong evidence for substitution on summarization/dialogue or simple single-turn instruction settings, but they do not settle whether AI feedback preserves preference diversity or avoids self-reinforcing bias under broader deployment.
- DPO and RRHF weaken the case for RLHF as a pipeline, but they do not answer whether the underlying preference labels should come from humans, curated synthetic sources, or AI judges.
- The literature shown here separates two questions that our paper must keep distinct: whether human data is needed at all, and where in the stack it is needed most (data collection, evaluation, final calibration, or continual monitoring).
- The field still lacks a clean bridge from contamination-prevalence measurements to causal estimates of downstream pretraining degradation.
- Filtered-web success papers mostly optimize benchmark performance, while documentation papers emphasize representational harms, bias, and contamination that may not show up in standard evaluations.
- Retrieval collapse results suggest live web consumption may be much more fragile than static pretraining on curated snapshots, but the boundary between those regimes is not yet well characterized.
- Do Social-R1-style gains transfer to out-of-distribution social tasks, or are they mostly improvements on the trained adversarial template family?
- Do synthetic or self-generated instruction datasets improve actual Theory-of-Mind competence, or mainly chat/instruction benchmark performance that is only weakly coupled to social reasoning?
- How much of current benchmark weakness reflects missing social-experience data versus benchmark artifacts, shortcut-sensitive evaluation, or modality gaps such as spatial, visual, and multi-turn grounding?