# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Model Collapse and Contamination Risk

**Anchor paper**: AI models collapse when trained on recursively generated data
  Why: It is the clearest category-A anchor for the beat because it consolidates the recursive-reuse collapse argument into a high-visibility statement about indiscriminate synthetic retraining, while still leaving room to state the key limitation that this is not a universal indictment of all synthetic-data use.

**Narrative spine** (6 papers):

  1. [2024] AI models collapse when trained on recursively generated data
     Role: Anchor the beat with the strongest general warning: indiscriminate recursive reuse of model outputs can erase distributional tails and produce collapse.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → To make that warning concrete rather than purely headline-level, earlier recursion work helps specify the mechanism by which repeated synthetic reuse forgets rare but important structure.
  2. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Provide the canonical mechanism for collapse under self-training: generated data recursively sharpens the distribution and causes tail loss.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But this literature does not justify the stronger claim that all synthetic data is harmful, so the next step is to introduce work showing that corrective or constrained loops can remain stable.
  3. [2024] Self-Correcting Self-Consuming Loops for Generative Model Training
     Role: Insert the required scope limit: collapse is not inevitable if self-consuming loops include a correction mechanism, so the risk is about uncontrolled recursion rather than synthetic data per se.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That bounded counterexample is strengthened by papers arguing that curation, rather than blanket avoidance, can make iterative synthetic pipelines productive.
  4. [2024] Self-Consuming Generative Models with Curated Data Provably Optimize H
     Role: Extend the limitation step with a curated-success case: carefully filtered self-consuming training can avoid collapse and even optimize toward human preferences.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Taken together, these papers mostly establish the danger of indiscriminate recursive reuse, not universal synthetic-data failure; the practical bridge is therefore narrower and empirical: are information environments accumulating enough synthetic content to create contamination pressure?
  5. [2026] Retrieval Collapses When AI Pollutes the Web
     Role: Supply the strongest category-B bridge in the provided set: in retrieval settings, synthetic-content accumulation can disproportionately contaminate exposure even before the whole pool is fully synthetic.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Even here the evidence is still domain- and platform-specific rather than a universal proof of web-scale contamination, which is why the literature then turns to a reactive question: can detectors reliably filter the problem away?
  6. [2023] Paraphrasing evades detectors of AI-generated text, but retrieval is a
     Role: Close the chain on detector fragility: reactive filtering can help, but adversarial paraphrasing sharply degrades detector performance and exposes the limits of relying on post hoc detection alone.
     Basis: thematic_progression
     → This leaves the beat on a bounded motivation claim: contamination pressure is plausible and increasingly measurable, but current filtering defenses are conditional and brittle rather than impossible or useless.

**Paragraph structure**:

  ¶1: Recursive synthetic reuse creates a real collapse risk, but the current literature supports a conditional warning rather than a universal ban on synthetic data.
    - AI models collapse when trained on recursively generated dat (2024)
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - doi:10.48550/ar (?)

---

## Beat 2: Partial Measurability of Web Drift

**Anchor paper**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Why: It is the clearest anchor for this beat because it converts a curated longitudinal web slice into measured content change over 1996-2021, showing that drift is observable in bounded domains without overstating that result as proof of web-wide contamination.

**Narrative spine** (6 papers):

  1. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Opens with the strongest available proxy-style evidence from category D: synthetic-text recursion can measurably reduce lexical, syntactic, and semantic diversity, motivating concern that drift may be detectable through distributional proxies while also remaining a laboratory result rather than a web audit.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Because proxy declines in diversity are indirect, the next step is to ask whether comparable change can be observed in real longitudinal slices of the web itself.
  2. [2021] WWW - Privacy Policies over Time: Curation and Analysis of a Million-D
     Role: Introduces a concrete longitudinal web dataset: a million privacy policies curated across two decades, establishing that some web domains can be tracked over time with explicit temporal structure.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → With that longitudinal corpus in place, later work can move from dataset construction to direct measurement of how the content of a bounded web genre changed.
  3. [2023] Privacy Policies across the Ages: Content of Privacy Policies 1996–202
     Role: Provides the main observational claim for this beat: privacy-policy content changed measurably from 1996-2021 in response to regulatory and institutional shifts, showing real drift in a large but genre-specific slice of the web.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Still, privacy policies are only one genre, so the argument must widen cautiously from bounded longitudinal observation to how web-scale crawls are documented and curated.
  4. [2021] Documenting Large Webtext Corpora: A Case Study on the Colossal Clean 
     Role: Shifts to crawl-curation practice by showing that C4 contains unexpected content and benchmark leakage artifacts, making web drift and contamination risk operationally visible at corpus-construction time rather than only through abstract proxies.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → A natural response is not to treat those artifacts as decisive proof of web-wide degradation, but to test whether more careful filtering and deduplication can still make web data useful.
  5. [2023] The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora w
     Role: Supplies required counterevidence: RefinedWeb argues that web data, when aggressively filtered and deduplicated, can outperform curated corpora, so measurable artifacts in raw crawls do not by themselves show that web pretraining has failed.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That curation-first reply is then extended to a much larger, multi-snapshot setting to ask whether filtered web data remains strong even as the web keeps changing.
  6. [2024] The FineWeb Datasets: Decanting the Web for the Finest Text Data at Sc
     Role: Closes with stronger counterevidence from large-scale curation: FineWeb shows that a heavily processed web dataset built from many Common Crawl snapshots can train strong models, sharpening the beat's narrow conclusion that observed drift is partial and indirect rather than decisive proof of web-wide contamination.
     Basis: verified_citation
     → Scope boundary: the corpus contains no post-2022 web-scale contamination audit, so this beat should end on rising measurable risk plus strong filtered-web counterevidence, not on a claim that web-wide degradation has been demonstrated.

**Paragraph structure**:

  ¶1: Measurement proxies can flag possible drift, but the available evidence is indirect and method-sensitive.
    Opening: "A cautious starting point is proxy measurement: diversity, entropy, and complexity indicators can register distributional change, but in this corpus they mostly come from synthetic-data settings or general corpus methodology rather than direct audits of the live web."
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Towards robust complexity indices in linguistic typology (2022)
    - Entropy and type-token ratio in gigaword corpora (2025)
  ¶2: Longitudinal observations show that some web subdomains do change measurably over time, but those observations remain bounded slices.
    Opening: "When the literature moves from proxies to observed web archives, it does find real temporal change: curated privacy-policy collections, broad web-history analyses, and recent Wikipedia studies all show that parts of the web evolve in content and composition."
    - WWW - Privacy Policies over Time: Curation and Analysis of a (2021)
    - Privacy Policies across the Ages: Content of Privacy Policie (2023)
    - "Way back then": A Data-driven View of 25+ years of Web Evol (2022)
    - The Rise of AI-Generated Content in Wikipedia (2024)
  ¶3: Crawl-curation studies make the risk operationally visible, but filtered-web results are also the beat's required counterevidence.
    Opening: "At web-crawl scale, documentation work shows why contamination and drift are plausible concerns, yet the strongest downstream evidence in this corpus also shows that carefully filtered web data can still train strong models."
    - Documenting Large Webtext Corpora: A Case Study on the Colos (2021)
    - Consent in Crisis: The Rapid Decline of the AI Data Commons (2024)
    - The RefinedWeb Dataset for Falcon LLM: Outperforming Curated (2023)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)

**Writing notes**: Keep this beat explicitly motivational: it establishes that web drift is partially measurable through proxies, bounded longitudinal slices, and corpus-documentation practices, but it does not provide the direct evidence base for any primary post-training claim. State plainly that category D is thin for true web auditing: its strongest contributions here are proxy metrics and synthetic-text experiments, not web-scale contamination measurements. Use the privacy-policy pair as the clearest longitudinal observation, then widen cautiously with web-history and Wikipedia examples as bounded corroboration. In the crawl section, contrast C4-style artifact discovery with the required counterevidence from RefinedWeb and FineWeb: filtered web data can remain highly effective, so observed artifacts are not decisive proof of global web degradation. End narrowly and honestly: measurable drift is partial and indirect; no post-2022 web-scale contamination audit exists in the corpus; therefore this beat supports rising background risk, not demonstrated web-wide pretraining failure.

---

## Beat 3: L_auth Framework Definition

**Anchor paper**: Towards robust complexity indices in linguistic typology
  Why: It is the best anchor for turning scattered diversity observations into a framework definition because it explicitly compares robustness of corpus-based complexity indices and warns against over-relying on unstable proxies like raw TTR. That lets L_auth define D2 and relate it to D3 without presenting either as a validated law.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Introduces the core provenance problem: recursive reuse of model-generated data can erase distributional tails, motivating Provenance Ratio (D1) as a design-level variable rather than assuming all training mixtures are equivalent.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If recursive training can destroy tail behavior, the next question is whether that failure is inevitable or whether it depends on how the loop is corrected and curated.
  2. [2024] Self-Correcting Self-Consuming Loops for Generative Model Training
     Role: Moves from collapse as a warning to controllable design choices: stability improves when self-consuming loops are corrected, which supports treating provenance and curation as input dimensions rather than a binary human-versus-synthetic verdict. This is the closest bridge in the set to D4 as a design-level notion.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once loop design becomes the variable of interest, the framework needs observable consequences of bad composition, and text-specific work measures those consequences as declines in diversity.
  3. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Provides the text-facing bridge from D1 inputs to D2 outcomes by showing lexical, syntactic, and semantic diversity decline under recursive synthetic training, especially on creative tasks.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But a reported drop in 'diversity' only helps define L_auth if the underlying indices are themselves robust across corpus size and content.
  4. [2022] Towards robust complexity indices in linguistic typology
     Role: Selects the measurement posture for D2: lexical diversity is useful, but not all traditional indices behave robustly, so the framework should privilege more stable diversity summaries over naive single-metric readings.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → After narrowing the lexical side, the framework still needs to explain how lexical variety relates to entropy-based summaries rather than treating them as interchangeable.
  5. [2025] Entropy and type-token ratio in gigaword corpora
     Role: Establishes that type-token behavior and entropy are related but not identical, justifying D2 and D3 as separate dimensions: lexical diversity captures richness of forms, while entropy captures distributional concentration and uncertainty.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That distinction opens room for a dedicated entropy dimension whose value depends on modeling and regularization choices, not just vocabulary breadth.
  6. [2020] Analyzing the Influence of Hyper-parameters and Regularizers of Topic 
     Role: Supplies the entropy-side ingredient for D3 by showing Renyi entropy can track topic-model structure and regularization effects, making entropy a useful descriptive outcome dimension. It also supports the caution that entropy choices require calibration, so L_auth should remain a synthesis of ingredients, not a standalone validated law.
     Basis: thematic_progression
     → Because entropy behavior depends on metric choice, regularization, and task setup, L_auth should end here as a descriptive framework for post-training data composition; weight calibration, pretraining operationalization, and any stronger law-like claims remain future work.

**Paragraph structure**:

  ¶1: Define the design-level inputs of L_auth: Provenance Ratio (D1) and a weaker, still under-specified Social Behavioral Diversity dimension (D4).
    Opening: "L_auth starts from controllable composition variables—how much fine-tuning data is human versus synthetic and how behaviorally curated that mixture is—because recursive-training studies show that provenance and curation shape stability more than any simple human/AI binary admits."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Self-Improving Diffusion Models with Synthetic Data (2024)
  ¶2: Define D2 as lexical diversity, the clearest emergent outcome axis in the set, while being explicit that measurement must rely on robust indices rather than naive proxy counts.
    Opening: "Given those inputs, the first observable outcome family in L_auth is lexical diversity: recursive synthetic training tends to compress it, but the framework should count only those diversity measures that remain informative across domains, corpus sizes, and writing conditions."
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Towards robust complexity indices in linguistic typology (2022)
    - Entropy and type-token ratio in gigaword corpora (2025)
    - Lexical and Statistical Analysis of Bangla Newspaper and Lit (2025)
    - Lexical Diversity of Czech L2 Texts at Different Proficiency (2025)
    - Training Models on Dialects of Translationese Shows How Lexi (2026)
  ¶3: Add D3 as entropy, a complementary distributional outcome dimension, then close with scope limits: no validated law, no detector claim, no stage-agnostic generalization, and no calibrated weights yet.
    Opening: "L_auth then adds entropy as a second outcome dimension: related to lexical variety but useful precisely because it captures concentration and regularization effects that vocabulary-richness measures alone can miss, while still requiring task-specific calibration."
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - A Theoretical Framework for Statistical Evaluability of Gene (2026)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)

**Writing notes**: Write this beat as a framework-definition section, not an evidence-of-effect section. Explicitly map the four dimensions: D1 Provenance Ratio and D4 Social Behavioral Diversity are design-level inputs about post-training data composition; D2 Lexical Diversity and D3 Entropy are measurable emergent outcomes. Be honest that D4 is the thinnest dimension in the current paper set: the evidence supports curation, preference alignment, and source heterogeneity as important inputs, but does not yet provide a settled direct metric for social-behavioral diversity in fine-tuning corpora. Use the recursive-training papers only to justify why such inputs matter, not to claim L_auth is a discovered law. When discussing D2, emphasize that robust lexical diversity metrics are preferred over raw TTR-only readings. When discussing D3, frame entropy as a complementary descriptive family of measures, not as a detection tool and not as universally calibrated across models or stages. End the beat with the explicit boundary that L_auth is a synthesis of metric ingredients for fine-tuning or other post-training data composition; it is not validated as stage-agnostic, it does not by itself establish downstream model gains, and dimension weighting/calibration is future work.

---

## Beat 4: Fine-tuning Data Source Affects Social Reasoning

**Anchor paper**: LIMA: Less Is More for Alignment
  Why: Anchor paper for Beat 4: LIMA shows that a small, carefully curated human-authored set can drive large alignment gains, making data provenance a high-leverage post-training variable.

**Narrative spine** (5 papers):

  1. [2022] Neural Theory-of-Mind? On the Limits of Social Intelligence in Large L
     Role: Establishes why social reasoning is the right downstream target: even strong LLMs lag on mental-state and norm-sensitive tasks, so this capability cannot be assumed from pretraining alone.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → Once social reasoning is established as a persistent weak spot, the next question is whether carefully curated post-training data can move that behavior more efficiently than scale alone. [thematic progression; no verified internal citation edge]
  2. [2023] LIMA: Less Is More for Alignment
     Role: Anchor paper for Beat 4: LIMA shows that a small, carefully curated human-authored set can drive large alignment gains, making data provenance a high-leverage post-training variable.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → After LIMA makes curation a plausible treatment variable, the literature asks whether provenance alters socially meaningful outputs rather than only general chat quality. [thematic progression; no verified internal citation edge]
  3. [2023] Whose Opinions Do Language Models Reflect?
     Role: Shows that post-training data source changes socially meaningful outputs, not just generic helpfulness: instruction tuning shifts whose opinions the model appears to reflect.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → If provenance affects social judgments, then the optimization pipeline itself matters, which is why later work isolates a simpler preference-learning objective. [thematic progression; no verified internal citation edge]
  4. [2023] Direct Preference Optimization: Your Language Model is Secretly a Rewa
     Role: Provides the clean methodological hinge: DPO simplifies preference optimization so feedback-source comparisons become more interpretable than full RLHF stacks.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → With a simpler alignment method in place, the strongest counterclaim is that AI-generated preference signals may substitute for human judgments on bounded tasks. [thematic progression; no verified internal citation edge]
  5. [2023] RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback wit
     Role: Provides required counterevidence: AI feedback can match RLHF on bounded dialogue and summarization tasks, so the claim must stay narrower than universal human-data superiority.

**Paragraph structure**:

  ¶1: Social reasoning remains a distinct post-training weak spot
    Opening: "The fine-tuning line should begin from task sensitivity, not from collapse theory: social commonsense and theory-of-mind style reasoning remain meaningfully weaker than generic instruction following."
    - Social IQa: Commonsense Reasoning about Social Interactions (2019)
    - Neural Theory-of-Mind? On the Limits of Social Intelligence  (2022)
  ¶2: Curated human data and provenance shape socially meaningful behavior
    Opening: "Against that backdrop, human conversational corpora and curated instruction sets make data provenance concrete, and LIMA plus opinion-shift evidence show that source quality affects socially meaningful outputs."
    - OpenAssistant Conversations -- Democratizing Large Language  (2023)
    - LIMA: Less Is More for Alignment (2023)
    - Whose Opinions Do Language Models Reflect? (2023)
  ¶3: Methodological hinge plus bounded-task counterevidence
    Opening: "The honest conclusion comes only after the counterexamples: DPO makes source comparisons cleaner, but AlpacaFarm, RLAIF, and Zephyr all show that synthetic or AI-feedback pipelines can succeed on bounded alignment objectives."
    - Direct Preference Optimization: Your Language Model is Secre (2023)
    - AlpacaFarm: A Simulation Framework for Methods that Learn fr (2023)
    - RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Fe (2023)

**Writing notes**: Keep Beat 4 clearly separate from collapse literature. The defensible chain is: social reasoning is a real post-training weak spot; curated human data can be disproportionately high leverage; provenance changes socially meaningful outputs; and bounded-task counterevidence prevents any universal claim that human data always wins. The final sentence of the beat should explicitly narrow the thesis to socially grounded, norm-sensitive behavior rather than alignment overall.

---

## Beat 5: Contrastive Fine-tuning Experiment

**Anchor paper**: LIMA: Less Is More for Alignment
  Why: LIMA is the cleanest anchor for this beat because it motivates a fixed-compute pilot design: behavior can shift through small, curated post-training data without changing the base model or inference budget. That makes it a natural bridge from benchmarked social deficits to a contrastive fine-tuning methodology, while still supporting the paper's cautious framing as initial evidence rather than validation.

**Narrative spine** (4 papers):

  1. [2019] Social IQa: Commonsense Reasoning about Social Interactions
     Role: Establishes Social IQa as a demanding evaluation target, which is why the pilot uses social reasoning rather than only generic chat benchmarks.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → Because the benchmark is intentionally socially grounded, the next step is a precedent showing that carefully curated fine-tuning data can materially change behavior. [thematic progression; no verified internal citation edge]
  2. [2023] LIMA: Less Is More for Alignment
     Role: Anchor paper for Beat 5: LIMA is the clearest precedent that data quality and curation can matter enough to justify a provenance-sensitive fine-tuning contrast.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → Once data quality is treated as the intervention, the method must stay simple enough that condition-to-condition differences remain interpretable. [thematic progression; no verified internal citation edge]
  3. [2023] Direct Preference Optimization: Your Language Model is Secretly a Rewa
     Role: Defines the pilot's methodological hinge: DPO keeps the optimization recipe simple enough that differences between data conditions remain interpretable.
     Basis: verified_citation
     Note: Verified by check_citations.py: Zephyr cites DPO.
     → With a controlled preference objective in place, the strongest next baseline is Zephyr, which applies AI-feedback distillation on top of a DPO-style alignment recipe. [verified citation order]
  4. [2023] Zephyr: Direct Distillation of LM Alignment
     Role: Provides the strongest competitive synthetic baseline: AI-feedback distillation can produce strong chat alignment, which is why the pilot must be framed as a directional test rather than a foregone human-data victory.

**Paragraph structure**:

  ¶1: Why the pilot uses social reasoning as its evaluation target
    Opening: "The experiment beat should begin by justifying the evaluation target: social reasoning remains difficult enough that small changes in data provenance are more likely to surface here than on generic chat benchmarks."
    - Social IQa: Commonsense Reasoning about Social Interactions (2019)
    - Neural Theory-of-Mind? On the Limits of Social Intelligence  (2022)
  ¶2: Why a provenance-sensitive contrast is methodologically plausible
    Opening: "LIMA motivates the treatment variable, DPO keeps the comparison interpretable, and AlpacaFarm shows why a synthetic baseline is methodologically reasonable even if it is not the same as socially grounded human data."
    - LIMA: Less Is More for Alignment (2023)
    - Direct Preference Optimization: Your Language Model is Secre (2023)
    - AlpacaFarm: A Simulation Framework for Methods that Learn fr (2023)
  ¶3: Why the outcome must be framed as directional rather than validated
    Opening: "The strongest existing counterevidence comes from bounded alignment tasks: RLAIF and Zephyr show that AI feedback can already be highly competitive, which is why the present experiment can only offer directional evidence on social reasoning rather than full validation."
    - RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Fe (2023)
    - Zephyr: Direct Distillation of LM Alignment (2023)

**Writing notes**: Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

---

## Beat 6: CampusGo as Deployed Core Contribution

**Anchor paper**: Position: Data Authenticity, Consent, & Provenance for AI are all broken: what will it take to fix them?
  Why: It is the clearest bridge from adjacent deployment and governance literatures to the specific AI-facing problem CampusGo addresses: current training pipelines lack reliable authenticity checks, consent tracking, and provenance preservation. This lets the beat frame CampusGo as deployed provenance-aware infrastructure without overstating evidence about downstream model gains.

**Narrative spine** (5 papers):

  1. [2006] Reality mining: sensing complex social systems
     Role: Provides the broad feasibility precedent: mobile sensing can capture rich human behavioral traces over time.
     Basis: verified_citation
     Note: Verified citation order: doi:10.1145/2632048.2632054 cites doi:10.1007/s00779-005-0046-3.
     → A general sensing precedent becomes relevant only after it is narrowed into a campus-specific behavioral setting. [verified citation order]
  2. [2014] StudentLife: assessing mental health, academic performance and behavio
     Role: Narrows that feasibility claim into the university setting by showing that continuous smartphone sensing can characterize student behavior in a campus environment.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → Once campus collection looks feasible, the key question becomes not sensing alone but how authenticity, consent, and provenance should be represented for AI use. [thematic progression; no verified internal citation edge]
  3. [2024] Position: Data Authenticity, Consent, & Provenance for AI are all brok
     Role: Anchor paper for Beat 6: AI data authenticity, consent, and provenance are currently fragmented, so a deployed CampusGo-style collection platform needs these requirements baked in from the start.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
  4. [2023] The CARE Principles and the Reuse, Sharing, and Curation of Indigenous
     Role: Adds the stewardship boundary: contributors must remain stakeholders in how sensitive data are curated and reused, which keeps CampusGo deployed-but-scoped rather than extractive or overclaimed.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
  5. [2020] Still in Need of Norms: The State of the Data in Citizen Science
     Role: Structured Beat 6 spine paper.

**Paragraph structure**:

  ¶1: Campus-situated collection is technically plausible
    Opening: "The beat should start with implementation feasibility only: adjacent mobile-sensing work shows that campus-scale behavioral collection is technically plausible, not that deployment alone proves model-training value."
    - Reality mining: sensing complex social systems (2006)
    - StudentLife: assessing mental health, academic performance a (2014)
  ¶2: AI-specific provenance requirements define the proposal core
    Opening: "What turns simple sensing into a defensible proposal is the provenance layer plus a downstream use case: authenticity, consent, and governance must be designed together, and OpenAssistant shows that intentionally collected human conversations can in fact become alignment data."
    - Position: Data Authenticity, Consent, & Provenance for AI ar (2024)
    - Perspective: The Power (Dynamics) of Open Data in Citizen Sc (2021)
  ¶3: Stewardship requirements keep CampusGo deployed but carefully scoped
    Opening: "The final move is a scope limit: stewardship principles show why CampusGo can be presented as a deployed provenance-aware platform, but not as a validated intervention for downstream model gains."
    - Still in Need of Norms: The State of the Data in Citizen Sci (2020)
    - The CARE Principles and the Reuse, Sharing, and Curation of  (2023)

**Writing notes**: Beat 6 should read as deployed requirements engineering, not downstream validation. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a deployed system would need to satisfy.

---

## Beat 7: Competing Explanations and Honest Scoping

**Anchor paper**: Self-Consistency Improves Chain of Thought Reasoning in Language Models
  Why: It is the clearest high-signal demonstration in this set that reasoning gains can arise from inference-time search and aggregation alone, making it the right anchor for an honest scope boundary around any data-composition claim.

**Narrative spine** (6 papers):

  1. [2022] Self-Consistency Improves Chain of Thought Reasoning in Language Model
     Role: Start by conceding the strongest general alternative: more test-time compute via self-consistency materially improves reasoning without changing training data or model architecture.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If simple sample-and-aggregate decoding already shifts performance, the next question is whether more structured reasoning formats can push gains further without any new corpus intervention.
  2. [2024] Faithful Logical Reasoning via Symbolic Chain-of-Thought
     Role: Extend the inference-time alternative from generic search to structured chain-of-thought: symbolic scaffolds can outperform standard CoT, so reasoning format itself is a live competing mechanism.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That makes the key adversarial test social reasoning itself: can inference-time structure improve theory-of-mind behavior even in smaller models?
  3. [2025] DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynam
     Role: Use the most on-point scope limiter: DEL-ToM reports theory-of-mind gains from inference-time scaling with a logic-grounded verifier, directly showing that social reasoning can improve without architecture changes.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once inference-time scaling alone can move social reasoning, attribution cannot stop at decoding; broader model and training-stage differences also remain plausible explanations.
  4. [2025] The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Com
     Role: Broaden the scope boundary beyond test-time compute: pragmatic competence varies across pre-training, SFT, and preference optimization, so model behavior also depends on training pipeline and model family.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → And if generic training stages already matter, targeted optimization for social reasoning is an even stronger competing mechanism against any data-only account.
  5. [2026] Social-R1: Towards Human-like Social Reasoning in LLMs
     Role: Show that specialized supervision can itself drive social-reasoning gains: process-reward RL on difficult social examples improves behavior, competing directly with explanations framed only in terms of corpus composition.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → A final complication is that some failures may reflect not missing knowledge but weak externalization or control over latent social representations.
  6. [2026] CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment
     Role: Close with the strongest honest narrowing: if models may already contain internal theory-of-mind knowledge that can be surfaced through causal steering, then the thesis here should be limited to fixed-compute data-composition effects rather than treated as the sole driver of social reasoning gains.
     Basis: thematic_progression
     → Taken together, these papers justify ending the beat with an explicit scope boundary: inference-time scaling, structured deliberation, supervision, and steering remain genuine alternative mechanisms.

**Paragraph structure**:

  ¶1: Inference-time compute and structured deliberation are genuine competing mechanisms, including in social reasoning.
    Opening: "A fair adversarial reading should begin by admitting that sizable reasoning gains can come from inference-time search, aggregation, and structured deliberation alone, even before changing the training corpus."
    - Self-Consistency Improves Chain of Thought Reasoning in Lang (2022)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning (2025)
    - Aham: A Metacognitive Architecture for Latent-Steered Theory (2026)
  ¶2: Attribution is further limited by pretraining composition, alignment format, distillation dynamics, and model-family differences; pure scale evidence is thinner here than inference-time evidence.
    Opening: "The mechanism picture broadens further once training pipeline, data scale and quality, in-context alignment, distillation dynamics, and model family are treated as active confounds rather than background noise."
    - The Pragmatic Mind of Machines: Tracing the Emergence of Pra (2025)
    - CCI4.0: A Bilingual Pretraining Dataset for Enhancing Reason (2025)
    - How Far Can In-Context Alignment Go? Exploring the State of  (2024)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)
    - Are Vision Language Models Cross-Cultural Theory of Mind Rea (2025)
  ¶3: Targeted supervision and steering can improve social reasoning, while persistent pragmatic gaps keep the thesis narrow and fixed-compute.
    Opening: "Finally, targeted supervision and causal steering show that social-reasoning behavior can be improved by mechanisms other than corpus composition, even as benchmark gaps in pragmatic competence remain."
    - Social-R1: Towards Human-like Social Reasoning in LLMs (2026)
    - Let's Verify Step by Step (2023)
    - CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind (2026)
    - Relevant answers to polar questions. (2025)
    - Relevant answers to polar questions (2025)

**Writing notes**: End this beat by narrowing, not defending. Explicitly say that inference-time scaling and structured CoT are real alternatives, and DEL-ToM is especially important because it suggests social-reasoning gains can arise from inference-time scaling alone. Therefore any downstream thesis should be framed as a claim about data-composition effects under fixed model and compute budgets, not as a general explanation of social-reasoning improvement. Also note that this candidate set gives stronger evidence for inference-time and training-stage confounds than for clean model-scale ablations; admit that limitation rather than overstating what is isolated. When drafting prose, treat the duplicated SymbCoT and PRIOR-PQ records as publication/preprint lineage rather than independent evidence.

---
