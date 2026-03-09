"""OpenAI 兼容代理服务

将 OpenAI 格式的 API 请求转换为通义千问格式，
使 Browser-Use 可以直接使用 ChatOpenAI 类。

使用方式：
1. 启动代理服务：python -m backend.proxy.openai_proxy
2. Browser-Use 配置 base_url=http://localhost:8000/v1
"""

import json
import logging
import os
import re
from contextlib import asynccontextmanager
from typing import Any

import dashscope
import uvicorn
from dashscope import MultiModalConversation
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置通义千问
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("DASHSCOPE_API_KEY 未配置")

dashscope.api_key = DASHSCOPE_API_KEY


# ============ 请求/响应模型 ============


class Message(BaseModel):
    role: str
    content: str | list[Any] | None = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: float | None = 0.7
    max_tokens: int | None = None
    response_format: dict | None = None
    stream: bool = False


class ChatCompletionChoice(BaseModel):
    index: int = 0
    message: Message
    finish_reason: str = "stop"


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: ChatCompletionUsage


# ============ 消息转换 ============


def extract_text_from_content(content: str | list[Any] | None) -> str:
    """从 content 中提取文本"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "text":
                    texts.append(part.get("text", ""))
            elif isinstance(part, str):
                texts.append(part)
        return "\n".join(texts)
    return str(content)


def extract_images_from_content(content: str | list[Any] | None) -> list[str]:
    """从 content 中提取图像 URL"""
    images = []
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "image_url":
                    url_data = part.get("image_url", {})
                    if isinstance(url_data, dict):
                        url = url_data.get("url", "")
                    else:
                        url = str(url_data)
                    if url:
                        images.append(url)
    return images


def convert_messages_to_qwen(messages: list[Message]) -> tuple[list[dict], list[str]]:
    """将 OpenAI 格式消息转换为通义千问格式

    Returns:
        (消息列表, 图像列表)
    """
    converted = []
    all_images = []

    for msg in messages:
        text = extract_text_from_content(msg.content)
        images = extract_images_from_content(msg.content)

        converted.append({"role": msg.role, "content": text})
        all_images.extend(images)

    return converted, all_images


def build_qwen_content(messages: list[dict], images: list[str]) -> list:
    """构建通义千问的多模态内容"""
    content = []

    # 添加图像
    for img in images:
        if img.startswith("http"):
            content.append({"image": img})
        elif img.startswith("data:"):
            # Base64 格式
            content.append({"image": img})
        else:
            # 本地文件路径 - 转换为 base64
            import base64
            try:
                with open(img, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
                content.append({"image": f"data:image/png;base64,{data}"})
            except Exception as e:
                logger.warning(f"无法读取图像文件 {img}: {e}")

    # 合并所有消息文本
    full_text = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
    content.append({"text": full_text})

    return content


# ============ API 调用 ============


def call_qwen_api(content: list, model: str = "qwen-vl-max") -> dict:
    """调用通义千问 API"""
    response = MultiModalConversation.call(
        model=model,
        messages=[{"role": "user", "content": content}],
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"通义千问 API 错误: {response.message}"
        )

    # 提取响应内容
    raw_content = response.output.choices[0].message.content
    if isinstance(raw_content, list):
        text = " ".join(
            item.get("text", "") for item in raw_content if isinstance(item, dict)
        )
    else:
        text = str(raw_content)

    return {
        "content": text,
        "usage": {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        }
    }


def ensure_json_format(content: str, response_format: dict | None) -> str:
    """确保输出符合 JSON 格式要求"""
    if response_format is None:
        return content

    # 检查是否要求 JSON 输出
    format_type = response_format.get("type", "")
    if format_type not in ("json_object", "json_schema"):
        return content

    # 如果内容已经包含 JSON，提取它
    # 尝试提取 markdown 代码块中的 JSON
    code_block_pattern = r"```(?:json)?\s*([\s\S]*?)```"
    matches = re.findall(code_block_pattern, content)
    for match in matches:
        try:
            json.loads(match.strip())
            return match.strip()
        except json.JSONDecodeError:
            continue

    # 尝试找到 JSON 对象
    json_pattern = r"\{[\s\S]*\}"
    matches = re.findall(json_pattern, content)
    for match in matches:
        try:
            json.loads(match)
            return match
        except json.JSONDecodeError:
            continue

    # 如果内容本身是有效 JSON
    try:
        json.loads(content)
        return content
    except json.JSONDecodeError:
        pass

    # 如果都不是，返回原始内容（可能导致 Browser-Use 解析失败）
    logger.warning(f"无法提取有效 JSON: {content[:200]}...")
    return content


# ============ FastAPI 应用 ============


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("OpenAI 兼容代理服务启动")
    logger.info(f"通义千问 API Key: {DASHSCOPE_API_KEY[:10]}...")
    yield
    logger.info("OpenAI 兼容代理服务关闭")


app = FastAPI(
    title="OpenAI 兼容代理",
    description="将 OpenAI API 请求转换为通义千问格式",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "provider": "qwen"}


@app.get("/v1/models")
async def list_models():
    """列出可用模型"""
    return {
        "object": "list",
        "data": [
            {
                "id": "qwen-vl-max",
                "object": "model",
                "created": 1700000000,
                "owned_by": "qwen",
            },
            {
                "id": "qwen-vl-plus",
                "object": "model",
                "created": 1700000000,
                "owned_by": "qwen",
            },
        ]
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """处理聊天完成请求"""
    import time
    import uuid

    request_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
    created = int(time.time())

    try:
        # 转换消息
        messages, images = convert_messages_to_qwen(request.messages)

        # 构建通义千问内容
        content = build_qwen_content(messages, images)

        # 调用通义千问
        result = call_qwen_api(content, model=request.model)

        # 处理 JSON 格式要求
        response_content = ensure_json_format(
            result["content"],
            request.response_format
        )

        # 构建响应
        return ChatCompletionResponse(
            id=request_id,
            created=created,
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content=response_content),
                    finish_reason="stop",
                )
            ],
            usage=ChatCompletionUsage(
                prompt_tokens=result["usage"]["prompt_tokens"],
                completion_tokens=result["usage"]["completion_tokens"],
                total_tokens=result["usage"]["total_tokens"],
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理请求失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """启动代理服务"""
    uvicorn.run(
        "backend.proxy.openai_proxy:app",
        host="0.0.0.0",
        port=8765,
        reload=True,
    )


if __name__ == "__main__":
    main()
