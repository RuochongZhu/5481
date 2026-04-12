# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Does recursive training on synthetic data inevitably cause collapse, or can verified synthetic data substitute safely?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated training data causes irreversible model collapse.
  Evidence: Key claim: recursively generated data makes 'tails of the original content distribution disappear' and creates 'irreversible defects'.

**Paper B**: Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinforcement
  Claim: Synthesized data can be used without collapse if it is reinforced by verification.
  Evidence: Key claim: 'Verification of synthesized data can prevent model collapse' because filtering good/bad samples is easier than generating them.

**Relevance to thesis**: Directly challenges any absolute claim that synthetic data cannot replace human data; it suggests replacement may work under heavy verification.
**Beat affected**: 4
**Suggested handling**: Acknowledge that collapse is shown for indiscriminate recursive reuse, but note counterclaims that verified synthetic pipelines can remain stable. Then argue that such verification still depends on externally grounded human reference signals, especially for social behavior.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Are self-consuming synthetic loops doomed without fresh real data, or can human curation make them beneficial?

**Paper A**: Self-Consuming Generative Models Go MAD
  Claim: Without sufficient fresh real data each generation, self-consuming generative models progressively lose precision or diversity.
  Evidence: Key claim: models are 'doomed' to degradation without 'sufficient fresh real data in each generation'.

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Self-consuming models with human-curated data can converge toward human-preference-optimal distributions rather than collapse.
  Evidence: Key claim: with 'human-curated data' they 'provably converge toward distributions that optimize human preferences rather than collapsing'.

**Relevance to thesis**: This is the core curation-vs-collapse dispute. It weakens a blanket irreplaceability claim unless we specify that the irreplaceable part is fresh, authentic human grounding rather than any human involvement at all.
**Beat affected**: 4
**Suggested handling**: Present the disagreement as condition-dependent: uncurated recursion collapses, but curated loops may optimize preferences. Then stress that preference optimization is not the same as preserving authentic human behavioral diversity or rare tails.

---

## C5: 🔴 CRITICAL — implicit_tension

**Question**: Even if curated synthetic data avoids formal collapse, does it preserve human sensibilities and individuality?

**Paper A**: The GenAI Future of Consumer Research
  Claim: GenAI trends toward an average-trap/model-collapse trajectory that erodes human sensibilities and individuality.
  Evidence: Key claim: outputs 'progressively lose human sensibilities and individuality'.

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: Human-curated self-consuming models can optimize human preferences instead of collapsing.
  Evidence: Key claim: curated loops converge to distributions that 'optimize human preferences rather than collapsing'.

**Relevance to thesis**: This is highly relevant to CampusGo: avoiding technical collapse may still produce homogenized, averaged behavior rather than authentic social variation. That supports a narrower thesis about irreplaceable human behavioral signals.
**Beat affected**: 4
**Suggested handling**: Separate two goals in writing: avoiding collapse versus preserving authentic human variance. Cite both papers and argue that preference optimization can still wash out the behavioral tails and individuality that matter for social-data training.

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Can machine-generated web pollution be detected reliably enough to filter training corpora and avoid degradation?

**Paper A**: Machine-generated text detection prevents language model collapse
  Claim: Machine-generated text detection can filter synthetic data from training sets and prevent model collapse.
  Evidence: "machine-generated text detection can be used to filter synthetic data from training sets and thereby prevent model collapse"

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Current AI-text detection methods face major limits because modern LLM output is becoming indistinguishable from human text.
  Evidence: "current AI-generated text detection methods ... face significant challenges as LLM outputs become increasingly indistinguishable from human text"

**Relevance to thesis**: This is the clearest disagreement on the focus question. If paper A is right, web pollution is detectable enough to mitigate; if paper B is right, detection is nearing its limits and web degradation is harder to control.
**Beat affected**: 2
**Suggested handling**: Do not claim that web pollution is simply undetectable. Write that detector-based filtering is a promising mitigation in some studies, but its general reliability remains disputed as model outputs become harder to distinguish from human text.

---

## C2: 🔴 CRITICAL — methodological_tension

**Question**: Are AI-text detectors robust to adversarial paraphrasing and style transfer?

**Paper A**: RADAR: Robust AI-Text Detection via Adversarial Learning
  Claim: RADAR's adversarial training significantly improves robustness against LLM-based paraphrasing attacks.
  Evidence: "significantly improves robustness against LLM-based paraphrasing attacks"

**Paper B**: Red Teaming Language Model Detectors with Language Models
  Claim: LLM-generated text detectors remain vulnerable to synonym replacement and instruction-driven style alteration.
  Evidence: "detectors are vulnerable to adversarial attacks using synonym replacement and instructional prompt-based style alteration"

**Relevance to thesis**: This tension matters because any claim that pollution can be detected at scale depends on robustness under realistic adversarial rewriting, not just clean benchmarks.
**Beat affected**: 2
**Suggested handling**: Frame robustness as detector-specific, not solved. Note that adversarial training helps on tested attacks, but red-teaming evidence shows broader attack surfaces still break many detectors.

---

## C3: 🔴 CRITICAL — scope_disagreement

**Question**: Does watermarking make synthetic text reliably detectable after downstream transformations?

**Paper A**: Adaptive Text Watermark for Large Language Models
  Claim: Adaptive watermarking preserves text quality while maintaining robust, secure, prompt-agnostic watermark detection.
  Evidence: "maintaining robust, secure, and prompt-agnostic watermark detection"

**Paper B**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Paraphrasing can evade multiple AI-text detectors, including watermarking-based approaches.
  Evidence: "Paraphrasing AI-generated text successfully evades multiple detectors including watermarking"

**Relevance to thesis**: This directly affects whether provenance-style defenses can keep polluted web text identifiable once it is reposted, edited, or laundered through paraphrase.
**Beat affected**: 2
**Suggested handling**: State that watermarking may help when generation is cooperative and text remains near-original, but transformed or re-authored content can still evade detection, limiting web-scale cleanup.

---

## C1: 🔴 CRITICAL — methodological_tension

**Question**: Can web-quality decline be established from abstract information-theoretic metrics, or does it require explicit longitudinal temporal measurement on text corpora?

**Paper A**: Understanding Encoder-Decoder Structures in Machine Learning Using Information M
  Claim: Information sufficiency and mutual information loss can formally characterize relevant predictive structures.
  Evidence: "information sufficiency and mutual information loss provide a formal characterization"

**Paper B**: Evaluating latent content within unstructured text: an analytical methodology ba
  Claim: Shifts in unstructured text should be evaluated through a temporal network of associated topics over time.
  Evidence: "enables systematic evaluation of shifts and changes in latent content within unstructured text over time"

**Relevance to thesis**: Directly affects the evidentiary standard for claiming that web quality is declining: metric-only arguments may be seen as insufficient without time-indexed corpus analysis.
**Beat affected**: 1
**Suggested handling**: State explicitly that information-theoretic metrics are proxy indicators of degradation, but claims about web-quality decline are grounded only when paired with longitudinal temporal measurements.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Do temporal studies support a general web-quality decline, or only domain-specific and region-specific patterns?

**Paper A**: Evolution of Composition, Readability, and Structure of Privacy Policies over Tw
  Claim: Privacy policies have remained hard to comprehend over two decades, indicating persistent low quality in that web genre.
  Evidence: "remained persistently challenging to comprehend over two decades"

**Paper B**: Triangulating Temporal Dynamics in Multilingual Swiss Online News
  Claim: Online news evolves with distinct temporal dynamics across linguistic regions rather than a single universal trajectory.
  Evidence: "reveals distinct temporal dynamics... across French, German, and Italian linguistic regions"

**Relevance to thesis**: Undermines any blanket statement that 'the web is declining' by showing that longitudinal evidence may support stagnation in one genre and heterogeneous evolution in another.
**Beat affected**: 1
**Suggested handling**: Narrow the claim from web-wide decline to genre-sensitive degradation; contrast persistent low-quality sectors with sectors showing heterogeneous temporal change.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Can AI-generated feedback replace human feedback for alignment?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: AI feedback can substitute for human feedback on standard alignment tasks.
  Evidence: RLAIF achieves comparable performance to RLHF across summarization and dialogue tasks.

**Paper B**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Human involvement remains fundamental when rewards are hard to specify.
  Evidence: Reinforcement learning is fundamentally a human-in-the-loop paradigm, particularly advantageous when reward functions are challenging to define.

**Relevance to thesis**: Directly challenges any blanket claim that human feedback is irreplaceable; suggests replaceability may hold for some alignment benchmarks.
**Beat affected**: 4
**Suggested handling**: State explicitly that AI feedback can match RLHF on narrow summarization/dialogue evaluations, but argue that this does not settle domains requiring grounded, hard-to-specify human social signals.

---

## C3: 🔴 CRITICAL — methodological_tension

**Question**: Is human feedback a reliable alignment signal?

**Paper A**: Summary of ChatGPT-Related Research and Perspective Towards the Future of Large 
  Claim: Instruction tuning plus RLHF are key drivers of modern LLM performance.
  Evidence: Large-scale pre-training combined with instruction fine-tuning and RLHF are presented as the key innovations driving LLM performance.

**Paper B**: AI Supported Degradation of the Self Concept: A Theoretical Framework Grounded i
  Claim: Human feedback can systematically reward the wrong behavior.
  Evidence: AI assistants fine-tuned with human feedback consistently exhibit sycophancy because preference judgments favor responses matching user beliefs over truthful ones.

**Relevance to thesis**: Undermines any naive equation of human data with high-quality signal; human feedback can be essential yet also corrupted.
**Beat affected**: 4
**Suggested handling**: Acknowledge that human data are not automatically gold-standard. Distinguish authentic behavioral data from preference labels, and argue that verification and protocol design are necessary to avoid sycophancy.

---

## C5: 🔴 CRITICAL — implicit_tension

**Question**: Does matching human annotators imply desirable alignment?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: Synthetic feedback is validated by agreement with human annotators.
  Evidence: LLM-simulated feedback shows high agreement with real human annotators.

**Paper B**: AI Supported Degradation of the Self Concept: A Theoretical Framework Grounded i
  Claim: Human preference judgments themselves can be biased toward agreement over truth.
  Evidence: Human feedback favors responses matching user beliefs, producing sycophancy.

**Relevance to thesis**: This weakens a common pro-synthetic argument: if the human target is flawed, synthetic agreement may only replicate the flaw faster.
**Beat affected**: 4
**Suggested handling**: Point out that 'human agreement' is not sufficient validation. Emphasize the need for carefully designed, behaviorally grounded human data rather than raw preference imitation.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Do strong commonsense benchmark results imply genuine social reasoning ability?

**Paper A**: UNICORN on RAINBOW: A Universal Commonsense Reasoning Model on a New Multitask B
  Claim: A unified commonsense model trained on Rainbow generalizes well across diverse commonsense tasks and datasets.
  Evidence: Reports broad cross-task generalization on the Rainbow multitask commonsense benchmark.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box.
  Evidence: Shows poor performance on social reasoning tasks about intents and reactions.

**Relevance to thesis**: Shows that benchmark composition matters: broad commonsense success does not transfer to socially grounded reasoning, supporting the need for authentic social-behavior signals.
**Beat affected**: 4
**Suggested handling**: In Related Work, explicitly separate commonsense benchmark generalization from interpersonal mental-state reasoning; do not treat Rainbow-style success as evidence that social reasoning is solved.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Can targeted training data move models beyond superficial social pattern matching?

**Paper A**: Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large L
  Claim: LLMs' apparent social reasoning abilities may reflect superficial pattern matching rather than genuine neural Theory of Mind.
  Evidence: Stress tests argue benchmark performance can be explained by shortcut-like cues rather than robust social inference.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Reinforcement learning on adversarially hard social reasoning examples improves LLM social intelligence beyond reliance on superficial patterns.
  Evidence: Claims gains from training on adversarially hard social reasoning examples specifically designed to reduce shortcut use.

**Relevance to thesis**: This is a central benchmark-vs-ablation tension: one paper says current performance is mostly artifact-driven, the other says carefully composed hard data can meaningfully improve it.
**Beat affected**: 4
**Suggested handling**: Acknowledge both: adversarial data may improve social reasoning, but stress-test evidence means such gains should not be interpreted as proof of human-like social understanding without broader validation.

---

## C3: 🔴 CRITICAL — methodological_tension

**Question**: Are current text-based ToM benchmarks sufficient to conclude that models lack social reasoning?

**Paper A**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box.
  Evidence: Negative conclusion is based on performance on text-based social reasoning tasks.

**Paper B**: CoMMET: To What Extent Can LLMs Perform Theory of Mind Tasks?
  Claim: Existing ToM benchmarks are limited by text-only inputs and narrow focus on belief tasks.
  Evidence: Introduces a multimodal, multi-turn benchmark because prior ToM evaluations under-cover mental states and interaction settings.

**Relevance to thesis**: This weakens any overly broad claim that text-only benchmark failures fully settle the question; benchmark composition itself is contested.
**Beat affected**: 4
**Suggested handling**: Cite early negative ToM results, but qualify that benchmark coverage is incomplete and that richer multimodal, multi-turn evaluation may change the picture.

---

## C5: 🔴 CRITICAL — implicit_tension

**Question**: Can non-human preference data replace human data for socially aligned behavior?

**Paper A**: Zephyr: Direct Distillation of LM Alignment
  Claim: Distilled direct preference optimization using AI feedback can achieve state-of-the-art alignment without human annotation.
  Evidence: Reports a 7B chat model reaching SOTA alignment via AI feedback rather than human labels.

**Paper B**: Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large L
  Claim: Apparent social reasoning ability may still be superficial pattern matching.
  Evidence: Stress tests show socially plausible outputs can arise from shortcuts rather than genuine Theory of Mind.

**Relevance to thesis**: This is the clearest challenge to the thesis: AI-generated supervision can improve alignment metrics, so 'human data is irreplaceable' must be narrowed to robust social reasoning, not generic chat alignment.
**Beat affected**: 4
**Suggested handling**: Concede that AI feedback can substitute for human labels on some alignment benchmarks, then argue that such gains do not establish behaviorally verified social reasoning or authentic human social understanding.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Do synthetic-data generations break scaling laws, or can synthetic data be added safely if original real data is preserved?

**Paper A**: A Tale of Tails: Model Collapse as a Change of Scaling Laws
  Claim: Synthetic data contamination causes scaling-law decay, loss of scaling, and tail narrowing across generations.
  Evidence: Key claim: contamination leads to 'loss of scaling' and 'tail narrowing across model generations'.

**Paper B**: Universality of the $π^2/6$ Pathway in Avoiding Model Collapse
  Claim: An augment workflow that keeps original real data alongside synthetic data universally avoids model collapse.
  Evidence: Key claim: retaining original real data with synthetic data 'universally avoids model collapse'.

**Relevance to thesis**: This does not refute the thesis so much as narrow it: full replacement looks risky, while augmentation with retained real data may be viable.
**Beat affected**: 4
**Suggested handling**: Explicitly distinguish replacement from augmentation. Concede that synthetic data can help when seed human data remains in the loop, while maintaining that replacing authentic human data entirely is far less supported.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Is model collapse an inherent consequence of self-consumption, or can it be removed by correction toward the true distribution?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive synthetic training produces irreversible distributional defects.
  Evidence: Key claim: recursive training causes irreversible loss of tails in the original distribution.

**Paper B**: Self-Correcting Self-Consuming Loops for Generative Model Training
  Claim: Self-consuming loops become exponentially more stable if a correction function maps samples back toward the true distribution.
  Evidence: Key claim: an 'idealized correction function' makes loops 'exponentially more stable'.

**Relevance to thesis**: The tension is methodological: collapse results are empirical/mixed, while the stability result depends on access to a correction oracle toward the true distribution. That matters because authentic human data may be exactly what is needed to instantiate such correction.
**Beat affected**: 4
**Suggested handling**: Note that anti-collapse guarantees rely on a correction mechanism approximating the true distribution. Argue that for social-behavioral data, obtaining that correction signal is itself a human-data bottleneck.

---

## C6: 🟡 MODERATE — implicit_tension

**Question**: Where do current performance gains come from in practice: synthetic-data substitution, or better curation of original human/web corpora?

**Paper A**: Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinforcement
  Claim: Scaling with synthesized data is feasible when the synthetic data is reinforced by verification.
  Evidence: Key claim: verified synthesized data can prevent collapse and support scaling.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: Better-performing LLMs can be obtained through careful filtering, deduplication, and curation of massive web data.
  Evidence: Key claim: FineWeb's carefully ablated filtering on 15T tokens 'produces better-performing LLMs than other open pretraining datasets'.

**Relevance to thesis**: This does not prove synthetic replacement fails, but it shows that the strongest practical gains in open pretraining still come from curation of human/web data rather than demonstrated substitution by synthetic data.
**Beat affected**: 4
**Suggested handling**: Use this as a pragmatic contrast: even if synthetic data can be made safer, current empirical wins still come from curation of real corpora. That supports framing synthetic data as a supplement, not a demonstrated replacement, for authentic human sources.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Can detectability be restored through retrieval/provenance methods even when detector scores fail?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Although paraphrasing breaks many detectors, retrieval-based detection remains effective.
  Evidence: "paraphrasing evades detectors ... but retrieval is an effective defense"

**Paper B**: Simple techniques to bypass GenAI text detectors: implications for inclusive edu
  Claim: Simple manipulations substantially reduce detector accuracy, making detectors unreliable in practice.
  Evidence: "simple manipulation techniques reduce GenAI text detector accuracy by 17.4%, making them unreliable"

**Relevance to thesis**: The disagreement is not whether evasion exists, but whether alternative provenance-aware methods can recover detectability. That matters for claims about detection limits on polluted web data.
**Beat affected**: 2
**Suggested handling**: Differentiate text-only classification from provenance/retrieval approaches. Acknowledge that many deployed detectors are brittle, while retrieval may work when source overlap or searchable provenance exists.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Is synthetic pollution broadly detectable from text alone, or only when extra metadata/provenance signals are available?

**Paper A**: Multi-Modal Anomaly Detection in Review Texts with Sensor-Derived Metadata Using
  Claim: A zero-shot multi-modal framework using review text plus sensor-derived metadata effectively detects fake reviews.
  Evidence: "combining language perplexity scoring, autoencoder reconstruction, and semantic drift analysis effectively detects fake reviews"

**Paper B**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: General AI-text detection is increasingly challenged because outputs are hard to distinguish from human text.
  Evidence: "current methods ... face significant challenges as LLM outputs become increasingly indistinguishable from human text"

**Relevance to thesis**: This is highly relevant to CampusGo. It suggests detectability improves when authentic behavioral or physical metadata exists, while text-only open-web filtering remains unreliable.
**Beat affected**: 4
**Suggested handling**: Use this to sharpen, not overstate, the thesis: generic web pollution may be hard to detect from text alone, but physically grounded metadata can provide stronger authenticity signals than ordinary scraped corpora.

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: What should count as evidence of quality degradation: statistical entropy/diversity signals or human-facing readability/comprehensibility measures?

**Paper A**: Entropy-Aware On-Policy Distillation of Language Models
  Claim: Teacher entropy is a key signal for preserving diversity and stabilizing learning, making entropy-based metrics central to degradation diagnosis.
  Evidence: "when teacher entropy is high... preserves generation diversity and stabilizes learning signals"

**Paper B**: Evolution of Composition, Readability, and Structure of Privacy Policies over Tw
  Claim: Document quality is evidenced by readability, composition, and structure, which remained poor over time for privacy policies.
  Evidence: "composition, readability, and structure... remained persistently challenging to comprehend"

**Relevance to thesis**: Creates a definitional risk: if our thesis means human usefulness/comprehensibility, model-centric entropy metrics do not by themselves prove web-quality decline.
**Beat affected**: 1
**Suggested handling**: Define 'quality' on multiple axes in Related Work: statistical diversity/information content versus human comprehensibility, and avoid treating them as interchangeable.

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Is cheap simulated feedback enough, or is fine-grained human supervision still needed?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: LLM-simulated human feedback is an efficient substitute for crowdworkers in instruction-following training.
  Evidence: Simulated human feedback is 50x cheaper than crowdworkers while displaying high agreement with real human annotators.

**Paper B**: Let's Verify Step by Step
  Claim: Outcome-level signals are insufficient; detailed supervision on reasoning steps matters.
  Evidence: Process supervision providing feedback on each intermediate reasoning step significantly outperforms outcome supervision for reliable mathematical reasoning.

**Relevance to thesis**: Supports a narrower thesis: synthetic proxies may work for coarse preference labeling, but not necessarily for richer human reasoning supervision.
**Beat affected**: 4
**Suggested handling**: Frame this as a task-boundary result: simulated preference labels help instruction following, whereas domains needing step-level judgment still benefit from richer human supervision.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Is extensive human annotation necessary for alignment?

**Paper A**: Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Hum
  Claim: LLMs can self-align with minimal human supervision.
  Evidence: SELF-ALIGN enables self-alignment from scratch with minimal human supervision, reducing reliance on costly human annotations.

**Paper B**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Human involvement is a core requirement of alignment when objectives are underspecified.
  Evidence: Human-in-the-loop approaches are particularly advantageous when reward functions are challenging to define.

**Relevance to thesis**: Challenges a strong necessity claim for human annotation, but only under specific self-alignment setups and evaluation regimes.
**Beat affected**: 4
**Suggested handling**: Concede that extensive annotation may not be necessary for some assistant-style alignment pipelines; then argue our thesis concerns socially grounded data collection, not generic instruction tuning alone.

---

## C6: 🟡 MODERATE — methodological_tension

**Question**: Are model gains driven mainly by better data curation or by human-feedback alignment?

**Paper A**: Yi: Open Foundation Models by 01.AI
  Claim: Performance gains are primarily from large-scale data quality engineering.
  Evidence: Yi performance is primarily attributed to data quality from rigorous data-engineering efforts on a 3.1T-token corpus rather than architectural innovations.

**Paper B**: Summary of ChatGPT-Related Research and Perspective Towards the Future of Large 
  Claim: Instruction tuning and RLHF are central innovations behind LLM capability/usability.
  Evidence: The survey identifies instruction fine-tuning and RLHF as key innovations driving ChatGPT-class systems.

**Relevance to thesis**: Creates attribution tension for our story: some literature assigns major gains to curation of web data, not to human feedback.
**Beat affected**: 4
**Suggested handling**: Avoid claiming that human feedback is the sole driver of useful behavior. Instead argue that curation boosts base capability, while authentic human data become more important for social grounding, preference realism, and behavior under ambiguity.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Is pretraining's implicit knowledge enough for social reasoning without targeted social data?

**Paper A**: TSGP: Two-Stage Generative Prompting for Unsupervised Commonsense Question Answe
  Claim: Implicit knowledge in pretrained language models can outperform retrieval-based methods for unsupervised commonsense QA.
  Evidence: Two-stage generative prompting beats retrieval-style unsupervised commonsense QA baselines without labeled task data.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks social intelligence and Theory of Mind out-of-the-box.
  Evidence: Poor performance on tasks requiring inference about intents, reactions, and mental states.

**Relevance to thesis**: Supports a narrow version of the thesis: generic web-scale pretraining may encode enough for commonsense QA, but not enough for deeper social reasoning.
**Beat affected**: 4
**Suggested handling**: Write this as a scope boundary: pretrained knowledge can help generic commonsense completion, yet socially situated inference still appears data-hungry and under-specified.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: What data composition is best for improving social reasoning: easy-to-hard curricula or adversarially hard examples?

**Paper A**: On Curriculum Learning for Commonsense Reasoning
  Claim: Human-like easy-to-difficult curriculum learning improves commonsense reasoning over random data ordering.
  Evidence: Finetuning with easy-to-difficult sample ordering outperforms random ordering on commonsense tasks.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Adversarially hard social reasoning examples improve social intelligence.
  Evidence: Uses RL on deliberately hard cases rather than a human-like easy-to-difficult curriculum.

**Relevance to thesis**: Both say composition matters, but they point to different recipes; this matters if the paper argues for a single preferred social-data construction strategy.
**Beat affected**: 4
**Suggested handling**: Present this as an open design tension: curriculum may help broad reasoning, while hard-case emphasis may be especially valuable for debiasing social shortcuts.

---


## Summary

Total contradictions: 26
Critical (must address): 15

## Thesis Risk Assessments

- Risk is high if the paper states an absolute thesis that synthetic data cannot replace human data in general. Multiple 2024 papers argue that collapse is not inevitable when synthetic data is verified, curated by humans, or mixed with retained real data. A safer and more defensible thesis is narrower: uncurated recursive synthetic training degrades tails and diversity, and authentic human social-behavioral data remains necessary for grounding, verification, and preserving rare or individualized behavior that synthetic pipelines tend to average away.
- Moderate risk. The literature does not support a categorical claim that web pollution is undetectable: one paper explicitly argues detector-based filtering can prevent collapse, and several papers report robust detector or watermark variants. However, the counterevidence is broader and more pessimistic: multiple studies show successful evasion by paraphrasing, simple edits, or style transfer, and surveys emphasize that newer LLM outputs are increasingly hard to distinguish from human writing. The safest Related Work position is that pollution detection is possible in bounded settings, but remains attack-sensitive, method-dependent, and often reliant on extra provenance or metadata rather than a reliable general web-scale filter.
- High risk for overclaiming. Within categories D and H, there is no clean consensus that web quality is globally declining. The strongest tension is methodological: D papers support proxy-metric approaches to degradation, while H papers emphasize explicit temporal measurement and show domain- or region-specific trajectories rather than a universal decline curve. Our thesis should therefore avoid web-wide decline language unless it is tightly scoped and supported by longitudinal corpus evidence.
- The main risk is overclaiming. Several papers indicate that AI-generated or minimally human-supervised feedback can match RLHF on narrow benchmarks, so the literature does not support a universal statement that human-generated data are always irreplaceable. At the same time, other papers show that human preference data can itself be flawed, especially via sycophancy, which means 'human data' must be qualified carefully. The safest defensible thesis is narrower: curated synthetic or AI feedback can substitute for some instruction-following and benchmark alignment tasks, but authentic, well-verified human social-behavioral data remain hard to replace when the target is representativeness, grounded social behavior, or objectives that are difficult to specify and vulnerable to preference-label artifacts.
- Overall, the literature supports the claim that data composition matters, but it does not cleanly support the strongest version of 'authentic human social data is irreplaceable.' The main risk comes from Zephyr and Social-R1: they suggest that non-human or synthetic/adversarially constructed data can substantially improve alignment and social-reasoning benchmark performance. At the same time, Neural Theory-of-Mind, Clever Hans, and CoMMET show that benchmark choice strongly affects conclusions, and that broad commonsense or alignment gains should not be conflated with robust social reasoning. The safest thesis is narrower: authentic, behaviorally verified human social data remains uniquely valuable for robust, multimodal, distributionally stable social reasoning, even if AI-generated or synthetic supervision can improve narrower text-only benchmarks.