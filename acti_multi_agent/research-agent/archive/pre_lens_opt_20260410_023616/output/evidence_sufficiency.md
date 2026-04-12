# Evidence Sufficiency Report

*Assessment of literature support for each beat of the paper*

---

## Beat 1: Crisis Exists 🔴 critical_gap

Supporting papers: 45
Key papers present: Self-Consuming Generative Models go MAD, A Tale of Tails: Model Collapse as a Change of Scaling Laws, Large Language Models Suffer From Their Own Output: An Analysis of the Self-Cons, A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train...
Key papers MISSING: The Curse of Recursion: Training on Generated Data Makes Models Forget, Alemohammad et al. 2024 paper measuring AI-generated content prevalence in web-scale corpora
Weakness: A and C are reasonably covered, but category B is effectively missing, so the corpus cannot document the scale of web pollution itself. The required chain 'collapse is real + web data is polluted + reactive detection fails' therefore breaks on the middle claim. This is reinforced by zero A-B and B-C intersections and a highly fragmented graph overall.

Evidence chain:
  → Self-Consuming Generative Models go MAD establishes recursive self-training degradation.
  → A Tale of Tails frames collapse as tail-loss/scaling-law change rather than a narrow artifact.
  → Large Language Models Suffer From Their Own Output extends the concern to LLM self-consumption.
  → Category C papers then show detector/watermark limits under paraphrase and light editing, so reactive filtering is unreliable.
  → But without category B, the corpus does not quantify how much polluted web data is actually present at web scale.

---

## Beat 2: Web Quality Declines Over Time 🔴 critical_gap

Supporting papers: 7
Key papers MISSING: A longitudinal Common Crawl or web-corpus study measuring growth of AI-generated text over time
Weakness: This beat depends on H plus D, but H has only 3 papers and D has only 4. The corpus has almost no direct temporal evidence for declining web quality, and the category gaps explicitly note that existing papers do not analyze growing AI-generated fractions in CommonCrawl or temporal drift. With only sparse D-H bridging and no strong citation structure, this claim is not supportable as written.

Evidence chain:
  → Category H provides a small start on temporal measurement of web quality.
  → Category D provides candidate entropy/diversity metrics.
  → Together they are too thin to demonstrate a robust longitudinal decline in web content quality.

---

## Beat 3: L_auth Theory and Novelty 🔴 critical_gap

Supporting papers: 4
Key papers MISSING: On Measures of Entropy and Information, On Information and Sufficiency
Weakness: Only 4 papers sit in D, with median year 2026 and median citations 0, so the theoretical base is both thin and immature. The listed D gaps say these papers do not connect theory to practical text-quality metrics or training-data curation. The corpus therefore does not adequately ground the proposed composite objective or establish that the exact L_auth combination is novel relative to prior work.

Evidence chain:
  → Existing D papers offer pieces of entropy/divergence machinery.
  → They do not clearly justify the specific KL-plus-alpha-divergence-plus-TTR composition.
  → No clear novelty-comparison chain is present to show that L_auth is a new contribution rather than a recombination of standard measures.

---

## Beat 4: Verified Social Data Outperforms Web-Scraped Data 🟡 adequate

Supporting papers: 57
Key papers MISSING: A direct head-to-head study comparing physically verified human interaction data against web-scraped corpora on social reasoning benchmarks
Weakness: This is the best-supported beat by raw count, drawing on E, F, I, and J. However, the evidence is fragmented: intersections are mostly bridging only, I and J are recent with low citation maturity, and there is no clearly identified flagship paper directly testing physically verified authentic social-behavioral data against web-scraped data. So the beat is supportable in principle, but the exact CampusGo-style claim is still somewhat inferential.

Evidence chain:
  → Category F supports the general value of human-authored or human-grounded data.
  → Category E supports data-quality and curation effects on downstream performance.
  → Category I supplies social-reasoning evaluation settings.
  → Category J provides ablation and fine-tuning methodology needed for a credible comparison.
  → Taken together, these categories can support an empirical validation section, but likely not a definitive one without a direct benchmark paper.

---

## Beat 5: CampusGo as Solution Mapping 🔴 critical_gap

Supporting papers: 31
Key papers present: A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train...
Key papers MISSING: A platform-design precedent for collecting verified offline social behavior specifically for ML training
Weakness: Although A is strong and G contains 4 highly cited platform-design papers, there are zero A-G edges and zero broader links from G into the rest of the argument. That means the corpus does not actually show how collapse theory or L_auth-style authenticity metrics map into platform mechanics. As a result, CampusGo's design logic is mostly conceptual rather than literature-backed.

Evidence chain:
  → Category A motivates the need for authentic human data accumulation.
  → Category G shows there are platform-design precedents for behavior collection.
  → But the corpus contains no real bridge from collapse/authenticity theory to a validated platform architecture, so the solution beat is not evidentially closed.

---

## Overall Assessment
The corpus is not sufficient to fully support the 5-beat paper. Beat 4 is the only beat that reaches adequacy, and even there the evidence is fragmented rather than tightly integrated. Beat 1 has strong collapse and detection material but fails on the missing pollution-scale literature. Beats 2 and 3 are critical gaps because temporal web-quality decline and the L_auth theoretical/novelty claim are both under-evidenced. Beat 5 is also a critical gap because platform-design precedent is too sparse and disconnected from the collapse/authenticity literature. The graph structure confirms this: 168 nodes but only 149 edges, 118 components, and 105 isolated papers, so the corpus is broad but not narratively connected.

## Missing Papers (search suggestions)

- **The Curse of Recursion: Training on Generated Data Makes Models Forget**: This is a canonical model-collapse paper that would strengthen Beat 1 by adding a widely recognized long-horizon recursive-training result and improving the theoretical continuity of category A.
  Search: `Search exact title plus authors Shumailov and model collapse recursion.`
- **Alemohammad et al. 2024 paper on AI-generated content prevalence in Common Crawl or web-scale corpora**: The largest hole in the corpus is category B: web pollution scale. A paper that estimates the prevalence and temporal growth of AI-generated web text is essential for Beat 1 and Beat 2.
  Search: `Search: Alemohammad Common Crawl AI-generated content prevalence web contamination 2024.`
- **On Measures of Entropy and Information**: This is a foundational source for alpha-divergence and entropy-style measurement. It would materially strengthen Beat 3 by grounding the D_alpha part of L_auth in canonical information theory.
  Search: `Search exact title with author Rényi and pair it with Kullback-Leibler foundational citations.`

## Strongest Narrative Thread
Self-Consuming Generative Models go MAD → A Tale of Tails: Model Collapse as a Change of Scaling Laws → Large Language Models Suffer From Their Own Output: An Analysis of the Self-Cons → A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Train... → Category C detector-limit papers on paraphrase and watermark evasion → Category F/E/I/J papers linking human-grounded data quality to social-reasoning evaluation
