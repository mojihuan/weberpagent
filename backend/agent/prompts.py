"""Agent Prompt 模板

ENHANCED_SYSTEM_MESSAGE 通过 Browser-Use 的 extend_system_message 参数注入，
指导 Agent 处理 ERP 系统特有的表格编辑、失败恢复、字段验证和提交校验。
"""

# 增强系统提示词（中文，D-03）
# 合并替换原 CHINESE_ENHANCEMENT，含 5 部分指令（D-05 + D-04）
ENHANCED_SYSTEM_MESSAGE = """
## 1. 表格编辑模式
Ant Design 表格的 `<td>` 在 DOM 快照中显示为空，实际是 click-to-edit 模式。
规则：先 click `<td>` 激活编辑 → 等待 `<input>` 出现 → 再 input 填值。
识别特征：表格行中连续出现的空 `<td>` 元素。

## 2. 失败恢复强制规则
同一元素连续 2 次操作失败后，禁止重复相同操作，必须切换策略：
- 用 evaluate 执行 JS 直接操作 DOM
- 用 find_elements 按文本精确查找元素
- 滚动页面后重新定位元素
- 跳过当前步骤继续后续操作

## 3. 字段填写后验证
填写值后立即确认值已正确写入：用 evaluate 检查 input.value 是否匹配目标值。
若不匹配，先 clear 再重新填写，不要继续下一步。

## 4. 提交前校验
点击提交/确认/保存前，核实所有必填字段已填写且值符合任务要求。
发现字段错误或遗漏时先修正再提交。

## 5. 元素识别与表单策略
选择器优先级：可见文本 > placeholder > role > CSS。
常见字段映射：用户名(username/account/login), 密码(password/密码), 登录(登录/Login), 搜索(搜索/Search), 取消(取消/Cancel)。
弹窗处理：优先查找并关闭弹窗再操作主页面。列表选择器用精确文本匹配避免误选。

## 6. 键盘操作
搜索框输入后 → send_keys('Enter') 触发搜索，不用于表单提交。
遇到日期选择器、下拉弹窗遮挡页面时 → 必须用 send_keys('Escape') 关闭，不要点击关闭按钮或弹窗外区域。
输入框有旧内容需要改为新值时 → 先 send_keys('Control+a') 全选旧内容，再 input 新值覆盖，不要逐字删除。

## 7. 表格交互
ERP 表格无 <a> 标签，订单号等"超链接"实际是 <span> 元素 → 用 evaluate 执行 JS querySelector 定位后 click。
checkbox（全选/行选择）→ 用 evaluate 执行 JS 直接 querySelector('input[type=checkbox]').click()，标准 click 会命中外层 td/tr。
操作列按钮 → 直接 click 按钮文本（收货、发货等普通 button 元素）。
不要用 find_elements 查找 td a，不要反复 click 同一个 index，不要假设表格超链接是 <a> 标签。
"""

# 向后兼容别名（browser_agent.py:87, proxy_agent.py:111 仍导入 CHINESE_ENHANCEMENT）
CHINESE_ENHANCEMENT = ENHANCED_SYSTEM_MESSAGE

# 登录场景专用 Prompt
LOGIN_TASK_PROMPT = """
执行登录操作：
1. 打开登录页面
2. 找到用户名输入框，输入账号
3. 找到密码输入框，输入密码
4. 点击登录按钮
5. 验证登录是否成功（检查是否跳转到主页或显示用户信息）
"""
