"""FastAPI 应用入口"""

import sys
import asyncio

# Windows asyncio 子进程兼容性修复
# browser_use 使用 asyncio.create_subprocess_exec 启动浏览器
# Windows 默认的 SelectorEventLoop 不支持子进程操作，需要 ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import os
import uuid
import traceback

# 禁用代理 - 避免 httpx 自动读取系统代理配置导致 LLM 调用超时
# 必须在 import 其他模块之前执行，确保 httpx 不会读取到代理配置
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'all_proxy']:
    os.environ.pop(proxy_var, None)

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api.routes import tasks, runs, reports, dashboard, external_operations, external_data_methods, external_assertions
from backend.config.settings import get_settings
from backend.config.validators import validate_weberp_path
from backend.db.database import init_db
# Import models to register them with Base before init_db()
from backend.db import models  # noqa: F401


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

    # 初始化数据库表
    await init_db()
    print("Database tables initialized.")

    # Validate WEBSERP_PATH if configured
    settings = get_settings()
    if settings.weberp_path:
        print(f"Validating WEBSERP_PATH: {settings.weberp_path}")
        validate_weberp_path(settings.weberp_path)
        print("WEBSERP_PATH validation passed.")

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
app.include_router(external_operations.router, prefix="/api")
app.include_router(external_data_methods.router, prefix="/api")
app.include_router(external_assertions.router, prefix="/api")


# Global exception handlers for consistent API response format

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with consistent format"""
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
                "request_id": request_id
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with consistent format"""
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "request_id": request_id,
                "details": exc.errors()
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    request_id = str(uuid.uuid4())
    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "request_id": request_id,
                "stack": traceback.format_exc() if logging.getLogger().level == logging.DEBUG else None
            }
        }
    )


@app.get("/")
async def root():
    return {"message": "Browser-Use API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
