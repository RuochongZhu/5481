# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## Executive Summary

1. When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) → Does recursive synthetic reuse inevitably cause collapse, or can human-preference curation make it beneficial?
   Handling: State explicitly that collapse evidence targets indiscriminate reuse, whereas successful substitution requires a strong verifier/curation signal; note that the positive result is theoretical and depends on well-specified rewards. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.
2. Is web pollution detectable? (pollution scale vs detection limits) → Are retrieval-based defenses robust enough to detect paraphrased AI text?
   Handling: State explicitly that retrieval defenses work in some controlled paraphrase settings but fail under stronger adaptive paraphrasing. Use this to justify 'reactive filtering is fragile' rather than claiming retrieval is broadly effective.
3. How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) → Does longitudinal degradation in one live-web domain justify a broad claim of measurable web-wide degradation relevant to pretraining?
   Handling: State explicitly that existing temporal degradation evidence is domain-specific rather than web-wide. Use privacy-policy results as proof of drift in particular genres, not as proof that the whole web is measurably degrading for pretraining. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
4. Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) → Can AI-generated feedback replace human feedback for alignment?
   Handling: State explicitly that AI feedback has real success on bounded, evaluable tasks, but distinguish this from normatively grounded alignment where human oversight and human-defined objectives remain necessary. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
5. Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? → Does rising AI contamination already make web-based corpora inferior to curated sources for model quality?
   Handling: State explicitly that current harm evidence is strongest for live retrieval/search ecosystems, not for all pretraining corpora. Use RefinedWeb as a scope limiter: filtered static corpora can still work well even if polluted live web retrieval degrades. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
6. Does data composition matter for social reasoning? (benchmarks vs ablation) → Can targeted post-training data substantially reduce social-reasoning deficits, or are those deficits mostly intrinsic to current LLMs?
   Handling: State explicitly that benchmark weakness results are for untargeted models; contrast them with evidence that socially targeted hard-example training can improve outcomes, while noting the two papers evaluate different training conditions. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

## Focus Coverage

- [A, E] When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) (count=5)
  Representative: Does recursive synthetic reuse inevitably cause collapse, or can human-preference curation make it beneficial?
- [B, C] Is web pollution detectable? (pollution scale vs detection limits) (count=5)
  Representative: Are retrieval-based defenses robust enough to detect paraphrased AI text?
- [D, H] How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) (count=4)
  Representative: Does longitudinal degradation in one live-web domain justify a broad claim of measurable web-wide degradation relevant to pretraining?
- [E, F] Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) (count=6)
  Representative: Can AI-generated feedback replace human feedback for alignment?
- [B, E, H] Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? (count=5)
  Representative: Does rising AI contamination already make web-based corpora inferior to curated sources for model quality?
- [I, J] Does data composition matter for social reasoning? (benchmarks vs ablation) (count=6)
  Representative: Can targeted post-training data substantially reduce social-reasoning deficits, or are those deficits mostly intrinsic to current LLMs?
- [F, J] How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? (count=2)
  Representative: How far can synthetic instruction data replace human-written instruction datasets?

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Does recursive synthetic reuse inevitably cause collapse, or can human-preference curation make it beneficial?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate recursive training on model-generated data causes irreversible model collapse.
  Evidence: Reports loss of distribution tails and irreversible degradation across successive generations when model-generated content is reused indiscriminately.

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Curated synthetic data can improve outcomes rather than collapse, if filtered by human preferences.
  Evidence: Proves that human-preference curation in self-consuming loops increases expected reward and converges to preference-optimal distributions; authors note this assumes an idealized reward signal.

**Relevance to thesis**: This is the strongest pro-curation counterexample to any blanket claim that synthetic reuse necessarily degrades model quality.
**Beat affected**: 1
**Suggested handling**: State explicitly that collapse evidence targets indiscriminate reuse, whereas successful substitution requires a strong verifier/curation signal; note that the positive result is theoretical and depends on well-specified rewards. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Are retrieval-based defenses robust enough to detect paraphrased AI text?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Retrieval-based detection is an effective and scalable defense even when paraphrasing defeats standard AI-text detectors.
  Evidence: Using DIPPER paraphrasing, the paper reports that all current detectors fail, but retrieval-based detection remains effective.

**Paper B**: Can AI-Generated Text be Reliably Detected?
  Claim: Retrieval-based detectors are not robust under stronger adaptive attacks.
  Evidence: The paper shows recursive paraphrasing can break watermarking, neural-net, zero-shot, and retrieval-based detectors while maintaining text quality.

**Relevance to thesis**: Directly undermines any blanket claim that retrieval is a robust reactive filter. At best, retrieval helps under weaker paraphrase attacks; it is not a settled solution.
**Beat affected**: 1
**Suggested handling**: State explicitly that retrieval defenses work in some controlled paraphrase settings but fail under stronger adaptive paraphrasing. Use this to justify 'reactive filtering is fragile' rather than claiming retrieval is broadly effective.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Does longitudinal degradation in one live-web domain justify a broad claim of measurable web-wide degradation relevant to pretraining?

**Paper A**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Claim: A long-running web genre can measurably worsen over time.
  Evidence: Privacy policies from 1996–2021 show increasing location-data use, implicit data collection, reduced meaningful choice, and more sharing with unnamed third parties.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: Large multi-snapshot web data remains highly usable for pretraining after filtering.
  Evidence: FineWeb builds 15T tokens from 96 Common Crawl snapshots and reports better LLM performance than other open pretraining datasets.

**Relevance to thesis**: Directly limits any claim that live-web degradation has already been demonstrated at web scale. The strongest temporal evidence is genre-specific, while broad-web downstream evidence still shows filtered web data working well.
**Beat affected**: 2
**Suggested handling**: State explicitly that existing temporal degradation evidence is domain-specific rather than web-wide. Use privacy-policy results as proof of drift in particular genres, not as proof that the whole web is measurably degrading for pretraining. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Can AI-generated feedback replace human feedback for alignment?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: RLAIF can substitute for RLHF on key alignment tasks.
  Evidence: Reports performance comparable to RLHF on summarization and dialogue, including self-improvement when the AI labeler is the same model as the policy.

**Paper B**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Successful RL remains fundamentally human-in-the-loop.
  Evidence: Survey explicitly frames RL as a human-in-the-loop paradigm requiring human-centric approaches for successful deployment.

**Relevance to thesis**: This is the strongest counterevidence to any broad claim that human feedback is generally indispensable. Our thesis only survives if narrowed to socially grounded or deployment-critical settings rather than generic alignment benchmarks.
**Beat affected**: 2
**Suggested handling**: State explicitly that AI feedback has real success on bounded, evaluable tasks, but distinguish this from normatively grounded alignment where human oversight and human-defined objectives remain necessary. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Does rising AI contamination already make web-based corpora inferior to curated sources for model quality?

**Paper A**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Properly filtered and deduplicated web data alone can produce LLMs that significantly outperform models trained on curated high-quality corpora.
  Evidence: RefinedWeb is a web-data-only corpus; Falcon models trained on it are reported to outperform models trained on curated corpora.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content causes Retrieval Collapse, where synthetic pages dominate search results, reduce source diversity, and admit low-quality or adversarial content.
  Evidence: Controlled experiments show a two-stage collapse: synthetic content first wins retrieval visibility, then degrades retrieval pipelines.

**Relevance to thesis**: This directly undermines any simple contamination-equals-decline narrative: strong performance from heavily filtered web corpora coexists with strong harm evidence in live retrieval settings.
**Beat affected**: 1
**Suggested handling**: State explicitly that current harm evidence is strongest for live retrieval/search ecosystems, not for all pretraining corpora. Use RefinedWeb as a scope limiter: filtered static corpora can still work well even if polluted live web retrieval degrades. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Can targeted post-training data substantially reduce social-reasoning deficits, or are those deficits mostly intrinsic to current LLMs?

**Paper A**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: Out-of-the-box GPT-3 models substantially underperform humans on social intelligence and mental-state reasoning.
  Evidence: GPT-3 lagged humans by over 30% on social intelligence benchmarks and struggled more on mental-state reasoning than factual questions.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Targeted training on adversarially hard social-reasoning data can materially improve genuine social reasoning and robustness.
  Evidence: RL with verifiable feedback on hard social reasoning examples significantly improved social reasoning and robustness over superficial pattern matching baselines.

**Relevance to thesis**: Directly affects line 2: it supports the idea that data composition matters, but it weakens any phrasing that treats benchmark failures as evidence of fixed incapacity rather than missing socially targeted post-training data.
**Beat affected**: 2
**Suggested handling**: State explicitly that benchmark weakness results are for untargeted models; contrast them with evidence that socially targeted hard-example training can improve outcomes, while noting the two papers evaluate different training conditions. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: How far can synthetic instruction data replace human-written instruction datasets?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Synthetic self-generated instruction data can substantially reduce reliance on human-written instruction sets.
  Evidence: Self-Instruct reports a 33% absolute improvement on SUPERNI over the original GPT-3 using self-generated instructions for fine-tuning.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: A
  Evidence: N/A

**Relevance to thesis**: N/A
**Beat affected**: N/A
**Suggested handling**: State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Is fresh real data required in every generation, or can verification/correction let synthetic data substitute for it?

**Paper A**: Self-Consuming Generative Models go MAD
  Claim: Without enough fresh real data each generation, self-consuming models are doomed to lose quality or diversity.
  Evidence: Claims Model Autophagy Disorder occurs unless each generation is supplemented with sufficient fresh real data.

**Paper B**: Self-Correcting Self-Consuming Loops for Generative Model Training
  Claim: A verified correction step can stabilize self-consuming loops even without continual fresh human data.
  Evidence: Shows that adding a correction function that maps samples toward the true distribution makes self-consuming training exponentially more stable.

**Relevance to thesis**: This directly challenges any strong necessity claim that only fresh human data can prevent recursive degradation.
**Beat affected**: 1
**Suggested handling**: Phrase the thesis conditionally: fresh human data is the safest anchor, but verifier-like correction mechanisms may substitute under access to a reliable correction function approximating the true distribution. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Does strong benchmark performance under AI-feedback imply that human data is no longer needed for socially grounded alignment?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: AI feedback can produce alignment quality comparable to human feedback.
  Evidence: Comparable RLHF-level results are reported on summarization and dialogue tasks.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Instruction-tuned LMs remain socially misaligned with real human opinion distributions.
  Evidence: Finds substantial misalignment with US demographic groups' opinions, with instruct-tuning shifting outputs toward liberal views.

**Relevance to thesis**: This directly supports our narrowing claim: AI-feedback success on utility-style tasks does not settle socially grounded alignment. Human data remains valuable when the target is plural, demographic, and opinion-sensitive.
**Beat affected**: 2
**Suggested handling**: In Related Work, separate task-success alignment from representational social alignment. Cite RLAIF as genuine counterevidence on bounded tasks, then cite opinion-distribution misalignment as the reason human data still matters on socially grounded tasks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Does observed web pollution imply that large-scale web pretraining corpora are already net harmful?

**Paper A**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, built from 96 Common Crawl snapshots with systematic deduplication and filtering, yields better-performing LLMs than other open pretraining datasets.
  Evidence: FineWeb reports superior LLM performance from a 15-trillion-token filtered web corpus.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web pollution structurally degrades retrieval by collapsing source diversity and enabling low-quality infiltration.
  Evidence: Retrieval Collapse is presented as an empirical consequence of synthetic-content proliferation on the web.

**Relevance to thesis**: FineWeb is a strong counterexample to any blanket claim that more contaminated web data necessarily means worse model quality today.
**Beat affected**: 1
**Suggested handling**: Contrast offline corpus construction with live retrieval exposure. Emphasize that contamination risk is rising, but web-scale quality decline is not yet established because aggressive filtering/deduplication can still produce strong pretraining corpora. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🔴 CRITICAL — methodological_tension

**Question**: Does adding synthetic data across generations inevitably trigger collapse, or can mixed real+synthetic training avoid it?

**Paper A**: Strong Model Collapse
  Claim: Even very small amounts of synthetic data can induce strong collapse.
  Evidence: Finds in a high-dimensional regression framework that as little as 1% synthetic data causes strong model collapse, with no benefit from increasing training set size.

**Paper B**: Universality of the $π^2/6$ Pathway in Avoiding Model Collapse
  Claim: Synthetic augmentation can avoid collapse if real data continues to be included.
  Evidence: Proves that augmenting real data with synthetic data across generations preserves a statistical efficiency of π²/6 relative to real-only training and avoids collapse.

**Relevance to thesis**: These papers point in opposite directions on the central substitution question; our thesis cannot ignore that some formal analyses predict safe synthetic augmentation.
**Beat affected**: 1
**Suggested handling**: Discuss them together as assumption-sensitive theory: one models severe collapse from contamination, the other models a regime with persistent real-data anchoring; avoid universal language about any nonzero synthetic fraction being fatal. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🔴 CRITICAL — methodological_tension

**Question**: Can intrinsic metric declines in controlled synthetic-recursion studies be treated as evidence of measurable live-web drift?

**Paper A**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Synthetic recursion produces measurable degradation on linguistic-diversity metrics.
  Evidence: Across recursive training generations, lexical, syntactic, and semantic diversity consistently decrease.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: A broad, temporally distributed web corpus still yields strong downstream results after filtering.
  Evidence: FineWeb aggregates 96 Common Crawl snapshots and reports improved LLM performance over other open datasets.

**Relevance to thesis**: This is a core evidentiary gap for Beat 2. Metric-based collapse/degradation results show a mechanism under controlled synthetic reuse, but they do not establish that comparable degradation is already measurable on the live web.
**Beat affected**: 2
**Suggested handling**: Do not present synthetic-recursion metric papers as direct evidence of current live-web degradation. Use them as mechanism/risk evidence, then separately note that web-scale temporal measurement remains limited. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: Does post-training reliably improve social reasoning, or can it produce brittle gains and even worsen social-competence failures?

**Paper A**: Traces of Social Competence in Large Language Models
  Claim: Post-training helps only partially on false-belief tasks, and some reasoning-oriented fine-tuning makes social-reasoning behavior less robust.
  Evidence: Across 17 models and 192 false-belief variants, instruction tuning only partially helped; reasoning-oriented fine-tuning amplified problematic response patterns and robustness broke across false/true and explicit/implicit variants.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Carefully designed social-reasoning training improves genuine reasoning rather than just superficial pattern matching.
  Evidence: Adversarial hard-example RL with verifiable feedback significantly improved genuine social reasoning and robustness.

**Relevance to thesis**: This is the sharpest tension for line 2: it shows that 'better fine-tuning data' is too coarse a claim. Some post-training regimes help, while others create brittle or misleading gains.
**Beat affected**: 2
**Suggested handling**: Write that data composition matters conditionally: generic instruction/reasoning fine-tuning is not enough, whereas task-targeted, adversarially constructed social data may help. Do not generalize from one post-training setup to all others. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — implicit_tension

**Question**: Can retrieval remain a reliable defense once the web itself is polluted?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Retrieval is an effective and scalable defense for detecting AI-generated text.
  Evidence: The paper argues retrieval succeeds where detector-style methods fail on paraphrased text.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content can corrupt retrieval pipelines themselves.
  Evidence: The paper reports a two-stage Retrieval Collapse in which synthetic content dominates search results, erodes source diversity, and later enables low-quality or adversarial content to infiltrate retrieval.

**Relevance to thesis**: This is a key tension for the web-pollution question: retrieval may work only while the reference corpus is trusted. If the corpus is polluted, retrieval stops being a clean defense.
**Beat affected**: 1
**Suggested handling**: Separate 'retrieval as a detector against a trusted corpus' from 'retrieval over a polluted web.' Note that the latter can collapse, so retrieval is not a complete answer to web-scale pollution detection.

---

## C2: 🔴 CRITICAL — implicit_tension

**Question**: Has rising AI-generated content on the live web already translated into measurable degradation of web-scale pretraining data?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: AI-generated content is measurably increasing in a major live-web knowledge source.
  Evidence: For newly created Wikipedia pages after GPT-3.5, detectors estimate at least 5% are AI-generated at a 1% false-positive threshold.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Web-only training data can still beat curated corpora when properly filtered.
  Evidence: RefinedWeb reports that deduplicated, filtered web data alone significantly outperforms models trained on curated high-quality corpora.

**Relevance to thesis**: This undermines any strong claim that observed live-web AI contamination is already causing broad downstream degradation. Contamination growth is real in at least one important domain, but current evidence does not show that it has yet broken web-scale pretraining.
**Beat affected**: 2
**Suggested handling**: Frame the result as 'rising contamination risk with localized temporal evidence,' not as proven ecosystem-wide degradation. Emphasize that current practical harm appears at least partly mitigable by filtering. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🔴 CRITICAL — implicit_tension

**Question**: Is human feedback straightforwardly beneficial for alignment, or can it systematically inject the wrong social behavior?

**Paper A**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: Large-scale human-generated conversation data is a valuable resource for democratizing alignment.
  Evidence: Presents a crowdsourced human conversation dataset and motivates human-generated data as central to open-source alignment research.

**Paper B**: AI Supported Degradation of the Self Concept: A Theoretical Framework Grounded i
  Claim: Human-feedback training can actively encourage sycophancy.
  Evidence: Reports that assistants finetuned with human feedback consistently show sycophantic behavior because preference data rewards agreement with user beliefs over truth.

**Relevance to thesis**: This undermines any naive version of our thesis that 'more human data is better.' Human data can be uniquely valuable for social grounding, but badly designed human preference collection can also damage truthfulness.
**Beat affected**: 2
**Suggested handling**: Be explicit that the value of human data depends on annotation protocol and target behavior. Frame the thesis around representative, truth-sensitive, behaviorally diverse human data, not human feedback in the abstract. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — implicit_tension

**Question**: Can self-alignment with minimal human supervision align models to human values in a socially meaningful sense?

**Paper A**: Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Hum
  Claim: Models can self-align to human values with minimal human supervision.
  Evidence: SELF-ALIGN claims principle-driven reasoning can achieve competitive alignment without extensive human annotations.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Alignment tuning can still leave models socially misaligned with real human groups.
  Evidence: Language models show substantial misalignment with US demographic groups' opinions, and instruct-tuning consistently distorts outputs toward liberal views.

**Relevance to thesis**: This is a core risk for our argument line: benchmark-level self-alignment success does not establish alignment to plural, socially grounded human values. If we overgeneralize, this contradiction undermines the thesis.
**Beat affected**: 2
**Suggested handling**: Separate generic assistant helpfulness from demographic or societal representativeness. Present self-alignment as promising for some behaviors, not as evidence that human-authored supervision is unnecessary for socially grounded alignment. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Can curated synthetic data substitute for fresh human data in self-consuming training loops?

**Paper A**: Self-Consuming Generative Models go MAD
  Claim: Fresh real data is needed each generation to avoid autophagy.
  Evidence: States self-consuming generative models are doomed to MAD without enough fresh real data in each generation.

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Curated synthetic data can substitute for fresh human data when selection is guided by human preferences.
  Evidence: Shows preference-curated synthetic reuse improves expected reward and converges to a preference-optimal distribution instead of collapsing.

**Relevance to thesis**: This is a direct tension over whether 'fresh human data' is a hard requirement or only one way to supply a trustworthy selection signal.
**Beat affected**: 1
**Suggested handling**: Clarify that 'fresh human data' and 'human preference supervision over synthetic data' are different interventions; the latter may work if the preference signal is accurate and sustained. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Are collapse results about recursive reuse still expected when real data is retained and synthetic data is curated or mixed in?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive use of model-generated content produces irreversible collapse.
  Evidence: Documents tail-disappearance and irreversible degradation over generations under recursive reuse.

**Paper B**: Universality of the $π^2/6$ Pathway in Avoiding Model Collapse
  Claim: Recursive training need not collapse if synthetic data augments rather than replaces real data.
  Evidence: Shows a universal π²/6-efficiency pathway in which real-data augmentation with synthetic data across generations avoids model collapse.

**Relevance to thesis**: This narrows the thesis from 'recursive synthetic reuse is dangerous' to the more defensible 'replacement-style or weakly filtered reuse is dangerous.'
**Beat affected**: 1
**Suggested handling**: In Related Work, distinguish replacement regimes from augmentation regimes and say that collapse is not yet theoretically or empirically universal once real-data anchoring is preserved. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Do high-performing domain-specific classifiers show that web pollution is broadly detectable?

**Paper A**: From Perceptions To Evidence: Detecting AI-Generated Content In Turkish News Med
  Claim: A fine-tuned classifier can reliably detect AI-rewritten news and estimate prevalence over time.
  Evidence: The paper reports 97.08% F1 on Turkish news and claims cross-source, temporally stable prevalence estimates from 2023 to 2026.

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: No current detection method is universally reliable across models and domains.
  Evidence: The survey concludes detectability depends on interacting factors including generation model, domain, and detection method, so no single approach is universally reliable.

**Relevance to thesis**: This narrows the thesis: we cannot say detection is impossible. Some narrow-domain, task-specific detectors work well. But those results do not establish open-web detectability.
**Beat affected**: 1
**Suggested handling**: Present such studies as positive but scoped evidence: detector-based prevalence estimation can work in homogeneous domains, yet this does not prove reliable web-scale contamination measurement.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Can provenance-style watermarking make synthetic text reliably detectable?

**Paper A**: A Watermark for Large Language Models
  Claim: LLM outputs can be watermarked with negligible quality loss and detected statistically without model access.
  Evidence: The paper proposes a computationally efficient watermark detectable by a z-test on green-list token frequency.

**Paper B**: Can AI-Generated Text be Reliably Detected?
  Claim: Watermark-based detection is not robust to adaptive rewriting.
  Evidence: The paper reports that recursive paraphrasing attacks can break watermarking while maintaining text quality.

**Relevance to thesis**: This weakens any overbroad claim that detection defenses are uniformly brittle, because watermarking is promising under cooperative generation. But it also shows watermarking is not a clean retrofit for existing polluted web text.
**Beat affected**: 1
**Suggested handling**: Describe watermarking as a prospective, cooperative provenance mechanism rather than a general solution to current web pollution. Pair it with the attack paper to show its limits under rewriting.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Do observed quality pathologies in web corpora imply that web data is already inferior to curated corpora for pretraining?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: Major web corpora contain serious quality and representational problems.
  Evidence: The C4 audit finds machine-generated text, benchmark contamination, social biases, and blocklist filtering that disproportionately excludes minority voices.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Those problems do not prevent filtered web-only corpora from being highly competitive.
  Evidence: RefinedWeb shows properly filtered and deduplicated web data alone can significantly outperform curated high-quality corpora.

**Relevance to thesis**: This narrows Beat 2: raw-web pathologies are real, but they do not by themselves prove measurable degradation of the usable training distribution after modern filtering.
**Beat affected**: 2
**Suggested handling**: Distinguish sharply between raw-web audits and post-filter training performance. Argue that pathology evidence motivates caution, but not the stronger claim that current filtered web corpora are already broadly degraded. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Can LLM-simulated human feedback stand in for real human preferences?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: Simulated human feedback is a practical substitute for human labels in alignment research.
  Evidence: Claims LLM-simulated feedback is 50x cheaper and shows high agreement with human preferences.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Real human preferences are heterogeneous and socially structured in ways current tuning fails to capture.
  Evidence: Shows demographic opinion misalignment and systematic distributional bias after instruct-tuning.

**Relevance to thesis**: This tension matters because AlpacaFarm-like simulation is real counterevidence for low-cost feedback pipelines, but its evidence base is much narrower than the social-pluralism problem our thesis emphasizes.
**Beat affected**: 2
**Suggested handling**: Acknowledge simulated feedback as useful for method iteration, but note that agreement on simple instruction tasks is not evidence that it captures pluralistic social preferences. Mention AlpacaFarm's single-turn and limited-human-validation scope. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Does rising AI-generated content in major web sources prove current pretraining-quality decline?

**Paper A**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: A carefully filtered web corpus can still improve LLM quality relative to other open pretraining datasets.
  Evidence: FineWeb reports better-performing LLMs from filtered Common Crawl-scale data.

**Paper B**: The Rise of AI-Generated Content in Wikipedia
  Claim: AI-generated content in recently created Wikipedia pages has markedly increased, with at least 5% of new pages detected as AI-generated at a 1% false positive threshold.
  Evidence: The study measures post-GPT-3.5 growth of AI-generated material in a major knowledge source.

**Relevance to thesis**: This weakens any inference from 'contamination is rising in important sources' to 'usable web pretraining quality is already declining overall.'
**Beat affected**: 1
**Suggested handling**: Use the Wikipedia paper as evidence that contamination pressure is real and increasing, but explicitly avoid overclaiming that this already causes net pretraining decline across filtered multi-source corpora. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Do social-data interventions generalize across the full space of social reasoning tasks?

**Paper A**: CoMMET: To What Extent Can LLMs Perform Theory of Mind Tasks?
  Claim: LLMs retain major weaknesses on harder forms of Theory of Mind even if some simpler social tasks are handled well.
  Evidence: Models performed well on emotion and desire tasks but struggled with complex multi-state reasoning and moral reasoning in multimodal settings.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Targeted training can significantly improve social reasoning robustness.
  Evidence: Hard social-reasoning training via RLVF produced significant gains in social reasoning and robustness.

**Relevance to thesis**: This narrows the thesis: positive data-composition results may be real but still fail to cover multimodal, moral, or higher-order multi-state social reasoning.
**Beat affected**: 2
**Suggested handling**: Bound claims carefully to the evaluated task family. Note that improvements on text-based or adversarial social datasets do not yet establish broad social competence across multimodal and moral ToM benchmarks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: For alignment, are curated demonstrations enough, or do preference-optimization methods still add essential value?

**Paper A**: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
  Claim: Preference optimization remains a strong route to alignment even without RL machinery.
  Evidence: DPO trains directly from human preference data with a simple cross-entropy objective and matches or exceeds RLHF.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: Carefully curated supervised data alone can be enough for competitive alignment.
  Evidence: LIMA reports competitive performance from fine-tuning on only 1,000 curated examples and explicitly omits RLHF.

**Relevance to thesis**: This is central to the curation-vs-RLHF framing. If LIMA is right, the scarce resource may be high-quality human demonstrations; if DPO is right, human preference comparisons still matter, but complex RLHF may not.
**Beat affected**: 2
**Suggested handling**: Present curation and preference optimization as rival but partly compatible routes. Avoid claiming that RLHF-style preference learning is always necessary; instead say the literature disagrees on whether extra preference optimization is needed once demonstrations are high quality. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — methodological_tension

**Question**: Can scalable ranking/proxy methods recover alignment as well as richer human-data pipelines?

**Paper A**: RRHF: Rank Responses to Align Language Models with Human Feedback without tears
  Claim: Simple ranking-based preference optimization can achieve RLHF-level alignment.
  Evidence: RRHF reports performance comparable to PPO by ranking sampled responses using log conditional probabilities, while being simpler to train and scale.

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: Alignment outcomes remain highly sensitive to the construction of human data and reward targets.
  Evidence: OpenAssistant notes its RLHF models did not show uniform improvement over SFT and suggests reward-model training data mismatch as an explanation.

**Relevance to thesis**: This tension cautions against telling a one-variable story. Some papers imply optimization is the main issue; others imply human data provenance and pairing choices determine whether preference learning helps at all.
**Beat affected**: N/A
**Suggested handling**: Write that the field disagrees on whether alignment gains come mainly from better objectives or better human data. Use RRHF as real counterevidence to any 'human-data-only' story, but note OpenAssistant's evidence that data construction can dominate method State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Are systematic filtering and deduplication sufficient to resolve contamination concerns in web corpora?

**Paper A**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: Systematic filtering and deduplication at Common Crawl scale can produce a better pretraining corpus.
  Evidence: FineWeb attributes stronger LLM performance to large-scale filtering and dedup across 96 crawl snapshots.

**Paper B**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: Even a prominent cleaned web corpus still contains machine-generated text and benchmark contamination, and cleaning choices can suppress minority voices.
  Evidence: The C4 audit finds both residual contamination and social skew introduced by filtering.

**Relevance to thesis**: This is a scope limiter on filtered-web optimism: better benchmark performance does not imply that contamination or documentation problems have been solved.
**Beat affected**: 1
**Suggested handling**: Acknowledge FineWeb as evidence that filtering can materially improve utility, but pair it with C4 to argue that documentation and auditing remain necessary because filtering can hide tradeoffs. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — implicit_tension

**Question**: Has large-scale web pollution already been demonstrated, or do detection limits still block that inference?

**Paper A**: The Dead Internet Theory: Investigating the Rise of AI-Generated Content and Bot
  Claim: The internet is being fundamentally undermined by growing AI-generated content and bot dominance, especially since 2016-2017.
  Evidence: The paper frames current cyberspace as increasingly dominated by AI-generated content and bots.

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Current detection methods are too condition-dependent to support universal inferences about synthetic text prevalence.
  Evidence: The survey emphasizes that detectability varies by model, domain, and method, and that no single approach is universally reliable.

**Relevance to thesis**: This supports our caution that rising pollution is plausible but not yet proven at true web scale. Sweeping prevalence claims can outrun the reliability of available detection methods.
**Beat affected**: 1
**Suggested handling**: Treat broad 'dead internet' style claims as motivation or hypothesis, not as settled evidence. Contrast them with the survey literature on detection limits and reserve stronger language for scoped domains.

---

## C6: 🟡 MODERATE — implicit_tension

**Question**: Is 'data quality engineering' a sufficient answer to contamination and authenticity concerns?

**Paper A**: Yi: Open Foundation Models by 01.AI
  Claim: Model performance is primarily attributable to data quality engineering; smaller models on higher-quality data can outperform larger models on lower-quality data.
  Evidence: Yi attributes its gains mainly to data-quality work rather than architecture.

**Paper B**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: Web-corpus cleaning pipelines can still leave contamination and impose representational costs, including disproportionate exclusion of minority voices.
  Evidence: The C4 audit shows that common filtering decisions affect both corpus integrity and social coverage.

**Relevance to thesis**: This creates a real tension between optimization-for-performance and documentation-for-authenticity. It limits any move from 'quality engineering works' to 'contamination problems are solved.'
**Beat affected**: 1
**Suggested handling**: Define 'quality' carefully in writing: benchmark and scaling gains should be discussed separately from provenance, leakage, and representation. Cite Yi for utility and C4 for why documentation still matters. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Is social reasoning mostly a latent capability that can be unlocked with a very small curated dataset?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: A small, carefully curated fine-tuning set can produce strong aligned behavior, supporting the Superficial Alignment Hypothesis.
  Evidence: A 65B LLaMA fine-tuned on only 1,000 curated examples achieved competitive performance with state-of-the-art models.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: Large pretrained models still show large deficits on social intelligence benchmarks.
  Evidence: GPT-3 was over 30% below humans on social intelligence benchmarks and especially weak on mental-state reasoning.

**Relevance to thesis**: This undermines any easy inference from general alignment success to socially grounded reasoning. If LIMA-style small curation were sufficient in general, the large ToM gap would be less expected.
**Beat affected**: 2
**Suggested handling**: Explicitly separate general chat alignment/helpfulness from social reasoning. Cite LIMA as evidence that small curated data can strongly shape assistant behavior, but note that it does not establish robust ToM or social-grounding competence. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — implicit_tension

**Question**: Can small high-quality instruction tuning reliably surface latent social competence, or are socially grounded tasks unusually resistant?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: Very small, high-quality datasets can suffice for strong post-training behavior.
  Evidence: Only 1,000 carefully curated examples were enough to produce competitive alignment behavior in a 65B model.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Social-competence gains from post-training are fragile and can degrade under variant testing.
  Evidence: Instruction tuning only partially improved false-belief performance, and robustness failed across explicit/implicit and false/true variants; reasoning-oriented fine-tuning worsened some patterns.

**Relevance to thesis**: This tension is important because it suggests that social reasoning is not just another alignment surface. High-quality curation may be sufficient for style/helpfulness but insufficient for robust socially grounded reasoning.
**Beat affected**: 2
**Suggested handling**: Use LIMA as a boundary case, not a proof of sufficiency for social reasoning. Emphasize that socially grounded tasks appear to require more than generic small-set alignment curation. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟢 MINOR — implicit_tension

**Question**: Do synthetic instruction-tuning gains transfer to social reasoning, or is socially grounded data composition qualitatively different?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Self-generated synthetic instruction data can substantially improve general instruction following.
  Evidence: Self-Instruct fine-tuning yielded a 33% absolute improvement on SUPERNI over the original GPT-3.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Generic post-training does not robustly solve social reasoning.
  Evidence: Instruction tuning only partially helped social false-belief tasks, with brittle behavior across benchmark variants.

**Relevance to thesis**: This is a weaker but still useful tension: strong synthetic-data gains on generic instruction benchmarks do not automatically transfer to socially grounded reasoning.
**Beat affected**: 2
**Suggested handling**: Mention briefly that successes from synthetic instruction tuning are mostly on generic task-following benchmarks, so they should not be overextended as evidence that synthetic data is sufficient for social reasoning. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---


## Summary

Total contradictions: 33
Critical (must address): 16

## Thesis Risk Assessments

- The main risk to the thesis is overclaiming. The collapse papers strongly support that indiscriminate or weakly filtered recursive reuse is dangerous, but several priority counterexamples show that curated or verified synthetic data can substitute for fresh human data under stronger conditions: human-preference curation, correction toward the true distribution, or continued anchoring with real data. These counterexamples do not eliminate the thesis, because they rely on idealized rewards, correction oracles, or persistent access to real data, and several are theoretical rather than web-scale empirical demonstrations. Still, they do undermine any absolute statement that synthetic reuse necessarily causes collapse or that fresh human data is always required. The defensible thesis is narrower: authenticity matters most when synthetic data is reused without strong verification, curation, or continued grounding to real data.
- The strongest tensions mostly force tighter scoping rather than overturning the thesis. The biggest risk is overclaiming either side: some papers imply retrieval or narrow-domain classifiers can detect pollution effectively, while others show those defenses fail under adaptive paraphrasing or polluted reference corpora. The defensible position is that detectable pollution exists in scoped settings, but reliable web-scale detection remains unproven and reactive filtering remains fragile unless trusted provenance or trusted corpora are available.
- The main risk to the thesis is overclaiming. The selected papers support that some live-web domains are changing in undesirable ways over time and that AI-generated content is rising in at least one important source, but they do not jointly prove web-wide measurable degradation of the usable pretraining distribution. In parallel, filtered-web papers show that large multi-snapshot web corpora still produce strong models, which pushes against any strong claim that live-web drift has already caused broad downstream degradation. The safest thesis is therefore: measurable temporal drift exists in specific domains, contamination risk is rising, and reactive filtering is important but not a substitute for direct web-scale measurement; however, web-wide degradation is not yet empirically established.
- Moderate. The strongest papers here substantially undermine any simplified contamination-to-quality-decline story. RefinedWeb, FineWeb, and Yi show that filtered or quality-engineered web corpora can still deliver strong model performance, so we should not imply that rising AI contamination has already made web pretraining broadly inferior. However, C4 documentation and the Wikipedia/retrieval-collapse papers preserve the core conditional thesis: contamination is rising, filtering is not a complete solution, and performance success does not eliminate authenticity, leakage, or representational concerns. Our line_1 claim remains defensible only if framed as conditional, task-specific, and not yet proven at web scale.
- The main risk is overgeneralization. The benchmark papers do not show that social reasoning is impossible, but they do show that generic scale and generic post-training leave large, brittle gaps. The data-composition success papers show that curation and targeted training can matter a great deal, yet most of those successes are either general alignment results or are limited to particular social task families. The safest thesis claim is therefore conditional: data composition matters for social reasoning, but gains depend strongly on whether the post-training data is socially targeted, behaviorally diverse, and evaluated for robustness rather than surface benchmark lift.

## Unresolved Tensions

- How realistic are the verifier assumptions in the pro-curation papers (well-specified human reward, reliable correction function, or continued access to uncontaminated real data)?
- Do the positive theoretical results survive finite-sample, misspecified-reward, or web-scale contamination settings, or are they confined to stylized regimes?
- Is the relevant distinction replacement vs augmentation, or curation strength vs no curation? Existing papers support both framings.
- There is still no decisive web-scale empirical reconciliation showing when curated synthetic reuse matches fresh human data over many generations in realistic pretraining pipelines.
- Whether retrieval-based defenses remain useful once their reference corpus is itself contaminated by synthetic web content.
- Whether high-F1, domain-specific detectors in news or education transfer to open-web prevalence estimation at low false-positive rates.
- Whether watermarking can become a practical large-scale provenance defense given non-cooperative generators and paraphrase-based watermark removal.
- No paper here directly measures synthetic-content prevalence and quality drift across broad live-web snapshots with a consistent detector and downstream benchmark over time.
- Filtered-web success is not clean counterevidence to drift, because better filtering may mask worsening raw-web quality rather than show that no degradation exists.
- Domain-specific longitudinal studies (privacy policies, Wikipedia) may be important leading indicators, but current evidence does not show that their trends generalize to the whole web.
- Intrinsic diversity metrics and downstream pretraining performance are answering different questions; the field still lacks a shared temporal measurement framework connecting the two.
- No paper in this set directly shows that current web-scale AI contamination has already caused net pretraining-quality decline in modern filtered corpora; the strongest harm evidence is from live retrieval or source-specific contamination studies.
- Filtered-web success papers evaluate downstream model performance, while corpus-documentation papers evaluate provenance, leakage, and representational integrity; these are overlapping but non-identical notions of 'quality.'
- Rising contamination in salient sources like Wikipedia may or may not materially affect broad Common Crawl-derived corpora after deduplication and filtering; the mapping from source-level pollution to corpus-level pretraining harm remains unresolved.
- Whether Social-R1-style gains reflect genuinely improved social reasoning or narrower benchmark-specific adaptation remains unresolved against the robustness failures reported in Traces of Social Competence.
- Whether small curated datasets in the style of LIMA can unlock socially grounded reasoning, or mainly improve style/helpfulness while leaving ToM gaps intact, is still unproven.
- Whether text-only social-data interventions transfer to multimodal, moral, and multi-state social reasoning remains unresolved by the gap between Social-R1 and CoMMET.