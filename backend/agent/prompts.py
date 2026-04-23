"""Agent Prompt 模板

ENHANCED_SYSTEM_MESSAGE 通过 Browser-Use 的 extend_system_message 参数注入，
指导 Agent 处理 ERP 系统特有的表格编辑、失败恢复、字段验证和提交校验。
"""

# 增强系统提示词（中文，D-03）
# 合并替换原 CHINESE_ENHANCEMENT，含 5 部分指令（D-05 + D-04）
ENHANCED_SYSTEM_MESSAGE = """
## 1. 表格编辑模式
Ant Design 表格使用 click-to-edit 模式：`<td>` 单元格在 DOM 快照中显示文本内容和点击索引，
如 `<td> [index]<span>0.00</span></td>`。
规则：先 CLICK 该 `<td>` 单元格 → 等待 `<input>` 出现 → 再 INPUT 填值。
识别特征：表格行中带索引的 `<td>` 单元格，文本内容为数值（如 0.00、210）。

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
表格中的订单号超链接、checkbox 等子元素 → 用 click 点击对应 index（DOM 已为它们分配独立索引）。
如果 click 未命中目标元素 → fallback 用 evaluate JS: document.querySelector('.hand').click() 或 document.querySelector('.el-checkbox').click()。
操作列按钮 → 直接 click 按钮文本即可。
不要用 find_elements 查找 td a（表格无 <a> 标签），不要反复 click 同一个 index。

## 8. 文件上传
遇到导入/上传按钮触发文件选择时 → 不要 click type="file" 的 input 元素（会被拦截），用 upload_file(index, '文件路径') 上传。
文件路径从 <available_file_paths> 标签中选择匹配类型的文件。Excel 导入选 .xlsx，图片上传选 .jpg/.png。
上传后等待文件名显示确认成功，不要用 evaluate 模拟文件选择。

## 9. ERP 表格单元格填写
ERP 表格每个商品行有多个可编辑数值单元格，通过行标识+列注释交叉定位：
每个 td 单元格上方有列注释 `<!-- 列: X -->`，每行上方有行注释 `<!-- 行: I数字 -->`。

**定位：**
看到 `<!-- 行: I数字 -->` → 找到目标行
看到 `<!-- 列: X -->` → 找到目标列
两者交叉 → 精确定位目标 <td> 单元格
示例：任务"填写 I01784004409597 的销售金额为 150" → 找 `<!-- 行: I01784004409597 -->` 行 + `<!-- 列: 销售金额 -->` 列 → 交叉 td

**操作：**
CLICK 交叉定位的 td → 等待 input 出现 → INPUT 填值
td 内部结构 `<td><div>0.00</div></td>` → 点击后出现 `<input>` → 填写新值
不要尝试直接查找 input（click-to-edit 模式下 input 点击前不在 DOM 中）

**验证：**
填写后检查 td 内显示值已变更（如 0.00 → 150），若不匹配先 clear 再重新填写

**异常处理：**
看到 `[已尝试 N 次 模式: ...]` → 切换策略，不要重复相同操作
策略优先级：`[策略: 1-原生 input]`→直接 input；`[策略: 2-需先 click]`→先 click 再 input；`[策略: 3-evaluate JS]`→用 JS 设值
click_no_effect→换 evaluate JS 点击；wrong_column→按行注释重定位；edit_not_active→先 click td 激活再填值
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
