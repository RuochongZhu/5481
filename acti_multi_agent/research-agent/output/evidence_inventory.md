# Evidence Inventory by Beat

## Beat 1: Model Collapse and Contamination Risk

The chain starts with formal and empirical recursive-training papers showing that self-consumption can damage a model's support, memory, or diversity. It is then qualified by papers showing that curated synthetic loops can sometimes help, which prevents overclaiming. Finally, contamination and prevalence papers make the risk operationally relevant by showing that synthetic material is already entering real information ecosystems. Together, these papers justify urgency and relevance, but they do not directly establish post-training social-reasoning performance effects.

- **Best single paper for the basic collapse mechanism; use as motivation, not as direct proof for downstream task claims.**
  Role: formal anchor for recursive-training risk
  Finding: Provides theoretical and empirical evidence that recursive training can collapse distributional support and erase low-probability modes.
- **Important bridge from general generative-model collapse to LLMs; explicitly include if it is currently absent from the draft.**
  Role: LLM-specific corroboration
  Finding: Shows iterative training on model-generated text can cause forgetting and degeneration in language-model behavior.
- **Use to qualify the claim: risk is real, but not inevitable under all synthetic-data regimes.**
  Role: boundary-condition paper
  Finding: Demonstrates that self-consuming loops need not always collapse if correction and curation mechanisms are introduced.
- **Helpful for nuance; supports the narrower claim that failure depends on data quality and loop design.**
  Role: countervailing evidence on curated synthetic data
  Finding: Shows carefully selected synthetic data can improve model performance in constrained settings.
- **Strong for operational relevance, but still domain-specific rather than web-scale LM evidence.**
  Role: operational consequence case study
  Finding: Reports domain-specific degradation from synthetic contamination, including loss of variability and worse reasoning quality.
- **Supports the claim that contamination is no longer hypothetical, though it does not establish LM collapse.**
  Role: real-world contamination relevance
  Finding: Documents how synthetic media can enter real information ecosystems and distort downstream use cases.

Remaining gaps:
  ⚠ Still missing a decisive web-scale study linking contamination prevalence to downstream LLM degradation over time.
  ⚠ Much of the strongest evidence is controlled
  ⚠ The support is real but mostly controlled, recent, and fragmented. Much of A is image/medical or analytical, while B/C emphasize contamination detection and prevalence rather than downstream LM harm at web scale. This is enough to motivate urgency, not to serve as direct proof for post-training claims.

---

## Beat 2: Web Drift Is Partially Measurable, Broad Degradation Still Unproven

Use this beat strictly as background motivation, not as direct evidence for any primary post-training claim. The clean argumentative arc is: proxy fragility -> bounded longitudinal drift -> crawl-curation implications. Be explicit that category D is method-thin for web drift specifically: these papers mainly justify why diversity/entropy proxies are partial instruments, not direct measurements of contamination. State clearly that synthetic-text studies show what proxy degradation could look like, but they do not demonstrate that the open web has already undergone the same process. Likewise, the privacy-policy and web-evolution papers show measurable temporal change in specific genres or macro site composition, not web-wide pretraining degradation. The C4 paper provides concrete motivation that crawl contents can include leakage, machine-generated text, and filtering bias, but it is still a corpus case study rather than a web-scale contamination audit. Include the required counterevidence plainly: RefinedWeb and FineWeb show that filtered web data still trains strong models, so observed drift signals do not by themselves prove collapse or unusable pretraining data. End the beat with the narrow scope boundary: measurable drift is partial and indirect, and no post-2022 web-scale contamination audit exists in the corpus.

- **Yoon Mi Oh et al. 2022**
  Role: Opens with the measurement problem: corpus-level drift is only observable through proxy metrics, and those proxies vary in robustness to corpus size and content changes.
  Finding: Traditional corpus-based complexity indices (TTR, word-level Entropy) are less robust to corpus size and content variation than newer indices (Word Information Density, Lexical Div
- **Yanzhu Guo et al. 2024**
  Role: Shows that recursive synthetic training can reduce lexical, syntactic, and semantic diversity, motivating why diversity-style proxies are worth monitoring while stopping short of any claim about the open web.
  Finding: Recursively training language models on synthetic text produced by predecessors leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative
- **Ryan Amos et al. 2021**
  Role: Provides a large curated longitudinal web subcorpus in which content change can actually be tracked over time, making web drift measurable in at least one stable genre.
  Finding: A curated longitudinal dataset of over one million English privacy policies spanning two decades reveals how the privacy policy landscape changed in response to evolving regulation
- **Isabel Wagner et al. 2023**
  Role: Anchor paper: confirms substantial multi-decade content evolution in privacy policies, giving the beat its strongest concrete example of measurable but genre-bounded web drift.
  Finding: Privacy policies have evolved over 25 years with measurable content changes in response to regulations like GDPR and CCPA, though gaps remain in user rights.
- **Vibhor Agarwal et al. 2022**
  Role: Broadens from a single document genre to macro web evolution, showing long-run shifts in the kinds of sites that dominate attention and therefore plausibly alter what crawls collect.
  Finding: Quantitative analysis of 25+ years of web evolution shows streaming media and social networking sites have replaced news and education websites in popularity.

Remaining gaps:
  ⚠ This beat is only supported in its narrower form. The corpus can justify that drift and quality variation are measurable and that curation matters, but the D-H link is thin and the literature does not directly prove broad web-scale training-data degradation over time.

---

## Beat 3: L_auth as a Descriptive Framework, Not a Validated Law

Write this beat as a careful synthesis, not a discovery claim. Define L_auth explicitly as a fine-tuning-focused descriptive framework with four dimensions: D1 Provenance Ratio and D4 Social Behavioral Diversity are ex ante data-composition inputs; D2 Lexical Diversity and D3 Entropy are ex post measurable outcomes. The strongest evidence in this set supports a pathway from provenance shifts to diversity shifts in post-training or recursive retraining settings. Be explicit that D4 is the least directly evidenced dimension here: the available papers mainly speak to curation, source breadth, and human-preference structure rather than a settled behavioral-diversity metric. Use the robust-complexity and entropy papers to justify metric families, not to claim a validated weighting scheme. End by stating plainly that L_auth is not a detection tool, not a validated standalone law, not stage-agnostic, and not yet calibrated for cross-dimension weights; extending operationalization to pretraining and learning the weights are

- **Ilia Shumailov et al. 2023**
  Role: Introduces the core framework pressure: when generated data is fed back into training, tail information disappears, motivating L_auth's D1 Provenance Ratio as an upstream composition variable rather than a mere bookkeeping detail.
  Finding: Training generative models on model-generated content causes irreversible Model Collapse where tails of the original distribution disappear.
- **Ilia Shumailov et al. 2024**
  Role: Provides the broader empirical collapse result that makes provenance-sensitive data composition a serious framework ingredient; it grounds D1 as a plausible fine-tuning design axis and cautions that narrow source loops can erase rare cases.
  Finding: Indiscriminate use of model-generated content in training causes irreversible model collapse where tails of the original data distribution disappear.
- **Yanzhu Guo et al. 2024**
  Role: Operational bridge from provenance to measurable outcomes: recursive training on synthetic text is shown to reduce lexical, syntactic, and semantic diversity, motivating D2 and D3 as emergent summaries of authenticity-sensitive data composition.
  Finding: Recursively training language models on synthetic text produced by predecessors leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative
- **Yoon Mi Oh et al. 2022**
  Role: Supplies the measurement discipline for D2 by showing that some traditional corpus indices are unstable under corpus-size and content variation, while newer lexical-diversity measures are more robust; this justifies treating lexical diversity as a designed metric family rather than a single fragile score.
  Finding: Traditional corpus-based complexity indices (TTR, word-level Entropy) are less robust to corpus size and content variation than newer indices (Word Information Density, Lexical Div
- **Pablo Rosillo-Rodes et al. 2025**
  Role: Clarifies the D2-D3 separation by showing that type-token ratio and word entropy are related but not identical corpus summaries; this supports L_auth's choice to keep Lexical Diversity and Entropy as complementary emergent outcomes rather than merge them.
  Finding: An empirical functional relation between word entropy and type-token ratio exists across corpora and languages, analytically derivable from Zipf's and Heaps' laws in the large-text

Remaining gaps:
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

Remaining gaps:
  ⚠ This is the strongest substantive line, but it still supports a narrower claim than the full thesis. F-J is the best-connected primary-evidence cluster, yet the corpus does not cleanly isolate provenance from other factors such as task design, annotation quality, or model family. The AI-feedback side is better supported on bounded tasks than on open-ended social grounding.

---

## Beat 5: Pilot Experiment at Fixed Inference-Time Compute Gives Directional, Not Definitive, Support

Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. State explicitly that the pilot fixes inference-time compute, prompt/interface conditions, and retrieval usage precisely because self-consistency, structured CoT, and DEL-ToM-style inference-time scaling are live rival explanations; the corpus does not let the paper apportion causal weight among those mechanisms after the fact. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

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

Remaining gaps:
  ⚠ The corpus is sufficient to support buildability and deployment value, not downstream model gains. G has credible implementation precedent, but the graph is weakly connected to the primary-evidence clusters, so CampusGo should be presented as an operational contribution rather than proof of training efficacy.

---

## Beat 7: Competing Explanations and Honest Scoping

Keep the tone concessive, not defensive. The point of this beat is to narrow the thesis: if later sections argue for data-composition effects, phrase them as effects observed under fixed model size and fixed inference-time budget, not as exclusive explanations of social-reasoning gains. DEL-ToM should be the main pivot because it most directly demonstrates ToM improvement from inference-time scaling alone. Self-Consistency and SymbCoT frame the broader test-time-compute and chain-of-thought alternative. The third and fourth spine positions then justify the explicit boundary: extended thinking, steering, RL, scale, and objective design are all live competitors. Also note that the evidence base here is heterogeneous and partly thin: several 2025-2026 papers are new, some are system papers, and two pairs are duplicate preprint/published versions (SymbCoT; Relevant answers to polar questions). In prose, prefer citing the published ACL and journal versions, while using the duplicates only if needed for metadata completeness.

- **Xuezhi Wang et al. 2022**
  Role: Establishes the basic adversarial premise: test-time compute over multiple reasoning paths can substantially improve reasoning, so observed gains need not come from data composition alone.
  Finding: Self-consistency decoding, which marginalizes over diverse sampled reasoning paths, substantially boosts chain-of-thought prompting performance on arithmetic and commonsense reason
- **Jundong Xu et al. 2024**
  Role: Shows that strengthening reasoning structure itself via symbolic chain-of-thought can outperform standard CoT, extending the alternative-mechanism story from more compute to better inference-time scaffolding.
  Finding: SymbCoT, integrating symbolic expressions and logic rules with chain-of-thought prompting, consistently and significantly outperforms standard CoT on logical reasoning benchmarks.
- **Yuheng Wu et al. 2025**
  Role: Moves the competing-mechanism argument directly into Theory-of-Mind: inference-time scaling with a logic-grounded verifier improves ToM in small models, so social-reasoning gains can arise from search and verification rather than only upstream data choices.
  Finding: DEL-ToM improves Theory-of-Mind reasoning in small language models through inference-time scaling using a Dynamic Epistemic Logic-grounded verifier rather than architectural change
- **Ariet Jha et al. 2026**
  Role: Extends the line to metacognitive and latent-steered reasoning systems, reinforcing that extended thinking itself is a plausible mechanism; this motivates an honest boundary that any thesis about data composition should be read at fixed model and inference-time budgets.
  Finding: Aham combines symbolic meta-reasoning with latent state steering to enable real-time self-regulated Theory-of-Mind sensitivity in large language models.
- **Hunter Lightman et al. 2023**
  Role: Process supervision is a distinct training-side alternative: gains may come from supervising intermediate reasoning quality rather than from data composition per se.
  Finding: Process supervision significantly outperforms outcome supervision for training models to solve problems from the MATH dataset, achieving 78% accuracy.

Remaining gaps:
  ⚠ This is the most under-covered beat. K is small, recent, and only lightly integrated with the rest of the graph. That is enough to require honest scoping, but not enough to convincingly apportion causal weight among data composition, chain-of-thought, model scale, and test-time compute.

---

## Suggested Paper Structure

- section_1_model_collapse_and_contamination_risk: ~6 papers, TBD pages
- section_2_partial_measurability_of_web_drift: ~5 papers, TBD pages
- section_3_l_auth_framework_definition: ~5 papers, TBD pages
- section_4_fine-tuning_data_source_affects_social_reasoning: ~5 papers, TBD pages
- section_5_contrastive_fine-tuning_experiment: ~5 papers, TBD pages
- section_6_campusgo_as_deployed_core_contribution: ~5 papers, TBD pages
- section_7_competing_explanations_and_honest_scoping: ~5 papers, TBD pages