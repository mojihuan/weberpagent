# 截图问题修复实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复 Playwright 截图等待字体加载超时的问题

**Architecture:** 修改 perception.py 中的 `_take_screenshot` 方法，移除 networkidle 等待，使用固定延迟

**Tech Stack:** Python, Playwright

---

## Task 1: 修复截图方法

**Files:**
- Modify: `backend/agent_simple/perception.py:68-121`

**Step 1: 修改 `_take_screenshot` 方法**

找到 `backend/agent_simple/perception.py` 第 68-121 行的 `_take_screenshot` 方法，替换为：

```python
async def _take_screenshot(self, max_retries: int = 3) -> str:
    """截图并转为 base64，带重试机制

    优化策略：
    1. 只等待 DOM 加载完成（domcontentloaded）
    2. 使用固定延迟等待 JS 渲染（不等待 networkidle）
    3. 缩短截图超时，快速失败重试
    4. 使用 viewport 截图（full_page=False）
    """
    for attempt in range(max_retries):
        try:
            # 1. 只等待 DOM 加载
            try:
                await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
            except Exception:
                pass

            # 2. 固定等待 JS 渲染（移除 networkidle 等待）
            await self.page.wait_for_timeout(1000)

            # 3. 直接截图
            screenshot_bytes = await self.page.screenshot(
                type="png",
                timeout=5000,  # 缩短超时
                full_page=False,
                animations="disabled",
                caret="initial",
            )

            print(f"✅ 截图成功 (大小: {len(screenshot_bytes)} bytes)")
            return base64.b64encode(screenshot_bytes).decode("utf-8")

        except Exception as e:
            print(f"⚠️ 截图失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await self.page.wait_for_timeout(500)

    # 所有尝试都失败，返回占位图
    print("⚠️ 所有截图尝试失败，使用占位图片")
    PLACEHOLDER_PNG = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    return base64.b64encode(PLACEHOLDER_PNG).decode("utf-8")
```

**关键改动说明：**

| 改动 | 原值 | 新值 | 原因 |
|-----|------|------|------|
| networkidle 等待 | 3000ms 超时 | **移除** | 字体加载可能卡住 |
| 固定延迟 | 500ms | **1000ms** | 给 JS 更多渲染时间 |
| 截图超时 | 10000ms | **5000ms** | 快速失败，快速重试 |
| caret 参数 | 无 | **"initial"** | 不等待光标渲染 |

**Step 2: 验证修改**

检查代码语法：

```bash
python -c "from backend.agent_simple.perception import PagePerception; print('✅ 语法检查通过')"
```

Expected: `✅ 语法检查通过`

**Step 3: 提交修改**

```bash
git add backend/agent_simple/perception.py
git commit -m "fix(perception): 修复截图超时问题 - 移除 networkidle 等待"
```

---

## Task 2: 验证修复效果

**Files:**
- Test: `backend/tests/test_login_e2e.py`

**Step 1: 运行登录场景测试**

```bash
source venv/bin/activate && python -m backend.tests.test_login_e2e
```

**Step 2: 检查截图输出**

```bash
ls -la outputs/tests/*/screenshots/
```

Expected: 每一步都有截图文件（非占位图）

**Step 3: 记录结果**

如果测试通过：
- 更新 `docs/progress.md`
- 提交验证结果

如果仍有问题：
- 查看具体错误信息
- 考虑进一步优化（禁用 Web 字体等）

---

## 成功标准

- [ ] 截图不再超时
- [ ] 每一步都有有效截图（文件大小 > 1KB）
- [ ] 登录场景测试通过

---

## 后备方案（如果仍有问题）

### 方案 B: 禁用 Web 字体

在 Playwright 启动时添加参数：

```python
# backend/agent_simple/agent.py 或测试文件中
browser = await playwright.chromium.launch(
    args=['--disable-remote-fonts']
)
```

### 方案 C: 更激进的超时策略

```python
await self.page.screenshot(
    timeout=3000,  # 更短超时
    full_page=False,
    animations="disabled",
    caret="initial",
    scale="css",  # 使用 CSS 像素比
)
```
