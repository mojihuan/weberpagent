"""FastAPI 应用入口"""

import os

# 禁用代理 - 避免 httpx 自动读取系统代理配置导致 LLM 调用超时
# 必须在 import 其他模块之前执行，确保 httpx 不会读取到代理配置
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy']:
    os.environ.pop(proxy_var, None)

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import tasks, runs, reports, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启用 DEBUG 日志以捕获完整错误堆栈
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # 专门为 browser_use 启用 DEBUG
    logging.getLogger('browser_use').setLevel(logging.DEBUG)
    logging.getLogger('cdp_use').setLevel(logging.DEBUG)
    print("Starting Browser-Use API Server...")
    yield
    print("Shutting down Browser-Use API Server...")


app = FastAPI(
    title="Browser-Use API",
    description="AI + Playwright UI 自动化测试平台 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api")
app.include_router(runs.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Browser-Use API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
