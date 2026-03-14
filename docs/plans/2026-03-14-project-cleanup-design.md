# 项目结构整理设计

## 概述

将项目根目录中与前端、后端、agent 无关的内容移入 `backup/` 文件夹，实现项目结构规整。

## 目标

- 清理根目录，只保留核心代码和必要配置
- 分类整理非核心内容到 backup 文件夹
- backup 文件夹不纳入 git 跟踪

## 整理后的目录结构

```
weberpagent/
├── backup/
│   ├── archives/              # 归档内容
│   │   ├── 工时/
│   │   ├── 测试案例/
│   │   ├── jianzhi_ui_test.egg-info/
│   │   ├── backend_archived/  # 原 backend/_archived/
│   │   └── docs_archived/     # 原 docs/_archived/
│   ├── runtime-data/          # 运行时数据
│   │   ├── outputs/
│   │   └── data/
│   └── temp/                  # 临时文件
│       ├── debug_memoryview_error.py
│       ├── test_backend_env.py
│       ├── login.log
│       └── .pytest_cache/
├── backend/
├── frontend/
├── docs/
├── .playwright-mcp/
├── .claude/
├── .venv/
├── .git/
├── .env
├── .env.example
├── .gitignore
├── .mcp.json
├── CLAUDE.md
├── pyproject.toml
└── uv.lock
```

## 移动操作清单

| 源位置 | 目标位置 |
|--------|----------|
| `工时/` | `backup/archives/工时/` |
| `测试案例/` | `backup/archives/测试案例/` |
| `jianzhi_ui_test.egg-info/` | `backup/archives/jianzhi_ui_test.egg-info/` |
| `backend/_archived/` | `backup/archives/backend_archived/` |
| `docs/_archived/` | `backup/archives/docs_archived/` |
| `outputs/` | `backup/runtime-data/outputs/` |
| `data/` | `backup/runtime-data/data/` |
| `debug_memoryview_error.py` | `backup/temp/` |
| `test_backend_env.py` | `backup/temp/` |
| `login.log` | `backup/temp/` |
| `.pytest_cache/` | `backup/temp/.pytest_cache/` |

## Git 操作

1. 创建 backup 目录结构
2. 移动所有文件到 backup
3. 使用 `git rm --cached -r` 停止跟踪 backup 文件夹
4. 更新 `.gitignore`，添加 `backup/`

## 注意事项

- 保留 `.playwright-mcp/` 和 `.claude/` 目录
- backup 文件夹完全从 git 跟踪中移除
- 移动操作保留文件历史
