"""FastAPI 应用入口"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import tasks, runs


@asynccontextmanager
async def lifespan(app: FastAPI):
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
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",  # Vite 可能使用备用端口
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api")
app.include_router(runs.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Browser-Use API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
