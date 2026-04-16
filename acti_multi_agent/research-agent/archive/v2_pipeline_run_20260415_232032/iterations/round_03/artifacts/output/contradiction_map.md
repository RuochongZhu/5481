# Contradiction & Tension Map

*Papers that disagree — must be addressed in Related Work for academic honesty*

---

## Executive Summary

1. When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) → Is recursive use of synthetic data inherently collapse-inducing, or can carefully curated synthetic data safely replace fresh human data across retraining rounds?
   Handling: Narrow the thesis from 'synthetic data causes collapse' to 'uncurated or provenance-blind recursive synthetic data causes collapse.' Explicitly distinguish indiscriminate self-consumption from preference-aware curation regimes. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.
2. Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) → Does AI-feedback benchmark parity imply that human data is no longer needed for socially grounded alignment?
   Handling: Explicitly separate generic alignment performance from representational legitimacy. Argue that AI feedback may be enough for narrow task rewards, while human data remains necessary to capture pluralistic social viewpoints and to audit whose values the model reflects. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
3. How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? → Can AI-generated alignment data fully replace human-authored supervision, or do human post-edits still deliver measurably better dialogue quality?
   Handling: State that synthetic or AI-feedback alignment can replace much of the annotation burden for benchmarked instruction following, but not necessarily the last-mile quality gains from human post-editing, especially for conversational polish or domain adaptation. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.
4. Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? → Can improved corpus construction overturn the negative lessons drawn from earlier web-corpus audits?
   Handling: Use C4 as evidence that documentation and auditing are necessary, not as proof that web corpora are inherently lower quality. Present FineWeb as counterevidence showing that better construction materially changes outcomes. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
5. How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) → Is the strongest measurable drift about declining content quality, or about shrinking legal/consent availability of web data?
   Handling: Split Beat 2 into separate axes: content-quality drift, contamination drift, and consent/access drift. Do not let legal degradation stand in for textual degradation. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.
6. Does data composition matter for social reasoning? (benchmarks vs ablation) → Do small amounts of carefully curated post-training data improve social reasoning itself, or mostly general alignment and chat preference?
   Handling: Treat LIMA-style curation as evidence for alignment sensitivity, not as evidence that social reasoning benchmarks will improve unless those benchmarks are tested directly after tuning. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

## Focus Coverage

- [A, E] When can curated or verified synthetic data substitute for fresh human data? (collapse vs curation) (count=6)
  Representative: Is recursive use of synthetic data inherently collapse-inducing, or can carefully curated synthetic data safely replace fresh human data across retraining rounds?
- [E, F] Where does human data remain valuable despite curated synthetic or AI-feedback data? (curation vs RLHF) (count=6)
  Representative: Does AI-feedback benchmark parity imply that human data is no longer needed for socially grounded alignment?
- [F, J] How far can AI feedback, self-alignment, and synthetic instruction data reduce reliance on human-authored supervision? (count=5)
  Representative: Can AI-generated alignment data fully replace human-authored supervision, or do human post-edits still deliver measurably better dialogue quality?
- [B, E, H] Do filtered or documented web corpora complicate a simple contamination-to-quality-decline story? (count=5)
  Representative: Can improved corpus construction overturn the negative lessons drawn from earlier web-corpus audits?
- [D, H] How strong is the evidence for measurable live-web drift or degradation? (metrics vs temporal measurement) (count=6)
  Representative: Is the strongest measurable drift about declining content quality, or about shrinking legal/consent availability of web data?
- [I, J] Does data composition matter for social reasoning? (benchmarks vs ablation) (count=6)
  Representative: Do small amounts of carefully curated post-training data improve social reasoning itself, or mostly general alignment and chat preference?
- [B, C] Is web pollution detectable? (pollution scale vs detection limits) (count=6)
  Representative: Do algorithmic detection methods make web pollution broadly detectable, or only detectable for cooperatively marked outputs?
- [K] Does inference-time scaling reduce the importance of training data quality for social reasoning? (count=6)
  Representative: Do inference-time ToM gains transfer to nuanced pragmatic relevance judgments, or only to narrower benchmark-style reasoning tasks?

---

## C1: 🔴 CRITICAL — direct_contradiction

**Question**: Is recursive use of synthetic data inherently collapse-inducing, or can carefully curated synthetic data safely replace fresh human data across retraining rounds?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate use of model-generated content in training causes irreversible model collapse, with tails of the original data distribution disappearing.
  Evidence: Mixed-method paper; key claim and abstract both state that recursively generated training data causes irreversible collapse and loss of low-probability modes/tails.

**Paper B**: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe
  Claim: In self-consuming generative models, curated synthetic data can provably prevent collapse and optimize toward human preferences under iterative retraining.
  Evidence: Theoretical paper; key claim says data curation in self-consuming loops provably avoids collapse and improves preference alignment rather than degrading it.

**Relevance to thesis**: This is the sharpest counterexample to any strong thesis that synthetic data cannot substitute for fresh human data. It says the failure mode is not syntheticity alone, but uncurated recursion.
**Beat affected**: 7
**Suggested handling**: Narrow the thesis from 'synthetic data causes collapse' to 'uncurated or provenance-blind recursive synthetic data causes collapse.' Explicitly distinguish indiscriminate self-consumption from preference-aware curation regimes. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Does AI-feedback benchmark parity imply that human data is no longer needed for socially grounded alignment?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: AI feedback can match RLHF on standard alignment tasks.
  Evidence: RLAIF reports comparable performance to RLHF on summarization and dialogue, the usual evidence base for replacing costly human preference collection.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Current language models remain substantially misaligned with US demographic groups' opinions, even after demographic steering.
  Evidence: The paper finds misalignment with demographic groups' opinions on a scale comparable to the Democrat-Republican divide on climate change, and notes this persists even after steering.

**Relevance to thesis**: This is the clearest place where human data still appears valuable: benchmark-level helpfulness can be reproduced with AI feedback, but socially representative alignment still fails, implying a need for authentic, diverse human opinion data.
**Beat affected**: 7
**Suggested handling**: Explicitly separate generic alignment performance from representational legitimacy. Argue that AI feedback may be enough for narrow task rewards, while human data remains necessary to capture pluralistic social viewpoints and to audit whose values the model reflects. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — scope_disagreement

**Question**: Can AI-generated alignment data fully replace human-authored supervision, or do human post-edits still deliver measurably better dialogue quality?

**Paper A**: Zephyr: Direct Distillation of LM Alignment
  Claim: Zephyr reports that direct preference optimization distilled from AI feedback can align a 7B model without human annotation.
  Evidence: The key claim says Zephyr-7B, trained via distilled direct preference optimization from AI feedback, surpasses Llama2-Chat-70B on MT-Bench without human annotation.

**Paper B**: Fine-tuning with HED-IT: The impact of human post-editing for dialogical languag
  Claim: Human post-editing improves fine-tuning data quality beyond unedited machine-generated dialogues.
  Evidence: The key claim says fine-tuning dialog models with human post-edited data yields higher perceived quality outputs than using unedited machine-generated dialogues.

**Relevance to thesis**: This is a direct scope limiter on the strongest 'no-human-annotation' story. Zephyr shows impressive benchmarked chat alignment from AI feedback alone, but HED-IT shows that when the target metric is perceived dialogue quality, human-authored correction still matters.
**Beat affected**: 7
**Suggested handling**: State that synthetic or AI-feedback alignment can replace much of the annotation burden for benchmarked instruction following, but not necessarily the last-mile quality gains from human post-editing, especially for conversational polish or domain adaptation. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🔴 CRITICAL — scope_disagreement

**Question**: Can improved corpus construction overturn the negative lessons drawn from earlier web-corpus audits?

**Paper A**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, built from 15 trillion tokens across 96 Common Crawl snapshots, yields better-performing LLMs than other open pretraining datasets, and FineWeb-Edu substantially improves knowledge and reasoning benchmarks.
  Evidence: The paper reports superior downstream performance from a large-scale 'decanted' web dataset and an education-focused variant that especially helps reasoning-intensive tasks.

**Paper B**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: C4 includes machine-generated text, benchmark examples, and biased filtering effects, indicating that large web corpora can hide serious quality and fairness issues.
  Evidence: The audit finds unexpected content and demographic skew introduced by the cleaning pipeline itself.

**Relevance to thesis**: FineWeb directly limits overgeneralization from C4-style failures. It suggests that contamination effects are pipeline-dependent, not an inevitable property of web-scale corpora.
**Beat affected**: 7
**Suggested handling**: Use C4 as evidence that documentation and auditing are necessary, not as proof that web corpora are inherently lower quality. Present FineWeb as counterevidence showing that better construction materially changes outcomes. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Is the strongest measurable drift about declining content quality, or about shrinking legal/consent availability of web data?

**Paper A**: Consent in Crisis: The Rapid Decline of the AI Data Commons
  Claim: During 2023-2024, web data restrictions grew rapidly, making over 5% of tokens in major AI corpora like C4 nonconsented.
  Evidence: The paper presents a longitudinal restriction signal affecting the AI data commons, quantified at the token level for major web corpora.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb still produces better-performing LLMs from large-scale web snapshots.
  Evidence: The paper shows strong training utility from web data despite broad concerns about the changing web ecosystem.

**Relevance to thesis**: These papers speak to different notions of degradation. One shows access/consent decline; the other shows continued performance value. Treating them as the same phenomenon would overstate the evidence.
**Beat affected**: 2
**Suggested handling**: Split Beat 2 into separate axes: content-quality drift, contamination drift, and consent/access drift. Do not let legal degradation stand in for textual degradation. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C1: 🟡 MODERATE — scope_disagreement

**Question**: Do small amounts of carefully curated post-training data improve social reasoning itself, or mostly general alignment and chat preference?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: A 65B LLM fine-tuned on only 1,000 carefully curated examples can reach performance comparable to or preferred over GPT-4 in 43% of pairwise evaluations, without reinforcement learning.
  Evidence: The paper's key result is a strong preference win from a very small, high-quality instruction-tuning set, implying that data curation can dominate quantity for alignment-style outcomes.

**Paper B**: Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs
  Claim: GPT-3 lacks robust social intelligence and Theory of Mind out-of-the-box, struggling substantially on SocialIQa and ToMi.
  Evidence: The paper evaluates GPT-3 on SocialIQa and ToMi and concludes that strong general language performance does not translate into social reasoning competence.

**Relevance to thesis**: This is not a direct contradiction, but it sharply limits scope: curation-driven post-training gains in helpfulness or preference do not establish improved social reasoning on ToM benchmarks.
**Beat affected**: 5
**Suggested handling**: Treat LIMA-style curation as evidence for alignment sensitivity, not as evidence that social reasoning benchmarks will improve unless those benchmarks are tested directly after tuning. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Do algorithmic detection methods make web pollution broadly detectable, or only detectable for cooperatively marked outputs?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: Real web pollution can contaminate retrieval exposure and mask degradation, implying that polluted content can pass through downstream systems without obvious warning signs.
  Evidence: The paper shows over 80% exposure contamination from a 67% polluted pool and emphasizes masked quality degradation in retrieval outputs.

**Paper B**: A Watermark for Large Language Models
  Claim: LLM outputs can be made algorithmically detectable from short token spans through watermarking with negligible quality loss.
  Evidence: Key claim states that green-token watermarking is detectable from short spans and does not materially hurt text quality.

**Relevance to thesis**: This is not a direct contradiction but a real scope limiter: watermarking shows detectability is possible in principle, while Retrieval Collapse suggests today's ambient web pollution is not automatically detectable because most polluted content is not guaranteed to be watermarked.
**Beat affected**: 6
**Suggested handling**: Treat watermarking as a forward-looking provenance mechanism, not as evidence that existing web-scale pollution is already detectable. Separate 'detectable if instrumented at generation time' from 'detectable post hoc on the open web.'

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Do inference-time ToM gains transfer to nuanced pragmatic relevance judgments, or only to narrower benchmark-style reasoning tasks?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: DEL-ToM improves ToM reasoning in small language models via inference-time scaling.
  Evidence: The paper reports benchmark gains on Theory-of-Mind reasoning through a verifier-guided inference method.

**Paper B**: Relevant answers to polar questions.
  Claim: A goal-sensitive probabilistic ToM model predicts human overinformative answering patterns better than LLMs.
  Evidence: The key claim says PRIOR-PQ outperforms LLMs on nuanced human relevance judgments in polar question answering, indicating that current LLM social-pragmatic behavior still lags cognitively grounded models.

**Relevance to thesis**: This limits how far an inference-time explanation can go. Even if DEL-ToM improves benchmark ToM, the remaining gap on pragmatic relevance leaves room for authentic social data to matter for real-world grounded behavior.
**Beat affected**: 7
**Suggested handling**: Narrow claims about inference-time gains to the tasks actually tested, and add human-centered pragmatic evaluations before concluding that data quality has become less important. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C1: 🔴 CRITICAL — methodological_tension

**Question**: Are problems found in large web corpora evidence of live-web degradation, or mainly evidence that preprocessing pipelines are the dominant variable?

**Paper A**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: C4 contains significant unexpected content, including machine-generated text and benchmark examples, and its blocklist filtering disproportionately removes text from certain populations.
  Evidence: The paper documents a major webtext corpus and reports contamination plus biased filtering behavior in the resulting dataset.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Properly filtered and deduplicated web data alone can train language models that significantly outperform models trained on curated corpora like The Pile.
  Evidence: The paper explicitly argues that web data only, when filtered and deduplicated well, outperforms curated mixtures traditionally assumed necessary.

**Relevance to thesis**: This is a central challenge to any Beat-2 claim that observable corpus defects straightforwardly prove live-web degradation. It suggests corpus quality may depend more on filtering choices than on irreversible decline in the web itself.
**Beat affected**: 2
**Suggested handling**: Frame C4 as evidence that raw or poorly processed web crawls are risky, not that the web is broadly unusable. Pair any degradation claim with the concession that improved filtering can recover strong training utility. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🔴 CRITICAL — methodological_tension

**Question**: Do more complex or reasoning-rich instruction datasets help social reasoning, or can they actually worsen false-belief behavior?

**Paper A**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: LLM-rewritten instructions via Evol-Instruct create higher-complexity training data that yields a model preferred over ChatGPT on complex tasks.
  Evidence: The paper's core intervention is richer, more complex instruction data, and its reported outcome is improved performance on complex-task preference evaluations.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Instruction tuning only partially helps Theory of Mind, and reasoning-oriented fine-tuning amplifies problematic response patterns on False Belief tasks.
  Evidence: Across 17 models and 192 False Belief variants, the paper finds that certain reasoning-oriented post-training regimes make socially diagnostic errors worse, not better.

**Relevance to thesis**: This is a strong methodological warning against equating richer or more complex post-training data with better social reasoning. Complexity can improve generic task preference while degrading canonical ToM behavior.
**Beat affected**: 6
**Suggested handling**: Separate 'complex task performance' from 'social reasoning performance' and report false-belief or related ToM checks after any reasoning-focused data augmentation. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🔴 CRITICAL — methodological_tension

**Question**: Can targeted social-reasoning training reliably improve Theory of Mind, or do some post-training objectives systematically distort it?

**Paper A**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Reinforcement learning with multi-dimensional process rewards on adversarially hard social reasoning examples yields more human-like social intelligence than outcome-based RL.
  Evidence: The paper reports gains specifically from training on hard social examples with process-aware rewards, indicating that socially targeted post-training can improve behavior.

**Paper B**: Traces of Social Competence in Large Language Models
  Claim: Reasoning-oriented fine-tuning amplifies problematic response patterns on False Belief tasks.
  Evidence: The paper shows that post-training intended to enhance reasoning can worsen performance on a core social-reasoning diagnostic, even when instruction tuning helps somewhat overall.

**Relevance to thesis**: Together these papers imply that data composition matters, but not monotonically: improvements depend on the exact social examples and training objective, so 'better post-training data' is too coarse a causal story.
**Beat affected**: 6
**Suggested handling**: Narrow the claim to say that specific socially grounded curricula and reward designs can help, while generic reasoning-oriented fine-tuning may hurt. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — implicit_tension

**Question**: Can self-alignment with minimal human supervision capture broad human values, or does it risk amplifying the base model's already narrow social priors?

**Paper A**: Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Hum
  Claim: Principle-driven self-alignment can produce assistants comparable to RLHF with only minimal human supervision.
  Evidence: The key claim says LLM-generated synthetic data plus a small set of human-written principles can yield helpful, ethical, and reliable assistants comparable to RLHF-based approaches. Its stated limitation notes dependence on the quality and coverage of those principles and potential self-consistency and bias issues from synthetic generation.

**Paper B**: Whose Opinions Do Language Models Reflect?
  Claim: Current language models are substantially misaligned with real human opinion distributions.
  Evidence: The key claim says current LMs exhibit substantial misalignment with US demographic groups' opinions, on par with the Democrat-Republican divide on climate change, even after demographic steering.

**Relevance to thesis**: This is one of the strongest scope threats. Self-alignment may work for generic assistant helpfulness, but if the base model already misrepresents human opinion diversity, using it to generate its own alignment data may entrench those biases rather than reduce the need for human-authored supervision safely.
**Beat affected**: 8
**Suggested handling**: Constrain claims to generic instruction-following or assistant usefulness unless demographic representativeness is explicitly evaluated. Add that pluralistic value alignment likely still needs diverse human-authored supervision or auditing. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Can retrieval remain an effective defense against AI-generated text once the retrieval corpus itself is polluted?

**Paper A**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content can trigger Retrieval Collapse: when 67% of the retrieval pool is contaminated, exposure contamination exceeds 80%, sources become homogenized, and quality degradation is masked.
  Evidence: Key claim reports 67% pool contamination leading to over 80% exposure contamination in search/RAG results, producing a 'deceptively healthy' state.

**Paper B**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Classifier-style detectors are brittle under paraphrasing, but retrieval is an effective defense against AI-generated text.
  Evidence: The paper reports that DIPPER paraphrasing drops DetectGPT accuracy from 70.3% to 4.6% at 1% false positive rate, while retrieval-based defenses can restore robustness.

**Relevance to thesis**: This is the sharpest tension for the detectability question. One paper treats retrieval as the fallback defense when detectors fail; the other shows that at sufficient web pollution levels, retrieval itself becomes contaminated and can no longer be assumed trustworthy.
**Beat affected**: 7
**Suggested handling**: State explicitly that retrieval-based detection only works when the reference corpus is provenance-filtered or otherwise trusted. Use this tension to motivate provenance-aware collection rather than generic web retrieval as a defense.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Can AI feedback largely replace human feedback for alignment quality, or is human involvement still fundamental?

**Paper A**: RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedb
  Claim: RLAIF achieves performance comparable to RLHF across summarization and dialogue tasks, and direct-RLAIF can outperform canonical RLAIF by taking rewards directly from an LLM.
  Evidence: The paper's key claim states comparable performance to RLHF on summarization and dialogue, with direct-RLAIF improving further via LLM-provided rewards.

**Paper B**: Human-in-the-Loop Reinforcement Learning: A Survey and Position on Requirements,
  Claim: Reinforcement learning is fundamentally a human-in-the-loop paradigm, and human-centric design is key to successful RL.
  Evidence: The survey's key claim explicitly frames RL as fundamentally human-in-the-loop and argues that human-centric design has been insufficiently addressed.

**Relevance to thesis**: This is a direct threat to any strong claim that authentic human feedback is generally necessary post-training: RLAIF presents a real alternative mechanism where model-mediated feedback recovers much of the observed alignment gain.
**Beat affected**: 7
**Suggested handling**: Narrow the thesis: concede that AI feedback can substitute for human labels on task-level helpfulness benchmarks, but argue that human data remains most valuable where goals are socially grounded, contested, or require accountable provenance. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C3: 🔴 CRITICAL — competing_mechanism

**Question**: Does successful pretraining on filtered web corpora neutralize the risk that AI-polluted web ecosystems still degrade system quality?

**Paper A**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: A carefully filtered and very large web corpus can improve model performance relative to other open pretraining datasets.
  Evidence: FineWeb reports better-performing LLMs overall, with FineWeb-Edu especially improving knowledge- and reasoning-intensive benchmarks.

**Paper B**: Retrieval Collapses When AI Pollutes the Web
  Claim: AI-generated web content causes retrieval collapse: 67% pool contamination yields over 80% exposure contamination, homogenizing sources while masking degradation.
  Evidence: The paper shows that contamination is amplified by retrieval dynamics, so users and RAG systems can see heavily polluted evidence even when the underlying pool appears only moderately contaminated.

**Relevance to thesis**: This introduces a real alternative mechanism. Even if filtered web corpora work well for pretraining, quality decline can still emerge later from retrieval-time exposure amplification rather than from training-data degradation alone.
**Beat affected**: 7
**Suggested handling**: Separate two claims: filtered static corpora can still support strong pretraining, while live retrieval over an AI-polluted web can independently degrade grounded outputs. Do not treat them as the same phenomenon. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🔴 CRITICAL — competing_mechanism

**Question**: Is better social reasoning caused mainly by post-training data composition, or by mechanisms that unlock Theory-of-Mind knowledge already latent in the model?

**Paper A**: LIMA: Less Is More for Alignment
  Claim: Carefully curated post-training data is a powerful lever: only 1,000 examples can produce large alignment gains.
  Evidence: LIMA attributes large usability gains to a small, carefully composed fine-tuning set, emphasizing training-data curation rather than additional RL or larger datasets.

**Paper B**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: LLMs already possess internal Theory-of-Mind knowledge but fail to externalize it reliably; causal steering can align internal cognition with stable external ToM behavior.
  Evidence: The paper argues the bottleneck is not missing social knowledge in training data, but unstable expression of latent ToM knowledge, and shows steering can improve external behavior without retraining data composition being the main lever.

**Relevance to thesis**: This is a genuine competing mechanism. If social reasoning is already latent and the main problem is externalization, then post-training data composition may be less causally central than steering or control-time interventions.
**Beat affected**: 7
**Suggested handling**: Present data composition as one candidate mechanism alongside latent-knowledge steering, and compare the two on matched social benchmarks before making strong causal claims. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C1: 🔴 CRITICAL — competing_mechanism

**Question**: Are social-reasoning gains mainly recoverable at inference time, rather than requiring stronger or more authentic training data?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: DEL-ToM improves Theory-of-Mind reasoning in small language models through inference-time scaling using a Dynamic Epistemic Logic-grounded verifier rather than architectural changes.
  Evidence: The key claim explicitly attributes ToM gains to inference-time scaling with a verifier; the abstract frames ToM as difficult for small models but proposes a test-time reasoning scaffold instead of changing training data or architecture.

**Paper B**: The Pragmatic Mind of Machines: Tracing the Emergence of Pragmatic Competence in
  Claim: Pre-training, SFT, and preference optimization stages differentially affect pragmatic competence across 22 models.
  Evidence: The ALTPRAG benchmark paper argues that pragmatic, social-adjacent competence depends on which training stage shaped the model, implying that learning history materially changes social behavior rather than merely being elicited at inference.

**Relevance to thesis**: This is a direct alternative explanation to any thesis claiming post-training data authenticity is the main cause of better socially grounded behavior: DEL-ToM says a strong part of the gain may come from verifier-guided inference instead.
**Beat affected**: 7
**Suggested handling**: Bound the thesis: claim authentic post-training data matters even after controlling for inference-time scaling. Add factorial experiments comparing the same base model under authentic-data post-training, DEL-ToM-style inference-time scaling, and both combined on identical social benchmarks. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C2: 🔴 CRITICAL — competing_mechanism

**Question**: Is weak social reasoning primarily a data problem, or an externalization/control problem in models that already contain latent ToM knowledge?

**Paper A**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: LLMs possess internal ToM knowledge but fail to externalize it reliably; causal-oriented steering can align internal cognition with stable external ToM behavior.
  Evidence: The abstract explicitly says the problem is not missing ToM knowledge per se but failure to express it consistently, and proposes causal steering as the fix.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Reinforcement learning with multi-dimensional process rewards on adversarially hard social reasoning examples yields more human-like social intelligence than outcome-based RL.
  Evidence: The key claim attributes better social intelligence to training on hard social examples with process-level rewards, i.e. improved learning signals rather than inference-only control.

**Relevance to thesis**: If CoSToM is right, then authentic post-training data may not be the main bottleneck; social competence may already exist internally and only need better elicitation. That directly pressures a data-centric thesis.
**Beat affected**: 7
**Suggested handling**: Separate acquisition from expression. Test whether provenance-rich post-training data increases latent ToM knowledge, externalization reliability, or both; include causal-steering baselines and probe-before/probe-after analyses. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C3: 🔴 CRITICAL — competing_mechanism

**Question**: Can inference-time epistemic verification substitute for high-quality curated data in producing reasoning gains relevant to social tasks?

**Paper A**: DEL-ToM: Inference-Time Scaling for Theory-of-Mind Reasoning via Dynamic Epistem
  Claim: DEL-ToM improves Theory-of-Mind reasoning through inference-time scaling with a Dynamic Epistemic Logic verifier.
  Evidence: The paper's stated mechanism is test-time verification and search, not better training data.

**Paper B**: CCI4.0: A Bilingual Pretraining Dataset for Enhancing Reasoning in Large Languag
  Claim: A carefully filtered 35TB bilingual pretraining dataset with deduplication, quality scoring, and fluency filtering enhances LLM reasoning.
  Evidence: The abstract emphasizes 'superior data quality' and 'diverse human-like reasoning trajectory' as the reason the dataset improves reasoning, making data quality the central mechanism.

**Relevance to thesis**: This is the core mechanism clash: one paper says reasoning gains can come from better inference scaffolding, the other says they come from better data curation. For the thesis, that means observed social gains could be over-attributed to data authenticity unless test-time methods are ruled out.
**Beat affected**: 7
**Suggested handling**: Run matched-model comparisons where only data provenance/quality changes, then add and remove verifier-guided inference. Report whether authentic-data gains persist under standardized decoding and scaling budgets. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Are current AI-text detection methods broadly reliable, or are strong reported accuracies mostly benchmark- and setup-specific?

**Paper A**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: No single current detection approach is universally reliable because detectability varies with generation method, domain, and detector type.
  Evidence: The survey's key claim explicitly says detectability depends on a combination of factors and that no single approach is universally reliable.

**Paper B**: Distinguishing Reality from AI: Approaches for Detecting Synthetic Content
  Claim: Hybrid multimodal detection approaches can achieve up to 92% accuracy, outperforming single-modality methods.
  Evidence: Key claim reports up to 92% accuracy for hybrid approaches in identifying synthetic content.

**Relevance to thesis**: This tension limits any broad claim that web pollution is 'detectable' simpliciter. High benchmark accuracy does not resolve the survey's broader conclusion that reliability depends heavily on domain and attack conditions.
**Beat affected**: 6
**Suggested handling**: Report detector results as conditional and benchmark-specific. Avoid converting strong closed-set accuracy into a claim of robust open-web pollution detectability.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Does scalable detection in controlled educational settings transfer to the open-web pollution problem?

**Paper A**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Current detectability varies substantially across domains and methods, so general claims of reliable detection are unwarranted.
  Evidence: The survey states that generation method, domain, and detector choice jointly determine detectability.

**Paper B**: AI See What You Did There – The Prevalence of LLM-Generated Answers in MOOC Resp
  Claim: AI-generated content is highly prevalent in MOOC responses and can be identified at scale using textual analysis metrics.
  Evidence: Key claim reports both high prevalence in MOOC student responses and successful identification through scalable textual analysis.

**Relevance to thesis**: The MOOC result is important but only partial evidence. It supports detectability in a narrow, stylized genre with institutional context, not necessarily in the broader and messier web-pollution setting.
**Beat affected**: 5
**Suggested handling**: Cite this as evidence for constrained-domain detectability, while reserving stronger claims about the open web unless supported by provenance-aware or real-world web measurements.

---

## C3: 🟡 MODERATE — scope_disagreement

**Question**: Can simulated human feedback replace large-scale crowd-sourced human annotation in open alignment pipelines?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: LLM-simulated human feedback is about 50x cheaper than crowdworkers while maintaining high agreement with actual human preferences.
  Evidence: The key claim states simulated feedback preserves high agreement with real human preferences at far lower cost, positioning human collection as economically avoidable in many experiments.

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: A large-scale crowd-sourced, human-annotated conversation corpus enables open and democratized research on LLM alignment.
  Evidence: The key claim centers the value of a human-annotated conversation corpus as an enabling asset for alignment research and democratization.

**Relevance to thesis**: These papers disagree on whether human data is the scarce ingredient or mainly a seed/benchmarking resource. AlpacaFarm treats human feedback as simulable; OpenAssistant treats authentic human annotation as the enabling substrate.
**Beat affected**: 6
**Suggested handling**: Present human data as an anchor rather than the only scalable training source: use human corpora for seeding, calibration, and auditing, while allowing simulated feedback for cheap iteration once the target distribution has been human-defined. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — scope_disagreement

**Question**: Does AI-simulated feedback generalize to safety-critical alignment, or are dedicated human preference labels still needed for harmlessness?

**Paper A**: AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
  Claim: Simulated feedback from an LLM is a viable, low-cost substitute for human feedback.
  Evidence: The key claim says LLM-simulated human feedback is 50x cheaper than crowdworkers while maintaining high agreement with actual human preferences.

**Paper B**: BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dat
  Claim: Safety alignment benefits from large, explicitly human-annotated datasets that disentangle helpfulness and harmlessness.
  Evidence: The key claim says BeaverTails provides 333,963 QA pairs with separately annotated helpfulness and harmlessness labels, enabling improved safety alignment of LLMs.

**Relevance to thesis**: AlpacaFarm supports strong reduction in human supervision for preference learning, but BeaverTails suggests that safety is a special case where fine-grained human labels may still be necessary because generic preference agreement is not the same as calibrated harmlessness supervision.
**Beat affected**: 7
**Suggested handling**: Claim that AI feedback is promising for rapid iteration and broad preference modeling, but qualify that safety-critical alignment may still require dedicated human annotation and domain-specific evaluation. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — scope_disagreement

**Question**: Does the rise of low-quality AI-written content in a major source like Wikipedia imply that web-derived corpora will generally decline in quality?

**Paper A**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Web data alone, when properly filtered and deduplicated, can outperform curated corpora for pretraining.
  Evidence: RefinedWeb argues that web-only training data can exceed the performance of curated alternatives such as The Pile.

**Paper B**: The Rise of AI-Generated Content in Wikipedia
  Claim: More than 5% of newly created English Wikipedia articles are flagged as AI-generated, and those articles are typically lower quality and often biased or self-promotional.
  Evidence: The paper documents measurable source-level degradation in a prominent web knowledge resource.

**Relevance to thesis**: Wikipedia contamination supports a decline story for at least one important source, but RefinedWeb shows that source-specific deterioration does not automatically translate into a universal decline for all filtered web corpora.
**Beat affected**: 7
**Suggested handling**: State that contamination is heterogeneous across sources. Use Wikipedia as evidence for targeted exclusions or downweighting, not as proof that all web-derived corpora are worsening in the same way. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C2: 🟡 MODERATE — scope_disagreement

**Question**: Does prioritizing instruction-tuning data quality improve socially grounded reasoning, or mainly broad instruction-following performance?

**Paper A**: From Quantity to Quality: Boosting LLM Performance with Self-Guided Data Selecti
  Claim: Self-guided data selection boosts LLM performance by prioritizing data quality over quantity for instruction tuning.
  Evidence: The paper explicitly manipulates training-set composition through self-guided selection and reports overall performance gains from higher-quality subsets.

**Paper B**: Relevant answers to polar questions.
  Claim: A goal-sensitive probabilistic Theory-of-Mind model predicts human overinformative answering patterns better than LLMs.
  Evidence: On polar-question relevance judgments, PRIOR-PQ outperforms LLMs on nuanced human pragmatics, showing that current LLMs still miss important social-pragmatic structure.

**Relevance to thesis**: This tension suggests that 'better data' can raise aggregate instruction-tuning performance while leaving key social-pragmatic reasoning deficits intact.
**Beat affected**: 5
**Suggested handling**: Require social-pragmatic evaluation, not just aggregate instruction benchmarks, when arguing that quality-based data selection improves social reasoning. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Do large-scale high-quality synthetic conversations close social-pragmatic reasoning gaps, or mainly improve chat performance?

**Paper A**: Enhancing Chat Language Models by Scaling High-quality Instructional Conversatio
  Claim: Scaling diverse, high-quality synthetic instructional conversations substantially improves open-source chat language model performance.
  Evidence: UltraChat's central result is that synthetic conversation scale and diversity produce better chat models, even without human queries.

**Paper B**: Relevant answers to polar questions.
  Claim: A probabilistic ToM model still predicts human relevance judgments in polar-question answering better than LLMs.
  Evidence: Despite progress in chat-oriented LLM training, the paper finds LLMs remain worse than a goal-sensitive ToM model on subtle relevance and overinformativeness judgments.

**Relevance to thesis**: This limits how far synthetic conversational data can be taken as evidence for social reasoning improvement: chat gains do not automatically imply human-like pragmatic inference.
**Beat affected**: 5
**Suggested handling**: Use social-pragmatic benchmarks as a separate evaluation axis for synthetic-conversation tuning, rather than inferring social gains from chat benchmark improvements. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — scope_disagreement

**Question**: Do elicitation and steering methods yield robust social reasoning, or do they risk overstating competence when evaluation broadens to false-belief and cross-cultural settings?

**Paper A**: CoSToM:Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment in Large 
  Claim: Causal-oriented steering can align internal cognition with stable external ToM behavior.
  Evidence: CoSToM's core claim is that reliable external ToM behavior can be produced by steering models that already contain latent ToM knowledge.

**Paper B**: Are Vision Language Models Cross-Cultural Theory of Mind Reasoners?
  Claim: Frontier VLMs achieve high overall ToM accuracy but still fail on false-belief reasoning and show systematic cultural bias.
  Evidence: The benchmark reports >93% overall ToM accuracy yet only 19-83% on false-belief probes, plus 20-30% regional gaps and social desirability bias, showing that high headline ToM scores can mask major social-reasoning failures.

**Relevance to thesis**: This is an honest scope limiter: even if steering or inference-time methods improve outward ToM behavior, those gains may not generalize to robust socially grounded competence. That preserves space for a data-authenticity account, but only if the thesis is framed around ecologically valid outcomes.
**Beat affected**: 7
**Suggested handling**: Use broader evaluations including false-belief, cultural transfer, and bias-sensitive tasks. Avoid treating improved benchmark ToM from steering as equivalent to robust socially grounded reasoning. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C2: 🟡 MODERATE — methodological_tension

**Question**: Do anti-collapse results for synthetic retraining depend on idealized correction mechanisms that may not exist in practice?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Recursive training on generated data leads to irreversible collapse in realistic mixed settings.
  Evidence: Mixed empirical/theoretical framing emphasizes actual degradation under recursive reuse of generated data, not just a pathological toy setup.

**Paper B**: Self-Correcting Self-Consuming Loops for Generative Model Training
  Claim: Self-consuming loops become exponentially more stable if an idealized correction function is introduced.
  Evidence: Mixed paper; abstract explicitly says stability comes from an 'idealized correction function,' making the rescue mechanism assumption-heavy.

**Relevance to thesis**: This does not kill the collapse argument, but it limits its scope: collapse may be avoidable if a sufficiently strong correction channel exists. The catch is that the correction channel may be unrealistic.
**Beat affected**: 5
**Suggested handling**: Treat this as a scope limiter, not a refutation. Note that the positive result relies on an idealized corrector, so the empirical burden shifts to whether such correction can be approximated in deployed systems. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Is robust detection mainly a post-hoc classification problem, or does it require generation-time provenance mechanisms?

**Paper A**: Paraphrasing evades detectors of AI-generated text, but retrieval is an effectiv
  Claim: Post-hoc AI-text detectors can be made nearly useless by paraphrasing.
  Evidence: DIPPER paraphrasing reduces DetectGPT detection accuracy from 70.3% to 4.6% at 1% false positive rate.

**Paper B**: Adaptive Text Watermark for Large Language Models
  Claim: Adaptive watermarking improves the quality, security, and robustness of watermark-based detection by watermarking only high-entropy tokens and using semantic scaling.
  Evidence: Key claim says adaptive watermarking improves robustness relative to prior watermark methods.

**Relevance to thesis**: This is a central methodological split: one line says post-hoc stylistic detection is brittle, while the other says robustness comes from instrumenting generation itself. That distinction matters for whether 'web pollution detection' is feasible in practice.
**Beat affected**: 7
**Suggested handling**: Separate classifier-style detection from provenance/watermark defenses in the thesis. Do not present watermark robustness as evidence that unwatermarked web pollution is generally detectable.

---

## C3: 🟡 MODERATE — methodological_tension

**Question**: Can metric declines in diversity be trusted as evidence of degradation without robust controls for corpus size and content variation?

**Paper A**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Recursively training language models on synthetic text leads to a consistent decline in lexical, syntactic, and semantic diversity, especially for creative tasks.
  Evidence: The paper's core evidence for degradation is metric-based decline in multiple diversity dimensions under recursive synthetic training.

**Paper B**: Towards robust complexity indices in linguistic typology
  Claim: Traditional corpus-based complexity indices such as TTR and word-level entropy are less robust to corpus size and content variation than newer indices across 47 languages.
  Evidence: The study directly warns that common corpus metrics can shift for methodological reasons, not only because underlying language quality changed.

**Relevance to thesis**: This does not refute degradation effects, but it limits how confidently metric changes alone can support a live-web drift claim. Beat 2 needs robust measurement, not just observed metric movement.
**Beat affected**: 2
**Suggested handling**: Require matched-size temporal samples, multiple diversity measures, and robustness checks before treating metric decline as evidence of real web degradation. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Is preference optimization the essential route to alignment, or can a very small curated human instruction set do most of the work?

**Paper A**: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
  Claim: RLHF can be reformulated as a simple classification loss, enabling direct preference optimization without reinforcement learning.
  Evidence: The paper's key claim is that direct policy optimization follows from reparameterizing the reward model, shifting emphasis from elaborate RL pipelines to the optimization objective over preference data.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: Fine-tuning a 65B LLM on only 1,000 carefully curated examples, without reinforcement learning, reaches performance comparable to or preferred over GPT-4 in 43% of cases.
  Evidence: LIMA explicitly argues that a tiny, high-quality curated set can produce strong alignment behavior without RL.

**Relevance to thesis**: This tension matters for curation vs RLHF: if LIMA is right, carefully curated human demonstrations may remain highly valuable even when preference optimization methods like DPO work well; if DPO is right, the bottleneck may be objective design over preference data rather than authenticity or amount of human curation.
**Beat affected**: 6
**Suggested handling**: Acknowledge that preference-optimization success is real counterevidence. Then argue the open question is not 'RLHF or not' but which parts of alignment require authentic human curation versus which can be delegated to better objectives on cheaper feedback. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C5: 🟡 MODERATE — methodological_tension

**Question**: Does ranking-based preference optimization reduce the need for curated human instruction data, or do small curated sets still have unique value?

**Paper A**: RRHF: Rank Responses to Align Language Models with Human Feedback without tears
  Claim: RRHF aligns language models with human preferences using a ranking loss on conditional probabilities while avoiding PPO complexity.
  Evidence: The key claim says RRHF can align to human preferences with a simpler ranking objective and only 1-2 models, implying much of the gain may come from the learning setup rather than from large bespoke curation.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: A small, carefully curated set of 1,000 human examples can yield strong alignment without reinforcement learning.
  Evidence: LIMA reports strong performance from limited but high-quality curated human data, explicitly minimizing the need for RL-style preference optimization.

**Relevance to thesis**: This is a genuine curation-vs-RLHF tension: RRHF suggests better use of preference comparisons can cheaply recover alignment, while LIMA suggests authentic curation itself may be the higher-value ingredient.
**Beat affected**: 6
**Suggested handling**: Frame this as a division of labor: curated human data may define the target behavior efficiently, while ranking/preference methods may refine it. Do not claim human curation is always superior; claim instead that it may be disproportionately valuable per example. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — methodological_tension

**Question**: Do quality filters and deduplication reliably solve web-corpus contamination, or can cleaning pipelines themselves introduce distortions?

**Paper A**: Yi: Open Foundation Models by 01.AI
  Claim: Yi's strong performance is primarily attributed to data quality achieved through a cascaded deduplication and quality filtering pipeline over 3.1 trillion tokens.
  Evidence: The system paper explicitly credits model strength to the quality effects of large-scale deduplication and filtering.

**Paper B**: Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Co
  Claim: C4's cleaning pipeline leaves machine-generated and benchmark-like content in place while disproportionately filtering out language from some populations.
  Evidence: The audit identifies both residual contamination and harmful side effects from blocklist-based cleaning.

**Relevance to thesis**: This tension matters because it shows 'filtering' is not a unitary solution. Some pipelines improve performance; others create bias or fail to remove problematic content. That weakens any simple contamination narrative in either direction.
**Beat affected**: 6
**Suggested handling**: Distinguish crude blocklist cleaning from more sophisticated cascaded filtering and deduplication, and require audits of both benchmark leakage and representational effects. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — implicit_tension

**Question**: Is explicit verification of human versus AI origin necessary to manage collapse, or can collapse be detected and mitigated from model statistics alone?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: The core risk is specifically recursive contamination by model-generated content replacing human data.
  Evidence: The collapse framing is origin-sensitive: the problem is defined as retraining on model-generated rather than human-generated data.

**Paper B**: Learning by Surprise: Surplexity for Mitigating Model Collapse in Generative AI
  Claim: Model collapse can be characterized from next-token probability distributions without knowing whether the data is human- or AI-generated.
  Evidence: Empirical paper; key claim and abstract explicitly reject the need for provenance labels to characterize collapse, proposing surplexity as an origin-agnostic signal.

**Relevance to thesis**: This is a real tension for any provenance-heavy account. If collapse can be monitored without source labels, verified synthetic provenance may be less necessary for detection than the thesis implies.
**Beat affected**: 5
**Suggested handling**: Differentiate governance from diagnostics. Provenance may still matter for accountability, preference preservation, and auditing even if collapse detection can be origin-agnostic. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🟡 MODERATE — implicit_tension

**Question**: Does long-run web compositional drift toward social and streaming content necessarily reduce the value of the web for text pretraining?

**Paper A**: "Way back then": A Data-driven View of 25+ years of Web Evolution
  Claim: Over 25+ years of web evolution, streaming media and social networking sites replaced news and education websites in popularity.
  Evidence: The paper provides direct temporal evidence that the web's composition changed substantially away from traditionally text-rich, informational domains.

**Paper B**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Filtered and deduplicated web data alone can significantly outperform curated corpora for language-model training.
  Evidence: Even without relying on hand-curated non-web sources, the extracted web text remains strong enough to beat standard curated baselines.

**Relevance to thesis**: The web clearly drifts over time, but compositional drift is not the same as measurable degradation in extractable training text. This is an honest scope limiter on Beat 2.
**Beat affected**: 2
**Suggested handling**: Distinguish between macro-level platform/popularity shifts and the narrower claim that usable text quality for pretraining has degraded. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C6: 🟡 MODERATE — implicit_tension

**Question**: Is human feedback intrinsically valuable for alignment, or can it systematically encode undesirable preferences such as sycophancy?

**Paper A**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: Large-scale human-annotated conversation data is an enabling resource for alignment.
  Evidence: OpenAssistant's contribution is precisely to build a crowd-sourced human corpus for alignment research.

**Paper B**: AI Supported Degradation of the Self Concept: A Theoretical Framework Grounded i
  Claim: Models finetuned with human feedback exhibit sycophancy because humans and preference models often prefer convincingly written sycophantic responses over correct ones.
  Evidence: The paper states that human feedback can reward agreement with user beliefs rather than truth, identifying a systematic failure mode inside human-preference-based training.

**Relevance to thesis**: This does not show human data is useless, but it sharply limits any simple 'more human feedback is better' thesis. Human data remains valuable only if the collection protocol targets truthfulness, diversity, and anti-sycophancy rather than raw preference satisfaction.
**Beat affected**: 7
**Suggested handling**: Distinguish authentic human data from uncritical human preference aggregation. Argue that provenance-aware human data should be collected with stronger annotation goals and evaluation against truthfulness and sycophancy, not just preference win rates. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — implicit_tension

**Question**: If filtered web corpora improve benchmark performance, are they therefore 'high quality' in the broader provenance and governance sense?

**Paper A**: The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Da
  Claim: Filtered, deduplicated web data can be high-quality enough to outperform curated corpora in model training.
  Evidence: RefinedWeb presents strong benchmark-based evidence that careful web-data processing yields superior training value.

**Paper B**: Consent in Crisis: The Rapid Decline of the AI Data Commons
  Claim: Major AI corpora including RefinedWeb and C4 contain growing amounts of nonconsented data; over 5% of tokens become nonconsented under observed 2023-2024 changes.
  Evidence: The paper audits consent dynamics and finds that standard corpus assembly practices fail to maintain robust consent provenance over time.

**Relevance to thesis**: This is an honest scope limiter: even when contamination does not visibly cause benchmark decline, corpus documentation can reveal serious provenance failures. So 'quality' cannot be reduced to downstream performance alone.
**Beat affected**: 6
**Suggested handling**: Split the argument into performance quality versus provenance quality. Acknowledge that filtered-web success complicates a contamination-decline story, while documentation papers show unresolved consent and governance deficits. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C3: 🟡 MODERATE — competing_mechanism

**Question**: Can synthetic data substitute for fresh human data if it is used as a negative-guidance signal rather than naively imitated?

**Paper A**: The Curse of Recursion: Training on Generated Data Makes Models Forget
  Claim: Training generative models on model-generated content causes irreversible model collapse and forgetting of the tails of the original distribution.
  Evidence: Mixed paper; key claim and abstract frame recursive training on generated data as producing irreversible forgetting and tail loss.

**Paper B**: Self-Improving Diffusion Models with Synthetic Data
  Claim: Synthetic data can help rather than harm when treated as negative guidance during diffusion generation, preventing autophagy disorder while preserving quality and diversity.
  Evidence: Empirical paper; key claim states that using synthetic data as negative guidance prevents collapse-like degradation and maintains diversity in diffusion models.

**Relevance to thesis**: This introduces a real competing mechanism: the effect of synthetic data depends on how it enters training. Synthetic data may be harmful as imitation targets but useful as contrastive or negative signals.
**Beat affected**: 7
**Suggested handling**: Separate 'synthetic-as-target' from 'synthetic-as-guidance.' Emphasize that collapse results do not automatically generalize to training schemes that use synthetic outputs adversarially or contrastively. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C4: 🟡 MODERATE — competing_mechanism

**Question**: Can even unverified synthetic self-training improve models if the update rule explicitly extrapolates away from synthetic-data degradation?

**Paper A**: AI models collapse when trained on recursively generated data
  Claim: Indiscriminate recursive training on model-generated data irreversibly degrades the learned distribution.
  Evidence: The paper's central evidence is that recursive reuse of generated data causes collapse, especially by erasing rare modes.

**Paper B**: Neon: Negative Extrapolation From Self-Training Improves Image Generation
  Claim: Negative extrapolation from self-training on synthetic data improves image generation quality by moving weights away from degraded self-training directions.
  Evidence: Mixed paper; abstract and key claim explicitly state that reversing gradient updates from synthetic self-training can improve, not degrade, image generation quality.

**Relevance to thesis**: This is a strong counterexample to any blanket claim that unverified synthetic data is always net harmful. It suggests the optimization rule can dominate the provenance effect.
**Beat affected**: 7
**Suggested handling**: Acknowledge that provenance is not the only causal lever; update geometry matters. Position authenticity as one important factor whose impact can be amplified or attenuated by training design. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---

## C2: 🟡 MODERATE — competing_mechanism

**Question**: Does measurable AI-content growth on a major live site imply broad web degradation, or can large-scale filtering and dataset construction offset it?

**Paper A**: The Rise of AI-Generated Content in Wikipedia
  Claim: Over 5% of newly created English Wikipedia articles are flagged as AI-generated, and these articles are typically of lower quality and often self-promotional or biased.
  Evidence: The study provides a concrete temporal signal on a live, high-visibility web source: increasing AI-generated content with measurable quality defects.

**Paper B**: The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale
  Claim: FineWeb, built from 96 Common Crawl snapshots and 15 trillion tokens, yields better-performing LLMs than other open pretraining datasets, with FineWeb-Edu further improving knowledge and reasoning benchmarks.
  Evidence: Despite drawing from broad web snapshots, the dataset improves downstream benchmark performance rather than showing degraded utility.

**Relevance to thesis**: Wikipedia gives real evidence of localized degradation, but FineWeb is a strong competing mechanism: the broader web may still be highly usable if filtered and aggregated well enough.
**Beat affected**: 2
**Suggested handling**: Use Wikipedia as domain-specific evidence of contamination growth. Avoid generalizing from it to a claim that overall web training value is already collapsing. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C5: 🟡 MODERATE — competing_mechanism

**Question**: Are alignment gains mainly coming from large-scale synthetic instruction generation, or from model scale plus a very small amount of carefully curated human supervision?

**Paper A**: WizardLM: Empowering large pre-trained language models to follow complex instruc
  Claim: Synthetic instruction rewriting at scale is a major driver of instruction-following improvement.
  Evidence: The key claim says WizardLM uses LLM-rewritten instructions via Evol-Instruct to create higher-complexity data and trains a model preferred over ChatGPT on complex tasks.

**Paper B**: LIMA: Less Is More for Alignment
  Claim: A tiny, high-quality human dataset may be enough when the base model is strong.
  Evidence: The key claim says LIMA fine-tunes a 65B model on only 1,000 carefully curated examples, without reinforcement learning, and achieves performance comparable to or preferred to GPT-4 in 43% of cases.

**Relevance to thesis**: This is a real alternative mechanism. WizardLM attributes success to synthetic data generation, while LIMA suggests that strong pretraining/model scale plus a tiny curated human set may explain much of the observed alignment gain. That weakens any claim that synthetic data is the uniquely important substitute for human supervision.
**Beat affected**: 6
**Suggested handling**: Present synthetic data as one viable route, not the sole explanation. Note that model scale and pretrained capability are competing mechanisms, and call for controlled same-base-model ablations comparing synthetic scale against small curated human sets. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C6: 🟡 MODERATE — competing_mechanism

**Question**: For open alignment, is the key enabler self-generated instruction data or large-scale crowd-sourced human conversations?

**Paper A**: Self-Instruct: Aligning Language Models with Self-Generated Instructions
  Claim: Instruction-following alignment can be bootstrapped from self-generated instruction data, reducing reliance on human annotations.
  Evidence: The key claim says language models can be aligned using self-generated instruction data, explicitly reducing reliance on costly human annotations.

**Paper B**: OpenAssistant Conversations -- Democratizing Large Language Model Alignment
  Claim: Open alignment research depends on access to a large human-annotated conversation corpus.
  Evidence: The key claim says a large-scale crowd-sourced, human-annotated conversation corpus enables open and democratized research on LLM alignment.

**Relevance to thesis**: These papers offer different answers to the same bottleneck. Self-Instruct says the bottleneck can be relaxed by synthetic bootstrapping; OpenAssistant treats broad human-authored conversational data as the enabling resource for open alignment. That is not a pure contradiction, but it is a meaningful competing story about what remains indispensable.
**Beat affected**: 5
**Suggested handling**: Frame this as a division of labor: synthetic instruction generation can bootstrap breadth cheaply, while human conversational corpora remain valuable for realism, diversity, and community-auditable alignment data. State explicitly that the corpus does not directly show AI-feedback or self-alignment failing on social-reasoning tasks; that domain restriction remains a hypothesis, not an established result.

---

## C4: 🟡 MODERATE — competing_mechanism

**Question**: Do chain-of-thought and test-time sampling reduce the apparent importance of training data quality for social reasoning?

**Paper A**: Self-Consistency Improves Chain of Thought Reasoning in Language Models
  Claim: Self-consistency decoding substantially boosts chain-of-thought performance by marginalizing over diverse sampled reasoning paths.
  Evidence: The key claim says reasoning performance improves via a decoding strategy alone on arithmetic and commonsense benchmarks, showing that large gains can come from inference-time path selection without retraining.

**Paper B**: Social-R1: Towards Human-like Social Reasoning in LLMs
  Claim: Human-like social reasoning improves when models are trained with multi-dimensional process rewards on adversarially hard social examples.
  Evidence: Social-R1 attributes gains to training-time social-process supervision on hard examples, implying that better learning signals, not just better decoding, are necessary for human-like social behavior.

**Relevance to thesis**: This does not directly refute a data-authenticity thesis, but it creates a serious competing explanation: some measured gains on social-adjacent tasks could be due to smarter inference rather than better data.
**Beat affected**: 7
**Suggested handling**: Acknowledge task mismatch and test self-consistency or extended-thinking baselines on the same social benchmarks used to support the data-authenticity thesis. If data still matters after strong inference-time baselines, the thesis is stronger. Treat inference-time scaling as a genuine competing mechanism and scope L_auth to fixed-compute data-composition effects unless direct evidence says otherwise.

---

## C5: 🟢 MINOR — scope_disagreement

**Question**: Do successful domain-specific detectors imply that open-web AI pollution is generally detectable?

**Paper A**: Detecting AI-Generated Text: Factors Influencing Detectability with Current Meth
  Claim: Detectability is contingent on generator, domain, and method; no universal detector exists.
  Evidence: The survey synthesizes current methods and concludes that reliability varies by generation method, domain, and detection technique.

**Paper B**: Phishing Detection 2.0: A Natural Language Processing Approach to Identifying Ge
  Claim: An NLP-based approach can distinguish AI-generated phishing messages from legitimate emails and human-written phishing attempts.
  Evidence: Key claim reports successful discrimination of AI-crafted phishing against both legitimate and human-phishing baselines.

**Relevance to thesis**: This is a scope-limiting tension rather than a rebuttal. Success on phishing email shows some polluted niches are detectable, but it does not establish that heterogeneous web pollution is detectable at scale.
**Beat affected**: 5
**Suggested handling**: Use niche detection papers as positive but bounded evidence. Explicitly note that success in a constrained threat domain does not settle the open-web question.

---

## C6: 🟢 MINOR — scope_disagreement

**Question**: Do longitudinal changes in a narrow live-web genre support a broad degradation thesis, or mainly show domain-specific evolution that metric-only decline studies cannot generalize from?

**Paper A**: Privacy Policies across the Ages: Content of Privacy Policies 1996–2021
  Claim: Privacy policies changed measurably from 1996 to 2021 in response to regulations such as GDPR and CCPA, though gaps remain in user rights.
  Evidence: This is direct temporal measurement on a live-web document class, showing structured change over 25 years rather than a simple monotonic decline.

**Paper B**: The Curious Decline of Linguistic Diversity: Training Language Models on Synthet
  Claim: Synthetic recursive training causes a consistent decline in linguistic diversity.
  Evidence: The decline is measured in a synthetic-data recursion setting, not in a broad longitudinal sample of the live web.

**Relevance to thesis**: This is a scope warning: the clearest live-web temporal evidence here is genre-specific and not uniformly degradational, while the strongest 'decline' paper is not actually measuring the live web.
**Beat affected**: 2
**Suggested handling**: Use the privacy-policy work as proof that temporal measurement is feasible, but concede that it does not establish general web degradation. Treat synthetic-recursion decline as an analogy or risk model, not direct Beat-2 evidence. State explicitly that the corpus still lacks a direct post-2022 web-scale contamination audit; this supports a rising-risk claim, not demonstrated general failure.

---

## C6: 🟢 MINOR — methodological_tension

**Question**: Is provenance metadata indispensable for safer data substitution, or are distributional quality signals enough?

**Paper A**: RedPajama: an Open Dataset for Training Large Language Models
  Claim: Large-scale datasets should expose quality signals and metadata to improve transparency and reproducibility in LLM training.
  Evidence: Benchmark paper; key claim emphasizes metadata and quality annotations as useful infrastructure for understanding and controlling training data composition.

**Paper B**: Learning by Surprise: Surplexity for Mitigating Model Collapse in Generative AI
  Claim: Collapse can be characterized without knowing whether examples are human- or AI-generated.
  Evidence: The surplexity paper explicitly states that its characterization does not require source-origin knowledge, pushing against provenance-dependent monitoring.

**Relevance to thesis**: This does not resolve whether synthetic data can replace human data, but it matters for the 'verified synthetic' part of the focus question: verification may be valuable, yet not strictly necessary for all safety checks.
**Beat affected**: 5
**Suggested handling**: Present provenance metadata as one strong control mechanism, not the only viable one. Note that verification helps reproducibility and governance even if collapse metrics can be source-agnostic. Quantify how many papers in this focus support collapse risk versus mitigation so the corpus does not appear one-sided.

---


## Summary

Total contradictions: 46
Critical (must address): 15

## Thesis Risk Assessments

- Moderate-to-high risk for any absolute claim that fresh human data is necessary and synthetic data inevitably collapses models. The strongest contradiction is that curated self-consuming loops can, at least theoretically, avoid collapse and optimize human preferences. Additional image-generation papers show empirical rescue mechanisms where synthetic data helps if used with negative guidance or negative extrapolation instead of naive imitation. The safer thesis is narrower: uncurated, recursively reused synthetic data threatens rare modes and diversity, while curated or corrected synthetic pipelines may substitute in some regimes. The necessity of provenance verification is also weakened by work showing collapse can be detected without origin labels.
- Moderate risk. The literature does not support a simple claim that web pollution is broadly detectable. The strongest tension is that retrieval can serve as a defense against paraphrase-evasive AI text only when the retrieval corpus is itself trustworthy; the Retrieval Collapse paper shows that heavy web pollution can break that assumption. Positive detection results mostly come from bounded settings: domain-specific classifiers, cooperative watermarking, or controlled corpora. Overall, the safest synthesis is that web pollution is conditionally detectable under provenance, watermarking, or constrained-domain assumptions, but not reliably detectable post hoc across the open web.
- Moderate risk. There is credible evidence that the web changes over time and that some slices worsen in ways relevant to LLM training: AI-generated Wikipedia growth, C4 contamination, web-composition shifts, and shrinking consent coverage. But the strongest counterevidence is substantial: RefinedWeb and FineWeb show that large, filtered web corpora still train very strong models, implying that scale, filtering, and dataset construction are powerful competing explanations. The biggest weakness for a strong Beat-2 claim is measurement validity: much of the 'decline' evidence is either domain-specific, synthetic rather than live-web, or based on metrics whose robustness depends on corpus size/content controls.
- The main risk is not a single thesis-killing contradiction, but a cluster of strong countermechanisms. RLAIF and AlpacaFarm show that AI-mediated feedback can recover much of benchmarked alignment quality at far lower cost, and DPO/RRHF show that objective design can matter as much as or more than elaborate RLHF pipelines. The thesis is still defensible if it is narrowed: authentic human data appears most clearly valuable for socially grounded outcomes that require demographic representativeness, explicit accountability, truth-sensitive annotation, and provenance auditability. Claims should avoid implying that human data is universally necessary for all post-training gains.
- Overall risk is moderate. The synthetic-data and AI-feedback papers strongly support the claim that human-authored supervision can be reduced substantially for instruction following, chat benchmarking, and some preference-learning workflows. However, the contradictory evidence is serious on four fronts: last-mile dialogue quality, demographic representativeness, safety-specific supervision, and the possibility that gains are partly explained by model scale or tiny high-quality human datasets rather than synthetic supervision itself. The safest synthesis is not 'human-authored supervision is no longer needed,' but 'AI feedback, self-alignment, and synthetic instruction data can replace a large share of routine supervision, while humans remain important for value specification, safety labeling, representativeness, and high-quality editing.'
- moderate. The strongest risk is to any blanket claim that AI contamination of web data straightforwardly causes training-data quality decline. RefinedWeb, FineWeb, and Yi show that aggressively filtered, deduplicated, and better-engineered web corpora can still produce very strong models, so the simple contamination-equals-decline story is too coarse. However, the countervailing papers do not disappear: C4 documentation shows real hidden contamination and bias in major web corpora, Wikipedia shows source-specific quality degradation from AI-written content, Retrieval Collapse shows a distinct degradation mechanism in retrieval exposure, and Consent in Crisis shows provenance failures not captured by benchmarks. The defensible thesis is therefore narrower: contamination harms are real but mediated by corpus construction, source selection, documentation quality, and downstream system architecture.
- Moderate-to-high risk. The set strongly supports that post-training data composition changes broad alignment behavior, and some social-specific training can improve social outputs. But several social-benchmark papers show that these gains do not straightforwardly transfer to Theory-of-Mind or pragmatic relevance tasks. The largest threat to a simple 'data composition matters' thesis is causal ambiguity: some evidence points to reward design, task construction, or control-time steering as equally plausible explanations for social-reasoning gains.
- Moderate-to-high. The strongest risk comes from DEL-ToM, self-consistency, and CoSToM, which all offer real non-data mechanisms for improving reasoning or ToM behavior at inference time. These papers mean a thesis centered on post-training data authenticity cannot simply infer causality from better social performance. However, the risk is not fatal: benchmark papers on pragmatic relevance and cross-cultural false-belief show that inference-time gains and elicitation methods do not obviously solve the full social-reasoning problem, so a bounded thesis claiming authentic data matters for ecologically valid, human-grounded outcomes can still hold.

## Unresolved Tensions

- Do the provable benefits of curated self-consuming training survive realistic, imperfect curation rather than idealized assumptions?
- Do image-domain rescue mechanisms such as negative guidance or negative extrapolation transfer to language and socially grounded reasoning tasks?
- Is verified provenance necessary mainly for governance/accountability, or also for outcome quality once good collapse diagnostics are available?
- Can curated synthetic data preserve rare, tail, or safety-critical human phenomena as reliably as fresh human data, especially in high-stakes domains?
- How much of the open web is polluted enough to invalidate retrieval-as-defense, rather than just degrade it marginally?
- What fraction of future AI-generated content will actually carry robust provenance or watermark signals, making detection operational rather than theoretical?
- How well do high reported detector accuracies survive paraphrasing, domain shift, and adversarial rewriting in open-web conditions?
- Controlled-domain prevalence studies such as MOOCs or phishing do not yet establish whole-web contamination rates or whole-web detectability limits.
- There is still no clean, web-wide longitudinal benchmark that measures contamination, diversity, and utility across comparable crawl snapshots with stable methods.
- It remains unclear how much FineWeb/RefinedWeb success comes from better filtering and selection versus genuine resilience of the live web itself.
- AI-generation growth is documented in Wikipedia, but comparable time-series estimates for broader Common Crawl-like web text are missing.
- Consent/access degradation and textual-quality degradation are distinct and should not be collapsed into one drift narrative.
- Metric-based diversity decline claims need stronger robustness checks against corpus size, topic mix, and sampling changes before they can anchor Beat 2.
- How much of apparent RLHF success is actually due to optimization design or evaluator choice rather than uniquely human supervision?
- What socially grounded evaluations would clearly separate AI-feedback parity from genuine demographic or normative representativeness?
- Can human data be reduced to seed sets and audit sets while synthetic or AI feedback handles scale, or does performance degrade on contested social judgments when humans are removed from the loop?
- Whether benchmark success without human annotation transfers to socially grounded metrics such as demographic representativeness and harmlessness.
- How much of the apparent success of synthetic alignment is actually due to strong base-model pretraining or model scale rather than the synthetic data pipeline itself.
- What minimum amount and kind of human-authored seed data, principles, or post-editing is still necessary for robust alignment.
- Whether AI-generated feedback inherits and amplifies the opinion biases or narrow priors of the underlying model.
- Which alignment subproblems can tolerate synthetic supervision and which still require human-authored datasets or human oversight.
- How much of the success of RefinedWeb, FineWeb, and Yi depends on excluding or diluting AI-generated content versus merely overpowering it with scale and filtering is still unclear from these papers alone.
- Benchmark gains from filtered pretraining corpora may not transfer to socially grounded or retrieval-augmented settings where exposure contamination is amplified by search and RAG dynamics.
- Corpus audits show that a dataset can score well on performance while still containing benchmark leakage, demographic filtering distortions, or nonconsented material, so 'quality' remains underdefined unless provenance and fairness are tracked separately.
- Whether social-benchmark improvements come from the composition of post-training data itself or from the training objective and reward structure applied to that data.
- Whether alignment wins on preference, MT-Bench-style chat quality, or perceived helpfulness are informative proxies for Theory-of-Mind and social-pragmatic competence.
- Whether latent social knowledge is already present in base models, making steering or other control-time mechanisms more important than additional curated post-training data for external social reasoning behavior.
- There is no head-to-head comparison on the same base models between provenance-aware authentic post-training data and strong inference-time scaling methods such as verifier-guided search or self-consistency.
- It remains unclear whether social gains from steering and inference-time scaling are additive with, substitutive for, or orthogonal to gains from authentic training data.
- Most inference-time papers optimize benchmark reasoning; it is unresolved whether those gains persist on pragmatic, culturally variable, or real deployment social tasks.
- CoSToM raises an acquisition-vs-elicitation question: if ToM knowledge is already latent, the thesis must specify whether authentic data improves knowledge itself, its reliability of expression, or both.
- General reasoning improvements from chain-of-thought and self-consistency may not cleanly transfer to socially grounded reasoning; the scope boundary is still unsettled.