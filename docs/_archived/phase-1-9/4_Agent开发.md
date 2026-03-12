# AI Agent 多 Agent 协作模式开发计划

## 0. 任务进度概览

### Phase 9: 多 Agent 协作模式（3-5 天）🔄

- [ ] 9.1 基础架构设计
- [ ] 9.2 CodeGenerator Agent 实现
- [ ] 9.3 CodeReviewer Agent 实现
- [ ] 9.4 CodeOptimizer Agent 实现
- [ ] 9.5 FormFiller Orchestrator 实现
- [ ] 9.6 主 Agent 集成
- [ ] 9.7 场景验证测试

### 里程碑

- [ ] M8: 多 Agent 协作完成 - 复杂表单场景验证通过

---

## 1. 背景与问题

### 1.1 现有问题

在 Phase 6-8 的测试中，发现 SimpleAgent 在处理**复杂表单**时存在以下问题：

| 问题 | 表现 | 根因 |
|------|------|------|
| **循环卡死** | 连续执行 `wait` 动作，无法推进 | 表单字段复杂，单步决策模式无法有效处理 |
| **任务描述模糊** | LLM 不知道该填什么值 | 用户提供的任务描述不够精确 |
| **元素识别困难** | 下拉框、日期选择器、级联选择等复杂组件 | 现有的 click/input 动作粒度太粗 |
| **效率低下** | 一个表单需要 10+ 步才能填完 | 单步执行模式不适合批量操作 |

### 1.2 解决思路

**核心想法**：让 LLM 生成 Playwright 代码片段，一次性完成表单填写

```
传统模式：
  感知 → 决策(click A) → 执行 → 感知 → 决策(input B) → 执行 → ...（循环 10+ 次）

新模式：
  感知 → 决策(生成代码) → 审查 → 执行 → 验证（1 轮完成）
```

---

## 2. 架构设计

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SimpleAgent (主控)                              │
│                                                                              │
│  1. 感知页面 (截图 + DOM)                                                     │
│  2. 决策：普通动作 OR 复杂表单？                                               │
│                                                                              │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────────┐
              │       决策分支                      │
              │                                     │
              │  普通动作 ───────────────────────────────────────┐
              │  (click/input/wait)                               │
              │                                                   ▼
              │  复杂表单 ──────┐                      ┌──────────────────┐
              │                 │                      │   Executor       │
              │                 │                      │   (现有模块)      │
              └─────────────────┼──────────────────────└──────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────────────────────────┐
        │                    FormFiller Orchestrator                        │
        │                    (表单填写编排器)                                │
        │                                                                   │
        │  输入: 截图 + DOM + 任务描述 + 表单数据                            │
        │  输出: 填写结果 + 验证截图                                         │
        │                                                                   │
        └───────────────────────────────┬───────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
        ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
        │  CodeGenerator   │  │  CodeReviewer    │  │  CodeOptimizer   │
        │  代码生成 Agent  │  │  代码审查 Agent  │  │  代码优化 Agent  │
        └──────────────────┘  └──────────────────┘  └──────────────────┘
```

### 2.2 协作流程图

```
Step 1: 代码生成                    Step 2: 代码审查
┌─────────────────────┐            ┌─────────────────────┐
│  CodeGenerator      │            │  CodeReviewer       │
│                     │            │                     │
│  输入:              │            │  检查项:            │
│  - 页面截图          │    ────►   │  1. 代码安全性      │
│  - DOM 元素列表      │            │  2. 选择器有效性    │
│  - 任务描述          │            │  3. 逻辑完整性      │
│  - 表单数据          │            │  4. API 正确性      │
│                     │            │                     │
│  输出:              │            │  输出:              │
│  Playwright 代码    │            │  approved: true/false│
└─────────────────────┘            └──────────┬──────────┘
                                             │
                                   ┌─────────┴─────────┐
                                   │                   │
                               approved=true      approved=false
                                   │                   │
                                   ▼                   ▼
Step 3: 执行代码              ┌─────────────────────────┐
┌─────────────────┐           │  CodeOptimizer          │
│  exec(code)     │           │                         │
│  或 sandbox     │           │  输入:                   │
└────────┬────────┘           │  - 原代码               │
         │                    │  - 审查问题             │
    ┌────┴────┐               │  - DOM 元素             │
    │         │               │                         │
  成功      失败              │  输出:                   │
    │         │               │  优化后的代码           │
    │         └──────────────►│                         │
    │                         └────────────┬────────────┘
    │                                      │
    │                                      │ (返回 Step 2)
    ▼
Step 4: 验证结果
┌─────────────────────────────────────────────────────────────┐
│  截图 + 视觉检查                                              │
│                                                              │
│  - 检查必填字段是否已填写                                     │
│  - 检查是否有错误提示                                         │
│  - 返回验证结果给主 Agent                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 模块详细设计

### 3.1 CodeGenerator Agent（代码生成）

**职责**：根据页面状态和任务描述，生成 Playwright 代码片段

**输入**：
- `screenshot`: 当前页面截图
- `elements`: DOM 可交互元素列表
- `task_description`: 任务描述（含表单数据）
- `form_fields`: 表单字段要求（可选）

**输出**：
```python
# 生成的 Playwright 代码片段
async def fill_form(page):
    # 填写收货人
    await page.get_by_placeholder("请输入收货人").fill("张三")
    # 填写电话
    await page.get_by_placeholder("请输入电话").fill("13800138000")
    # 选择省份
    await page.locator(".province-select").click()
    await page.get_by_text("北京市").click()
    # ...
```

**Prompt 模板**：
```
你是一个 Playwright 自动化代码生成专家。

## 当前任务
{task_description}

## 页面截图
[截图]

## 可交互元素
{elements}

## 表单数据
{form_data}

## 要求
1. 使用 Playwright API（page.get_by_*、page.locator 等）
2. 优先使用 placeholder、label、role 定位
3. 处理下拉框、日期选择器等复杂组件
4. 生成可直接执行的 async 函数代码

## 输出格式
直接输出 Python 代码，不要包裹在 ```python 中
```

### 3.2 CodeReviewer Agent（代码审查）

**职责**：审查生成的代码是否安全、有效、完整

**检查项**：
| 检查项 | 说明 | 严重级别 |
|--------|------|----------|
| **安全性** | 无危险操作（文件系统、网络请求等） | CRITICAL |
| **选择器有效性** | 选择器与 DOM 元素匹配 | HIGH |
| **逻辑完整性** | 覆盖所有必填字段 | HIGH |
| **API 正确性** | Playwright API 使用正确 | MEDIUM |
| **异常处理** | 有适当的等待和异常处理 | LOW |

**输出**：
```json
{
  "approved": false,
  "issues": [
    {
      "severity": "HIGH",
      "line": 3,
      "message": "选择器 '.province-select' 在 DOM 中不存在"
    }
  ],
  "suggestions": [
    "建议使用 get_by_role('combobox', name='省份') 替代 CSS 选择器"
  ]
}
```

### 3.3 CodeOptimizer Agent（代码优化）

**职责**：根据审查意见或执行错误，优化代码

**输入**：
- `original_code`: 原始代码
- `issues`: 审查问题列表（可选）
- `execution_error`: 执行错误信息（可选）
- `elements`: DOM 元素列表

**输出**：优化后的 Playwright 代码

**优化策略**：
1. **选择器替换**：根据审查建议替换无效选择器
2. **错误修复**：根据执行错误调整代码
3. **备选方案**：提供多种定位策略

### 3.4 FormFiller Orchestrator（编排器）

**职责**：协调三个 Agent 的工作流程

**流程控制**：
```python
async def fill_form(self, state: PageState, task: str) -> FillResult:
    # 1. 生成代码
    code = await self.code_generator.generate(state, task)

    # 2. 审查循环（最多 3 轮）
    for round in range(3):
        review = await self.code_reviewer.review(code, state.elements)

        if review.approved:
            break

        # 优化代码
        code = await self.code_optimizer.optimize(
            code, review.issues, state.elements
        )
    else:
        return FillResult(success=False, error="代码审查未通过")

    # 3. 执行代码
    try:
        await self._execute_code(code)
    except Exception as e:
        # 执行失败，尝试优化
        code = await self.code_optimizer.optimize(
            code, execution_error=str(e), elements=state.elements
        )
        await self._execute_code(code)

    # 4. 验证结果
    screenshot = await self._take_screenshot()
    verification = await self._verify_form(screenshot, task)

    return FillResult(
        success=verification.success,
        screenshot=screenshot,
        issues=verification.issues
    )
```

---

## 4. 主 Agent 集成

### 4.1 决策分支

在 `SimpleAgent.decide()` 中添加表单检测逻辑：

```python
async def decide(self, task: str, state: PageState) -> Action:
    # 检测是否为复杂表单场景
    if self._is_complex_form(state):
        return Action(
            action="fill_form",  # 新增动作类型
            target=None,
            value=None,
            metadata={"use_code_generation": True}
        )

    # 原有逻辑
    return await self._normal_decide(task, state)

def _is_complex_form(self, state: PageState) -> bool:
    """检测是否为复杂表单"""
    # 1. 检查元素类型分布
    input_count = sum(1 for e in state.elements if e.tag == "INPUT")
    select_count = sum(1 for e in state.elements if e.tag == "SELECT")

    # 2. 检查页面 URL
    is_form_url = "form" in state.url or "add" in state.url

    # 3. 综合判断
    return input_count >= 3 and is_form_url
```

### 4.2 执行分支

在 `Executor.execute()` 中添加 `fill_form` 处理：

```python
async def execute(self, action: Action, elements: list) -> ActionResult:
    if action.action == "fill_form":
        return await self._fill_form_with_code(action, elements)
    # ... 原有逻辑
```

---

## 5. 类型定义

### 5.1 新增类型

```python
# types.py

class ActionType(str, Enum):
    NAVIGATE = "navigate"
    CLICK = "click"
    INPUT = "input"
    WAIT = "wait"
    DONE = "done"
    FILL_FORM = "fill_form"  # 新增

class GeneratedCode(BaseModel):
    """生成的代码"""
    code: str = Field(description="Playwright 代码片段")
    description: str = Field(description="代码功能描述")

class ReviewResult(BaseModel):
    """代码审查结果"""
    approved: bool = Field(description="是否通过审查")
    issues: list[ReviewIssue] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)

class ReviewIssue(BaseModel):
    """审查问题"""
    severity: str = Field(description="严重级别: CRITICAL/HIGH/MEDIUM/LOW")
    line: int | None = Field(description="行号")
    message: str = Field(description="问题描述")

class FillResult(BaseModel):
    """表单填写结果"""
    success: bool = Field(description="是否成功")
    screenshot: str | None = Field(description="验证截图路径")
    issues: list[str] = Field(default_factory=list, description="剩余问题")
    code: str | None = Field(description="最终执行的代码")
```

---

## 6. 文件结构

```
backend/agent_simple/
├── __init__.py
├── agent.py              # 主 Agent（添加 fill_form 决策）
├── perception.py         # 感知模块（不变）
├── decision.py           # 决策模块（添加表单检测）
├── executor.py           # 执行模块（添加 fill_form 执行）
├── prompts.py            # Prompt 模板（不变）
├── types.py              # 类型定义（添加新类型）
│
├── form_filler/          # 新增：表单填写子模块
│   ├── __init__.py
│   ├── orchestrator.py   # FormFiller 编排器
│   ├── code_generator.py # CodeGenerator Agent
│   ├── code_reviewer.py  # CodeReviewer Agent
│   ├── code_optimizer.py # CodeOptimizer Agent
│   ├── prompts.py        # 子 Agent Prompt 模板
│   └── sandbox.py        # 代码沙箱执行器
```

---

## 7. 安全考虑

### 7.1 POC 阶段（当前）

- **完全信任**：直接 `exec()` 执行生成的代码
- **风险接受**：仅用于开发测试环境

### 7.2 生产阶段（未来）

- **白名单机制**：只允许特定 Playwright API
- **沙箱隔离**：使用 RestrictedPython 或类似工具
- **代码签名**：验证代码来源

```python
# 白名单示例
ALLOWED_APIS = {
    "page.fill",
    "page.click",
    "page.select_option",
    "page.type",
    "page.press",
    "page.check",
    "page.uncheck",
    "page.locator",
    "page.get_by_text",
    "page.get_by_placeholder",
    "page.get_by_role",
    "page.get_by_label",
    "page.wait_for_selector",
    "page.wait_for_timeout",
}
```

---

## 8. 实施计划

### Phase 9: 多 Agent 协作模式（3-5 天）

```
Day 1: 基础架构
├── 9.1.1 创建 form_filler 目录结构
├── 9.1.2 定义新类型（GeneratedCode, ReviewResult 等）
├── 9.1.3 实现 sandbox.py 基础执行器
└── 9.1.4 编写 CodeGenerator Prompt 模板

Day 2: Agent 实现
├── 9.2.1 实现 CodeGenerator Agent
├── 9.2.2 实现 CodeReviewer Agent
├── 9.2.3 编写单元测试
└── 9.2.4 验证生成/审查流程

Day 3: 完善协作
├── 9.3.1 实现 CodeOptimizer Agent
├── 9.3.2 实现 FormFiller Orchestrator
├── 9.3.3 添加审查-优化循环
└── 9.3.4 添加执行错误恢复

Day 4: 主 Agent 集成
├── 9.4.1 添加 _is_complex_form 检测
├── 9.4.2 修改 Executor 支持 fill_form
├── 9.4.3 添加验证截图逻辑
└── 9.4.4 集成测试

Day 5: 场景验证
├── 9.5.1 编写采购单表单测试
├── 9.5.2 运行测试并调优
├── 9.5.3 生成测试报告
└── 9.5.4 更新文档
```

### 任务清单

- [ ] 9.1 基础架构设计
  - [ ] 9.1.1 创建 `backend/agent_simple/form_filler/` 目录
  - [ ] 9.1.2 在 `types.py` 中添加新类型定义
  - [ ] 9.1.3 实现 `sandbox.py` 代码执行器
  - [ ] 9.1.4 编写子 Agent Prompt 模板

- [ ] 9.2 CodeGenerator Agent 实现
  - [ ] 9.2.1 实现 `code_generator.py`
  - [ ] 9.2.2 编写单元测试
  - [ ] 9.2.3 验证代码生成质量

- [ ] 9.3 CodeReviewer Agent 实现
  - [ ] 9.3.1 实现 `code_reviewer.py`
  - [ ] 9.3.2 编写单元测试
  - [ ] 9.3.3 验证审查准确性

- [ ] 9.4 CodeOptimizer Agent 实现
  - [ ] 9.4.1 实现 `code_optimizer.py`
  - [ ] 9.4.2 编写单元测试
  - [ ] 9.4.3 验证优化效果

- [ ] 9.5 FormFiller Orchestrator 实现
  - [ ] 9.5.1 实现 `orchestrator.py`
  - [ ] 9.5.2 实现审查-优化循环
  - [ ] 9.5.3 实现执行错误恢复
  - [ ] 9.5.4 编写单元测试

- [ ] 9.6 主 Agent 集成
  - [ ] 9.6.1 添加 `_is_complex_form()` 检测
  - [ ] 9.6.2 修改 `decision.py` 支持表单决策
  - [ ] 9.6.3 修改 `executor.py` 支持 `fill_form` 动作
  - [ ] 9.6.4 添加验证截图逻辑
  - [ ] 9.6.5 集成测试

- [ ] 9.7 场景验证测试
  - [ ] 9.7.1 编写采购单表单测试用例
  - [ ] 9.7.2 运行测试并调优
  - [ ] 9.7.3 生成测试报告
  - [ ] 9.7.4 更新文档

---

## 9. 验收标准

### 功能验收

| 场景 | 成功标准 |
|------|----------|
| **代码生成** | 能根据截图+DOM 生成可执行的 Playwright 代码 |
| **代码审查** | 能检测出选择器无效、API 错误等问题 |
| **代码优化** | 能根据审查意见或执行错误优化代码 |
| **表单填写** | 复杂表单能在 3 轮内完成填写 |

### 性能指标

| 指标 | 目标值 |
|------|--------|
| 代码生成耗时 | ≤ 15s |
| 代码审查耗时 | ≤ 5s |
| 表单填写成功率 | ≥ 80% |
| 代码一次通过率 | ≥ 50% |

---

## 10. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| LLM 生成的代码质量不稳定 | 执行失败 | 多轮审查-优化循环 |
| 代码执行安全风险 | 系统受损 | POC 阶段隔离环境，生产阶段白名单 |
| 复杂组件（日期选择器等）难以处理 | 填写失败 | 提供 few-shot 示例 |
| 国产模型代码生成能力有限 | 代码质量差 | 使用 DeepSeek-Coder 等代码模型 |

---

## 11. 后续扩展

### 短期（POC 完成后）

1. **白名单沙箱**：限制可执行的 API
2. **代码缓存**：相似表单复用已验证的代码
3. **人工确认模式**：生成代码后展示给用户确认

### 长期（产品化）

1. **代码模板库**：常见表单的标准化模板
2. **自学习机制**：根据执行结果自动优化 Prompt
3. **多语言支持**：生成 Cypress、Selenium 等代码
