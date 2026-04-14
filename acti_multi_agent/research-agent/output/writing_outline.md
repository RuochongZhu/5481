# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Model Collapse and Contamination Risk

**Anchor paper**: AI models collapse when trained on recursively generated data
  Why: This is the clearest high-signal anchor for Beat 1 because it consolidates the recursive-reuse literature into a widely recognized mixed empirical-theoretical statement: indiscriminate training on recursively generated data can cause irreversible collapse, especially through loss of distribution tails. It supports the beat's opening claim without forcing the stronger and unsupported claim that all synthetic data is harmful.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Introduces the core collapse mechanism: recursive training on generated data makes models forget low-probability regions of the original distribution.
     Basis: thematic_progression
     → Follow-up work sharpens this into a more operational condition, arguing that the key danger is self-consuming training without enough fresh real data entering each generation.
  2. [2023] Self-Consuming Generative Models go MAD
     Role: Extends the collapse story into the go-MAD framework, specifying that insufficient fresh real data leads to quality or diversity degradation across generations.
     Basis: verified_citation
     → Taken together, these early results motivate a broader synthesis: recursive reuse is risky not as a slogan, but as a generational distribution-shift process.
  3. [2024] AI models collapse when trained on recursively generated data
     Role: Serves as the beat's anchor by establishing collapse under recursively generated training data and foregrounding irreversible tail loss as the central failure mode.
     Basis: thematic_progression
     → Crucially, however, this literature mainly proves risk under indiscriminate recursive reuse, not universal synthetic-data failure; later work makes that scope limit explicit by showing stable mixed-data regimes.
  4. [2024] Universality of the $π^2/6$ Pathway in Avoiding Model Collapse
     Role: Provides the required counterpoint: mixed real-plus-synthetic training can avoid collapse, so the evidence supports a narrower warning about unmanaged recursive reuse rather than a blanket rejection of synthetic data.
     Basis: verified_citation
     → Once narrowed in that way, the next question becomes empirical rather than theoretical: are real information environments accumulating enough synthetic content for recursive exposure to become a practical pretraining concern?
  5. [2025] Quantifying Large Language Model Usage in Scientific Papers
     Role: Offers one of the strongest domain-specific measurements of contamination pressure by quantifying LLM usage in scientific writing, while still falling short of proving universal web-scale contamination.
     Basis: thematic_progression
     → Because these contamination measurements remain partial and environment-specific, the literature also asks whether reactive filtering can reliably keep synthetic text out of future corpora.
  6. [2023] Can AI-Generated Text be Reliably Detected?
     Role: Closes the chain on the limits of reactive filtering by showing that many detector families can be broken under recursive paraphrasing, making post hoc cleanup fragile rather than impossible.
     Basis: thematic_progression
     → Overall, the strongest Beat 1 conclusion is conditional: recursive synthetic reuse is a real pretraining risk, contamination pressure is increasingly plausible but not yet universally proven, and detector-based filtering is an unstable last line of defense.

**Paragraph structure**:

  ¶1: Recursive synthetic reuse can cause collapse, but the evidence supports a narrower claim about indiscriminate reuse rather than universal synthetic-data failure.
    Opening: "Recent work has made a strong case that recursively training models on their own outputs can collapse the learned distribution, especially by erasing rare but important tails, while also showing that this risk is conditional rather than universal."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - Self-Consuming Generative Models go MAD (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Universality of the $π^2/6$ Pathway in Avoiding Model Collap (2024)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
  ¶2: Evidence that contamination pressure is building in information environments is emerging, but it remains partial, measurement-specific, and not yet a proof of universal web-scale contamination.
    Opening: "The bridge from collapse theory to current pretraining risk is more tentative: available studies indicate rising exposure to machine-generated content in scientific writing and parts of the web, but the evidence is still domain-specific and incomplete."
    - Quantifying Large Language Model Usage in Scientific Papers (2025)
    - 74% of New Webpages Include AI Content (Study of 900k Pages) (2025)
    - More Articles Are Now Created by AI Than Humans (2025)
    - Retrieval Collapses When AI Pollutes the Web (2026)
  ¶3: Reactive filtering is an important mitigation idea, but the detector literature shows that it is brittle under paraphrase and simple evasion tactics.
    Opening: "A natural response to contamination pressure is to detect and filter AI-generated text after the fact, yet the strongest detector studies suggest this defense is only partially reliable once adversaries or even routine rewriting enter the loop."
    - A Watermark for Large Language Models (2023)
    - Can AI-Generated Text be Reliably Detected? (2023)
    - Paraphrasing evades detectors of AI-generated text, but retr (2023)
    - Simple techniques to bypass GenAI text detectors: implicatio (2024)

**Writing notes**: Keep the beat explicitly three-step: collapse risk -> tentative contamination-pressure evidence -> reactive filtering limits. Make the scope admission unavoidable before any category-B bridge: the literature strongly supports risk from indiscriminate recursive reuse, not the claim that all synthetic data is harmful. Name the counterevidence directly: pi^2/6 mixed real+synthetic pathway, self-correcting loops, and curated synthetic-data regimes. For category B, use cautious language such as 'emerging', 'domain-specific', and 'not yet universal proof'; avoid saying the web is definitively contaminated at training-relevant scale. For category C, avoid saying detection is impossible; the stronger claim is that watermarking and other detectors are fragile under paraphrase or low-effort manipulation, even if retrieval or provenance-aware defenses can still help in narrower settings. Do not import any fine-tuning evidence from categories F, I, or J.

---

## Beat 2: Partial Measurability of Web Drift

**Anchor paper**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Why: It is the strongest direct longitudinal content study in the set: a large, curated 25-year web genre analysis that shows measurable drift while remaining appropriately domain-bounded rather than claiming web-wide contamination.

**Narrative spine** (6 papers):

  1. [2022] Towards robust complexity indices in linguistic typology
     Role: Establishes the measurement caution: corpus-level diversity or complexity signals can be tracked, but metric choice is sensitive to sampling and corpus size, so any drift claim should begin with bounded proxies rather than sweeping web-wide conclusions.
     Basis: thematic_progression
     → Because the corpus contains no post-2022 web-scale contamination audit, the literature moves from abstract proxy robustness to longitudinal web archives where change can be observed directly within a stable document genre.
  2. [2021] WWW - Privacy Policies over Time: Curation and Analysis of a Million-D
     Role: Provides a concrete long-span web measurement case by curating a million-document privacy-policy corpus and showing systematic temporal drift in length, readability, and ambiguity.
     Basis: thematic_progression
     → Extending this curated privacy-policy line, later work deepens the content analysis and shows that the drift is not only stylistic but also substantive.
  3. [2023] Privacy Policies across the Ages: Content of Privacy Policies 1996–202
     Role: Strengthens the longitudinal evidence with a 1996-2021 content analysis showing increasing use of location data, implicit collection, limited user choice, and growing third-party sharing; this is the beat's anchor example of measurable web drift.
     Basis: verified_citation
     → Taken together, these genre-specific findings motivate a broader question: do similarly large shifts appear in the web's overall sectoral composition and platform ecology?
  4. [2022] "Way back then": A Data-driven View of 25+ years of Web Evolution
     Role: Widens the frame from one document genre to 25+ years of web evolution, showing shifts in dominant site types and platform composition across the web archive.
     Basis: thematic_progression
     → But longitudinal web evolution studies still do not quantify synthetic contamination rates, so the narrative turns to crawl-construction work that inspects present-day pretraining corpora and tests whether filtered web data remains usable.
  5. [2023] The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora w
     Role: Supplies the required counterevidence: with careful filtering and deduplication, web-only data can still train strong LLMs, so observed drift is not decisive proof that web corpora are already unusable.
     Basis: thematic_progression
     → Building on this web-only curation result, later work scales the pipeline across many Common Crawl snapshots and again reports strong performance, reinforcing the need for a narrow conclusion.
  6. [2024] The FineWeb Datasets: Decanting the Web for the Finest Text Data at Sc
     Role: Closes on curation practice rather than proof of failure: systematic large-scale filtering over 96 Common Crawl snapshots yields better-performing pretraining data, implying that measurable drift creates rising risk and curation pressure, not demonstrated web-wide degradation.
     Basis: verified_citation
     → Therefore, the literature supports only a partial and indirect measurability claim: some drift and access changes are observable, but no post-2022 web-scale contamination audit in this corpus establishes web-wide pretraining degradation.

**Paragraph structure**:

  ¶1: Proxy metrics can register distributional change, but only indirectly and with substantial dependence on metric robustness.
    Opening: "Because no post-2022 web-scale contamination audit exists in the corpus, this section begins with measurement proxies: work on corpus complexity, entropy, and topic-structure diagnostics shows that distributional change can be tracked, but only through metrics whose stability and interpretability must be handled carefully."
    - Towards robust complexity indices in linguistic typology (2022)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
  ¶2: Longitudinal archive studies show clear web drift in bounded domains and broad platform composition, without directly measuring web-wide synthetic contamination.
    Opening: "More concrete evidence comes from longitudinal web observations: privacy-policy archives and long-range web-history analyses show that web content and attention patterns have shifted substantially over time, but these studies remain domain-specific or structural rather than direct contamination audits."
    - WWW - Privacy Policies over Time: Curation and Analysis of a (2021)
    - Privacy Policies across the Ages: Content of Privacy Policie (2023)
    - "Way back then": A Data-driven View of 25+ years of Web Evol (2022)
    - Evolution of diversity and dominance of companies in online  (2021)
  ¶3: Crawl-curation studies reveal present-day risk signals, yet also show that filtered web corpora still train strong models.
    Opening: "Current pretraining-corpus work sharpens the picture but keeps the conclusion narrow: corpus audits find artifacts, governance constraints, and bounded signs of AI-text growth, while RefinedWeb and FineWeb demonstrate that carefully filtered web data still supports strong language models."
    - Documenting Large Webtext Corpora: A Case Study on the Colos (2021)
    - The RefinedWeb Dataset for Falcon LLM: Outperforming Curated (2023)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)
    - Consent in Crisis: The Rapid Decline of the AI Data Commons (2024)
    - The Rise of AI-Generated Content in Wikipedia (2024)

**Writing notes**: Keep the claim explicitly narrow. This beat is about partial measurability of drift, not demonstrated web-wide contamination or failure. State plainly that no post-2022 web-scale contamination audit exists in the corpus. Use the D-category papers only to motivate why proxies are fragile and indirect. Then pivot to H-category longitudinal studies as the strongest direct evidence of change over time, especially the privacy-policy line and web-evolution archive work. In the final paragraph, juxtapose risk signals (C4 artifacts, shrinking data commons, Wikipedia AI-content growth) with required counterevidence (RefinedWeb and FineWeb), so the conclusion is: drift and curation pressure are measurable in parts, risk is rising, but filtered web corpora still produce strong models and the literature here does not prove web-wide pretraining degradation.

---

## Beat 3: L_auth Framework Definition

**Anchor paper**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text
  Why: It is the clearest bridge paper for this beat: it connects synthetic-data provenance to measured declines in lexical, syntactic, and semantic diversity, linking collapse-style concerns to the metric ingredients later assembled into L_auth.

**Narrative spine** (5 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Establishes the provenance-side motivation for D1 by showing that recursive training on generated data removes tail support and reduces diversity across generations.
     Basis: thematic_progression
     → If recursive synthetic reuse can erase distributional tails, the next question is how that loss appears in observable language statistics rather than only in abstract collapse arguments.
  2. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Provides the main empirical bridge from provenance to outcomes by showing that synthetic retraining is accompanied by declines in lexical, syntactic, and semantic diversity.
     Basis: thematic_progression
     → Once diversity decline is visible empirically, the literature turns to a harder measurement question: which indices are stable enough to summarize that change without being dominated by corpus-size artifacts?
  3. [2022] Towards robust complexity indices in linguistic typology
     Role: Grounds D2 metric choice by showing that common corpus complexity measures vary in robustness, motivating careful use of lexical-diversity indicators rather than naive reliance on raw TTR-style counts.
     Basis: thematic_progression
     → This caution about lexical metrics motivates adding entropy-based summaries, so that L_auth does not depend on a single family of diversity statistics.
  4. [2020] Analyzing the Influence of Hyper-parameters and Regularizers of Topic 
     Role: Supports D3 by treating Renyi entropy as an informative structural statistic, showing that entropy can track meaningful organization changes even if the setting is topic modeling rather than language-model pretraining.
     Basis: thematic_progression
     → From there, the key issue is how entropy relates back to lexical-diversity measures, since L_auth includes both and must avoid pretending they are fully independent.
  5. [2025] Entropy and type-token ratio in gigaword corpora
     Role: Links D2 and D3 by showing a consistent empirical and analytic relation between word entropy and type-token ratio, supporting their joint inclusion while also signaling potential overlap and the need for future calibration.
     Basis: thematic_progression
     → Taken together, these papers justify L_auth as a grounded synthesis of provenance and diversity ingredients, but not yet as a calibrated standalone law.

**Paragraph structure**:

  ¶1: Why L_auth needs a provenance input dimension (D1)
    Opening: "Recursive-training studies make clear that any descriptive framework for synthetic-data effects must track provenance explicitly, because the fraction of fresh human data versus model-generated reuse changes whether distributions remain stable or collapse."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Self-Consuming Generative Models go MAD (2023)
    - A Theoretical Perspective: How to Prevent Model Collapse in  (2025)
  ¶2: From provenance shifts to measurable outcome dimensions (D2 lexical diversity, D3 entropy)
    Opening: "The main bridge to L_auth comes from work showing that synthetic retraining is associated with observable diversity decline, together with metric papers clarifying which lexical and entropy-based summaries are robust enough to describe that shift."
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Towards robust complexity indices in linguistic typology (2022)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - Entropy and type-token ratio in gigaword corpora (2025)
  ¶3: D4 as a motivated but thinner dimension, and the scope limits of L_auth
    Opening: "A smaller and more conceptual literature suggests that provenance also affects social or behavioral variety, but this dimension is currently less directly operationalized than lexical diversity or entropy and should be presented as a motivated design input rather than a settled metric."
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - ChatGPT is incredible (at being average) (2025)
    - The GenAI Future of Consumer Research (2025)

**Writing notes**: Frame L_auth as a stage-agnostic descriptive synthesis, not a discovered law. Make the architecture explicit: D1 Provenance Ratio and D4 Social Behavioral Diversity are upstream design-level inputs; D2 Lexical Diversity and D3 Entropy are downstream measurable outcomes. The strongest evidence chain in the selected papers is D1 to D2/D3, especially via The Curious Decline of Linguistic Diversity. The evidence base for D4 is materially thinner and more conceptual, so say that openly rather than overstating it. Do not describe L_auth as a detection tool. Also note that D2 and D3 are related rather than fully independent, with the entropy-TTR paper implying possible redundancy; this is exactly why weight calibration should be stated as future work rather than implied to be solved already.

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
    - Zephyr: Direct Distillation of LM Alignment (2023)

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

## Beat 6: CampusGo as Design Proposal

**Anchor paper**: Position: Data Authenticity, Consent, & Provenance for AI are all broken: what will it take to fix them?
  Why: This paper most directly frames the design requirements relevant to CampusGo by arguing that AI data authenticity, consent, and provenance are currently fragmented and need unified treatment. It motivates a platform proposal without implying that any platform solution, including CampusGo, is already validated.

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
     Role: Anchor paper for Beat 6: AI data authenticity, consent, and provenance are currently fragmented, so any collection platform needs these design requirements baked in from the start.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → Once provenance requirements are explicit, the next question is whether intentionally collected human interaction data can actually flow into alignment pipelines; OpenAssistant provides that bridge. [thematic progression; no verified internal citation edge]
  4. [2023] OpenAssistant Conversations -- Democratizing Large Language Model Alig
     Role: Provides the bridge from collection to downstream use: intentionally gathered human conversations can become alignment corpora, so a CampusGo-style platform is not just sensing infrastructure but a potential data-generation pathway.
     Basis: thematic_progression
     Note: No direct internal citation edge was found; order is justified by the argument progression rather than by a verified citation chain.
     → A usable human-data pipeline is still not enough unless contributors remain visible as ongoing stakeholders in reuse and curation decisions. [thematic progression; no verified internal citation edge]
  5. [2023] The CARE Principles and the Reuse, Sharing, and Curation of Indigenous
     Role: Adds the stewardship boundary: contributors must remain stakeholders in how sensitive data are curated and reused, which keeps CampusGo proposal-framed rather than extractive.

**Paragraph structure**:

  ¶1: Campus-situated collection is technically plausible
    Opening: "The proposal should start with feasibility only: adjacent mobile-sensing work shows that campus-scale behavioral collection is technically plausible, not that it is automatically appropriate for AI training data."
    - Reality mining: sensing complex social systems (2006)
    - StudentLife: assessing mental health, academic performance a (2014)
  ¶2: AI-specific provenance requirements define the proposal core
    Opening: "What turns simple sensing into a defensible proposal is the provenance layer plus a downstream use case: authenticity, consent, and governance must be designed together, and OpenAssistant shows that intentionally collected human conversations can in fact become alignment data."
    - Position: Data Authenticity, Consent, & Provenance for AI ar (2024)
    - OpenAssistant Conversations -- Democratizing Large Language  (2023)
    - Perspective: The Power (Dynamics) of Open Data in Citizen Sc (2021)
  ¶3: Stewardship requirements keep CampusGo proposal-framed
    Opening: "The final move is a scope limit: stewardship principles show why CampusGo can only be presented as a motivated design direction and not as a validated intervention."
    - Still in Need of Norms: The State of the Data in Citizen Sci (2020)
    - The CARE Principles and the Reuse, Sharing, and Curation of  (2023)

**Writing notes**: Beat 6 should read as requirements engineering, not validation. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a system would need to satisfy.

---
