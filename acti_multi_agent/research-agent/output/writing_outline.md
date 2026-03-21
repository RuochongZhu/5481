# Related Work Writing Outline

*Auto-generated narrative structure for each beat*

---

## Beat 1: Crisis Exists

**Anchor paper**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Why: The foundational paper that established the model collapse phenomenon with 441 citations, serving as the theoretical bedrock that all subsequent work builds upon.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Establishes the foundational model collapse theory
     → Building on this theoretical foundation, subsequent work has confirmed that training on synthetic data creates measurable stability issues...
  2. [2023] On the Stability of Iterative Retraining of Generative Models on their
     Role: Provides theoretical analysis of stability impacts in mixed datasets
     → Expanding beyond theoretical concerns, empirical evidence has demonstrated that these collapse dynamics manifest in practical settings...
  3. [2024] AI models collapse when trained on recursively generated data
     Role: Demonstrates empirical evidence of irreversible model collapse
     → As these collapse patterns have been confirmed across different model architectures, the scope of the crisis has expanded to encompass the entire generative AI ecosystem...
  4. [2023] Towards Understanding the Interplay of Generative Artificial Intellige
     Role: Reveals the systemic nature of AI content contamination on the internet
     → This contamination crisis extends beyond individual models to threaten the reliability of content detection systems...
  5. [2023] A Survey on LLM-Generated Text Detection: Necessity, Methods, and Futu
     Role: Establishes the imperative need for detection systems to combat misuse
     → While detection represents one defensive approach, the fundamental challenge of distinguishing authentic from synthetic content continues to intensify...
  6. [2023] Cognitive Constraint Simulation and the Geometry of Human Authorship: 
     Role: Provides theoretical framework for understanding why detection remains challenging

**Paragraph structure**:

  ¶1: Model collapse theory and empirical validation
    Opening: "Recent work has established that generative models trained on their own output exhibit irreversible degradation where distribution tails disappear, a phenomenon termed model collapse."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - Self-Consuming Generative Models Go MAD (2023)
    - Self-Consuming Generative Models go MAD (2023)
    - Large Language Models Suffer From Their Own Output: An Analy (2023)
    - On the Stability of Iterative Retraining of Generative Model (2023)
    - AI models collapse when trained on recursively generated dat (2024)
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
  ¶2: Systemic contamination and ecosystem-wide implications
    Opening: "Beyond individual model degradation, generative AI creates feedback loops by contributing synthetic content to future training repositories, threatening the entire AI ecosystem."
    - Towards Understanding the Interplay of Generative Artificial (2023)
    - When AI Eats Itself: On the Caveats of AI Autophagy (2024)
  ¶3: Detection challenges and the authenticity crisis
    Opening: "The imperative need for detecting machine-generated content faces fundamental theoretical and practical limitations, as current detection systems struggle with out-of-distribution synthetic text in realistic settings."
    - A Survey on LLM-Generated Text Detection: Necessity, Methods (2023)
    - A Survey on Hallucination in Large Language Models: Principl (2023)
    - Cognitive Constraint Simulation and the Geometry of Human Au (2023)
    - Machine-Generated Text: A Comprehensive Survey of Threat Mod (2023)
    - Detecting computer-generated disinformation (2021)

**Writing notes**: Key tension to address: While model collapse appears inevitable in pure synthetic training scenarios, the literature reveals ongoing debate about whether proper data curation and mixing strategies can mitigate these effects. Emphasize the urgency of the problem while acknowledging that solutions exist but require careful implementation.

---

## Beat 2: Empirical Degradation

**Anchor paper**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Why: This is the foundational empirical work that first demonstrated measurable model collapse effects, with 441 citations and cited by nearly all subsequent model collapse papers

**Narrative spine** (5 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Establishes empirical evidence of model collapse when training on generated data
     → Building on this foundational observation of distribution tail disappearance, theoretical work examined the underlying mechanisms...
  2. [2023] On the Stability of Iterative Retraining of Generative Models on their
     Role: Provides theoretical framework for understanding stability in mixed real/synthetic training
     → These theoretical insights led to more nuanced empirical investigations of the collapse phenomenon...
  3. [2024] A Tale of Tails: Model Collapse as a Change of Scaling Laws
     Role: Reframes model collapse as changes in scaling laws rather than simple degradation
     → Recent comprehensive analyses have revealed the complexity and diversity of collapse phenomena...
  4. [2025] Position: Model Collapse Does Not Mean What You Think
     Role: Demonstrates that model collapse encompasses eight distinct definitions, revealing measurement complexity
     → Complementing these foundational insights, emerging diagnostic frameworks provide new measurement approaches...
  5. [2026] Spectral Archaeology: The Causal Topology of Model Evolution
     Role: Introduces spectral analysis methods for training-free detection of model degradation

**Paragraph structure**:

  ¶1: Foundational empirical evidence of model collapse
    Opening: "Recent empirical work has demonstrated that training language models on recursively generated data leads to measurable degradation through model collapse phenomena."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - Towards Understanding the Interplay of Generative Artificial (2023)
    - AI models collapse when trained on recursively generated dat (2024)
  ¶2: Theoretical frameworks and mechanistic understanding
    Opening: "Building on these empirical observations, theoretical analyses have revealed the underlying mechanisms driving model collapse as changes in scaling laws and stability dynamics."
    - On the Stability of Iterative Retraining of Generative Model (2023)
    - Heat Death of Generative Models in Closed-Loop Learning (2024)
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
    - Collapse or Thrive? Perils and Promises of Synthetic Data in (2024)
    - A Closer Look at Model Collapse: From a Generalization-to-Me (2025)
  ¶3: Advanced measurement and diagnostic approaches
    Opening: "Recent work has revealed the complexity of measuring model collapse, with distinct definitions requiring sophisticated diagnostic frameworks to detect degradation patterns."
    - Position: Model Collapse Does Not Mean What You Think (2025)
    - When Models Don't Collapse: On the Consistency of Iterative  (2025)
    - Spectral Archaeology: The Causal Topology of Model Evolution (2026)
    - Long-Tail Knowledge in Large Language Models: Taxonomy, Mech (2026)
    - Do Large Language Models (Really) Need Statistical Foundatio (2025)

**Writing notes**: Key tension to address: While early work focused on dramatic collapse scenarios, recent research shows the phenomenon is more nuanced with multiple definitions and potential mitigation strategies. The narrative should progress from clear empirical evidence to complex theoretical understanding to advanced measurement approaches. Emphasize the evolution from simple 'models break' to 'models change in measurable ways that can be detected and potentially managed.'

---

## Beat 3: Theoretical Framework

**Anchor paper**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Why: Most cited paper (441) that establishes the foundational theory of model collapse as irreversible distribution tail disappearance - the core phenomenon our L_auth framework addresses

**Narrative spine** (5 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Establishes foundational theory of model collapse as irreversible distribution tail disappearance
     → Building on this empirical demonstration of collapse, theoretical frameworks emerged to formalize the underlying mechanisms...
  2. [2023] On the Stability of Iterative Retraining of Generative Models on their
     Role: Provides theoretical stability analysis for mixed real-synthetic training
     → This stability perspective was extended to characterize collapse as fundamental changes in model scaling behavior...
  3. [2024] A Tale of Tails: Model Collapse as a Change of Scaling Laws
     Role: Reframes model collapse through scaling law perspective, showing mathematical signatures
     → While these works established collapse theory, they lacked practical frameworks for measuring authenticity. Recent advances in information theory provide the foundation...
  4. [2025] Do Large Language Models (Really) Need Statistical Foundations?
     Role: Establishes necessity of statistical foundations for LLMs due to data dependency
     → This statistical foundation enables novel authenticity metrics that can capture the distribution properties central to collapse...
  5. [2025] Information Retrieval in the Age of Generative AI: The RGB Model
     Role: Introduces stochastic modeling for information dynamics in generative AI era
     → These theoretical advances culminate in our novel L_auth framework that combines divergence measures with linguistic authenticity indicators...

**Paragraph structure**:

  ¶1: Foundational model collapse theory
    Opening: "Recent theoretical work has established that training generative models on their own outputs leads to irreversible model collapse where distribution tails disappear..."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - Towards Understanding the Interplay of Generative Artificial (2023)
    - On the Stability of Iterative Retraining of Generative Model (2023)
    - Heat Death of Generative Models in Closed-Loop Learning (2024)
  ¶2: Mathematical characterization of collapse dynamics
    Opening: "This collapse phenomenon manifests as measurable changes in scaling laws, though definitional precision remains critical for theoretical progress..."
    - A Tale of Tails: Model Collapse as a Change of Scaling Laws (2024)
    - Position: Model Collapse Does Not Mean What You Think (2025)
    - Collapse or Thrive? Perils and Promises of Synthetic Data in (2024)
  ¶3: Statistical foundations for authenticity measurement
    Opening: "These theoretical insights require rigorous statistical foundations to develop practical authenticity measures that can detect and prevent collapse..."
    - Do Large Language Models (Really) Need Statistical Foundatio (2025)
    - When Models Don't Collapse: On the Consistency of Iterative  (2025)
    - Information Retrieval in the Age of Generative AI: The RGB M (2025)
    - SIGMA: Scalable Spectral Insights for LLM Model Collapse (2026)

**Writing notes**: Key tension to address: Most existing work focuses on post-hoc detection of collapse rather than real-time authenticity measurement. Our L_auth framework fills this gap by providing a principled combination of KL divergence (distribution matching), alpha-divergence (tail preservation), and TTR (linguistic authenticity) that can be computed during training. Emphasize how this theoretical contribution builds on established collapse theory while enabling practical prevention strategies.

---

## Beat 4: Validation Experiment

**Anchor paper**: Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data
  Why: Most cited foundational paper establishing that model collapse can be broken through accumulating real and synthetic data, providing the core theoretical framework that subsequent papers build upon

**Narrative spine** (6 papers):

  1. [2024] Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accum
     Role: Establishes the foundational finding that model collapse is not inevitable
     → Building on this theoretical breakthrough, researchers have explored optimal mixing strategies...
  2. [2024] Self-Consuming Generative Models with Curated Data Provably Optimize H
     Role: Provides theoretical framework for optimal curation in self-consuming loops
     → Extending these optimization principles to practical implementation...
  3. [2024] Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Ge
     Role: Demonstrates practical strategies for managing data workflows to prevent collapse
     → Recent work has further refined these approaches through dynamic adaptation...
  4. [2025] Escaping Collapse: The Strength of Weak Data for Large Language Model 
     Role: Shows that proper curation enables continual improvement without collapse
     → Complementing these curation approaches, diversity-based methods have emerged...
  5. [2025] What Matters in LLM-generated Data: Diversity and Its Effect on Model 
     Role: Establishes data diversity as critical factor in preventing collapse
     → Advanced verification mechanisms have been proposed to ensure quality...
  6. [2025] Escaping Model Collapse via Synthetic Data Verification: Near-term Imp
     Role: Introduces external verification as a robust collapse prevention mechanism

**Paragraph structure**:

  ¶1: Theoretical foundations of collapse prevention
    Opening: "Recent theoretical advances have challenged the inevitability of model collapse, demonstrating that strategic data management can maintain performance across training generations."
    - Is Model Collapse Inevitable? Breaking the Curse of Recursio (2024)
    - Self-Consuming Generative Models with Curated Data Provably  (2024)
    - Universality of the $π^2/6$ Pathway in Avoiding Model Collap (2024)
    - Open Problems and Fundamental Limitations of Reinforcement L (2023)
  ¶2: Practical implementation strategies
    Opening: "Translating these theoretical insights into practice requires careful attention to data curation workflows and diversity preservation mechanisms."
    - Collapse or Thrive? Perils and Promises of Synthetic Data in (2024)
    - Escaping Collapse: The Strength of Weak Data for Large Langu (2025)
    - Self-Improving Diffusion Models with Synthetic Data (2024)
    - What Matters in LLM-generated Data: Diversity and Its Effect (2025)
    - Unveiling the Flaws: Exploring Imperfections in Synthetic Da (2024)
  ¶3: Advanced verification and quality control
    Opening: "The most robust approaches to collapse prevention incorporate external verification mechanisms and real-time quality assessment."
    - Escaping Model Collapse via Synthetic Data Verification: Nea (2025)
    - Learning by Surprise: Surplexity for Mitigating Model Collap (2024)
    - Self-Correcting Self-Consuming Loops for Generative Model Tr (2024)
    - The Power of Noise: Redefining Retrieval for RAG Systems (2024)
    - RAG vs Fine-tuning: Pipelines, Tradeoffs, and a Case Study o (2024)
    - Preventing Model Collapse Under Overparametrization: Optimal (2025)

**Writing notes**: Key tension to address: Balance between theoretical guarantees and practical implementation constraints. Emphasize the progression from basic accumulation strategies to sophisticated verification systems. Highlight how empirical validation supports theoretical predictions about optimal mixing ratios and diversity requirements.

---

## Beat 5: Platform Solution

**Anchor paper**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Why: The foundational work establishing model collapse from recursive training - the core problem our CampusGo platform addresses. This highly-cited paper (441 citations) provides the theoretical grounding that motivates platform-based solutions.

**Narrative spine** (6 papers):

  1. [2023] The Curse of Recursion: Training on Generated Data Makes Models Forget
     Role: Establishes the fundamental problem of model collapse from recursive training
     → Building on this theoretical foundation of collapse mechanisms, subsequent work has explored systematic approaches to mitigate these issues...
  2. [2022] Beyond the Imitation Game: Quantifying and extrapolating the capabilit
     Role: Demonstrates the need for comprehensive evaluation frameworks to address model collapse
     → While benchmarking frameworks reveal the scope of the problem, recent advances focus on prevention strategies...
  3. [2024] Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accum
     Role: Shows that strategic mixing of real and synthetic data can prevent collapse
     → This mixing approach has inspired platform-level solutions that curate data sources...
  4. [2025] Escaping Collapse: The Strength of Weak Data for Large Language Model 
     Role: Establishes that proper synthetic data curation enables continual improvement
     → These curation principles directly inform the design of verification-based platforms...
  5. [2025] Escaping Model Collapse via Synthetic Data Verification: Near-term Imp
     Role: Proposes external verification as a concrete mechanism for preventing collapse
     → Such verification mechanisms can be implemented at scale through platform architectures that integrate human oversight...
  6. [2024] OpenScholar: Synthesizing Scientific Literature with Retrieval-augment
     Role: Demonstrates successful implementation of retrieval-augmented systems for scientific literature
     → This success in scientific domains validates the platform approach for verified content generation in educational settings.

**Paragraph structure**:

  ¶1: Foundational collapse theory and evaluation needs
    Opening: "The foundational challenge of model collapse from recursive training on synthetic data has motivated the development of comprehensive evaluation frameworks to assess and prevent degradation across diverse domains."
    - The Curse of Recursion: Training on Generated Data Makes Mod (2023)
    - Beyond the Imitation Game: Quantifying and extrapolating the (2022)
    - A systematic evaluation of large language models of code (2022)
    - Holistic Evaluation of Language Models (2022)
    - MTEB: Massive Text Embedding Benchmark (2023)
  ¶2: Data mixing and curation strategies
    Opening: "Strategic approaches to preventing model collapse center on optimal mixing of real and synthetic data, with recent work establishing that proper curation can enable continual model improvement rather than degradation."
    - Is Model Collapse Inevitable? Breaking the Curse of Recursio (2024)
    - Escaping Collapse: The Strength of Weak Data for Large Langu (2025)
    - Dialogue Response Ranking Training with Large-Scale Human Fe (2020)
    - Preventing Model Collapse Under Overparametrization: Optimal (2025)
  ¶3: Platform-based verification solutions
    Opening: "These theoretical insights have culminated in practical platform solutions that implement external verification mechanisms, with demonstrated success in scientific literature synthesis suggesting broader applicability to educational content generation."
    - Escaping Model Collapse via Synthetic Data Verification: Nea (2025)
    - OpenScholar: Synthesizing Scientific Literature with Retriev (2024)
    - Chatbot Arena: An Open Platform for Evaluating LLMs by Human (2024)

**Writing notes**: Key tension to address: The progression from identifying the collapse problem to implementing platform solutions. Emphasize how CampusGo represents the natural evolution from theoretical understanding to practical implementation. The narrative should flow from problem identification (collapse theory) through systematic evaluation approaches to concrete platform-based solutions with verified social data.

---
