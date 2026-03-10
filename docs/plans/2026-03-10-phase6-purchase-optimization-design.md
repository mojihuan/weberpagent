# Phase 6 设计：采购表单测试与优化

> 设计日期： 2026-03-10
> 維护者： Claude

## 1. 背景

> 绯兔
</system_message>
</environment_details>
</task>
<plan>
# 背景

Phase 4 场景验证中，采购单场景超过 25 步仍未完成。Phase 5 针对 Agent 进行了全面优化（ Prompt、执行层、感知层、反思层），登录场景已验证成功（8 步完成）。

</details>
</step>
<step>
<type>text</type>
<text>
现在需要针对采购单场景进行优化验证。
</text>
</step>
<step>
<type>text</type>
<text>
## 2. 目标
</text>
</step>
<step>
<type>text</type>
<text>
让采购单场景**连续 2 次运行通过**，验证 Agent 的稳定性。
</text>
</step>
<step>
<type>text</type>
<text>
### 成功标准
</text>
</step>
<step>
<type>text</type>
<text>
- 采购单场景完成步数 ≤ 25
- 无错误中断
- **连续 2 次运行都通过**
</text>
</step>
<step>
<type>text</type>
<text>
## 3. 核心任务
</text>
</step>
<step>
<type>text</type>
<text>
| 任务 | 说明 | 状态 |
|------|------|------|
| 6.1 分析失败原因 | 分析 Phase 4 采购单场景的详细日志，找出具体失败点 | 待开始 |
| 6.2 Prompt 优化 | 领域特定 Prompt 增强（侧边栏导航、表单填写指导） | 待开始 |
| 6.3 运行测试 | 运行采购单场景测试 | 待开始 |
| 6.4 验证稳定性 | 第二次运行测试，验证连续通过 | 待开始 |
| 6.5 生成报告 | 输出 Phase 6 测试报告 | 待开始 |
</text>
</step>
<step>
<type>text</type>
<text>
## 4. 技术设计
</text>
</step>
<step>
<type>text</type>
<text>
### 4.1 迭代策略
</text>
</step>
<step>
<type>text</type>
<text>
采用"先简后繁"策略：
</text>
</step>
<step>
<type>text</type>
<text>
**第 1 轮**: Prompt 优化 + 运行测试
</text>
</step>
<step>
<type>text</type>
<text>
- 优化 `prompts.py` 中的系统提示词
- 添加侧边栏导航指导
- 添加表单填写指导
- 运行测试，记录结果
</text>
</step>
<step>
<type>text</type>
<text>
**第 2 轮**: 再次运行测试（验证稳定性)
</text>
</step>
<step>
<type>text</type>
<text>
- 如果第 1 轮通过，直接运行第二次
- 如果第 1 轮失败，分析原因：
  - Prompt 问题 → 调整 Prompt，重试
  - 执行问题 → 考虑执行层优化
</text>
</step>
<step>
<type>text</type>
<text>
**第 3 轮**: 针对性修复 + 最终测试
</text>
</step>
<step>
<type>text</type>
<text>
- 仅在必要时使用
- 针对第 1-2 轮发现的具体问题进行修复
</text>
</step>
<step>
<type>text</type>
<text>
### 4.2 Prompt 优化要点
</text>
</step>
<step>
<type>text</type>
<text>
**侧边栏导航**:
</text>
</step>
<step>
<type>text</type>
<text>
```text
# 侧边栏导航规则
- 侧边栏通常位于页面左侧
- 点击侧边栏菜单项展开子菜单
- 如果菜单已展开，再次点击会收起（注意判断）
- 多级菜单需要逐级点击（如： 采购管理 → 采购订单 → 新增）
```
</text>
</step>
<step>
<type>text</type>
<text>
**表单填写**:
</text>
</step>
<step>
<type>text</type>
<text>
```text
# 表单填写规则
- 先识别必填字段（通常有 * 标记）
- 下拉选择器： 点击展开选项，点击选项
- 日期选择器： 点击打开日历，选择日期
- 文本输入框： 直接输入内容
- 提交前检查表单是否填写完整
```
</text>
</step>
<step>
<type>text</type>
<text>
### 4.3 测试配置
</text>
</step>
<step>
<type>text</type>
<text>
复用 Phase 4 的测试配置:
</text>
</step>
<step>
<type>text</type>
<text>
- `backend/config/test_targets.yaml` - 测试目标配置
- `backend/tests/conftest.py` - pytest fixtures
- `backend/tests/test_purchase_e2e.py` - 采购单测试用例
</text>
</step>
<step>
<type>text</type>
<text>
### 4.4 输出目录
</text>
</step>
<step>
<type>text</type>
<text>
```
outputs/tests/phase6/
├── run1/                    # 第 1 轮测试
│   ├── screenshots/        # 截图
│   ├── purchase_report.json
│   └── logs/
├── run2/                    # 第 2 轮测试
│   ├── screenshots/
│   ├── purchase_report.json
│   └── logs/
└── phase6_summary.json      # 汇总报告
```
</text>
</step>
<step>
<type>text</type>
<text>
## 5. 风险与应对
</text>
</step>
<step>
<type>text</type>
<text>
| 风险 | 可能性 | 应对措施 |
|------|--------|----------|
| Prompt 优化效果不佳 | 中 | 增加更多 few-shot 示例 |
| 侧边栏结构复杂 | 低 | 优化元素定位策略 |
| 表单控件类型多样 | 中 | 增强执行层对特殊控件的支持 |
| 3 轮仍未通过 | 低 | 记录问题，进入 Phase 7 总结 |
</text>
</step>
<step>
<type>text</type>
<text>
## 6. 完成标准
</text>
</step>
<step>
<type>text</type>
<text>
- [ ] 采购单场景连续 2 次通过
- [ ] 生成 Phase 6 测试报告
- [ ] 更新 `docs/progress.md`
- [ ] 更新 `docs/1_后端主计划.md` 任务勾选
