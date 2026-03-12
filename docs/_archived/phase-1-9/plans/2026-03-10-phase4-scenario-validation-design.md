# Phase 4: 场景验证设计文档

> 创建日期: 2026-03-10
> 状态: 待实施

## 1. 概述

Phase 4 的目标是验证自研简化版 Agent 在真实业务场景中的表现，测试 AI 决策 + Playwright 执行的技术闭环。

### 验证场景

| 场景 | 描述 | 复杂度 |
|------|------|--------|
| 登录 | 打开页面 → 输入账号密码 → 登录成功 | 简单 |
| 新增采购单 | 登录 → 导航 → 填表单 → 提交 → 验证 | 复杂 |

### 测试目标

- ERP 系统: `https://erptest.epbox.cn/`
- 测试账号: `Y96230027`
- 测试密码: `Aa123456`

## 2. 项目结构

```
backend/tests/
├── conftest.py              # pytest fixtures（浏览器、LLM、配置）
├── test_login_e2e.py        # 登录场景测试（新建）
├── test_purchase_e2e.py     # 新增采购单场景测试（新建）
└── run_phase4.py            # 批量运行 + 统计报告（新建）
```

## 3. 测试配置

更新 `backend/config/test_targets.yaml`：

```yaml
# 基础 URL
base_url: "https://erptest.epbox.cn/"

# 登录场景配置
login:
  url: "/"
  account: "Y96230027"
  password: "Aa123456"
  success_indicators:
    - "商品采购"
    - "采购管理"
    - "欢迎"

# 新增采购单场景配置
purchase:
  # 导航路径
  navigation:
    - "商品采购"
    - "采购管理"
    - "新增采购单"
  # 新增按钮
  add_button: "新增"
  # 设备类型选项
  device_types:
    - "手机"
    - "平板电脑"
    - "笔记本电脑"
    - "智能手表"
  # 成功标志
  success_indicator: "记录出现在列表中"
```

## 4. 测试用例设计

### 4.1 登录场景 (`test_login_e2e.py`)

```python
async def test_login_e2e():
    """端到端登录测试"""
    task = """
    在 ERP 系统执行登录操作：
    1. 打开 https://erptest.epbox.cn/
    2. 在账号输入框输入 Y96230027
    3. 在密码输入框输入 Aa123456
    4. 点击登录按钮
    5. 确认登录成功（检测"商品采购"或"欢迎"等元素）
    """
    # 预期：5 步内完成，成功率 > 90%
```

### 4.2 新增采购单场景 (`test_purchase_e2e.py`)

```python
async def test_purchase_e2e():
    """端到端新增采购单测试"""
    task = """
    在 ERP 系统完成新增采购单操作：
    1. 登录系统（账号 Y96230027，密码 Aa123456）
    2. 点击侧边栏"商品采购"
    3. 点击"采购管理"
    4. 点击"新增采购单"
    5. 点击"新增"按钮
    6. 选择设备类型"手机"
    7. 填写表单必填字段（自由发挥）
    8. 提交表单
    9. 确认成功（按钮下方出现新记录）
    """
    # 预期：20 步内完成，成功率 > 60%
```

## 5. 统计报告模块

### 5.1 数据结构

```python
@dataclass
class TestResult:
    scenario: str           # 场景名称
    success: bool           # 是否成功
    steps: int              # 执行步数
    duration: float         # 耗时（秒）
    error: str | None       # 错误信息
    screenshots: list[str]  # 截图路径列表
```

### 5.2 报告输出格式

```
========== Phase 4 测试报告 ==========

场景              成功    步数    耗时
─────────────────────────────────────
登录场景           ✅      4      12.3s
新增采购单         ✅     15      45.2s
─────────────────────────────────────
总计通过率: 100% (2/2)
平均步数: 9.5
平均耗时: 28.8s
```

### 5.3 JSON 报告

```json
{
  "phase": "Phase 4",
  "date": "2026-03-10",
  "results": [
    {
      "scenario": "login",
      "success": true,
      "steps": 4,
      "duration": 12.3,
      "error": null
    },
    {
      "scenario": "purchase",
      "success": true,
      "steps": 15,
      "duration": 45.2,
      "error": null
    }
  ],
  "summary": {
    "total": 2,
    "passed": 2,
    "failed": 0,
    "pass_rate": 1.0,
    "avg_steps": 9.5,
    "avg_duration": 28.8
  }
}
```

## 6. 验收标准

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **场景通过率** | ≥ 80% (2/2 通过) | 2 个场景全部成功 |
| **单步推理耗时** | ≤ 10s | 每步 AI 决策时间 |
| **登录场景步数** | ≤ 5 步 | 打开页面 + 输入账号 + 输入密码 + 登录 |
| **采购单步数** | ≤ 20 步 | 导航 + 填表 + 提交 |
| **自愈成功率** | ≥ 50% | 失败后能通过反思重试恢复 |
| **截图完整率** | 100% | 每步都有截图记录 |

## 7. 实施计划

```
Phase 4: 场景验证（预计 2-3 天）
├── 4.1 更新测试配置 (test_targets.yaml)
├── 4.2 创建 pytest fixtures (conftest.py)
├── 4.3 编写登录场景测试 (test_login_e2e.py)
├── 4.4 编写采购单场景测试 (test_purchase_e2e.py)
├── 4.5 实现统计报告模块 (run_phase4.py)
└── 4.6 运行测试并生成报告
```

## 8. 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| ERP 系统不稳定 | 中 | 高 | 准备备用测试时间，多次重试 |
| 表单结构复杂 | 高 | 中 | AI 自由发挥，不强制特定字段 |
| 网络延迟 | 低 | 中 | 增加等待时间，使用 headless=False 便于调试 |
| 模型 API 限流 | 低 | 中 | 在请求间增加延迟 |

## 9. 后续工作

Phase 4 完成后：
- Phase 5: 总结与复盘
  - 整理测试报告
  - 分析失败原因
  - 输出 POC 结论和后续建议
