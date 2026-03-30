# Requirements: aiDriveUITest

**Defined:** 2026-03-30
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.7.0 Requirements

扩展 AI Agent 操作能力边界，覆盖 ERP 测试中表格交互、文件导入、键盘操作和缓存断言等场景。

### Table Interactions (TBL)

- [ ] **TBL-01**: Agent 能定位并点击表格行中的 checkbox 实现单行选择
- [ ] **TBL-02**: Agent 能定位并点击表头的全选 checkbox 实现全选操作
- [ ] **TBL-03**: Agent 能识别并点击表格中的超链接文本（如订单号、物品编号链接）
- [ ] **TBL-04**: Agent 能定位并点击表格行中的图标/操作按钮（编辑、删除、查看等）

### File Import (IMP)

- [ ] **IMP-01**: Agent 能触发文件上传对话框并上传 Excel 文件完成数据导入
- [ ] **IMP-02**: Agent 能触发文件上传并上传图片文件

### Assertion Tuning (AST)

- [ ] **AST-01**: 断言能正确传递 headers 参数并完成接口调用验证
- [ ] **AST-02**: inventory_list_data 的 i(库存状态)、j(物品状态) 参数组合正确传递并返回有效数据

### Keyboard Operations (KB)

- [ ] **KB-01**: Agent 能执行 Ctrl+V 粘贴操作，将剪贴板内容粘贴到输入框
- [ ] **KB-02**: Agent 能在输入框中按回车键触发搜索/确认（如物品编号输入后回车）
- [ ] **KB-03**: Agent 能按 ESC 键关闭弹窗（如日期选择器遮挡时的处理）

### Cache Assertions (CAC)

- [ ] **CAC-01**: 执行用例步骤前能通过查询列表获取物品编号等数据并缓存
- [ ] **CAC-02**: 执行完用例后能用缓存的值进行断言验证（无唯一标识场景）

## Out of Scope

| Feature | Reason |
|---------|--------|
| 拖拽操作 | 当前 ERP 场景不涉及 |
| 多窗口/多标签页操作 | 超出当前操作边界范围 |
| 右键上下文菜单 | 非典型 ERP 操作 |
| 滚动表格翻页 | 已在之前版本验证 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TBL-01 | Phase 53 | Pending |
| TBL-02 | Phase 53 | Pending |
| TBL-03 | Phase 53 | Pending |
| TBL-04 | Phase 53 | Pending |
| IMP-01 | Phase 54 | Pending |
| IMP-02 | Phase 54 | Pending |
| AST-01 | Phase 55 | Pending |
| AST-02 | Phase 55 | Pending |
| KB-01 | Phase 52 | Pending |
| KB-02 | Phase 52 | Pending |
| KB-03 | Phase 52 | Pending |
| CAC-01 | Phase 55 | Pending |
| CAC-02 | Phase 55 | Pending |

**Coverage:**
- v0.7.0 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0

---
*Requirements defined: 2026-03-30*
*Last updated: 2026-03-30 after roadmap creation*
