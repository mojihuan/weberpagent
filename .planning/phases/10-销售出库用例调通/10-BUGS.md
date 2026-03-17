# Phase 10 - 发现的问题

## Issue #0: 销售出库用例需要原生 ERP API (Deferred)

**发现时间:** 2026-03-17
**状态:** 延迟到下一里程碑
**阻塞计划:** 10-03 (API 断言验证), 10-04 (端到端测试)

### 问题描述
销售出库用例需要调用原生 ERP 接口来创建真实数据（订单、库存变动），当前的外部 API 模块（`erp_api`）尚未实现这些功能。

### 根本原因
当前 `erp_api` 模块主要用于验证目的，缺少：
- 创建销售订单的接口
- 执行库存变动的接口
- 与真实 ERP 系统的数据同步

### 解决方案
下一里程碑将实现原生 ERP API 集成，届时：
1. 实现 `erp_api` 模块的真实数据创建接口
2. 重新执行销售出库用例
3. 验证 API 断言功能与真实数据

### 临时方案
- Plan 10-03 改用登录用例验证 API 断言功能
- Plan 10-04 可选择跳过或使用简化场景

---

## Bug #1: 任务详情页 API 缺失 (P1)

**发现时间:** 2026-03-17
**状态:** 待修复

### 问题描述
点击任务卡片后，任务详情页空白，后端报 404 错误。

### 错误日志
```
INFO:     127.0.0.1:57287 - "GET /api/tasks/9b7264eb/runs HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:57288 - "GET /api/tasks/9b7264eb/stats HTTP/1.1" 404 Not Found
```

### 根本原因
后端 `backend/api/routes/tasks.py` 缺少以下 API 端点：
- `GET /tasks/{task_id}/runs` - 获取任务的执行记录列表
- `GET /tasks/{task_id}/stats` - 获取任务的统计数据

### 前端调用位置
`frontend/src/api/tasks.ts`:
```typescript
// Line 53
async getRuns(taskId: string): Promise<Run[]> {
    return apiClient<Run[]>(`/tasks/${taskId}/runs`)
}

// Line 57
async getStats(taskId: string) {
    return apiClient<{ date: string; runs: number; successRate: number }[]>(`/tasks/${taskId}/stats`)
}
```

### 修复方案
在 `backend/api/routes/tasks.py` 添加：

```python
from backend.db.repository import RunRepository

@router.get("/{task_id}/runs", response_model=list[RunResponse])
async def get_task_runs(
    task_id: str,
    repo: RunRepository = Depends(get_run_repo),
):
    return await repo.list_by_task(task_id)

@router.get("/{task_id}/stats")
async def get_task_stats(
    task_id: str,
    repo: RunRepository = Depends(get_run_repo),
):
    # 返回每日统计数据
    return await repo.get_stats_by_task(task_id)
```

需要在 `RunRepository` 中添加：
- `list_by_task(task_id)` 方法
- `get_stats_by_task(task_id)` 方法

### 临时解决方案
- 可以从任务列表页面直接点击"执行"按钮运行任务
- 或者直接通过 API 调用执行任务

---

## Bug #2: target_url 未传递给 Agent (P0 - 阻塞)

**发现时间:** 2026-03-17
**状态:** ✅ 已修复 (2026-03-17)

**修复提交:** 待提交

### 问题描述
Agent 从 `about:blank` 开始执行，而不是从任务配置的 `target_url` 开始。

### 错误日志
```
INFO:     [Agent]   ⚠️ Eval: Waited for page to load but DOM remains empty - about:blank has no content. Verdict: Failure - need URL to proceed.
```

### 根本原因
1. `run_agent_background` 函数签名没有 `target_url` 参数
2. `background_tasks.add_task()` 调用时没有传递 `task.target_url`
3. `agent_service.run_with_cleanup` 没有接收和使用 `target_url`

### 代码位置
`backend/api/routes/runs.py`:
```python
# 第 378-388 行 - 缺少 target_url 传递
background_tasks.add_task(
    run_agent_background,
    run.id,
    task_id,
    task.name,
    task.description,  # task_description
    task.max_steps,
    preconditions,
    api_assertions,
    # 缺少: task.target_url
)
```

### 修复方案 (已实施)

采用简单方案：将 target_url 拼接到任务描述前面，让 Agent 自己导航。

**修改文件:**
1. `backend/api/routes/runs.py` - 添加 target_url 参数传递
2. `backend/core/agent_service.py` - 将 target_url 拼接到任务描述

**实际代码:**
```python
# agent_service.py
if target_url:
    actual_task = f"目标URL: {target_url}\n\n任务:\n{task}"
```

---

---

## Issue #3: erp_api 模块缺少必要函数 (Blocking)

**发现时间:** 2026-03-17
**状态:** 阻塞 - 需要下一里程碑实现
**阻塞计划:** 10-03, 10-04

### 问题描述
`erp_api` 外部模块缺少执行 API 断言所需的函数：
- `get_current_user()` - 获取当前登录用户
- `get_order()` - 获取订单详情
- 其他业务相关函数

### 根本原因
当前 `erp_api` 模块仅作为占位符存在，未实现与真实 ERP 系统的集成。

### 解决方案
下一里程碑需要：
1. 实现完整的 `erp_api` 模块
2. 包含所有业务场景所需的函数
3. 与真实 ERP 系统对接

### 影响
- Phase 10 无法完整验证 API 断言功能
- 销售出库用例无法端到端执行
- 需要延后到 erp_api 模块完成后重新验证

