# Evidence Inventory by Beat

## Beat 1: Model Collapse and Contamination Risk

Keep the prose explicitly motivational: this beat raises risk and pressure conditions but is not the direct evidence base for the later primary post-training claim. Preserve the three-step chain: recursive reuse risk, partial contamination-pressure evidence, then detector fragility. After the Nature paper, insert an explicit sentence such as: 'Importantly, this literature mainly establishes failure under indiscriminate recursive reuse, not universal synthetic-data failure.' Use Self-Correcting Self-Consuming Loops and Curated Data as the in-set counterevidence, and note that an additional mixed real+synthetic non-collapse pathway (the pi^2/6 line) exists but is not represented in the supplied candidate set, so it should be acknowledged in prose as external counterevidence rather than omitted. When discussing category-B papers, say contamination is demonstrated in specific environments—science papers, new webpages, political images, MOOCs, selected news ecosystems, retrieval pools—not uniformly proven at web scale. When discussing category-C papers, avoid saying detection is impossible; say instead that detection is context-dependent, often evadable under paraphrase or distribution shift, and partly supplemented by watermarking or retrieval-based defenses.

- **Ilia Shumailov et al. 2023**
  Role: Opens the beat by establishing the core hazard: recursive training on model-generated outputs can erase rare modes and induce collapse.
  Finding: Training generative models on model-generated content causes irreversible Model Collapse where tails of the original distribution disappear.
- **Ilia Shumailov et al. 2024**
  Role: Anchor paper that crystallizes collapse risk as a serious motivation for worrying about self-reinforcing synthetic data loops.
  Finding: Indiscriminate use of model-generated content in training causes irreversible model collapse where tails of the original data distribution disappear.
- **Nate Gillman et al. 2024**
  Role: Provides the required scope-limiting turn: self-consuming loops can be stabilized under corrective conditions, so collapse is contingent rather than universal.
  Finding: Introducing an idealized correction function makes self-consuming generative training loops exponentially more stable against collapse.
- **Weixin Liang et al. 2025**
  Role: First bridge into contamination pressure, using a concrete domain-specific measurement of LLM-written or LLM-modified scientific text.
  Finding: Up to 22.5% of computer science papers showed LLM modification by September 2024, demonstrating academic text contamination at scale.
- **Hongyeon Yu et al. 2026**
  Role: Makes the contamination-pressure bridge more concrete by showing that retrieval systems can become overexposed to synthetic content even before complete pool saturation.
  Finding: 67% pool contamination with AI-generated content leads to over 80% exposure contamination in retrieval systems, creating a homogenized yet deceptively healthy state.
- **Damien Ferbach et al. 2024**
  Role: Supports Beat 1 via category A
  Finding: Data curation in self-consuming generative models can provably optimize human preferences and prevent model collapse under iterative retraining.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ The support is real but mostly controlled, recent, and fragmented. Much of A is image/medical or analytical, while B/C emphasize contamination detection and prevalence rather than downstream LM harm at web scale. This is enough to motivate urgency, not to serve as direct proof for post-training claims.

---

## Beat 2: Web Drift Is Partially Measurable, Broad Degradation Still Unproven

Keep the tone explicitly motivational. The argument should be: drift is partly measurable through proxies, visible in some longitudinal web subdomains, and consequential enough to motivate better crawl curation. Do not convert this into direct evidence for the paper's primary post-training claim. State plainly that the evidence here is partial and indirect: it does not prove web-wide pretraining degradation or contamination. Required counterevidence must be foregrounded, not buried: RefinedWeb and FineWeb show that carefully filtered web data still trains strong models. Use C4 to show that crawl artifacts are real, but not to claim a generalized contemporary failure mode. End with the explicit limitation that no post-2022 web-scale contamination audit exists in the corpus.

- **Yoon Mi Oh et al. 2022**
  Role: Establishes the measurement problem: corpus-level drift is often observed through proxy statistics, but those statistics vary in robustness to corpus size and content, so any drift signal must be treated as indirect.
  Finding: Traditional corpus-based complexity indices (TTR, word-level Entropy) are less robust to corpus size and content variation than newer indices (Word Information Density, Lexical Div
- **Ryan Amos et al. 2021**
  Role: Provides the first strong longitudinal observation: a million-document privacy-policy corpus showing that at least one major web genre changes measurably across decades and in response to regulation.
  Finding: A curated longitudinal dataset of over one million English privacy policies spanning two decades reveals how the privacy policy landscape changed in response to evolving regulation
- **Isabel Wagner et al. 2023**
  Role: Extends the privacy-policy line from collection to substantive content drift, showing measurable longitudinal shifts while still remaining domain-specific rather than web-wide.
  Finding: Privacy policies have evolved over 25 years with measurable content changes in response to regulations like GDPR and CCPA, though gaps remain in user rights.
- **Jesse Dodge et al. 2021**
  Role: Shifts from observing web change to documenting crawl artifacts, showing that a major pretraining corpus already contains unexpected content, benchmark leakage, and filtering distortions.
  Finding: The Colossal Clean Crawled Corpus (C4) contains significant unexpected content including machine-generated text and benchmark evaluation examples, and its blocklist filtering dispr
- **Guilherme Penedo et al. 2023**
  Role: Supplies required counterevidence: filtered, deduplicated web-only data can outperform curated corpora, so measurable crawl issues do not by themselves imply that web pretraining data has broadly degraded.
  Finding: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora like The Pile.
- **Sergei Koltcov et al. 2020**
  Role: Supports Beat 2 via category D
  Finding: The minimum of Renyi entropy coincides with the true number of topics in labelled collections, enabling principled analysis of regularization effects on topic models.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ This beat is only supported in its narrower form. The corpus can justify that drift and quality variation are measurable and that curation matters, but the D-H link is thin and the literature does not directly prove broad web-scale training-data degradation over time.

---

## Beat 3: L_auth as a Descriptive Framework, Not a Validated Law

Keep the prose definitional, not triumphalist. Present L_auth as a fine-tuning-focused descriptive synthesis with four dimensions: D1 Provenance Ratio and D4 Social Behavioral Diversity as design-level inputs; D2 Lexical Diversity and D3 Entropy as measurable emergent outcomes. Be explicit that evidence is strongest for D1->D2/D3 style relationships and much thinner for D4, which is only partially proxied here by genre, proficiency group, and source-language differences. Do not call L_auth a validated law, discovery, detector, or stage-agnostic framework. Say directly that pretraining operationalization remains future work, and that weight calibration across D1-D4 is also future work rather than something established by the cited literature.

- **Yoon Mi Oh et al. 2022**
  Role: Establishes the measurement philosophy for L_auth: lexical diversity and entropy-related indices are useful only when their robustness to corpus size and content is made explicit, which fits D2 and D3 as emergent outcomes rather than intrinsic constants.
  Finding: Traditional corpus-based complexity indices (TTR, word-level Entropy) are less robust to corpus size and content variation than newer indices (Word Information Density, Lexical Div
- **Pablo Rosillo-Rodes et al. 2025**
  Role: Provides the bridge between D2 and D3 by showing a functional relation between type-token behavior and word entropy across corpora, justifying why L_auth keeps them separate but coordinated.
  Finding: An empirical functional relation between word entropy and type-token ratio exists across corpora and languages, analytically derivable from Zipf's and Heaps' laws in the large-text
- **Yanzhu Guo et al. 2024**
  Role: Supplies that applied link: recursive training on synthetic text yields declines in lexical, syntactic, and semantic diversity, making diversity loss a concrete outcome signature of provenance changes.
  Finding: Recursively training language models on synthetic text produced by predecessors leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative
- **Ilia Shumailov et al. 2023**
  Role: Generalizes the outcome story into a provenance-ratio story: repeated training on generated data erases tail events, motivating D1 as a design-level input describing how much human-origin versus model-origin data is in the fine-tuning pool.
  Finding: Training generative models on model-generated content causes irreversible Model Collapse where tails of the original distribution disappear.
- **Nate Gillman et al. 2024**
  Role: Introduces the first explicit moderation claim in the spine: under an idealized correction function, self-consuming loops can be stabilized, implying that provenance effects depend on training design rather than expressing a universal law.
  Finding: Introducing an idealized correction function makes self-consuming generative training loops exponentially more stable against collapse.
- **Sergei Koltcov et al. 2020**
  Role: Supports Beat 3 via category D
  Finding: The minimum of Renyi entropy coincides with the true number of topics in labelled collections, enabling principled analysis of regularization effects on topic models.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ The framework is plausible, but the literature does not validate L_auth as a general law. Cross-category integration is weak, most papers are very recent, and there is little direct evidence that an authenticity variable behaves consistently across stages, scales, or domains.

---

## Beat 4: Provenance Matters Most on Socially Grounded Tasks; AI Feedback Still Helps on Bounded Tasks

Keep Beat 4 clearly separate from collapse literature. The defensible chain is: social reasoning is a real post-training weak spot; curated human data can be disproportionately high leverage; provenance changes socially meaningful outputs; and bounded-task counterevidence prevents any universal claim that human data always wins. The final sentence of the beat should explicitly narrow the thesis to socially grounded, norm-sensitive behavior rather than alignment overall.

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
- **Carl Orge Retzlaff et al. 2024**
  Role: Supports Beat 4 via category F
  Finding: Reinforcement learning is fundamentally a human-in-the-loop paradigm, and human-centric design is key to successful RL but has been insufficiently addressed.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ This is the strongest substantive line, but it still supports a narrower claim than the full thesis. F-J is the best-connected primary-evidence cluster, yet the corpus does not cleanly isolate provenance from other factors such as task design, annotation quality, or model family. The AI-feedback side is better supported on bounded tasks than on open-ended social grounding.

---

## Beat 5: Pilot Experiment at Fixed Inference-Time Compute Gives Directional, Not Definitive, Support

Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

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
- **Carl Orge Retzlaff et al. 2024**
  Role: Supports Beat 5 via category F
  Finding: Reinforcement learning is fundamentally a human-in-the-loop paradigm, and human-centric design is key to successful RL but has been insufficiently addressed.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ The corpus can make the pilot plausible, but it cannot strongly validate it. There is little direct literature matching the exact design: fixed inference-time compute, provenance-controlled fine-tuning data, and socially grounded evaluation. Because K is sparse, alternative explanations from test-time compute are not well bounded.

---

## Beat 6: CampusGo as Deployed Provenance-Aware Collection Platform

Beat 6 should read as deployed requirements engineering, not downstream validation. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a deployed system would need to satisfy.

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
- **Caren B. Cooper et al. 2021**
  Role: Supports Beat 6 via category G
  Finding: Stewarding volunteer-generated citizen science data requires ethical decisions about power, attribution, access, and data governance beyond standard technical considerations.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ The corpus is sufficient to support buildability and deployment value, not downstream model gains. G has credible implementation precedent, but the graph is weakly connected to the primary-evidence clusters, so CampusGo should be presented as an operational contribution rather than proof of training efficacy.

---

## Beat 7: Competing Explanations and Honest Scoping

Write this beat as a concessionary scope paragraph, not as a rebuttal section. State early that inference-time scaling is a real alternative, and use DEL-ToM as the sharpest reason to narrow the claim. Treat the SymbCoT and Relevant answers pairs as duplicate venue/preprint trails rather than independent evidence bursts. End explicitly on the boundary: the contribution, if maintained, is about data-composition effects under fixed model size and test-time budget, not about universally explaining or maximizing social reasoning.

- **Xuezhi Wang et al. 2022**
  Role: Establishes the first serious competing mechanism: test-time compute can raise reasoning quality by aggregating multiple sampled chains, even when training data stay fixed.
  Finding: Self-consistency decoding, which marginalizes over diverse sampled reasoning paths, substantially boosts chain-of-thought prompting performance on arithmetic and commonsense reason
- **Jundong Xu et al. 2024**
  Role: Moves from generic self-consistency to structured chain-of-thought, showing that symbolic scaffolding can improve reasoning beyond standard CoT.
  Finding: SymbCoT, integrating symbolic expressions and logic rules with chain-of-thought prompting, consistently and significantly outperforms standard CoT on logical reasoning benchmarks.
- **Yuheng Wu et al. 2025**
  Role: Provides the strongest direct alternative for this beat by demonstrating Theory-of-Mind gains from verifier-guided inference-time scaling alone, including on smaller models.
  Finding: DEL-ToM improves Theory-of-Mind reasoning in small language models through inference-time scaling using a Dynamic Epistemic Logic-grounded verifier rather than architectural change
- **Kefan Yu et al. 2025**
  Role: Broadens the alternative set beyond test-time compute by showing that pragmatic competence changes across pre-training, SFT, and preference-optimization stages.
  Finding: Pre-training, SFT, and preference optimization stages differentially affect pragmatic competence in LLMs, as measured by the ALTPRAG benchmark across 22 models.
- **Jincenzi Wu et al. 2026**
  Role: Closes the main thread with social-reasoning-specific optimization evidence, indicating that process rewards and adversarial training can improve behavior without appealing to the focal data-composition story.
  Finding: Reinforcement learning with multi-dimensional process rewards on adversarially hard social reasoning examples yields more human-like social intelligence in LLMs than outcome-based 
- **Jundong Xu et al. 2024**
  Role: Supports Beat 7 via category K
  Finding: SymbCoT, integrating symbolic expressions and logic rules with chain-of-thought prompting, consistently and significantly outperforms standard CoT on logical reasoning benchmarks.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: evidence inventory must contain exactly 7 beats, got 3; 'suggested_paper_outline' must be a non-empty object
  ⚠ This is the most under-covered beat. K is small, recent, and only lightly integrated with the rest of the graph. That is enough to require honest scoping, but not enough to convincingly apportion causal weight among data composition, chain-of-thought, model scale, and test-time compute.

---

## Suggested Paper Structure

- section_1_model_collapse_and_contamination_risk: ~6 papers, TBD pages
- section_2_partial_measurability_of_web_drift: ~6 papers, TBD pages
- section_3_l_auth_framework_definition: ~6 papers, TBD pages
- section_4_fine-tuning_data_source_affects_social_reasoning: ~6 papers, TBD pages
- section_5_contrastive_fine-tuning_experiment: ~6 papers, TBD pages
- section_6_campusgo_as_deployed_core_contribution: ~6 papers, TBD pages
- section_7_competing_explanations_and_honest_scoping: ~6 papers, TBD pages