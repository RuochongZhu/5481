# API Chain Setup

更新时间：2026-04-09（本地）

## 1. 当前这套 research-agent 的真实链路

现在项目不是单一搜索器，而是分层链路：

- `OpenAlex`：Phase 1 主检索骨架
- `Semantic Scholar`：citation intents、recommendations、SPECTER2 enrichment
- `arXiv`：预印本补充
- `Crossref`：canonical identity / DOI / publisher / retraction / license 权威层
- `OpenCitations`：当 S2 不够用时，做 DOI-to-DOI citation fallback
- `Anthropic`：Claude 主抽取与分类大脑
- `OpenAI`：GPT-5.4 reasoning brains，用于图谱分析、矛盾、reviewer 类任务
- `Nomic`：Atlas 可视化或 embedding 云端承载（可选）

一句话就是：

`search backbone -> identity authority -> citation fallback -> reasoning brains`


## 2. 你现在要准备哪些 API

### 必填

- `ANTHROPIC_API_KEY`
  - 没它，Phase 2 之后基本跑不起来。

### 强烈建议

- `OPENALEX_MAILTO`
  - OpenAlex polite pool 标识；建议填真实邮箱。
- `OPENAI_API_KEY`
  - 当前仓库已经支持直接走 OpenAI Platform API，不依赖 ChatGPT 网页。

### 推荐

- `S2_API_KEY`
  - 不填也能部分跑，但 citation / embedding / graph enrichment 会明显变弱。
- `CROSSREF_MAILTO`
  - 建议填真实邮箱。
- `CROSSREF_TOOL_NAME`
  - 填 `research-agent` 即可。

### 可选

- `OPENALEX_API_KEY`
  - 当前代码已预留；有的话更稳。
- `OPENCITATIONS_ACCESS_TOKEN`
  - 用于 citation fallback。
- `NOMIC_API_KEY`
  - 只有你要做 Nomic Atlas 可视化时才需要。
- `CROSSREF_PLUS_API_TOKEN`
  - 只有买了 Metadata Plus 才需要。


## 3. OpenAI 是怎么接的

当前仓库不是“连接 ChatGPT 网页”，而是直接调用 OpenAI 官方 Platform API：

- endpoint: `/v1/responses`
- 默认推理模型：`gpt-5.4`
- 推理强度：`medium / high / xhigh`

这套逻辑现在已经在 [src/api_client.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/src/api_client.py) 里生效，也在 [run_codex_parallel.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/run_codex_parallel.py) 里作为 direct fallback 生效。

也就是说：

- 你填的是 `OPENAI_API_KEY`
- 代码直接调模型
- 不依赖 ChatGPT 对话界面
- 不共享 ChatGPT 历史会话


## 4. ChatGPT 和 OpenAI API 的关系

这两者要分开看：

- `ChatGPT`：产品端订阅
- `OpenAI API`：开发者平台计费

所以你如果想让这个仓库稳定用 GPT-5.4，关键不是 ChatGPT 会员，而是：

- OpenAI Platform 账户可用
- `OPENAI_API_KEY` 可调用 Responses API
- 账户里有 API 额度


## 5. 当前模型大脑划分

### Claude 层

- `MODEL_FAST=claude-sonnet-4-6`
  - 高频、便宜、适合分类与常规抽取
- `MODEL_DEEP=claude-opus-4-6`
  - 低频、贵、适合深抽取

### GPT-5.4 reasoning 层

- `medium`
  - 关系分析、覆盖度类任务
- `high`
  - gap synthesis、narrative、evidence synthesis
- `xhigh`
  - contradiction、honesty、reviewer 级复核


## 6. scite 现在是什么状态

当前仓库还没有正式接入 scite。

所以：

- 你买了 scite 会员，这本身没错
- 但这套代码当前不会自动调用 scite
- 现阶段 scite 更像下一步的 honesty / contradiction 增强层

在没有确认稳定接法前，不建议先在 `.env` 硬造 `SCITE_API_KEY`。


## 7. 推荐填法

直接从 [.env.example](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/.env.example) 复制成 `.env`，然后优先填这些：

1. `ANTHROPIC_API_KEY`
2. `OPENALEX_MAILTO`
3. `OPENAI_API_KEY`
4. `S2_API_KEY`
5. `CROSSREF_MAILTO`
6. `OPENCITATIONS_ACCESS_TOKEN`


## 8. 现在架构层面的结论

这套项目已经不是“只靠 Anthropic 跑一串 prompts”了，而是：

- 检索层有主骨架
- 身份层有 DOI authority
- 图层有 fallback citation source
- 推理层开始做 brain routing

下一步最值得继续补的是：

1. 再次 fresh rerun 一次 Phase 1 -> Phase 3，验证 Crossref/OpenCitations 实际增益
2. 继续把 `scite` 接到 honesty / contradiction 阶段
3. 把 knowledge graph 变成 queryable graph service
