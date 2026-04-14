# Evidence Sufficiency Report

*Assessment of literature support for each beat of the paper*

---

## Beat 1: Model Collapse and Contamination Risk 🟢 strong

Supporting papers: 21
Key papers present: Self-Consuming Generative Models go MAD, Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe, A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train, How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model, The Curse of Recursion: Training on Generated Data Makes Models Forget
Weakness: The corpus strongly supports that recursive synthetic reuse can cause collapse and that contamination risk is rising, but it only supports a cautious mitigation claim: collapse is avoidable in mixed or curated regimes, and the practical thresholds for web-scale failure remain unresolved.

Evidence chain:
  → Self-Consuming Generative Models go MAD establishes recursive degeneration under self-consuming training.
  → The Curse of Recursion: Training on Generated Data Makes Models Forget shows forgetting and diversity loss from generated-data reuse.
  → How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model quantifies degradation rather than treating collapse as a purely anecdotal risk.
  → Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe shows curated real data can mitigate or delay collapse.
  → A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train narrows the claim: collapse is real, but not universal under curation and mixed-data assumptions.

---

## Beat 2: Web Drift and Limits of Reactive Filtering 🟡 adequate

Supporting papers: 12
Key papers MISSING: DataComp-LM: In Search of the Next Generation of Training Sets for Language Models, FineWeb: Decanting the Web for the Finest Text Data at Scale
Weakness: Support is partial, which is acceptable for this beat. The corpus can support that drift is measurable through proxies and that filtering/curation can still yield strong web corpora, but it cannot support a strong causal claim that post-2022 AI content has already contaminated the web at model-relevant scale. Category H is small, D-H linkage is sparse, and B/C literature still leaves prevalence thresholds and downstream effects open.

Evidence chain:
  → Category D papers provide proxy-style measurements for web drift and authenticity-related signals.
  → Category B papers document rising AI-generated content prevalence in parts of the web and scholarly ecosystems.
  → Category C papers show reactive detection and watermarking are limited and fragile under paraphrase, editing, and deployment shift.
  → Category H papers indicate filtered web corpora can still be useful for strong model training.
  → Taken together, the evidence supports measurable drift risk, not web-scale causal proof of contamination damage.

---

## Beat 3: L_auth as a Stage-Agnostic Descriptive Framework 🟡 adequate

Supporting papers: 13
Key papers present: Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe, A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train
Weakness: The bridge is conceptually defensible but not empirically validated as a law. D has enough material to motivate measurable ingredients, and A/E/I give a rationale for provenance, diversity, and entropy-like dimensions, but the corpus does not yet show that the four dimensions form a validated, predictive, stage-agnostic metric system.

Evidence chain:
  → Collapse papers in A motivate why authenticity-related properties of training data matter.
  → Proxy and measurement work in D contributes observable ingredients for provenance, lexical diversity, and entropy-style signals.
  → Dataset quality and provenance papers in E and I justify adding behavioral and source-side dimensions.
  → The synthesis supports L_auth as a descriptive organizing framework.
  → The corpus does not validate L_auth as a universal predictive law, so the claim must remain explicitly modest.

---

## Beat 4: Social Reasoning and Data Provenance 🟡 adequate

Supporting papers: 14
Key papers MISSING: Less Is More for Alignment (LIMA), AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback, Constitutional AI / RLAIF-style AI-feedback paper
Weakness: This beat can support only the narrower claim. The F/I/J evidence base is large enough to argue that provenance and behavioral diversity matter for socially grounded fine-tuning, but not that human data is always superior. The crucial exemplars named in the target argument line are not verifiable from the supplied metadata, so the corpus presently supports a cautious version better than a headline claim.

Evidence chain:
  → Category F papers supply the main evidence that socially grounded or instruction-following performance is sensitive to fine-tuning data choice.
  → Category J papers show that AI feedback can substitute for human feedback on bounded optimization tasks.
  → Category I papers add recent provenance and diversity-focused evidence relevant to social reasoning transfer.
  → Together these categories support the narrow conclusion that curated human data appears especially valuable for socially grounded tasks.
  → This line is properly separated from collapse evidence: A has zero direct edges to F, I, and J.

---

## Beat 5: Contrastive Fine-Tuning Experiment 🟠 weak

Supporting papers: 9
Key papers MISSING: Less Is More for Alignment (LIMA), AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
Weakness: The corpus can justify a pilot experiment and can plausibly deliver directional support, but it does not look sufficient to claim robust validation of a high/medium/low L_auth contrastive study on social reasoning benchmarks. Category I is small and very recent, direct F-I-J integration is sparse, and the supplied evidence does not reveal a canonical controlled paper that already ties provenance, behavioral diversity, and social benchmarks together.

Evidence chain:
  → Category I papers provide the closest ingredients for authenticity-aware data partitioning.
  → Category F papers provide social reasoning benchmarks and task sensitivity.
  → Category J papers provide AI-feedback comparison baselines for bounded-task substitution.
  → These components are enough for a pilot directional result.
  → They are not enough for a definitive validation of the full experimental claim.

---

## Beat 6: CampusGo Proposal 🟠 weak

Supporting papers: 7
Weakness: The proposal is motivated but not validated. Category G has enough material to justify building a provenance-rich social interaction platform, but the graph is highly disconnected from A/E/I, so the corpus does not show that a CampusGo-like system will actually optimize D1 and D4 in a way that improves downstream model quality. This beat can only support a design direction.

Evidence chain:
  → Category G papers make platform-mediated, provenance-aware data collection plausible.
  → Category I motivates why provenance and social behavioral diversity are worth optimizing.
  → Category E suggests that dataset design choices can matter for downstream quality.
  → The resulting evidence supports CampusGo as a motivated collection strategy.
  → It does not validate CampusGo as a solved intervention or performance-improving system.

---

## Overall Assessment
The corpus is sufficient for a cautious 6-beat paper, but unevenly. Argument Line 1 is the strongest part: Beat 1 is genuinely strong, and Beat 2 is adequate if the claim stays explicitly non-causal and proxy-based. Beat 3 works as a conceptual bridge, not as a validated theory. Argument Line 2 is supportable only in a narrower form: Beat 4 is adequate for the claim that provenance and social behavioral diversity matter especially for socially grounded tasks, but Beat 5 is only weak as a validation beat and Beat 6 is weak as an application beat. The cleanest structural result is argument-line separation: Category A has zero direct edges to F, I, and J, so the fine-tuning argument is not being improperly propped up by pretraining collapse papers. The main vulnerability is not lack of any evidence, but lack of direct, mature, named exemplars linking provenance-controlled fine-tuning to social reasoning outcomes and then to a concrete collection platform.

## Missing Papers (search suggestions)

- **Less Is More for Alignment (LIMA)**: Central for Beat 4 because it is the canonical evidence that a small amount of carefully curated human data can be disproportionately valuable in instruction/fine-tuning. Without it, the human-curation side of the fine-tuning argument is under-anchored.
  Search: `Search for 'LIMA less is more for alignment curated human data instruction tuning social reasoning'.`
- **AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback**: Important for Beats 4-5 because it provides a concrete bounded-task comparison point for when synthetic or automated feedback can substitute for human feedback. It helps narrow the claim instead of overstating human-data superiority.
  Search: `Search for 'AlpacaFarm learn from human feedback AI feedback bounded tasks benchmark'.`
- **DataComp-LM: In Search of the Next Generation of Training Sets for Language Models**: Important for Beat 2 and indirectly Beat 3 because it strengthens the filtered-web-corpus side of the story with a recognized data curation benchmark, helping support the claim that web data can remain useful under strong filtering even as drift risk rises.
  Search: `Search for 'DataComp-LM filtered web corpus curation language models training data quality'.`

## Strongest Narrative Thread
Self-Consuming Generative Models go MAD → The Curse of Recursion: Training on Generated Data Makes Models Forget → How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model → Self-Consuming Generative Models with Curated Data Provably Optimize Human Prefe → A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train
