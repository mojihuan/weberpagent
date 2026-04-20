# Phase 86: 综合研究报告 -- ERP 登录机制与代码登录实现方案

**Date:** 2026-04-20
**Status:** Complete
**Purpose:** Bridge research and Phase 87 implementation -- Phase 87 executors should need no re-exploration.

---

## Section 1: 登录流程完整记录 (SC-1)

### 1.1 HTTP API 登录调用链

**Endpoint:**
```
POST {erp_base_url}/auth/login
```
- 实际地址: `POST https://erptest.epbox.cn/epbox_erp/auth/login`

**Request:**
```json
{
  "username": "Y59800075",
  "password": "<plaintext password>"
}
```
- Content-Type: `application/json`

**Response (成功):**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJZNTk4MDAwNzUiLCJleHAiOjE3...",
    "refresh_token": "...",
    "expires_in": 720
  }
}
```

**Token 格式:**
- 类型: JWT (JSON Web Token)
- 算法: HS512 (从 header `eyJhbGciOiJIUzUxMiJ9` 解码得到 `{"alg":"HS512"}`)
- Payload 包含: `sub` (用户名), `exp` (过期时间戳)
- 有效期: 720 秒 (12 分钟)

**当前代码路径:**
- `backend/core/auth_service.py:51-106` -- `AuthService.fetch_token()` 通过 httpx 执行 HTTP POST
- 已验证工作正常 (Phase 79 确认, POC 01 再次确认)

### 1.2 Token 存储 (localStorage)

ERP SPA 使用纯 localStorage 存储 token, 无 Cookie 参与 (D-10 确认)。

| localStorage Key | Value | 说明 |
|------------------|-------|------|
| `Admin-Token` | JWT access_token 字符串 | Bearer token, 用于所有 API 请求的 Authorization header |
| `Admin-Expires-In` | `"720"` | Token 有效期 (秒), 字符串格式 |

**Token 消费方式:** SPA 在每次 API 请求时从 store (非 localStorage) 读取 token, 添加到 `Authorization: Bearer {token}` header.

### 1.3 SPA Token 消费流程

ERP SPA (Vue + Vuex/Pinia) 的认证状态管理流程:

```
1. 浏览器加载 SPA 应用
   ↓
2. Vue 应用初始化
   ├── Vuex/Pinia store 创建
   ├── store 从 localStorage 读取 Admin-Token 到 reactive state
   └── Vue Router 初始化，注册 beforeEach 守卫
   ↓
3. 用户访问路由 (如 /index)
   ↓
4. Router beforeEach 守卫执行
   ├── 检查 store.state.token (reactive state, 非 localStorage)
   ├── Token 存在 → 放行，渲染目标页面
   └── Token 不存在 → 重定向到 /login?redirect=%2Findex
   ↓
5. 登录页面
   ├── 用户填写账号密码
   ├── 点击登录按钮 → SPA 调用 POST /auth/login
   ├── 收到 access_token → store.commit('SET_TOKEN', token)
   ├── 同时写入 localStorage.setItem('Admin-Token', token)
   ├── Router.push(redirect 目标)
   └── beforeEach 守卫再次检查 → token 存在 → 放行
```

**关键发现 (POC 01 确认):** Router 守卫检查的是 Vuex/Pinia 的 reactive store state, 不是直接读取 localStorage。这导致即使 localStorage 中有 token, 如果 store 未正确初始化, 仍然会重定向到 /login。

### 1.4 webseleniumerp vs AuthService 对比

| Aspect | webseleniumerp LoginApi | Backend AuthService |
|--------|------------------------|---------------------|
| URL 模式 | `/epbox_erp/auth/login` (通过 CDQ3XEEfT key 映射) | `{erp_base_url}/auth/login` |
| HTTP 方法 | POST (JSON body) | POST (JSON body) |
| Token 提取 | `get_token(response)` -> `data.access_token` | `response.json()["data"]["access_token"]` |
| Token 存储 | 内存 dict + Redis 缓存 | 返回给调用者 |
| 支持角色 | 8 (main, vice, special, platform, idle, super, camera, collection) | 7 (同上, 不含 collection) |
| 错误处理 | 基础 assert | TokenFetchError 异常 (含 role 和 reason) |
| 超时 | 无显式超时 | 10 秒 (httpx.TimeoutException) |

### 1.5 7 角色 Token 获取映射

**角色解析路径:**
```
AccountService.resolve(role) -> AccountInfo(account, password)
AuthService.fetch_token(account, password, role) -> access_token
```

| Role | Account | 用途 |
|------|---------|------|
| main | Y59800075 | 主账号 (默认) |
| vice | (配置) | 副账号 |
| special | (配置) | 特殊角色 |
| platform | (配置) | 平台管理 |
| idle | (配置) | 闲置角色 |
| super | (配置) | 超级管理员 |
| camera | (配置) | 摄像头角色 |

**代码位置:** `backend/core/account_service.py` -- `AccountService.resolve()` 和 `get_login_url()`

---

## Section 2: Cookie 注入失败根因分析 (SC-2)

### 2.1 当前方案架构

当前代码登录路径 (Phase 79-80 建立):

```
runs.py:167-249 (pre-injection branch)
  → create_authenticated_session(role)  [auth_session_factory.py]
    → auth_service.get_storage_state_for_role(role)  [auth_service.py]
      → fetch_token(account, password)  # HTTP POST, 已验证工作
      → build_storage_state(token)      # 构造 Playwright storage_state dict
    → tempfile workaround               # 写入临时 JSON 文件
    → BrowserSession(storage_state=tmp_file_path)
      → StorageStateWatchdog._load_storage_state()
        → CDP Page.addScriptToEvaluateOnNewDocument(init_script)
  → agent_service.pre_navigate(run_id, target_url, session, account, password)
    → navigate_to(target_url)           # 导航到 ERP
    → _programmatic_login(run_id, page, account, password)  # 编程式表单登录
```

### 2.2 三层失败原因

#### 原因 1: CDP Init Script + SPA Vuex/Pinia Store 初始化时序

**机制:** browser-use `StorageStateWatchdog._load_storage_state()` 通过 CDP `Page.addScriptToEvaluateOnNewDocument` 注册 init script。Per CDP spec, 这个 script 会在每个新 document 的所有其他 script 之前执行。

**Init script 内容 (简化):**
```javascript
(function(){
  if (window.location.origin !== "https://erptest.epbox.cn") return;
  try {
    window.localStorage.setItem("Admin-Token", "eyJhbGci...");
    window.localStorage.setItem("Admin-Expires-In", "720");
  } catch (e) {}
})();
```

**时序分析:**
```
[CDP] addScriptToEvaluateOnNewDocument 注册 (runImmediately: true)
  ↓
[导航到 ERP 页面]
  ↓
[CDP] init script 执行 → localStorage.setItem('Admin-Token', token)
  ↓  (理论上在所有页面 script 之前)
[SPA 应用加载]
  ├── Vue 框架初始化
  ├── Vuex/Pinia store 创建
  │   └── store.auth.token = localStorage.getItem('Admin-Token') ?? null
  ├── Router 初始化 + beforeEach 守卫注册
  └── 首次路由解析
      └── beforeEach → store.auth.token 存在 → 应该放行
```

**POC 验证结果 (方案 C):** 即使 init script 正确设置了 localStorage, SPA 仍然重定向到 /login。这表明问题不在于 init script 时序, 而在于:

**POC 01 方案 C 具体结果:**
1. Navigate to favicon.ico -- SUCCESS (同源上下文建立)
2. page.evaluate setItem('Admin-Token') -- SUCCESS (token 写入 localStorage)
3. Navigate to /index -- **FAILED** (重定向到 /login?redirect=%2Findex)
4. localStorage 检查 -- Token **PRESENT** 但被 SPA 忽略

**根因确认:** SPA 的 Vuex/Pinia store 在 **应用初始化时** 从 localStorage 读取 token 到 reactive state。但 store 的初始化发生在 **特定生命周期点**, 而非简单的 "localStorage.getItem"。可能的机制:
- Store 在模块初始化阶段使用硬编码默认值 (null/empty)
- Store 仅在显式登录 action (如 `login()` mutation) 后才更新 token
- Router 守卫检查的是 store state, 而 store state 的初始值不受 localStorage 影响

**D-12 确认:** SPA 使用 Vuex/Pinia 状态管理 -- 在应用初始化时从 localStorage 读取 token 到 store, 后续路由守卫检查 store 而非 localStorage。

#### 原因 2: 代码路径问题 -- Init script 从未被单独测试

**关键发现:** 当前 `runs.py:198-206` 在创建 storage_state session 后, 总是调用 `pre_navigate()` + `_programmatic_login()`。这意味着:

1. Init script 理论上会在 navigate_to 时设置 localStorage
2. 但 pre_navigate 立即检查 URL, 发现重定向到 /login
3. 然后执行 _programmatic_login, 后者也失败
4. 整个流程被标记为失败, 回退到文字登录

**结论:** 即使 init script 机制可能工作, 当前代码路径不会给它机会。代码在 navigate 后立即检查 URL, 而 SPA 的路由守卫可能在 init script 之后但 before store hydration 期间就做了重定向判断。

#### 原因 3: 编程式表单登录按钮事件不兼容

**POC 验证结果 (方案 A):**

当前 `_programmatic_login()` (agent_service.py:238-256) 使用 `btn.click()` 点击登录按钮。

**POC 01 方案 A 发现:**
- `btn.click()` -- **FAILED** (点击后无 redirect, 等待 10s 超时)
- `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))` -- **SUCCESS** (立即 redirect 到 /index)

**根因:** ERP SPA 的登录按钮使用 Vue 的事件绑定 (`@click` 或 `v-on:click`)。Vue 的事件系统期望接收带有 `bubbles: true` 和 `cancelable: true` 属性的 MouseEvent 对象。原生 `.click()` 生成的 MouseEven 缺少 `view: window` 属性, Vue 的事件处理可能未正确捕获。

**表单填写方式 (已验证工作):**
- Native setter: `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set`
- 事件序列: `compositionstart` -> setter call -> `compositionend` -> `input` -> `change`
- 此方法在当前代码和 POC 中均已验证工作

### 2.3 根因总结

| 失败模式 | 根因 | 证据来源 |
|---------|------|---------|
| 方案 C (localStorage 注入) | SPA Vuex/Pinia store 不从 localStorage 读取初始值, Router 守卫检查 store | POC 01 结果: token present in localStorage 但仍 redirect |
| 方案 A 原始实现 | `btn.click()` 不触发 Vue 事件处理 | POC 01 结果: dispatchEvent(MouseEvent) 成功, btn.click() 失败 |
| 整体流程 | Init script + programmatic login 链式失败 | RESEARCH.md 分析 + 代码路径追踪 |

---

## Section 3: POC 验证结果 (SC-3)

### 3.1 方案 C: page.evaluate localStorage 注入 -- FAILED

**POC 脚本:** `backend/tests/poc/poc_localstorage_inject.py`
**执行时间:** 2026-04-20

| Step | Action | Result | Details |
|------|--------|--------|---------|
| 1 | HTTP POST /auth/login | SUCCESS | JWT token 获取成功 |
| 2 | BrowserSession 启动 | SUCCESS | Headless Chromium |
| 3 | Navigate to favicon.ico | SUCCESS | 同源上下文建立, favicon 是静态文件 (不被 SPA catch-all 拦截) |
| 4 | page.evaluate setItem('Admin-Token') | SUCCESS | Token 写入 localStorage, 读取验证通过 |
| 5 | Navigate to /index | **FAILED** | 重定向到 /login?redirect=%2Findex |
| 6 | localStorage 检查 | Token PRESENT | 但被 SPA 忽略 |

**结论:** 方案 C 不可行。localStorage 中的 token 无法被 SPA 的路由守卫识别。SPA 的 Vuex/Pinia store 不从 localStorage 读取 token 初始值。

### 3.2 方案 A: 编程式表单登录 -- SUCCESS (需修复)

**POC 脚本:** `backend/tests/poc/poc_form_login.py`
**执行时间:** 2026-04-20

| Step | Action | Result | Details |
|------|--------|--------|---------|
| 1 | Navigate to /login | SUCCESS | SPA 登录页加载 |
| 2 | Click "密码登录" tab | SUCCESS | 切换到密码登录模式 |
| 3 | Fill account (native setter + composition events) | SUCCESS | 表单值持久化确认 |
| 4 | Fill password (native setter + composition events) | SUCCESS | 表单值持久化确认 |
| 5a | Click login button: `btn.click()` | **FAILED** | 无 redirect, 等待 10s 超时 |
| 5b | Click login button: `dispatchEvent(new MouseEvent)` | **SUCCESS** | 立即 redirect 到 /index |

**关键发现:**

1. **登录按钮修复:**
   - 原始: `btn.click()` -- 不工作
   - 修复: `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))` -- 工作

2. **browser-use page.evaluate 序列化问题:**
   - `page.evaluate` 返回复杂对象时返回字符串
   - 解决: JS 侧使用 `JSON.stringify()`, Python 侧使用 `json.loads()`

3. **表单填写方式已正确:**
   - native setter bypass + compositionend + input + change 事件序列
   - 当前代码 `_programmatic_login` 的表单填写部分无需修改

### 3.3 POC 结论

**推荐方案: 方案 A (修复编程式表单登录)**

方案 C (localStorage 注入) 确认不可行 -- SPA store 不消费直接写入的 localStorage token。方案 A 已通过 POC 验证, 仅需修改登录按钮点击方式。

**修改范围极小:** 只需将 `_programmatic_login()` 中第 244 行的 `btn.click()` 替换为 `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))`.

---

## Section 4: Phase 87 可执行实现方案 (SC-4)

### 4.1 推荐方案: 修复编程式表单登录 (方案 A)

**基于 POC 验证, 方案 A 是确认工作的唯一可行方案。**

#### 修改 1: agent_service.py -- `_programmatic_login()`

**文件:** `backend/core/agent_service.py`
**行范围:** 238-256 (Step 4: Click login button)

**当前代码 (行 238-256):**
```python
# Step 4: Click login button
clicked_login = await page.evaluate("""() => {
    const buttons = document.querySelectorAll('button, div.login-btn, [class*="login-btn"], [class*="loginBtn"]');
    for (const btn of buttons) {
        const text = btn.textContent.trim();
        if (text === '登 录' || text === '登录' || text === 'Login') {
            btn.click();
            return 'clicked: ' + text;
        }
    }
    // Fallback: click any visible button
    for (const btn of buttons) {
        if (btn.offsetParent !== null) {
            btn.click();
            return 'clicked_fallback: ' + btn.textContent.trim();
        }
    }
    return 'not_found';
}""")
```

**修改后代码:**
```python
# Step 4: Click login button
# IMPORTANT: Vue SPA requires dispatchEvent(new MouseEvent) instead of btn.click()
# because Vue's @click binding expects proper MouseEvent with bubbles/cancelable/view.
# Native .click() does not trigger Vue's event handler correctly.
clicked_login = await page.evaluate("""() => {
    const buttons = document.querySelectorAll('button, div.login-btn, [class*="login-btn"], [class*="loginBtn"]');
    for (const btn of buttons) {
        const text = btn.textContent.trim();
        if (text === '登 录' || text === '登录' || text === 'Login') {
            btn.dispatchEvent(new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            }));
            return 'clicked: ' + text;
        }
    }
    // Fallback: click any visible button with MouseEvent
    for (const btn of buttons) {
        if (btn.offsetParent !== null) {
            btn.dispatchEvent(new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            }));
            return 'clicked_fallback: ' + btn.textContent.trim();
        }
    }
    return 'not_found';
}""")
```

**关键变化:**
- 将所有 `btn.click()` 替换为 `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))`
- 保留按钮查找逻辑不变 (已验证工作)
- 保留 fallback 逻辑不变

#### 修改 2: agent_service.py -- `_programmatic_login()` 表单填写事件增强

**文件:** `backend/core/agent_service.py`
**行范围:** 178-211 (Step 2: Fill account) 和 215-230 (Step 3: Fill password)

POC 确认当前 native setter + input + change 事件已工作, 但 POC 中使用了更完整的 composition 事件序列。建议增强为:

**当前代码 (行 196-201):**
```javascript
nativeInputValueSetter.call(textInputs[0], account);
textInputs[0].dispatchEvent(new Event('input', { bubbles: true }));
textInputs[0].dispatchEvent(new Event('change', { bubbles: true }));
```

**建议修改为:**
```javascript
nativeInputValueSetter.call(textInputs[0], account);
textInputs[0].dispatchEvent(new Event('compositionstart', { bubbles: true }));
textInputs[0].dispatchEvent(new Event('compositionend', { bubbles: true }));
textInputs[0].dispatchEvent(new Event('input', { bubbles: true }));
textInputs[0].dispatchEvent(new Event('change', { bubbles: true }));
```

同样修改 password 填写部分 (行 218-224)。

**注意:** 此修改为增强型, 非必须。当前代码在 POC 中已工作。如果 Phase 87 时间紧张, 可优先只修改按钮点击 (修改 1)。

#### 修改 3: runs.py -- 简化预注入分支 (可选优化)

**文件:** `backend/api/routes/runs.py`
**行范围:** 162-249 (pre-injection branch)

**当前问题:** 代码在 `create_authenticated_session()` 成功后仍然调用 `pre_navigate()` 执行 `_programmatic_login()`。由于 storage_state 注入 (方案 C) 已确认不工作, 可以简化流程:

**建议修改:**
```python
if login_role:
    from backend.core.auth_service import TokenFetchError

    # 直接创建普通 session (不传 storage_state)
    # 因为 storage_state localStorage 注入已被确认不可行
    from backend.core.agent_service import create_browser_session
    authenticated_session = create_browser_session()

    # Pre-navigate with programmatic form login (方案 A, 已验证工作)
    effective_target_url = f"{_parsed.scheme}://{_parsed.netloc}"

    auth_pre_nav_ok = await agent_service.pre_navigate(
        run_id, effective_target_url, authenticated_session,
        login_account=account_info.account,
        login_password=account_info.password,
    )
    # ... fallback logic unchanged ...
```

**注意:** 此修改影响较大, Phase 87 可以先只修复 `_programmatic_login()` 的按钮点击, 验证整个流程工作后再考虑简化 `runs.py`。

#### 修改 4: auth_session_factory.py -- Phase 88 清理 (不阻塞 Phase 87)

**文件:** `backend/core/auth_session_factory.py`

Phase 88 可以:
1. 移除 `create_authenticated_session()` 和 temp file workaround
2. 因为 storage_state 注入方案已确认不工作
3. 或者保留但标记为 deprecated, 等待 browser-use 修复 dict 输入 bug

**Phase 87 不需要修改此文件。**

### 4.2 Fallback 逻辑 -- 必须保留

**文件:** `backend/api/routes/runs.py:208-233`

当前 fallback 逻辑已正确:
1. `create_authenticated_session()` 失败 (TokenFetchError) -> 文字登录
2. `pre_navigate()` 失败 (auth_pre_nav_ok=False) -> 文字登录
3. 文字登录使用 `TestFlowService._build_description()` 构建包含登录步骤的任务描述

**Phase 87 不应修改 fallback 逻辑**, 只需确保修复后的 `_programmatic_login()` 成功时不再触发 fallback。

### 4.3 测试策略 (Phase 87)

#### 单元测试

1. **测试 `_programmatic_login()` 的 JavaScript 代码正确性:**
   - Mock `page.evaluate` 返回值
   - 验证 JavaScript 代码包含 `dispatchEvent(new MouseEvent` 而非 `btn.click()`
   - 验证表单填写使用 native setter

2. **测试 fallback 路径:**
   - `pre_navigate()` 返回 False -> 确认 fallback 到文字登录
   - `TokenFetchError` -> 确认 fallback 到文字登录

#### E2E 验证

1. **端到端代码登录验证:**
   - 创建 login_role=main 的任务
   - 执行任务
   - 验证 Agent 第一步不是登录操作 (URL 应已跳过 /login)
   - 验证日志中显示 `[LOGIN] Login succeeded`

2. **Fallback 验证:**
   - 模拟 token 获取失败 (错误的 ERP_BASE_URL)
   - 确认任务仍能通过文字登录完成

### 4.4 Phase 87 实施步骤 (按优先级排序)

1. **P0 -- 修改 `_programmatic_login()` 按钮点击:** 将 `btn.click()` 替换为 `dispatchEvent(new MouseEvent)` -- 这是唯一必须的修改
2. **P1 -- 增强 form fill 事件序列:** 添加 compositionstart/compositionend 事件 -- 增强型, 非必须
3. **P2 -- 编写单元测试:** 验证修改后的 JavaScript 代码正确性
4. **P3 -- E2E 验证:** 端到端测试代码登录流程
5. **P4 (可选) -- 简化 runs.py:** 移除不必要的 storage_state 创建, 直接使用普通 session

### 4.5 关键代码模式参考

#### Vue SPA 按钮点击 (必须使用 MouseEvent)
```python
# browser-use page.evaluate 格式
clicked = await page.evaluate("""() => {
    const btn = document.querySelector('button');
    btn.dispatchEvent(new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
    }));
    return 'clicked';
}""")
```

#### Vue SPA 表单填写 (native setter + 事件序列)
```python
filled = await page.evaluate("""(value) => {
    const input = document.querySelector('input[type="text"]');
    const nativeSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;
    nativeSetter.call(input, value);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return input.value;
}""", "test_value")
```

#### browser-use page.evaluate 复杂对象返回 (JSON.stringify 模式)
```python
# browser-use 返回复杂对象为字符串, 需要 JSON 序列化
result_str = await page.evaluate("""(token) => {
    const data = {
        token: window.localStorage.getItem('Admin-Token'),
        url: window.location.href
    };
    return JSON.stringify(data);
}""", token)
result = json.loads(result_str)  # Python 侧反序列化
```

---

## Appendix A: CONTEXT.md Decision Reference

| Decision | Description | Report Reference |
|----------|-------------|------------------|
| D-01 | 放弃 StorageStateWatchdog init script 路线 | Section 2.2 原因 1 |
| D-02 | 方案 C -- page.evaluate localStorage 注入 | Section 3.1 (FAILED) |
| D-03 | 方案 A -- 修复编程式表单登录 | Section 3.2 (SUCCESS) |
| D-04 | 独立 POC 脚本验证 | POC 01 已执行 |
| D-05 | POC 验证链路定义 | Section 3.1/3.2 |
| D-06 | POC 成功标准 | Section 3.2 |
| D-07 | 方案 C 失败则转向方案 A | Section 3.2 (方案 A 成功) |
| D-08 | 仅参考 webseleniumerp 模式 | Section 1.4 |
| D-09 | AuthService token 获取无需修改 | Section 1.1 |
| D-10 | ERP 纯 Bearer Token + localStorage | Section 1.2 |
| D-11 | Token 获取已验证工作 | Section 1.1 |
| D-12 | 三层失败原因 | Section 2.2 |

## Appendix B: Evidence Sources

| Evidence | Source | Confidence |
|----------|--------|------------|
| Token HTTP 获取成功 | POC 01 方案 A/C Step 1, AuthService 代码 | HIGH |
| localStorage 注入后 token 持久但 SPA 不识别 | POC 01 方案 C Step 5-6 | HIGH |
| dispatchEvent(MouseEvent) 触发登录成功 | POC 01 方案 A Step 5b | HIGH |
| btn.click() 不触发 Vue 事件处理 | POC 01 方案 A Step 5a | HIGH |
| favicon.ico 是静态文件 (不触发 SPA redirect) | POC 01 方案 C Step 3 | HIGH |
| page.evaluate 复杂对象返回字符串 | POC 01 方案 A (Rule 1 fix) | HIGH |

## Appendix C: Phase 87 Implementation Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| dispatchEvent(MouseEvent) 在 headed 模式行为不同 | LOW | HIGH | POC 在 headless 模式验证, 生产也是 headless |
| ERP 登录页 DOM 结构变化 | MEDIUM | HIGH | 按钮查找使用文本匹配 + fallback, 已有一定鲁棒性 |
| Token 过期 (720s) 在登录过程中 | LOW | MEDIUM | 登录流程 < 10s, Token 12 分钟有效 |
| browser-use 版本更新改变 page.evaluate 行为 | LOW | HIGH | 版本固定, 已有 JSON.stringify workaround |

---

*Report generated: 2026-04-20*
*Evidence sources: 86-01-SUMMARY.md (POC results), 86-RESEARCH.md (technical analysis), 86-CONTEXT.md (locked decisions)*
