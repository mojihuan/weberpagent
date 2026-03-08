"""Agent Prompt 模板"""

# 中文页面处理增强指令
# 通过 Browser-Use 的 extend_system_message 参数注入
CHINESE_ENHANCEMENT = """
## 中文页面处理增强

1. **元素识别优先级**
   - 优先使用可见文本（按钮文字、链接文字）
   - 其次使用 placeholder 属性
   - 最后使用 aria-label 或 title

2. **常见中文表单字段**
   - 用户名/账号: username, account, login, 用户名, 账号
   - 密码: password, pwd, passwd, 密码
   - 登录: 登录, 登入, 确定, 提交, Login
   - 搜索: 搜索, 查询, 检索, Search
   - 取消: 取消, 关闭, Cancel

3. **错误处理策略**
   - 遇到验证码时，等待 5 秒后重试
   - 页面加载超时时，刷新页面
   - 元素未找到时，先滚动页面再查找
   - 表单提交失败时，检查错误提示并调整

4. **动作输出格式**
   始终输出标准 JSON 格式：
   ```json
   {
     "action": "click|fill|goto|select|scroll|wait|done",
     "selector": "CSS选择器或文本",
     "value": "输入值（fill时使用）",
     "reasoning": "执行此动作的原因"
   }
   ```

5. **选择器策略**
   - 优先使用文本选择器: text=登录
   - 其次使用 role 选择器: role=button[name="登录"]
   - 最后使用 CSS 选择器: button.login-btn
"""

# 登录场景专用 Prompt
LOGIN_TASK_PROMPT = """
执行登录操作：
1. 打开登录页面
2. 找到用户名输入框，输入账号
3. 找到密码输入框，输入密码
4. 点击登录按钮
5. 验证登录是否成功（检查是否跳转到主页或显示用户信息）
"""
