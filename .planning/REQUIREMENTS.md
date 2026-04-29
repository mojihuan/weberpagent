# Requirements: aiDriveUITest v0.11.0

**Defined:** 2026-04-29
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.11.0 Requirements

代码清理里程碑：删除测试基础设施 + 深度代码质量优化。

### 测试清理

- [x] **TEST-01**: 删除整个 tests/ 目录（所有测试文件、conftest.py、测试数据）
- [x] **TEST-02**: 清理 pyproject.toml / requirements 中的测试依赖（pytest、pytest-asyncio、pytest-timeout、httpx 等）
- [x] **TEST-03**: 清理 pytest 配置（pytest.ini、pyproject.toml 中的 [tool.pytest] 段、VS Code 测试配置）
- [x] **TEST-04**: 清理源代码中仅用于测试的引用（# pytest 标记、test-only helper、mock fixture）

### 死代码清理

- [x] **DEAD-01**: 删除未使用的 import 语句
- [ ] **DEAD-02**: 删除未被调用的函数和方法
- [ ] **DEAD-03**: 删除未引用的变量和常量
- [x] **DEAD-04**: 删除整个文件未被 import 的废弃模块

### 重复逻辑合并

- [ ] **DUP-01**: 识别并合并相同或高度相似的函数
- [ ] **DUP-02**: 合并重复的错误处理模式
- [ ] **DUP-03**: 统一重复的数据转换/序列化逻辑

### 命名规范化

- [ ] **NAME-01**: 统一函数命名风格（snake_case 一致性）
- [ ] **NAME-02**: 统一变量命名（消除缩写歧义，语义化命名）
- [ ] **NAME-03**: 统一文件/模块命名（符合 Python 包命名规范）

### 类型标注

- [ ] **TYPE-01**: 为所有公共函数补全参数和返回值类型标注
- [ ] **TYPE-02**: 为核心数据模型补全字段类型标注
- [ ] **TYPE-03**: 添加 py.typed 标记文件，启用严格类型检查

### 函数/模块优化

- [ ] **FUNC-01**: 拆分过长函数（>50 行）为更小的单一职责函数
- [ ] **FUNC-02**: 重组职责不清晰的模块（高内聚低耦合）
- [ ] **FUNC-03**: 简化复杂的条件逻辑和深层嵌套（>4 层）
- [ ] **FUNC-04**: 统一错误处理模式（消除重复 try-except，统一异常类型）

## Out of Scope

| Feature | Reason |
|---------|--------|
| 大规模架构重构 | 不改变整体系统设计，只做模块内优化 |
| 新功能开发 | 本里程碑仅做清理 |
| 性能优化 | 专注于代码质量，不做性能调优 |
| 服务器部署更新 | 服务器可忽略 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TEST-01 | Phase 120 | Complete |
| TEST-02 | Phase 120 | Complete |
| TEST-03 | Phase 120 | Complete |
| TEST-04 | Phase 120 | Complete |
| DEAD-01 | Phase 121 | Complete |
| DEAD-02 | Phase 121 | Pending |
| DEAD-03 | Phase 121 | Pending |
| DEAD-04 | Phase 121 | Complete |
| DUP-01 | Phase 122 | Pending |
| DUP-02 | Phase 122 | Pending |
| DUP-03 | Phase 122 | Pending |
| NAME-01 | Phase 123 | Pending |
| NAME-02 | Phase 123 | Pending |
| NAME-03 | Phase 123 | Pending |
| TYPE-01 | Phase 123 | Pending |
| TYPE-02 | Phase 123 | Pending |
| TYPE-03 | Phase 123 | Pending |
| FUNC-01 | Phase 124 | Pending |
| FUNC-02 | Phase 124 | Pending |
| FUNC-03 | Phase 124 | Pending |
| FUNC-04 | Phase 124 | Pending |

**Coverage:**
- v0.11.0 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-04-29*
*Last updated: 2026-04-29 after initial definition*
