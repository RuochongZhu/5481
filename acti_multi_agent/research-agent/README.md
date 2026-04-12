# Research Agent Pipeline

当前项目的主文档是：

- [CURRENT_STATUS_AND_RECOMMENDATIONS.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/CURRENT_STATUS_AND_RECOMMENDATIONS.md)

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
- [CURRENT_STATUS_AND_RECOMMENDATIONS.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/CURRENT_STATUS_AND_RECOMMENDATIONS.md)
- [RESEARCH_QUESTION.md](/Users/zhuricardo/Desktop/GitHub/5481/acti_multi_agent/research-agent/RESEARCH_QUESTION.md)

## 历史文档

以下文档仍保留，但不再是现行口径：

- `ARCHITECTURE_UPGRADE_NOTES.md`
- `API_CHAIN_SETUP.md`
- `HANDOFF_STATUS_2026-04-09.md`
