# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Crisis Exists

**Anchor paper**: AI models collapse when trained on recursively generated data
  Why: This is the clearest anchor for Beat 1 because it turns the model-collapse concern into high-visibility empirical evidence: recursive training on model-generated data produces irreversible defects and tail loss, making the crisis concrete rather than speculative.

**Narrative spine** (6 papers):

  1. [2023] Self-Consuming Generative Models go MAD
     Role: Introduces the core crisis mechanism: self-consuming training loops degrade precision or diversity when fresh real data is insufficient.
     → Subsequent work sharpened this intuition by showing that the danger is not just lower quality, but a structural distortion of the data distribution and the scaling laws learned from it.
  2. [2024] A Tale of Tails: Model Collapse as a Change of Scaling Laws
     Role: Reframes model collapse as tail narrowing and scaling-law decay, giving the crisis a more general theoretical language.
     → This theoretical account was then reinforced by direct empirical evidence that recursive training causes irreversible defects in learned distributions.
  3. [2024] AI models collapse when trained on recursively generated data
     Role: Provides decisive empirical confirmation that indiscriminate reuse of synthetic data causes model collapse and disappearance of distributional tails.
     → Once collapse was established as real, later papers shifted from asking whether the problem exists to asking what unusually strong safeguards would be needed to avoid it.
  4. [2024] Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinf
     Role: Shows that scaling with synthetic data requires verification and reinforcement, implying that safe reuse is conditional rather than automatic.
     → But these conditional escape routes assume that synthetic contamination can be recognized or controlled, which leads directly to the literature on detection and post-hoc defenses.
  5. [2023] Paraphrasing evades detectors of AI-generated text, but retrieval is a
     Role: Establishes that a major reactive defense is brittle: simple paraphrasing can evade AI-text detectors, even when retrieval helps in some settings.
     → Follow-on adversarial evaluations generalized this point, showing that detector fragility persists under more systematic LLM-mediated attacks.
  6. [2024] Red Teaming Language Model Detectors with Language Models
     Role: Concludes the thread by demonstrating that detector-based responses remain vulnerable to red-teaming and style-transfer attacks, underscoring that reactive solutions lag the contamination problem.

**Paragraph structure**:

  ¶1: Model collapse is a real and escalating consequence of recursive training on synthetic outputs.
    Opening: "Recent work converges on a common warning: when generative models are trained on their own outputs without enough fresh real data, quality and diversity do not compound—they erode."
    - Self-Consuming Generative Models go MAD (2023)
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
    - AI models collapse when trained on recursively generated dat (2024)
    - ChatGPT is incredible (at being average) (2025)
    - The GenAI Future of Consumer Research (2025)
  ¶2: The proposed ways to avoid collapse are highly conditional, which reinforces rather than dissolves the sense of crisis.
    Opening: "Importantly, papers that claim collapse can be mitigated do so by imposing strong assumptions—correction functions, verification, curation, or retention of original data—that are difficult to satisfy at web scale."
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Beyond Model Collapse: Scaling Up with Synthesized Data Requ (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Universality of the $π^2/6$ Pathway in Avoiding Model Collap (2024)
  ¶3: Reactive responses to synthetic contamination, especially detection-based ones, are brittle and incomplete.
    Opening: "If web-scale contamination cannot be prevented upstream, one natural fallback is to detect AI-generated content downstream—but this literature largely shows how fragile that strategy remains."
    - Paraphrasing evades detectors of AI-generated text, but retr (2023)
    - RADAR: Robust AI-Text Detection via Adversarial Learning (2023)
    - Simple techniques to bypass GenAI text detectors: implicatio (2024)
    - Red Teaming Language Model Detectors with Language Models (2024)
    - Digital Watermarking—A Meta-Survey and Techniques for Fake N (2024)
    - Detecting AI-Generated Text: Factors Influencing Detectabili (2025)

**Writing notes**: Center the section on a two-step tension: first, the model-collapse literature establishes that recursive synthetic training is a genuine failure mode; second, the papers proposing fixes only succeed under unusually strong assumptions, while detector-based downstream responses are easy to evade or still fragmented. That lets the beat argue not merely that the crisis exists, but that the most obvious reactive defenses are inadequate. Because category B is underrepresented in the provided high-signal set, use the A papers to establish recursive contamination dynamics and the C papers to show why post-hoc policing of polluted data is not a sufficient remedy.

---

## Beat 2: Empirical Degradation

**Anchor paper**: Evolution of Composition, Readability, and Structure of Privacy Policies over Two Decades
  Why: It provides the clearest direct longitudinal evidence for this beat: a two-decade audit of a major web genre showing that web-native documents remain stubbornly difficult to comprehend despite external pressure to improve, making the case that content quality problems are measurable over time rather than anecdotal.

**Narrative spine** (6 papers):

  1. [2021] Evaluating latent content within unstructured text: an analytical meth
     Role: Establishes the measurement toolkit for tracking latent topical and semantic change in unstructured text across time.
     → With a temporal analysis framework in place, later work could move from describing drift abstractly to testing whether specific web genres were actually improving in readability and structure.
  2. [2023] Evolution of Composition, Readability, and Structure of Privacy Polici
     Role: Provides a concrete longitudinal case study showing that a core web document genre—privacy policies—has remained persistently hard to read over two decades.
     → Because this problem appears in a high-stakes, heavily regulated genre, the next step is to ask whether similar temporal instability appears across broader online discourse ecosystems.
  3. [2026] Triangulating Temporal Dynamics in Multilingual Swiss Online News
     Role: Extends the temporal perspective to large-scale multilingual online news, showing that web discourse evolves unevenly across language communities rather than converging toward a stable quality baseline.
     → Once temporal instability is visible across web-native text streams, corpus builders must treat the open web as a moving target rather than a static reservoir of interchangeable training data.
  4. [2024] RedPajama: an Open Dataset for Training Large Language Models
     Role: Shows that large-scale pretraining corpus construction now explicitly foregrounds composition, filtering, and transparency because raw web data quality is too heterogeneous to take for granted.
     → That recognition leads naturally to work asking whether stronger multi-snapshot filtering and deduplication can actually recover better web text at scale.
  5. [2024] The FineWeb Datasets: Decanting the Web for the Finest Text Data at Sc
     Role: Supplies large-scale empirical evidence that careful filtering and deduplication over many Common Crawl snapshots materially improve corpus utility, implying that substantial low-value or degraded content is present in the open web stream.
     → But if filtered corpora perform better, a final methodological question remains: do these filters capture genuinely higher-quality language, or merely distributions that better match downstream benchmarks?
  6. [2025] The Data-Quality Illusion: Rethinking Classifier-Based Quality Filteri
     Role: Introduces the key caveat for this beat by arguing that classifier-based quality gains can be partly illusory, sharpening the need for degradation measures that separate true quality loss from benchmark-specific distribution matching.
     → This caveat motivates our own empirical framing, which treats degradation as a measurable change in informativeness and diversity rather than as a proxy score alone.

**Paragraph structure**:

  ¶1: How temporal degradation in web text can be measured
    Opening: "Empirical work on web degradation begins by operationalizing change over time, first through temporal modeling of latent content and then through information-based accounts of what is lost when text distributions drift."
    - Evaluating latent content within unstructured text: an analy (2021)
    - Understanding Encoder-Decoder Structures in Machine Learning (2024)
    - Evolution of Composition, Readability, and Structure of Priv (2023)
  ¶2: Longitudinal evidence that web-native text streams are unstable and require curation
    Opening: "Using these measurement ideas, later studies show that temporal instability is not confined to one document type but appears across multilingual news ecosystems and large crawl-based pretraining corpora."
    - Triangulating Temporal Dynamics in Multilingual Swiss Online (2026)
    - RedPajama: an Open Dataset for Training Large Language Model (2024)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)
    - Improving Romanian LLM Pretraining Data using Diversity and  (2025)
  ¶3: Why filtering helps, and why naive quality metrics can still mislead
    Opening: "The newest literature complicates the picture by showing both that low-quality web text has real downstream costs and that apparent quality improvements can partly reflect distribution matching rather than universally better language."
    - The Data-Quality Illusion: Rethinking Classifier-Based Quali (2025)
    - LLMs Can Get "Brain Rot"! (2025)
    - Large Language Models Suffer From Their Own Output: An Analy (2023)
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
    - Recursive Training Loops in LLMs: How training data properti (2025)

**Writing notes**: Keep the section tightly empirical: start with measurement, move to longitudinal evidence, then end with corpus-construction consequences and metric caveats. A key tension to address is that some studies show clear deterioration, while others show persistent low quality or composition drift rather than a strictly monotonic decline; present these together as evidence that open-web text quality is unstable, measurable, and increasingly nontrivial to recover. Use RedPajama and FineWeb not as solution papers but as implicit admissions from dataset builders that raw web data now requires substantial intervention. Reserve full model-collapse discussion for Beat 1; here, collapse papers should only appear briefly as downstream consequences of degraded distributions.

---

## Beat 3: Theoretical Framework

**Anchor paper**: Understanding Encoder-Decoder Structures in Machine Learning Using Information Measures
  Why: This is the clearest formal bridge from the beat's problem setting to the paper's proposed objective: it treats information measures as principled descriptors of latent predictive structure, which makes it the best anchor for motivating L_auth as an information-theoretic authenticity criterion rather than an ad hoc heuristic.

**Narrative spine** (6 papers):

  1. [2023] Large Language Models Suffer From Their Own Output: An Analysis of the
     Role: Establishes the core failure mode in language models: recursive training on model outputs degrades quality and diversity, creating the need for a theory of authenticity that is sensitive to distributional drift.
     → Subsequent theory makes this intuition more precise by showing that collapse is not only a drop in quality, but a systematic reshaping of the distribution's tails and scaling behavior.
  2. [2024] A Tale of Tails: Model Collapse as a Change of Scaling Laws
     Role: Reframes model collapse as a change in scaling laws and tail behavior, giving a distributional explanation for why homogenization and rare-mode loss should be central targets of any authenticity objective.
     → Once collapse is understood as a structural distribution shift, the next step is to characterize when synthetic-data mixing remains statistically tolerable and when it becomes fundamentally unsafe.
  3. [2024] How Bad is Training on Synthetic Data? A Statistical Analysis of Langu
     Role: Provides a statistical account of language-model collapse under synthetic training and formalizes the idea that only limited synthetic mixing is safe, motivating an objective that can regulate deviation from the human data distribution.
     → These collapse results motivate a move from diagnosis to construction: rather than only bounding contamination, recent work asks how information measures can define the admissible predictive structure directly.
  4. [2024] Understanding Encoder-Decoder Structures in Machine Learning Using Inf
     Role: Supplies the beat's main theoretical anchor by grounding model behavior in information measures, supporting the use of divergence-based terms as principled components of an authenticity loss.
     → If information measures define the target structure, then the choice of divergence becomes consequential; recent distillation work shows that one-sided objectives can preserve accuracy while still eroding diversity.
  5. [2026] Entropy-Aware On-Policy Distillation of Language Models
     Role: Shows that augmenting reverse KL with forward KL under high-entropy conditions preserves generation diversity, directly supporting the inclusion of a divergence term that is sensitive to uncertainty and mode coverage rather than peak likelihood alone.
     → This logic extends further in newer distillation theory, where balanced or symmetric alignment is used to prevent both overconfidence and collapse of internal reasoning trajectories.
  6. [2026] DistillLens: Symmetric Knowledge Distillation Through Logit Lens
     Role: Closes the spine by arguing for symmetric knowledge distillation across intermediate representations, reinforcing the paper's claim that authenticity should balance fidelity and diversity instead of optimizing only for narrow agreement.
     → From here, the paragraph can pivot to supporting work on monitoring collapse, interpreting homogenization, and operationalizing collapse-sensitive signals.

**Paragraph structure**:

  ¶1: From recursive self-training to formal collapse dynamics
    Opening: "The theoretical framework starts from work showing that recursive reuse of model outputs induces a measurable distribution shift, and that this shift is best understood as collapse of diversity and tail support rather than as a generic quality decline."
    - Large Language Models Suffer From Their Own Output: An Analy (2023)
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
    - How Bad is Training on Synthetic Data? A Statistical Analysi (2024)
    - Universality of the $π^2/6$ Pathway in Avoiding Model Collap (2024)
  ¶2: Why authenticity should be divergence-based and diversity-aware
    Opening: "Against that backdrop, recent theory motivates authenticity objectives in explicitly information-theoretic terms, where divergence choice governs whether learning preserves informative uncertainty and rare-but-valid modes."
    - Understanding Encoder-Decoder Structures in Machine Learning (2024)
    - Entropy-Aware On-Policy Distillation of Language Models (2026)
    - DistillLens: Symmetric Knowledge Distillation Through Logit  (2026)
    - Back to Basics: Revisiting Exploration in Reinforcement Lear (2026)
  ¶3: Operationalizing collapse-sensitive signals and interpreting homogenization
    Opening: "Complementary papers then show how collapse can be measured, bounded, and conceptually interpreted, strengthening the case for an authenticity loss that combines fidelity to the source distribution with explicit pressure against homogenization."
    - Learning by Surprise: Surplexity for Mitigating Model Collap (2024)
    - Model Non-Collapse: Minimax Bounds for Recursive Discrete Di (2025)
    - Recursive Training Loops in LLMs: How training data properti (2025)
    - ChatGPT is incredible (at being average) (2025)
    - SIGMA: Scalable Spectral Insights for LLM Collapse (2026)

**Writing notes**: Keep the section centered on the paper's contribution, not on collapse theory for its own sake. The rhetorical flow should be: collapse literature establishes the need for authenticity-sensitive objectives; information-theoretic work justifies divergence-based formulation; distillation and optimization papers show why one-sided likelihood matching is insufficient; supporting papers motivate the diversity-sensitive component of L_auth. Be explicit that prior work motivates individual ingredients—distribution matching, symmetric/diversity-preserving divergence design, and collapse monitoring—but does not unify them into the paper's proposed L_auth = lambda1*D_KL + lambda2*D_alpha + lambda3*(1-TTR_r). Also note that the lexical-diversity term is motivated indirectly by the homogenization and tail-loss literature rather than borrowed wholesale from a single prior objective.

---

## Beat 4: Validation Experiment

**Anchor paper**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Why: It most directly motivates the beat by showing that large language models can perform competitively on generic language tasks yet still fail on social-intelligence judgments, making social reasoning the right validation target for comparing verified social data against web-scraped data.

**Narrative spine** (6 papers):

  1. [2021] UNICORN on RAINBOW: A Universal Commonsense Reasoning Model on a New M
     Role: Establishes the pre-beat baseline that broad commonsense reasoning can look strong on multitask benchmarks, creating the expectation that web-trained models should generalize to related reasoning settings.
     → However, later work showed that success on aggregate commonsense benchmarks does not imply reliable social understanding.
  2. [2022] Neural Theory-of-Mind? On the Limits of Social Intelligence in Large L
     Role: Defines the central failure mode for this beat by demonstrating that large LMs lack robust social intelligence and Theory-of-Mind-style reasoning out of the box.
     → Subsequent stress tests sharpened this critique by arguing that apparent social reasoning gains often reflect shortcut exploitation rather than genuine mental-state modeling.
  3. [2024] Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning 
     Role: Strengthens the case that current models' social reasoning is brittle, benchmark-sensitive, and often driven by superficial pattern matching.
     → Because benchmark gains alone were not enough, the field increasingly turned to preference-based post-training as an alternative route to better behavior.
  4. [2023] Direct Preference Optimization: Your Language Model is Secretly a Rewa
     Role: Represents the canonical alignment turn: instead of changing pretraining data, models are optimized directly against preference signals to improve outputs.
     → Yet stronger alignment pipelines still leave unresolved whether improved behavior comes from grounded social understanding or from better imitation of feedback.
  5. [2023] Demystifying CLIP Data
     Role: Provides a cross-domain argument that data curation can matter more than architecture, supporting the hypothesis that capability differences may primarily trace back to data quality.
     → Text-pretraining results then extended this point by showing that careful web-data filtering measurably improves downstream model quality at scale.
  6. [2024] The FineWeb Datasets: Decanting the Web for the Finest Text Data at Sc
     Role: Shows that even within web-derived corpora, better filtering and deduplication produce stronger language models, setting up our stronger claim that verified social data should outperform merely curated web data on social reasoning.
     → This motivates a direct validation experiment: compare models trained on noisy web sources against models trained on socially verified data for social-reasoning tasks.

**Paragraph structure**:

  ¶1: From generic commonsense progress to exposed failures on social reasoning
    Opening: "Recent work shows that while language models have become strong on broad commonsense benchmarks, these gains do not reliably transfer to socially grounded reasoning."
    - UNICORN on RAINBOW: A Universal Commonsense Reasoning Model  (2021)
    - TSGP: Two-Stage Generative Prompting for Unsupervised Common (2022)
    - On Curriculum Learning for Commonsense Reasoning (2022)
    - Neural Theory-of-Mind? On the Limits of Social Intelligence  (2022)
    - Clever Hans or Neural Theory of Mind? Stress Testing Social  (2024)
  ¶2: Why alignment and preference optimization are not sufficient substitutes for socially grounded data
    Opening: "A parallel line of work improves model behavior through preference-based alignment, but these methods mainly optimize responses to feedback rather than the provenance or fidelity of the knowledge being learned."
    - Direct Preference Optimization: Your Language Model is Secre (2023)
    - RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Fe (2023)
    - AlpacaFarm: A Simulation Framework for Methods that Learn fr (2023)
    - Principle-Driven Self-Alignment of Language Models from Scra (2023)
    - Zephyr: Direct Distillation of LM Alignment (2023)
    - AI Supported Degradation of the Self Concept: A Theoretical  (2023)
  ¶3: Data quality as the more plausible lever, culminating in the need for verified social data
    Opening: "Independent data-centric studies increasingly suggest that curated data quality, more than architecture alone, is a primary determinant of downstream capability."
    - Demystifying CLIP Data (2023)
    - Yi: Open Foundation Models by 01.AI (2024)
    - The FineWeb Datasets: Decanting the Web for the Finest Text  (2024)
    - On LLMs-Driven Synthetic Data Generation, Curation, and Eval (2024)

**Writing notes**: Key tension to emphasize: the literature shows two different stories about improving models. One story is benchmark and alignment progress: better prompting, curricula, and preference optimization can raise aggregate performance and chat quality. The other story is that social reasoning remains brittle and shortcut-driven, implying that post-hoc alignment does not solve the core grounding problem. Use paragraph 1 to establish that generic commonsense success is not enough for social intelligence. Use paragraph 2 to acknowledge the strength of alignment work while framing it as behavior-shaping rather than evidence-quality control; the sycophancy result is especially useful as a limitation. Use paragraph 3 to pivot to the data-centric explanation: if curation quality drives performance in multimodal and text settings, then socially verified data is a principled next step beyond filtered web corpora. End the section by stating that our validation experiment tests exactly this hypothesis: whether verified social data produces better social-reasoning performance than web-scraped data under otherwise comparable training conditions.

---

## Beat 5: Platform Solution

**Anchor paper**: Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinforcement
  Why: This is the clearest bridge between the collapse literature and platform design: it reframes the remedy as verification and reinforcement of data quality rather than simply generating more content, which directly motivates a verification-first platform like CampusGo.

**Narrative spine** (6 papers):

  1. [2023] Self-Consuming Generative Models go MAD
     Role: Introduces the core failure mode of self-consuming generative loops: without fresh real data, precision or diversity must degrade over generations.
     → This initial warning is then generalized into a broader account of collapse as a structural property of recursively generated training data.
  2. [2024] AI models collapse when trained on recursively generated data
     Role: Establishes model collapse as a general empirical phenomenon and identifies the disappearance of low-probability tails as the key distributional failure.
     → Once collapse is understood as a data-governance problem, later work asks what practical intervention can actually keep recursive pipelines stable.
  3. [2024] Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinf
     Role: Supplies the beat's central design premise: verified or reinforced synthetic data can avert collapse, making validation workflows more important than raw content generation.
     → If verification is the actionable safeguard, the platform question becomes how to capture, preserve, and reuse those validation signals as provenance.
  4. [2020] Materials Cloud, a platform for open computational science
     Role: Shows that a platform can make provenance first-class through persistent, citable graphs that preserve the lineage of computational outputs.
     → But provenance stored inside one platform is not enough; it must also travel with artefacts in a portable, machine-readable form.
  5. [2022] Packaging research artefacts with RO-Crate
     Role: Provides a lightweight packaging model for portable metadata and provenance, suggesting how authenticity signals can move across systems rather than remain siloed.
     → Even portable provenance is insufficient, however, if user interfaces obscure where content came from or how it was verified.
  6. [2022] Situating Search
     Role: Argues that LLM-mediated information interfaces reduce transparency and verification, motivating platform designs that expose provenance and trust cues directly to users.
     → Together, these strands justify CampusGo as a verification-first, provenance-visible platform rather than a generic content host.

**Paragraph structure**:

  ¶1: Collapse literature turns synthetic-data risk into a design requirement for fresh, verified inputs
    Opening: "Recent work on self-consuming training loops increasingly suggests that the solution space is not merely better modeling, but preserving access to fresh, validated human data as recursive reuse grows."
    - Self-Consuming Generative Models go MAD (2023)
    - Large Language Models Suffer From Their Own Output: An Analy (2023)
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
    - AI models collapse when trained on recursively generated dat (2024)
    - How Bad is Training on Synthetic Data? A Statistical Analysi (2024)
    - Beyond Model Collapse: Scaling Up with Synthesized Data Requ (2024)
  ¶2: Prevention depends on correction, curation, source retention, and defenses against bad curation
    Opening: "Follow-on theory sharpens this point by showing that recursive stability hinges on how verification and curation are enforced, not just on whether synthetic data are present."
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Universality of the $π^2/6$ Pathway in Avoiding Model Collap (2024)
    - A Theoretical Perspective: How to Prevent Model Collapse in  (2025)
    - Self-Consuming Generative Models with Adversarially Curated  (2025)
  ¶3: Platform precedents show how provenance can be captured, packaged, and surfaced to users
    Opening: "Systems work on reproducibility and search transparency then provides the architectural pieces for a solution: provenance must be recorded in the backend, packaged for reuse, and made visible at the interface level."
    - Materials Cloud, a platform for open computational science (2020)
    - AiiDA 1.0, a scalable computational infrastructure for autom (2020)
    - Packaging research artefacts with RO-Crate (2022)
    - Situating Search (2022)

**Writing notes**: Key tension to emphasize: collapse-prevention papers increasingly argue for verification, curation, and retention of real-source lineage, but they mostly treat these as abstract training-loop interventions rather than concrete product features. Conversely, provenance-platform papers show how lineage and metadata can be captured and shared, yet they focus on scientific workflows rather than socially verified data or user-facing authenticity judgments. Position CampusGo as the missing synthesis: a platform that operationalizes collapse-resistant data governance through explicit provenance, verification workflows, and interface-visible trust signals aligned with L_auth.

---
