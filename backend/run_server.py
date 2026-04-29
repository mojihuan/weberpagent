"""
Windows 兼容的 FastAPI 服务器启动脚本

解决 Windows 上 asyncio 子进程兼容性问题：
- browser_use 使用 asyncio.create_subprocess_exec 启动浏览器
- Windows 默认的 SelectorEventLoop 不支持子进程操作
- 必须使用 ProactorEventLoop

使用方法:
    uv run python backend/run_server.py
    # 或
    python -m backend.run_server
"""

import sys
import asyncio

# ⚠️ 必须在导入任何其他模块之前设置事件循环策略
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import os
import uvicorn

# 禁用代理
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy']:
    os.environ.pop(proxy_var, None)


def main() -> None:
    """启动 FastAPI 服务器"""
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,  # Windows + Python 3.14 需要禁用热重载，否则子进程无法正确设置事件循环
    )


if __name__ == "__main__":
    main()
