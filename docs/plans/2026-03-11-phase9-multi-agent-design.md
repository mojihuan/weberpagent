# Phase 9: 多 Agent 协作模式设计文档

> 创建日期: 2026-03-11
> 状态: 已确认，待实施

## 1. 背景与问题

### 1.1 现有问题

SimpleAgent 在处理**复杂表单**时存在以下问题：

| 问题 | 表现 | 根因 |
|------|------|------|
| 循环卡死 | 连续执行 `wait` 动作，无法推进 | 表单字段复杂，单步决策模式无法有效处理 |
| 任务描述模糊 | LLM 不知道该填什么值 | 用户提供的任务描述不够精确 |
| 元素识别困难 | 下拉框、日期选择器、级联选择等复杂组件 | 现有的 click/input 动作粒度太粗 |
| 效率低下 | 一个表单需要 10+ 步才能填完 | 单步执行模式不适合批量操作 |

### 1.2 解决思路

**核心想法**：让 LLM 生成 Playwright 代码片段，一次性完成表单填写

```
传统模式：
  感知 → 决策(click A) → 执行 → 感知 → 决策(input B) → 执行 → ...（循环 10+ 次）

新模式：
  感知 → 决策(生成代码) → 审查 → 执行 → 验证（1 轮完成）
```

---

## 2. 关键设计决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 实现方式 | 分阶段实现（Day 1-5） | 便于验证和调整 |
| LLM 模型 | 可配置切换，默认通义千问 | 复用现有 SDK，集成成本低 |
| 表单数据 | 混合模式（有规则按规则，无规则自由发挥） | 兼顾有效性和灵活性 |
| 沙箱安全 | POC 信任执行 | 简化实现，测试环境可接受 |

---

## 3. 架构设计

### 3.1 整体架构图

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
        │  输入: 截图 + DOM + 任务描述                                       │
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

### 3.2 协作流程

```
Step 1: 代码生成                    Step 2: 代码审查
┌─────────────────────┐            ┌─────────────────────┐
│  CodeGenerator      │            │  CodeReviewer       │
│                     │            │                     │
│  输入:              │    ────►   │  检查项:            │
│  - 页面截图          │            │  1. 代码安全性      │
│  - DOM 元素列表      │            │  2. 选择器有效性    │
│  - 任务描述          │            │  3. 逻辑完整性      │
│                     │            │  4. API 正确性      │
│  输出:              │            │                     │
│  Playwright 代码    │            │  输出:              │
└─────────────────────┘            │  approved: true/false│
                                   └──────────┬──────────┘
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

## 4. 模块详细设计

### 4.1 CodeGenerator Agent

**职责**：根据页面状态和任务描述，生成 Playwright 代码片段

**输入**：
- `screenshot`: 当前页面截图（base64）
- `elements`: DOM 可交互元素列表
- `task_description`: 任务描述

**输出**：`GeneratedCode`
```python
class GeneratedCode(BaseModel):
    code: str           # Playwright async 函数代码
    description: str    # 代码功能描述
    field_values: dict  # 生成的字段值（用于验证）
```

**字段数据生成规则**：

| 字段类型 | 识别规则 | 生成规则 |
|----------|----------|----------|
| 手机号 | label/placeholder 含"手机/电话/tel/phone" | 138 开头 11 位数字 |
| 邮箱 | label/placeholder 含"邮箱/email/mail" | `test_{random}@example.com` |
| 姓名 | label/placeholder 含"姓名/收货人/联系人" | 随机中文姓名 |
| 日期 | type="date" 或含"日期/date" | 今天或未来随机日期 |
| 金额 | 含"金额/价格/price/amount" | 100-10000 随机数 |
| 地址 | 含"地址/address" | 随机省市地址 |
| 其他 | 无规则 | 随机生成合理文本 |

### 4.2 CodeReviewer Agent

**职责**：审查生成的代码是否安全、有效、完整

**检查项**：

| 检查项 | 说明 | 严重级别 |
|--------|------|----------|
| 安全性 | 无危险操作（文件系统、网络请求等） | CRITICAL |
| 选择器有效性 | 选择器与 DOM 元素匹配 | HIGH |
| 逻辑完整性 | 覆盖所有必填字段 | HIGH |
| API 正确性 | Playwright API 使用正确 | MEDIUM |
| 异常处理 | 有适当的等待和异常处理 | LOW |

**输出**：`ReviewResult`
```python
class ReviewResult(BaseModel):
    approved: bool                    # 是否通过审查
    issues: list[ReviewIssue]         # 问题列表
    suggestions: list[str]            # 优化建议
```

### 4.3 CodeOptimizer Agent

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

### 4.4 FormFiller Orchestrator

**职责**：协调三个 Agent 的工作流程

**流程控制**：
```python
async def fill_form(self, state: PageState, task: str) -> FillResult:
    # 1. 生成代码
    generated = await self.code_generator.generate(state, task)

    # 2. 审查循环（最多 3 轮）
    code = generated.code
    for round in range(3):
        review = await self.code_reviewer.review(code, state.elements)
        if review.approved:
            break
        code = await self.code_optimizer.optimize(code, review.issues, state.elements)
    else:
        return FillResult(success=False, error="代码审查未通过")

    # 3. 执行代码
    try:
        await self._execute_code(code, self.page)
    except Exception as e:
        # 执行失败，尝试 1 次优化
        code = await self.code_optimizer.optimize(code, execution_error=str(e))
        await self._execute_code(code, self.page)

    # 4. 验证结果
    screenshot = await self._take_screenshot()
    return FillResult(success=True, screenshot=screenshot, code=code)
```

---

## 5. 主 Agent 集成

### 5.1 复杂表单检测

```python
def _is_complex_form(self, state: PageState) -> bool:
    """检测是否为复杂表单"""
    # 1. 检查元素类型分布
    input_count = sum(1 for e in state.elements if e.tag in ("INPUT", "SELECT", "TEXTAREA"))

    # 2. 检查页面 URL
    is_form_url = any(kw in state.url.lower() for kw in ["form", "add", "edit", "create"])

    # 3. 综合判断
    return input_count >= 3 and is_form_url
```

### 5.2 决策分支

在 `decision.py` 中添加：
```python
async def decide(self, task: str, state: PageState) -> Action:
    if self._is_complex_form(state):
        return Action(
            action="fill_form",
            thought="检测到复杂表单，使用代码生成模式"
        )
    # 原有逻辑...
```

### 5.3 执行分支

在 `executor.py` 中添加：
```python
async def execute(self, action: Action, state: PageState) -> ActionResult:
    if action.action == "fill_form":
        return await self._fill_form_with_code(state)
    # 原有逻辑...
```

---

## 6. 类型定义

### 6.1 新增类型（添加到 `types.py`）

```python
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
    field_values: dict = Field(default_factory=dict, description="生成的字段值")


class ReviewIssue(BaseModel):
    """审查问题"""
    severity: str = Field(description="严重级别: CRITICAL/HIGH/MEDIUM/LOW")
    line: int | None = Field(default=None, description="行号")
    message: str = Field(description="问题描述")


class ReviewResult(BaseModel):
    """代码审查结果"""
    approved: bool = Field(description="是否通过审查")
    issues: list[ReviewIssue] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class FillResult(BaseModel):
    """表单填写结果"""
    success: bool = Field(description="是否成功")
    screenshot: str | None = Field(default=None, description="验证截图路径")
    code: str | None = Field(default=None, description="最终执行的代码")
    error: str | None = Field(default=None, description="错误信息")
```

---

## 7. 文件结构

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

## 8. 实施计划（Day 1-5）

### Day 1: 基础架构
- [ ] 创建 `form_filler/` 目录结构
- [ ] 在 `types.py` 中添加新类型定义
- [ ] 实现 `sandbox.py` 代码执行器
- [ ] 编写子 Agent Prompt 模板

### Day 2: Agent 实现（上）
- [ ] 实现 `code_generator.py`
- [ ] 编写单元测试
- [ ] 验证代码生成质量

### Day 3: Agent 实现（下）
- [ ] 实现 `code_reviewer.py`
- [ ] 实现 `code_optimizer.py`
- [ ] 编写单元测试

### Day 4: 编排器 + 主 Agent 集成
- [ ] 实现 `orchestrator.py`
- [ ] 修改 `decision.py` 支持表单检测
- [ ] 修改 `executor.py` 支持 `fill_form` 动作
- [ ] 集成测试

### Day 5: 场景验证
- [ ] 编写采购单表单测试用例
- [ ] 运行测试并调优
- [ ] 生成测试报告
- [ ] 更新文档

---

## 9. 验收标准

### 功能验收

| 场景 | 成功标准 |
|------|----------|
| 代码生成 | 能根据截图+DOM 生成可执行的 Playwright 代码 |
| 代码审查 | 能检测出选择器无效、API 错误等问题 |
| 代码优化 | 能根据审查意见或执行错误优化代码 |
| 表单填写 | 复杂表单能在 3 轮内完成填写 |

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
| 代码执行安全风险 | 系统受损 | POC 阶段隔离环境 |
| 复杂组件（日期选择器等）难以处理 | 填写失败 | Prompt 中提供 few-shot 示例 |
| 国产模型代码生成能力有限 | 代码质量差 | 可切换 DeepSeek 等代码模型 |
