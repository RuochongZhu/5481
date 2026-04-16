# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Model Collapse and Contamination Risk

**Anchor paper**: AI models collapse when trained on recursively generated data
  Why: Best category-A anchor for Beat 1 because it consolidates the recursive synthetic-reuse literature into a widely recognized collapse result, giving the motivation section a clear starting point while still allowing an explicit later qualification that the result applies to indiscriminate reuse rather than all synthetic-data practice.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Opens the beat with the core warning: recursive training on model-generated data erases low-probability tails and induces forgetting, establishing collapse as a plausible failure mode of self-consuming pipelines.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → This initial warning is then broadened and stabilized by a higher-visibility account that frames tail-loss under recursive reuse as a general model-collapse risk rather than a one-off artifact.
  2. [2024] AI models collapse when trained on recursively generated data
     Role: Anchor paper that crystallizes the main motivation claim: indiscriminate reuse of generated data can drive irreversible collapse, especially through loss of distributional diversity.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Before bridging from recursive training loops to claims about polluted information environments, the literature itself imposes a key limit: these results mainly show the danger of uncontrolled self-consumption, not that all synthetic data use is harmful.
  3. [2024] Self-Correcting Self-Consuming Loops for Generative Model Training
     Role: Provides the explicit scope-limiting step required before category B: self-correcting loops can stabilize recursive training, so collapse is not inevitable when corrective structure is present.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → With that boundary stated, the motivation question becomes narrower and more empirical: where do real information environments show enough synthetic encroachment to create practical contamination pressure?
  4. [2025] Quantifying Large Language Model Usage in Scientific Papers
     Role: Supplies a concrete but bounded bridge into category B by showing measurable LLM modification in scientific writing, indicating contamination pressure in one consequential information environment without proving universal web-scale pollution.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Scientific text is one specific environment; the next issue is whether contamination can also distort what retrieval systems expose users to when broader corpora are polluted.
  5. [2026] Retrieval Collapses When AI Pollutes the Web
     Role: Shows a downstream consequence of contamination pressure rather than simple prevalence: when web pools are sufficiently polluted, retrieval exposure can become even more contaminated than the underlying corpus, creating deceptively healthy outputs.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Even so, polluted retrieval pools do not by themselves prove ubiquitous contamination, which is why the literature often turns to filtering and detection as a reactive line of defense.
  6. [2023] Paraphrasing evades detectors of AI-generated text, but retrieval is a
     Role: Closes the chain by showing the limits of reactive filtering: paraphrasing can evade multiple AI-text detectors, although retrieval-based defense can recover some robustness, so detection is fragile rather than impossible.
     Basis: thematic_progression

**Paragraph structure**:

  ¶1: Recursive synthetic reuse creates a real collapse risk, but the literature also contains explicit counterexamples showing that synthetic data is not uniformly destructive.
    Opening: "Related work first establishes why recursive self-reuse is a credible failure mode, then immediately narrows that claim by distinguishing indiscriminate self-consumption from corrected or curated synthetic-data regimes."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Self-Improving Diffusion Models with Synthetic Data (2024)
  ¶2: Evidence of contamination pressure in information environments is growing, but it is still partial, domain-specific, and not yet a definitive proof of universal web-scale pollution.
    Opening: "The bridge from collapse theory to live corpora is suggestive rather than complete: several studies document meaningful synthetic encroachment in specific environments, and retrieval work shows why even partial pollution can matter operationally."
    - Quantifying Large Language Model Usage in Scientific Papers (2025)
    - 74% of New Webpages Include AI Content (Study of 900k Pages) (2025)
    - AI See What You Did There – The Prevalence of LLM-Generated  (2026)
    - Retrieval Collapses When AI Pollutes the Web (2026)
  ¶3: Reactive filtering is only a partial safeguard because detectors are attack-sensitive, cooperation-dependent, and strongly domain-conditional.
    Opening: "A final line of work asks whether contamination can simply be detected and filtered away, and the answer is mixed: defenses exist, but they are brittle enough that they cannot serve as the sole remedy."
    - Paraphrasing evades detectors of AI-generated text, but retr (2023)
    - A Watermark for Large Language Models (2023)
    - Detecting AI-Generated Text: Factors Influencing Detectabili (2025)

**Writing notes**: Keep the prose explicitly motivational, not evidentiary for the paper's main post-training claim. The beat should read as a three-step chain: collapse risk under recursive reuse; partial and still incomplete evidence that some information environments are already under contamination pressure; then the fragility of detection-based cleanup. Be explicit about limits at each step. Do not claim all synthetic data is harmful: paragraph 1 should cite self-correcting loops, curated self-consuming training, and self-improving diffusion as counterevidence. Do not claim web-scale contamination is settled: paragraph 2 should say the evidence is strongest in bounded domains such as scientific papers and MOOCs, with webpage and retrieval studies suggesting broader pressure but not proving universal contamination. Do not claim detection is impossible: paragraph 3 should note that paraphrasing breaks many detectors, yet retrieval-based defense and watermarking can still help under some conditions. The supplied candidate set does not include a dedicated pi^2/6 mixed-real-plus-synthetic counterexample, so if outside citations are allowed in drafting, add that paper alongside the self-correcting and curated-synthetic counterexamples. Avoid using perception/labeling studies as proof of contamination prevalence. End the beat with a cautionary limitation, not a thesis defense: these studies motivate concern and scoping, but they are not the direct evidence base for Beats 4-5.

---

## Beat 2: Partial Measurability of Web Drift

**Anchor paper**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Why: It is the clearest content-level example of measurable longitudinal change within a stable web genre, making it a strong anchor for the beat's narrow claim: drift can be observed in bounded slices of the web, but that does not amount to proof of web-wide pretraining contamination.

**Narrative spine** (6 papers):

  1. [2022] Towards robust complexity indices in linguistic typology
     Role: Opens with the measurement problem: corpus-level diversity and complexity indicators differ in robustness, so any drift argument depends on which proxy is being used and how stable it is.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once proxy sensitivity is acknowledged, the next step is to inspect a web domain that can actually be followed over time rather than inferred only from abstract corpus statistics.
  2. [2021] WWW - Privacy Policies over Time: Curation and Analysis of a Million-D
     Role: Provides a curated longitudinal web dataset in a stable genre, showing that web change can sometimes be measured directly when collection and curation are controlled.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Using that curated corpus, later work moves from dataset construction to substantive measurement of how the content itself changed across decades.
  3. [2023] Privacy Policies across the Ages: Content of Privacy Policies 1996–202
     Role: Anchor example of bounded, content-level drift: privacy policies measurably changed from 1996 to 2021, illustrating that longitudinal web drift is observable in some subdomains.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But a well-tracked genre is still only one slice of the web, so the narrative next turns to crawl-derived corpora, where the practical question becomes what modern web curation actually encounters.
  4. [2021] Documenting Large Webtext Corpora: A Case Study on the Colossal Clean 
     Role: Shifts from longitudinal observation to crawl-curation practice by showing that a major webtext corpus contains unexpected content and filtering artifacts, making data quality concerns concrete for pretraining pipelines.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → However, artifacts in one crawl-derived corpus do not establish web-wide degradation, which is why later work asks whether stronger filtering and deduplication can still produce effective web-only training data.
  5. [2023] The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora w
     Role: Introduces required counterevidence: properly filtered and deduplicated web data can still train strong models, narrowing the claim from demonstrated failure to rising risk and curation dependence.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → FineWeb extends this argument at larger scale, reinforcing that measurable drift and curation pressure do not by themselves imply that the usable web text pool has already collapsed.
  6. [2024] The FineWeb Datasets: Decanting the Web for the Finest Text Data at Sc
     Role: Ends on the strongest modern crawl-curation counterpoint: large-scale filtered Common Crawl data remains highly useful, so the honest conclusion is partial and indirect observability of drift, not decisive proof of web-wide contamination.
     Basis: verified_citation
     → Taken together, these studies motivate concern and measurement efforts, but the corpus contains no post-2022 web-scale contamination audit, so this beat should close on scope rather than causal certainty.

**Paragraph structure**:

  ¶1: Measurement proxies can suggest distributional change, but they are indirect and method-sensitive.
    Opening: "Before asking whether the web is drifting in ways relevant to language-model training, this literature first shows that the available textual proxies for diversity, complexity, and distribution shift are informative but not fully robust."
    - Towards robust complexity indices in linguistic typology (2022)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Entropy and type-token ratio in gigaword corpora (2025)
    - A Theoretical Framework for Statistical Evaluability of Gene (2026)
  ¶2: Longitudinal web observations show real change in bounded domains, but still fall short of a web-wide contamination audit.
    Opening: "When the corpus shifts from abstract proxy work to longitudinal observation, the evidence becomes more concrete: several studies document substantial temporal change in specific web subdomains and platform ecosystems."
    - WWW - Privacy Policies over Time: Curation and Analysis of a (2021)
    - Privacy Policies across the Ages: Content of Privacy Policie (2023)
    - "Way back then": A Data-driven View of 25+ years of Web Evol (2022)
    - Event Detection in Wikipedia Edit History Improved by Docume (2021)
    - Evolution of diversity and dominance of companies in online  (2021)
    - The Rise of AI-Generated Content in Wikipedia (2024)
  ¶3: Crawl-curation practice reveals data-quality and access pressures, yet the strongest modern results still show filtered web data training strong models.
    Opening: "The most practically relevant papers then turn from observing change to building pretraining corpora, where they find curation artifacts, changing consent conditions, and composition effects—but also strong counterevidence that filtered web text remains highly useful."
    - Documenting Large Webtext Corpora: A Case Study on the Colos (2021)
    - The RefinedWeb Dataset for Falcon LLM: Outperforming Curated (2023)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)
    - Consent in Crisis: The Rapid Decline of the AI Data Commons (2024)
    - Training Models on Dialects of Translationese Shows How Lexi (2026)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)

**Writing notes**: Write this beat explicitly as background motivation, not as the evidence base for the main post-training claim. The argumentative arc should be: proxy measures are imperfect; some web subdomains show clear longitudinal change; crawl builders face real quality and consent pressures; yet RefinedWeb and FineWeb are mandatory counterevidence showing that filtered web data still trains strong models. State plainly that measurable drift is partial and indirect, not decisive proof of web-wide contamination, and that no post-2022 web-scale contamination audit exists in the corpus. If a concluding sentence is needed, use a scope boundary such as: 'Current work motivates concern and better auditing, but it does not demonstrate web-wide pretraining degradation.'

---

## Beat 3: L_auth Framework Definition

**Anchor paper**: Towards robust complexity indices in linguistic typology
  Why: It most directly justifies treating lexical diversity as a robust descriptive dimension rather than relying on fragile corpus-size-sensitive proxies, which is central to D2 in L_auth.

**Narrative spine** (5 papers):

  1. [2022] Towards robust complexity indices in linguistic typology
     Role: Defines D2 as a robustness-aware lexical-diversity dimension and cautions against naive corpus metrics such as simple TTR or raw word entropy.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If D2 needs robust measurement, L_auth also needs a distributional uncertainty dimension that is explicitly quantifiable, which motivates D3.
  2. [2020] Analyzing the Influence of Hyper-parameters and Regularizers of Topic 
     Role: Supplies D3 with an entropy-based ingredient by showing Renyi entropy can track meaningful structure under controlled modeling variation, making entropy a plausible measurable outcome.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → With D2 and D3 framed as measurable outcomes, the next step is to show that synthetic post-training mixtures actually move those outcomes in practice.
  3. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Connects the framework to LLM-relevant evidence by showing recursive synthetic training reduces linguistic diversity, making D2/D3 outcome shifts empirically salient.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once diversity decline is observable, provenance stops being a background detail and becomes a candidate input variable for the framework.
  4. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Provides the core recursive-training collapse account that motivates D1 Provenance Ratio: when generated data feeds future training, tail support can disappear.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If provenance composition matters, then the way data is curated and socially filtered also becomes a plausible design-level input rather than a downstream afterthought.
  5. [2024] Self-Consuming Generative Models with Curated Data Provably Optimize H
     Role: Bridges from raw provenance counts to D4 Social Behavioral Diversity by arguing that curated, user-shaped self-consuming loops can change collapse dynamics, suggesting composition depends on who contributes and how selection occurs.
     Basis: verified_citation
     → This is also the scope boundary: L_auth synthesizes input and outcome dimensions for post-training data composition, but does not yet calibrate their weights or claim a universal law.

**Paragraph structure**:

  ¶1: Define the measurable outcome side of L_auth: D2 Lexical Diversity and D3 Entropy.
    Opening: "L_auth begins by treating lexical diversity and entropy as measurable emergent outcomes of post-training data composition, while admitting that not all common proxies are equally robust."
    - Towards robust complexity indices in linguistic typology (2022)
    - Lexical and Statistical Analysis of Bangla Newspaper and Lit (2025)
    - Lexical Diversity of Czech L2 Texts at Different Proficiency (2025)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - Efficient Perplexity Bound and Ratio Matching in Discrete Di (2025)
  ¶2: Show why those outcomes matter under synthetic recursion and provenance dilution.
    Opening: "Recursive-training studies then make the framework operational: as synthetic text recirculates, diversity declines and collapse-like distributional signatures become observable."
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Learning by Surprise: Surplexity for Mitigating Model Collap (2024)
  ¶3: Promote composition variables to inputs: D1 Provenance Ratio and D4 Social Behavioral Diversity.
    Opening: "Taken together, mitigation and curation papers suggest that post-training composition has at least two controllable inputs—how much generated material is used and how socially curated or behaviorally diverse that material is—while also marking the limits of current evidence."
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Self-Improving Diffusion Models with Synthetic Data (2024)

**Writing notes**: Keep the section definitional, not triumphalist. Present D1 and D4 as design-level inputs, and D2 and D3 as measurable outcomes. Use the collapse papers to motivate why provenance and curation belong in the framework, not to claim validated downstream model gains. End explicitly that L_auth is a synthesis for fine-tuning/post-training data composition, not a standalone law across all training stages, and that weight calibration across the four dimensions is future work.

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
     → With a controlled preference objective in place, the strongest next baseline is Zephyr, which applies AI-feedback distillation on top of a DPO-style alignment recipe while still leaving inference-time compute fixed so rival decoding explanations can be named explicitly later. [verified citation order]
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

**Writing notes**: Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. Handle LIMA explicitly as a cross-beat paper: in Beat 4 it supports the broader claim that curation matters, while in Beat 5 it only motivates why a provenance-sensitive intervention is worth testing. State explicitly that the pilot fixes inference-time compute, prompt/interface conditions, and retrieval usage precisely because self-consistency, structured CoT, and DEL-ToM-style inference-time scaling are live rival explanations; the corpus does not let the paper apportion causal weight among those mechanisms after the fact. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

---

## Beat 6: CampusGo as Deployed Core Contribution

**Anchor paper**: Position: Data Authenticity, Consent, & Provenance for AI are all broken: what will it take to fix them?
  Why: Use Longpre et al. as the requirement-setting anchor: it crisply diagnoses the AI-side failures in authenticity, consent, and provenance that CampusGo is designed to operationalize against. It should frame the problem and the design criteria, not stand in as evidence that CampusGo solves the full agenda or improves downstream models.

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

**Writing notes**: Beat 6 should read as deployed requirements engineering, not downstream validation. Longpre et al. (2024) is the diagnosis anchor that names the broken properties of present AI data pipelines; CampusGo is positioned as one concrete operationalization of those requirements for socially grounded post-training data, not as proof that the full authenticity agenda is solved. Start from campus feasibility, pivot to the AI-specific provenance/authenticity problem, and then use OpenAssistant as the concrete bridge showing that intentionally collected human interactions can become alignment corpora. End on governance and stewardship constraints. Do not claim that any existing paper proves CampusGo will improve downstream models; the literature only motivates what such a deployed system would need to satisfy.

---

## Beat 7: Competing Explanations and Honest Scoping

**Anchor paper**: Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
  Why: This paper is the cleanest anchor for adversarial scoping because it directly argues that test-time compute can rival or exceed parameter scaling as a source of capability gains. That makes inference-time scaling a genuine alternative mechanism that the thesis should narrow around rather than dismiss.

**Narrative spine** (6 papers):

  1. [2022] Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
     Role: Establishes the first honest competing mechanism: substantial reasoning gains can appear at inference time through prompting alone, without changing the training corpus.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If prompting already unlocks latent reasoning, the next question is whether allocating more inference-time exploration can improve performance further without retraining.
  2. [2022] Self-Consistency Improves Chain of Thought Reasoning in Language Model
     Role: Shows that extra sampling and aggregation over multiple reasoning traces improves performance, turning inference-time search into a concrete alternative explanation for gains.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once multiple sampled traces matter, test-time compute stops looking like a minor decoding detail and starts looking like a bona fide scaling axis.
  3. [2024] Scaling LLM Test-Time Compute Optimally can be More Effective than Sca
     Role: Makes the core adversarial claim explicit: optimally scaling test-time compute can be more effective than scaling model parameters, so capability gains cannot be attributed to data factors alone.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That framing naturally leads to work operationalizing 'more thinking' through simple, controllable inference budgets.
  4. [2025] s1: Simple test-time scaling
     Role: Provides a practical extended-thinking result in which budget forcing and small supervised tuning produce large reasoning gains, reinforcing that compute allocation at inference can materially change outcomes.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But inference budget is not the only competing mechanism: post-training procedures can also induce stronger reasoning behavior that would confound any data-composition story.
  5. [2025] DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcem
     Role: Adds a second strong alternative mechanism by showing that reinforcement learning can induce powerful reasoning behavior, suggesting that post-training optimization and extended reasoning traces may drive gains independently of corpus composition.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Crucially, these alternative mechanisms are not limited to math-style tasks; emerging work carries them into social and belief-tracking settings as well.
  6. [2025] DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynam
     Role: Extends the competing-mechanism argument into Theory-of-Mind reasoning, showing that inference-time scaling can improve social reasoning without architectural change; this is the key scope limiter for any broader social-capability thesis.
     Basis: thematic_progression
     → This is the beat's scope boundary: if social-reasoning gains can arise from inference-time scaling alone, then L_auth should be narrowed to fixed-compute data-composition effects rather than presented as the sole driver of downstream capability.

**Paragraph structure**:

  ¶1: Inference-time reasoning methods already provide a strong alternative explanation for capability gains.
    Opening: "Before attributing improved reasoning to training-data composition, prior work shows that prompting, diverse sampling, and more structured reasoning at inference time can substantially raise performance even when the underlying model and corpus stay fixed."
    - Chain-of-Thought Prompting Elicits Reasoning in Large Langua (2022)
    - Self-Consistency Improves Chain of Thought Reasoning in Lang (2022)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - Scaling LLM Test-Time Compute Optimally can be More Effectiv (2024)
  ¶2: Extended thinking, RL-based reasoning, and social-reasoning-specific scaling results force a narrower claim centered on fixed-compute comparisons.
    Opening: "The scoping pressure becomes stronger once test-time budgets, reasoning-oriented post-training, and emerging social-reasoning results are considered together: these mechanisms can generate real gains on their own, so any positive thesis should be limited to what data composition explains after holding inference compute and post-training regime fixed."
    - s1: Simple test-time scaling (2025)
    - DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via  (2025)
    - DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning (2025)
    - The Pragmatic Mind of Machines: Tracing the Emergence of Pra (2025)

**Writing notes**: Order the beat as an honest narrowing move, not a rebuttal. Emphasize that direct internal citation links were not provided, so the spine follows thematic progression and a historical build-up from prompting to search, then to explicit test-time compute scaling, then to post-training and social-reasoning extensions. State plainly that inference-time scaling is a genuine alternative mechanism. Do not imply CoT or test-time compute are minor effects. Use the DEL-ToM result to make the crucial adversarial point that social reasoning itself may improve from inference-time scaling, which means L_auth should be framed only as a data-composition effect under fixed model, fixed post-training recipe, and fixed inference budget. Also admit that the social/pragmatic evidence base here is thinner than the general reasoning evidence, so the final sentence should mark a scope boundary rather than claim a decisive causal ranking among mechanisms.

---
