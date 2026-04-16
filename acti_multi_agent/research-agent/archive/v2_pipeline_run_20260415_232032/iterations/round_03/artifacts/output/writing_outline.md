# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Model Collapse and Contamination Risk

**Anchor paper**: AI models collapse when trained on recursively generated data
  Why: Best category-A anchor for the beat: it consolidates the recursive-reuse collapse argument at high visibility, gives the cleanest statement of tail-loss under indiscriminate synthetic retraining, and sets up the needed scope-limiting contrast with later mitigation papers.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Opens the beat by establishing the core hazard: recursive training on model-generated outputs can erase rare modes and induce collapse.
     Basis: thematic_progression
     → Nature 2024 takes this initial warning and turns it into a more general, prominent statement: when reuse is indiscriminate, recursive synthetic training drives irreversible tail loss.
  2. [2024] AI models collapse when trained on recursively generated data
     Role: Anchor paper that crystallizes collapse risk as a serious motivation for worrying about self-reinforcing synthetic data loops.
     Basis: thematic_progression
     → At the same time, this line of work mostly demonstrates risk under indiscriminate recursive reuse, not that all synthetic data is harmful; the next step is to mark that boundary explicitly.
  3. [2024] Self-Correcting Self-Consuming Loops for Generative Model Training
     Role: Provides the required scope-limiting turn: self-consuming loops can be stabilized under corrective conditions, so collapse is contingent rather than universal.
     Basis: verified_citation
     → Once collapse is treated as a conditional risk rather than a universal law, the motivating question shifts to the information environment: are real domains accumulating enough synthetic material for those risky feedback conditions to matter?
  4. [2025] Quantifying Large Language Model Usage in Scientific Papers
     Role: First bridge into contamination pressure, using a concrete domain-specific measurement of LLM-written or LLM-modified scientific text.
     Basis: thematic_progression
     → But domain-specific uptake in science is not yet proof of uniform web-scale contamination, so the next literature asks whether retrieval environments show stronger downstream exposure effects.
  5. [2026] Retrieval Collapses When AI Pollutes the Web
     Role: Makes the contamination-pressure bridge more concrete by showing that retrieval systems can become overexposed to synthetic content even before complete pool saturation.
     Basis: thematic_progression
     → If information environments are plausibly under contamination pressure, an obvious response is to detect and filter synthetic outputs; the detector literature, however, shows that this backstop is brittle under adaptation.
  6. [2023] Paraphrasing evades detectors of AI-generated text, but retrieval is a
     Role: Closes the beat by showing the limits of reactive filtering: text detectors can be defeated by paraphrase, even if retrieval-based defenses remain partially helpful.
     Basis: thematic_progression

**Paragraph structure**:

  ¶1: Recursive synthetic reuse creates a real collapse risk, but the literature itself already shows that the strongest claims concern indiscriminate reuse rather than all synthetic-data regimes.
    Opening: "The literature first establishes a genuine recursive-reuse hazard—especially loss of rare structure and tail diversity—while also making clear that this is not a blanket indictment of all synthetic data."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Loss Distribution Collapse: A Structural Theory of Dataset D (2026)
    - AI-generated data contamination erodes pathological variabil (2026)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
  ¶2: After that scope limit, the bridge to contamination is empirical and still incomplete: several studies show synthetic uptake in bounded information environments, and retrieval work suggests these pressures can amplify exposure before total saturation.
    Opening: "With collapse reframed as a contingent risk, the key motivating question becomes whether real information environments are accumulating enough synthetic material for those conditions to arise in practice."
    - Self-Improving Diffusion Models with Synthetic Data (2024)
    - Neon: Negative Extrapolation From Self-Training Improves Ima (2025)
    - Quantifying Large Language Model Usage in Scientific Papers (2025)
    - 74% of New Webpages Include AI Content (Study of 900k Pages) (2025)
    - More Articles Are Now Created by AI Than Humans (2025)
    - Retrieval Collapses When AI Pollutes the Web (2026)
  ¶3: Reactive filtering is only a partial safeguard: prevalence studies increasingly rely on detectors, yet detector-focused work shows easy evasion, uneven performance, and only conditional defenses.
    Opening: "A final motivation is that even if contamination pressure is only partially mapped, the obvious remedy—detect and filter synthetic content—looks fragile once generators adapt and detection moves across domains."
    - Synthetic Politics: Prevalence, Spreaders, and Emotional Rec (2025)
    - AI See What You Did There – The Prevalence of LLM-Generated  (2026)
    - Assessing the Prevalence of AI-Generated Content in Leading  (2026)
    - Paraphrasing evades detectors of AI-generated text, but retr (2023)
    - A Watermark for Large Language Models (2023)
    - Detecting AI-Generated Text: Factors Influencing Detectabili (2025)

**Writing notes**: Keep the prose explicitly motivational: this beat raises risk and pressure conditions but is not the direct evidence base for the later primary post-training claim. Preserve the three-step chain: recursive reuse risk, partial contamination-pressure evidence, then detector fragility. After the Nature paper, insert an explicit sentence such as: 'Importantly, this literature mainly establishes failure under indiscriminate recursive reuse, not universal synthetic-data failure.' Use Self-Correcting Self-Consuming Loops and Curated Data as the in-set counterevidence, and note that an additional mixed real+synthetic non-collapse pathway (the pi^2/6 line) exists but is not represented in the supplied candidate set, so it should be acknowledged in prose as external counterevidence rather than omitted. When discussing category-B papers, say contamination is demonstrated in specific environments—science papers, new webpages, political images, MOOCs, selected news ecosystems, retrieval pools—not uniformly proven at web scale. When discussing category-C papers, avoid saying detection is impossible; say instead that detection is context-dependent, often evadable under paraphrase or distribution shift, and partly supplemented by watermarking or retrieval-based defenses.

---

## Beat 2: Partial Measurability of Web Drift

**Anchor paper**: WWW - Privacy Policies over Time: Curation and Analysis of a Million-Document Dataset
  Why: It is the clearest anchor for this beat because it turns abstract concerns about drift into a concrete longitudinal measurement program: a large, curated, time-spanning web-domain dataset that shows measurable change without overstating those changes as web-wide contamination.

**Narrative spine** (6 papers):

  1. [2022] Towards robust complexity indices in linguistic typology
     Role: Establishes the measurement problem: corpus-level drift is often observed through proxy statistics, but those statistics vary in robustness to corpus size and content, so any drift signal must be treated as indirect.
     Basis: thematic_progression
     → Because proxy metrics alone cannot identify where web drift is happening, the narrative moves to longitudinal datasets that observe concrete changes within specific web domains over time.
  2. [2021] WWW - Privacy Policies over Time: Curation and Analysis of a Million-D
     Role: Provides the first strong longitudinal observation: a million-document privacy-policy corpus showing that at least one major web genre changes measurably across decades and in response to regulation.
     Basis: thematic_progression
     → Having established a curated longitudinal corpus, the next paper deepens the claim by analyzing how the content of that same web genre changed from 1996 to 2021.
  3. [2023] Privacy Policies across the Ages: Content of Privacy Policies 1996–202
     Role: Extends the privacy-policy line from collection to substantive content drift, showing measurable longitudinal shifts while still remaining domain-specific rather than web-wide.
     Basis: verified_citation
     → These domain-level observations motivate a broader question for LLM data: how crawl builders detect, document, and filter changing web content in practice.
  4. [2021] Documenting Large Webtext Corpora: A Case Study on the Colossal Clean 
     Role: Shifts from observing web change to documenting crawl artifacts, showing that a major pretraining corpus already contains unexpected content, benchmark leakage, and filtering distortions.
     Basis: thematic_progression
     → If large crawls contain such artifacts, the next step is not to infer collapse, but to ask whether stronger filtering and deduplication can still make web data useful.
  5. [2023] The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora w
     Role: Supplies required counterevidence: filtered, deduplicated web-only data can outperform curated corpora, so measurable crawl issues do not by themselves imply that web pretraining data has broadly degraded.
     Basis: verified_citation
     → FineWeb then extends this filtration-and-scaling story, testing whether careful curation over many Common Crawl snapshots preserves or improves training value.
  6. [2024] The FineWeb Datasets: Decanting the Web for the Finest Text Data at Sc
     Role: Closes the chain with stronger counterevidence from a larger, more recent web dataset: extensive filtering across many crawl snapshots still yields strong models, which narrows the conclusion to partial, indirect measurability of drift rather than demonstrated web-wide contamination.
     Basis: verified_citation
     → The beat should therefore end on a scope boundary: this corpus contains no post-2022 web-scale contamination audit, so the literature supports rising risk and partial observability, not decisive proof of web-wide failure.

**Paragraph structure**:

  ¶1: Measurement proxies can signal distributional change, but they are indirect and method-sensitive.
    Opening: "The most accessible evidence for web drift comes from proxy statistics such as topic structure, entropy, and lexical diversity, but this literature mainly shows that such measurements are possible and fragile, not that web-wide contamination has been demonstrated."
    - Towards robust complexity indices in linguistic typology (2022)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Entropy and type-token ratio in gigaword corpora (2025)
  ¶2: Longitudinal web studies show measurable change in specific domains and platforms, not a full web-scale contamination audit.
    Opening: "Moving from abstract proxies to observed web history, longitudinal studies make clear that some web domains and platforms drift substantially over time, but the evidence remains segmented by genre, site class, or platform rather than truly web-wide."
    - WWW - Privacy Policies over Time: Curation and Analysis of a (2021)
    - Privacy Policies across the Ages: Content of Privacy Policie (2023)
    - "Way back then": A Data-driven View of 25+ years of Web Evol (2022)
    - Evolution of diversity and dominance of companies in online  (2021)
    - The Rise of AI-Generated Content in Wikipedia (2024)
  ¶3: Crawl-curation papers document risk signals but also provide counterevidence that filtered web data remains highly effective.
    Opening: "At the corpus-construction level, the literature documents benchmark leakage, unexpected content, and shifting consent conditions in web crawls, yet it also shows that aggressive filtering and deduplication can still produce very strong pretraining data—and no post-2022 web-scale contamination audit exists in this corpus."
    - Documenting Large Webtext Corpora: A Case Study on the Colos (2021)
    - The RefinedWeb Dataset for Falcon LLM: Outperforming Curated (2023)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)
    - Consent in Crisis: The Rapid Decline of the AI Data Commons (2024)

**Writing notes**: Keep the tone explicitly motivational. The argument should be: drift is partly measurable through proxies, visible in some longitudinal web subdomains, and consequential enough to motivate better crawl curation. Do not convert this into direct evidence for the paper's primary post-training claim. State plainly that the evidence here is partial and indirect: it does not prove web-wide pretraining degradation or contamination. Required counterevidence must be foregrounded, not buried: RefinedWeb and FineWeb show that carefully filtered web data still trains strong models. Use C4 to show that crawl artifacts are real, but not to claim a generalized contemporary failure mode. End with the explicit limitation that no post-2022 web-scale contamination audit exists in the corpus.

---

## Beat 3: L_auth Framework Definition

**Anchor paper**: Towards robust complexity indices in linguistic typology
  Why: It is the best anchor for defining L_auth as a descriptive framework rather than a law: it explicitly compares lexical-diversity and entropy-style complexity indices, shows which are robust to corpus-size and content variation, and therefore supports D2 and D3 as measurable but corpus-sensitive outcome dimensions.

**Narrative spine** (6 papers):

  1. [2022] Towards robust complexity indices in linguistic typology
     Role: Establishes the measurement philosophy for L_auth: lexical diversity and entropy-related indices are useful only when their robustness to corpus size and content is made explicit, which fits D2 and D3 as emergent outcomes rather than intrinsic constants.
     Basis: thematic_progression
     → Once diversity metrics are treated as corpus-sensitive rather than absolute, the next step is to clarify how lexical diversity and entropy relate analytically while still tracking different aspects of post-training data composition.
  2. [2025] Entropy and type-token ratio in gigaword corpora
     Role: Provides the bridge between D2 and D3 by showing a functional relation between type-token behavior and word entropy across corpora, justifying why L_auth keeps them separate but coordinated.
     Basis: thematic_progression
     → With D2 and D3 grounded as measurable outcomes, the framework needs evidence that composition shifts in fine-tuning-like data actually move those outcomes in practice.
  3. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Supplies that applied link: recursive training on synthetic text yields declines in lexical, syntactic, and semantic diversity, making diversity loss a concrete outcome signature of provenance changes.
     Basis: thematic_progression
     → That diversity-loss result motivates a broader provenance argument: if synthetic text occupies too much of the training mix, the concern is not only surface variety but contraction of the underlying distribution itself.
  4. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Generalizes the outcome story into a provenance-ratio story: repeated training on generated data erases tail events, motivating D1 as a design-level input describing how much human-origin versus model-origin data is in the fine-tuning pool.
     Basis: thematic_progression
     → Having framed provenance ratio as consequential, the next question is whether these effects are inevitable or whether loop design can moderate them.
  5. [2024] Self-Correcting Self-Consuming Loops for Generative Model Training
     Role: Introduces the first explicit moderation claim in the spine: under an idealized correction function, self-consuming loops can be stabilized, implying that provenance effects depend on training design rather than expressing a universal law.
     Basis: verified_citation
     → If collapse depends on how recursive data are managed, then curation and socially grounded selection become natural candidate inputs for the framework's design-side dimensions, including D4.
  6. [2024] Self-Consuming Generative Models with Curated Data Provably Optimize H
     Role: Ends the spine by showing that curated self-consuming data can behave differently under strong assumptions, which motivates L_auth's final move: D1 and D4 are design-level composition variables, while D2 and D3 are the measurable outcomes they may influence.
     Basis: verified_citation
     → Together these papers justify L_auth as a synthesis for post-training data composition; they do not validate it as a standalone law, a detector, or a stage-agnostic result, and they leave cross-dimension weight calibration open.

**Paragraph structure**:

  ¶1: Define the measurable outcome side of L_auth: D2 lexical diversity and D3 entropy are related but distinct, and both require robustness-aware operationalization.
    Opening: "We define L_auth first on the outcome side: lexical diversity and entropy are not interchangeable quality labels, but corpus-sensitive measurements whose usefulness depends on robust operationalization across domains, sizes, and source populations."
    - Towards robust complexity indices in linguistic typology (2022)
    - Entropy and type-token ratio in gigaword corpora (2025)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - Lexical and Statistical Analysis of Bangla Newspaper and Lit (2025)
    - Lexical Diversity of Czech L2 Texts at Different Proficiency (2025)
  ¶2: Introduce the provenance-sensitive mechanism behind those outcomes: changes in data origin can reduce diversity and compress tails, motivating D1 as a design input while only weakly sketching D4 through source-group variation.
    Opening: "The framework's input side is motivated by evidence that when model-origin data becomes too dominant, measurable outcomes shift: linguistic diversity declines, rare events disappear, and source properties begin to shape what the learner can still represent."
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - AI-generated data contamination erodes pathological variabil (2026)
    - Training Models on Dialects of Translationese Shows How Lexi (2026)
    - Learning by Surprise: Surplexity for Mitigating Model Collap (2024)
  ¶3: State the design-side scope of L_auth: provenance ratio and socially grounded curation appear to matter, but the literature shows conditional moderation rather than a validated law, leaving calibration and generalization open.
    Opening: "What the recursive-training literature currently supports is not a stage-agnostic law of authenticity, but a narrower design claim: outcomes depend on how synthetic and human data are mixed, corrected, curated, and evaluated during post-training."
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Self-Improving Diffusion Models with Synthetic Data (2024)
    - Neon: Negative Extrapolation From Self-Training Improves Ima (2025)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)
    - A Theoretical Framework for Statistical Evaluability of Gene (2026)

**Writing notes**: Keep the prose definitional, not triumphalist. Present L_auth as a fine-tuning-focused descriptive synthesis with four dimensions: D1 Provenance Ratio and D4 Social Behavioral Diversity as design-level inputs; D2 Lexical Diversity and D3 Entropy as measurable emergent outcomes. Be explicit that evidence is strongest for D1->D2/D3 style relationships and much thinner for D4, which is only partially proxied here by genre, proficiency group, and source-language differences. Do not call L_auth a validated law, discovery, detector, or stage-agnostic framework. Say directly that pretraining operationalization remains future work, and that weight calibration across D1-D4 is also future work rather than something established by the cited literature.

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
  Why: Anchor paper for Beat 5: LIMA is the clearest precedent that data quality and curation can matter enough to justify a provenance-sensitive fine-tuning contrast.

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
  Why: It is the closest AI-facing articulation of the exact infrastructure gaps CampusGo is meant to address—authenticity, consent tracking, and provenance—while still allowing an honest framing that CampusGo is a deployed system contribution rather than evidence of downstream model improvement.

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

**Anchor paper**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistemic Logic
  Why: It is the most direct scope-limiting paper for this beat because it shows Theory-of-Mind gains from inference-time scaling alone, without changing model architecture or training data. That makes it the clearest evidence that any thesis here should be narrowed to fixed-compute data-composition effects rather than treated as a general explanation of social-reasoning improvement.

**Narrative spine** (5 papers):

  1. [2022] Self-Consistency Improves Chain of Thought Reasoning in Language Model
     Role: Establishes the first serious competing mechanism: test-time compute can raise reasoning quality by aggregating multiple sampled chains, even when training data stay fixed.
     Basis: thematic_progression
     → If extra inference-time search already improves reasoning, the next issue is whether more structured reasoning formats outperform plain sampling and therefore further limit any data-only account.
  2. [2024] Faithful Logical Reasoning via Symbolic Chain-of-Thought
     Role: Moves from generic self-consistency to structured chain-of-thought, showing that symbolic scaffolding can improve reasoning beyond standard CoT.
     Basis: thematic_progression
     → That progression matters for scoping because the real question is not only whether reasoning improves at test time, but whether social reasoning itself can improve the same way.
  3. [2025] DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynam
     Role: Provides the strongest direct alternative for this beat by demonstrating Theory-of-Mind gains from verifier-guided inference-time scaling alone, including on smaller models.
     Basis: thematic_progression
     → Once social-reasoning gains can arise from inference-time compute alone, honest scoping requires widening the comparison set to training-stage and elicitation mechanisms that may also shift behavior.
  4. [2025] The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Com
     Role: Broadens the alternative set beyond test-time compute by showing that pragmatic competence changes across pre-training, SFT, and preference-optimization stages.
     Basis: thematic_progression
     → If competence depends on training stage as well as inference-time procedure, then targeted supervision and reward design become additional nontrivial explanations for observed gains.
  5. [2026] Social-R1: Towards Human-like Social Reasoning in LLMs
     Role: Closes the main thread with social-reasoning-specific optimization evidence, indicating that process rewards and adversarial training can improve behavior without appealing to the focal data-composition story.
     Basis: thematic_progression
     → Taken together, these papers argue for a narrow claim: any contribution here should be framed as a fixed-compute data-composition effect, not as a general account of social-reasoning improvement.

**Paragraph structure**:

  ¶1: Inference-time scaling and structured reasoning are genuine alternatives to data-based explanations.
    Opening: "A first and nontrivial competing explanation is that reasoning improvements can emerge from inference-time computation and structure alone, even with no change to the underlying training corpus."
    - Self-Consistency Improves Chain of Thought Reasoning in Lang (2022)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning (2025)
    - Aham: A Metacognitive Architecture for Latent-Steered Theory (2026)
  ¶2: Training-stage, supervision, optimization, and steering mechanisms provide additional explanations for gains in pragmatic or social behavior.
    Opening: "A second family of alternatives shifts attention from test-time compute to how competence is elicited, optimized, or externalized through supervision and training design."
    - The Pragmatic Mind of Machines: Tracing the Emergence of Pra (2025)
    - Let's Verify Step by Step (2023)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)
    - CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind (2026)
    - Social-R1: Towards Human-like Social Reasoning in LLMs (2026)
  ¶3: Context effects, data scale, and hard pragmatic evaluations all narrow the scope of any broad causal claim.
    Opening: "Finally, deployment context, corpus scale and curation, and tougher pragmatic evaluations all caution against treating one mechanism as a complete explanation of social-reasoning performance."
    - How Far Can In-Context Alignment Go? Exploring the State of  (2024)
    - CCI4.0: A Bilingual Pretraining Dataset for Enhancing Reason (2025)
    - Are Vision Language Models Cross-Cultural Theory of Mind Rea (2025)
    - Relevant answers to polar questions. (2025)
    - Relevant answers to polar questions (2025)

**Writing notes**: Write this beat as a concessionary scope paragraph, not as a rebuttal section. State early that inference-time scaling is a real alternative, and use DEL-ToM as the sharpest reason to narrow the claim. Treat the SymbCoT and Relevant answers pairs as duplicate venue/preprint trails rather than independent evidence bursts. End explicitly on the boundary: the contribution, if maintained, is about data-composition effects under fixed model size and test-time budget, not about universally explaining or maximizing social reasoning.

---
