# Phase 35: 文档完善 - Research

**Researched:** 2026-03-23
**Domain:** Technical Documentation / Assertion System Usage Guide
**Confidence:** HIGH

## Summary

Phase 35 为断言系统编写用户文档。断言系统是 aiDriveUITest 平台的核心验证功能，允许 QA 测试人员配置三层参数来验证业务数据。文档需要覆盖完整的工作流程（从前端配置到执行到报告查看）、三层参数详解、以及常见问题解答。

**Primary recommendation:** 创建 `docs/断言系统使用指南.md`，采用示例驱动的方式，以销售出库断言为典型案例，清晰说明三层参数（api_params/field_params/params）的配置方式。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 受众 = 两者兼顾（QA + 开发人员）
  - QA 部分：简单易懂的步骤说明
  - 开发部分：API 参考和数据结构说明
- **D-02:** 文档位置 = **`docs/断言系统使用指南.md`**
- **D-03:** 文档形式 = **纯 Markdown**（文字说明 + 代码块示例，暂不包含截图）
- **D-04:** 主要章节 = **三个核心部分**
  1. 完整工作流程（从前端配置到执行到查看结果）
  2. 三层参数详解（api_params/field_params/params）
  3. 报告解读（如何理解断言结果）
- **D-05:** 开发者内容 = **基础 API 参考和数据结构**
- **D-06:** 讲解风格 = **示例驱动**
- **D-07:** 示例场景 = **销售出库断言**（`sell_sale_item_list_assert`）
- **D-08:** FAQ 范围 = **预防性 FAQ**（常见错误和解决方案）
- **D-09:** FAQ 深度 = **精简版（5-8 个问题）**

### Claude's Discretion
- 具体文档的排版和措辞
- FAQ 问题的选择和解答方式
- 代码示例的详细程度

### Deferred Ideas (OUT OF SCOPE)
- 含截图的详细教程 — 后续版本考虑
- 前端应用内嵌帮助文档 — 未来需求
- 完整故障排查指南 — 后续版本考虑
- 多场景示例（库存、采购等） — 后续版本考虑

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOC-01 | 记录断言系统的使用方式（如何配置三层参数） | 三层参数详解、前端配置流程、代码示例 |
| DOC-02 | 记录常见问题和注意事项 | FAQ 部分、常见错误、解决方案 |
</phase_requirements>

## Standard Stack

### Core
| Library/Tool | Version | Purpose | Why Standard |
|--------------|---------|---------|--------------|
| Markdown | N/A | 文档格式 | 项目现有文档标准，与 `docs/测试步骤.md` 保持一致 |
| TypeScript types | N/A | 数据结构参考 | `frontend/src/types/index.ts` 提供准确的类型定义 |

### Supporting
| Library/Tool | Purpose | When to Use |
|--------------|---------|-------------|
| `docs/测试步骤.md` | 参考文档 | 销售出库断言示例模板 |
| `external_precondition_bridge.py` | 后端实现参考 | 理解三层参数处理逻辑 |
| `FieldParamsEditor.tsx` | 前端 UI 参考 | 描述配置界面操作 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 纯 Markdown | Docusaurus/VuePress | 静态站点生成器需要额外配置，当前阶段纯 Markdown 更简洁 |
| 单一受众文档 | 分离 QA/开发文档 | 分离会增加维护成本，当前用户规模适合合并文档 |

## Architecture Patterns

### Recommended Document Structure

```
docs/
├── 断言系统使用指南.md    # 本 Phase 创建
├── 测试步骤.md            # 现有参考
└── README.md              # 现有文档导航
```

### Pattern 1: 示例驱动文档结构

**What:** 以具体用例演示每个参数的作用
**When to use:** 讲解三层参数、配置流程时
**Example:**

```markdown
## 三层参数详解

以销售出库断言 `sell_sale_item_list_assert` 为例：

### 第一层：API 参数 (api_params)
用于控制 API 查询条件...

### 第二层：字段参数 (field_params)
用于指定要验证的字段和期望值...

### 第三层：通用参数 (params)
向后兼容的参数层...
```

### Pattern 2: FAQ 结构

**What:** 问题 - 原因 - 解决方案 三段式
**When to use:** 记录常见问题
**Example:**

```markdown
### Q: 断言失败但数据看起来正确？

**原因:** 时间参数使用了固定值而非 "now"

**解决方案:** 使用时间预设如 `now-1m` 或 `now-5m`...
```

### Anti-Patterns to Avoid
- **无示例的纯概念解释:** 用户难以理解抽象描述
- **过于技术化的术语:** QA 用户可能不熟悉
- **过长的代码块:** 应拆分为可理解的小段

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 文档站点 | 自定义 HTML 站点 | 纯 Markdown | 项目已有 docs/ 目录结构 |
| 类型定义文档 | 手写类型说明 | 引用 types/index.ts | 保证准确性，减少维护成本 |
| 代码示例 | 虚构的示例 | 基于真实代码 | 与实际实现保持一致 |

**Key insight:** 文档应基于现有代码和实现，而非虚构场景。

## Common Pitfalls

### Pitfall 1: 三层参数混淆

**What goes wrong:** 用户不清楚 api_params、field_params、params 的区别
**Why it happens:** 三个参数层功能相似但用途不同
**How to avoid:** 用表格明确对比三层的用途

| 参数层 | 用途 | 示例 |
|--------|------|------|
| api_params | API 查询条件 | `salesOrder: 'SA'` |
| field_params | 字段验证 | `saleTime: 'now'` |
| params | 向后兼容 | 旧参数格式 |

**Warning signs:** 用户配置了错误层级的参数

### Pitfall 2: 时间参数使用固定值

**What goes wrong:** 断言因时间不匹配而失败
**Why it happens:** 用户输入具体时间而非 "now" 表达式
**How to avoid:** 文档明确说明时间预设的使用方式

支持的时间预设：
- `now` - 当前时间
- `now-1m` - 1 分钟前
- `now-5m` - 5 分钟前
- `now-1h` - 1 小时前
- `now-1d` - 1 天前

### Pitfall 3: Headers 选择错误

**What goes wrong:** 使用了错误的登录身份导致数据查询失败
**Why it happens:** 不理解 headers 代表登录账号/身份
**How to avoid:** 说明各 headers 选项的含义

可用 Headers：
- `main` - 主账号
- `idle` - 闲置账号
- `vice` - 副账号
- `special` - 特殊账号
- `super` - 超级账号
- `camera` - 相机账号
- `platform` - 平台账号

### Pitfall 4: 字段参数未填写期望值

**What goes wrong:** 选中字段但未填写期望值，断言无法执行
**Why it happens:** UI 允许选中字段但期望值为空
**How to avoid:** 提示用户必须为选中的字段填写期望值

## Code Examples

### 销售出库断言配置示例

```typescript
// 断言配置结构 (AssertionConfig)
const assertionConfig = {
  className: 'PcAssert',
  methodName: 'sell_sale_item_list_assert',
  headers: 'main',           // 使用主账号登录
  data: 'main',              // 使用主数据源
  api_params: {
    salesOrder: 'SA',        // 销售单号前缀
    articlesStateStr: '已销售' // 物品状态
  },
  field_params: {
    saleTime: 'now-1m'       // 销售时间：1分钟前
  }
}
```

### 时间参数转换逻辑

```python
# Source: backend/core/external_precondition_bridge.py
# "now" 值转换为格式化时间字符串

def _convert_now_values(kwargs: dict) -> dict:
    """将 'now' 值转换为 YYYY-MM-DD HH:mm:ss 格式

    支持格式:
    - 'now' -> 当前时间
    - 'now-2m' -> 2分钟前
    - 'now+5m' -> 5分钟后
    - 'now-1h' -> 1小时前
    """
    result = {}
    for key, value in kwargs.items():
        if _is_time_field(key) and isinstance(value, str) and value.startswith('now'):
            # 解析并计算时间偏移
            ...
            result[key] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            result[key] = value
    return result
```

### 断言执行结果结构

```typescript
// 断言执行结果 (来自 execute_assertion_method)
interface AssertionExecutionResult {
  success: boolean      // 执行是否成功（无异常）
  passed: boolean       // 断言是否通过
  fields: FieldResult[] // 字段级验证结果
  error: string | null  // 错误信息
  error_type: string | null  // 错误类型
  duration: number      // 执行耗时（秒）
}

interface FieldResult {
  name: string          // 字段名
  expected: string      // 期望值
  actual: string        // 实际值
  passed: boolean       // 是否通过
  comparison_type: 'equals' | 'contains'  // 比较类型
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Python 代码字符串配置 | 结构化 JSON 配置 | Phase 28-30 | 更安全、更易维护 |
| 单层参数 | 三层参数（api_params/field_params/params） | Phase 30 | 更清晰的参数分层 |
| 固定时间值 | "now" 表达式 | Phase 30 | 动态时间支持 |

**Deprecated/outdated:**
- `params` 作为主要参数层：应优先使用 `api_params` 和 `field_params`
- 硬编码时间值：应使用 `now` 表达式

## Open Questions

1. **是否需要英文版文档？**
   - What we know: 当前用户为中文 QA 团队
   - What's unclear: 未来是否需要国际化支持
   - Recommendation: 先只做中文版，如有需求再翻译

2. **FAQ 是否需要链接到详细排查指南？**
   - What we know: D-09 限定为精简版（5-8 个问题）
   - What's unclear: 复杂问题如何处理
   - Recommendation: FAQ 中提供简要解答，复杂问题标记为"后续版本详细指南"

## Validation Architecture

> nyquist_validation: true (enabled in .planning/config.json)

### Test Framework
| Property | Value |
|----------|-------|
| Framework | 无（文档验证为人工审阅） |
| Config file | N/A |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| DOC-01 | 断言系统使用文档已创建 | Manual Review | `cat docs/断言系统使用指南.md` | N/A - Wave 0 |
| DOC-02 | 常见问题已记录 | Manual Review | `grep "## FAQ" docs/断言系统使用指南.md` | N/A - Wave 0 |

### Sampling Rate
- **Per task commit:** 无自动化测试
- **Per wave merge:** 人工审阅文档内容
- **Phase gate:** 文档完成且内容覆盖三个核心部分

### Wave 0 Gaps
- [ ] `docs/断言系统使用指南.md` — 主文档文件
- [ ] 人工审阅检查清单 — 确保覆盖所有决策点

*(文档验证依赖人工审阅，非自动化测试)*

## Sources

### Primary (HIGH confidence)
- `.planning/phases/35-文档完善/35-CONTEXT.md` - 用户决策和约束
- `backend/core/external_precondition_bridge.py` - 断言执行实现
- `frontend/src/types/index.ts` - TypeScript 类型定义

### Secondary (MEDIUM confidence)
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx` - 字段配置 UI
- `frontend/src/components/TaskModal/AssertionSelector.tsx` - 断言选择器 UI
- `frontend/src/pages/ReportDetail.tsx` - 报告展示
- `docs/测试步骤.md` - 现有文档格式参考

### Tertiary (LOW confidence)
- 无

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 基于项目现有结构
- Architecture: HIGH - 基于已实现的代码
- Pitfalls: HIGH - 来自 Phase 33-34 的实际验证经验

**Research date:** 2026-03-23
**Valid until:** 长期有效（文档结构稳定，除非系统架构变更）
