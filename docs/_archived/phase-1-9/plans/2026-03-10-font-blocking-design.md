# 字体拦截设计文档

## 问题描述

在执行 E2E 测试时，截图操作频繁超时失败：

```
Page.screenshot: Timeout 5000ms exceeded.
Call log:
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
```

**根本原因**：目标 ERP 系统使用阿里云 CDN 的外部字体（iconfont），Playwright 截图时会等待所有字体加载完成，当网络请求较慢时导致超时。

## 解决方案

使用 Playwright 的 `route` 功能拦截并阻止字体请求，从根本上避免字体加载等待。

## 设计细节

### 修改文件

- `backend/agent_simple/perception.py`

### 实现方式

```python
class Perception:
    def __init__(self, page: Page):
        self.page = page
        self._font_blocker_set = False

    async def _ensure_font_blocker(self):
        """确保字体拦截器已设置（只执行一次）"""
        if self._font_blocker_set:
            return

        async def block_fonts(route):
            if route.request.resource_type == "font":
                await route.abort()
            else:
                await route.continue_()

        await self.page.route("**", block_fonts)
        self._font_blocker_set = True

    async def _take_screenshot(self, max_retries: int = 3) -> str:
        # 确保字体拦截器已设置
        await self._ensure_font_blocker()

        # 后续截图逻辑不变
        # ...
```

### 调用时机

在 `Perception` 初始化后，首次截图前设置拦截器。使用 `_font_blocker_set` 标志确保只设置一次。

### 影响评估

| 方面 | 影响 |
|------|------|
| 视觉效果 | iconfont 图标显示为 fallback（方框或空白） |
| LLM 理解 | 不受影响（已确认图标不重要，文字标签是关键） |
| 截图速度 | 大幅提升（无字体等待） |
| 稳定性 | 消除超时失败 |

## 预期效果

| 指标 | 修改前 | 修改后 |
|------|--------|--------|
| 截图耗时 | 5-10s（经常超时） | <1s |
| 超时失败率 | ~80% | ~0% |

## 风险评估

- **低风险**：改动范围小，只影响字体加载逻辑
- **可回滚**：如有问题，移除拦截器代码即可恢复

## 测试计划

1. 运行现有登录测试 `test_login_e2e.py`
2. 验证所有截图步骤都能成功
3. 确认 LLM 仍能正确理解页面并完成任务
