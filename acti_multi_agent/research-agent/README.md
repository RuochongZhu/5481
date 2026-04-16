# Research Agent Pipeline

当前项目的主文档是：

- [CURRENT_STATUS_AND_RECOMMENDATIONS.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/CURRENT_STATUS_AND_RECOMMENDATIONS.md)

如果 `README` 与主文档冲突，以主文档为准。

## 当前定位

这个仓库当前不是“自动选题机”。
它的当前定位是：

- 为既定 thesis 收集和组织文献证据
- 构建 canonical identity layer 与 knowledge graph
- 支持 5-beat evidence chain 的 narrative / contradiction / evidence outputs

## 当前已验证状态

截至 2026-04-09 本地复跑后，已验证完成：

- Phase `1`
- Phase `2`
- Phase `2.5`
- Phase `3`

尚未在本轮重新验证：

- Phase `3.5`
- Phase `3.7`
- Phase `3.8`
- Phase `4`
- Phase `5`

## 最小使用方式

优先使用项目自带虚拟环境：

```bash
./.venv/bin/python main.py --status
./.venv/bin/python main.py --phase 1
./.venv/bin/python main.py --phase 2
./.venv/bin/python main.py --phase 2.5
./.venv/bin/python main.py --phase 3
```

如果 `.venv` 不存在，再自行创建环境并安装依赖：

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## 关键文件

- [main.py](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/main.py)
- [state.json](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/state.json)
- [CURRENT_STATUS_AND_RECOMMENDATIONS.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/CURRENT_STATUS_AND_RECOMMENDATIONS.md)
- [RESEARCH_QUESTION.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/RESEARCH_QUESTION.md)

## 目录结构

- `src/`: 核心管线实现
- `config/`: 检索、分类、人工覆盖配置
- `data/`: 原始数据、解析数据、处理产物、PDF
- `analysis/`: 当前轮分析 JSON
- `output/`: 当前轮可读产物
- `archive/`: 历史快照与分轮归档
- `agent_logs/`: 运行日志
- `docs/`: 项目说明、研究问题、历史 handoff 文档
- `scripts/`: 本地辅助脚本

## 文档入口

- 当前主文档: [CURRENT_STATUS_AND_RECOMMENDATIONS.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/CURRENT_STATUS_AND_RECOMMENDATIONS.md)
- 研究问题: [RESEARCH_QUESTION.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/RESEARCH_QUESTION.md)
- 管线说明: [PIPELINE_EXPLAINER_FOR_PAPER_USE.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/PIPELINE_EXPLAINER_FOR_PAPER_USE.md)
- 文档索引: [docs/README.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/docs/README.md)

## 历史文档

以下文档仍保留，但不再是现行口径：

- `docs/ARCHITECTURE_UPGRADE_NOTES.md`
- `docs/API_CHAIN_SETUP.md`
- `docs/HANDOFF_STATUS_2026-04-09.md`
