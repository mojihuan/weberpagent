# 截图问题修复设计

**日期**: 2026-03-10
**状态**: 待实施
**优先级**: P0

---

## 1. 问题描述

Agent 运行时截图失败，报错提示等待字体加载超时。

**影响**：
- LLM 无法"看到"页面内容
- 只能依赖 DOM 文本做决策
- 决策质量严重下降

---

## 2. 根因分析

当前截图流程 (`perception.py:68-121`)：

```python
# 问题代码
await self.page.wait_for_load_state("networkidle", timeout=3000)  # 可能卡住
await self.page.screenshot(timeout=10000)
```

| 问题点 | 说明 |
|-------|------|
| `networkidle` 等待 | 等待网络完全空闲，字体加载慢时卡住 |
| 字体 CDN 问题 | Web 字体从 CDN 加载，响应慢或失败 |
| 超时设置 | 10 秒可能不够，但也可能太长 |

---

## 3. 修复方案

**核心思路**：不等待字体，直接截 viewport

### 3.1 修改内容

文件：`backend/agent_simple/perception.py`

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

            # 2. 固定等待 JS 渲染（不等待 networkidle）
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

### 3.2 关键改动

| 改动 | 原值 | 新值 | 原因 |
|-----|------|------|------|
| networkidle 等待 | 3000ms 超时 | **移除** | 字体加载可能卡住 |
| 固定延迟 | 500ms | **1000ms** | 给 JS 更多渲染时间 |
| 截图超时 | 10000ms | **5000ms** | 快速失败，快速重试 |

---

## 4. 验证方式

修复后运行登录场景测试：

```bash
python -m backend.tests.test_login_e2e
```

**成功标准**：
- 截图不再超时
- 每一步都有有效截图（非占位图）
- 登录场景通过

---

## 5. 后续优化（如果修复后仍有问题）

1. **禁用 Web 字体**：启动浏览器时添加 `--disable-remote-fonts`
2. **增加等待策略**：等待特定元素出现后再截图
3. **降级处理**：截图失败时记录日志但不影响流程

---

## 6. 相关文件

- 修改文件：`backend/agent_simple/perception.py`
- 测试文件：`backend/tests/test_login_e2e.py`
