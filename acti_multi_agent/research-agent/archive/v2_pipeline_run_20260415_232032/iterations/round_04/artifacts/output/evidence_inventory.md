# Evidence Inventory by Beat

## Beat 1: Model Collapse and Contamination Risk

Conservative fallback inventory aligned to narrative chains and classified metadata. Use these papers as candidates, not as a polished evidence chain.

- **Ilia Shumailov et al. 2024**
  Role: Anchor the beat with the strongest general warning: indiscriminate recursive reuse of model outputs can erase distributional tails and produce collapse.
  Finding: Indiscriminate use of model-generated content in training causes irreversible model collapse where tails of the original data distribution disappear.
- **Ilia Shumailov et al. 2023**
  Role: Provide the canonical mechanism for collapse under self-training: generated data recursively sharpens the distribution and causes tail loss.
  Finding: Training generative models on model-generated content causes irreversible Model Collapse where tails of the original distribution disappear.
- **Nate Gillman et al. 2024**
  Role: Insert the required scope limit: collapse is not inevitable if self-consuming loops include a correction mechanism, so the risk is about uncontrolled recursion rather than synthetic data per se.
  Finding: Introducing an idealized correction function makes self-consuming generative training loops exponentially more stable against collapse.
- **Damien Ferbach et al. 2024**
  Role: Extend the limitation step with a curated-success case: carefully filtered self-consuming training can avoid collapse and even optimize toward human preferences.
  Finding: Data curation in self-consuming generative models can provably optimize human preferences and prevent model collapse under iterative retraining.
- **Hongyeon Yu et al. 2026**
  Role: Supply the strongest category-B bridge in the provided set: in retrieval settings, synthetic-content accumulation can disproportionately contaminate exposure even before the whole pool is fully synthetic.
  Finding: 67% pool contamination with AI-generated content leads to over 80% exposure contamination in retrieval systems, creating a homogenized yet deceptively healthy state.
- **Sina Alemohammad et al. 2025**
  Role: Supports Beat 1 via category A
  Finding: Reversing gradient updates from self-training on synthetic data extrapolates away from degraded weights and improves image generation quality.

Remaining gaps:
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
  ⚠ The support is real but mostly controlled, recent, and fragmented. Much of A is image/medical or analytical, while B/C emphasize contamination detection and prevalence rather than downstream LM harm at web scale. This is enough to motivate urgency, not to serve as direct proof for post-training claims.

---

## Beat 2: Web Drift Is Partially Measurable, Broad Degradation Still Unproven

Keep this beat explicitly motivational: it establishes that web drift is partially measurable through proxies, bounded longitudinal slices, and corpus-documentation practices, but it does not provide the direct evidence base for any primary post-training claim. State plainly that category D is thin for true web auditing: its strongest contributions here are proxy metrics and synthetic-text experiments, not web-scale contamination measurements. Use the privacy-policy pair as the clearest longitudinal observation, then widen cautiously with web-history and Wikipedia examples as bounded corroboration. In the crawl section, contrast C4-style artifact discovery with the required counterevidence from RefinedWeb and FineWeb: filtered web data can remain highly effective, so observed artifacts are not decisive proof of global web degradation. End narrowly and honestly: measurable drift is partial and indirect; no post-2022 web-scale contamination audit exists in the corpus; therefore this beat supports rising background risk, not demonstrated web-wide pretraining failure.

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
- **Sergei Koltcov et al. 2020**
  Role: Supports Beat 2 via category D
  Finding: The minimum of Renyi entropy coincides with the true number of topics in labelled collections, enabling principled analysis of regularization effects on topic models.

Remaining gaps:
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
  ⚠ This beat is only supported in its narrower form. The corpus can justify that drift and quality variation are measurable and that curation matters, but the D-H link is thin and the literature does not directly prove broad web-scale training-data degradation over time.

---

## Beat 3: L_auth as a Descriptive Framework, Not a Validated Law

Write this beat as a framework-definition section, not an evidence-of-effect section. Explicitly map the four dimensions: D1 Provenance Ratio and D4 Social Behavioral Diversity are design-level inputs about post-training data composition; D2 Lexical Diversity and D3 Entropy are measurable emergent outcomes. Be honest that D4 is the thinnest dimension in the current paper set: the evidence supports curation, preference alignment, and source heterogeneity as important inputs, but does not yet provide a settled direct metric for social-behavioral diversity in fine-tuning corpora. Use the recursive-training papers only to justify why such inputs matter, not to claim L_auth is a discovered law. When discussing D2, emphasize that robust lexical diversity metrics are preferred over raw TTR-only readings. When discussing D3, frame entropy as a complementary descriptive family of measures, not as a detection tool and not as universally calibrated across models or stages. End the beat with the explicit boundary that L_auth is a synthesis of metric ingredients for fine-tuning or other post-training data composition; it is not validated as stage-agnostic, it does not by itself establish downstream model gains, and dimension weighting/calibration is future work.

- **Ilia Shumailov et al. 2023**
  Role: Introduces the core provenance problem: recursive reuse of model-generated data can erase distributional tails, motivating Provenance Ratio (D1) as a design-level variable rather than assuming all training mixtures are equivalent.
  Finding: Training generative models on model-generated content causes irreversible Model Collapse where tails of the original distribution disappear.
- **Nate Gillman et al. 2024**
  Role: Moves from collapse as a warning to controllable design choices: stability improves when self-consuming loops are corrected, which supports treating provenance and curation as input dimensions rather than a binary human-versus-synthetic verdict. This is the closest bridge in the set to D4 as a design-level notion.
  Finding: Introducing an idealized correction function makes self-consuming generative training loops exponentially more stable against collapse.
- **Yanzhu Guo et al. 2024**
  Role: Provides the text-facing bridge from D1 inputs to D2 outcomes by showing lexical, syntactic, and semantic diversity decline under recursive synthetic training, especially on creative tasks.
  Finding: Recursively training language models on synthetic text produced by predecessors leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative
- **Yoon Mi Oh et al. 2022**
  Role: Selects the measurement posture for D2: lexical diversity is useful, but not all traditional indices behave robustly, so the framework should privilege more stable diversity summaries over naive single-metric readings.
  Finding: Traditional corpus-based complexity indices (TTR, word-level Entropy) are less robust to corpus size and content variation than newer indices (Word Information Density, Lexical Div
- **Pablo Rosillo-Rodes et al. 2025**
  Role: Establishes that type-token behavior and entropy are related but not identical, justifying D2 and D3 as separate dimensions: lexical diversity captures richness of forms, while entropy captures distributional concentration and uncertainty.
  Finding: An empirical functional relation between word entropy and type-token ratio exists across corpora and languages, analytically derivable from Zipf's and Heaps' laws in the large-text
- **Sergei Koltcov et al. 2020**
  Role: Supports Beat 3 via category D
  Finding: The minimum of Renyi entropy coincides with the true number of topics in labelled collections, enabling principled analysis of regularization effects on topic models.

Remaining gaps:
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
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
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
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
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
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
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
  ⚠ The corpus is sufficient to support buildability and deployment value, not downstream model gains. G has credible implementation precedent, but the graph is weakly connected to the primary-evidence clusters, so CampusGo should be presented as an operational contribution rather than proof of training efficacy.

---

## Beat 7: Competing Explanations and Honest Scoping

End this beat by narrowing, not defending. Explicitly say that inference-time scaling and structured CoT are real alternatives, and DEL-ToM is especially important because it suggests social-reasoning gains can arise from inference-time scaling alone. Therefore any downstream thesis should be framed as a claim about data-composition effects under fixed model and compute budgets, not as a general explanation of social-reasoning improvement. Also note that this candidate set gives stronger evidence for inference-time and training-stage confounds than for clean model-scale ablations; admit that limitation rather than overstating what is isolated. When drafting prose, treat the duplicated SymbCoT and PRIOR-PQ records as publication/preprint lineage rather than independent evidence.

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
- **Jundong Xu et al. 2024**
  Role: Supports Beat 7 via category K
  Finding: SymbCoT, integrating symbolic expressions and logic rules with chain-of-thought prompting, consistently and significantly outperforms standard CoT on logical reasoning benchmarks.

Remaining gaps:
  ⚠ Inventory was synthesized conservatively from corpus-grounded papers after the structured generator returned an invalid schema.
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