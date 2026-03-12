# SSE 流实现设计

## 概述

实现真实的 SSE 流式执行监控，支持实时推送 Browser-Use Agent 的执行步骤、截图和和推理过程。

## 技术选型

- **数据库**: SQLite + SQLAlchemy
- **截图存储**: 本地文件 (`backend/data/screenshots/`)
- **SSE 事件格式**: 与前端 mock 格式一致

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                         │
│  ┌─────────────────────────────────────────────────────────────┤
│  database.db (SQLite)    │    routes/runs.py    │    agent_service.py │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POST /api/runs/{run_id}/execute (SSE)          │
│                              │                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                  StreamingResponse (SSE)                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                │
│              ┌───────────────┴────────────────┐                │
│              │   started   │     step       │   finished      │
│              │   (run开始) │   (每步执行)  │   (执行完成)    │
│              └───────────────┴────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## 数据库设计

### tasks 表

```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    target_url TEXT DEFAULT '',
    max_steps INTEGER DEFAULT 10,
    status TEXT DEFAULT 'draft',  -- draft, ready
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### runs 表

```sql
CREATE TABLE runs (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(id),
    status TEXT DEFAULT 'pending',  -- pending, running, success, failed, stopped
    started_at DATETIME,
    finished_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

### steps 表

```sql
CREATE TABLE steps (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES runs(id),
    step_index INTEGER NOT NULL,
    action TEXT NOT NULL,
    reasoning TEXT,
    screenshot_path TEXT,  -- 本地文件路径: data/screenshots/xxx.png
    status TEXT NOT NULL,  -- success, failed
    error TEXT,
    duration_ms INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);
```

## API 端点设计

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/runs` | POST | 创建执行记录 |
| `/api/runs/{run_id}/execute` | POST | SSE 流式执行 |
| `/api/runs/{run_id}/screenshots/{step_index}` | GET | 获取截图 |
| `/api/runs/{run_id}/stop` | POST | 停止执行 |

## SSE 事件格式

### event: started

```json
{
  "event": "started",
  "data": { "run_id": "xxx", "task_name": "登录测试" }
}
```

### event: step

```json
{
  "event": "step",
  "data": {
    "index": 1,
    "action": "点击登录按钮",
    "reasoning": "AI 分析：检测到登录按钮...",
    "screenshot_url": "/api/runs/xxx/screenshots/1",
    "status": "success",
    "duration_ms": 1500
  }
}
```

### event: finished

```json
{
  "event": "finished",
  "data": {
    "status": "success",
    "total_steps": 10,
    "duration_ms": 15000
  }
}
```

### event: error

```json
{
  "event": "error",
  "data": { "error": "错误信息" }
}
```

## 后端文件改动

| 文件 | 描述 |
|------|------|
| `backend/db/__init__.py` | 数据库模块初始化 |
| `backend/db/database.py` | SQLAlchemy 连接配置 |
| `backend/db/models.py` | SQLAlchemy ORM 模型 |
| `backend/db/schemas.py` | Pydantic 请求/响应模型 |
| `backend/db/repository.py` | 数据库操作封装 |
| `backend/core/agent_service.py` | 添加 step_callback 支持 |
| `backend/api/routes/runs.py` | SSE 流式响应、截图 API |
| `backend/api/routes/tasks.py` | 迁移到 SQLite |

## 前端文件改动

| 文件 | 描述 |
|------|------|
| `frontend/src/hooks/useRunStream.ts` | 实现真实 SSE 连接 |
| `frontend/src/api/runs.ts` | 添加 API 调用 |

## 截图存储

- **路径**: `backend/data/screenshots/`
- **命名**: `{run_id}_{step_index}.png`
- **访问**: 通过 `/api/runs/{run_id}/screenshots/{step_index}` 返回

## 实现顺序

1. 数据库层 (SQLite + SQLAlchemy)
2. 后端 Agent Service 回调支持
3. 后端 SSE 路由实现
4. 前端 SSE 连接实现
5. 集成测试
