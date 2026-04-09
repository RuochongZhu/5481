# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can synthetic/generated data be used to train models without quality degradation?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated content causes irreversible model collapse where distribution tails disappear
  Evidence: AI models collapse when trained on recursively generated data - demonstrates irreversible defects

**Paper B**: Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Re
  Claim: Accumulating real and synthetic data over time can break the curse of model collapse
  Evidence: Title explicitly states breaking the curse of recursion by accumulating real AND synthetic data

**Relevance to thesis**: Directly challenges our claim that synthetic data causes information degradation - one paper supports our thesis while another claims the problem can be solved
**Beat affected**: 4
**Suggested handling**: Acknowledge in §2 that the model collapse debate is ongoing, with recent work (2024) suggesting accumulation strategies might mitigate collapse, but emphasize our focus on social/behavioral data where such strategies may not apply

---

## C3: 🔴 CRITICAL — methodological_tension

**Question**: How severe is the model collapse phenomenon?

**Paper A**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Claim: Training on model-generated content causes irreversible defects where distribution tails disappear
  Evidence: The Curse of Recursion - empirically demonstrates irreversible degradation

**Paper B**: On the Stability of Iterative Retraining of Generative Models on their own Data
  Claim: Training generative models on mixed real and synthetic datasets has measurable stability impacts
  Evidence: Focuses on stability rather than collapse, suggesting the problem is manageable

**Relevance to thesis**: Different characterizations of the same phenomenon - one says irreversible, another says manageable
**Beat affected**: 4
**Suggested handling**: Present both perspectives but emphasize that even 'manageable' degradation is unacceptable for authentic human behavioral data collection

---

## C5: 🔴 CRITICAL — direct_contradiction

**Question**: Does the scale of synthetic data generation compensate for quality issues?

**Paper A**: A Tale of Tails: Model Collapse as a Change of Scaling Laws
  Claim: Model collapse manifests as changes in scaling laws when synthetic data enters training corpora
  Evidence: Shows that scaling laws fundamentally change with synthetic data

**Paper B**: Data-centric Artificial Intelligence: A Survey
  Claim: The role of data in AI has been significantly magnified, giving rise to the emerging concept of data-centric AI
  Evidence: Survey emphasizing quantity and curation of data without distinguishing synthetic vs. real

**Relevance to thesis**: One shows synthetic data breaks scaling assumptions, other treats all data equally in data-centric AI
**Beat affected**: 2
**Suggested handling**: Use the scaling law changes as strong evidence that synthetic and real data are fundamentally different

---

## C1: 🔴 CRITICAL — methodological_tension

**Question**: Can AI-generated content be reliably detected at scale?

**Paper A**: Cognitive Constraint Simulation and the Geometry of Human Authorship: A First-Pr
  Claim: LLM-generated text can be detected through negative curvature regions of log probability function
  Evidence: We identify a property of the structure of an LLM's probability function that is useful for such detection... text sampled from an LLM tends to occupy negative curvature regions

**Paper B**: Machine-Generated Text: A Comprehensive Survey of Threat Models and Detection Me
  Claim: Machine-generated text is increasingly difficult to distinguish with significant technical challenges
  Evidence: Machine-generated text is increasingly difficult to distinguish from text authored by humans... Detection of machine-generated text presents significant technical challenges with numerous open problems

**Relevance to thesis**: Critical for determining if web pollution from AI content is actually detectable at the scale our thesis assumes
**Beat affected**: 3
**Suggested handling**: Acknowledge in §3 that while theoretical detection methods exist, practical deployment at web scale remains an open challenge, supporting our need for authentic human data sources

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can model collapse be avoided when training on synthetic data?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated content causes irreversible model collapse
  Evidence: Model collapse is irreversible where distribution tails disappear

**Paper B**: Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Generating W
  Claim: Model collapse can be avoided by managing how available data are used in pretraining workflows
  Evidence: Experiments show collapse can be contained through proper data management

**Relevance to thesis**: Critical for Beat 3 claim about information degradation - some papers suggest it's manageable
**Beat affected**: 3
**Suggested handling**: Acknowledge in §4 that while some argue collapse is avoidable through careful data curation, this requires human verification and authentic data mixing - supporting our thesis

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: What constitutes 'model collapse' and how severe is it?

**Paper A**: Position: Model Collapse Does Not Mean What You Think
  Claim: Model collapse research encompasses eight distinct definitions causing fundamental misunderstanding
  Evidence: Industry leaders and journals have prophesied catastrophic consequences based on misunderstood definitions

**Paper B**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Claim: Training on model-generated content causes irreversible defects
  Evidence: Clear demonstration of distribution tail disappearance

**Relevance to thesis**: Fundamental to our degradation argument - if 'collapse' has 8 different meanings, which one supports our thesis?
**Beat affected**: 3
**Suggested handling**: Must clarify in §2 which definition of model collapse we adopt and why it matters for social behavioral data specifically

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can synthetic data prevent model collapse when used recursively?

**Paper A**: Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Re
  Claim: Accumulating real and synthetic data over time can break the curse of model collapse
  Evidence: Recent investigations into model-data feedback loops proposed that such loops would lead to model collapse... accumulating real and synthetic data can break this curse

**Paper B**: Open Problems and Fundamental Limitations of Reinforcement Learning from Human F
  Claim: RLHF has fundamental limitations that require a multi-faceted approach to safer AI development
  Evidence: RLHF has emerged as the central method... there has been relatively little public work systematizing its flaws... fundamental limitations of RLHF

**Relevance to thesis**: Critical for Beat 4's claim about irreplaceable human data - if synthetic data accumulation prevents collapse, it challenges our core argument
**Beat affected**: 4
**Suggested handling**: Acknowledge that while accumulation may delay collapse, it doesn't eliminate the need for authentic human behavioral data, especially for social reasoning tasks

---

## C3: 🔴 CRITICAL — methodological_tension

**Question**: Can self-generated data produce high-quality training sets?

**Paper A**: Baize: An Open-Source Chat Model with Parameter-Efficient Tuning on Self-Chat Da
  Claim: Parameter-efficient tuning on self-generated chat data creates models with good multi-turn dialogue performance
  Evidence: We propose a pipeline that can automatically generate a high-quality multi-turn chat corpus by leveraging ChatGPT to engage in a conversation with itself

**Paper B**: Combating misinformation in the age of LLMs: Opportunities and challenges
  Claim: LLMs can both combat and generate misinformation at scale
  Evidence: LLMs can be a double-edged sword... LLMs bring promising opportunities for combating misinformation... [but also generate it]

**Relevance to thesis**: Self-generated data may appear high-quality but could propagate misinformation - supports Beat 3's information cascade concerns
**Beat affected**: 3
**Suggested handling**: Highlight that self-chat data lacks grounding in real human interactions and may amplify biases, supporting our authentic data argument

---

## C5: 🔴 CRITICAL — direct_contradiction

**Question**: Can synthetic social data adequately simulate human social interactions?

**Paper A**: Social Simulacra: Creating Populated Prototypes for Social Computing Systems
  Claim: Social simulacra can generate realistic social interactions for prototyping at scale
  Evidence: Social simulacra can generate realistic social interactions for prototyping social computing systems at scale

**Paper B**: A Pre-Training Based Personalized Dialogue Generation Model with Persona-Sparse 
  Claim: Persona-sparse data is a fundamental problem in dialogue systems
  Evidence: This problem is still far from well explored due to... the persona sparsity issue observed in most dialogue corpora

**Relevance to thesis**: Directly relevant - if simulacra work, why need CampusGo? But persona sparsity shows synthetic can't capture human diversity
**Beat affected**: 7
**Suggested handling**: Acknowledge simulacra for prototyping but emphasize they lack authentic behavioral grounding needed for real social understanding

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Is synthetic data generation beneficial for AI development?

**Paper A**: Self-Consuming Generative Models go MAD
  Claim: Without enough fresh real data, autophagous generative models progressively decrease in quality or diversity
  Evidence: Self-Consuming Generative Models go MAD - demonstrates progressive quality degradation

**Paper B**: Unnatural Instructions: Tuning Language Models with (Almost) No Human Labor
  Claim: Language models can generate 240,000 diverse instruction examples with virtually no human labor
  Evidence: Unnatural Instructions successfully uses synthetic data for instruction tuning

**Relevance to thesis**: Shows synthetic data works for some tasks (instruction generation) but fails for others - need to clarify our scope
**Beat affected**: 1
**Suggested handling**: Clarify that our thesis specifically concerns social behavioral data and human interaction patterns, not all types of synthetic data generation

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Can AI-generated social data replace human social data?

**Paper A**: Social Simulacra: Creating Populated Prototypes for Social Computing Systems
  Claim: Social simulacra can generate realistic social interactions for prototyping social computing systems at scale
  Evidence: Successfully creates populated prototypes using AI-generated social behaviors

**Paper B**: Towards Understanding the Interplay of Generative Artificial Intelligence and th
  Claim: Generative AI tools create feedback loops by contributing AI-generated content to future training data repositories
  Evidence: Warns about the societal impacts of AI-generated content polluting training data

**Relevance to thesis**: Social Simulacra suggests AI can simulate human social behavior, undermining our claim that authentic human data is irreplaceable
**Beat affected**: 5
**Suggested handling**: Distinguish between prototyping/simulation (where approximations suffice) and training data collection (where authenticity matters)

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Are current AI systems capable of generating undetectable fake content?

**Paper A**: GenAI against humanity: nefarious applications of generative artificial intellig
  Claim: GenAI creates indistinguishable deepfakes that blur reality
  Evidence: Picture living in a world where deepfakes are indistinguishable from reality, where synthetic

**Paper B**: TweepFake: About detecting deepfake tweets
  Claim: Deepfake tweets can be detected with appropriate systems
  Evidence: A deepfake tweet detection system is needed to prevent adversaries from exploiting GPT-2-like models

**Relevance to thesis**: Affects whether web pollution is a detectable problem or an invisible crisis
**Beat affected**: 2
**Suggested handling**: Clarify that detection capability varies by domain - text may be detectable in constrained contexts (tweets) but not in general web content

---

## C3: 🟡 MODERATE — implicit_tension

**Question**: Do AI systems rely on spurious correlations rather than genuine understanding?

**Paper A**: AI for radiographic COVID-19 detection selects shortcuts over signal
  Claim: COVID-19 detection AI relies on confounding factors not medical pathology
  Evidence: deep learning systems to detect COVID-19 from chest radiographs rely on confounding factors rather than medical pathology

**Paper B**: Bad Actor, Good Advisor: Exploring the Role of Large Language Models in Fake New
  Claim: GPT-3.5 can effectively expose fake news with multi-perspective rationales
  Evidence: GPT 3.5 can expose fake news with multi-perspective rationales but underperforms fine-tuned BERT

**Relevance to thesis**: Suggests AI systems trained on web data may learn spurious patterns rather than genuine human behavior
**Beat affected**: 4
**Suggested handling**: Use as evidence that web-scraped training data leads to brittle models that fail on real-world tasks, supporting need for authentic behavioral data

---

## C3: 🟡 MODERATE — direct_contradiction

**Question**: Can models improve when trained on contaminated/synthetic data?

**Paper A**: Heat Death of Generative Models in Closed-Loop Learning
  Claim: Closed-loop training leads to knowledge collapse and distribution degeneration
  Evidence: Empirical demonstration of degradation in closed-loop scenarios

**Paper B**: From Collapse to Improvement: Statistical Perspectives on the Evolutionary Dynam
  Claim: Models can improve when trained on contaminated data if sufficient fresh information is maintained
  Evidence: Statistical analysis shows potential for improvement with fresh data mixing

**Relevance to thesis**: Suggests our authentic human data could be the 'fresh information' needed to prevent collapse
**Beat affected**: 4
**Suggested handling**: Use this tension to strengthen our argument - improvement requires authentic human data streams, exactly what CampusGo provides

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Is model collapse inevitable in all domains?

**Paper A**: How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model 
  Claim: Model collapse cannot be avoided when training solely on synthetic data
  Evidence: Theoretical analysis shows unavoidable degradation with pure synthetic data

**Paper B**: When Models Don't Collapse: On the Consistency of Iterative MLE
  Claim: Model collapse in MLE can be avoided under standard assumptions
  Evidence: Mathematical proof under specific conditions

**Relevance to thesis**: The disagreement on inevitability supports our focus on domains where collapse is most severe
**Beat affected**: 3
**Suggested handling**: Clarify that for social behavioral tasks specifically, collapse appears inevitable without authentic data

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Is synthetic data generation effective for specialized domains?

**Paper A**: Brain Tumor Classification Using a Combination of Variational Autoencoders and G
  Claim: Combining variational autoencoders and GANs solves the limitation of insufficient medical imaging data
  Evidence: Recent advances in deep learning for medical imaging have shown remarkable results... combining VAE and GANs solves insufficient data limitation

**Paper B**: Unnatural Instructions: Tuning Language Models with (Almost) No Human Labor
  Claim: Language models can generate diverse instruction examples but with noise
  Evidence: We collect 240,000 diverse instruction examples with virtually no human labor... dataset contains a fair amount of noise

**Relevance to thesis**: Shows synthetic data works for structured domains (medical imaging) but fails for nuanced human language tasks
**Beat affected**: 4
**Suggested handling**: Use this contrast to support Beat 4 - synthetic data succeeds in constrained domains but fails for open-ended human behavioral tasks

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Does scale alone improve data quality and model performance?

**Paper A**: The Falcon Series of Open Language Models
  Claim: Falcon-180B trained on 3.5 trillion web tokens outperforms previous models
  Evidence: Falcon-180B has been trained on over 3.5 trillion tokens of text--the largest openly documented pretraining run

**Paper B**: The Power of Noise: Redefining Retrieval for RAG Systems
  Claim: The retrieval component of RAG systems deserves increased research attention for improved performance
  Evidence: RAG has become increasingly important... the retrieval component deserves increased research attention

**Relevance to thesis**: Scale without quality (Falcon) vs. targeted retrieval (RAG) - supports our argument that quality authentic data > quantity
**Beat affected**: 1
**Suggested handling**: Use to argue that massive web scraping (Falcon) is reaching diminishing returns, while targeted authentic data (our approach) provides better signal

---

## C4: 🟢 MINOR — direct_contradiction

**Question**: Can LLMs provide reliable judgments for information retrieval tasks?

**Paper A**: Perspectives on Large Language Models for Relevance Judgment
  Claim: LLM judgments may correlate with trained human assessors for retrieval evaluation
  Evidence: LLM-based relevance judgments may correlate with trained human assessors for retrieval system evaluation

**Paper B**: A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challe
  Claim: LLMs are prone to hallucination, generating nonfactual content in IR systems
  Evidence: LLMs are prone to hallucination, generating plausible yet nonfactual content... raises significant concerns over the reliability of LLMs in real-world information retrieval (IR) systems

**Relevance to thesis**: Minor tension about whether AI can replace human judgment, but both support that human verification is still needed
**Beat affected**: 1
**Suggested handling**: Note in footnote that even when LLMs show correlation with human judgments, hallucination risks make human verification essential

---

## C5: 🟢 MINOR — implicit_tension

**Question**: How quickly does quality degradation occur?

**Paper A**: A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspecti
  Claim: Collapse manifests as transition from generalization to memorization driven by declining entropy
  Evidence: Entropy-based measurements show gradual degradation

**Paper B**: A Tale of Tails: Model Collapse as a Change of Scaling Laws
  Claim: Model collapse manifests as changes in scaling laws
  Evidence: Scaling law analysis reveals different degradation patterns

**Relevance to thesis**: Different metrics show different degradation rates - which matters for urgency of our solution
**Beat affected**: 3
**Suggested handling**: Note in limitations that degradation speed varies by metric, but all show eventual decline

---


## Summary

Total contradictions: 19
Critical (must address): 9

## Thesis Risk Assessments

- The contradictions reveal significant ongoing debate about synthetic data's viability. The most critical challenge comes from recent 2024 work claiming accumulation strategies can prevent model collapse (C1). The Social Simulacra paper (C4) also poses a direct challenge by demonstrating AI-generated social interactions. However, most papers support concerns about synthetic data quality, and none specifically address authentic human behavioral data for social applications. The key is to narrow our claims to the specific domain of social behavioral signals rather than all synthetic data.
- The contradictions reveal significant uncertainty about the detectability of web pollution at scale. While theoretical detection methods exist (C1), practical deployment remains challenging. The scope disagreements (C2) suggest detection capability is domain-specific, which could undermine claims about widespread undetectable pollution. However, evidence of AI systems learning spurious correlations (C3) strongly supports our thesis that web-scraped data produces brittle models. Overall risk: MODERATE - we should emphasize detection difficulty rather than impossibility, and focus on the quality degradation aspect rather than pure detectability.
- The contradictions reveal significant debate about model collapse severity and inevitability. However, most papers agree that pure synthetic data training causes problems, and mixing with authentic data helps - directly supporting our thesis. The key risk is the definitional confusion around 'model collapse' which we must address clearly.
- The accumulation paper (C1) poses the highest risk by suggesting synthetic+real data accumulation prevents collapse. However, this can be countered by: 1) Their approach still requires continuous real data injection, 2) They don't test on social/behavioral tasks where authenticity matters most, 3) The fundamental information theory limits (Beat 2) still apply. The social simulacra paper (C5) is also concerning but can be positioned as useful for prototyping, not production systems requiring real human understanding.