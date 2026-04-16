# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## Executive Summary

1. Is web pollution detectable? (pollution scale vs detection limits) → Is AI-generated web pollution practically detectable at scale, or are current detectors too brittle?
   Handling: Separate detector success in cooperative or provider-controlled settings from adversarial open-web conditions. Do not write as if current detection tooling has solved contamination measurement. Distinguish brittle classifier-style detection from retrieval or provenance-based defenses. If a paper is a scope-limited prevalence study, treat it as partial evidence, not direct proof of web-scale contamination. This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central.
2. When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) → Can curated synthetic data prevent recursive collapse well enough to substitute for fresh human data?
   Handling: State explicitly that the collapse result applies to indiscriminate or weakly controlled recursive reuse. Separate 'distribution preservation' from 'preference optimization,' and note that the pro-curation result is theoretical and conditional on effective user curation. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.
3. How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) → Has measurable live-web drift already made web-only pretraining unreliable, or is the evidence still partial?
   Handling: Narrow the claim to rising contamination risk plus incomplete measurement. Treat filtered-web success as a scope limiter, not as proof that contamination is harmless. Look for both support and limitations: metric papers, longitudinal corpora, and filtered-web results should jointly test how far Beat 2 can really go. This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
4. Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) → Does high agreement between simulated and human feedback mean human preference collection can be safely replaced?
   Handling: Distinguish aggregate annotation agreement from subgroup-faithful social grounding. Emphasize that human data remains valuable when the goal is not just cheap preference supervision, but coverage of real population diversity and contested norms. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
5. Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? → Does strong performance from filtered web-only pretraining undercut a simple claim that AI contamination in web data necessarily causes quality decline?
   Handling: State the thesis conditionally: unfiltered or search-mediated web pollution can degrade downstream information quality, but filtered, deduplicated pretraining corpora can still produce strong models. Separate pretraining-corpus quality from retrieval-exposure dynamics. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
6. Does data composition matter for social reasoning? (benchmarks vs ablation) → Do higher-complexity instruction datasets strengthen social reasoning, or can reasoning-oriented fine-tuning actually worsen Theory-of-Mind behavior?
   Handling: Explicitly separate 'complex task performance' from 'social reasoning quality.' Cite Traces of Social Competence as evidence that socially grounded outcomes can diverge from generic reasoning gains, motivating a social-specific loss or evaluation term such as L_auth rather than generic complexity-based data design. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

## Argument-Line Coverage

- Fine-tuning / Post-training (count=9)
  Focuses: Does data composition matter for social reasoning? (benchmarks vs ablation) | How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? | When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) | Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?
  Representative: Do higher-complexity instruction datasets strengthen social reasoning, or can reasoning-oriented fine-tuning actually worsen Theory-of-Mind behavior?
- Cross-line (count=10)
  Focuses: Is web pollution detectable? (pollution scale vs detection limits) | How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) | Does data composition matter for social reasoning? (benchmarks vs ablation) | When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
  Representative: Is AI-generated web pollution practically detectable at scale, or are current detectors too brittle?
- Adversarial / Competing Mechanisms (count=18)
  Focuses: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) | Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) | Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? | Does inference-time scaling reduce the importance of training data quality for social reasoning?
  Representative: Can curated synthetic data prevent recursive collapse well enough to substitute for fresh human data?

## Focus Coverage

- [B, C] Is web pollution detectable? (pollution scale vs detection limits) (count=2)
  Representative: Is AI-generated web pollution practically detectable at scale, or are current detectors too brittle?
- [A, E] When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) (count=6)
  Representative: Can curated synthetic data prevent recursive collapse well enough to substitute for fresh human data?
- [D, H] How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) (count=2)
  Representative: Has measurable live-web drift already made web-only pretraining unreliable, or is the evidence still partial?
- [E, F] Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) (count=6)
  Representative: Does high agreement between simulated and human feedback mean human preference collection can be safely replaced?
- [B, E, H] Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? (count=5)
  Representative: Does strong performance from filtered web-only pretraining undercut a simple claim that AI contamination in web data necessarily causes quality decline?
- [I, J] Does data composition matter for social reasoning? (benchmarks vs ablation) (count=6)
  Representative: Do higher-complexity instruction datasets strengthen social reasoning, or can reasoning-oriented fine-tuning actually worsen Theory-of-Mind behavior?
- [F, J] How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? (count=4)
  Representative: Is alignment fundamentally human-in-the-loop, or can AI systems supervise alignment with only minimal direct human labeling?
- [K] Does inference-time scaling reduce the importance of training data quality for social reasoning? (count=6)
  Representative: Even if inference-time scaling improves benchmark Theory-of-Mind, does it solve the harder socially grounded failures that matter in practice?

---

## Structural Limitations

- All categories are populated, but the corpus is still asymmetric: F=19 while K=8; treat this as uneven evidence density rather than balanced coverage.
- No paper in the current corpus directly provides a broad post-2022 web-scale contamination audit; Beat 2 remains a multi-paper inference chain rather than a single-study demonstration.
- The corpus contains strong AI-feedback and self-alignment success papers, but it does not directly show those methods failing on social-reasoning tasks; that scope boundary is still hypothetical.
- Category K papers must be treated as adversarial scope evidence; do not write as if data provenance is the only plausible mechanism for social-reasoning gains.
- Contradiction handling should distinguish evidence-backed scope limits from proposed thesis-saving explanations; when the corpus lacks a direct bridge, say so explicitly.

## Fine-tuning / Post-training

### C3: 🔴 CRITICAL — scope_disagreement

**Source focus**: Does data composition matter for social reasoning? (benchmarks vs ablation)
**Question**: Do higher-complexity instruction datasets strengthen social reasoning, or can reasoning-oriented fine-tuning actually worsen Theory-of-Mind behavior?

**Paper A**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: LLM-rewritten instructions via Evol-Instruct produce higher-complexity training data that yields a model preferred over ChatGPT on complex tasks.
  Evidence: WizardLM argues that "higher-complexity training data" from Evol-Instruct improves performance on "complex tasks," implying composition and difficulty of post-training data are key levers.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Instruction tuning partially improves Theory of Mind in LLMs but reasoning-oriented fine-tuning amplifies problematic response patterns.
  Evidence: Traces of Social Competence reports that instruction tuning only "partially helps ToM" and that "reasoning-oriented fine-tuning amplifies problematic response patterns" on False Belief variants.

**Relevance to thesis**: This is one of the strongest scope limiters. WizardLM suggests more sophisticated data composition helps hard tasks, but Traces of Social Competence says the same broad intuition may break for social reasoning: reasoning-focused tuning can make ToM behavior worse.
**Beat affected**: 6
**Suggested handling**: Explicitly separate 'complex task performance' from 'social reasoning quality.' Cite Traces of Social Competence as evidence that socially grounded outcomes can diverge from generic reasoning gains, motivating a social-specific loss or evaluation term such as L_auth rather than generic complexity-based data design. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C4: 🔴 CRITICAL — methodological_tension

**Source focus**: How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision?
**Question**: Is alignment fundamentally human-in-the-loop, or can AI systems supervise alignment with only minimal direct human labeling?

**Paper A**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: The survey argues that reinforcement learning is fundamentally a human-in-the-loop paradigm and that human-centric approaches are key to successful RL.
  Evidence: Key claim explicitly frames RL as 'fundamentally a human-in-the-loop paradigm' and stresses human-centric requirements, implying that durable alignment should keep humans central.

**Paper B**: Constitutional AI: Harmlessness from AI Feedback
  Claim: Constitutional AI claims a harmless, non-evasive assistant can be trained using only AI-generated feedback guided by a constitution, without human labels for harmful outputs.
  Evidence: Key claim states 'without human labels for harmful outputs,' and the abstract says the system trains through self-improvement using AI feedback rather than direct human labeling.

**Relevance to thesis**: This is a framework-level disagreement about how far human-authored supervision can be removed. Constitutional AI suggests that, once principles are specified, AI feedback can replace much direct human labeling; the survey warns that alignment remains fundamentally human-centered.
**Beat affected**: 4
**Suggested handling**: Separate two roles of humans: humans may not need to label every training example, but they still author constitutions, define acceptable tradeoffs, and evaluate failures. That preserves the survey's human-centric concern while acknowledging AI-feedback scalability. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C5: 🔴 CRITICAL — methodological_tension

**Source focus**: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
**Question**: Is 'verified synthetic data' a realistic condition, or do mitigation schemes rely on provenance information that is often unavailable?

**Paper A**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: User-curated synthetic data can prevent collapse and optimize human preferences.
  Evidence: The result depends on successful user curation, which implicitly requires knowing enough about sample quality and origin to curate the self-consuming loop.

**Paper B**: Learning by Surprise: Surplexity for Mitigating Model Collapse in Generative AI
  Claim: Model collapse can be characterized from next-token distributions because existing mitigation methods often assume reliable knowledge of whether data are human-authored or AI-generated, which is often unavailable.
  Evidence: The paper explicitly names provenance knowledge as a weak point in current mitigation approaches and proposes a collapse signal that does not require origin labels.

**Relevance to thesis**: This is a major deployment-level tension: pro-verification results may only hold when provenance is observable, while real-world web-scale retraining often lacks trustworthy origin labels.
**Beat affected**: 5
**Suggested handling**: Acknowledge that verified-synthetic substitution is credible mainly in closed pipelines with platform-level provenance or human-in-the-loop curation. Avoid assuming detector-based provenance is sufficient in open data collection. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

### C4: 🔴 CRITICAL — methodological_tension

**Source focus**: Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?
**Question**: Do documentation findings about hidden contamination and biased filtering in web corpora challenge the interpretation of filtered-web success as evidence against contamination harms?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: C4 contains unexpected content, including machine-generated text and benchmark evaluation data, and its blocklist filtering disproportionately removes text from certain communities.
  Evidence: The key claim identifies both hidden contamination and representational distortion from filtering choices in a major web corpus.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Filtered and deduplicated web data alone can outperform curated corpora in LM pretraining.
  Evidence: RefinedWeb's central result is that web-only data, once refined, can surpass curated mixtures like The Pile.

**Relevance to thesis**: This is not a direct contradiction on outcomes, but a serious methodological tension. RefinedWeb shows filtered web can work very well; the C4 documentation paper warns that what counts as 'filtered' may hide machine-generated artifacts, benchmark leakage, and social skew. That means filtered-web success does not erase authenticity concerns.
**Beat affected**: 4
**Suggested handling**: Use this as an honesty layer: filtered-web wins should be presented alongside documentation requirements about residual contamination and filtering bias. Emphasize that better benchmark performance does not prove absence of contamination or fair representation. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### C1: 🔴 CRITICAL — competing_mechanism

**Source focus**: How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision?
**Question**: Can open alignment reach top-tier chat performance without collecting new human-authored preference data?

**Paper A**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: OpenAssistant argues that a large-scale, crowd-sourced, multilingual human-generated conversation corpus can democratize LLM alignment research by providing open high-quality feedback data.
  Evidence: Key claim explicitly centers a human-generated conversation corpus. The abstract frames alignment progress around SFT and RLHF and presents the dataset as the open data substrate for such human-feedback-based alignment.

**Paper B**: Zephyr: Direct Distillation of LM Alignment
  Claim: Zephyr claims that distilled direct preference optimization with AI feedback can align a 7B model strongly enough to surpass Llama2-Chat-70B on MT-Bench without human annotation.
  Evidence: Key claim states that Zephyr-7B surpasses Llama2-Chat-70B on MT-Bench using AI feedback and 'without human annotation,' offering a concrete alternative to human-authored alignment data.

**Relevance to thesis**: This is a direct pressure test on the need for human-authored supervision. If AI-feedback distillation can already beat strong chat baselines, then human-authored supervision may be less necessary for mainstream instruction-following than OpenAssistant-style dataset building suggests.
**Beat affected**: 7
**Suggested handling**: Narrow the human-supervision claim: human-authored data may be most necessary for bootstrapping teachers, multilingual coverage, and auditing, while marginal alignment improvements can come from AI-generated preferences. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C2: 🟡 MODERATE — scope_disagreement

**Source focus**: Does data composition matter for social reasoning? (benchmarks vs ablation)
**Question**: Does synthetic/self-generated instruction data improve the specific capability of social reasoning, or only instruction following more broadly?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Language models can be aligned to follow instructions using self-generated instruction data, reducing reliance on costly human annotations.
  Evidence: Self-Instruct claims models can be aligned using "self-generated instruction data," demonstrating that dataset construction choices can substitute for more expensive human-labeled tuning data.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on tasks measuring intent, reaction, and mental state inference.
  Evidence: Neural Theory-of-Mind finds substantial failures on "intent, reaction, and mental state inference" tasks, which are more socially grounded than generic instruction following.

**Relevance to thesis**: This is a real but weaker tension: Self-Instruct supports the general importance of data composition, while Neural Theory-of-Mind says social reasoning remains weak on dedicated tests. The disagreement is about transfer scope, not whether data matters at all.
**Beat affected**: 6
**Suggested handling**: Frame Self-Instruct as indirect support only. Note that synthetic instruction data may improve obedience/helpfulness without establishing social cognition unless evaluated on ToM or related benchmarks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C2: 🟡 MODERATE — methodological_tension

**Source focus**: How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision?
**Question**: Is crowd-sourced human feedback the right default for alignment research once simulated feedback becomes cheap and high-agreement?

**Paper A**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: OpenAssistant presents large-scale crowd-sourced human conversations as the route to democratizing alignment research with open, high-quality human feedback data.
  Evidence: The title and key claim emphasize crowd-sourced, human-generated conversations. The abstract motivates open alignment through accessible human feedback resources.

**Paper B**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: AlpacaFarm claims that LLM-simulated human feedback is about 50 times cheaper than crowdworkers while maintaining high agreement with humans, enabling low-cost feedback-learning research.
  Evidence: Key claim explicitly states '50x cheaper than crowdworkers' and 'maintaining high agreement with humans,' which challenges the cost-benefit case for collecting large new human preference datasets in many experimental settings.

**Relevance to thesis**: If simulated feedback approximates human judgments at much lower cost, then the practical reliance on human-authored supervision may drop sharply even if human data remains the gold standard.
**Beat affected**: 6
**Suggested handling**: Treat human feedback as calibration and validation data, while simulated feedback serves as a research and iteration multiplier. Distinguish scientific convenience from normative legitimacy. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C5: 🟡 MODERATE — methodological_tension

**Source focus**: Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?
**Question**: Does evidence that filtering improves web corpora conflict with evidence that filtering itself can create representational and contamination problems?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: Large webtext corpora can include machine-generated text and benchmark data, while blocklist filtering disproportionately removes some communities' content.
  Evidence: The case study on C4 documents both contamination and uneven social effects from the filtering process itself.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb improves LLM performance over other open datasets, especially when filtered for educational content.
  Evidence: The key claim explicitly attributes stronger results to web-scale filtering and selection, with educational-content filtering producing the best gains.

**Relevance to thesis**: This tension narrows the scope of any simple contamination story. FineWeb implies filtering can turn web data into a superior training resource; the C4 documentation paper shows that filtration choices may also silently reshape whose language remains and what contamination persists.
**Beat affected**: 4
**Suggested handling**: Describe filtering as a double-edged mechanism: it can improve average model quality while introducing fairness and documentation concerns. Recommend provenance reports and bias audits alongside performance claims. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### C4: 🟡 MODERATE — implicit_tension

**Source focus**: Does data composition matter for social reasoning? (benchmarks vs ablation)
**Question**: Is better data selection enough for social reasoning, or are social failures robust even when post-training data quality is improved?

**Paper A**: From Quantity to Quality: Boosting LLM Performance with Self-Guided Data Selecti
  Claim: Self-guided data selection for instruction tuning improves LLM performance by prioritizing data quality over quantity.
  Evidence: From Quantity to Quality claims instruction tuning improves when models prioritize "data quality over quantity," directly supporting a composition-sensitive view of post-training.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Instruction tuning partially improves Theory of Mind in LLMs but reasoning-oriented fine-tuning amplifies problematic response patterns.
  Evidence: The social-benchmark paper shows only partial ToM gains and notes that some fine-tuning regimes "amplif[y] problematic response patterns," limiting how far generic quality-selection results can be extrapolated.

**Relevance to thesis**: This tension matters because it narrows the causal claim. Data selection clearly matters for broad instruction tuning, but the social-reasoning evidence suggests that not all 'better' data compositions improve socially grounded inference.
**Beat affected**: 6
**Suggested handling**: Treat data quality as necessary but not sufficient. Add a scope note that social reasoning may require socially targeted data composition rather than generic quality filtering alone. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## Cross-line

### H1: 🔴 CRITICAL — direct_contradiction

**Source focus**: Is web pollution detectable? (pollution scale vs detection limits)
**Question**: Is AI-generated web pollution practically detectable at scale, or are current detectors too brittle?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Paraphrasing AI-generated text with an 11B parameter model (DIPPER) evades multiple detectors, but retrieval-based defense can restore robustness.
  Evidence: Fallback evidence via key claim and keyword hits: detect, detection, watermark, retrieval-based, effective defense, robust.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content causes Retrieval Collapse, where 67% pool contamination leads to over 80% exposure contamination in search results while masking accuracy degradation.
  Evidence: Fallback evidence via key claim and keyword hits: adversarial.

**Relevance to thesis**: This determines whether Beat 2 can claim contamination is observable in practice or only a plausible risk. If detectors are brittle, the argument must rely on measured prevalence and provenance-limited defenses rather than simple detectability claims.
**Beat affected**: 2
**Suggested handling**: Separate detector success in cooperative or provider-controlled settings from adversarial open-web conditions. Do not write as if current detection tooling has solved contamination measurement. Distinguish brittle classifier-style detection from retrieval or provenance-based defenses. If a paper is a scope-limited prevalence study, treat it as partial evidence, not direct proof of web-scale contamination. This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central.

---

### H1: 🔴 CRITICAL — scope_disagreement

**Source focus**: How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement)
**Question**: Has measurable live-web drift already made web-only pretraining unreliable, or is the evidence still partial?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: Over 5% of newly created English Wikipedia articles are flagged as AI-generated, and these articles are typically of lower quality and more self-promotional.
  Evidence: Fallback evidence via key claim and keyword hits: lower bounds, ai-generated content.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora like The Pile.
  Evidence: Fallback evidence via key claim and keyword hits: filtered, deduplicated, outperform, web data alone, properly filtered.

**Relevance to thesis**: This is the main limiter on Beat 2. Measured contamination growth does not automatically prove that web-only corpora are already unusable if filtered-web training papers still perform strongly.
**Beat affected**: 2
**Suggested handling**: Narrow the claim to rising contamination risk plus incomplete measurement. Treat filtered-web success as a scope limiter, not as proof that contamination is harmless. Look for both support and limitations: metric papers, longitudinal corpora, and filtered-web results should jointly test how far Beat 2 can really go. This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### H2: 🔴 CRITICAL — direct_contradiction

**Source focus**: Is web pollution detectable? (pollution scale vs detection limits)
**Question**: Is AI-generated web pollution practically detectable at scale, or are current detectors too brittle?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Paraphrasing AI-generated text with an 11B parameter model (DIPPER) evades multiple detectors, but retrieval-based defense can restore robustness.
  Evidence: Fallback evidence via key claim and keyword hits: detect, detection, watermark, retrieval-based, effective defense, robust.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: 67% pool contamination with AI-generated content leads to over 80% exposure contamination in retrieval systems, creating homogenized yet deceptively healthy search results.
  Evidence: Fallback evidence via key claim and keyword hits: adversarial.

**Relevance to thesis**: This determines whether Beat 2 can claim contamination is observable in practice or only a plausible risk. If detectors are brittle, the argument must rely on measured prevalence and provenance-limited defenses rather than simple detectability claims.
**Beat affected**: 2
**Suggested handling**: Separate detector success in cooperative or provider-controlled settings from adversarial open-web conditions. Do not write as if current detection tooling has solved contamination measurement. Distinguish brittle classifier-style detection from retrieval or provenance-based defenses. If a paper is a scope-limited prevalence study, treat it as partial evidence, not direct proof of web-scale contamination. This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central.

---

### H2: 🔴 CRITICAL — scope_disagreement

**Source focus**: How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement)
**Question**: Has measurable live-web drift already made web-only pretraining unreliable, or is the evidence still partial?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: Over 5% of newly created English Wikipedia articles are flagged as AI-generated, and these articles are typically of lower quality and more self-promotional.
  Evidence: Fallback evidence via key claim and keyword hits: lower bounds, ai-generated content.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, a 15-trillion token dataset from 96 Common Crawl snapshots, produces better-performing LLMs than other open pretraining datasets, especially when filtered for educational content.
  Evidence: Fallback evidence via key claim and keyword hits: filtered, outperform, documented.

**Relevance to thesis**: This is the main limiter on Beat 2. Measured contamination growth does not automatically prove that web-only corpora are already unusable if filtered-web training papers still perform strongly.
**Beat affected**: 2
**Suggested handling**: Narrow the claim to rising contamination risk plus incomplete measurement. Treat filtered-web success as a scope limiter, not as proof that contamination is harmless. Look for both support and limitations: metric papers, longitudinal corpora, and filtered-web results should jointly test how far Beat 2 can really go. This pair came from the deterministic fallback, so keep the prose cautious and verify the pair manually before making it central. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### C1: 🔴 CRITICAL — methodological_tension

**Source focus**: Does data composition matter for social reasoning? (benchmarks vs ablation)
**Question**: Do wins from small, curated alignment datasets show improved social reasoning, or only improved generic preference/alignment behavior?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: Fine-tuning a 65B LLM on only 1,000 carefully curated examples without RL achieves performance comparable or preferred to GPT-4 in 43% of cases.
  Evidence: LIMA reports that a model fine-tuned on "only 1,000 carefully curated examples" is "preferred to GPT-4 in 43% of cases," using alignment-style evaluation rather than Theory-of-Mind tests.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on tasks measuring intent, reaction, and mental state inference.
  Evidence: Neural Theory-of-Mind explicitly says GPT-3 "struggl[es] substantially on tasks measuring intent, reaction, and mental state inference," showing poor social reasoning on dedicated benchmarks.

**Relevance to thesis**: This is the clearest benchmark-vs-ablation tension in the set. LIMA is strong evidence that data quality/composition can improve general alignment behavior, but Neural Theory-of-Mind shows that such gains cannot be assumed to transfer to social reasoning. It limits any claim that curated post-training data alone explains socially grounded competence.
**Beat affected**: 6
**Suggested handling**: Use LIMA only as evidence that composition matters for general alignment efficiency. Pair it with an explicit caveat that social reasoning requires separate evaluation, and avoid treating preference wins as proof of Theory-of-Mind improvement. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C3: 🟡 MODERATE — scope_disagreement

**Source focus**: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
**Question**: Can verified synthetic feedback replace fresh human supervision in post-training even if synthetic pretraining data are risky?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive training on model-generated data erodes the original distribution and causes irreversible collapse.
  Evidence: The paper's evidence centers on generative retraining over synthetic outputs, where rare modes and tail behavior disappear over generations.

**Paper B**: Constitutional AI: Harmlessness from AI Feedback
  Claim: A harmless assistant can be trained using only AI-generated feedback guided by a constitution, without human labels for harmful outputs.
  Evidence: The paper empirically demonstrates post-training with AI feedback constrained by explicit principles, showing that human labels are not strictly necessary for this alignment objective.

**Relevance to thesis**: This is a strong pro-verification counterexample: synthetic supervision can substitute for fresh human labels in a narrow, rule-constrained post-training setting, even if open-ended recursive pretraining collapses.
**Beat affected**: 6
**Suggested handling**: Distinguish pretraining distribution learning from post-training alignment. Concede that verified or constitution-guided synthetic feedback can replace some human annotation, while arguing that this does not prove equivalence to fresh human data for preserving world-grounded tail phenomena. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

### C4: 🟡 MODERATE — scope_disagreement

**Source focus**: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
**Question**: Can curated self-generated instruction data substitute for fresh human instruction data in practice?

**Paper A**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Recursively training language models on synthetic text leads to a consistent decline in lexical, syntactic, and semantic diversity across generations.
  Evidence: The paper provides empirical evidence that synthetic recursion reduces diversity, suggesting degradation when model outputs replace human text over time.

**Paper B**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Language models can be aligned to follow instructions using self-generated instruction data, reducing reliance on costly human annotations.
  Evidence: The paper empirically shows that self-generated instruction data can successfully align models, directly claiming substitution for at least part of the human instruction-tuning pipeline.

**Relevance to thesis**: This is a meaningful scope limiter: synthetic data may be poor at preserving broad linguistic diversity, yet still good enough for narrow instruction-following objectives.
**Beat affected**: 6
**Suggested handling**: Frame the disagreement as objective-specific. Synthetic instruction data can substitute for human data in constrained post-training tasks, but that does not imply safe replacement of fresh human data for broad-distribution pretraining or socially grounded rare-case coverage. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

### C4: 🟡 MODERATE — methodological_tension

**Source focus**: Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)
**Question**: Where does human data add value: in large-scale preference optimization or in a tiny, carefully curated instruction set?

**Paper A**: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
  Claim: RLHF can be solved with a simple classification loss by reparameterizing the reward model and directly optimizing preferences.
  Evidence: The paper argues that the core of RLHF can be reduced to direct preference optimization, making preference data the central object and reducing the need for complex RL machinery.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: Fine-tuning a 65B LLM on only 1,000 carefully curated examples without RL achieves performance comparable or preferred to GPT-4 in 43% of cases.
  Evidence: LIMA claims that very small, high-quality human curation can yield strong alignment outcomes without RLHF-style preference optimization.

**Relevance to thesis**: These papers disagree less on outcomes than on where human value lives. DPO implies scalable preference comparisons are the key alignment signal; LIMA implies small amounts of highly authentic, carefully curated human data may matter more than elaborate preference-optimization pipelines.
**Beat affected**: 5
**Suggested handling**: Present this as a methodological tension, not a direct contradiction. Use it to refine the thesis: human data may remain most valuable when it is selective and high-quality, even if expensive large-scale RLHF pipelines are not always necessary. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C5: 🟡 MODERATE — methodological_tension

**Source focus**: Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)
**Question**: Is human feedback best captured by ranking/preference losses, or can minimal curated supervision replace RLHF altogether?

**Paper A**: RRHF: Rank Responses to Align Language Models with Human Feedback without tears
  Claim: RRHF aligns language models with human preferences using ranking loss on log-conditional probabilities, achieving comparable performance to PPO with fewer models and simpler training.
  Evidence: The paper claims RLHF-like gains can be obtained through a simpler ranking-based preference objective, preserving the value of preference data while reducing training complexity.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: A 65B model fine-tuned on 1,000 carefully curated examples without RL can achieve very strong alignment results.
  Evidence: LIMA argues that alignment may largely be a formatting/style problem solvable by small amounts of curated demonstration data rather than preference-ranking pipelines.

**Relevance to thesis**: This tension matters because it changes the thesis target. If RRHF is right, human data remains valuable mainly as ranked preference signal. If LIMA is right, the scarce resource is not preference labels at scale but a tiny amount of exceptionally authentic curated instruction data.
**Beat affected**: 5
**Suggested handling**: Frame this as uncertainty about the form of valuable human data. Human data may remain crucial, but the strongest evidence does not yet settle whether rankings, demonstrations, or conversations are the indispensable component. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C5: 🟡 MODERATE — methodological_tension

**Source focus**: How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision?
**Question**: Are strong alignment gains mostly about scaling synthetic instruction data, or can very small curated datasets already do most of the job?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: LIMA claims that fine-tuning a 65B model on only 1,000 carefully curated examples, without RL, achieves performance comparable to or preferred over GPT-4 in 43% of cases.
  Evidence: Key claim emphasizes extreme data efficiency: only 1,000 curated examples and no RL are said to be enough for strong chat behavior.

**Paper B**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: WizardLM claims that LLM-rewritten instructions via Evol-Instruct create higher-complexity training data that yields a model preferred over ChatGPT on complex tasks.
  Evidence: Key claim explicitly attributes gains to synthetic expansion toward more complex instructions, suggesting that richer synthetic data generation is a major driver of alignment quality.

**Relevance to thesis**: These papers disagree on the main lever for reducing human supervision. LIMA implies a little high-quality human data may suffice; WizardLM implies synthetic scaling and complexity engineering can keep pushing performance.
**Beat affected**: 6
**Suggested handling**: Present this as a conditional split: for strong base models, tiny curated sets may unlock latent abilities, but synthetic complexity expansion may matter more for broader coverage and harder tasks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## Adversarial / Competing Mechanisms

### C1: 🔴 CRITICAL — scope_disagreement

**Source focus**: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
**Question**: Can curated synthetic data prevent recursive collapse well enough to substitute for fresh human data?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated content in training causes irreversible model collapse, with tails of the original data distribution disappearing.
  Evidence: The paper reports mixed empirical evidence across generative settings that recursive training on synthetic outputs leads to irreversible degradation and loss of rare modes, framing fresh human data as necessary to preserve the original distribution.

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: User-curated synthetic data in self-consuming generative models can provably optimize human preferences and prevent model collapse.
  Evidence: The paper gives a theoretical result that, under user curation, self-consuming loops need not collapse and can instead move the model toward human-preference optima.

**Relevance to thesis**: This is the central tension for the focus question: collapse is not presented as inevitable if synthetic data are curated, so any thesis claiming fresh human data are always required would be overstated.
**Beat affected**: 7
**Suggested handling**: State explicitly that the collapse result applies to indiscriminate or weakly controlled recursive reuse. Separate 'distribution preservation' from 'preference optimization,' and note that the pro-curation result is theoretical and conditional on effective user curation. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

### C2: 🔴 CRITICAL — scope_disagreement

**Source focus**: Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)
**Question**: Does high agreement between simulated and human feedback mean human preference collection can be safely replaced?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: LLM-simulated human feedback is 50x cheaper than crowdworkers while maintaining high agreement with humans, enabling low-cost research on learning from feedback.
  Evidence: The abstract claims simulated feedback preserves substantial agreement with human judgments at much lower cost, suggesting synthetic raters are a viable stand-in for human evaluators.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Language models are substantially misaligned with different US demographic groups' opinions.
  Evidence: The paper finds broad disagreement between model outputs and human subgroup opinions even after steering, indicating that 'agreement with humans' in aggregate can hide failures to capture plural or minority preferences.

**Relevance to thesis**: This is an important scope limiter. Simulated feedback may be good enough for aggregate benchmark research, yet still fail precisely where authentic human data matters most: representing heterogeneous social preferences rather than a single averaged evaluator.
**Beat affected**: 7
**Suggested handling**: Distinguish aggregate annotation agreement from subgroup-faithful social grounding. Emphasize that human data remains valuable when the goal is not just cheap preference supervision, but coverage of real population diversity and contested norms. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C1: 🔴 CRITICAL — scope_disagreement

**Source focus**: Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?
**Question**: Does strong performance from filtered web-only pretraining undercut a simple claim that AI contamination in web data necessarily causes quality decline?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content causes Retrieval Collapse: when 67% of the retrieval pool is contaminated, over 80% of retrieved exposure becomes contaminated, while degradation is partly masked.
  Evidence: The paper's key claim reports a quantitative amplification effect from 67% pool contamination to more than 80% exposure contamination in search/RAG results, with homogenized but deceptively healthy outputs.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora such as The Pile.
  Evidence: The key claim explicitly says web data only, once filtered and deduplicated, outperforms curated-corpus baselines rather than showing inevitable decline.

**Relevance to thesis**: This is a major scope limiter against any contamination-equals-decline narrative. One paper shows severe harm in live retrieval ecosystems; the other shows that heavily refined web corpora can be highly effective for pretraining. The tension implies that filtration regime and task setting matter as much as contamination presence.
**Beat affected**: 7
**Suggested handling**: State the thesis conditionally: unfiltered or search-mediated web pollution can degrade downstream information quality, but filtered, deduplicated pretraining corpora can still produce strong models. Separate pretraining-corpus quality from retrieval-exposure dynamics. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### C4: 🟡 MODERATE — scope_disagreement

**Source focus**: Does inference-time scaling reduce the importance of training data quality for social reasoning?
**Question**: Even if inference-time scaling improves benchmark Theory-of-Mind, does it solve the harder socially grounded failures that matter in practice?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: DEL-ToM presents consistent ToM improvements from inference-time belief tracing in small language models.
  Evidence: Key claim/abstract: DEL-ToM "consistently improves Theory-of-Mind reasoning in small language models without architectural changes."

**Paper B**: Are Vision Language Models Cross-Cultural Theory of Mind Reasoners?
  Claim: The cross-cultural VLM benchmark shows that strong headline ToM scores can coexist with major false-belief deficits, regional variance, and social desirability bias.
  Evidence: Abstract/key claim: frontier VLMs achieve ">93% accuracy on cross-cultural ToM probes" but still show "false-belief reasoning deficits (19–83% accuracy)," "20–30% regional gaps," and "social desirability bias."

**Relevance to thesis**: This is an honest scope limiter. Inference-time methods may improve narrow ToM tasks yet fail on cross-cultural, false-belief, or bias-sensitive settings. That means test-time gains may not eliminate the relevance of authentic socially grounded training data for deployment-critical behavior.
**Beat affected**: 7
**Suggested handling**: Constrain any competing-mechanism claim to the benchmark regime actually tested. Require cross-cultural false-belief and bias evaluations before concluding that inference-time scaling materially reduces the need for authentic post-training data. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

### C2: 🔴 CRITICAL — scope_disagreement

**Source focus**: Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?
**Question**: Do large, aggressively filtered Common Crawl derivatives show that web contamination does not straightforwardly translate into lower model quality?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI pollution of the web structurally harms retrieval systems, producing exposure contamination and masked accuracy degradation.
  Evidence: The paper reports Retrieval Collapse, where contaminated web pools disproportionately dominate retrieved evidence, suggesting quality failures from polluted web inputs.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, built from 96 Common Crawl snapshots and 15 trillion tokens, yields better-performing LLMs than other open pretraining datasets, especially with educational-content filtering.
  Evidence: The key claim ties model gains to large-scale web decanting and filtering rather than to avoidance of web data; the abstract emphasizes dependence on both size and quality.

**Relevance to thesis**: This tension strongly complicates a simple decline story. It suggests polluted web content can be disastrous in one pipeline stage while filtered web at scale remains a high-performing training substrate.
**Beat affected**: 7
**Suggested handling**: Distinguish between raw web exposure and refined web corpora. Frame contamination effects as pipeline-dependent: retrieval is highly vulnerable to exposure amplification, whereas pretraining can benefit from large-scale filtering and selection. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### C1: 🔴 CRITICAL — competing_mechanism

**Source focus**: Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)
**Question**: If RLAIF matches RLHF on standard alignment tasks, where is uniquely human post-training data still necessary?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: RLAIF achieves performance comparable to RLHF across summarization and dialogue tasks, and direct-RLAIF outperforms canonical RLAIF by obtaining rewards directly from an LLM.
  Evidence: The paper states that collecting high-quality human preference labels is expensive and reports comparable performance to RLHF using AI feedback instead of human feedback.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Current language models exhibit substantial misalignment with US demographic groups' opinions, even after demographic steering.
  Evidence: The paper reports that model opinions are misaligned with real human demographic groups at a magnitude comparable to major political divides, implying that task-level success does not guarantee socially grounded alignment to actual human populations.

**Relevance to thesis**: This is strong counterevidence to any broad claim that authentic human data is always necessary for post-training quality. It narrows the thesis: human data looks less necessary for generic helpfulness benchmarks, but still valuable when the target is representation of real, heterogeneous human viewpoints.
**Beat affected**: 7
**Suggested handling**: State explicitly that AI feedback is a credible substitute for human labels on standard summarization/dialogue optimization, but argue that authentic human data remains uniquely valuable for demographic validity, contested preferences, and socially grounded opinion alignment. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C5: 🔴 CRITICAL — competing_mechanism

**Source focus**: Does data composition matter for social reasoning? (benchmarks vs ablation)
**Question**: Is weak social reasoning caused mainly by poor post-training data composition, or by a failure to externalize ToM knowledge that is already internally encoded?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: Fine-tuning on a small, carefully curated dataset can strongly improve aligned behavior, implying post-training data composition is a high-leverage factor.
  Evidence: LIMA's central empirical result is that "only 1,000 carefully curated examples" can produce large alignment gains, making post-training composition look causally important.

**Paper B**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: LLMs encode intrinsic Theory of Mind features internally but fail to externalize them reliably; causal-oriented steering can align internal ToM knowledge with external behavior.
  Evidence: CoSToM explicitly argues that models already have "intrinsic Theory of Mind features internally" and that the key failure is unreliable externalization, which can be corrected by "causal-oriented steering."

**Relevance to thesis**: This is a direct competing mechanism against a pure data-composition story. If ToM is already latent and the bottleneck is externalization, then changing training data composition may be less decisive than activation/steering methods for social reasoning outcomes.
**Beat affected**: 7
**Suggested handling**: Acknowledge CoSToM as an alternative explanation. Recast the thesis from 'data composition is the sole driver' to 'data authenticity/composition is one driver among others, alongside representation externalization and control-time steering.' State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C1: 🔴 CRITICAL — competing_mechanism

**Source focus**: Does inference-time scaling reduce the importance of training data quality for social reasoning?
**Question**: Can structured inference-time reasoning recover social reasoning performance without changing training data, thereby reducing how much post-training data quality matters?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: DEL-ToM argues that inference-time scaling via Dynamic Epistemic Logic-grounded belief tracing consistently improves Theory-of-Mind reasoning in small language models without architectural changes.
  Evidence: Abstract/key claim: "Inference-time scaling via Dynamic Epistemic Logic-grounded belief tracing consistently improves Theory-of-Mind reasoning in small language models without architectural changes."

**Paper B**: The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Competence in
  Claim: The Pragmatic Mind of Machines argues that pragmatic competence depends on training stage, with pre-training, SFT, and preference optimization each having different effects across 22 models.
  Evidence: Abstract/key claim: "Pre-training, SFT, and preference optimization stages differentially affect pragmatic competence in LLMs as measured by the ALTPRAG benchmark across 22 models."

**Relevance to thesis**: This is the strongest direct competing-mechanism tension. If social/pragmatic reasoning can be substantially improved by a test-time epistemic scaffold, then a thesis centered on post-training data authenticity risks overstating training-data causality unless it shows effects beyond what inference-time support can explain.
**Beat affected**: 7
**Suggested handling**: Treat DEL-ToM-style inference scaffolds as a first-class rival explanation. Evaluate L_auth effects with and without DEL-ToM on the same models and tasks; claim training-data importance only for the residual performance gap not closed by test-time epistemic tracing. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

### C2: 🔴 CRITICAL — competing_mechanism

**Source focus**: Does inference-time scaling reduce the importance of training data quality for social reasoning?
**Question**: Is weak social reasoning mainly a problem of missing training signals, or of latent Theory-of-Mind knowledge not being reliably externalized at inference time?

**Paper A**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: CoSToM claims that LLMs already encode intrinsic Theory-of-Mind features internally, and that causal-oriented steering can align that internal knowledge with external behavior.
  Evidence: Abstract/key claim: "LLMs encode intrinsic Theory of Mind features internally but fail to externalize them reliably; causal-oriented steering can align internal ToM knowledge with external behavior."

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Social-R1 claims that reinforcement learning with multi-dimensional process rewards aligned to human cognition improves social reasoning beyond outcome-based RL.
  Evidence: Abstract/key claim: "Reinforcement learning with multi-dimensional process rewards aligned to human cognition improves social reasoning in LLMs beyond outcome-based RL."

**Relevance to thesis**: These papers offer opposing causal stories for social reasoning gains. CoSToM says the capability may already be present and needs better inference-time access; Social-R1 says better training-time reward/process signals are needed. If CoSToM is right, authentic post-training data may be less central than the thesis implies.
**Beat affected**: 7
**Suggested handling**: Frame the thesis as one mechanism among at least two: data/reward learning and inference-time externalization. A decisive test would compare causal steering, social-process RL, and their combination under matched base models and datasets. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

### C6: 🟡 MODERATE — scope_disagreement

**Source focus**: Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)
**Question**: Do self-generated or synthetic instruction pipelines reduce the importance of authentic human instruction data?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Language models can be aligned to follow instructions using self-generated instruction data, reducing reliance on costly human annotations.
  Evidence: Self-Instruct explicitly argues that model-generated instructions can replace substantial amounts of human-written instruction data for alignment.

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: A large-scale, crowd-sourced, multilingual human-generated conversation corpus is valuable open infrastructure for alignment.
  Evidence: OpenAssistant positions human-generated, multilingual conversations and rankings as a key resource for democratizing and improving alignment research.

**Relevance to thesis**: This is a clear scope disagreement over whether authentic human data is essential or mainly a bootstrap resource. Self-Instruct is substantial counterevidence for generic instruction-following, while OpenAssistant suggests human data remains important for realism, multilingual breadth, and grounding in actual user interaction.
**Beat affected**: 6
**Suggested handling**: Concede that synthetic instruction generation can substitute for humans on generic instruction-following. Then reserve the stronger claim for settings requiring natural conversational distributions, multilingual nuance, and user-grounded preference diversity. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C3: 🟡 MODERATE — scope_disagreement

**Source focus**: Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story?
**Question**: Is degraded web quality the main driver of model performance limits, or can sophisticated deduplication and quality filtering offset it?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content can dominate retrieval outputs and create misleadingly healthy-seeming results despite real degradation.
  Evidence: The reported >80% exposure contamination from a 67% polluted pool indicates strong downstream brittleness once the live web is polluted.

**Paper B**: Yi: Open Foundation Models by 01.AI
  Claim: Yi's strong benchmark performance is primarily attributable to data quality obtained through cascaded deduplication and quality filtering over 3.1 trillion tokens.
  Evidence: The key claim makes data quality engineering, not curated non-web sourcing, the primary explanation for strong results.

**Relevance to thesis**: This limits any blanket argument that more AI-tainted web data straightforwardly means worse models. Yi suggests that quality-control mechanisms can remain powerful even at massive scale.
**Beat affected**: 7
**Suggested handling**: Rephrase the thesis around conditional vulnerability: web pollution is a serious risk, but corpus engineering can partially offset it for pretraining. Avoid claiming monotonic decline without specifying filtering strength and downstream use. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

### C3: 🟡 MODERATE — methodological_tension

**Source focus**: Does inference-time scaling reduce the importance of training data quality for social reasoning?
**Question**: Do reasoning-oriented interventions help social reasoning more at inference time than at training time?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: DEL-ToM reports that adding structured inference-time belief tracing improves ToM reasoning in small models without changing the architecture.
  Evidence: Abstract/key claim: "Inference-time scaling via Dynamic Epistemic Logic-grounded belief tracing consistently improves Theory-of-Mind reasoning in small language models without architectural changes."

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Traces of Social Competence finds that instruction tuning only partially improves ToM, while reasoning-oriented fine-tuning amplifies problematic response patterns.
  Evidence: Abstract/key claim: "Instruction tuning partially improves Theory of Mind in LLMs but reasoning-oriented fine-tuning amplifies problematic response patterns."

**Relevance to thesis**: This does not refute training-data effects, but it sharply limits simple narratives. More 'reasoning' is not uniformly good: reasoning-heavy post-training can worsen social behavior, while reasoning-heavy inference scaffolds can help. That weakens any monotonic claim that better post-training data/processes alone drive socially grounded gains.
**Beat affected**: 7
**Suggested handling**: Distinguish training-time reasoning interventions from inference-time reasoning interventions. The thesis should avoid treating them as interchangeable and should test whether L_auth predicts gains after controlling for reasoning-oriented fine-tuning side effects. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

### C2: 🟡 MODERATE — competing_mechanism

**Source focus**: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
**Question**: Is recursive synthetic training unstable by default, or can correction mechanisms make it viable without fresh human data?

**Paper A**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Claim: Training generative models on model-generated content causes irreversible model collapse where tails of the original distribution disappear.
  Evidence: The paper argues that generated-data recursion makes models forget rare structure, treating self-training as intrinsically degenerative.

**Paper B**: Self-Correcting Self-Consuming Loops for Generative Model Training
  Claim: Introducing an idealized correction function makes self-consuming generative training loops exponentially more stable and prevents collapse.
  Evidence: The paper identifies an explicit correction mechanism as the key causal variable and shows, in a mixed theoretical/experimental setup, that collapse can be avoided when correction is available.

**Relevance to thesis**: This weakens any simple 'synthetic data causes collapse' narrative by introducing a concrete alternative mechanism: the problem may be lack of correction, not syntheticity per se.
**Beat affected**: 7
**Suggested handling**: Treat this as a scope limiter: recursive training is dangerous without correction, but not necessarily with strong error-correction or verification. Emphasize that the correction function is idealized and may be hard to realize in open settings. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

### C6: 🟡 MODERATE — competing_mechanism

**Source focus**: When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation)
**Question**: Are observed gains from 'curation' really evidence that synthetic data can replace fresh human data, or are they better explained by aggressive filtering of large human/web corpora?

**Paper A**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Curated synthetic self-consumption can optimize human preferences and avoid collapse.
  Evidence: The paper presents curation of synthetic data as the decisive ingredient that makes self-consuming loops beneficial rather than destructive.

**Paper B**: Yi: Open Foundation Models by 01.AI
  Claim: Yi models' strong performance is primarily attributable to data quality achieved through cascaded deduplication and quality filtering of 3.1 trillion tokens.
  Evidence: The paper attributes model quality to large-scale filtering and deduplication of non-synthetic training data, offering a strong non-synthetic explanation for performance gains.

**Relevance to thesis**: This is an alternative-mechanism challenge: better outcomes may come from better human/web data curation, not from synthetic substitution. That limits how strongly one can generalize from curated-synthetic successes.
**Beat affected**: 7
**Suggested handling**: Require apples-to-apples comparisons against equally curated fresh-human-data baselines. Do not treat improvement under curated synthetic data as proof that fresh human data are unnecessary when large, high-quality real corpora remain available. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

### C3: 🟡 MODERATE — competing_mechanism

**Source focus**: Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF)
**Question**: Can constitutional or AI-only feedback remove the need for human labels in alignment?

**Paper A**: Constitutional AI: Harmlessness from AI Feedback
  Claim: A harmless yet non-evasive AI assistant can be trained using only AI-generated feedback guided by a constitution of principles, without human labels for harmful outputs.
  Evidence: The abstract explicitly says the system is trained 'without any human labels identifying harmful outputs,' presenting AI supervision itself as sufficient for an important alignment target.

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: A large-scale, crowd-sourced, multilingual human-generated conversation corpus can democratize LLM alignment research by providing open high-quality feedback data.
  Evidence: The paper's core contribution is that open, human-generated conversational and feedback data are valuable infrastructure for alignment, implying human-authored supervision remains important.

**Relevance to thesis**: This is real counterevidence against a blanket human-data necessity claim. However, it is also scope-limited: Constitutional AI focuses on harmlessness under an explicit constitution, whereas OpenAssistant emphasizes broader, multilingual, user-facing alignment grounded in actual human interactions.
**Beat affected**: 6
**Suggested handling**: Acknowledge that AI-only feedback can work well when the objective is codified in advance by a fixed constitution. Then argue that authentic human data still matters for open-ended, multilingual, socially situated interactions where the target values are not fully specifiable upfront. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C6: 🟡 MODERATE — competing_mechanism

**Source focus**: Does data composition matter for social reasoning? (benchmarks vs ablation)
**Question**: For social reasoning, is post-training data composition the key lever, or does the optimization objective/reward design matter more?

**Paper A**: From Quantity to Quality: Boosting LLM Performance with Self-Guided Data Selecti
  Claim: Self-guided data selection for instruction tuning improves LLM performance by prioritizing data quality over quantity.
  Evidence: From Quantity to Quality makes the case that selecting better instruction-tuning data is a major source of downstream gains.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Reinforcement learning with multi-dimensional process rewards aligned to human cognition improves social reasoning in LLMs beyond outcome-based RL.
  Evidence: Social-R1 reports that social reasoning improves through "multi-dimensional process rewards aligned to human cognition," pointing to reward structure, not just data composition, as the critical mechanism.

**Relevance to thesis**: This weakens any monocausal reading of the thesis. Even if data composition matters, Social-R1 suggests that socially grounded reasoning may depend more on how training signals reward intermediate cognitive processes than on which instruction examples are selected.
**Beat affected**: 7
**Suggested handling**: Position data composition as interacting with objective design. If arguing for L_auth, note that its effects may need to be disentangled from reward/process-supervision effects in social tasks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

### C5: 🟡 MODERATE — competing_mechanism

**Source focus**: Does inference-time scaling reduce the importance of training data quality for social reasoning?
**Question**: Could extra test-time compute be a stronger driver of performance than scaling model parameters or training-stage changes, including on social-adjacent tasks?

**Paper A**: Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model
  Claim: This paper argues that optimally scaling test-time compute can be more effective than scaling model parameters for improving performance.
  Evidence: Abstract/key claim: "Optimally scaling LLM test-time compute can be more effective than scaling model parameters for improving performance."

**Paper B**: The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Competence in
  Claim: ALTPRAG reports that pragmatic competence differs across pre-training, SFT, and preference-optimization stages.
  Evidence: Abstract/key claim: "Pre-training, SFT, and preference optimization stages differentially affect pragmatic competence in LLMs."

**Relevance to thesis**: This is indirect but important. If compute scaling can dominate model-scale changes in general, then a training-data-centered account of social reasoning needs to show it explains variance that cannot be matched by extra inference-time compute. Otherwise data authenticity may be only one contributor among several.
**Beat affected**: 7
**Suggested handling**: Present this as a live external validity threat rather than a refutation. Run pragmatic/social benchmarks under controlled test-time compute budgets to measure whether L_auth still predicts outcomes after compute scaling. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

### C6: 🟢 MINOR — implicit_tension

**Source focus**: Does inference-time scaling reduce the importance of training data quality for social reasoning?
**Question**: Are at least some apparent social-reasoning deficits artifacts of evaluating models without generic inference-time reasoning scaffolds?

**Paper A**: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
  Claim: Chain-of-thought prompting substantially improves reasoning performance at inference time without modifying training data.
  Evidence: Abstract/key claim: "Chain-of-thought prompting enables large language models to substantially improve reasoning performance at inference time without modifying training data."

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: Neural Theory-of-Mind? finds that GPT-3 lacks social intelligence out-of-the-box and struggles on intent, reaction, and mental-state inference tasks.
  Evidence: Abstract/key claim: "GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on tasks measuring intent, reaction, and mental state inference."

**Relevance to thesis**: This is only a scope tension, not a direct contradiction, because the ToM paper evaluates out-of-the-box ability while CoT shows what prompting can unlock in other reasoning domains. Still, it cautions against interpreting poor unscaffolded social reasoning as pure evidence of missing training-data quality.
**Beat affected**: 7
**Suggested handling**: Re-evaluate social-reasoning baselines with CoT/self-consistency-style scaffolds before attributing deficits mainly to post-training data. If deficits persist under scaffolding, the data-authenticity argument is stronger. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---


## Summary

Total contradictions: 37
Critical (must address): 18

## Thesis Risk Assessments

- Moderate. The strongest collapse papers do not survive as universal claims once conditioning variables are introduced: user curation, explicit correction, constitutional constraints, and narrow post-training objectives all provide credible cases where synthetic data or feedback can replace some fresh human supervision. However, these counterexamples are mostly conditional, objective-specific, or theoretical. The biggest remaining support for the thesis is that open-ended recursive pretraining still appears fragile, rare-tail preservation remains unresolved, and provenance/verification assumptions often break in realistic web-scale settings.
- Heuristic contradiction fallback used after model failure. Treat the strongest tension around 'Paraphrasing evades detectors of AI-generated text vs Retrieval Collapses When AI Pollutes the Web' as a scope limiter for this focus question, not as a settled verdict. Original error: OpenAI agent_run failed after 3 retries. Last model: gpt-5.4. State has been saved — you can resume with --resume.
- Heuristic contradiction fallback used after model failure. Treat the strongest tension around 'The Rise of AI-Generated Content in Wikipedia vs The RefinedWeb Dataset for Falcon LLM: Outperformi' as a scope limiter for this focus question, not as a settled verdict. Original error: OpenAI agent_run failed after 3 retries. Last model: gpt-5.4. State has been saved — you can resume with --resume.
- The thesis faces substantial but not fatal risk from the AI-feedback and synthetic-data papers. RLAIF, Constitutional AI, AlpacaFarm, DPO, RRHF, and Self-Instruct jointly show that for many standard alignment objectives, curated synthetic data, AI feedback, or simplified preference optimization can rival or replace expensive human-supervised RLHF pipelines. That is real counterevidence, not a side note. The defensible position is narrower: authentic human data appears least necessary for generic benchmarkable helpfulness and harmlessness, but remains most valuable where the target is socially grounded legitimacy rather than aggregate task performance—especially demographic representativeness, plural and contested preferences, multilingual realism, and high-precision curation of scarce examples.
- The strongest papers in this set show that synthetic instruction data, AI feedback, and self-alignment can substantially reduce the amount of new human-authored supervision needed for open-model instruction following. However, the contradiction set indicates that this substitution is not total: human-authored data remains difficult to remove for bootstrapping, legitimacy, demographic representativeness, and evaluation. The main risk is overclaiming from benchmark parity to broad human alignment.
- Overall risk to a simple contamination-to-quality-decline story is high. The strongest counterpressure comes from RefinedWeb, FineWeb, and Yi, which all report that filtered, deduplicated, or quality-screened web corpora can produce very strong models, sometimes outperforming curated alternatives. The strongest harm evidence in this set comes from retrieval and source-specific pollution papers, especially Retrieval Collapse and the Wikipedia study, but those results operate in different regimes: live search/RAG exposure or contaminated subdomains rather than carefully refined pretraining corpora. The C4 documentation paper is especially important because it prevents overclaiming on either side: it shows that web corpora can hide machine-generated text and benchmark contamination, and that filtering can create social skew. Net: these papers do not support a universal contamination-equals-decline law; they support a conditional thesis where outcomes depend on filtration quality, documentation, source mix, and whether the system consumes raw web content or refined corpora.
- moderate. The selected J papers provide real evidence that post-training data composition and curation matter for general alignment and instruction following, but the I papers repeatedly show that this does not straightforwardly translate to social reasoning. The strongest risks are: (1) benchmark mismatch, where preference or instruction-following gains are not evidence of Theory-of-Mind competence; (2) social-specific negative or partial results, where reasoning-oriented fine-tuning can worsen ToM behavior; and (3) alternative mechanisms, especially internal-knowledge externalization and reward-design effects. So the thesis is supportable only in a narrowed form: data composition matters, but current evidence does not show it is sufficient or dominant for social reasoning outcomes.
- Moderate-to-high risk if the thesis implies that post-training data authenticity is the dominant or sufficient explanation for socially grounded reasoning outcomes. The sharpest risks come from DEL-ToM and CoSToM, which suggest that social-reasoning failures can be mitigated by inference-time scaffolds or steering without changing the underlying training data. However, the risk is not thesis-fatal if the thesis is framed more carefully: authentic post-training data may still matter, especially for cross-cultural robustness, false-belief reasoning, bias control, and real-world externalization, but it must be positioned alongside inference-time scaling, steering, and reward-design mechanisms rather than above them by default.

## Unresolved Tensions

- Whether curated synthetic data can preserve rare, socially important tail cases rather than merely optimize average preferences or benchmark performance.
- How to operationalize 'verified' synthetic data at scale when provenance labels are missing or unreliable in open-web collection.
- Whether post-training successes with AI feedback or self-generated instructions transfer to broad pretraining regimes without diversity collapse.
- Whether apparent benefits of synthetic curation remain after comparison to equally strong filtering, deduplication, and freshness in human/web data.
- What empirical evidence, not just theory, shows long-horizon self-consuming loops remain stable under realistic curation noise.
- Whether provenance-style defenses scale outside provider-controlled ecosystems.
- How much detector robustness survives paraphrase, human editing, and mixed-authorship settings.
- Fallback heuristic used for Is web pollution detectable? (pollution scale vs detection limits); review the cited pair manually if this focus question becomes central in the prose.
- Whether measured contamination in a few platforms or corpora generalizes to broad web pretraining mixtures.
- How much current filtering pipelines are already offsetting contamination without making the risk disappear.
- Fallback heuristic used for How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement); review the cited pair manually if this focus question becomes central in the prose.
- How much of the apparent success of AI-feedback methods comes from benchmark choice rather than true capture of heterogeneous human values?
- Do simulated or AI raters preserve minority and subgroup preferences, or only majority/LLM-prior judgments?
- Is the scarce resource actually large-scale human preference data, or tiny amounts of exceptionally curated human demonstrations?
- Can constitutions and AI feedback encode enough normative detail to replace authentic human feedback in open-ended social settings?
- How should one measure 'human value' in post-training: aggregate win rate, demographic faithfulness, multilingual coverage, or resistance to sycophancy and opinion drift?
- How much of the apparent success of AI feedback is downstream of hidden human supervision in teacher models, constitutions, or seed datasets?
- Do synthetic-data and AI-feedback wins on MT-Bench, summarization, and dialogue transfer to pluralistic social preference alignment across demographic groups?
- When papers say 'without human annotation,' are they replacing ongoing labels only, or truly removing dependence on prior human-authored supervision?
- Is the main driver of success synthetic supervision itself, or the strength of the base model and teacher model that generate the synthetic data?
- How much AI-generated or benchmark-leaked content remains inside successful filtered corpora such as RefinedWeb and FineWeb after cleaning, and at what level does it begin to measurably hurt performance?
- Are benchmark improvements from aggressive web filtering masking fairness, coverage, or community-representation losses similar to those documented for C4 blocklists?
- Why does web pollution appear catastrophic for retrieval exposure while filtered web remains effective for pretraining: is the key difference ranking dynamics, deduplication, source selection, or contamination concentration?
- Do educational-content filters improve average benchmark scores by narrowing domain diversity, thereby complicating claims about overall data authenticity or social grounding?
- Can provenance and documentation practices close the gap between high-performing filtered web corpora and concerns about hidden machine-generated content, consent, and representational bias?
- Would socially targeted data curation, rather than generic high-quality instruction tuning, close the Theory-of-Mind gaps reported by Neural Theory-of-Mind and Traces of Social Competence?
- Are social benchmark failures mainly due to missing social knowledge in training data, or due to failures in eliciting/externalizing knowledge already present in the model as CoSToM suggests?
- How much of observed social-reasoning improvement is attributable to data composition versus optimization objective, especially process-reward RL as in Social-R1?
- Do preference-based chat benchmarks systematically overstate socially grounded competence relative to dedicated ToM, false-belief, or multi-turn social benchmarks?
- Whether DEL-ToM-style gains transfer from benchmark ToM tasks to open-ended, deployed social reasoning settings.
- Whether authentic post-training data and inference-time scaling are additive, substitutive, or interactive mechanisms.
- Whether causal steering is merely exposing pre-existing social knowledge or depends on prior training stages that already encode the needed representations.
- How much of the apparent effect of post-training quality disappears once models are given CoT, self-consistency, or budget-forced test-time compute.
- Whether cross-cultural false-belief failures and social desirability bias can be fixed by inference-time methods alone, or require different training data/provenance.