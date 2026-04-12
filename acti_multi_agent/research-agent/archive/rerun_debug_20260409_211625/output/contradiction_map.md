# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can synthetic data with proper curation avoid model collapse?

**Paper A**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Self-consuming generative models with human-curated synthetic data provably optimize human preferences and avoid collapse
  Evidence: Human curation can prevent model collapse and actually optimize for human preferences

**Paper B**: How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model 
  Claim: Model collapse cannot be avoided when training solely on synthetic data but mixing real and synthetic data has limits
  Evidence: Statistical analysis shows collapse is inevitable with synthetic-only training

**Relevance to thesis**: Directly impacts our claim about human data being irreplaceable - if curation can prevent collapse, our argument needs refinement
**Beat affected**: 4
**Suggested handling**: Acknowledge that while some theoretical work suggests curation can prevent collapse, empirical evidence shows limitations. Emphasize that authentic human behavioral data remains critical for social reasoning tasks

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Does synthetic data mixed with real data accelerate or harm training?

**Paper A**: Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling L
  Claim: Mixing 1/3 rephrased synthetic data with 2/3 natural web texts speeds up pre-training 5-10x
  Evidence: Large-scale empirical study shows significant speedup with appropriate mixing

**Paper B**: Large Language Models Suffer From Their Own Output: An Analysis of the Self-Cons
  Claim: Self-consuming training loops in LLMs reduce quality and diversity, leading to model collapse similar to image generation
  Evidence: LLM-generated content in training loops reduces both quality and diversity

**Relevance to thesis**: Challenges our position that synthetic data degrades models - shows it can actually accelerate training under certain conditions
**Beat affected**: 3
**Suggested handling**: Clarify that synthetic data benefits are task-specific: rephrasing may help with language tasks but fails for authentic social behavioral modeling that CampusGo targets

---

## C5: 🔴 CRITICAL — direct_contradiction

**Question**: Can AI models generate new knowledge autonomously through self-produced data?

**Paper A**: Generalising from Self-Produced Data: Model Training Beyond Human Constraints
  Claim: AI models can autonomously generate and validate knowledge through environment interaction using unbounded numeric rewards
  Evidence: Proposes framework for models to generate new knowledge beyond human constraints

**Paper B**: Self-Consuming Generative Models go MAD
  Claim: Without enough fresh real data, autophagous loops cause generative models' quality or diversity to progressively decrease
  Evidence: Empirical evidence shows progressive degradation without fresh human data

**Relevance to thesis**: Directly challenges our claim that human data is essential - suggests AI can bootstrap its own knowledge
**Beat affected**: 4
**Suggested handling**: Distinguish between formal/mathematical domains where self-generation may work vs social/behavioral domains where human authenticity is irreplaceable

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can AI-generated text be reliably detected?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: DIPPER paraphrasing successfully evades multiple AI-generated text detectors including watermarking and GPTZero
  Evidence: Paraphrasing evades detectors of AI-generated text

**Paper B**: RADAR: Robust AI-Text Detection via Adversarial Learning
  Claim: RADAR framework provides robust AI-text detection through joint adversarial training
  Evidence: RADAR: Robust AI-Text Detection via Adversarial Learning

**Relevance to thesis**: Directly impacts Beat 5's claim about pollution detection - if AI text can evade detection, web pollution may be unmeasurable
**Beat affected**: 5
**Suggested handling**: Acknowledge in §6 that detection effectiveness varies by method and attack sophistication, citing both papers to show the arms race nature

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: What accuracy levels can AI-text detectors achieve?

**Paper A**: Simple techniques to bypass GenAI text detectors: implications for inclusive edu
  Claim: Simple content manipulation techniques reduce GenAI text detector accuracy by 17.4%
  Evidence: Simple techniques to bypass GenAI text detectors

**Paper B**: Distinguishing Reality from AI: Approaches for Detecting Synthetic Content
  Claim: Stylometric analysis reaches 80% independent accuracy
  Evidence: Multiple detection approaches achieve varying accuracy rates, with stylometric analysis reaching 80%

**Relevance to thesis**: Questions whether we can reliably measure web pollution if detection accuracy varies so widely
**Beat affected**: 5
**Suggested handling**: Frame as detection being method-dependent: some approaches work well on naive AI text but fail against adversarial examples

---

## C5: 🔴 CRITICAL — implicit_tension

**Question**: Is the homogenization effect (brain rot) detectable?

**Paper A**: ChatGPT is incredible (at being average)
  Claim: LLM output homogenization produces aggregated clichés and trivialities
  Evidence: ChatGPT is incredible (at being average)...output homogenization

**Paper B**: LLMs Can Get "Brain Rot"!
  Claim: Continual exposure to junk web text causes lasting cognitive decline in large language models
  Evidence: LLMs Can Get 'Brain Rot'!...continual exposure to junk web text induces lasting cognitive decline

**Relevance to thesis**: Both support our thesis but suggest pollution may be more about quality degradation than quantity - harder to detect than binary AI/human
**Beat affected**: 5
**Suggested handling**: Use to strengthen argument that pollution isn't just about AI content but about information quality decay

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can high-quality training data be effectively filtered from web-crawled datasets?

**Paper A**: The Data-Quality Illusion: Rethinking Classifier-Based Quality Filtering for LLM
  Claim: Classifier-based Quality Filtering improves downstream performance but paradoxically doesn't enhance language modeling on high-quality datasets
  Evidence: CQF trains a binary classifier to distinguish between pretraining data and a small, high-quality set... but paradoxically doesn't enhance language modeling

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb produces better-performing LLMs than other open pretraining datasets through careful curation strategies
  Evidence: FineWeb, a 15-trillion token dataset derived from 96 Common Crawl snapshots that produces better-performing LLMs

**Relevance to thesis**: Challenges our claim that web data quality is declining if curation can still produce high-quality datasets
**Beat affected**: 3
**Suggested handling**: Acknowledge that while curation can improve relative quality, the absolute quality ceiling may still be declining over time

---

## C4: 🔴 CRITICAL — implicit_tension

**Question**: Can we reliably measure quality decline when measurement methods themselves are evolving?

**Paper A**: A Comparison of Commercial Sentiment Analysis Services
  Claim: Commercial sentiment analysis services show varying performance across different metrics
  Evidence: varying performance across accuracy, precision, recall, and F1 measures... constant evolution in the field

**Paper B**: Detecting AI-Generated Code Assignments Using Perplexity of Large Language Model
  Claim: Different computational language models reveal distinct aspects of semantic loosening
  Evidence: Different computational language models reveal distinct aspects... five language models with different computational architectures

**Relevance to thesis**: If our measurement tools give different results, how can we definitively claim quality is declining?
**Beat affected**: 2
**Suggested handling**: Acknowledge measurement challenges but argue for convergent evidence across multiple metrics showing degradation

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can AI-generated feedback replace human feedback for model alignment?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: AI feedback can achieve comparable performance to human feedback for reinforcement learning alignment
  Evidence: RLAIF... offers a promising alternative that trains the reward model on preferences generated by an off-the-shelf LLM. Across the tasks of summarization, [shows comparable performance]

**Paper B**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Human-in-the-Loop reinforcement learning is fundamentally necessary even when agents perform autonomously
  Evidence: we consider RL as fundamentally a Human-in-the-Loop (HITL) paradigm, even when an agent eventually performs its task autonomously

**Relevance to thesis**: Directly impacts our claim about irreplaceable human behavioral data - if AI feedback equals human feedback, our thesis is weakened
**Beat affected**: 4
**Suggested handling**: Acknowledge that RLAIF works for certain tasks like summarization but emphasize that social behavioral data requires genuine human input that AI cannot simulate

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: Does self-consuming synthetic data lead to model collapse or optimization?

**Paper A**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Self-consuming generative models with human-curated synthetic data provably optimize human preferences and avoid collapse
  Evidence: Self-consuming generative models with human-curated synthetic data provably optimize human preferences and avoid collapse

**Paper B**: Self-Consuming Generative Models with Adversarially Curated Data
  Claim: Self-consuming loops with adversarially curated data drive models toward manipulated preferences
  Evidence: Self-consuming retraining loops with adversarially curated data can drive models toward distributions that optimize manipulated preferences

**Relevance to thesis**: Critical for Beat 3 - whether curation prevents collapse depends on who does the curating and their incentives
**Beat affected**: 3
**Suggested handling**: Use this tension to strengthen our argument: curation quality depends on authentic human involvement vs adversarial manipulation, supporting our campus-verified data approach

---

## C5: 🔴 CRITICAL — direct_contradiction

**Question**: Can LLMs generate better rewards than human experts?

**Paper A**: Eureka: Human-Level Reward Design via Coding Large Language Models
  Claim: LLMs can generate reward functions that outperform expert human-engineered rewards for complex manipulation tasks
  Evidence: Eureka exploits the remarkable zero-shot generation... [generates] reward functions that outperform expert human-engineered rewards

**Paper B**: Let's Verify Step by Step
  Claim: Process supervision significantly outperforms outcome supervision for training reliable reasoning models
  Evidence: Process supervision significantly outperforms outcome supervision for training reliable reasoning models

**Relevance to thesis**: If LLMs can design better rewards than humans, it challenges our human data necessity claim
**Beat affected**: 4
**Suggested handling**: Clarify that Eureka's success is in robotics/manipulation tasks, while human behavioral data remains crucial for social reasoning and authentic interaction patterns

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Do LLMs possess genuine Theory of Mind capabilities?

**Paper A**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks social intelligence and Theory of Mind capabilities for understanding intents and reactions in social interactions
  Evidence: Direct empirical testing shows GPT-3 fails at Theory of Mind tasks

**Paper B**: Are Vision Language Models Cross-Cultural Theory of Mind Reasoners?
  Claim: Frontier VLMs achieve >93% accuracy on cultural ToM tasks
  Evidence: Empirical evaluation on CulturalToM-VQA benchmark shows frontier models achieving over 93% accuracy

**Relevance to thesis**: Critical for Beat 3 claim that physical verification and authentic social data is needed - if models already achieve 93% on ToM, why do we need CampusGo?
**Beat affected**: 3
**Suggested handling**: Clarify that high performance on controlled benchmarks doesn't translate to real-world social reasoning, note false belief tasks show much lower performance (19-83%)

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Can synthetic benchmarks adequately evaluate social reasoning?

**Paper A**: UNICORN on RAINBOW: A Universal Commonsense Reasoning Model on a New Multitask B
  Claim: Rainbow multitask benchmark effectively evaluates commonsense model generalization across multiple tasks and datasets
  Evidence: Proposes benchmark as effective evaluation method for commonsense reasoning

**Paper B**: Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large L
  Claim: LLMs may exhibit Clever Hans effects in social reasoning rather than genuine Theory of Mind capabilities
  Evidence: Shows that apparent social reasoning performance may be spurious pattern matching rather than genuine understanding

**Relevance to thesis**: Directly impacts our argument that benchmarks are insufficient for measuring real social intelligence
**Beat affected**: 2
**Suggested handling**: Use this tension to support our thesis - benchmarks can show high scores while models still fail at genuine social reasoning

---

## C5: 🔴 CRITICAL — direct_contradiction

**Question**: Do LLMs' self-reported capabilities match their actual behavioral performance?

**Paper A**: The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior
  Claim: LLMs show dissociation between self-reported personality traits and actual behavioral performance in tasks
  Evidence: Empirical testing reveals disconnect between what LLMs claim about themselves and how they actually behave

**Paper B**: Are Vision Language Models Cross-Cultural Theory of Mind Reasoners?
  Claim: Frontier VLMs achieve >93% accuracy on cultural ToM tasks
  Evidence: High benchmark scores suggest strong social reasoning capabilities

**Relevance to thesis**: Critical support for our thesis - benchmarks may be measuring self-report accuracy rather than genuine social understanding
**Beat affected**: 2
**Suggested handling**: Highlight this as evidence that benchmark performance doesn't equal real social intelligence

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: How should model collapse be measured and characterized?

**Paper A**: Learning by Surprise: Surplexity for Mitigating Model Collapse in Generative AI
  Claim: Surplexity measures can characterize model collapse directly from next-token probability distributions without knowing data origin
  Evidence: Proposes surplexity as a direct measure from probability distributions

**Paper B**: RedPajama: an Open Dataset for Training Large Language Models
  Claim: Different human dataset properties lead to distribution shifts of different magnitudes in recursive training
  Evidence: Shows collapse depends heavily on properties of original human data

**Relevance to thesis**: Different measurement approaches may show different severity of collapse, affecting our claims about degradation
**Beat affected**: 3
**Suggested handling**: Note that collapse measurement remains contested, but all approaches agree that authentic human data properties fundamentally shape model behavior

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Is data curation or data authenticity more important for model quality?

**Paper A**: Demystifying CLIP Data
  Claim: CLIP's success stems primarily from its data curation approach rather than model architecture
  Evidence: Demonstrates curation strategies as primary driver of success

**Paper B**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated content in training causes irreversible model collapse with tail distribution disappearance
  Evidence: Shows that regardless of curation, synthetic data loses tail distributions

**Relevance to thesis**: Tension between emphasizing curation quality vs data authenticity - we claim authenticity matters most for social data
**Beat affected**: 4
**Suggested handling**: Acknowledge both matter but argue that for social behavioral data, no amount of curation can replace authentic human interactions captured by CampusGo

---

## C3: 🟡 MODERATE — direct_contradiction

**Question**: Can watermarking provide reliable AI-text detection?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Paraphrasing successfully evades watermarking
  Evidence: DIPPER paraphrasing successfully evades multiple AI-generated text detectors including watermarking

**Paper B**: Adaptive Text Watermark for Large Language Models
  Claim: Adaptive watermarking maintains strong security and robustness
  Evidence: Adaptive watermarking strategy improves text quality by selectively watermarking high-entropy token distributions

**Relevance to thesis**: Affects our ability to track AI-generated content proliferation on the web
**Beat affected**: 5
**Suggested handling**: Note that watermarking effectiveness depends on whether attackers actively try to remove it

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Is authorship verification effective against LLM impersonation?

**Paper A**: Authorship Impersonation via LLM Prompting does not Evade Authorship Verificatio
  Claim: LLM-generated authorial impersonations cannot evade existing forensic authorship verification systems
  Evidence: Authorship verification (AV)...LLM-generated authorial impersonations cannot evade existing forensic authorship verification

**Paper B**: Red Teaming Language Model Detectors with Language Models
  Claim: LLM detectors can be successfully attacked using word replacement and writing style modification
  Evidence: Red Teaming Language Model Detectors with Language Models

**Relevance to thesis**: Different scopes - authorship verification vs general detection - but both relate to pollution detection
**Beat affected**: 5
**Suggested handling**: Clarify that specialized forensic methods may work better than general detectors

---

## C2: 🟡 MODERATE — methodological_tension

**Question**: How should we measure information quality in text data?

**Paper A**: Entropy and type-token ratio in gigaword corpora
  Claim: Entropy and type-token ratio show empirical functional relations across massive linguistic datasets
  Evidence: lexical diversity is characterized in terms of the type-token ratio and the word entropy... investigate both diversity metrics in six massive linguistic datasets

**Paper B**: Entropy-Aware On-Policy Distillation of Language Models
  Claim: Entropy-based measures must balance mode-seeking precision with diversity preservation
  Evidence: mode-seeking property of reverse KL reduces generation diversity... balances mode-seeking precision with diversity preservation in high-entropy scenarios

**Relevance to thesis**: Different entropy measures could lead to different conclusions about whether web quality is declining
**Beat affected**: 2
**Suggested handling**: Specify which entropy measures we use and why they're appropriate for detecting quality degradation

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Is document comprehension quality declining over time?

**Paper A**: Evolution of Composition, Readability, and Structure of Privacy Policies over Tw
  Claim: Privacy policies remain persistently challenging to comprehend despite two decades of privacy design and regulatory advancements
  Evidence: users have often needed help reading and understanding such documents... fundamental problems with privacy policies persist despite advancements

**Paper B**: Triangulating Temporal Dynamics in Multilingual Swiss Online News
  Claim: Swiss multilingual digital media shows distinct temporal trends across linguistic regions in news coverage patterns
  Evidence: temporal trends in Swiss digital media... distinct temporal trends across French, German, and Italian linguistic regions

**Relevance to thesis**: One shows persistent quality issues, the other shows changing patterns without quality judgment
**Beat affected**: 3
**Suggested handling**: Note that quality degradation may be domain-specific - some text types maintain standards while others decline

---

## C5: 🟡 MODERATE — direct_contradiction

**Question**: Does data pruning/filtering solve quality problems in web-scraped data?

**Paper A**: When Less is More: Investigating Data Pruning for Pretraining LLMs at Scale
  Claim: Perplexity-based data pruning can maintain model performance while significantly reducing pretraining dataset size
  Evidence: efforts to prune these datasets down to a higher quality subset... maintain model performance while significantly reducing pretraining dataset size

**Paper B**: LLMs Can Get "Brain Rot"!
  Claim: Continual exposure to junk web text causes lasting cognitive decline in large language models
  Evidence: continual exposure to junk web text induces lasting cognitive decline... controlled experiments on real Twitter/X corpora

**Relevance to thesis**: One suggests quality issues are solvable through filtering, the other suggests fundamental degradation
**Beat affected**: 3
**Suggested handling**: Clarify that filtering can help but cannot reverse underlying quality decline in source material

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Can synthetic data improve model training without degradation?

**Paper A**: Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling L
  Claim: Mixing 1/3 rephrased synthetic data with 2/3 natural web texts speeds up pre-training 5-10x
  Evidence: Mixing 1/3 rephrased synthetic data with 2/3 natural web texts speeds up pre-training 5-10x

**Paper B**: Self-Improving Diffusion Models with Synthetic Data
  Claim: SIMS training can improve diffusion models using synthetic data without causing collapse
  Evidence: SIMS training concept can improve diffusion models using synthetic data without causing model collapse

**Relevance to thesis**: These papers show synthetic data works for specific ratios/domains, but don't address social behavioral data
**Beat affected**: 3
**Suggested handling**: Acknowledge that synthetic data can augment training in controlled proportions, but emphasize the domain-specificity: social behaviors require authentic human data

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Is human curation sufficient to prevent synthetic data problems?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: LLM-simulated human feedback is 50x cheaper than crowdworkers and shows high agreement with humans
  Evidence: LLM-simulated human feedback is 50x cheaper than crowdworkers and shows high agreement with humans

**Paper B**: AI Supported Degradation of the Self Concept: A Theoretical Framework Grounded i
  Claim: AI assistants trained with human feedback consistently exhibit sycophancy across text-generation tasks
  Evidence: human feedback may also encourage model responses that match user beliefs over truthful ones, a behaviour known as sycophancy

**Relevance to thesis**: Suggests even human feedback can be problematic, which could undermine our human data superiority claim
**Beat affected**: 4
**Suggested handling**: Distinguish between anonymous crowdworker feedback and authenticated campus behavioral data - quality and context of human data matters

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: Does parameter-efficient fine-tuning preserve or compromise social reasoning capabilities?

**Paper A**: MetaMind: Modeling Human Social Thoughts with Metacognitive Multi-Agent Systems
  Claim: MetaMind multi-agent framework emulates human-like social reasoning through collaborative Theory-of-Mind and Moral agents
  Evidence: System-based approach claims to achieve human-like social reasoning

**Paper B**: S3LoRA: Safe Spectral Sharpness-Guided Pruning in Adaptation of Agent Planner
  Claim: S3LoRA mitigates safety risks in LoRA-adapted models...can unintentionally compromise safety alignment, leading to unsafe or unstable behaviors
  Evidence: Shows that LoRA adaptations can compromise model behaviors in agent planning tasks

**Relevance to thesis**: Suggests that even with authentic data, fine-tuning methods may introduce new problems
**Beat affected**: 4
**Suggested handling**: Acknowledge that data quality alone isn't sufficient - proper training methods are also crucial

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Are current evaluation methods capturing real social intelligence?

**Paper A**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Social-R1 framework enables human-like social reasoning by training on adversarial cases that resist shortcuts
  Evidence: Claims to achieve human-like social reasoning through specialized training

**Paper B**: Multi-speaker Attention Alignment for Multimodal Social Interaction
  Claim: MLLMs show substantially weaker cross-modal attention in multi-speaker scenes compared to object-centric images
  Evidence: Shows fundamental limitations in social scene understanding despite claims of social intelligence

**Relevance to thesis**: Supports our argument that current approaches miss fundamental aspects of social interaction
**Beat affected**: 3
**Suggested handling**: Use to strengthen Beat 3 - even specialized social reasoning systems fail at basic multi-modal social tasks

---


## Summary

Total contradictions: 25
Critical (must address): 14

## Thesis Risk Assessments

- The contradictions reveal significant nuance in the synthetic data debate. While our core thesis about authentic human behavioral data remains defensible, we must acknowledge: (1) Synthetic data with proper curation can work for some tasks, (2) The definition and measurement of 'collapse' varies, (3) Some theoretical frameworks suggest self-improvement is possible. Our strongest position is to focus on the unique requirements of social behavioral data where authenticity cannot be synthesized.
- The contradictions reveal a fundamental challenge: while our thesis claims web pollution is detectable (Beat 5), the evidence shows detection is an active arms race with no clear winner. Papers show detection methods can achieve 80% accuracy but simple attacks reduce this by 17.4%, and paraphrasing can evade even watermarking. This doesn't invalidate our thesis but requires reframing: instead of claiming pollution is easily detectable, we should acknowledge the detection challenge and argue that CampusGo provides verified human data as a complementary solution rather than relying solely on detection.
- The contradictions reveal a critical weakness: while we claim web quality is declining, multiple papers show successful quality filtering and curation methods. The key distinction we must make is between relative improvements through filtering versus absolute quality decline in the raw web corpus. The measurement methodology tensions (C2, C4) are particularly concerning as they could undermine our empirical claims about degradation.
- The contradictions reveal significant nuance in the synthetic vs human data debate. While some papers show AI-generated data can match or exceed human data in specific domains (summarization, robotics), the key distinction appears to be domain-specificity. Our thesis remains defensible if we emphasize that social behavioral data has unique properties that synthetic data cannot replicate, particularly around authentic human interactions and avoiding adversarial manipulation.
- The contradictions reveal a fundamental split in the field: benchmarks show high performance (>93% on some ToM tasks) while behavioral studies show fundamental failures. This actually SUPPORTS our thesis by demonstrating that current evaluation methods are inadequate. The key risk is that readers might see high benchmark scores and question why CampusGo is needed - we must clearly articulate that these benchmarks test pattern matching, not genuine social understanding.