# Seismic Intel Hub (localhost app)

一个本地运行的地震情报看板，基于 **USGS Earthquake Catalog API**，支持筛选、可视化和后续扩展到更多数据源。

## 快速启动

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m app.main
```

打开：`http://127.0.0.1:8000`

## Deploy to DigitalOcean App Platform

部署前请确认：

- 应用监听 `0.0.0.0` 和环境变量 `PORT`（`app/main.py` 已支持）
- 根目录包含 `Procfile`（本仓库已提供）
- `requirements.txt` 包含 `gunicorn`（本仓库已提供）

建议在 DO 的 Health Check Path 配置为：`/api/v1/health`

本地模拟生产启动：

```bash
gunicorn --bind 0.0.0.0:${PORT:-8080} app.main:app
```

## Lab: AI Reporter Script (Submission)

本仓库已包含一个“API -> 数据处理 -> AI -> 写入文件”的完整脚本：`lab_ai_reporter.py`。

运行步骤：

1) 启动本地 API（提供 `/api/v1/earthquakes`）：

```bash
python3 -m app.main
```

2) 配置本地 AI：

- Ollama（本地）：确保 Ollama 正在运行（可选 `OLLAMA_HOST` / `OLLAMA_MODEL`，默认 `llama3.2:1b`）

3) 生成报告（会写入 `reports/`）：

```bash
python3 lab_ai_reporter.py
```

## 功能亮点

- 酷炫玻璃态 + 霓虹风格 dashboard（fancy UI）
- 实时调用 USGS 数据（无需 API Key）
- 筛选项：时间区间、最小震级、返回数量
- 三类可视化：震级分布、时间趋势、全球散点（经纬度）
- 结构可扩展：`app/providers/` 下可新增其他 API provider

## 项目结构

- `app/main.py`：Flask 服务与 API 路由
- `app/providers/base.py`：provider 抽象接口
- `app/providers/usgs.py`：USGS 数据适配层
- `app/providers/factory.py`：provider 注册与切换
- `static/`：前端页面、样式、图表逻辑

## API Submission Content (English, no table)

1. API Name:
USGS Earthquake Catalog API

2. Official Documentation URL:
https://earthquake.usgs.gov/fdsnws/event/1/

3. Does it require an API key:
No API key required (free public access).

Key information from documentation:
- Base URL: https://earthquake.usgs.gov/fdsnws/event/1/query
- Authentication: None
- Request format: GET request with URL query parameters
- Response formats: GeoJSON, CSV, XML, and others
- Common parameters: starttime, endtime, minmagnitude, limit, format

Why this API:
- It is fully free to use.
- No registration and no API key are required.
- It returns rich multi-row real-world data (earthquake records).
- It is reliable for building analysis/reporting features and easy to integrate.

## Posit Connect 部署

本项目可直接以 Flask API 部署到 Posit Connect，入口为 `app.main:app`。

详细步骤见：`POSIT_CONNECT_DEPLOY.md`

开发/测试依赖建议单独安装：

```bash
pip install -r requirements-dev.txt
```
