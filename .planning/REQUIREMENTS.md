# Requirements: aiDriveUITest v0.4.1

**Defined:** 2026-03-21
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.4.1 Requirements

需求目标：修正断言系统的参数结构，支持三层参数配置。

### Assertion Fields Discovery (字段发现) - Phase 28

- [ ] **FLD-01**: 使用 AST 解析 base_assertions_field.py 中的 param 字典，提取所有字段
- [x] **FLD-02**: API 端点 GET /api/external-assertions/fields 返回字段列表
- [x] **FLD-03**: 字段列表包含 name, path, is_time_field, group, description（从字段名自动生成）

### Frontend Fields Configuration (前端字段配置) - Phase 29

- [ ] **UI-01**: 断言配置弹窗分为三个区域：data 选择、api_params、field_params
- [ ] **UI-02**: field_params 支持按分组浏览、搜索字段（300+ 字段按命名模式分组）
- [ ] **UI-03**: 时间字段值输入有 "now" 快捷按钮（传字符串 "now"，后端处理）
- [ ] **UI-04**: 支持添加/删除多个字段配置

### Assertion Execution (断言执行) - Phase 30

- [ ] **EXEC-01**: execute_assertion_method() 接收三层参数结构 (data, api_params, field_params)
- [ ] **EXEC-02**: 适配层将 field_params 中的 "now" 转换为实际时间字符串
- [ ] **EXEC-03**: 捕获 AssertionError，解析为结构化字段结果 (name, expected, actual, passed)

### End-to-End Verification (端到端验证) - Phase 31

- [ ] **E2E-01**: 完整断言流程测试（配置 → 执行 → 结果展示），使用 Mock ERP
- [ ] **E2E-02**: 测试断言成功和断言失败两种场景

## v0.5.0 Requirements (Deferred)

以下需求推迟到后续版本：

- 断言模板保存/复用
- 断言历史记录查询
- 鉴权机制（当前单用户本地使用）
- 结果持久化存储

## Out of Scope

| Feature | Reason |
|---------|--------|
| 修改 base_assert.py | 使用适配层模式，避免破坏现有功能 |
| 手动补充 300 字段 description | 工作量巨大，使用自动生成 |
| 运行时反射解析字段 | BaseApi 依赖过重，使用 AST 解析 |
| 真实 ERP E2E 测试 | 环境依赖，使用 Mock |

## API Contract

### Request Body (前端 → 后端)

```json
{
  "class_name": "PcAssert",
  "method_name": "attachment_inventory_list_assert",
  "data": "main",
  "api_params": {
    "i": 1,
    "headers": "main"
  },
  "field_params": {
    "statusStr": "已完成",
    "createTime": "now"
  }
}
```

### Response (后端 → 前端)

```json
{
  "success": true,
  "passed": false,
  "duration": 1.23,
  "fields": [
    {"name": "statusStr", "expected": "已完成", "actual": "进行中", "passed": false},
    {"name": "createTime", "expected": "now", "actual": "2026-03-21 10:30:00", "passed": true}
  ]
}
```

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FLD-01 | Phase 28 | Pending |
| FLD-02 | Phase 28 | Complete |
| FLD-03 | Phase 28 | Complete |
| UI-01 | Phase 29 | Pending |
| UI-02 | Phase 29 | Pending |
| UI-03 | Phase 29 | Pending |
| UI-04 | Phase 29 | Pending |
| EXEC-01 | Phase 30 | Pending |
| EXEC-02 | Phase 30 | Pending |
| EXEC-03 | Phase 30 | Pending |
| E2E-01 | Phase 31 | Pending |
| E2E-02 | Phase 31 | Pending |

**Coverage:**
- v0.4.1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-21*
*Last updated: 2026-03-21 after review feedback*
