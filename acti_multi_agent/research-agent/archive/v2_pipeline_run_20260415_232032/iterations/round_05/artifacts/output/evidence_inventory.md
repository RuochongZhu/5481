# Evidence Inventory by Beat

## Beat 1: Model Collapse and Contamination Risk

The motivation chain starts with formal and empirical work showing that recursive self-training can collapse generative models or make them forget. It is then narrowed by mitigation papers showing that curation and correction matter, which prevents overclaiming. Domain-specific contamination studies show that the harm is not merely theoretical: synthetic contamination can remove rare but important signal and degrade reasoning. Finally, prevalence papers make the risk operationally relevant by showing that AI-generated content is already entering training corpora.

- **Use as the lead citation for the claim that self-consumption is a real failure mode, not just a metaphor.**
  Role: anchor theory-and-evidence paper
  Finding: Establishes that recursive training on model-generated data can progressively destroy rare-event support and induce collapse.
- **Important because it moves the collapse argument closer to text and LMs rather than only abstract or image settings.**
  Role: LM-specific corroboration
  Finding: Shows that repeated retraining on generated text causes forgetting and degradation in language models.
- **Cite to avoid overstating inevitability; the risk is serious but conditional on curation and loop design.**
  Role: boundary-condition paper
  Finding: Demonstrates that quality controls and correction loops can mitigate some recursive-training harms.
- **Useful for the narrower claim that synthetic data is not uniformly bad; uncurated self-consumption is the concern.**
  Role: qualified counterexample
  Finding: Shows that synthetic data can help when it is curated, bounded, and combined with an appropriate training strategy.
- **Supports the claim that contamination can damage downstream reasoning, not just distributional aesthetics.**
  Role: domain-harm exemplar
  Finding: Finds that contamination with synthetic data can erase clinically important variability and harm diagnostic reasoning in a high-stakes domain.
- **Lower-weight than the core collapse papers, but useful for showing that contamination harms extend beyond benchmark settings.**
  Role: cross-domain motivation paper
  Finding: Shows that synthetic media contamination can distort evidence ecosystems and decision-making outside core ML benchmarks.

Remaining gaps:
  ⚠ No paper in the current corpus directly proves web-scale downstream LM collapse from naturally accumulating AI text over long time horizons.
  ⚠ Collapse thresholds, contamination rates, and real-world exposure levels remain weakly quantified.
  ⚠ Most evidence is recent and fragmented across modalities and domains, so this beat should motivate urgency rather than serve as direct proof for later experimental claims.
  ⚠ The support is real but mostly controlled, recent, and fragmented. Much of A is image/medical or analytical, while B/C emphasize contamination detection and prevalence rather than downstream LM harm at web scale. This is enough to motivate urgency, not to serve as direct proof for post-training claims.

---

## Beat 2: Web Drift Is Partially Measurable, Broad Degradation Still Unproven

This beat should argue something narrower than 'the web is collapsing.' RefinedWeb-style work establishes that web data quality varies and that curation choices matter for LLM training. Authenticity-measurement papers show that at least some aspects of drift are observable, and prevalence papers suggest that AI-generated content is part of that drift. The combined literature therefore supports a measurable-drift claim, but not a strong claim that web-scale degradation is already broad, monotonic, or causally linked to downstream LLM decline everywhere.

- **Yanzhu Guo et al. 2024**
  Role: Opens with the strongest available proxy-style evidence from category D: synthetic-text recursion can measurably reduce lexical, syntactic, and semantic diversity, motivating concern that drift may be detectable through distributional proxies while also remaining a laboratory result rather than a web audit.
  Finding: Recursively training language models on synthetic text produced by predecessors leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative
- **Ryan Amos et al. 2021**
  Role: Introduces a concrete longitudinal web dataset: a million privacy policies curated across two decades, establishing that some web domains can be tracked over time with explicit temporal structure.
  Finding: A curated longitudinal dataset of over one million English privacy policies spanning two decades reveals how the privacy policy landscape changed in response to evolving regulation
- **Isabel Wagner et al. 2023**
  Role: Provides the main observational claim for this beat: privacy-policy content changed measurably from 1996-2021 in response to regulatory and institutional shifts, showing real drift in a large but genre-specific slice of the web.
  Finding: Privacy policies have evolved over 25 years with measurable content changes in response to regulations like GDPR and CCPA, though gaps remain in user rights.
- **Jesse Dodge et al. 2021**
  Role: Shifts to crawl-curation practice by showing that C4 contains unexpected content and benchmark leakage artifacts, making web drift and contamination risk operationally visible at corpus-construction time rather than only through abstract proxies.
  Finding: The Colossal Clean Crawled Corpus (C4) contains significant unexpected content including machine-generated text and benchmark evaluation examples, and its blocklist filtering dispr
- **Guilherme Penedo et al. 2023**
  Role: Supplies required counterevidence: RefinedWeb argues that web data, when aggressively filtered and deduplicated, can outperform curated corpora, so measurable artifacts in raw crawls do not by themselves show that web pretraining has failed.
  Finding: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora like The Pile.

Remaining gaps:
  ⚠ The corpus lacks a definitive longitudinal study linking measured web contamination directly to downstream LLM quality changes at scale.
  ⚠ Detector-based prevalence estimates remain noisy and sensitive to false positives, false negatives, and domain shift.
  ⚠ The D-to-H link is still indirect: measurability is stronger than causal proof of broad degradation.
  ⚠ This beat is only supported in its narrower form. The corpus can justify that drift and quality variation are measurable and that curation matters, but the D-H link is thin and the literature does not directly prove broad web-scale training-data degradation over time.

---

## Beat 3: L_auth as a Descriptive Framework, Not a Validated Law

The framework beat should present L_auth as a useful descriptive variable: as the share or influence of authentic human-origin signal falls, models may face higher risk of distortion or collapse. A-papers justify the mechanism, D-papers justify approximate measurement, and H-papers justify the importance of corpus-quality proxies. But constructive self-consuming papers make clear that L_auth is not a validated natural law; synthetic data can help under curation, correction, and targeted objectives. The framework is therefore best presented as an organizing lens for empirical work, not as a settled equation of model performance.

- **Use to motivate why an authenticity-share variable is conceptually sensible.**
  Role: mechanistic foundation
  Finding: Supplies the core intuition that reduced access to authentic generative support can drive collapse.
- **Important for mapping the framework from abstract generative models onto language settings.**
  Role: LM-oriented mechanism paper
  Finding: Shows language-model forgetting under recursive generated-data exposure.
- **This is key for framing L_auth as descriptive rather than universal or deterministic.**
  Role: non-law boundary paper
  Finding: Shows that recursive loops can be stabilized or improved under controlled correction schemes.
- **Use to show that authenticity is not the only relevant variable; curation and objective alignment also matter.**
  Role: qualified constructive paper
  Finding: Proves that self-consuming pipelines can remain beneficial when synthetic data is curated toward a target objective.
- **Yanzhu Guo et al. 2024**
  Role: Provides the text-facing bridge from D1 inputs to D2 outcomes by showing lexical, syntactic, and semantic diversity decline under recursive synthetic training, especially on creative tasks.
  Finding: Recursively training language models on synthetic text produced by predecessors leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative

Remaining gaps:
  ⚠ No paper in the corpus validates a single L_auth metric against downstream performance across multiple domains and model families.
  ⚠ The framework still lacks agreed operationalization: authenticity share, provenance confidence, novelty, and curation quality may all matter separately.
  ⚠ Current evidence does not establish stable thresholds or a law-like functional form.
  ⚠ The framework is plausible, but the literature does not validate L_auth as a general law. Cross-category integration is weak, most papers are very recent, and there is little direct evidence that an authenticity variable behaves consistently across stages, scales, or domains.

---

## Beat 4: Primary Social Reasoning Is the Relevant Capability Target

This beat should establish why social reasoning, rather than generic factual QA, is the capability that matters for the paper's primary setting. F-papers define the problem: users ask underspecified questions inside social contexts, so effective systems must infer intent, norms, and situational constraints. I-papers then show that context-aware and adaptive interventions can improve such interactions. J-papers provide the evaluation vocabulary needed to test these claims with human-centered measures. Together, these papers justify the problem framing and the choice of outcomes for the primary study.

- **Maarten Sap et al. 2022**
  Role: Establishes why social reasoning is the right downstream target: even strong LLMs lag on mental-state and norm-sensitive tasks, so this capability cannot be assumed from pretraining alone.
  Finding: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on SocialIQa and ToMi benchmarks.
- **Chunting Zhou et al. 2023**
  Role: Anchor paper for Beat 4: LIMA shows that a small, carefully curated human-authored set can drive large alignment gains, making data provenance a high-leverage post-training variable.
  Finding: Fine-tuning a 65B LLM on only 1,000 carefully curated examples without reinforcement learning achieves performance comparable or preferred to GPT-4 in 43% of cases.
- **Shibani Santurkar et al. 2023**
  Role: Shows that post-training data source changes socially meaningful outputs, not just generic helpfulness: instruction tuning shifts whose opinions the model appears to reflect.
  Finding: Current LMs exhibit substantial misalignment with US demographic groups' opinions, on par with the Democrat-Republican divide on climate change, even after demographic steering.
- **Rafael Rafailov et al. 2023**
  Role: Provides the clean methodological hinge: DPO simplifies preference optimization so feedback-source comparisons become more interpretable than full RLHF stacks.
  Finding: RLHF can be reformulated as a simple classification loss by reparameterizing the reward model, enabling direct policy optimization without reinforcement learning.
- **Harrison Lee et al. 2023**
  Role: Provides required counterevidence: AI feedback can match RLHF on bounded dialogue and summarization tasks, so the claim must stay narrower than universal human-data superiority.
  Finding: RLAIF achieves comparable performance to RLHF across summarization and dialogue tasks, and direct-RLAIF outperforms canonical RLAIF by obtaining rewards directly from an LLM.

Remaining gaps:
  ⚠ The excerpted corpus does not yet show whether social-reasoning gains transfer across institutions, cultures, or accessibility needs.
  ⚠ Existing benchmarks may undercapture long-horizon usefulness and real-world consequences of socially poor guidance.
  ⚠ The literature may still blur social reasoning with better prompting or better retrieval unless experiments isolate those mechanisms.
  ⚠ This is the strongest substantive line, but it still supports a narrower claim than the full thesis. F-J is the best-connected primary-evidence cluster, yet the corpus does not cleanly isolate provenance from other factors such as task design, annotation quality, or model family. The AI-feedback side is better supported on bounded tasks than on open-ended social grounding.

---

## Beat 5: Primary Experiment Should Isolate Social Reasoning from Retrieval and Interface Effects

The experiment beat should not merely claim that a new system performs better; it should show what mechanism is being tested. F-papers justify why social reasoning should affect action selection. I-papers provide precedents for designing interventions and ablations that distinguish reasoning from retrieval, prompting, or interface polish. J-papers define rigorous outcome measures, including blinded human evaluation, multi-turn behavior metrics, and subgroup robustness checks. This produces an evidence base for an experiment that isolates the paper's central causal claim rather than just reporting aggregate win rates.

- **Maarten Sap et al. 2019**
  Role: Establishes Social IQa as a demanding evaluation target, which is why the pilot uses social reasoning rather than only generic chat benchmarks.
  Finding: Social IQa provides a large-scale benchmark for evaluating commonsense reasoning about people's actions, intents, and reactions in social interactions.
- **Chunting Zhou et al. 2023**
  Role: Anchor paper for Beat 5: LIMA is the clearest precedent that data quality and curation can matter enough to justify a provenance-sensitive fine-tuning contrast.
  Finding: Fine-tuning a 65B LLM on only 1,000 carefully curated examples without reinforcement learning achieves performance comparable or preferred to GPT-4 in 43% of cases.
- **Rafael Rafailov et al. 2023**
  Role: Defines the pilot's methodological hinge: DPO keeps the optimization recipe simple enough that differences between data conditions remain interpretable.
  Finding: RLHF can be reformulated as a simple classification loss by reparameterizing the reward model, enabling direct policy optimization without reinforcement learning.
- **Lewis Tunstall et al. 2023**
  Role: Provides the strongest competitive synthetic baseline: AI-feedback distillation can produce strong chat alignment, which is why the pilot must be framed as a directional test rather than a foregone human-data victory.
  Finding: Distilled direct preference optimization from AI feedback enables a 7B model (Zephyr-7B) to surpass Llama2-Chat-70B on MT-Bench without human annotation.
- **Maarten Sap et al. 2022**
  Role: Broader theory-of-mind benchmark evidence showing that social reasoning deficits persist in strong LLMs.
  Finding: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on SocialIQa and ToMi benchmarks.

Remaining gaps:
  ⚠ A large randomized field trial may still be missing from the corpus.
  ⚠ Longitudinal outcomes such as sustained trust, learning, or behavioral change are likely undermeasured.
  ⚠ There may be limited prior work on how to cleanly separate social reasoning from hidden product-quality improvements such as UI or latency.
  ⚠ The corpus can make the pilot plausible, but it cannot strongly validate it. There is little direct literature matching the exact design: fixed inference-time compute, provenance-controlled fine-tuning data, and socially grounded evaluation. Because K is sparse, alternative explanations from test-time compute are not well bounded.

---

## Beat 6: CampusGo as the Instrumented Infrastructure Contribution

Beat 6 should inventory the system contribution as infrastructure: a deployable, instrumented, governance-aware platform that can support real use and later experimentation. The G-papers justify architecture, logging, integration, safety, and operations. This is enough to support claims about buildability, deployability, and research-enablement. It is not enough, by itself, to validate downstream user impact or generalized performance gains, so the beat should remain explicitly infrastructural.

- **N. Eagle et al. 2006**
  Role: Provides the broad feasibility precedent: mobile sensing can capture rich human behavioral traces over time.
  Finding: Mobile phone sensing data can reveal complex social system patterns through large-scale behavioral observation.
- **Rui Wang et al. 2014**
  Role: Narrows that feasibility claim into the university setting by showing that continuous smartphone sensing can characterize student behavior in a campus environment.
  Finding: Smartphone sensing can continuously assess college students' mental health, academic performance, and behavioral trends in naturalistic settings.
- **Shayne Longpre et al. 2024**
  Role: Anchor paper for Beat 6: AI data authenticity, consent, and provenance are currently fragmented, so a deployed CampusGo-style collection platform needs these requirements baked in from the start.
  Finding: Data authenticity verification, consent tracking, and provenance preservation are systemically broken in current AI training pipelines, with ~5% of C4 tokens and 45% of content res
- **Neha Gupta et al. 2023**
  Role: Adds the stewardship boundary: contributors must remain stakeholders in how sensitive data are curated and reused, which keeps CampusGo deployed-but-scoped rather than extractive or overclaimed.
  Finding: The CARE principles provide a framework for Indigenous data governance that redresses hidden costs borne by Indigenous communities in archaeological data sharing and reuse.
- **Anne Bowser et al. 2020**
  Role: Structured Beat 6 spine paper.
  Finding: Citizen science projects perform well on data quality and governance but lack open data access, documentation, interoperability, and long-term preservation practices.

Remaining gaps:
  ⚠ Infrastructure papers do not by themselves establish improved user outcomes or superior reasoning quality.
  ⚠ The corpus may not include long-term deployment evidence across multiple semesters or campuses.
  ⚠ Operational feasibility is stronger than causal evidence of educational, navigational, or accessibility benefit.
  ⚠ The corpus is sufficient to support buildability and deployment value, not downstream model gains. G has credible implementation precedent, but the graph is weakly connected to the primary-evidence clusters, so CampusGo should be presented as an operational contribution rather than proof of training efficacy.

---

## Beat 7: Competing Mechanisms That Could Also Explain Observed Gains

The adversarial beat should map the strongest competing mechanisms that could explain any observed gains: fresher data, better domain match, benchmark leakage, tool access, interface quality, user selection, and pipeline curation. The purpose is not to dismiss these alternatives but to show that they are credible and should shape the experimental design. A strong paper will explicitly compare against these possibilities, or at minimum delimit which ones are ruled out and which remain plausible.

- **Xuezhi Wang et al. 2022**
  Role: Start by conceding the strongest general alternative: more test-time compute via self-consistency materially improves reasoning without changing training data or model architecture.
  Finding: Self-consistency decoding, which marginalizes over diverse sampled reasoning paths, substantially boosts chain-of-thought prompting performance on arithmetic and commonsense reason
- **Jundong Xu et al. 2024**
  Role: Extend the inference-time alternative from generic search to structured chain-of-thought: symbolic scaffolds can outperform standard CoT, so reasoning format itself is a live competing mechanism.
  Finding: SymbCoT, integrating symbolic expressions and logic rules with chain-of-thought prompting, consistently and significantly outperforms standard CoT on logical reasoning benchmarks.
- **Yuheng Wu et al. 2025**
  Role: Use the most on-point scope limiter: DEL-ToM reports theory-of-mind gains from inference-time scaling with a logic-grounded verifier, directly showing that social reasoning can improve without architecture changes.
  Finding: DEL-ToM improves Theory-of-Mind reasoning in small language models through inference-time scaling using a Dynamic Epistemic Logic-grounded verifier rather than architectural change
- **Kefan Yu et al. 2025**
  Role: Broaden the scope boundary beyond test-time compute: pragmatic competence varies across pre-training, SFT, and preference optimization, so model behavior also depends on training pipeline and model family.
  Finding: Pre-training, SFT, and preference optimization stages differentially affect pragmatic competence in LLMs, as measured by the ALTPRAG benchmark across 22 models.
- **Jincenzi Wu et al. 2026**
  Role: Show that specialized supervision can itself drive social-reasoning gains: process-reward RL on difficult social examples improves behavior, competing directly with explanations framed only in terms of corpus composition.
  Finding: Reinforcement learning with multi-dimensional process rewards on adversarially hard social reasoning examples yields more human-like social intelligence in LLMs than outcome-based 

Remaining gaps:
  ⚠ The current corpus excerpt does not indicate which competing mechanisms have already been experimentally excluded.
  ⚠ Some alternatives may interact, making single-factor adjudication difficult.
  ⚠ Without strong baselines and controls, attribution to social reasoning or authenticity effects will remain contestable.
  ⚠ This is the most under-covered beat. K is small, recent, and only lightly integrated with the rest of the graph. That is enough to require honest scoping, but not enough to convincingly apportion causal weight among data composition, chain-of-thought, model scale, and test-time compute.

---

## Suggested Paper Structure

- section_1_motivation_collapse: ~6 papers, 2-3 pages
- section_2_motivation_web_drift: ~5 papers, 2-3 pages
- section_3_framework_lauth: ~5 papers, 2-3 pages
- section_4_fine-tuning_data_source_affects_social_reasoning: ~5 papers, TBD pages
- section_5_contrastive_fine-tuning_experiment: ~5 papers, TBD pages
- section_6_campusgo_as_deployed_core_contribution: ~5 papers, TBD pages
- section_7_competing_explanations_and_honest_scoping: ~5 papers, TBD pages