# Requirements: aiDriveUITest

**Defined:** 2026-03-17
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告
## v0.2.1 Requirements (Partially Complete - Blocked)

本里程碑目标是调通核心测试用例的端到端执行。
### 登录用例
- [x] **LOGN-01**: 用户可以在前端创建登录测试任务（4 步骤)
- [x] **LOGN-02**: 登录用例可以端到端执行成功
- [x] **LOGN-03**: 执行结果在报告中正确展示
### 销售出库用例
- [ ] **SALE-01**: 用户可以在前端配置前置条件 `self.pre.operations(data=['FA1', 'HC1'])`
- [x] **SALE-02**: 用户可以在步骤中使用动态数据方法 `self.copy()` 和 `self.affix()`
- [x] **SALE-03**: 用户可以在步骤中使用随机数方法 `self.sf`
- [ ] **SALE-04**: 用户可以配置 API 断言验证销售单号、状态、时间
- [ ] **SALE-05**: 销售出库用例可以端到端执行成功
- [ ] **SALE-06**: 前置条件执行结果正确传递到测试步骤中
- [ ] **SALE-07**: API 断言结果在报告中正确展示
### Bug 修复
- [ ] **BUGS-01**: 调通过程中发现的执行引擎 Bug 已修复
- [ ] **BUGS-02**: 调通过程中发现的前端 Bug 已修复
### 文档指南
- [ ] **DOCS-01**: 提供登录用例的前端填写指南
- [ ] **DOCS-02**: 提供销售出库用例的前端填写指南（含前置条件、动态数据、断言配置）
## v0.3 Requirements (Current Milestone)
**Goal:** 将 webseleniumerp 项目的 base_prerequisites.py 集成到当前平台
### 配置 (CONFIG)
- [x] **CONFIG-01**: 用户可以在 .env 中配置 WEBSERP_PATH 指向 webseleniumerp 项目路径
- [x] **CONFIG-02**: 系统启动时验证 WEBSERP_PATH 路径有效性
- [x] **CONFIG-03**: 提供 webseleniumerp 的 config/settings.py 模板文档
### 后端桥接模块 (BRIDGE)
- [x] **BRIDGE-01**: 创建 ExternalPreconditionBridge 模块，隔离外部项目导入
- [x] **BRIDGE-02**: 实现 get_available_operations() 返回操作码列表及描述
- [ ] **BRIDGE-03**: 提供 `/api/external-operations` API 端点
- [ ] **BRIDGE-04**: 实现操作码执行功能，与现有 PreconditionService 集成
### 前端集成 (FRONTEND)
- [ ] **FRONT-01**: 前置条件编辑器中添加操作码选择器组件
- [ ] **FRONT-02**: 操作码按模块分组显示 (配件、财务、运营、平台等)
- [ ] **FRONT-03**: 支持多选操作码
- [ ] **FRONT-04**: 选中操作码后自动生成 Python 代码模板
### 验证 (VALIDATE)
- [ ] **VAL-01**: 完整流程测试： 选择操作码 → 执行前置条件 → 查看结果
- [ ] **VAL-02**: 错误处理： 外部项目缺失、配置错误、执行失败
## v0.4 Requirements (Deferred)
推迟到后续版本：
### 批量执行
- **BATCH-01**: Excel 导入测试用例
- **BATCH-02**: 批量运行测试用例
- **BATCH-03**: 批量执行结果汇总
## Out of Scope
| Feature | Reason |
|---------|--------|
| 用户认证/权限管理 | 单用户本地使用 |
| 服务器部署 | 只需本地开发环境运行 |
| 多语言支持 | 只支持中文 |
| 修改 webseleniumerp 项目代码 | 只读取，不修改外部项目 |
## Traceability
| Requirement | Phase | Status |
|-------------|-------|--------|
| CONFIG-01 | Phase 13 | Complete |
| CONFIG-02 | Phase 13 | Complete |
| CONFIG-03 | Phase 13 | Complete |
| BRIDGE-01 | Phase 14 | Complete |
| BRIDGE-02 | Phase 14 | Complete |
| BRIDGE-03 | Phase 14 | Pending |
| BRIDGE-04 | Phase 14 | Pending |
| FRONT-01 | Phase 15 | Pending |
| FRONT-02 | Phase 15 | Pending |
| FRONT-03 | Phase 15 | Pending |
| FRONT-04 | Phase 15 | Pending |
| VAL-01 | Phase 16 | Pending |
| VAL-02 | Phase 16 | Pending |
**Coverage:**
- v0.3 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓
---
*Requirements defined: 2026-03-17*
*Last updated: 2026-03-17 after v0.3 milestone definition*
