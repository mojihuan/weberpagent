# Phase 22: Bug Fix Sprint - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

修复 Phase 20-21 测试阶段发现的所有 bug，并通过回归测试验证。

**Scope:**
- 修复 16 个过时测试（测试代码与当前 API 不匹配）
- 归档 18 个遗留测试文件（导入已删除模块）
- 修复 Phase 20 延后的 9 个 Low 级别 UI/功能 bug
- 全量回归测试验证

**Out of Scope:**
- 新功能开发
- 性能优化
- 架构重构

**依赖:**
- Phase 20 (E2E Testing + Manual Verification) - 已发现并记录 bug
- Phase 21 (Unit Test Coverage) - 已建立测试基准

</domain>

<decisions>
## Implementation Decisions

### 实施顺序
- **测试优先**: 先修复测试代码确保回归测试可用，再修复产品 bug
- **理由**: 没有健康的测试套件，无法验证 bug 修复的正确性

### 测试修复策略

#### 失败测试修复 (16个)
1. **test_external_bridge.py** (7个失败)
   - 问题: 测试期望 `WEBSERP_PATH` 未配置时返回空结果，但环境已配置
   - 修复: 使用 mock 或环境变量清理确保测试隔离

2. **test_browser_cleanup.py** (2个失败)
   - 问题: API 签名已更改（增加了 `target_url` 和 `task_id` 参数）
   - 修复: 更新 mock 参数匹配新签名

3. **test_config** (5个失败)
   - 问题: 测试假设 WEBSERP_PATH 为 None，但环境已配置
   - 修复: 使用 monkeypatch 或 fixture 清理环境

4. **test_precondition_service.py** (1个失败)
   - 问题: 复杂前置条件测试与桥接模块集成问题
   - 修复: 更新测试以匹配当前桥接行为

#### 遗留测试文件归档 (18个)
- **处理方式**: 移动到 `backend/tests/_archived/` 目录
- **文件列表**:
  - test_agent.py
  - test_agent_optimized.py
  - test_code_generator.py
  - test_code_optimizer.py
  - test_code_reviewer.py
  - test_dashboard_api.py
  - test_decision.py
  - test_delivery_form.py
  - test_executor.py
  - test_form_filler_integration.py
  - test_login_e2e.py
  - test_memory.py
  - test_memory_integration.py
  - test_orchestrator.py
  - test_perception.py
  - test_phase5_unit.py
  - test_purchase_e2e.py
  - test_sandbox.py
- **原因**: 这些文件导入 `backend.agent_simple` 等已删除模块

### Low Bug 修复范围

#### DataMethodSelector UI 问题 (5个)
1. **#1**: 方法列表未按类分组显示
   - 当前: 长滚动列表
   - 目标: 折叠的类分组（如 "BaseParams"、"OtherParams"）

2. **#2**: 已选择方法不在底部汇总区域显示
   - 当前: 底部汇总区域不显示已选方法
   - 目标: 显示已选方法列表

3. **#3**: 已选择的方法数量显示不正确
   - 当前: 显示数量与实际选择不符
   - 目标: 正确显示选中数量

4. **#4**: 参数配置步骤不显示参数类型提示
   - 当前: 参数输入项旁边没有显示类型
   - 目标: 显示 "integer"、"string" 等类型提示

5. **#6**: 参数输入无类型校验
   - 当前: 所有参数都可以输入任何内容
   - 目标: 数字字段只允许数字输入

#### 代码生成与交互 (3个)
6. **#9**: 默认值带引号导致执行失败
   - 当前: 字符串参数默认值显示为 `'main'`（带引号）
   - 目标: 去除多余引号

7. **#10**: 生成代码缺少 import 语句
   - 当前: 只有 `context.get_data()` 调用
   - 目标: 包含必要的 import 语句（如需要）

8. **#11**: Escape 键无法关闭模态框
   - 当前: 按 Escape 无响应
   - 目标: Escape 键关闭 DataMethodSelector 模态框

#### 报告展示问题 (1个)
9. **#15**: 报告页面缺少前置条件执行信息
   - **需添加元素**:
     - 前置条件状态区（执行状态 + 耗时）
     - 变量展示区（变量名 + 变量值）
     - 详情展开选项（可展开查看详细日志）

### 回归测试范围
- **全量测试**: 所有单元测试 + API 测试 + E2E 测试
- **通过标准**: 所有测试通过，无新增失败用例

### Claude's Discretion
- 具体测试修复的实现细节
- UI 组件的具体实现方式
- 报告页面布局设计
- 归档目录的命名和位置

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 测试修复参考
- `backend/tests/unit/test_external_bridge.py` — 需要修复的 7 个测试
- `backend/tests/unit/test_browser_cleanup.py` — 需要修复的 2 个测试
- `backend/tests/unit/test_config/` — 需要修复的配置测试
- `backend/tests/unit/test_precondition_service.py` — 需要修复的桥接集成测试

### Bug 修复参考
- `frontend/src/components/TaskModal/DataMethodSelector.tsx` — DataMethodSelector 组件 (#1, #2, #3, #4, #6, #9, #11)
- `frontend/src/components/TaskModal/TaskForm.tsx` — 代码生成逻辑 (#10)
- `frontend/src/pages/ReportPage.tsx` — 报告页面 (#15)
- `backend/api/routes/runs.py` — 执行结果数据结构

### 前置阶段参考
- `.planning/phases/20-e2e-testing-manual-verification/20-VERIFICATION.md` — Bug 列表和详细描述
- `.planning/phases/20-e2e-testing-manual-verification/20-CONTEXT.md` — E2E 测试上下文
- `.planning/phases/21-unit-test-coverage/21-VERIFICATION.md` — 单元测试验证结果

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `is_available()` — 检查 WEBSERP_PATH 配置状态
  - `get_operations_grouped()` — 获取操作码分组
  - `get_data_methods_grouped()` — 获取数据方法分组
- `frontend/src/components/TaskModal/DataMethodSelector.tsx`:
  - 4 步向导组件
  - 方法选择、参数配置、预览提取、确认生成
- `e2e/tests/` — E2E 测试模式参考

### Established Patterns
- **测试隔离**: 使用 `monkeypatch` 或 `mock.patch` 清理环境变量
- **UI 组件**: React + Tailwind CSS，使用 Ant Design 组件库
- **模态框交互**: 使用 Ant Design Modal 组件
- **报告展示**: 使用折叠面板展示详细信息

### Integration Points
- DataMethodSelector 与 TaskForm 集成（代码生成）
- 报告页面与执行结果 API 集成
- 测试套件与 CI/CD 集成（未来）

### 已知技术债务
- Pydantic v2 迁移警告（schemas.py 中的 class-based config）
- 自定义 pytest mark 警告（level1, level2, level3）

</code_context>

<specifics>
## Specific Ideas

- 测试修复应使用 `monkeypatch.setenv` 和 `monkeypatch.delenv` 确保环境隔离
- DataMethodSelector 类分组可使用 Ant Design Collapse 组件
- 报告页面前置条件区可复用现有的 CollapsibleSection 组件
- 归档测试文件时保留 README 说明归档原因

</specifics>

<deferred>
## Deferred Ideas

- CI 集成覆盖率门槛 — 后续版本
- Pydantic v2 迁移 — 后续版本
- 自定义 pytest mark 注册 — 后续版本

</deferred>

---
*Phase: 22-bug-fix-sprint*
*Context gathered: 2026-03-19*
