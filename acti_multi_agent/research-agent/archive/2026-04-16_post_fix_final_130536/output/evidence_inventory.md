# Evidence Inventory by Beat

## Beat 1: Model Collapse and Contamination Risk

The beat begins with the strongest recursive-training papers showing that self-consuming loops can shrink diversity and degrade models. It then adds contamination-in-practice papers showing that synthetic pollution is not merely hypothetical. Finally, curation and self-correction papers narrow the claim: the evidence supports urgency for provenance-aware data collection and filtering, but not the stronger claim that any use of synthetic data inevitably causes collapse.

- **Best single citation for the core model-collapse mechanism.**
  Role: anchor theoretical and empirical evidence
  Finding: Shows that recursive training on model-generated data can narrow distributions and degrade model quality.
- **Useful for connecting formal collapse arguments to language-model practice.**
  Role: early LLM-specific warning
  Finding: Demonstrates catastrophic forgetting and distributional impoverishment when LLMs are retrained on their own outputs.
- **Important because it shows collapse risk is conditional, not universal.**
  Role: mitigation via curation
  Finding: Argues that self-consuming loops can be stabilized if synthetic data are carefully curated against human-preference criteria.
- **Supports a nuanced urgency claim rather than a fatalistic one.**
  Role: mechanistic refinement
  Finding: Introduces self-correction mechanisms showing that contamination harms can be reduced when loops are filtered or corrected.
- **Useful as a concrete downstream example outside generic LLM benchmarks.**
  Role: domain-specific empirical corroboration
  Finding: Finds severe vocabulary and diagnostic degradation when medical records are contaminated with synthetic data.
- **Helps move the argument from abstract risk to operational plausibility.**
  Role: practical contamination scenario
  Finding: Shows that synthetic contamination in online streams can degrade continual learning systems in realistic update settings.

Remaining gaps:
  ⚠ Evidence is still recent and fragmented across modalities and domains.
  ⚠ Most papers establish risk mechanisms, not broad web-scale prevalence.
  ⚠ This beat should motivate provenance-aware collection, not serve as direct proof for socially grounded post-training benefits in Beats 4-5.
  ⚠ Good as urgency-setting background, but not as the direct proof base for socially grounded post-training claims. Much of the evidence is recent, fragmented, and often domain-specific; mitigation and generalization across modalities remain underdeveloped.

---

## Beat 2: Web Drift and Partial Measurability

This beat should make a narrower claim than 'the web is ruined.' Bounded-domain papers show that AI-content growth and drift can be measured in slices of the web. Contamination and recursive-training papers then explain why such drift could matter downstream. The combined chain supports partial measurability and plausible harm pathways, but not a strong claim that the open web as a whole has already broadly degraded as a training source.

- **Good evidence for bounded-domain drift, not for total web degradation.**
  Role: slice-level measurement example
  Finding: Shows that AI-generated media can measurably infiltrate a concrete web-facing domain and distort information quality.
- **Use carefully as a framing citation, not as decisive empirical proof.**
  Role: conceptual framing of web pollution
  Finding: Reviews the plausibility and limits of claims that online ecosystems are increasingly saturated with generated content and bots.
- **Connects partial measurability of drift to realistic degradation pathways.**
  Role: mechanism from drift to degradation
  Finding: Shows how contamination in evolving online streams can produce measurable downstream learning harm.
- **Best used as an existence proof in a bounded domain.**
  Role: domain-specific contamination measurement
  Finding: Provides a concrete example where synthetic contamination is not only detectable but materially harmful.
- **Supports consequence, not direct web measurement.**
  Role: back-end consequence model
  Finding: Explains why measured drift matters if generated content re-enters training pipelines.
- **Helps complete the drift-to-risk chain.**
  Role: language-model consequence model
  Finding: Shows that contamination becomes consequential when models ingest their own or similar generated outputs.

Remaining gaps:
  ⚠ No strong end-to-end web-scale demonstration of broad training-quality degradation.
  ⚠ The D-H connection remains thin: measurement exists, but authenticity-aware causal interpretation is limited.
  ⚠ Several available papers are domain-specific or conceptual rather than web-scale empirical studies.
  ⚠ The corpus supports only the narrower claim that web drift and AI-content growth are partially measurable in slices of the web. It does not directly prove broad web-scale degradation of training quality, and the D-H connection is especially thin in the graph.

---

## Beat 3: L_auth as Descriptive Framework

The framework beat should present L_auth as an organizing lens: model behavior after post-training depends not only on quantity, but on the authenticity, composition, and curation of supervision. LIMA supplies the strongest direct precedent for high-quality human-authored post-training data. Collapse and curation papers explain why provenance and composition plausibly matter. OpenAssistant shows how authentic conversational collection can instantiate the framework. The claim should remain descriptive and stage-specific, not a universal law.

- **Best citation for the idea that authenticity and composition can matter more than raw volume in post-training.**
  Role: missing but crucial framework anchor
  Finding: Argues that a small amount of high-quality human-authored supervision can strongly improve instruction following.
- **Useful for formalizing why composition matters.**
  Role: curation principle
  Finding: Provides a theoretical reason to think data authenticity or preference-consistency matters for fine-tuning outcomes.
- **Supports L_auth as descriptive rather than absolute.**
  Role: conditionality of effects
  Finding: Shows that quality control mediates the effects of self-generated data, implying authenticity is one axis among several.
- **Use as motivation for the framework, not as direct validation of it.**
  Role: background pressure for the framework
  Finding: Establishes that data provenance and composition can materially affect future model quality.
- **Bridges collapse work to language-model post-training concerns.**
  Role: language-model bridge
  Finding: Provides an LLM-specific argument that source authenticity and distributional integrity can matter during retraining.
- **Helps make L_auth concrete as a data-design lens.**
  Role: operational example of authentic conversational data
  Finding: Shows how large-scale human conversation collection can support alignment-oriented post-training.

Remaining gaps:
  ⚠ Cross-stage validation is weak; evidence is stronger for fine-tuning than for pretraining or broad stage-agnostic claims.
  ⚠ Authenticity is confounded with curation, difficulty, and preference alignment.
  ⚠ The framework is plausible and useful, but not yet a validated law.
  ⚠ The corpus can motivate L_auth as a useful organizing lens for fine-tuning data-authenticity effects, but not as a validated law. The underlying D category is very new and weakly integrated with A/E/I, so stage-agnostic or causal claims would be under-supported.

---

## Beat 4: Primary Claim: Socially Grounded Post-Training Improves Social Reasoning

Keep Beat 4 clearly separate from collapse literature. The defensible chain is: social reasoning is a real post-training weak spot; curated human data can be disproportionately high leverage; provenance changes socially meaningful outputs; and bounded-task counterevidence prevents any universal claim that human data always wins. The final sentence of the beat should explicitly narrow the thesis to socially grounded, norm-sensitive behavior rather than alignment overall.

- **Strong support for the idea that authentic conversational quality matters in post-training.**
  Role: quality-over-quantity anchor
  Finding: Finds that a relatively small set of carefully selected human examples can produce large alignment gains.
- **Maarten Sap et al. 2022**
  Role: Establishes why social reasoning is the right downstream target: even strong LLMs lag on mental-state and norm-sensitive tasks, so this capability cannot be assumed from pretraining alone.
  Finding: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on tasks measuring intent, reaction, and mental state inference.
- **Shibani Santurkar et al. 2023**
  Role: Shows that post-training data source changes socially meaningful outputs, not just generic helpfulness: instruction tuning shifts whose opinions the model appears to reflect.
  Finding: Current language models exhibit substantial misalignment with US demographic groups' opinions, on par with the Democrat-Republican divide on climate change, even after demographic 
- **Rafael Rafailov et al. 2023**
  Role: Provides the clean methodological hinge: DPO simplifies preference optimization so feedback-source comparisons become more interpretable than full RLHF stacks.
  Finding: RLHF can be solved with a simple classification loss by reparameterizing the reward model to extract the optimal policy in closed form.
- **Harrison Lee et al. 2023**
  Role: Provides required counterevidence: AI feedback can match RLHF on bounded dialogue and summarization tasks, so the claim must stay narrower than universal human-data superiority.
  Finding: RLAIF achieves comparable performance to RLHF across summarization and dialogue tasks, and direct-RLAIF outperforms canonical RLAIF by obtaining rewards directly from an LLM.

Remaining gaps:
  ⚠ This is the strongest literature-backed beat, but the claim must stay narrow. The corpus supports that provenance and genuine human interaction data seem especially valuable for socially grounded tasks, while AI feedback can work well on bounded objectives; it does not prove provenance superiority across all post-training settings.

---

## Beat 5: Fixed-Compute Pilot Evidence

Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. Handle LIMA explicitly as a cross-beat paper: in Beat 4 it supports the broader claim that curation matters, while in Beat 5 it only motivates why a provenance-sensitive intervention is worth testing. State explicitly that the pilot fixes inference-time compute, prompt/interface conditions, and retrieval usage precisely because self-consistency, structured CoT, and DEL-ToM-style inference-time scaling are live rival explanations; the corpus does not let the paper apportion causal weight among those mechanisms after the fact. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

- **Maarten Sap et al. 2019**
  Role: Establishes Social IQa as a demanding evaluation target, which is why the pilot uses social reasoning rather than only generic chat benchmarks.
  Finding: Social IQa provides a large-scale benchmark for evaluating commonsense reasoning about people's actions, intents, and reactions in social interactions.
- **Chunting Zhou et al. 2023**
  Role: Anchor paper for Beat 5: LIMA is the clearest precedent that data quality and curation can matter enough to justify a provenance-sensitive fine-tuning contrast.
  Finding: Fine-tuning a 65B LLM on only 1,000 carefully curated examples without RL achieves performance comparable or preferred to GPT-4 in 43% of cases.
- **Rafael Rafailov et al. 2023**
  Role: Defines the pilot's methodological hinge: DPO keeps the optimization recipe simple enough that differences between data conditions remain interpretable.
  Finding: RLHF can be solved with a simple classification loss by reparameterizing the reward model to extract the optimal policy in closed form.
- **Lewis Tunstall et al. 2023**
  Role: Provides the strongest competitive synthetic baseline: AI-feedback distillation can produce strong chat alignment, which is why the pilot must be framed as a directional test rather than a foregone human-data victory.
  Finding: Distilled direct preference optimization using AI feedback enables a 7B model (Zephyr-7B) to surpass Llama2-Chat-70B on MT-Bench without human annotation.
- **Maarten Sap et al. 2022**
  Role: Broader theory-of-mind benchmark evidence showing that social reasoning deficits persist in strong LLMs.
  Finding: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box, struggling substantially on tasks measuring intent, reaction, and mental state inference.

Remaining gaps:
  ⚠ The literature justifies running a fixed-inference-compute pilot, but does not by itself validate strong conclusions from it. The biggest gap is lack of close precedent that cleanly disentangles provenance/data composition from inference-time scaling, chain-of-thought, and model-scale effects on socially grounded tasks.

---

## Beat 6: CampusGo as Deployed Provenance Infrastructure

Beat 6 should read as deployed requirements engineering, not downstream validation. Longpre et al. (2024) is the diagnosis anchor that names the broken properties of present AI data pipelines; CampusGo is positioned as one concrete operationalization of those requirements for socially grounded post-training data, not as proof that the full authenticity agenda is solved. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a deployed system would need to satisfy.

- **N. Eagle et al. 2006**
  Role: Provides the broad feasibility precedent: mobile sensing can capture rich human behavioral traces over time.
  Finding: Mobile phone sensor data can be used to sense and model complex social systems in naturalistic settings.
- **Rui Wang et al. 2014**
  Role: Narrows that feasibility claim into the university setting by showing that continuous smartphone sensing can characterize student behavior in a campus environment.
  Finding: Smartphone sensing can continuously assess college students' mental health, academic performance, and behavioral trends in naturalistic settings.
- **Shayne Longpre et al. 2024**
  Role: Anchor paper for Beat 6: AI data authenticity, consent, and provenance are currently fragmented, so a deployed CampusGo-style collection platform needs these requirements baked in from the start.
  Finding: Data authenticity verification, consent tracking, and provenance preservation are systemically broken in current AI training practices, with ~5% of C4 tokens and 45% of content res
- **Neha Gupta et al. 2023**
  Role: Adds the stewardship boundary: contributors must remain stakeholders in how sensitive data are curated and reused, which keeps CampusGo deployed-but-scoped rather than extractive or overclaimed.
  Finding: The CARE principles provide an intellectual framework for Indigenous data governance that highlights hidden costs of data sharing borne by Indigenous communities in archaeology.
- **Anne Bowser et al. 2020**
  Role: Structured Beat 6 spine paper.
  Finding: Citizen science projects perform well on data quality and governance but lack open data access, documentation, interoperability, and long-term preservation.

Remaining gaps:
  ⚠ Adequate support exists for presenting CampusGo as a real implementation and deployment contribution. However, deployment demonstrates collection capability and provenance instrumentation, not downstream model improvement; the corpus does not close that gap for you.

---

## Beat 7: Competing Explanations and Honest Scoping

Order the beat as an honest narrowing move, not a rebuttal. Emphasize that direct internal citation links were not provided, so the spine follows thematic progression and a historical build-up from prompting to search, then to explicit test-time compute scaling, then to post-training and social-reasoning extensions. State plainly that inference-time scaling is a genuine alternative mechanism. Do not imply CoT or test-time compute are minor effects. Use the DEL-ToM result to make the crucial adversarial point that social reasoning itself may improve from inference-time scaling, which means L_auth should be framed only as a data-composition effect under fixed model, fixed post-training recipe, and fixed inference budget. Also admit that the social/pragmatic evidence base here is thinner than the general reasoning evidence, so the final sentence should mark a scope boundary rather than claim a decisive causal ranking among mechanisms.

- **Jason Wei et al. 2022**
  Role: Establishes the first honest competing mechanism: substantial reasoning gains can appear at inference time through prompting alone, without changing the training corpus.
  Finding: Chain-of-thought prompting enables large language models to substantially improve reasoning performance at inference time without modifying training data.
- **Xuezhi Wang et al. 2022**
  Role: Shows that extra sampling and aggregation over multiple reasoning traces improves performance, turning inference-time search into a concrete alternative explanation for gains.
  Finding: Self-consistency decoding, which marginalizes over diverse sampled reasoning paths, substantially boosts chain-of-thought prompting accuracy on arithmetic and commonsense reasoning
- **Charlie Snell et al. 2024**
  Role: Makes the core adversarial claim explicit: optimally scaling test-time compute can be more effective than scaling model parameters, so capability gains cannot be attributed to data factors alone.
  Finding: Optimally scaling LLM test-time compute can be more effective than scaling model parameters for improving performance.
- **Niklas Muennighoff et al. 2025**
  Role: Provides a practical extended-thinking result in which budget forcing and small supervised tuning produce large reasoning gains, reinforcing that compute allocation at inference can materially change outcomes.
  Finding: Supervised finetuning on a curated 1,000-example dataset with budget forcing enables a 32B model to exceed o1-preview on competitive reasoning benchmarks.
- **DeepSeek-AI et al. 2025**
  Role: Adds a second strong alternative mechanism by showing that reinforcement learning can induce powerful reasoning behavior, suggesting that post-training optimization and extended reasoning traces may drive gains independently of corpus composition.
  Finding: Strong inference-time reasoning gains are reproducible in open-weight models via reinforcement learning, demonstrating they are not exclusive to proprietary systems.

Remaining gaps:
  ⚠ This beat works if it stays genuinely adversarial. The key alternative mechanisms are present, but the corpus still lacks decisive head-to-head studies against provenance/data-composition effects, so the paper should surface these as real scope limiters rather than try to dismiss them.

---

## Suggested Paper Structure

- section_1_model_collapse_and_contamination_risk: ~6 papers, TBD pages
- section_2_partial_measurability_of_web_drift: ~6 papers, TBD pages
- section_3_l_auth_framework_definition: ~6 papers, TBD pages
- section_4_fine-tuning_data_source_affects_social_reasoning: ~5 papers, TBD pages
- section_5_contrastive_fine-tuning_experiment: ~5 papers, TBD pages
- section_6_campusgo_as_deployed_core_contribution: ~5 papers, TBD pages
- section_7_competing_explanations_and_honest_scoping: ~5 papers, TBD pages