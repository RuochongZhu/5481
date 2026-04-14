# Evidence Inventory by Beat

## Beat 1: Model Collapse and Contamination Risk

Keep the beat explicitly three-step: collapse risk -> tentative contamination-pressure evidence -> reactive filtering limits. Make the scope admission unavoidable before any category-B bridge: the literature strongly supports risk from indiscriminate recursive reuse, not the claim that all synthetic data is harmful. Name the counterevidence directly: pi^2/6 mixed real+synthetic pathway, self-correcting loops, and curated synthetic-data regimes. For category B, use cautious language such as 'emerging', 'domain-specific', and 'not yet universal proof'; avoid saying the web is definitively contaminated at training-relevant scale. For category C, avoid saying detection is impossible; the stronger claim is that watermarking and other detectors are fragile under paraphrase or low-effort manipulation, even if retrieval or provenance-aware defenses can still help in narrower settings. Do not import any fine-tuning evidence from categories F, I, or J.

- **Ilia Shumailov et al. 2023**
  Role: Introduces the core collapse mechanism: recursive training on generated data makes models forget low-probability regions of the original distribution.
  Finding: Training on model-generated content causes irreversible model collapse where tails of the original content distribution disappear across multiple model families.
- **Josue Casco-Rodriguez et al. 2023**
  Role: Extends the collapse story into the go-MAD framework, specifying that insufficient fresh real data leads to quality or diversity degradation across generations.
  Finding: Without enough fresh real data in each generation, self-consuming generative models are doomed to Model Autophagy Disorder (MAD), losing quality or diversity.
- **Ilia Shumailov et al. 2024**
  Role: Serves as the beat's anchor by establishing collapse under recursively generated training data and foregrounding irreversible tail loss as the central failure mode.
  Finding: Indiscriminate use of model-generated content in training causes irreversible model collapse where tails of the original content distribution disappear across successive generation
- **Apratim Dey et al. 2024**
  Role: Provides the required counterpoint: mixed real-plus-synthetic training can avoid collapse, so the evidence supports a narrower warning about unmanaged recursive reuse rather than a blanket rejection of synthetic data.
  Finding: Augmenting real data with synthetic data across generations universally preserves a statistical efficiency of π²/6 relative to using only real data, avoiding model collapse.
- **Weixin Liang et al. 2025**
  Role: Offers one of the strongest domain-specific measurements of contamination pressure by quantifying LLM usage in scientific writing, while still falling short of proving universal web-scale contamination.
  Finding: Up to 22.5% of computer science papers showed LLM modification by September 2024, demonstrating academic text contamination at population scale.
- **Elvis Dohmatob et al. 2024**
  Role: Supports Beat 1 via category A
  Finding: Even as little as 1% synthetic data in the training corpus causes strong model collapse where increasing training set size no longer improves performance.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: 'suggested_paper_outline' must be a non-empty object
  ⚠ The corpus strongly supports that recursive synthetic reuse can cause collapse and that contamination risk is rising, but it only supports a cautious mitigation claim: collapse is avoidable in mixed or curated regimes, and the practical thresholds for web-scale failure remain unresolved.

---

## Beat 2: Web Drift and Limits of Reactive Filtering

Keep the claim explicitly narrow. This beat is about partial measurability of drift, not demonstrated web-wide contamination or failure. State plainly that no post-2022 web-scale contamination audit exists in the corpus. Use the D-category papers only to motivate why proxies are fragile and indirect. Then pivot to H-category longitudinal studies as the strongest direct evidence of change over time, especially the privacy-policy line and web-evolution archive work. In the final paragraph, juxtapose risk signals (C4 artifacts, shrinking data commons, Wikipedia AI-content growth) with required counterevidence (RefinedWeb and FineWeb), so the conclusion is: drift and curation pressure are measurable in parts, risk is rising, but filtered web corpora still produce strong models and the literature here does not prove web-wide pretraining degradation.

- **Yoon Mi Oh et al. 2022**
  Role: Establishes the measurement caution: corpus-level diversity or complexity signals can be tracked, but metric choice is sensitive to sampling and corpus size, so any drift claim should begin with bounded proxies rather than sweeping web-wide conclusions.
  Finding: Traditional corpus-based complexity indices (Type-Token Ratio, word-level Entropy) are more prone to fluctuation with corpus size changes than newer indices (Word Information Densi
- **Ryan Amos et al. 2021**
  Role: Provides a concrete long-span web measurement case by curating a million-document privacy-policy corpus and showing systematic temporal drift in length, readability, and ambiguity.
  Finding: Privacy policies are becoming longer, harder to read, and more ambiguous over time, while severely underreporting usage of third parties and tracking technologies.
- **Isabel Wagner et al. 2023**
  Role: Strengthens the longitudinal evidence with a 1996-2021 content analysis showing increasing use of location data, implicit collection, limited user choice, and growing third-party sharing; this is the beat's anchor example of measurable web drift.
  Finding: Despite GDPR and CCPA, privacy policies show increasing use of location data, implicit data collection, lack of meaningful choice, and growing data sharing with unnamed third parti
- **Vibhor Agarwal et al. 2022**
  Role: Widens the frame from one document genre to 25+ years of web evolution, showing shifts in dominant site types and platform composition across the web archive.
  Finding: Over 25+ years, web content has shifted from news and education-related websites toward streaming media and social networking sites, with major changes in dominant platforms.
- **Guilherme Penedo et al. 2023**
  Role: Supplies the required counterevidence: with careful filtering and deduplication, web-only data can still train strong LLMs, so observed drift is not decisive proof that web corpora are already unusable.
  Finding: Properly filtered and deduplicated web data alone can produce LLMs that significantly outperform models trained on curated high-quality corpora.
- **Sergei Koltcov et al. 2020**
  Role: Supports Beat 2 via category D
  Finding: The minimum of Renyi entropy coincides with the true number of topics in labelled collections, providing a principled way to analyze regularization effects on topic models.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: 'suggested_paper_outline' must be a non-empty object
  ⚠ Support is partial, which is acceptable for this beat. The corpus can support that drift is measurable through proxies and that filtering/curation can still yield strong web corpora, but it cannot support a strong causal claim that post-2022 AI content has already contaminated the web at model-relevant scale. Category H is small, D-H linkage is sparse, and B/C literature still leaves prevalence thresholds and downstream effects open.

---

## Beat 3: L_auth as a Stage-Agnostic Descriptive Framework

Frame L_auth as a stage-agnostic descriptive synthesis, not a discovered law. Make the architecture explicit: D1 Provenance Ratio and D4 Social Behavioral Diversity are upstream design-level inputs; D2 Lexical Diversity and D3 Entropy are downstream measurable outcomes. The strongest evidence chain in the selected papers is D1 to D2/D3, especially via The Curious Decline of Linguistic Diversity. The evidence base for D4 is materially thinner and more conceptual, so say that openly rather than overstating it. Do not describe L_auth as a detection tool. Also note that D2 and D3 are related rather than fully independent, with the entropy-TTR paper implying possible redundancy; this is exactly why weight calibration should be stated as future work rather than implied to be solved already.

- **Ilia Shumailov et al. 2023**
  Role: Establishes the provenance-side motivation for D1 by showing that recursive training on generated data removes tail support and reduces diversity across generations.
  Finding: Training on model-generated content causes irreversible model collapse where tails of the original content distribution disappear across multiple model families.
- **Yanzhu Guo et al. 2024**
  Role: Provides the main empirical bridge from provenance to outcomes by showing that synthetic retraining is accompanied by declines in lexical, syntactic, and semantic diversity.
  Finding: Recursively training language models on synthetic text generated by predecessors causes consistent decreases in lexical, syntactic, and semantic diversity of outputs.
- **Yoon Mi Oh et al. 2022**
  Role: Grounds D2 metric choice by showing that common corpus complexity measures vary in robustness, motivating careful use of lexical-diversity indicators rather than naive reliance on raw TTR-style counts.
  Finding: Traditional corpus-based complexity indices (Type-Token Ratio, word-level Entropy) are more prone to fluctuation with corpus size changes than newer indices (Word Information Densi
- **Sergei Koltcov et al. 2020**
  Role: Supports D3 by treating Renyi entropy as an informative structural statistic, showing that entropy can track meaningful organization changes even if the setting is topic modeling rather than language-model pretraining.
  Finding: The minimum of Renyi entropy coincides with the true number of topics in labelled collections, providing a principled way to analyze regularization effects on topic models.
- **Pablo Rosillo-Rodes et al. 2025**
  Role: Links D2 and D3 by showing a consistent empirical and analytic relation between word entropy and type-token ratio, supporting their joint inclusion while also signaling potential overlap and the need for future calibration.
  Finding: There exists a consistent empirical functional relation between word entropy and type-token ratio across gigaword corpora, analytically derivable from Zipf's and Heaps' laws in the
- **Sergei Koltcov et al. 2020**
  Role: Supports Beat 3 via category D
  Finding: Topic model outputs exhibit self-similar behavior under cluster number variation, enabling renormalization-based optimization of topic count selection.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: 'suggested_paper_outline' must be a non-empty object
  ⚠ The bridge is conceptually defensible but not empirically validated as a law. D has enough material to motivate measurable ingredients, and A/E/I give a rationale for provenance, diversity, and entropy-like dimensions, but the corpus does not yet show that the four dimensions form a validated, predictive, stage-agnostic metric system.

---

## Beat 4: Social Reasoning and Data Provenance

Keep Beat 4 clearly separate from collapse literature. The defensible chain is: social reasoning is a real post-training weak spot; curated human data can be disproportionately high leverage; provenance changes socially meaningful outputs; and bounded-task counterevidence prevents any universal claim that human data always wins. The final sentence of the beat should explicitly narrow the thesis to socially grounded, norm-sensitive behavior rather than alignment overall.

- **Maarten Sap et al. 2022**
  Role: Establishes why social reasoning is the right downstream target: even strong LLMs lag on mental-state and norm-sensitive tasks, so this capability cannot be assumed from pretraining alone.
  Finding: Out-of-the-box GPT-3 models lag behind humans by over 30% on social intelligence benchmarks and struggle with mental state reasoning compared to factual questions.
- **Chunting Zhou et al. 2023**
  Role: Anchor paper for Beat 4: LIMA shows that a small, carefully curated human-authored set can drive large alignment gains, making data provenance a high-leverage post-training variable.
  Finding: Fine-tuning a 65B LLaMA model on only 1,000 carefully curated examples without RLHF produces competitive performance with state-of-the-art models, supporting the Superficial Alignm
- **Shibani Santurkar et al. 2023**
  Role: Shows that post-training data source changes socially meaningful outputs, not just generic helpfulness: instruction tuning shifts whose opinions the model appears to reflect.
  Finding: Language models exhibit substantial misalignment with US demographic groups' opinions, and instruct-tuning distorts opinion distributions with consistent biases toward liberal view
- **Rafael Rafailov et al. 2023**
  Role: Provides the clean methodological hinge: DPO simplifies preference optimization so feedback-source comparisons become more interpretable than full RLHF stacks.
  Finding: Direct Preference Optimization enables training language models from human preferences with a simple cross-entropy loss, matching or exceeding RLHF without reinforcement learning.
- **Harrison Lee et al. 2023**
  Role: Provides required counterevidence: AI feedback can match RLHF on bounded dialogue and summarization tasks, so the claim must stay narrower than universal human-data superiority.
  Finding: RLAIF achieves comparable performance to RLHF across summarization and dialogue tasks, and can enable LLM self-improvement even when the AI labeler is the same model as the policy.
- **Carl Orge Retzlaff et al. 2024**
  Role: Supports Beat 4 via category F
  Finding: Reinforcement learning is fundamentally a human-in-the-loop paradigm requiring human-centric approaches for successful deployment.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: 'suggested_paper_outline' must be a non-empty object
  ⚠ This beat can support only the narrower claim. The F/I/J evidence base is large enough to argue that provenance and behavioral diversity matter for socially grounded fine-tuning, but not that human data is always superior. The crucial exemplars named in the target argument line are not verifiable from the supplied metadata, so the corpus presently supports a cautious version better than a headline claim.

---

## Beat 5: Contrastive Fine-Tuning Experiment

Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

- **Maarten Sap et al. 2019**
  Role: Establishes Social IQa as a demanding evaluation target, which is why the pilot uses social reasoning rather than only generic chat benchmarks.
  Finding: Large pretrained language models achieve only up to 65% accuracy on Social IQA compared to nearly 90% human performance, showing social commonsense reasoning remains challenging fo
- **Chunting Zhou et al. 2023**
  Role: Anchor paper for Beat 5: LIMA is the clearest precedent that data quality and curation can matter enough to justify a provenance-sensitive fine-tuning contrast.
  Finding: Fine-tuning a 65B LLaMA model on only 1,000 carefully curated examples without RLHF produces competitive performance with state-of-the-art models, supporting the Superficial Alignm
- **Rafael Rafailov et al. 2023**
  Role: Defines the pilot's methodological hinge: DPO keeps the optimization recipe simple enough that differences between data conditions remain interpretable.
  Finding: Direct Preference Optimization enables training language models from human preferences with a simple cross-entropy loss, matching or exceeding RLHF without reinforcement learning.
- **Lewis Tunstall et al. 2023**
  Role: Provides the strongest competitive synthetic baseline: AI-feedback distillation can produce strong chat alignment, which is why the pilot must be framed as a directional test rather than a foregone human-data victory.
  Finding: Distilled direct preference optimization from AI feedback on a 7B model achieves chat alignment competitive with 70B models and proprietary systems without sampling-based RL.
- **Maarten Sap et al. 2022**
  Role: Broader theory-of-mind benchmark evidence showing that social reasoning deficits persist in strong LLMs.
  Finding: Out-of-the-box GPT-3 models lag behind humans by over 30% on social intelligence benchmarks and struggle with mental state reasoning compared to factual questions.
- **Carl Orge Retzlaff et al. 2024**
  Role: Supports Beat 5 via category F
  Finding: Reinforcement learning is fundamentally a human-in-the-loop paradigm requiring human-centric approaches for successful deployment.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: 'suggested_paper_outline' must be a non-empty object
  ⚠ The corpus can justify a pilot experiment and can plausibly deliver directional support, but it does not look sufficient to claim robust validation of a high/medium/low L_auth contrastive study on social reasoning benchmarks. Category I is small and very recent, direct F-I-J integration is sparse, and the supplied evidence does not reveal a canonical controlled paper that already ties provenance, behavioral diversity, and social benchmarks together.

---

## Beat 6: CampusGo Proposal

Beat 6 should read as requirements engineering, not validation. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a system would need to satisfy.

- **N. Eagle et al. 2006**
  Role: Provides the broad feasibility precedent: mobile sensing can capture rich human behavioral traces over time.
  Finding: Mobile phone sensing can capture complex social systems through continuous collection of machine-sensed behavioral data from human interactions.
- **Rui Wang et al. 2014**
  Role: Narrows that feasibility claim into the university setting by showing that continuous smartphone sensing can characterize student behavior in a campus environment.
  Finding: Continuous smartphone sensing reveals significant correlations between objective behavioral sensor data and mental well-being and academic performance outcomes among college studen
- **Shayne Longpre et al. 2024**
  Role: Anchor paper for Beat 6: AI data authenticity, consent, and provenance are currently fragmented, so any collection platform needs these design requirements baked in from the start.
  Finding: Existing data provenance solutions for AI training are fragmented and a unified framework integrating authenticity, consent, and provenance metadata is urgently needed.
- **Andreas Köpf et al. 2023**
  Role: Provides the bridge from collection to downstream use: intentionally gathered human conversations can become alignment corpora, so a CampusGo-style platform is not just sensing infrastructure but a potential data-generation pathway.
  Finding: A large-scale open-source dataset of human-generated conversations for LLM alignment can be crowdsourced to democratize RLHF research.
- **Neha Gupta et al. 2023**
  Role: Adds the stewardship boundary: contributors must remain stakeholders in how sensitive data are curated and reused, which keeps CampusGo proposal-framed rather than extractive.
  Finding: The CARE principles framework reveals hidden costs of archaeological data ecosystems borne by Indigenous communities and repositions Indigenous peoples as active stewards of their 
- **Anne Bowser et al. 2020**
  Role: Supports Beat 6 via category G
  Finding: Citizen science projects perform well in data quality assessment and governance but often lack open data access, documentation, and interoperability.

Remaining gaps:
  ⚠ Fallback generated after evidence inventory parse failure: evidence inventory invalid: 'suggested_paper_outline' must be a non-empty object
  ⚠ The proposal is motivated but not validated. Category G has enough material to justify building a provenance-rich social interaction platform, but the graph is highly disconnected from A/E/I, so the corpus does not show that a CampusGo-like system will actually optimize D1 and D4 in a way that improves downstream model quality. This beat can only support a design direction.

---

## Suggested Paper Structure

- section_1_model_collapse_and_contamination_risk: ~6 papers, TBD pages
- section_2_partial_measurability_of_web_drift: ~6 papers, TBD pages
- section_3_l_auth_framework_definition: ~6 papers, TBD pages
- section_4_fine-tuning_data_source_affects_social_reasoning: ~6 papers, TBD pages
- section_5_contrastive_fine-tuning_experiment: ~6 papers, TBD pages
- section_6_campusgo_as_design_proposal: ~6 papers, TBD pages