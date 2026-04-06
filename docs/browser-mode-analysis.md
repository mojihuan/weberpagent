# 浏览器模式分析报告

v0.4.0 本地开发时 Playwright 会弹出浏览器窗口（headed 模式），当前版本不再弹出。经 Phase 63 系统化代码对比，根因已确认：提交 `f951791` (2026-03-24) 为 Linux 服务器部署引入了 `BrowserSession(headless=True)`，覆盖了 browser-use 的自动检测机制，导致所有环境（包括本地开发）都以 headless 模式运行。

## 根因

提交 f951791 引入 `BrowserSession(headless=True)` 用于 Linux 服务器部署。browser-use 默认的自动检测机制会根据运行环境决定 headed/headless（macOS 有显示器则 headed，Linux 服务器无显示器则 headless）。f951791 的显式 `headless=True` 覆盖了这一自动检测，而 `create_browser_session()` 被 `run_simple()` 和 `run_with_streaming()` 共享，导致本地开发也运行在 headless 模式。

## 关键差异

| 项目 | v0.4.0 | 当前版本 |
|------|--------|----------|
| headless 模式 | Auto-detect（macOS=headed） | 显式 True |
| browser_session | None（未传递） | `create_browser_session()` |
| Chrome args | 0 个（browser-use 默认） | 7 个（6 项目 + --headless=new） |
| Agent class (streaming) | `Agent` | `MonitoredAgent` |
| 参数数量 (streaming) | 5 | 13+ |

## 修复建议

1. **恢复 browser-use 自动检测（推荐）**: 移除显式 `headless=True`，让 browser-use 根据运行环境自动选择 headed/headless。需区分本地开发和服务器部署环境。

2. **环境变量控制 headless**: 使用环境变量（如 `BROWSER_HEADLESS`）控制模式，默认自动检测，服务器部署时通过环境变量覆盖。

3. **在 headed 模式下重新测试 DOM Patch**: 恢复 headed 模式后，测试哪些 DOM Patch 仍然必要，区分 headless 特定和普遍有用的 patch。

4. **保留 DOM Patch 作为 fallback**: 即使恢复 headed 模式，服务器部署仍需 headless，DOM Patch 可作为安全网保留。

## 详细报告

完整技术报告包含差异列表、DOM Patch 评估、配置演变时间线等详细内容，参见 `.planning/phases/64-分析报告输出/64-REPORT.md`
