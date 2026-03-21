# Vibe Research: Complete Paper Logic Chain & Automated Execution Plan

## Paper Working Title

**"Authentic Human Behavioral Data as AI Training Signal: Quantifying Information Loss in Web-Scraped Corpora and Designing Physically-Grounded Data Generation Platforms"**

---

## 0. 论文总图景 (Big Picture)

### 核心论点 (One-sentence thesis)

Web-scraped训练数据正在经历信息退化（尾部坍塌、熵下降、多样性丧失），而经过物理验证的真实人类社交行为数据——特别是在social intelligence和human alignment维度——提供了不可替代的训练信号；CampusGo是一个按照这些原则设计的、正在运行的数据生成平台。

### 叙事五拍结构

```
Beat 1: 危机存在 (Literature) ──────→ 已证实：AI训练在web数据上正在退化
    ↓
Beat 2: 数据证据 (Empirical) ──────→ API爬取数据实证：web内容质量趋势
    ↓
Beat 3: 理论框架 (L_auth) ─────────→ 定义authenticity loss，量化退化机制
    ↓
Beat 4: 验证方案 (Experiment) ─────→ 用外部真实社交数据fine-tune，测social tasks
    ↓
Beat 5: CampusGo设计 (Solution) ──→ 一个持续产出这种数据的平台，已在运行
```

### Research Gap 精确定位

已知（文献已解决的）：
- Model collapse的理论机制（Shumailov 2024, Dohmatob 2024）
- 合成数据在预训练中的scaling law（纯合成不优于CommonCrawl，但混合有益）
- RLHF/preference data的高成本（高质量人类数据成本是计算成本的3.1倍）
- 数据积累可避免collapse（Gerstgrasser 2024）

未知（本文要填的gap）：
- **没有人量化过"social intelligence"维度上authentic vs web-scraped数据的训练效果差异**
- **没有人将Gerstgrasser的积累原则连接到一个具体的、物理验证的数据生成平台设计**
- **缺乏一个从信息论（entropy/divergence）到平台设计特征的完整映射框架**

本文的贡献不是"CampusGo让AI更强"，而是：
1. 定义并量化了L_auth（authenticity loss function）
2. 实证验证了authentic social data在social reasoning任务上的不可替代性
3. 将理论原则映射到了一个已部署平台的具体设计决策

---

## 1. Beat 1: The Crisis Exists（文献综述）

### 1.1 本节学术目标

证明三件事：
- (a) Model collapse是已被理论证明和实验验证的真实现象
- (b) Web-scale训练数据正在被AI生成内容污染
- (c) 现有的解决方案（数据过滤、检测AI文本、数据清洗）都是reactive的，没有proactive的方案

### 1.2 所需文献分类

| 类别 | 目标数量 | 关键搜索方向 | 作用 |
|------|---------|-------------|------|
| A. Model Collapse Theory | 30-40篇 | 递归训练退化、尾部坍塌、MAD | 建立问题的理论基础 |
| B. Web Data Pollution | 20-30篇 | AI生成内容在web上的比例、CommonCrawl退化 | 建立问题的现实紧迫性 |
| C. AI Text Detection | 20-30篇 | 检测方法、检测器的局限性 | 论证reactive方案不够 |
| D. Information Theory + Text | 20-30篇 | n-gram entropy、perplexity、LLM文本统计特征 | 为L_auth提供理论工具 |
| E. Data Quality for Training | 30-40篇 | 数据筛选、去重、质量评估方法 | 建立"数据质量影响训练效果"的因果链 |
| F. Human Data Value | 15-20篇 | RLHF成本、preference data、human-in-the-loop | 论证human data的不可替代性 |
| G. Platform/System Design | 10-15篇 | 数据平台设计、provenance验证、federated learning | Beat 5的理论背景 |

### 1.3 自动化执行 — Claude Code Agent Prompt

```
SYSTEM: You are a literature discovery agent for a paper on AI training data quality 
and the value of authentic human behavioral data.

CURRENT PHASE: Beat 1 — Literature Review
TASK: For each of the 7 categories (A-G), run search queries and collect papers.

CATEGORY-SPECIFIC SEARCH QUERIES:

Category A (Model Collapse Theory):
  OpenAlex: "model collapse generative AI", "recursive training degradation", 
            "self-consuming generative models", "tail collapse scaling laws"
  arXiv: all:"model collapse" AND all:"training data"
         all:"self-consuming" AND all:"generative"
  S2 citation expand from: Shumailov 2024 (603d3f90...), Alemohammad 2024

Category B (Web Data Pollution):
  OpenAlex: "AI generated content web pollution", "synthetic text contamination internet",
            "CommonCrawl quality degradation over time", "web corpus synthetic content fraction"
  arXiv: all:"web data" AND all:"AI generated" AND all:"contamination"

Category C (AI Text Detection):
  OpenAlex: "AI generated text detection", "machine generated text classifier",
            "watermarking language model output", "detector evasion AI text"
  arXiv: all:"detecting" AND all:"AI generated text"

Category D (Information Theory + Text):
  OpenAlex: "n-gram entropy language model", "perplexity human vs AI text",
            "text diversity measurement information theory", "KL divergence text distribution"
  arXiv: all:"entropy" AND all:"language model" AND all:"text diversity"

Category E (Data Quality for Training):
  OpenAlex: "data quality LLM training", "data curation pretraining",
            "data mixing ratio language model", "deduplication training data effect"
  arXiv: all:"data quality" AND all:"pretraining" AND all:"language model"

Category F (Human Data Value):
  OpenAlex: "RLHF human feedback cost", "preference data quality alignment",
            "human annotation vs synthetic labeling", "human data bottleneck AI training"
  arXiv: all:"human data" AND all:"alignment" AND all:"training"

Category G (Platform Design):
  OpenAlex: "data provenance verification platform", "authentic data generation system",
            "community platform behavioral data", "anti-algorithmic design"

FOR EACH PAPER FOUND:
- Record: title, authors, year, venue, DOI, abstract, citation_count
- Assign primary_category (A-G) and up to 2 secondary categories
- Extract one_sentence_contribution
- Note: what does this paper NOT address? (gap_it_leaves)

QUALITY GATES:
- Total target: 180-220 unique papers
- Each category must have ≥ 10 papers
- At least 40% from 2023-2026
- No unverifiable citations (every paper must have DOI or arXiv ID)

OUTPUT: data/processed/beat1_corpus.json
```

---

## 2. Beat 2: Empirical Evidence（数据实证）

### 2.1 本节学术目标

用可复现的数据分析证明：web上可获取的文本数据的信息质量正在随时间下降。这是Beat 1理论预测的实证验证。

### 2.2 需要回答的具体研究问题

- RQ2a: 在过去3-5年间，主流web数据源的n-gram entropy是否呈下降趋势？
- RQ2b: AI生成内容在社交平台上的估计比例是多少？有多大的跨平台差异？
- RQ2c: 不同类型的数据源（开放社交 vs 带验证机制的社区）在文本多样性指标上是否有系统性差异？

### 2.3 数据源及获取方法

| 数据源 | API / 获取方式 | 数据量目标 | 你能拿到什么 |
|--------|--------------|-----------|-------------|
| **Bluesky firehose** | AT Protocol `com.atproto.sync.subscribeRepos`，完全开放 | 10万条帖子 | 带时间戳的社交文本，用户元数据 |
| **Stack Overflow data dump** | archive.org 季度发布，CC-BY-SA授权 | 50万条回答 | 带reputation的经过同行验证的文本 |
| **Reddit (Pushshift archive)** | 学术镜像 + r/datasets | 10万条帖子 | 2020-2023的subreddit文本时间序列 |
| **OpenAlex abstracts** | OpenAlex API（你已有脚本） | 5万篇摘要 | 学术写作的entropy时间趋势 |
| **CampusGo Supabase** | 直连你的数据库（已有权限） | 全量 | GPS验证的社交互动文本 |

### 2.4 要计算的指标

| 指标 | 公式/方法 | 意义 |
|------|----------|------|
| **2-gram entropy** | H₂ = -Σ p(w₁w₂) log₂ p(w₁w₂) | 文本可预测性；越低说明越模式化 |
| **3-gram entropy** | 同上，3-gram | 更长程的多样性测量 |
| **Type-Token Ratio (TTR)** | unique_tokens / total_tokens（取定长窗口避免长度偏差） | 词汇丰富度 |
| **Hapax ratio** | 只出现1次的词 / total unique | 尾部丰富度的直接测量 |
| **Perplexity (GPT-2 scorer)** | PPL = exp(NLL) | 文本对标准LM的"惊奇度"；越高=越不像AI生成 |
| **AI content fraction** | 用Binoculars/GLTR/DetectGPT检测 | 估计数据源中AI生成内容的比例 |

### 2.5 自动化执行 — Claude Code Agent Prompt

```
SYSTEM: You are a data analysis agent. You crawl text datasets and compute 
information-theoretic metrics to measure text diversity trends.

CURRENT PHASE: Beat 2 — Empirical Evidence of Web Content Degradation
TASK: For each data source, collect text data and compute 6 metrics.

WORKFLOW:
1. For each data source in [Bluesky, StackOverflow, Reddit, OpenAlex, CampusGo]:
   a. Fetch text data using the appropriate API/file
   b. Clean: remove URLs, @mentions, markdown formatting
   c. Tokenize using tiktoken (cl100k_base, same tokenizer as GPT-4)
   d. For temporal analysis: bin data by month/quarter
   e. Compute all 6 metrics per time bin

2. CRITICAL FEASIBILITY CHECK (run this FIRST on a small sample):
   - Take 1000 texts from each source
   - Compute 2-gram entropy
   - If entropy varies < 0.1 bits across sources → signal may be too weak
   - If entropy varies > 0.5 bits → strong signal, proceed with full dataset
   - Record feasibility result in analysis/beat2_feasibility.json

3. For temporal degradation:
   - Plot metric vs time for each source
   - Fit linear regression: metric = β₀ + β₁·time
   - Report slope (β₁), p-value, R²
   - If p < 0.05 and β₁ < 0 → statistically significant decline

4. For cross-source comparison:
   - Box plots of each metric across sources
   - Kruskal-Wallis test for significant differences
   - Pairwise Mann-Whitney U tests with Bonferroni correction

OUTPUT FILES:
- data/processed/beat2_metrics_by_source.csv
- analysis/beat2_feasibility.json (run FIRST)
- analysis/beat2_temporal_trends.json
- analysis/beat2_cross_source_comparison.json
- output/beat2_figures/ (all plots as PNG)

IF FEASIBILITY CHECK FAILS (signal too weak):
- Record the null result
- Shift Beat 2 to literature-based indirect evidence only
- Use Briesch et al. 2023 EMNLP + Shumailov 2024 experimental results as proxy
- This is NOT a paper failure — it's an honest empirical finding
```

---

## 3. Beat 3: Theoretical Framework — L_auth

### 3.1 本节学术目标

提出一个信息论框架来量化"数据真实性损失"（Authenticity Loss），将Beat 1和Beat 2中发现的问题形式化为可计算的指标体系。

**这一节主要靠你的脑子，不靠AI。** AI的角色是搜集相关的信息论工具和已有框架，确保你没有重新发明已存在的东西。

### 3.2 L_auth框架（从之前修正后的版本）

```
L_auth = λ₁·D_KL(P_human ‖ P_data) + λ₂·D_α(P_human ‖ P_data) + λ₃·(1 - TTR_r)
```

三个分量的正交性论证：
- D_KL：bulk divergence，被高概率事件主导。collapse初期不敏感。
- D_α (Rényi, α=2)：tail-sensitive。D_KL可以低（bulk还行）但D_α高（尾巴没了）。
- 1-TTR_r：无需分布估计的实用指标。直接从raw text可算。

此外定义三个结构性指标：
- PV (Physical Verifiability)：数据中有物理验证信号的比例
- AR (Accumulation Rate)：真实数据累积速率，d|D_real|/dt > 0
- PD (Provenance Depth)：每个数据点的验证层数 (1-4)

### 3.3 与已有框架的关系（AI要帮你搜的）

```
SYSTEM: You are a theoretical literature agent.

TASK: Search for existing frameworks that overlap with L_auth to ensure novelty.

SEARCH FOR:
1. "data quality metric information theory" — 是否有人已经定义了类似的loss function?
2. "authenticity score data verification" — 是否有人做过数据真实性的量化?
3. "entropy based data quality assessment" — 信息论在数据质量评估中的已有应用
4. "Rényi divergence application text analysis" — Rényi散度在NLP中的使用先例
5. "training data quality metric LLM" — LLM训练中已有的数据质量指标

FOR EACH RELEVANT PAPER:
- What exactly did they define?
- How is L_auth different or more general?
- Can we cite them as "building on" or must we cite them as "concurrent work"?

OUTPUT: analysis/beat3_novelty_check.json
```

### 3.4 你需要做的（非自动化）

- 写出L_auth的完整数学定义和性质分析
- 证明三个分量的正交性（或至少论证它们捕获不同信号）
- 定义λ权重的校准方法（不是固定常数，是用已知authentic/synthetic对比来调参）
- 讨论L_auth与Gerstgrasser积累条件的关系：AR > 0 ⟹ L_auth不会单调增长
- 讨论局限性：L_auth是对文本数据定义的，对非文本（图像、行为日志）需要扩展

---

## 4. Beat 4: Validation with External Data（实验验证）

### 4.1 本节学术目标

这是论文的**实验核心**。要回答一个具体问题：

**在social intelligence / social reasoning任务上，用经过身份验证的人类社交数据fine-tune的模型，是否优于用未验证的web-scraped数据fine-tune的模型？**

注意：不是证明在所有任务上都优于。是证明在**这个specific维度**上有不可替代的价值。

### 4.2 实验设计

```
实验变量:
  自变量: 训练数据的authenticity level
    - Condition A: "Web-scraped" — Reddit + random web text, 未做AI内容过滤
    - Condition B: "Filtered" — 同样来源, 但用AI检测器过滤掉疑似合成内容
    - Condition C: "Verified authentic" — Stack Overflow (reputation > 100的回答) 
                   + Bluesky (early adopter, pre-bot-wave) + CampusGo data

  因变量:
    1. Social reasoning accuracy (自定义benchmark, 见下)
    2. Output text diversity (TTR, entropy of model outputs)
    3. Tone/register appropriateness (人工评估 or LLM-as-judge)
    4. Standard perplexity on held-out human text

  控制变量:
    - 数据量: 三组等量 (e.g., 各50K条文本)
    - Base model: 同一个 (TinyLlama 1.1B 或 Phi-3-mini)
    - Fine-tune method: LoRA, 同超参
    - Evaluation: 同一benchmark
```

### 4.3 Social Reasoning Benchmark（你需要设计/找的）

这是Beat 4最关键的一步——你需要一个evaluation set来测"social intelligence"。几个选项：

| 选项 | 来源 | 规模 | 优劣势 |
|------|------|------|--------|
| **SocialIQA** | AllenAI, 已有benchmark | 38K题 | 成熟benchmark，但可能已被主流模型过拟合 |
| **EmpatheticDialogues** | Facebook Research | 25K对话 | 测情感理解 |
| **自建mini-benchmark** | 你自己写20-50道题 | 20-50题 | 最relevant但规模小，统计power弱 |
| **混合策略** | SocialIQA子集 + 自建10题 | ~200题 | 兼顾validity和specificity |

推荐混合策略：用SocialIQA的一个子集（100题）测general social reasoning，然后自己设计50题测**campus-specific social scenarios**（判断邀请是否真诚、理解群聊中的social dynamics、识别"委婉拒绝"等）。

### 4.4 自动化执行 — Claude Code Agent Prompt

```
SYSTEM: You are an experiment execution agent for a fine-tuning comparison study.

CURRENT PHASE: Beat 4 — Validation Experiment
TASK: Prepare three training datasets, fine-tune models, and evaluate.

STEP 1: DATA PREPARATION
For each condition (A: web-scraped, B: filtered, C: verified):
  a. Collect 50K text samples
  b. Standardize format: {"text": "...", "source": "...", "verification_level": 0-4}
  c. Compute L_auth metrics on each dataset (from Beat 3 framework)
  d. Save to data/experiment/condition_{A|B|C}.jsonl

CONDITION A (web-scraped):
  - Reddit: random sample from r/college, r/socialskills, r/relationships
  - Random web text from C4 or Dolma subset
  - NO filtering for AI content

CONDITION B (filtered):
  - Same sources as A
  - Run Binoculars AI detector, remove texts scored > 0.7 AI probability
  - Log: how many texts removed? What fraction?

CONDITION C (verified authentic):
  - Stack Overflow answers where answerer has reputation > 100 (verified human expertise)
  - Bluesky posts from accounts created before 2024 (pre-bot-wave)
  - CampusGo: chat messages + activity descriptions + comments (GPS+QR verified)
  - ALL texts have at least 1 layer of identity verification

STEP 2: FINE-TUNING
  - Base model: TinyLlama-1.1B-Chat (or Phi-3-mini-4k if compute allows)
  - Method: LoRA (r=16, alpha=32, target_modules=["q_proj","v_proj"])
  - Training: 3 epochs, lr=2e-4, batch_size=4, gradient_accumulation=8
  - Three runs: model_A, model_B, model_C
  - Log all training metrics to output/training_logs/

STEP 3: EVALUATION
  For each model, compute:
  a. SocialIQA subset (100 questions): accuracy
  b. Custom social scenarios (50 questions): accuracy
  c. Generated text diversity: give 50 prompts about social situations,
     collect completions, compute TTR and 2-gram entropy of outputs
  d. Perplexity on held-out human social text (1000 samples not in any training set)

STEP 4: STATISTICAL ANALYSIS
  - For each metric: three-group comparison (Kruskal-Wallis)
  - Pairwise: A vs C (main comparison), A vs B (does filtering help?), B vs C (verification > filtering?)
  - Effect size: Cohen's d for each pair
  - Report p-values with Bonferroni correction

OUTPUT:
  - analysis/beat4_results.json
  - output/beat4_figures/ (bar charts with error bars, per metric per condition)
  - analysis/beat4_interpretation.md (auto-generated summary of findings)

CRITICAL: If condition C does NOT outperform A on social reasoning tasks:
  - This is a valid result. Report it honestly.
  - Investigate: is the evaluation insensitive? Is 50K samples too few? 
    Is the base model too small to show the effect?
  - Beat 5 shifts framing: "CampusGo produces data that is structurally 
    different (higher diversity, physical grounding) even if downstream 
    performance gains require larger-scale validation"
```

---

## 5. Beat 5: CampusGo as Solution（方案呈现）

### 5.1 本节学术目标

在Beat 4建立了"verified authentic social data在social reasoning上有优势（或至少有结构性差异）"之后，论证CampusGo是一个被设计来**系统性、持续性产出这类数据**的平台。

关键转换：从"我们证明了这种数据有价值" → "我们设计了一个持续产出这种数据的系统"。

### 5.2 需要呈现的内容

| 内容 | 来源 | AI辅助程度 |
|------|------|-----------|
| 4层authenticity stack设计原则 | 你的设计决策，结合Beat 3理论 | 低——这是你的设计哲学 |
| Feature → L_auth metric映射 | 修正后版本（Strong/Moderate/Weak标注） | 中——AI帮搜类似mapping框架 |
| 反算法设计的信息论分析 | 博弈论框架：移除推荐算法=移除adversary优化目标 | 中——AI搜博弈论文献 |
| Gerstgrasser积累原则的映射 | Supabase append-only → d\|D_real\|/dt > 0 | 低——直接对应 |
| 当前开发状态和数据规模 | 138 commits, Supabase统计, 用户反馈 | 低——你已有数据 |
| CampusGo数据的L_auth指标计算 | 对Supabase数据跑Beat 2同样的metric pipeline | 高——完全自动化 |
| 与Beat 4实验中condition C的连接 | CampusGo数据是condition C的一部分 | 低——叙事连接 |

### 5.3 诚实框架

```
CampusGo是什么：
  - 一个真实运行的校园社区平台
  - 产出的数据具有物理验证（GPS+QR）和身份验证（.edu+JWT）
  - 数据积累是append-only的，满足Gerstgrasser条件
  - 反算法设计消除了performative content incentive

CampusGo不是什么：
  - 不是一个数据量足以做大模型预训练的数据源
  - 不是一个通用的AI训练数据平台
  - 当前用户量有限，部分指标（如TTR）的统计power可能不足
  - Rating→tail divergence的映射较弱

论文贡献是什么：
  不是CampusGo这个产品本身
  而是：从信息论损失函数 → 平台设计原则的完整映射方法论
  CampusGo是这个方法论的一个实例化（instantiation）
  其他校园社区或身份验证社交平台可以用同样的方法论评估自己
```

### 5.4 自动化执行 — Claude Code Agent Prompt

```
SYSTEM: You are a data analysis agent for CampusGo platform data.

CURRENT PHASE: Beat 5 — CampusGo Data Analysis
TASK: Compute L_auth metrics on CampusGo's real operational data.

DATA SOURCE: Supabase database (connection string in .env)

QUERIES TO RUN:
1. Total data volume:
   - SELECT COUNT(*) FROM activities
   - SELECT COUNT(*) FROM messages (across all chat types)
   - SELECT COUNT(*) FROM checkins
   - SELECT COUNT(*) FROM ratings

2. Text data for metrics:
   - Extract all message texts (anonymize user IDs)
   - Extract activity descriptions
   - Extract comment texts

3. Compute Beat 2 metrics on CampusGo text:
   - 2-gram entropy, TTR, hapax ratio, perplexity
   - Compare with same metrics computed on Reddit/Bluesky in Beat 2

4. Physical verification statistics:
   - PV: what % of data points have GPS+QR dual verification?
   - PD distribution: how many data points have 1/2/3/4 verification layers?

5. Accumulation rate:
   - Plot cumulative data volume over time
   - Fit growth curve: confirm d|D_real|/dt > 0

OUTPUT:
  - analysis/beat5_campusgo_metrics.json
  - analysis/beat5_campusgo_vs_baseline_comparison.json
  - output/beat5_figures/
```

---

## 6. 论文结构映射 (Section → Beat → 自动化)

| 论文Section | 对应Beat | 页数估计 | AI自动化占比 | 关键产出 |
|------------|---------|---------|-------------|---------|
| 1. Introduction | 浓缩Beat 1-5 | 2页 | 20% | 问题、贡献、论文结构 |
| 2. Related Work | Beat 1 | 5-6页 | 80% | 200篇文献的结构化综述 |
| 3. Problem Characterization | Beat 2 | 3-4页 | 70% | 实证退化曲线、跨源对比 |
| 4. Theoretical Framework | Beat 3 | 3-4页 | 30% | L_auth定义、性质、校准方法 |
| 5. Experimental Validation | Beat 4 | 4-5页 | 60% | 三组对比实验、统计分析 |
| 6. CampusGo: A Case Study | Beat 5 | 3-4页 | 50% | 设计映射、数据分析、limitations |
| 7. Discussion | Cross-beat | 2-3页 | 20% | 含义、局限性、future work |
| 8. Conclusion | Summary | 1页 | 10% | |
| **总计** | | **23-29页** | **~50%** | |

---

## 7. 自动化Pipeline总调度 — Claude Code Master Prompt

这是丢给Claude Code的**顶层调度prompt**，它读state.json决定下一步做什么：

```
SYSTEM: You are a research pipeline orchestrator for a paper on AI training data 
authenticity. You manage a multi-phase research workflow.

MASTER WORKFLOW:
  Phase 1 (Beat 1): Literature discovery → 200 papers → classified corpus
  Phase 2 (Beat 2): Empirical data collection → metrics computation → degradation analysis
  Phase 3 (Beat 3): Novelty check → existing framework survey (supports human-written theory)
  Phase 4 (Beat 4): Experiment preparation → fine-tuning → evaluation → statistical analysis  
  Phase 5 (Beat 5): CampusGo data analysis → metrics → comparison with baselines

STATE FILE: state.json
  {
    "current_phase": 1,
    "current_step": "1.3_openalex_search",
    "completed": ["1.1_seed_papers", "1.2_search_queries"],
    "blocked": [],
    "papers_found": 0,
    "papers_target": 200,
    "feasibility_check_passed": null,
    "notes": []
  }

RULES:
1. Read state.json at the start of every iteration
2. Execute the next incomplete step
3. Update state.json with results
4. Commit to git after each step
5. If a step fails, log the error and move to the next non-dependent step
6. NEVER fabricate data or citations
7. If a feasibility check fails, update the plan accordingly (see Beat 2 prompt)

PHASE DEPENDENCIES:
  Phase 1 → Phase 2 (Beat 2 needs literature to cite)
  Phase 1 → Phase 3 (novelty check needs to know what exists)
  Phase 2 → Phase 4 (experiment design informed by Beat 2 findings)
  Phase 2 → Phase 5 (same metrics pipeline applied to CampusGo)
  Phase 3 → Phase 4 (L_auth framework defines what experiment measures)
  Phase 4 → Phase 5 (CampusGo data is condition C in the experiment)

  Phases 1, 2, 3 can run in parallel.
  Phase 4 depends on 1+2+3 being done.
  Phase 5 depends on 2+4 being done.

AFTER EACH PHASE COMPLETES:
  Run the quality gate check (see research_agent_blueprint.md Part 4)
  Record pass/fail in state.json
  If fail, list specific remediation steps before proceeding
```

---

## 8. 关键风险 & 诚实备案

| 风险 | 概率 | 如果发生了怎么办 |
|------|------|----------------|
| Beat 2 信号太弱（web退化趋势不显著） | 中 | 转为文献间接证据，Beat 2变成"measurement methodology"而非"empirical finding" |
| Beat 4 实验无显著差异 | 中-高 | 报告null result + 分析原因（数据量、模型规模、评估灵敏度），Beat 5重心转向"structural difference"而非"performance gain" |
| CampusGo数据量不足以做统计分析 | 中 | Beat 5变为"design case study + preliminary metrics"，明确标注需要更大规模验证 |
| L_auth与已有框架重复 | 低 | Phase 3 novelty check会提前发现。如果重复：改为"extending framework X with physical grounding dimension" |
| fine-tune需要GPU但你没有 | 低 | Google Colab Pro ($10)提供T4/A100。或者用Hugging Face Spaces免费tier（有排队） |

---

## 9. 文件清单总汇

你目前手上已经有的文件：
```
已生成：
  research_agent_blueprint.md  — 工具链架构 + 三层检索脚本 + prompt模板 + 12卡点
  api_setup_guide.md           — 每个API的获取步骤 + .env加载代码
  .env.template                — 环境变量模板
  verify_env.py                — 一键连接验证
  .gitignore                   — 防泄露
  complete_execution_manual.md — 从零到产出的7步操作手册

本文档：
  paper_logic_chain.md         — 论文五拍逻辑 + 每一步的agent prompt + 风险备案
```

你还需要创建的：
```
config/seed_papers.json        — 5篇种子论文（手册Step 2.1已给出内容）
config/search_queries.json     — 搜索查询（手册Step 2.2已给出内容）
scripts/phase1_openalex.py     — 从blueprint Step 1.3 Layer 1拆出
scripts/phase1_arxiv.py        — 从blueprint Step 1.3 Layer 3拆出
scripts/phase1_s2_expand.py    — 从blueprint Step 1.3 Layer 2拆出
scripts/phase1_merge.py        — 从blueprint Step 1.3.4拆出
scripts/beat2_metrics.py       — 从本文档Beat 2 prompt实现
scripts/beat4_experiment.py    — 从本文档Beat 4 prompt实现
scripts/beat5_campusgo.py      — 从本文档Beat 5 prompt实现
state.json                     — agent loop初始状态（Phase 7 master prompt定义）
```