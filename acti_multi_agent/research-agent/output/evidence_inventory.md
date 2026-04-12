# Evidence Inventory by Beat

## Beat 1: Crisis Exists

The crisis case starts with direct demonstrations that recursive training on synthetic outputs degrades models. The strongest anchor is the Nature paper on model collapse, which establishes the phenomenon empirically and theoretically. The Curse of Recursion sharpens the mechanism by showing that rare information is forgotten first, making collapse visible as loss of tail knowledge. Self-Consuming Generative Models go MAD extends the problem beyond language to generative modeling more broadly. The theoretical prevention paper then clarifies that avoiding collapse requires favorable conditions, especially around access to real or well-controlled data, and those conditions cannot be assumed in open-web pipelines. Self-correcting loops show that active safeguards can help, which reinforces the premise that the uncontrolled default is unsafe. Finally, the homogenization paper gives an observable output-level symptom: models become more average, which is what a collapse trajectory should look like before total failure.

- **AI models collapse when trained on recursively generated data (2024)**
  Role: Anchor paper establishing that recursive training can cause model collapse
  Finding: Provides combined empirical and theoretical evidence that repeated training on model-generated data degrades distributional fidelity and amplifies errors, especially in low-probability regions.
- **The Curse of Recursion (2023)**
  Role: Shows the mechanism of forgetting under synthetic-data reuse
  Finding: Demonstrates that recursive training causes models to forget rare or tail information, linking collapse to a memorization-over-generalization dynamic.
- **Self-Consuming Generative Models go MAD (2023)**
  Role: Cross-domain empirical confirmation in generative modeling
  Finding: Shows autophagous training loops in generative image models can induce degeneration and instability, indicating collapse is not limited to one model family.
- **A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Training (2025)**
  Role: Formalizes when collapse risk appears and when it can be avoided
  Finding: Develops a theoretical framework explaining why some self-consuming setups collapse and others do not, emphasizing that prevention depends on conditions unlikely to be guaranteed on the open web.
- **Self-Correcting Self-Consuming Loops for Generative Model Training (2024)**
  Role: Shows that mitigation requires active correction rather than passive reuse
  Finding: Introduces a self-correcting mechanism that stabilizes self-consuming loops, implying collapse is a real baseline risk unless interventions are added.
- **ChatGPT is incredible (at being average) (2025)**
  Role: Supplies a behavioral signature of homogenization
  Finding: Argues that LLM outputs trend toward average, clichéd responses, offering a qualitative manifestation of the same homogenization predicted by collapse theory.

Remaining gaps:
  ⚠ Need tighter integration between collapse theory and direct web-pollution prevalence evidence.
  ⚠ Need stronger real-world estimates of how much current training data is already contaminated by AI-generated text and images.
  ⚠ Need more cross-domain evidence connecting theoretical collapse metrics to production-scale foundation-model pipelines.

---

## Beat 2: Web Drift Is Partially Measurable

This beat can support a cautious but important claim: web drift is measurable in principle, though not yet causally pinned on post-2022 AI contamination at full web scale. Dataset and pipeline papers such as Demystifying CLIP Data, RedPajama, and Yi show that provenance, filtering, and quality controls are already concrete engineering objects. That means temporal and source-based auditing is feasible. The homogenization paper adds a plausible signal family at the output level, while The GenAI Future of Consumer Research explains why one should expect average-trap dynamics once synthetic content becomes widespread. The model-collapse anchor then turns these measurements from merely descriptive indicators into variables with strategic significance. The resulting chain is not a direct proof of web-scale AI-induced drift after 2022, but it does justify the stronger methodological claim that such drift is partially measurable and should be studied with provenance plus diversity metrics.

- **Demystifying CLIP Data (2023)**
  Role: Shows that data quality and curation are measurable and materially important
  Finding: Reverse-engineers a major multimodal dataset pipeline and shows that curation choices strongly affect data quality, making provenance and filtering operational variables rather than abstractions.
- **RedPajama: an Open Dataset for Training Large Language Models (2024)**
  Role: Provides transparent web-scale corpus infrastructure for reproducible auditing
  Finding: Offers an open large-scale language-model dataset with documented sourcing and processing, enabling temporal and provenance-aware inspection of web data composition.
- **Yi: Open Foundation Models by 01.AI (2024)**
  Role: Evidence that large-scale training pipelines already depend on explicit data-engineering choices
  Finding: Describes extensive data processing and curation for foundation models, supporting the claim that web quality is not only measurable but actively managed in practice.
- **ChatGPT is incredible (at being average) (2025)**
  Role: Provides a candidate downstream signature of contamination or homogenization
  Finding: Identifies output averaging and cliché formation as observable symptoms, suggesting that entropy/diversity-style drift measures are plausible even if not yet standardized.
- **The GenAI Future of Consumer Research (2025)**
  Role: Frames drift as a broader socio-technical trajectory rather than a narrow benchmark issue
  Finding: Articulates a democratization-to-average-trap-to-collapse trajectory, motivating why changes in web content quality should be tracked longitudinally.
- **AI models collapse when trained on recursively generated data (2024)**
  Role: Supplies the reason measurement matters
  Finding: Shows that if synthetic reuse rises over time, measurable corpus drift is not just descriptive noise but a potential causal precursor to collapse.

Remaining gaps:
  ⚠ No direct post-2022 web-scale contamination audit cleanly linking temporal drift to AI-generated content reuse.
  ⚠ Weak bridge between corpus-quality measurement papers and collapse-specific papers.
  ⚠ Need standardized entropy, diversity, and provenance metrics that can distinguish AI contamination from ordinary domain shift or SEO churn.

---

## Beat 3: L_auth Is a Grounded Synthesis

L_auth is grounded because it is not introduced as a free-floating new metric; it synthesizes three already-supported literatures. First, collapse theory says outcomes depend on the mix and quality of recursively reused versus non-recursive data. Second, curation papers show that provenance and quality can be observed in actual datasets and pipelines. Third, homogenization work suggests downstream symptoms that such a variable should predict. The theoretical prevention paper provides the main logic: the relevant quantity is not simply synthetic share, but the effective availability of high-quality non-collapsing signal. Curated-data and π²/6 pathway papers refine that logic by showing authenticity must be weighted and conditional, not binary. Demystifying CLIP Data and RedPajama contribute the operational side by showing how source, filtering, and curation information can be attached to real corpora. ChatGPT is incredible (at being average) gives an output-level pattern against which the construct could be validated. Together, these papers make L_auth a grounded synthesis rather than an ad hoc term.

- **A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Training (2025)**
  Role: Primary theoretical foundation for an authenticity-weighted construct
  Finding: Shows that collapse risk depends on training conditions, especially the availability and role of non-recursive high-quality data, which directly motivates an authenticity-weighted variable.
- **Self-Consuming Generative Models with Curated Data Provably Optimize Human Preferences (2024)**
  Role: Shows why curation quality must be part of the construct, not just real-vs-synthetic source labels
  Finding: Proves that self-consuming training can remain beneficial when synthetic data are strongly curated against human preferences, implying that authenticity should be modeled as graded and quality-sensitive.
- **Universality of the π²/6 Pathway in Avoiding Model Collapse (2024)**
  Role: Supports mixture-based formulations of authenticity
  Finding: Shows that augmenting real data with synthetic data can avoid collapse under a universal pathway, supporting a weighted rather than binary conception of authentic content share.
- **Demystifying CLIP Data (2023)**
  Role: Provides observable proxy variables for the construct
  Finding: Demonstrates that data quality, provenance, and curation can be operationalized in real pipelines, offering measurable inputs for an authenticity score.
- **RedPajama: an Open Dataset for Training Large Language Models (2024)**
  Role: Provides the corpus substrate on which L_auth-like measurement could be computed
  Finding: Supplies a transparent large-scale dataset context in which source composition and filtering decisions can be tracked and reproduced.
- **ChatGPT is incredible (at being average) (2025)**
  Role: Provides an output-side validation target for the construct
  Finding: Offers homogenization as an expected downstream symptom if an authenticity-weighted training environment deteriorates, giving L_auth a plausible behavioral correlate.

Remaining gaps:
  ⚠ Need a formal definition of L_auth with explicit variables, units, and calibration procedure.
  ⚠ Need direct empirical validation that L_auth predicts collapse or homogenization better than simpler metrics such as synthetic-share percentage.
  ⚠ Need benchmarks spanning text, image, and multimodal corpora to test whether L_auth generalizes across domains.

---

## Beat 4: L_auth Can Be Tested Experimentally

An experimental program follows naturally from the existing literature. The recursive-training papers tell us what to manipulate: the proportion and quality of generated data reintroduced into training. The forgetting paper tells us what to measure: tail recall, diversity loss, and degradation of rare knowledge. Theoretical work says these outcomes should depend on boundary conditions, which is exactly where L_auth becomes useful as a structured treatment variable. Dataset-pipeline papers show that provenance and curation features can be tracked well enough to build controlled train/test regimes. Finally, self-correcting loops provide a ready-made intervention arm, allowing the experiment to compare low-L_auth recursive training, high-L_auth curated training, and corrected-recursion training. That makes beat 4 stronger than a speculative methods section: it is a falsifiable program built directly out of the current evidence base.

- **AI models collapse when trained on recursively generated data (2024)**
  Role: Defines the basic experimental manipulation and expected failure mode
  Finding: Establishes recursive training on generated data as a controllable intervention with measurable degradation outcomes.
- **The Curse of Recursion (2023)**
  Role: Specifies sensitive dependent variables for evaluation
  Finding: Shows that rare-event forgetting is an early and informative collapse indicator, suggesting concrete evaluation metrics for an L_auth experiment.
- **Self-Correcting Self-Consuming Loops for Generative Model Training (2024)**
  Role: Provides a positive-control intervention arm
  Finding: Demonstrates a stabilizing mechanism for self-consuming loops, enabling experiments that compare unmanaged recursion against corrected recursion.
- **A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Training (2025)**
  Role: Supplies hypotheses about boundary conditions
  Finding: Predicts that collapse outcomes depend on data quality and training conditions, which can be encoded as experimentally varied L_auth levels.
- **Demystifying CLIP Data (2023)**
  Role: Shows how to instrument provenance and curation variables in practice
  Finding: Provides evidence that curation attributes can be recovered and manipulated, making authenticity-weighted dataset construction experimentally feasible.
- **RedPajama: an Open Dataset for Training Large Language Models (2024)**
  Role: Offers a reproducible large-scale corpus base for implementation
  Finding: Supports the feasibility of building transparent train/validation splits where source composition and contamination controls can be documented.

Remaining gaps:
  ⚠ No standard benchmark yet combines recursive exposure, provenance labels, and downstream collapse metrics in one public protocol.
  ⚠ Need clearer methods for estimating hidden synthetic contamination in ostensibly human corpora.
  ⚠ Need longitudinal experiments large enough to separate collapse effects from normal scaling-law improvements or domain adaptation.

---

## Beat 5: Mitigation Requires Curation and Provenance, Not Simple Filtering

The solution beat should argue against simplistic detector-first or filter-only strategies and toward a layered curation regime. The theoretical prevention paper says collapse avoidance depends on conditions, which makes one-off cleanup inadequate. Curated synthetic data can still be useful, but only when quality control is strong enough to preserve human-preference signal. Self-correcting loops and the π²/6 pathway suggest two complementary tactics: active correction during recursive training and maintaining a sufficiently strong stream of real data. Demystifying CLIP Data, Yi, and RedPajama then move the argument from theory to operations by showing that provenance, curation, and transparent dataset construction are implementable. The resulting logic is that mitigation is not merely about detecting AI text after the fact; it is about preserving authentic signal through source-aware data governance, reproducible corpus construction, and controlled synthetic augmentation.

- **A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Training (2025)**
  Role: Main theoretical guide for prevention strategy
  Finding: Argues that prevention is possible only under specific conditions tied to data composition and training design, implying governance and curation are first-order requirements.
- **Self-Consuming Generative Models with Curated Data Provably Optimize Human Preferences (2024)**
  Role: Supports curated synthetic data as a conditional solution
  Finding: Shows that synthetic data need not be harmful if aggressively curated against human preferences, reframing the solution as selective reuse rather than blanket prohibition.
- **Self-Correcting Self-Consuming Loops for Generative Model Training (2024)**
  Role: Supports active correction mechanisms
  Finding: Demonstrates that self-consuming loops can be stabilized by explicit corrective procedures, suggesting monitoring and intervention can reduce collapse risk.
- **Universality of the π²/6 Pathway in Avoiding Model Collapse (2024)**
  Role: Supports mixed real-plus-synthetic training as a viable design principle
  Finding: Provides theoretical evidence that adding sufficient real data alongside synthetic data can preserve model quality, favoring mixture management over naive filtering.
- **Demystifying CLIP Data (2023)**
  Role: Supports provenance-aware data governance
  Finding: Shows that data pipeline transparency and curation materially affect quality, implying prevention must begin at collection and filtering stages.
- **Yi: Open Foundation Models by 01.AI (2024)**
  Role: Shows operational feasibility of large-scale data governance
  Finding: Documents a real foundation-model pipeline where extensive data engineering is already central, indicating that provenance-heavy mitigation is practical at scale.
- **RedPajama: an Open Dataset for Training Large Language Models (2024)**
  Role: Supports open auditing and reproducibility as mitigation infrastructure
  Finding: Provides a transparent corpus basis for contamination audits, mitigation ablations, and shared evaluation protocols.

Remaining gaps:
  ⚠ Need robust provenance standards that work across text, image, audio, and multimodal web data.
  ⚠ Need evidence on cost, scalability, and incentive compatibility of curation-heavy defenses for frontier model developers.
  ⚠ Need stronger comparisons between provenance-aware governance and detector-only or watermark-only approaches under adversarial adaptation.

---

## Suggested Paper Structure

- section_1_crisis: ~6 papers, 4-5 pages
- section_2_measurement: ~6 papers, 3-4 pages
- section_3_synthesis: ~6 papers, 3-4 pages
- section_4_experiment: ~6 papers, 4-5 pages
- section_5_solution: ~7 papers, 3-4 pages