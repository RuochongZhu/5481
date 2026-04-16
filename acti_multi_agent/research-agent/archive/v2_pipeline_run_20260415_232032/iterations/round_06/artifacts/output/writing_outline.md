# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Model Collapse and Contamination Risk

**Anchor paper**: AI models collapse when trained on recursively generated data
  Why: It is the clearest high-visibility synthesis of the recursive-reuse collapse mechanism and is the best anchor for stating the narrow motivation claim: indiscriminate self-reuse can erase distributional tails, which motivates concern without implying that all synthetic-data use is harmful.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Opens the beat with the basic mechanism: recursive training on model outputs can make generative models forget rare but important parts of the original distribution.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Nature 2024 then turns this from an early warning into a more consolidated empirical-and-theoretical statement about indiscriminate recursive reuse.
  2. [2024] AI models collapse when trained on recursively generated data
     Role: Anchor paper that sharpens the motivation: recursive synthetic reuse can cause irreversible tail loss and homogenization under uncontrolled retraining.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But the relevant claim must be narrowed before leaving the lab setting: the collapse literature mainly establishes risk under poorly controlled self-reuse, not universal failure of all synthetic-data regimes.
  3. [2024] Self-Correcting Self-Consuming Loops for Generative Model Training
     Role: Explicit scope-limiting counterevidence: self-consuming loops can be stabilized if correction is introduced, so collapse is conditional rather than inevitable.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → With that limitation stated, the next question is not whether synthetic data always fails, but whether real information environments are accumulating enough machine-generated material for uncontrolled reuse to become plausible.
  4. [2025] Quantifying Large Language Model Usage in Scientific Papers
     Role: Provides a bounded real-world bridge by showing measurable LLM-written or LLM-modified contamination in one concrete corpus, scientific papers.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Evidence outside specific corpora remains incomplete, yet retrieval studies suggest that even partial contamination can be amplified by downstream systems.
  5. [2026] Retrieval Collapses When AI Pollutes the Web
     Role: Supplies the strongest category-B system-level bridge: in retrieval pipelines, contaminated pools can yield much higher contaminated exposure, though this is still a pipeline-specific result rather than proof of universal web-scale contamination.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If contamination can enter and then be amplified by retrieval, a natural response is filtering; the final step asks how reliable detector-based filtering actually is under adaptation.
  6. [2023] Paraphrasing evades detectors of AI-generated text, but retrieval is a
     Role: Closes on the limits of reactive filtering: detector-only approaches can be defeated by paraphrasing, while retrieval-based defenses recover some robustness, so detection is fragile rather than impossible.
     Basis: thematic_progression
     → This motivation beat should therefore end on a scoped takeaway: recursive synthetic reuse is a plausible risk mechanism, contamination signals exist in bounded environments, and current filtering defenses remain conditional and attack-sensitive.

**Paragraph structure**:

  ¶1: Recursive synthetic reuse can collapse models under indiscriminate retraining, but the literature itself already shows that this is a conditional risk rather than a blanket indictment of all synthetic data.
    Opening: "The model-collapse literature motivates caution about recursive synthetic reuse, while also supplying its own first scope limit: the strongest failure results concern uncontrolled self-recycling, not every pipeline that mixes in generated data."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Self-Improving Diffusion Models with Synthetic Data (2024)
  ¶2: The bridge from collapse theory to real information environments is suggestive but incomplete: several studies report measurable contamination in specific corpora and systems, yet they do not prove universal web-scale takeover.
    Opening: "Outside controlled retraining loops, the evidence base is thinner and more domain-specific, but it does indicate growing contamination pressure in scientific text, newly created webpages, and retrieval pipelines."
    - Quantifying Large Language Model Usage in Scientific Papers (2025)
    - 74% of New Webpages Include AI Content (Study of 900k Pages) (2025)
    - More Articles Are Now Created by AI Than Humans (2025)
    - Retrieval Collapses When AI Pollutes the Web (2026)
  ¶3: Reactive filtering is therefore relevant but not decisive: detectors can succeed in constrained settings, yet adversarial rewriting and domain shifts make detector-only governance brittle.
    Opening: "A natural response is to detect and filter synthetic content, but the detection literature mostly points to a moving-target defense: useful in scoped domains, breakable under paraphrase or distribution shift, and not a clean substitute for upstream control."
    - Paraphrasing evades detectors of AI-generated text, but retr (2023)
    - A Watermark for Large Language Models (2023)
    - Detecting AI-Generated Text: Factors Influencing Detectabili (2025)
    - Distinguishing Reality from AI: Approaches for Detecting Syn (2024)
    - Detecting AI-Generated Code Assignments Using Perplexity of  (2024)
    - Phishing Detection 2.0: A Natural Language Processing Approa (2023)

**Writing notes**: Keep this beat explicitly motivational. Do not present pretraining collapse papers as direct proof of the paper's later post-training claim. State the scope boundary in plain language: the literature mainly shows that indiscriminate recursive reuse is risky; it does not show that all synthetic data is harmful. In paragraph 1, foreground counterevidence rather than burying it: self-correcting loops, curated self-consuming training, and controlled synthetic guidance all show pathways that avoid collapse. The requested mixed real-plus-synthetic pi^2/6 counterexample is not present in the provided paper set, so add that exact citation during manuscript drafting; this chain currently represents that limiting idea with the available self-correcting and curated-data papers. In paragraph 2, be honest that contamination evidence is domain-specific and partly detector-dependent; say that scientific writing, sampled webpages, and retrieval systems show pressure signals, but universal web contamination is not established. In paragraph 3, avoid saying detection is impossible: watermarking and narrow-domain classifiers can work, yet paraphrasing and domain variation make reactive filtering fragile under adversarial conditions. Omit social-perception papers here unless framed as downstream consequences rather than proof of contamination prevalence. Use the final sentence to hand off to later beats by saying this literature motivates upstream controls and careful evaluation, not that it already validates downstream performance harms.

---

## Beat 2: Partial Measurability of Web Drift

**Anchor paper**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Why: It is the clearest anchor for this beat because it operationalizes long-horizon content drift in a large, curated slice of the web, while still making the key scope point: measurable change is visible in a bounded genre, not equivalent to proof of web-wide contamination.

**Narrative spine** (6 papers):

  1. [2022] Towards robust complexity indices in linguistic typology
     Role: Opens with the measurement problem: corpus-level drift is only observable through proxy metrics, and those proxies vary in robustness to corpus size and content changes.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If drift metrics are themselves fragile, the next question is what kinds of degradation they might actually detect when text production becomes more synthetic.
  2. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Shows that recursive synthetic training can reduce lexical, syntactic, and semantic diversity, motivating why diversity-style proxies are worth monitoring while stopping short of any claim about the open web.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But synthetic-recursion experiments are not web audits, so the argument must move from laboratory-style proxy behavior to longitudinal observations of real web domains.
  3. [2021] WWW - Privacy Policies over Time: Curation and Analysis of a Million-D
     Role: Provides a large curated longitudinal web subcorpus in which content change can actually be tracked over time, making web drift measurable in at least one stable genre.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That longitudinal setup is then extended by later work, which confirms that the observed changes persist across a longer historical window.
  4. [2023] Privacy Policies across the Ages: Content of Privacy Policies 1996–202
     Role: Anchor paper: confirms substantial multi-decade content evolution in privacy policies, giving the beat its strongest concrete example of measurable but genre-bounded web drift.
     Basis: verified_citation
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Even so, one genre cannot stand in for the whole web, so the literature next broadens to macro-level observations about how the web's composition changes over time.
  5. [2022] "Way back then": A Data-driven View of 25+ years of Web Evolution
     Role: Broadens from a single document genre to macro web evolution, showing long-run shifts in the kinds of sites that dominate attention and therefore plausibly alter what crawls collect.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Those broad shifts matter for language-model training only indirectly; the operational question is what actually enters crawled corpora and how filtering changes that picture.
  6. [2021] Documenting Large Webtext Corpora: A Case Study on the Colossal Clean 
     Role: Bridges observation to practice by showing that a major crawl-derived corpus can contain benchmark leakage, machine-generated text, and skew introduced by filtering choices, while still not constituting a post-2022 web-scale contamination audit.
     Basis: thematic_progression
     → Later web-only curation work, especially RefinedWeb and FineWeb, complicates any simple decline story: filtered web data can still train strong models, so the narrow conclusion is partial and indirect measurability of rising risk rather than demonstrated web-wide contamination.

**Paragraph structure**:

  ¶1: Measurement proxies can indicate drift, but only indirectly and with substantial dependence on metric choice.
    Opening: "Before asking whether the web is drifting in ways relevant to pretraining, the literature first shows that drift is observable only through imperfect textual proxies whose stability depends on the metric and setting."
    - Towards robust complexity indices in linguistic typology (2022)
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Entropy and type-token ratio in gigaword corpora (2025)
  ¶2: Longitudinal studies of bounded web slices show real content change over time, but the evidence is genre-specific rather than web-wide.
    Opening: "Once the measurement caveat is clear, longitudinal web studies do find substantial change—but mostly in curated subdomains where repeated observation is feasible."
    - WWW - Privacy Policies over Time: Curation and Analysis of a (2021)
    - Privacy Policies across the Ages: Content of Privacy Policie (2023)
    - "Way back then": A Data-driven View of 25+ years of Web Evol (2022)
    - Evolution of diversity and dominance of companies in online  (2021)
    - Event Detection in Wikipedia Edit History Improved by Docume (2021)
  ¶3: Crawl-curation papers reveal localized contamination, access, and filtering issues, yet newer filtered web datasets remain strong, so the conclusion stays narrow.
    Opening: "When the focus shifts from observing change to building pretraining corpora, the evidence becomes operational: some crawls contain leakage or synthetic content and the accessible web is changing, but improved filtering still produces highly effective web-only datasets."
    - Documenting Large Webtext Corpora: A Case Study on the Colos (2021)
    - The Rise of AI-Generated Content in Wikipedia (2024)
    - Consent in Crisis: The Rapid Decline of the AI Data Commons (2024)
    - The RefinedWeb Dataset for Falcon LLM: Outperforming Curated (2023)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)

**Writing notes**: Use this beat strictly as background motivation, not as direct evidence for any primary post-training claim. The clean argumentative arc is: proxy fragility -> bounded longitudinal drift -> crawl-curation implications. Be explicit that category D is method-thin for web drift specifically: these papers mainly justify why diversity/entropy proxies are partial instruments, not direct measurements of contamination. State clearly that synthetic-text studies show what proxy degradation could look like, but they do not demonstrate that the open web has already undergone the same process. Likewise, the privacy-policy and web-evolution papers show measurable temporal change in specific genres or macro site composition, not web-wide pretraining degradation. The C4 paper provides concrete motivation that crawl contents can include leakage, machine-generated text, and filtering bias, but it is still a corpus case study rather than a web-scale contamination audit. Include the required counterevidence plainly: RefinedWeb and FineWeb show that filtered web data still trains strong models, so observed drift signals do not by themselves prove collapse or unusable pretraining data. End the beat with the narrow scope boundary: measurable drift is partial and indirect, and no post-2022 web-scale contamination audit exists in the corpus.

---

## Beat 3: L_auth Framework Definition

**Anchor paper**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text
  Why: It is the clearest bridge paper for this beat: it connects an upstream data-composition choice (synthetic versus human text) to downstream changes in linguistic diversity, which lets L_auth define Provenance Ratio as a design input and Lexical Diversity/Entropy as emergent outcomes without overstating a universal law.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Introduces the core framework pressure: when generated data is fed back into training, tail information disappears, motivating L_auth's D1 Provenance Ratio as an upstream composition variable rather than a mere bookkeeping detail.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That theoretical warning is not enough for a framework by itself, so the next step is broader empirical confirmation that recursive synthetic training can systematically compress a model's support.
  2. [2024] AI models collapse when trained on recursively generated data
     Role: Provides the broader empirical collapse result that makes provenance-sensitive data composition a serious framework ingredient; it grounds D1 as a plausible fine-tuning design axis and cautions that narrow source loops can erase rare cases.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once provenance is treated as an upstream knob, the framework needs observable downstream consequences; the most relevant next move is to track whether linguistic diversity actually declines as synthetic share rises.
  3. [2024] The Curious Decline of Linguistic Diversity: Training Language Models 
     Role: Operational bridge from provenance to measurable outcomes: recursive training on synthetic text is shown to reduce lexical, syntactic, and semantic diversity, motivating D2 and D3 as emergent summaries of authenticity-sensitive data composition.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → But if diversity is going to serve as a framework outcome, L_auth must be careful about which diversity indices are robust enough to use across corpora and domains.
  4. [2022] Towards robust complexity indices in linguistic typology
     Role: Supplies the measurement discipline for D2 by showing that some traditional corpus indices are unstable under corpus-size and content variation, while newer lexical-diversity measures are more robust; this justifies treating lexical diversity as a designed metric family rather than a single fragile score.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Lexical diversity alone is not sufficient, however; L_auth needs a second emergent axis that captures uncertainty or spread in the token distribution without collapsing it into the same statistic.
  5. [2025] Entropy and type-token ratio in gigaword corpora
     Role: Clarifies the D2-D3 separation by showing that type-token ratio and word entropy are related but not identical corpus summaries; this supports L_auth's choice to keep Lexical Diversity and Entropy as complementary emergent outcomes rather than merge them.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → With that distinction in place, the framework can borrow a concrete entropy-oriented measurement precedent, while still admitting that calibration across tasks remains unresolved.
  6. [2020] Analyzing the Influence of Hyper-parameters and Regularizers of Topic 
     Role: Provides a usable precedent for D3: Renyi-entropy-based analysis can reveal structure and sensitivity in modeled text collections, supporting entropy as a practical ingredient in L_auth even though the exact weighting of entropy against the other dimensions is still open.
     Basis: thematic_progression
     → From here the framework should stop at synthesis: L_auth is a fine-tuning-oriented descriptive scheme for post-training data composition, not a validated standalone law, not stage-agnostic, and not yet equipped with calibrated cross-dimension weights.

**Paragraph structure**:

  ¶1: D1 Provenance Ratio as a design-level input: recursive synthetic training changes support, but those effects are modulated by curation and correction rather than fixed by law.
    Opening: "L_auth begins upstream: in fine-tuning, the proportion of human versus model-generated material is a composition choice, and recursive-training papers show that this choice can reshape the support and rarity structure a model retains."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Self-Improving Diffusion Models with Synthetic Data (2024)
    - Neon: Negative Extrapolation From Self-Training Improves Ima (2025)
  ¶2: D2 Lexical Diversity as an emergent outcome, with only indirect support for D4 Social Behavioral Diversity; current evidence shows diversity shifts under source changes, but D4 remains the thinnest dimension in this set.
    Opening: "The framework then separates upstream composition from downstream observation: if provenance and source breadth change, the first effects we can measure reliably are shifts in lexical and distributional diversity rather than a single authenticity score."
    - The Curious Decline of Linguistic Diversity: Training Langua (2024)
    - Towards robust complexity indices in linguistic typology (2022)
    - Lexical and Statistical Analysis of Bangla Newspaper and Lit (2025)
    - Lexical Diversity of Czech L2 Texts at Different Proficiency (2025)
    - Training Models on Dialects of Translationese Shows How Lexi (2026)
    - AI-generated data contamination erodes pathological variabil (2026)
  ¶3: D3 Entropy as a complementary emergent outcome and explicit scope limit: entropy-based summaries are useful ingredients, but finite-sample evaluability and cross-dimension weighting remain open.
    Opening: "Entropy gives L_auth a second emergent axis alongside lexical diversity, but the literature supports it mainly as a practical measurement ingredient, not as proof of a universal authenticity law."
    - Entropy and type-token ratio in gigaword corpora (2025)
    - Analyzing the Influence of Hyper-parameters and Regularizers (2020)
    - Renormalization Analysis of Topic Models (2020)
    - A Theoretical Framework for Statistical Evaluability of Gene (2026)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)
    - Efficient Perplexity Bound and Ratio Matching in Discrete Di (2025)

**Writing notes**: Write this beat as a careful synthesis, not a discovery claim. Define L_auth explicitly as a fine-tuning-focused descriptive framework with four dimensions: D1 Provenance Ratio and D4 Social Behavioral Diversity are ex ante data-composition inputs; D2 Lexical Diversity and D3 Entropy are ex post measurable outcomes. The strongest evidence in this set supports a pathway from provenance shifts to diversity shifts in post-training or recursive retraining settings. Be explicit that D4 is the least directly evidenced dimension here: the available papers mainly speak to curation, source breadth, and human-preference structure rather than a settled behavioral-diversity metric. Use the robust-complexity and entropy papers to justify metric families, not to claim a validated weighting scheme. End by stating plainly that L_auth is not a detection tool, not a validated standalone law, not stage-agnostic, and not yet calibrated for cross-dimension weights; extending operationalization to pretraining and learning the weights are

---

## Beat 4: Fine-tuning Data Source Affects Social Reasoning

**Anchor paper**: LIMA: Less Is More for Alignment
  Why: LIMA is the cleanest source-sensitive anchor in this set: it shows that a small amount of carefully curated human post-training data can substantially shift assistant behavior, making data provenance and curation central variables. That makes it a useful hinge between social-reasoning evaluations and later counterevidence from synthetic or AI-feedback pipelines.

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

**Writing notes**: Beat 5 must stay method-and-pilot framed. The clearest inspectable chain is benchmark sensitivity -> LIMA as quality-sensitive precedent -> DPO as controlled optimization method -> Zephyr as the strongest AI-feedback baseline, with AlpacaFarm and RLAIF used as supporting narrowing evidence rather than as extra spine detours. State explicitly that the pilot fixes inference-time compute, prompt/interface conditions, and retrieval usage precisely because self-consistency, structured CoT, and DEL-ToM-style inference-time scaling are live rival explanations; the corpus does not let the paper apportion causal weight among those mechanisms after the fact. End on limitations, not victory language: a 3B model may not separate data conditions sharply, D1 and D4 co-vary in the design, and the strongest non-human baselines come from bounded alignment tasks rather than dedicated social-reasoning comparisons.

---

## Beat 6: CampusGo as Deployed Core Contribution

**Anchor paper**: Position: Data Authenticity, Consent, & Provenance for AI are all broken: what will it take to fix them?
  Why: It is the closest paper to CampusGo's claimed contribution: it names authenticity, consent, and provenance as broken properties in AI data pipelines, letting the beat present CampusGo as deployed infrastructure that operationalizes these requirements without overstating evidence about downstream model performance.

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
  Why: DEL-ToM is the clearest scope-setting anchor because it shows social-reasoning gains from inference-time scaling alone, without changing model architecture, making it a direct competitor to any broader training-data explanation.

**Narrative spine** (4 papers):

  1. [2022] Self-Consistency Improves Chain of Thought Reasoning in Language Model
     Role: Establishes the basic adversarial premise: test-time compute over multiple reasoning paths can substantially improve reasoning, so observed gains need not come from data composition alone.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → If simple sample-and-aggregate decoding already changes outcomes, the next question is whether richer chain-of-thought structure can explain additional gains without invoking new training data.
  2. [2024] Faithful Logical Reasoning via Symbolic Chain-of-Thought
     Role: Shows that strengthening reasoning structure itself via symbolic chain-of-thought can outperform standard CoT, extending the alternative-mechanism story from more compute to better inference-time scaffolding.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → Once reasoning improves through structured test-time scaffolds, it becomes necessary to ask whether social reasoning in particular can also be unlocked this way.
  3. [2025] DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynam
     Role: Moves the competing-mechanism argument directly into Theory-of-Mind: inference-time scaling with a logic-grounded verifier improves ToM in small models, so social-reasoning gains can arise from search and verification rather than only upstream data choices.
     Basis: thematic_progression
     Note: Order is justified by the argument progression rather than a verified internal citation chain.
     → That result broadens the scope challenge: if verifier-guided scaling helps, even more elaborate meta-reasoning systems may also compete with a data-composition explanation.
  4. [2026] Aham: A Metacognitive Architecture for Latent-Steered Theory-of-Mind i
     Role: Extends the line to metacognitive and latent-steered reasoning systems, reinforcing that extended thinking itself is a plausible mechanism; this motivates an honest boundary that any thesis about data composition should be read at fixed model and inference-time budgets.
     Basis: thematic_progression
     → Taken together, these papers argue for narrowing claims to fixed-compute data-composition effects rather than treating social-reasoning gains as uniquely attributable to training data.

**Paragraph structure**:

  ¶1: Test-time compute and reasoning-trace design are genuine alternative explanations for performance gains.
    Opening: "Before attributing gains to training data composition, related work should acknowledge that decoding strategy, chain-of-thought structure, process supervision, and in-context examples can each move reasoning performance substantially."
    - Self-Consistency Improves Chain of Thought Reasoning in Lang (2022)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - Faithful Logical Reasoning via Symbolic Chain-of-Thought (2024)
    - Let's Verify Step by Step (2023)
    - How Far Can In-Context Alignment Go? Exploring the State of  (2024)
  ¶2: For social reasoning specifically, inference-time scaling, metacognitive scaffolds, steering, and process-reward RL all act as plausible competing mechanisms.
    Opening: "The strongest scope limiter comes from work showing that Theory-of-Mind and pragmatic competence can improve through test-time verification, extended meta-reasoning, internal-state steering, or specialized reinforcement learning even without a new data-composition story."
    - DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning (2025)
    - Aham: A Metacognitive Architecture for Latent-Steered Theory (2026)
    - CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind (2026)
    - Social-R1: Towards Human-like Social Reasoning in LLMs (2026)
    - The Pragmatic Mind of Machines: Tracing the Emergence of Pra (2025)
  ¶3: Model scale, modality, upstream dataset design, and training objectives remain additional explanations, while benchmark evidence shows persistent pragmatic gaps.
    Opening: "A balanced scoping paragraph should therefore end by noting that larger or multimodal models, large curated pretraining corpora, and objective-level changes are all viable sources of improvement, and none erase the remaining human-like pragmatic failures."
    - Are Vision Language Models Cross-Cultural Theory of Mind Rea (2025)
    - Relevant answers to polar questions. (2025)
    - Relevant answers to polar questions (2025)
    - CCI4.0: A Bilingual Pretraining Dataset for Enhancing Reason (2025)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)

**Writing notes**: Keep the tone concessive, not defensive. The point of this beat is to narrow the thesis: if later sections argue for data-composition effects, phrase them as effects observed under fixed model size and fixed inference-time budget, not as exclusive explanations of social-reasoning gains. DEL-ToM should be the main pivot because it most directly demonstrates ToM improvement from inference-time scaling alone. Self-Consistency and SymbCoT frame the broader test-time-compute and chain-of-thought alternative. The third and fourth spine positions then justify the explicit boundary: extended thinking, steering, RL, scale, and objective design are all live competitors. Also note that the evidence base here is heterogeneous and partly thin: several 2025-2026 papers are new, some are system papers, and two pairs are duplicate preprint/published versions (SymbCoT; Relevant answers to polar questions). In prose, prefer citing the published ACL and journal versions, while using the duplicates only if needed for metadata completeness.

---
