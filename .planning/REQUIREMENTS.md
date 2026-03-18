# Requirements: aiDriveUITest v0.3.1

**Defined:** 2026-03-18
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v1 Requirements (v0.3.1)

数据获取方法集成需求，支持从 webseleniumerp 的 base_params.py 获取查询数据并传递给测试步骤。

### 后端

- [x] **DATA-01**: 扫描 base_params.py 获取所有 `xxx_data()` 方法的签名和参数信息
- [x] **DATA-02**: 提供数据获取方法列表 API（按模块分组，包含方法描述）
- [x] **DATA-03**: 执行数据获取方法并返回 JSON 结果

### 前端

- [ ] **UI-01**: DataMethodSelector 组件（复用 OperationCodeSelector 的模块分组模式）
- [ ] **UI-02**: 参数配置表单（动态生成 i/j/k 等参数输入框）
- [ ] **UI-03**: 字段提取路径配置（支持 `[0].imei` 语法）
- [ ] **UI-04**: 变量命名配置（生成变量赋值代码）

### 集成

- [ ] **INT-01**: 前置条件代码生成（将数据获取代码注入前置条件块）
- [ ] **INT-02**: context 变量存储（数据获取结果存入执行上下文）
- [ ] **INT-03**: Jinja2 变量替换（测试步骤中使用 `{{imei}}` 引用）

## v2 Requirements (Future)

推迟到后续版本的需求。

- **INT-04**: 支持链式数据获取（一个方法的输出作为另一个方法的输入）
- **UI-05**: 数据预览功能（执行前预览获取的数据）
- **DATA-04**: 数据缓存机制（避免重复查询）

## Out of Scope

明确排除的功能和原因。

| Feature | Reason |
|---------|--------|
| 数据修改方法 | 只支持查询类 xxx_data() 方法，不支持写入操作 |
| 自定义 Python 代码 | 数据获取通过 UI 配置，不开放自由代码编辑 |
| 跨任务数据共享 | 数据仅在当前任务执行上下文有效 |

## Traceability

需求到阶段的映射。

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 17 | Complete |
| DATA-02 | Phase 17 | Complete |
| DATA-03 | Phase 17 | Complete |
| UI-01 | Phase 18 | Pending |
| UI-02 | Phase 18 | Pending |
| UI-03 | Phase 18 | Pending |
| UI-04 | Phase 18 | Pending |
| INT-01 | Phase 19 | Pending |
| INT-02 | Phase 19 | Pending |
| INT-03 | Phase 19 | Pending |

**Coverage:**
- v1 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0

## 用例示例

```
前置条件配置:
1. 选择数据获取方法: inventory_list_data (库存|库存列表)
2. 配置参数: i=2, j=13
3. 配置提取路径: [0].imei
4. 配置变量名: imei

生成的前置条件代码:
```python
imei = context.get_data('inventory_list_data', i=2, j=13)[0]['imei']
```

测试步骤:
"输入 {{imei}} 到 IMEI 输入框"
```

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-18 - v0.3.1 roadmap created, traceability updated*
