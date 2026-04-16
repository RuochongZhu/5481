# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## Executive Summary

1. When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) → Can curated recursive synthetic data substitute for fresh human data without collapse, or does recursive training inevitably erase tail information?
   Handling: State the thesis conditionally: indiscriminate recursive substitution collapses, but curated synthetic data may work when selection is explicitly aligned to human preferences and tail preservation assumptions hold. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.
2. Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) → Does agreement with simulated or AI feedback imply real social alignment across human groups?
   Handling: Differentiate generic preference agreement from demographic or community-grounded alignment. Use this tension to argue that human data remains especially important for subgroup representativeness, contested values, and opinion-sensitive applications. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
3. How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? → Does AI-distilled alignment without human annotation generalize to socially grounded alignment, or only to benchmarked instruction-following?
   Handling: Treat MT-Bench-style gains as evidence for generic assistantness, not for human representativeness; require subgroup audits and provenance-sensitive human evaluation before claiming broad replacement of human supervision. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
4. How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) → Do longitudinal web studies show generalized degradation, or mainly domain-specific evolution that should not be conflated with synthetic-text decline?
   Handling: Frame synthetic-text decline as a risk model for future web degradation, not as direct evidence that the live web has already degraded broadly. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
5. Does data composition matter for social reasoning? (benchmarks vs ablation) → Do tiny, carefully curated instruction datasets produce genuine social reasoning gains, or mainly chat-alignment gains that do not transfer to Theory-of-Mind benchmarks?
   Handling: Treat LIMA as evidence for alignment/data-efficiency, not as direct evidence for social reasoning. Require social-benchmark ablations before generalizing from curated SFT success to ToM competence. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
6. Is web pollution detectable? (pollution scale vs detection limits) → Do watermark-style provenance signals make web pollution detectable in practice, or only in cooperative generation settings?
   Handling: Position watermarking as a prospective provenance mechanism, not evidence that current web pollution is broadly detectable. Make explicit that cooperative source-side marking and open-web retrospective detection are different regimes.

## Focus Coverage

- [A, E] When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) (count=6)
  Representative: Can curated recursive synthetic data substitute for fresh human data without collapse, or does recursive training inevitably erase tail information?
- [E, F] Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) (count=6)
  Representative: Does agreement with simulated or AI feedback imply real social alignment across human groups?
- [F, J] How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? (count=4)
  Representative: Does AI-distilled alignment without human annotation generalize to socially grounded alignment, or only to benchmarked instruction-following?
- [D, H] How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) (count=6)
  Representative: Do longitudinal web studies show generalized degradation, or mainly domain-specific evolution that should not be conflated with synthetic-text decline?
- [I, J] Does data composition matter for social reasoning? (benchmarks vs ablation) (count=6)
  Representative: Do tiny, carefully curated instruction datasets produce genuine social reasoning gains, or mainly chat-alignment gains that do not transfer to Theory-of-Mind benchmarks?
- [B, C] Is web pollution detectable? (pollution scale vs detection limits) (count=5)
  Representative: Do watermark-style provenance signals make web pollution detectable in practice, or only in cooperative generation settings?
- [B, E, H] Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? (count=5)
  Representative: Does lower-quality AI-generated content in a major source like Wikipedia imply overall decline in filtered web pretraining corpora?
- [K] Does inference-time scaling reduce the importance of training data quality for social reasoning? (count=6)
  Representative: Do inference-time chain-of-thought gains on benchmark reasoning transfer to socially grounded pragmatic reasoning?

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Can curated recursive synthetic data substitute for fresh human data without collapse, or does recursive training inevitably erase tail information?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated content in training causes irreversible model collapse, with disappearance of tails of the original distribution.
  Evidence: The key claim states that recursively generated training data causes 'irreversible model collapse' and that 'tails of the original data distribution disappear.'

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Under curated self-consuming training, synthetic data can prevent collapse and even optimize toward human preferences.
  Evidence: The key claim says that 'Data curation in self-consuming generative models can provably optimize human preferences and prevent model collapse under iterative retraining.' The abstract frames this as a response to unavoidable synthetic contamination in web-scale data.

**Relevance to thesis**: This is the strongest counterexample to any blanket claim that synthetic data cannot substitute for fresh human data. The disagreement turns on curation quality and selection objective, not on synthetic origin alone.
**Beat affected**: 7
**Suggested handling**: State the thesis conditionally: indiscriminate recursive substitution collapses, but curated synthetic data may work when selection is explicitly aligned to human preferences and tail preservation assumptions hold. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🔴 CRITICAL — scope_disagreement

**Question**: Does agreement with simulated or AI feedback imply real social alignment across human groups?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: LLM-simulated human feedback is far cheaper than crowdworkers while maintaining high agreement with actual human preferences.
  Evidence: Key claim: "LLM-simulated human feedback is 50x cheaper than crowdworkers while maintaining high agreement with actual human preferences."

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Current language models remain substantially misaligned with demographic groups' opinions, even after demographic steering.
  Evidence: Key claim: "Current LMs exhibit substantial misalignment with US demographic groups' opinions, on par with the Democrat-Republican divide on climate change, even after demographic steering."

**Relevance to thesis**: This sharply limits what 'agreement' means. Simulated feedback may track aggregate annotator preferences on benchmark tasks while still failing at socially grounded representation of real populations. That is exactly where authentic human data still looks valuable.
**Beat affected**: 6
**Suggested handling**: Differentiate generic preference agreement from demographic or community-grounded alignment. Use this tension to argue that human data remains especially important for subgroup representativeness, contested values, and opinion-sensitive applications. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🔴 CRITICAL — scope_disagreement

**Question**: Does AI-distilled alignment without human annotation generalize to socially grounded alignment, or only to benchmarked instruction-following?

**Paper A**: Zephyr: Direct Distillation of LM Alignment
  Claim: Direct preference optimization from AI feedback enables a 7B model to surpass Llama2-Chat-70B on MT-Bench without human annotation.
  Evidence: The key claim emphasizes benchmark-beating performance despite removing human annotation from the post-training pipeline.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Current LMs exhibit substantial misalignment with US demographic groups' opinions, even after demographic steering.
  Evidence: The key claim says misalignment is large enough to be 'on par with the Democrat-Republican divide on climate change,' showing failure on socially grounded preference representation.

**Relevance to thesis**: This is a major scope limiter for synthetic-only alignment claims: benchmark success without human annotation does not show that models capture diverse human viewpoints or socially grounded preferences.
**Beat affected**: 7
**Suggested handling**: Treat MT-Bench-style gains as evidence for generic assistantness, not for human representativeness; require subgroup audits and provenance-sensitive human evaluation before claiming broad replacement of human supervision. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Do longitudinal web studies show generalized degradation, or mainly domain-specific evolution that should not be conflated with synthetic-text decline?

**Paper A**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Claim: Privacy policies changed measurably from 1996 to 2021 in response to regulations such as GDPR and CCPA, though gaps remain in user rights.
  Evidence: The paper offers direct temporal measurement of web-text change over 25 years, but the change is structured and regulation-driven rather than a simple quality collapse.

**Paper B**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Recursive training on synthetic text causes consistent declines in linguistic diversity.
  Evidence: The paper demonstrates a degradation mechanism under recursive synthetic-data generation, not a direct measurement of open-web time evolution.

**Relevance to thesis**: This limits how far Beat 2 can go. Synthetic-recursion results identify a plausible degradation mechanism, but longitudinal live-web evidence here shows adaptation and drift, not a uniform downward trend.
**Beat affected**: 2
**Suggested handling**: Frame synthetic-text decline as a risk model for future web degradation, not as direct evidence that the live web has already degraded broadly. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🟡 MODERATE — scope_disagreement

**Question**: Do tiny, carefully curated instruction datasets produce genuine social reasoning gains, or mainly chat-alignment gains that do not transfer to Theory-of-Mind benchmarks?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: LIMA argues that data composition matters strongly for alignment: a 65B LLM fine-tuned on only 1,000 carefully curated examples can perform comparably to much larger aligned systems.
  Evidence: Key claim states that fine-tuning a 65B LLM on 1,000 carefully curated examples without reinforcement learning achieves performance comparable or preferred to GPT-4 in 43% of cases.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: Neural Theory-of-Mind finds that large LMs still lack robust social intelligence and Theory of Mind on explicit social benchmarks.
  Evidence: Key claim states GPT-3 lacks social intelligence out-of-the-box, struggling substantially on SocialIQa and ToMi benchmarks.

**Relevance to thesis**: This does not refute that composition matters, but it limits the scope: generic curated alignment data can improve preference judgments without demonstrating improved social reasoning.
**Beat affected**: 6
**Suggested handling**: Treat LIMA as evidence for alignment/data-efficiency, not as direct evidence for social reasoning. Require social-benchmark ablations before generalizing from curated SFT success to ToM competence. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Do watermark-style provenance signals make web pollution detectable in practice, or only in cooperative generation settings?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: Web pollution can become severe enough to contaminate most retrieved exposure while remaining hard to notice operationally.
  Evidence: The paper's main empirical result is that 67% pool contamination yields over 80% exposure contamination, with quality degradation masked by a homogenized result set.

**Paper B**: A Watermark for Large Language Models
  Claim: LLM outputs can be watermarked so that generated text is algorithmically detectable from short token spans with negligible quality loss.
  Evidence: The paper proposes green-token promotion during sampling and reports short-span detectability without materially harming output quality.

**Relevance to thesis**: This is not a direct contradiction, but a key scope limiter: watermarking supports detectability only when generators adopt it, whereas Retrieval Collapse concerns the already-existing, largely unwatermarked web.
**Beat affected**: 6
**Suggested handling**: Position watermarking as a prospective provenance mechanism, not evidence that current web pollution is broadly detectable. Make explicit that cooperative source-side marking and open-web retrospective detection are different regimes.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Does lower-quality AI-generated content in a major source like Wikipedia imply overall decline in filtered web pretraining corpora?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: Over 5% of newly created English Wikipedia articles are flagged as AI-generated, and these articles are typically of lower quality and often self-promotional or biased.
  Evidence: The paper identifies measurable AI-generation penetration in Wikipedia creation and ties it to degraded article quality and bias-related concerns.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: A heavily filtered multi-snapshot web corpus can still improve LLM performance relative to other open pretraining datasets.
  Evidence: FineWeb reports better model performance from a very large Common Crawl-derived corpus and FineWeb-Edu further improves knowledge- and reasoning-intensive benchmarks.

**Relevance to thesis**: This is a scope disagreement rather than a direct contradiction. Wikipedia may be locally degrading under AI content, but FineWeb suggests such local pollution does not automatically translate into whole-web pretraining decline when corpus selection is broad and aggressively filtered.
**Beat affected**: 5
**Suggested handling**: Constrain claims to source-specific degradation. Treat polluted subdomains like Wikipedia as risk hotspots, not as sufficient evidence that all filtered web corpora are deteriorating. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Do inference-time chain-of-thought gains on benchmark reasoning transfer to socially grounded pragmatic reasoning?

**Paper A**: Self-Consistency Improves Chain of Thought Reasoning in Language Models
  Claim: Self-consistency decoding substantially boosts chain-of-thought performance on arithmetic and commonsense reasoning benchmarks.
  Evidence: The key claim states that self-consistency 'substantially boosts chain-of-thought prompting performance on arithmetic and commonsense reasoning benchmarks' by marginalizing over diverse sampled reasoning paths.

**Paper B**: Relevant answers to polar questions.
  Claim: A goal-sensitive probabilistic Theory-of-Mind model predicts human overinformative answers better than LLMs.
  Evidence: The paper claims that PRIOR-PQ 'predicts human overinformative answering patterns better than LLMs,' showing that current LLMs still lag on nuanced pragmatic relevance despite broad reasoning advances.

**Relevance to thesis**: This is not a direct contradiction, but it limits how far one can generalize inference-time reasoning gains. Stronger decoding can improve standard reasoning benchmarks while still leaving socially grounded pragmatics unsolved, which preserves room for training-data/authenticity explanations.
**Beat affected**: 7
**Suggested handling**: Do not treat benchmark CoT gains as evidence that data quality no longer matters for social reasoning. Require direct evaluation on pragmatic and human-judgment tasks before downgrading the role of authentic post-training data. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C3: 🔴 CRITICAL — scope_disagreement

**Question**: Are synthetic instruction/dialogue datasets sufficient on their own, or does human post-editing still materially improve output quality?

**Paper A**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: LLM-rewritten instructions via Evol-Instruct produce higher-complexity training data that yields a model preferred over ChatGPT on complex tasks.
  Evidence: The key claim presents synthetic instruction rewriting as a successful route to stronger instruction-following performance without relying on manual creation of complex instruction data.

**Paper B**: Fine-tuning with HED-IT: The impact of human post-editing for dialogical languag
  Claim: Fine-tuning with human post-edited data yields higher perceived quality outputs than using unedited machine-generated dialogues.
  Evidence: The key claim directly compares human-post-edited versus machine-generated dialogue data and finds an advantage for the human-edited version.

**Relevance to thesis**: This is an important scope limiter: synthetic data may work well on benchmarked instruction complexity, yet human-authored revision still appears to matter for perceived conversational quality.
**Beat affected**: 6
**Suggested handling**: Avoid claiming full replacement of human supervision; instead argue that synthetic data can cover broad instruction-following, while human post-editing remains valuable for style, coherence, and user-perceived quality. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: Is collapse an unavoidable consequence of synthetic retraining, or can the training objective be changed so synthetic data becomes safe or even helpful?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive use of generated data causes irreversible degradation and loss of distributional support.
  Evidence: The paper's key claim is that model-generated data in training leads to irreversible collapse, especially disappearance of distribution tails.

**Paper B**: Self-Improving Diffusion Models with Synthetic Data
  Claim: Synthetic data can be used in a controlled way to prevent autophagy disorder and preserve quality and diversity.
  Evidence: The key claim states that 'Treating synthetic data as negative guidance during generation can prevent model autophagy disorder and maintain quality and diversity.' The abstract explicitly positions this as a mitigation for pressure to train on synthetic data when real data is scarce.

**Relevance to thesis**: This limits the scope of collapse claims: synthetic data may be harmful under naïve reuse, but not under objectives that treat it as a corrective signal rather than a plain replacement for human data.
**Beat affected**: 7
**Suggested handling**: Distinguish 'train-on-synthetic as replacement' from 'use synthetic as constrained guidance.' Note that the latter does not vindicate unrestricted substitution, but it does show collapse is not mechanically inevitable. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C5: 🔴 CRITICAL — methodological_tension

**Question**: When filtered-web datasets outperform alternatives, is that evidence against web degradation, or evidence that heavy filtering can mask contamination while introducing new biases?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: C4 contains significant unexpected content, including machine-generated text and benchmark examples, and its blocklist filtering disproportionately removes text from certain populations.
  Evidence: The paper shows both contamination and representational distortion inside a major web corpus.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Filtered and deduplicated web data alone can outperform curated corpora.
  Evidence: The paper argues that careful filtering is sufficient to turn raw web data into a superior pretraining source.

**Relevance to thesis**: This creates a central interpretation problem: high-performing filtered-web corpora do not by themselves show that the live web is healthy, because preprocessing may simultaneously remove harmful drift and alter authenticity or representativeness.
**Beat affected**: 2
**Suggested handling**: Report contamination rates, leakage, and population effects alongside performance. Do not use downstream gains alone as evidence that live-web degradation is negligible. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: When instruction-tuning data quality is improved, does social reasoning reliably improve, or can fine-tuning still worsen false-belief behavior?

**Paper A**: From Quantity to Quality: Boosting LLM Performance with Self-Guided Data Selecti
  Claim: Improving data quality through self-guided selection boosts LLM performance, implying composition is more important than raw quantity for fine-tuning outcomes.
  Evidence: Key claim states that self-guided data selection for instruction tuning can boost LLM performance by prioritizing data quality over quantity.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: On social reasoning specifically, fine-tuning is not uniformly beneficial: instruction tuning helps only partially, and reasoning-oriented fine-tuning can amplify bad ToM behavior.
  Evidence: Key claim states that instruction tuning partially helps Theory of Mind in LLMs, but reasoning-oriented fine-tuning amplifies problematic response patterns on False Belief tasks.

**Relevance to thesis**: This is a strong scope limiter for the main claim. It suggests that 'better instruction data' is not enough as a general rule for social reasoning and may even backfire on core social-cognitive evaluations.
**Beat affected**: 6
**Suggested handling**: Narrow the claim to targeted or authenticity-sensitive social data, and explicitly note that generic quality-based fine-tuning gains do not guarantee gains on false-belief or mental-state tasks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🔴 CRITICAL — methodological_tension

**Question**: Do more complex, reasoning-oriented instruction datasets improve social reasoning, or can they make Theory-of-Mind errors worse?

**Paper A**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: WizardLM claims that making instruction data more complex via Evol-Instruct yields better downstream behavior on complex tasks.
  Evidence: Key claim states that LLM-rewritten instructions via Evol-Instruct produce higher-complexity training data that yields a model preferred over ChatGPT on complex tasks.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: For social reasoning, more reasoning-oriented fine-tuning is not uniformly helpful and can amplify problematic false-belief patterns.
  Evidence: Key claim states that reasoning-oriented fine-tuning amplifies problematic response patterns on False Belief tasks, even though instruction tuning partially helps.

**Relevance to thesis**: This is a direct tension for the 'data composition matters' claim: complexity-enhanced instruction data may improve generic complex-task preference while degrading performance on social-cognitive tasks.
**Beat affected**: 6
**Suggested handling**: Explicitly separate generic reasoning complexity from socially grounded reasoning quality. Social benchmarks should be a required validation layer for any claim that richer instruction data improves social reasoning. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — implicit_tension

**Question**: Does better optimization to human preferences always improve alignment, or can it amplify preference pathologies like sycophancy?

**Paper A**: RRHF: Rank Responses to Align Language Models with Human Feedback without tears
  Claim: RRHF can align language models to human preferences using a ranking loss while avoiding PPO complexity.
  Evidence: Key claim: "RRHF aligns language models with human preferences using ranking loss on conditional probabilities, avoiding PPO's complexity while requiring only 1-2 models."

**Paper B**: AI Supported Degradation of the Self Concept: A Theoretical Framework Grounded i
  Claim: Human-feedback-tuned assistants can become sycophantic because humans and preference models may prefer convincing agreement over correctness.
  Evidence: Key claim: "AI assistants finetuned with human feedback consistently exhibit sycophancy, partly because humans and preference models prefer convincingly-written sycophantic responses over correct ones."

**Relevance to thesis**: This is a key limiter on claims that human preference data is straightforwardly valuable. Human data remains valuable, but only if authenticity is distinguished from raw preference optimization; otherwise alignment may optimize the wrong social target.
**Beat affected**: 6
**Suggested handling**: Argue that authentic human data is not equivalent to uncorrected preference labels. Emphasize that human data is most valuable when paired with provenance, subgroup context, and truthfulness-aware evaluation rather than naive preference maximization. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Can retrieval remain a reliable defense once the underlying web corpus is itself heavily polluted by AI-generated text?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content can trigger Retrieval Collapse: when 67% of the candidate pool is contaminated, retrieval exposure exceeds 80% contaminated results, producing homogenized sources while masking quality degradation.
  Evidence: The paper reports an empirical retrieval failure mode in which high pool contamination translates into even higher exposure contamination, and the abstract emphasizes a 'deceptively healthy' state where degradation is not obvious from system behavior alone.

**Paper B**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Although paraphrasing can destroy classifier-style detection, retrieval is presented as an effective defense that restores robustness.
  Evidence: The paper shows DIPPER paraphrasing drops DetectGPT accuracy from 70.3% to 4.6% at 1% false positive rate, but then argues retrieval-based defenses can recover robustness against such attacks.

**Relevance to thesis**: This is the strongest tension for the detectability question: retrieval is proposed as a defense in one paper, but another says polluted retrieval environments themselves collapse and hide the problem.
**Beat affected**: 7
**Suggested handling**: Separate 'retrieval over a trusted corpus' from 'retrieval over the open web.' Treat retrieval as a conditional defense that requires provenance control, corpus curation, or contamination auditing; do not cite it as a general solution to web-scale pollution.

---

## C3: 🔴 CRITICAL — competing_mechanism

**Question**: Does rising AI-generated content on the live web imply broad training-data degradation, or can filtering and deduplication largely neutralize that effect?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: More than 5% of newly created English Wikipedia articles are flagged as AI-generated, and those articles are typically lower quality and often self-promotional or biased.
  Evidence: This is direct temporal evidence that a major live-web knowledge source is accumulating lower-quality AI-generated content.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora like The Pile.
  Evidence: The paper's central result is that web-only data, once aggressively cleaned, is sufficient for strong pretraining performance.

**Relevance to thesis**: This is a major scope limiter. It supports source-level contamination but challenges any broad claim that live-web degradation already makes web-scale pretraining materially worse overall.
**Beat affected**: 2
**Suggested handling**: State that contamination is demonstrated for specific sources, but quantify its end-to-end training impact with time-sliced ablations before generalizing to the whole web. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C4: 🔴 CRITICAL — competing_mechanism

**Question**: Does long-run compositional drift of the web amount to degradation for LLM pretraining, or can large-scale quality filtering over many snapshots still improve outcomes?

**Paper A**: "Way back then": A Data-driven View of 25+ years of Web Evolution
  Claim: Over 25+ years, streaming media and social networking sites have replaced news and education websites in popularity.
  Evidence: The paper provides direct longitudinal evidence that the web's content mix has shifted away from historically text-rich, informational domains.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, built from 96 Common Crawl snapshots, produces better-performing LLMs than other open pretraining datasets, and FineWeb-Edu strongly improves knowledge and reasoning benchmarks.
  Evidence: Despite drawing from broad web snapshots over time, the dataset yields superior downstream performance after filtering and selection.

**Relevance to thesis**: This is a serious competing mechanism against a strong degradation reading. Temporal drift is real, but the existence of better-performing filtered corpora implies that drift does not straightforwardly translate into lower training utility.
**Beat affected**: 2
**Suggested handling**: Separate 'web composition changed' from 'usable training quality declined'; require matched-snapshot experiments showing that later raw web slices are worse even after comparable filtering. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Can AI-generated preference signals replace expensive human feedback for alignment on standard tasks?

**Paper A**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Human-in-the-loop reinforcement learning treats RL as fundamentally human-centered, with human-centric design described as key to successful RL.
  Evidence: Key claim: "Reinforcement learning is fundamentally a human-in-the-loop paradigm, and human-centric design is key to successful RL."

**Paper B**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: RLAIF can match RLHF performance, and direct-RLAIF can even outperform canonical RLAIF by using LLM-provided rewards instead of human labels.
  Evidence: Key claim: "RLAIF achieves comparable performance to RLHF across summarization and dialogue tasks, and direct-RLAIF outperforms canonical RLAIF by obtaining rewards directly from an LLM." The abstract explicitly motivates this by the high cost of human preference labels.

**Relevance to thesis**: This is the strongest counterexample to any broad claim that human post-training data is generally indispensable. It suggests human data may be most valuable for calibration, auditing, or socially grounded edge cases, rather than for scaling routine preference supervision.
**Beat affected**: 7
**Suggested handling**: Concede that on mainstream summarization/dialogue benchmarks, AI feedback is a real substitute for human feedback. Narrow the thesis to cases where authentic human provenance is needed for representativeness, contested norms, or community-specific judgments. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Does AI-generated web pollution necessarily imply lower-quality training data, or can strong filtering and deduplication preserve high-quality web-only pretraining?

**Paper A**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora like The Pile.
  Evidence: The paper's central result is that a web-only corpus, after filtering and deduplication, outperforms curated-corpus baselines, directly arguing that web origin alone does not doom data quality.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content causes Retrieval Collapse: 67% pool contamination leads to over 80% exposure contamination in search results, homogenizing sources while masking quality degradation.
  Evidence: The paper reports a nonlinear exposure effect in retrieval systems, where contaminated content becomes overrepresented and quality degradation is hidden behind apparently healthy retrieval outputs.

**Relevance to thesis**: This is a major scope limiter against a simple contamination-equals-decline story. One paper shows that engineered web corpora can work extremely well; the other shows that unfiltered retrieval exposure can collapse under pollution. The tension suggests the mechanism is not 'web data bad' in general, but whether collection and exposure are controlled.
**Beat affected**: 7
**Suggested handling**: Narrow the thesis: contamination harms are real in open-web retrieval and weakly filtered pipelines, but RefinedWeb shows those harms are not universal under strong filtering, deduplication, and corpus construction. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🔴 CRITICAL — competing_mechanism

**Question**: If the web is increasingly polluted, can large-scale refinement still turn Common Crawl into better training data than other open corpora?

**Paper A**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, a 15-trillion token dataset from 96 Common Crawl snapshots, produces better-performing LLMs than other open pretraining datasets, and FineWeb-Edu dramatically improves knowledge- and reasoning-intensive benchmarks.
  Evidence: The paper attributes gains to large-scale decanting of Common Crawl and reports benchmark improvements over alternative open pretraining datasets, including on reasoning-heavy tasks.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web pollution structurally degrades retrieval, with 67% pool contamination producing over 80% exposure contamination and source homogenization.
  Evidence: The reported collapse mechanism implies that downstream systems consuming polluted web content can look healthy while becoming substantively less diverse and lower quality.

**Relevance to thesis**: FineWeb is strong evidence that filtered web corpora can remain or become excellent even while the broader open web becomes worse for retrieval. That directly complicates any monotonic contamination-to-quality-decline narrative.
**Beat affected**: 7
**Suggested handling**: Explicitly separate pretraining-corpus engineering from live-web retrieval. Use Retrieval Collapse as evidence about unfiltered exposure dynamics, not as proof that all web-derived training corpora are declining in quality. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🔴 CRITICAL — competing_mechanism

**Question**: Is weak social reasoning mainly a training-data composition problem, or an elicitation/externalization problem that can be fixed without new data?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: LIMA supports a data-composition account: careful curation of a small post-training dataset can drive major alignment gains.
  Evidence: The paper reports strong alignment outcomes from only 1,000 carefully curated examples and no reinforcement learning.

**Paper B**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: CoSToM proposes a competing mechanism: LLMs already contain internal Theory-of-Mind knowledge, but fail to externalize it reliably; causal steering improves stable external ToM behavior.
  Evidence: Key claim states that LLMs possess internal ToM knowledge but fail to externalize it reliably, and that causal-oriented steering can align internal cognition with stable external ToM behavior.

**Relevance to thesis**: This is a real alternative explanation. If social reasoning is latent and mainly blocked at readout or control time, then post-training data composition may be less central than steering or elicitation mechanisms.
**Beat affected**: 7
**Suggested handling**: Acknowledge this as a competing mechanism, not a refutation. The thesis should compare provenance-aware data interventions against steering-based interventions on the same social benchmarks. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Are social-reasoning failures mainly due to missing authentic training signals, or do models already contain Theory-of-Mind knowledge that can be unlocked at inference time?

**Paper A**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: LLMs already possess internal Theory-of-Mind knowledge, and causal-oriented steering can make that knowledge appear as stable external ToM behavior.
  Evidence: The abstract states that 'LLMs possess internal ToM knowledge but fail to externalize it reliably' and that causal-oriented steering can 'align internal cognition with stable external ToM behavior.' This makes externalization/steering a rival explanation to data-quality deficits.

**Paper B**: The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Competence in
  Claim: Pragmatic competence depends materially on the training pipeline, with different effects from pre-training, SFT, and preference optimization.
  Evidence: The paper's key claim says 'Pre-training, SFT, and preference optimization stages differentially affect pragmatic competence in LLMs,' and the abstract describes stage-specific effects on social-adjacent reasoning across 22 models.

**Relevance to thesis**: This is a direct competing mechanism. If CoSToM is right, socially grounded failures may reflect poor readout of latent competence rather than insufficiently authentic post-training data. If ALTPRAG-style stage effects are right, training data and supervision remain causally important.
**Beat affected**: 7
**Suggested handling**: Treat this as a major adversarial alternative. Test whether provenance/authenticity still predicts social outcomes after adding causal steering on the same base model, and report whether steering closes or only partially closes the gap. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C2: 🔴 CRITICAL — competing_mechanism

**Question**: Does inference-time scaling reduce the importance of training data quality for social reasoning?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: Inference-time scaling with a Dynamic Epistemic Logic verifier can improve Theory-of-Mind reasoning in small language models without changing the architecture.
  Evidence: The key claim says 'DEL-ToM improves Theory-of-Mind reasoning in small language models through inference-time scaling using a Dynamic Epistemic Logic-grounded verifier rather than architectural changes.' The abstract explicitly frames this as an inference-time route to better ToM.

**Paper B**: The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Competence in
  Claim: Training-stage differences substantially affect pragmatic competence.
  Evidence: The benchmark paper reports that pre-training, SFT, and preference optimization have different measurable effects on pragmatic competence across 22 models, indicating that what happens during training matters for social-adjacent behavior.

**Relevance to thesis**: This is the clearest direct tension for the focus question. DEL-ToM says substantial ToM gains can come from test-time logic/verifier machinery alone, while ALTPRAG-style results say social/pragmatic competence tracks training-stage differences.
**Beat affected**: 7
**Suggested handling**: Explicitly acknowledge DEL-ToM as a real rival mechanism. Run controlled comparisons: same base model and training data, with and without DEL-ToM, then test whether authenticity-sensitive post-training still explains variance beyond verifier-based inference-time scaling. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Does synthetic data fail as a substitute for human data in general, or only for broad-distribution pretraining rather than narrow post-training alignment tasks?

**Paper A**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Claim: Training generative models on model-generated content causes irreversible model collapse with loss of distribution tails.
  Evidence: The key claim states that recursive training on generated data makes models forget and that tails of the original distribution disappear.

**Paper B**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Self-generated instruction data can substitute for costly human annotation in instruction tuning.
  Evidence: The key claim says that language models can be aligned using 'self-generated instruction data,' thereby 'reducing reliance on costly human annotations.'

**Relevance to thesis**: This is an important scope limiter: synthetic substitution can work in post-training instruction alignment even if it is risky for repeated full-distribution generative pretraining.
**Beat affected**: 6
**Suggested handling**: Separate pretraining-distribution preservation from post-training supervision generation. Do not generalize collapse results from generative recursion to instruction-tuning regimes without rare-tail preservation requirements. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Can curated synthetic rewrites outperform human-authored supervision in some tasks, despite collapse results for recursive synthetic pretraining?

**Paper A**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Claim: Recursive model-generated training data causes forgetting and collapse.
  Evidence: The paper claims that generated-data training leads to irreversible forgetting and collapse of the original distribution's tails.

**Paper B**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: LLM-rewritten instructions can produce better supervision than human-written data for complex instruction following.
  Evidence: The key claim states that 'LLM-rewritten instructions via Evol-Instruct produce higher-complexity training data that yields a model preferred over ChatGPT on complex tasks.'

**Relevance to thesis**: This is a strong pro-curation counterexample: synthetic data is not merely a fallback for missing humans, but can sometimes be the preferred supervision source when the objective is complexity amplification rather than faithful distribution preservation.
**Beat affected**: 6
**Suggested handling**: Frame the thesis around what fresh human data is uniquely needed for: grounding, rare cases, and social authenticity. Concede that curated synthetic transformations can outperform raw human supervision on bounded optimization targets. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Can successful large-scale detection in a constrained domain like MOOCs be generalized to the heterogeneous web?

**Paper A**: AI See What You Did There – The Prevalence of LLM-Generated Answers in MOOC Resp
  Claim: AI-generated content is highly prevalent in MOOC responses and can be identified at scale using textual analysis metrics.
  Evidence: The paper reports both prevalence and scalable identification in an educational setting with repeated task structure, common prompt formats, and relatively narrow genre variation.

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Detectability depends on generation method, domain, and detection technique; no single approach is universally reliable.
  Evidence: The survey's central conclusion is that current methods vary substantially across domains and models, so broad generalization is not warranted.

**Relevance to thesis**: This is a scope limiter rather than a thesis-killer: domain-specific detectability does not establish detectability of polluted web content in the wild.
**Beat affected**: 5
**Suggested handling**: Use MOOC results only as evidence for structured, institutionally bounded settings. Avoid extrapolating them to open-web contamination without cross-domain validation.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Does synthetic instruction generation remove the need for human instruction data, or does a tiny curated human set still carry disproportionate value?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Self-generated instruction data can align models while reducing reliance on costly human annotations.
  Evidence: Key claim: "Language models can be aligned to follow instructions using self-generated instruction data, reducing reliance on costly human annotations."

**Paper B**: LIMA: Less Is More for Alignment
  Claim: A very small but carefully curated human dataset can produce strong alignment without RL.
  Evidence: Key claim: "Fine-tuning a 65B LLM on only 1,000 carefully curated examples without reinforcement learning achieves performance comparable or preferred to GPT-4 in 43% of cases."

**Relevance to thesis**: These papers jointly suggest that human data may no longer be needed in large volumes, but may still be highly valuable in small, high-quality, carefully curated form. This is a scope refinement, not a thesis-killer.
**Beat affected**: 5
**Suggested handling**: Frame human data value in terms of sample efficiency and seed quality rather than raw volume. Concede that synthetic expansion can replace scale, while arguing that curated human exemplars still anchor behavior and evaluation targets. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Is minimal-supervision self-alignment enough for safety alignment, or do safety-critical settings still require large human-labeled datasets?

**Paper A**: Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Hum
  Claim: Principle-driven self-alignment with LLM-generated synthetic data and minimal human supervision can produce assistants comparable to RLHF-based approaches.
  Evidence: The key claim reports helpful, ethical, and reliable assistants from synthetic data with only minimal human input, though the paper notes dependence on the quality and coverage of the small set of human-written principles.

**Paper B**: BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dat
  Claim: BeaverTails provides separately annotated helpfulness and harmlessness labels for 333,963 QA pairs, enabling improved safety alignment of LLMs.
  Evidence: The key claim foregrounds a large human-preference

**Relevance to thesis**: N/A
**Beat affected**: N/A
**Suggested handling**: State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Does scaling diverse, high-quality synthetic conversation data solve pragmatic social reasoning?

**Paper A**: Enhancing Chat Language Models by Scaling High-quality Instructional Conversatio
  Claim: UltraChat argues that scaling diverse, high-quality synthetic instructional conversations substantially improves chat model performance.
  Evidence: Key claim states that scaling high-quality synthetic instructional conversations without human queries can substantially improve open-source chat language model performance.

**Paper B**: Relevant answers to polar questions.
  Claim: On nuanced pragmatic social judgment, current LLMs still underperform a goal-sensitive probabilistic Theory-of-Mind model.
  Evidence: Key claim states that PRIOR-PQ predicts human overinformative answering patterns better than LLMs.

**Relevance to thesis**: This tension suggests that better synthetic conversation composition improves generic chat behavior, but not necessarily the socially grounded inferential abilities needed for pragmatic relevance judgments.
**Beat affected**: 6
**Suggested handling**: Use this as evidence that composition likely matters only when it contains socially diagnostic structure; generic synthetic chat scaling should not be presented as sufficient for social reasoning. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Can self-generated instruction data substitute for socially grounded data in pragmatic question answering?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Self-Instruct argues that language models can be aligned effectively using self-generated instruction data, reducing dependence on expensive human annotations.
  Evidence: Key claim states that language models can be aligned to follow instructions using self-generated instruction data, reducing reliance on costly human annotations.

**Paper B**: Relevant answers to polar questions.
  Claim: Nuanced pragmatic relevance judgments still favor an explicit goal-sensitive ToM model over state-of-the-art LLMs.
  Evidence: Key claim states that PRIOR-PQ predicts human relevance judgments in polar question answering better than LLMs.

**Relevance to thesis**: This limits how far annotation-light data-composition successes can be taken: self-generated instruction diversity may help instruction following, but not the social inference needed for relevance and goal-tracking.
**Beat affected**: 6
**Suggested handling**: Frame self-generated instruction data as useful for alignment efficiency, while noting that pragmatic social reasoning may require explicitly socially grounded or provenance-aware examples. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Do logic-enhanced inference-time scaffolds solve social reasoning, or mainly improve formal benchmark reasoning?

**Paper A**: Faithful Logical Reasoning via Symbolic Chain-of-Thought
  Claim: Symbolic Chain-of-Thought significantly outperforms standard CoT on logical reasoning benchmarks.
  Evidence: The key claim says SymbCoT, which integrates symbolic expressions and logic rules with CoT prompting, 'consistently and significantly outperforms standard CoT on logical reasoning benchmarks.'

**Paper B**: Are Vision Language Models Cross-Cultural Theory of Mind Reasoners?
  Claim: Even frontier models with high overall Theory-of-Mind accuracy still fail on false-belief reasoning and show social desirability bias across cultures.
  Evidence: The benchmark reports '>93% overall ToM accuracy' for frontier VLMs but also '19-83% accuracy' on false-belief reasoning, '20-30% gaps' across regions, and systematic social desirability bias.

**Relevance to thesis**: SymbCoT suggests that formal reasoning scaffolds can produce large gains, but the cross-cultural ToM paper shows that socially grounded understanding remains brittle even in very strong models. This limits any claim that inference-time logic alone makes training data quality unimportant.
**Beat affected**: 7
**Suggested handling**: Position symbolic/inference-time gains as potentially task-specific. Evaluate whether such methods help on cross-cultural false-belief and bias-sensitive settings before using them to discount provenance-aware social data collection. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: If recursive synthetic training is irreversible, how can later work report recovery or improvement from self-training on synthetic data?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Once recursively trained on generated data, models undergo irreversible collapse.
  Evidence: The core claim uses the language of 'irreversible model collapse' under recursive training on model-generated content.

**Paper B**: Neon: Negative Extrapolation From Self-Training Improves Image Generation
  Claim: Self-training on synthetic data can improve image generation if updates are reversed into negative extrapolation away from degraded weights.
  Evidence: The key claim says that 'Reversing gradient updates from self-training on synthetic data extrapolates away from degraded weights and improves image generation quality.' The abstract notes this even under pressure to use synthetic augmentation when real data is limited.

**Relevance to thesis**: This is a serious challenge to the irreversibility part of the collapse narrative. It suggests the failure mode may be tied to standard update rules rather than to synthetic data per se.
**Beat affected**: 7
**Suggested handling**: Keep the collapse claim tied to conventional recursive retraining. Acknowledge that alternative optimization dynamics can partially reverse degradation, especially in image-generation settings. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: Are high reported detection accuracies robust under adversarial rewriting, or mainly benchmark results in easier settings?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Classifier-style AI-text detection is highly brittle under paraphrasing.
  Evidence: Using the 11B-parameter DIPPER paraphraser, the paper reduces DetectGPT accuracy from 70.3% to 4.6% at 1% false positive rate, showing that post-hoc textual signatures can be largely erased.

**Paper B**: Distinguishing Reality from AI: Approaches for Detecting Synthetic Content
  Claim: Hybrid multimodal detection approaches can reach up to 92% accuracy, outperforming single-modality methods.
  Evidence: The survey synthesizes results reporting high synthetic-content detection accuracy, especially when multiple modalities or signals are combined.

**Relevance to thesis**: This tension matters because benchmark accuracy claims can overstate real detectability if they are not stress-tested against paraphrasing and adaptive contamination tactics.
**Beat affected**: 7
**Suggested handling**: Treat high-accuracy detector results as upper bounds from structured evaluations. Require adversarial evaluation before using them as evidence that web pollution is detectable at scale.

---

## C5: 🟡 MODERATE — methodological_tension

**Question**: How strong are internet-wide pollution claims when the measurement foundation for detecting AI text is itself non-universal?

**Paper A**: The Dead Internet Theory: Investigating the Rise of AI-Generated Content and Bot
  Claim: The Dead Internet Theory is substantively supported by growing dominance of bots and AI-generated content that alters online interactions.
  Evidence: The paper advances a broad survey-level claim that bot and AI-content growth has become structurally important enough to substantiate the theory.

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Current AI-text detectability is contingent on domain, generation method, and detection technique, with no universally reliable method.
  Evidence: The survey explicitly concludes that existing detection approaches do not generalize reliably across contexts.

**Relevance to thesis**: This tension does not refute pollution concerns, but it weakens strong web-scale prevalence rhetoric if the underlying identification tools are unstable or domain-limited.
**Beat affected**: 4
**Suggested handling**: Downgrade sweeping 'web-wide dominance' claims to motivating hypotheses unless backed by direct platform measurements, provenance signals, or domain-specific audits with known error rates.

---

## C1: 🟡 MODERATE — methodological_tension

**Question**: Are diversity metrics alone strong enough to establish measurable degradation, or are some of the common metrics too unstable under corpus variation?

**Paper A**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Recursively training language models on synthetic text leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative tasks.
  Evidence: The paper presents empirical degradation signals in multiple diversity dimensions under recursive synthetic-data training.

**Paper B**: Towards robust complexity indices in linguistic typology
  Claim: Traditional corpus-based complexity indices such as type-token ratio and word-level entropy are less robust to corpus size and content variation than newer indices.
  Evidence: Across 47 languages, the paper finds that TTR and entropy are comparatively sensitive to corpus size/content effects, which can confound cross-corpus comparisons.

**Relevance to thesis**: This does not refute degradation, but it weakens any Beat 2 argument that relies on simple lexical-diversity metrics as if they were direct evidence of live-web decline.
**Beat affected**: 2
**Suggested handling**: Treat metric-based degradation claims as provisional unless they are replicated with size-matched corpora and more robust diversity indices. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🟡 MODERATE — methodological_tension

**Question**: Do entropy and type-token ratio provide stable temporal drift measurements in practice, or only under large-text asymptotics?

**Paper A**: Entropy and type-token ratio in gigaword corpora
  Claim: Word entropy and type-token ratio follow an empirical functional relation across corpora and languages, derivable from Zipf's and Heaps' laws in the large-text limit.
  Evidence: The paper argues that these diversity measures are linked analytically and empirically across languages when corpora are sufficiently large.

**Paper B**: Towards robust complexity indices in linguistic typology
  Claim: TTR and word-level entropy are less robust than newer complexity indices when corpus size and content vary.
  Evidence: The paper explicitly shows that these classic measures are sensitive to corpus composition and sampling, which is exactly the condition in temporal web slices.

**Relevance to thesis**: This creates a real measurement tension: a metric can be theoretically well-behaved in the limit while still being unreliable for practical temporal web comparisons.
**Beat affected**: 2
**Suggested handling**: Use entropy/TTR only with explicit large-sample checks and pair them with robustness-tested measures before inferring degradation over time. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🟡 MODERATE — methodological_tension

**Question**: If human preference data matters, is RLHF itself necessary, or is the optimization machinery largely replaceable?

**Paper A**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: The survey frames RL as a fundamentally human-in-the-loop paradigm, implying that successful alignment is tightly linked to the human-feedback RL setup.
  Evidence: Key claim: "Reinforcement learning is fundamentally a human-in-the-loop paradigm."

**Paper B**: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
  Claim: DPO shows the core RLHF objective can be reformulated as a simple classification loss, eliminating the need for explicit reinforcement learning.
  Evidence: Key claim: "RLHF can be reformulated as a simple classification loss by reparameterizing the reward model, enabling direct policy optimization without reinforcement learning."

**Relevance to thesis**: This does not refute the value of human data, but it does refute any conflation of human-data value with RLHF pipeline complexity. The literature supports separating 'human signal' from 'RL machinery.'
**Beat affected**: 7
**Suggested handling**: State explicitly that the claim is about the source and authenticity of preference data, not about PPO or RLHF as the uniquely correct optimization method. Treat DPO as a scope-limiting simplification, not a side note. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🟡 MODERATE — methodological_tension

**Question**: Does open alignment still require large human-authored corpora once simulated feedback achieves high agreement with humans?

**Paper A**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: A large-scale crowd-sourced, human-annotated conversation corpus enables open and democratized research on LLM alignment.
  Evidence: The abstract centers alignment progress on human-annotated SFT and preference-style data, presenting the corpus as the enabling resource for open alignment research.

**Paper B**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: LLM-simulated human feedback is 50x cheaper than crowdworkers while maintaining high agreement with actual human preferences.
  Evidence: The key claim reports both a major cost reduction and strong agreement with real human preferences, implying a scalable substitute for crowd annotation.

**Relevance to thesis**: This tension goes directly to reliance on human-authored supervision: if simulated feedback is faithful enough, large human conversation collections may be less necessary than OpenAssistant implies.
**Beat affected**: 6
**Suggested handling**: Frame human corpora as high-value calibration and transparency resources rather than the only viable source of supervision; distinguish bootstrap data from scalable feedback generation. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Can better corpus engineering convert the liabilities of web crawl data into a performance advantage?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: Documenting C4 reveals machine-generated text, benchmark examples, and socially skewed filtering artifacts.
  Evidence: The study shows that even a widely used cleaned crawl can contain unexpected synthetic and evaluation content, while its cleaning steps introduce representational bias.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb's 15-trillion-token, 96-snapshot web dataset produces better-performing LLMs than other open pretraining datasets, with FineWeb-Edu especially improving knowledge and reasoning benchmarks.
  Evidence: FineWeb is explicitly presented as a large-scale refinement of Common Crawl that yields superior downstream model performance, suggesting the pipeline can be engineered to extract high-quality value from the web.

**Relevance to thesis**: Together these papers imply that the decisive variable is not simply contamination level but corpus construction quality. That weakens any simple story where more web contamination straightforwardly means worse model quality.
**Beat affected**: 6
**Suggested handling**: Use C4 documentation to justify why corpus documentation and auditing are needed; use FineWeb to show that those interventions can succeed at scale. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C6: 🟡 MODERATE — implicit_tension

**Question**: Even when filtered web corpora yield strong models, do they remain socially and procedurally defensible as data sources?

**Paper A**: Yi: Open Foundation Models by 01.AI
  Claim: Yi models' strong performance is primarily attributed to data quality from a cascaded deduplication and quality filtering pipeline over 3.1 trillion tokens.
  Evidence: The system paper explicitly credits performance to aggressive data-quality engineering over a massive web-derived corpus.

**Paper B**: Consent in Crisis: The Rapid Decline of the AI Data Commons
  Claim: In 2023-2024, web data restrictions grew rapidly, rendering over 5% of tokens in major AI corpora like C4 nonconsented due to ineffective consent protocols.
  Evidence: The paper documents that major web corpora can remain high-performing yet still contain materially nonconsented data as consent conditions change.

**Relevance to thesis**: This does not contradict model-quality gains, but it sharply limits what those gains establish. A filtered web corpus can be high quality in the benchmark sense while still failing on provenance and consent, so 'quality did not decline' is not the whole story.
**Beat affected**: 6
**Suggested handling**: Distinguish technical quality from legitimacy and provenance. Present filtered-web success as a performance result, not a full vindication of current web-corpus practices. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C6: 🟡 MODERATE — implicit_tension

**Question**: Can inference-time logic-based ToM improvements substitute for socially grounded competence on pragmatic human judgments?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: A verifier-driven inference-time scaling method can improve Theory-of-Mind reasoning in small language models.
  Evidence: DEL-ToM is explicitly presented as improving ToM reasoning 'through inference-time scaling' using a logic-grounded verifier and not through architectural retraining.

**Paper B**: Relevant answers to polar questions.
  Claim: State-of-the-art LLMs still underperform a probabilistic ToM model on nuanced relevance judgments in polar question answering.
  Evidence: PRIOR-PQ is reported to predict human relevance and overinformativeness patterns better than LLMs, indicating that socially grounded pragmatic competence remains incomplete in current language models.

**Relevance to thesis**: This is a scope-limiting tension: DEL-ToM may raise performance on ToM-style tasks, but the pragmatic relevance paper suggests that socially grounded humanlike reasoning is not obviously solved by inference-time logic. That leaves room for authentic social training data to matter.
**Beat affected**: 7
**Suggested handling**: Acknowledge that inference-time scaling may improve structured ToM tasks without eliminating deficits on pragmatics. Test DEL-ToM-style methods on relevance-judgment datasets before concluding that training-data quality has become secondary. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C6: 🟡 MODERATE — competing_mechanism

**Question**: Are observed gains really about fresh human provenance, or can large-scale quality filtering and deduplication dominate provenance effects in practice?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Synthetic contamination in recursive training is the mechanism driving collapse and tail loss.
  Evidence: The paper attributes degradation to training on model-generated data, emphasizing recursive contamination as the cause of irreversible collapse.

**Paper B**: Yi: Open Foundation Models by 01.AI
  Claim: Strong model performance is primarily attributable to data quality from a cascaded deduplication and quality filtering pipeline over 3.1 trillion tokens.
  Evidence: The key claim for Yi says its strong performance is 'primarily attributed to data quality' produced by large-scale deduplication and filtering.

**Relevance to thesis**: This introduces a real competing mechanism: some performance differences attributed to fresh human data may instead be explained by aggressive filtering, deduplication, and scale. That does not refute collapse, but it weakens provenance-only explanations.
**Beat affected**: 5
**Suggested handling**: Be explicit that provenance is not the only operative variable. Compare provenance-aware claims against scale, deduplication, and quality-filtering baselines before concluding that fresh human data is uniquely responsible for gains. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C6: 🟡 MODERATE — competing_mechanism

**Question**: Are downstream alignment gains mainly about human feedback, or can upstream corpus curation and filtering dominate model quality?

**Paper A**: Yi: Open Foundation Models by 01.AI
  Claim: Yi attributes its strong performance primarily to large-scale data-quality engineering through cascaded deduplication and quality filtering.
  Evidence: Key claim: "Yi models' strong performance is primarily attributed to data quality from a cascaded deduplication and quality filtering pipeline over 3.1 trillion tokens."

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: OpenAssistant presents a large-scale crowd-sourced human-annotated conversation corpus as an enabling resource for LLM alignment.
  Evidence: Key claim: "A large-scale crowd-sourced, human-annotated conversation corpus enables open and democratized research on LLM alignment."

**Relevance to thesis**: This is a real competing mechanism: some apparent alignment or usability gains may come more from massive pretraining-data curation than from human post-training data. That weakens any claim assigning too much causal credit to RLHF-style supervision alone.
**Beat affected**: 4
**Suggested handling**: Separate base-model capability from post-training alignment. Acknowledge that upstream curation can dominate broad performance, while reserving the human-data claim for norms, preferences, and socially grounded behavior that filtering alone cannot specify. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🟡 MODERATE — competing_mechanism

**Question**: Is better social reasoning primarily a matter of inference-time steering, or of targeted training with hard social examples and process rewards?

**Paper A**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: Stable external ToM behavior can be obtained by steering models that already contain latent ToM knowledge.
  Evidence: CoSToM argues that LLMs 'possess internal ToM knowledge' and that causal steering aligns that internal cognition with external ToM outputs.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: More human-like social intelligence comes from reinforcement learning with multi-dimensional process rewards on adversarially hard social reasoning examples.
  Evidence: The key claim says that 'reinforcement learning with multi-dimensional process rewards on adversarially hard social reasoning examples yields more human-like social intelligence' than outcome-based RL. This points to targeted training signals, not just inference-time control.

**Relevance to thesis**: These papers offer different causal stories. CoSToM weakens the claim that missing authentic data is the central bottleneck, while Social-R1 supports the idea that carefully constructed social training signals matter.
**Beat affected**: 7
**Suggested handling**: Present these as potentially complementary but unresolved. Test substitution vs additivity: does causal steering still help after Social-R1 training, and does Social-R1 still help after steering? Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---


## Summary

Total contradictions: 44
Critical (must address): 18

## Thesis Risk Assessments

- Moderate. A universal 'synthetic data cannot replace fresh human data' thesis is not supported by this set. The strongest opposing evidence shows three viable substitution regimes: curated recursive retraining with preference-aware selection, modified self-training objectives that use synthetic data safely, and post-training instruction tuning with self-generated supervision. However, these counterexamples are narrower than the collapse papers: they usually depend on curation, correction functions, bounded tasks, or alternative objectives rather than plain recursive replacement. The safest thesis is therefore conditional: unverified or indiscriminate recursive substitution risks collapse and tail loss, but curated or verified synthetic data can substitute for fresh human data in constrained regimes.
- Overall risk is moderate. The strongest evidence points against any simple claim that web pollution is broadly detectable today: classifier-style detectors are brittle under paraphrasing, and even retrieval-based defenses may fail once the retrieval corpus itself is polluted. At the same time, watermarking and structured-domain detectors show that detectability is possible under narrower, cooperative, or highly constrained conditions. The honest synthesis is that web pollution is only conditionally detectable; current evidence does not support a blanket claim of reliable open-web detection.
- The evidence for measurable live-web drift is strong, but the evidence for broad live-web degradation is only moderate. Longitudinal H papers clearly show temporal change in web composition, policy language, AI-content incidence, and consent status. However, D-side metric evidence is methodologically fragile, and strong filtered-web results from FineWeb and RefinedWeb provide real competing explanations: drift may be substantial while usable training quality remains recoverable through filtering, deduplication, and selection. Beat 2 is safest if stated as 'the web is measurably changing, with documented contamination and access degradation in some slices,' not 'the live web has already undergone a general measurable quality collapse for pretraining.'
- The literature does not support a blanket claim that human post-training data is always necessary or uniquely effective. The biggest risks come from RLAIF and AlpacaFarm, which show that AI-generated or simulated feedback can match human-feedback pipelines on common alignment benchmarks, and from DPO/RRHF, which show that much of RLHF's optimization stack is replaceable. The strongest defensible position is narrower: human data remains most valuable where authentic social grounding matters, especially for subgroup representation, contested norms, failure analysis, and correcting preference pathologies such as sycophancy. Small, carefully curated human datasets may still have outsized value even when synthetic or AI feedback handles scale.
- Moderate. The harm papers provide real evidence that AI pollution can degrade specific information ecosystems, especially unfiltered retrieval environments and source-specific domains like Wikipedia, and that documentation can uncover serious contamination and bias problems. But RefinedWeb, FineWeb, and Yi are strong counterevidence against any universal claim that more web contamination straightforwardly causes lower model quality. The defensible thesis is narrower: contamination risk is real, but outcomes depend heavily on filtering, deduplication, corpus documentation, snapshot diversity, and whether the system consumes the live web through retrieval rather than a carefully engineered training corpus.
- Overall risk is moderate-to-high for any broad claim that post-training data composition by itself explains social reasoning gains. The J papers consistently show that curation, filtering, complexity, or synthetic scaling can improve alignment and chat performance, but the I papers show that these gains do not automatically transfer to Theory-of-Mind, false-belief reasoning, or pragmatic relevance judgments. The strongest risk comes from two places: (1) social-benchmark papers showing that fine-tuning can partially help yet still worsen specific ToM behaviors, and (2) CoSToM offering a genuine competing mechanism in which latent social knowledge already exists and the main problem is externalization rather than data composition. The thesis is safest if narrowed to: data composition matters, but only targeted, socially grounded, authenticity-sensitive composition should be expected to improve social reasoning.
- The strongest risk to the thesis is real and should be stated plainly: multiple papers offer credible non-data mechanisms for better social reasoning, especially DEL-ToM's verifier-based inference-time scaling and CoSToM's claim that ToM knowledge is already latent and mainly needs steering. These are genuine competing explanations, not side notes. However, the risk is not thesis-fatal yet, because the papers showing inference-time or steering gains are mostly benchmark-focused, while other work shows persistent failures on pragmatics, false belief, cross-cultural generalization, and stage-sensitive social competence. The safest thesis position is therefore: authentic post-training data likely matters, but it is not the only mechanism; inference-time scaling, steering, and model-internal latent knowledge are serious alternatives that must be experimentally ruled out or shown to be complementary.

## Unresolved Tensions

- Which curation or verification signals actually preserve rare tails and socially grounded edge cases, rather than only improving average preference fit?
- Do instruction-tuning successes with synthetic data transfer to full-distribution pretraining, or are they only valid for narrow post-training supervision tasks?
- How much of the positive evidence is due to curation itself versus competing mechanisms such as model scale, massive token counts, deduplication, or filtering?
- Can provenance-aware verification reliably identify when synthetic data is safe enough to substitute for human data, or are objective-level corrections more important than source labels?
- The current set does not resolve whether strong inference-time scaling or other test-time techniques can compensate for weaker training-data authenticity, so authenticity remains only one of several plausible mechanisms.
- What contamination rate do real open-web retrieval systems currently face, and how close are they to the collapse regime reported at 67% pool contamination?
- Can retrieval-based defenses still work when the reference corpus has mixed or unknown provenance rather than being clean and curated?
- How much of real-world AI-generated web text is watermarked or provenance-tagged, and do those signals survive reposting, editing, or paraphrasing?
- Which detector results transfer from narrow domains like MOOCs, phishing, or code assignments to heterogeneous web text, and with what false positive rates?
- We still lack matched time-slice pretraining experiments that compare earlier vs later raw web snapshots under identical filtering, deduplication, and model budgets.
- Metric-based degradation claims need stronger validation because classic diversity measures can be sensitive to corpus size and content shifts.
- Evidence for AI-generated drift is currently strong in specific sources like Wikipedia, but not yet sufficient to quantify whole-web contamination.
- Filtered-web performance gains do not resolve whether authenticity, representativeness, and consent are degrading simultaneously on the live web.
- Whether RLAIF-style parity with RLHF holds outside summarization/dialogue and into high-stakes socially grounded tasks.
- Whether simulated or AI feedback preserves minority-group and community-specific preferences rather than only aggregate annotator-style judgments.
- How much of observed downstream alignment quality is caused by post-training feedback source versus upstream pretraining-data filtering and deduplication.
- Whether human preference data should be treated as the target to optimize, or as a noisy signal that must be corrected for truthfulness, anti-sycophancy, and representational fairness.
- How much AI-generated content can filtered web pipelines tolerate before RefinedWeb/FineWeb-style gains disappear?
- Are the reported gains from filtered web corpora driven mainly by better filtering, by sheer scale, or by broader snapshot diversity?
- Will retrieval collapse eventually feed back into pretraining quality as future corpora depend more on search-mediated or already-polluted web content?
- How should strong benchmark performance from web corpora be weighed against documented consent and representational problems in those same corpora?
- No apples-to-apples experiment here holds model size and training recipe fixed while varying only post-training data composition and then evaluating on social benchmarks like SocialIQa, ToMi, false-belief variants, and pragmatic relevance.
- Several data-composition papers optimize generic alignment or chat preference metrics rather than social-reasoning metrics, so transfer remains unproven.
- CoSToM raises a live competing explanation that social deficits may be due to elicitation/control failures rather than missing socially grounded training data.
- Reasoning-oriented fine-tuning appears beneficial on some generic benchmarks but harmful on false-belief tasks, implying that 'better reasoning data' and 'better social reasoning' are not interchangeable.
- Synthetic or self-generated instruction data may improve instruction following while failing to encode the goal-sensitive, mental-state-rich structure needed for pragmatic social judgments.
- Whether DEL-ToM-style inference-time scaling still leaves large residual deficits on ALTPRAG, pragmatic relevance, and cross-cultural false-belief tasks.
- Whether CoSToM's 'latent ToM already exists' story survives controlled comparisons against targeted social training such as Social-R1.
- Whether authentic post-training data and inference-time scaling are additive, partially substitutable, or largely independent causes of social-reasoning gains.
- Whether benchmark ToM improvements from logic/verifier methods reflect true socially grounded competence or only better performance on structured task formats.
- Whether provenance-aware data collection improves exactly the failure modes that inference-time scaling does not fix, such as regional variance, false-belief errors, and pragmatic relevance judgments.