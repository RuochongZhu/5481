# Research Agent Pipeline

PhD 选题辅助工具 — 从 2000+ 篇论文中识别 research gaps 并生成 thesis proposals。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API keys（复制 .env 从父目录或手动创建）
# 需要：ANTHROPIC_API_KEY, OPENALEX_MAILTO, S2_API_KEY (可选)

# 3. 查看架构
python main.py --demo

# 4. 运行 pipeline
python main.py --phase 1    # 搜索论文（无需 Anthropic key）
python main.py --phase 2    # 分类论文（需要 Anthropic key）
python main.py --phase 3    # 构建图谱 + gap 分析
python main.py --phase 4    # 生成选题提案

# 5. Codex 交叉验证（独立进程，用本地 codex 配置或 OpenAI fallback）
python run_codex_parallel.py --tasks 3,6
```

## 项目结构

```
research-agent/
├── main.py                    # 主入口
├── run_codex_parallel.py      # Codex 交叉验证（6 个独立任务）
├── .env                       # API keys
├── state.json                 # Pipeline 状态（断点续跑）
├── config/                    # 搜索配置 + 分类定义 + 种子论文
├── src/                       # 9 个模块
│   ├── api_client.py          # OpenAlex + S2 + arXiv + Anthropic
│   ├── phase1_corpus.py       # 3 层搜索 + 去重
│   ├── phase2_extraction.py   # Claude 分类
│   ├── phase3_graph.py        # networkx 图谱 + gap 合成
│   ├── phase4_topics.py       # 选题评分 + thesis 生成
│   ├── prompts.py             # 3 个 agent 的 system prompts
│   └── ...
├── data/
│   ├── raw/                   # API 原始结果 + 手动导入
│   └── processed/             # corpus_unified.json, classified.json
├── analysis/                  # gaps_ranked.json, graph_metrics.json
└── output/                    # thesis_proposals.md, gap_analysis_report.md
```

## 核心功能

### Phase 1: 3 层搜索（无需 Anthropic key）
- **Layer 1**: OpenAlex 批量搜索（10 queries × 300 papers）
- **Layer 2**: Semantic Scholar 引用链扩展（5 seed papers）
- **Layer 3**: arXiv 最新预印本（5 queries）
- 去重：DOI 优先 + 标题 Jaccard > 0.8
- 输出：~2300 篇论文

### Phase 2: Claude 分类
- 按相关性过滤到 ~300 篇
- 批量分类（10 papers/call）到 A-G 类别
- 输出：~200 篇分类论文

### Phase 3: 图谱 + Gap 分析
- networkx 构建引用图
- 7×7 类别交叉矩阵
- Gap Synthesizer agent 识别 top 10 gaps
- 输出：gaps_ranked.json

### Phase 4: 选题生成
- 5 维评分（novelty, feasibility, advisor, CampusGo, publication）
- Top 3 生成 thesis statement + proposal sketch
- 输出：thesis_proposals.md

### Codex 交叉验证
6 个独立任务，用 `codex exec` 或 OpenAI API fallback：
1. **classification_audit** — 审计分类质量
2. **gap_novelty_check** — 验证 gap 新颖性
3. **campusgo_honesty_check** — 独立评估 CampusGo 相关性
4. **methodology_feasibility** — PhD 可行性评估
5. **intersection_validation** — 验证类别交叉矩阵
6. **alternative_gaps** — 生成 pipeline 遗漏的 gaps

## 使用场景

### 场景 1: 首次运行
```bash
python main.py --phase 1    # 搜索 ~2300 篇论文（~10 分钟）
python main.py --phase 2    # 分类 ~300 篇（~5 分钟，30 API calls）
python main.py --phase 3    # 图谱 + gap 分析（~2 分钟）
python main.py --phase 4    # 生成选题（~2 分钟）
```

### 场景 2: 导入 Undermind/Elicit 导出
```bash
# 把 CSV/BibTeX 放到 data/raw/
python main.py --import-file ~/Downloads/undermind_export.csv
# 删除 state.json 重跑 Phase 1，或手动合并
```

### 场景 3: 只重跑分类 + 分析（保留论文库）
```bash
# 修改 config/categories.json 或 src/prompts.py
python -c "
import json
with open('state.json') as f: s = json.load(f)
for p in ['2','3','4']:
    s['phases'][p]['status'] = 'pending'
    for step in s['phases'][p]['steps']:
        s['phases'][p]['steps'][step]['status'] = 'pending'
with open('state.json','w') as f: json.dump(s,f,indent=2)
"
python main.py --phase 2
python main.py --phase 3
python main.py --phase 4
```

### 场景 4: Codex 交叉验证
```bash
# 跑完 Phase 1-4 后
python run_codex_parallel.py --tasks 3,6    # CampusGo 诚实检查 + 替代 gaps
python run_codex_parallel.py                # 全部 6 个任务
```

## 配置

### .env 文件
```bash
# Anthropic (Phase 2-4)
ANTHROPIC_API_KEY=sk-ant-api03-...

# OpenAlex polite pool (Phase 1)
OPENALEX_MAILTO=your@cornell.edu

# Semantic Scholar (Phase 1, 可选，提速 10x)
S2_API_KEY=...

# OpenAI (Codex fallback, 可选)
OPENAI_API_KEY=sk-proj-...
```

### 搜索配置 (config/search_queries.json)
```json
{
  "queries": [
    {"query": "model collapse synthetic data", "max_pages": 3},
    {"query": "authentic data collection platform", "max_pages": 2}
  ],
  "arxiv_queries": [
    "all:\"model collapse\" AND all:\"training data\""
  ]
}
```

### 分类定义 (config/categories.json)
7 个类别：A (Model Collapse Theory), B (Synthetic Data Detection), C (Data Provenance), D (Information Theory), E (Platform Design), F (Mitigation), G (Empirical Measurement)

## 输出

### thesis_proposals.md
Top 3 选题，每个包含：
- Weighted score (5 维)
- Thesis statement
- 3-paragraph proposal sketch
- Methodology outline
- Conversation partners (相关论文)

### gap_analysis_report.md
10 个 research gaps，每个包含：
- Research question
- Bridges categories
- Feasibility + CampusGo relevance
- Score

### gaps_ranked.json
完整 gap 数据（JSON 格式，可编程处理）

## 注意事项

1. **Phase 1 无需 Anthropic key** — 只用免费 API（OpenAlex, S2, arXiv）
2. **断点续跑** — state.json 记录进度，崩溃后 `--resume` 继续
3. **Codex fallback** — 如果 `~/.codex/config.toml` 的 proxy 挂了，自动用 OPENAI_API_KEY 直连
4. **CampusGo 相关性** — Gap Synthesizer 已更新，明确 CampusGo 是 web/mobile app，不是 IoT/federated learning
5. **成本估算** — Phase 2-4 约 30-40 API calls，~$1-2（Sonnet 4）

## 故障排查

```bash
# 查看状态
python main.py --status

# 查看日志
tail -f agent_logs/run_*.log

# 重置某个 phase
python -c "
import json
with open('state.json') as f: s = json.load(f)
s['phases']['2']['status'] = 'pending'
with open('state.json','w') as f: json.dump(s,f,indent=2)
"

# 清理缓存
rm -rf __pycache__ src/__pycache__
```
