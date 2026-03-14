# 故障排除指南

本目录记录了项目中遇到的问题及其解决方案。

## 目录

### 2026-03

- [Memoryview 错误修复](./memoryview-error-fix.md) - 后端 API 调用时 `memoryview: a bytes-like object is required, not 'str'` 错误的修复

## 常见问题

### 1. LLM 调用超时

**错误信息**: `LLM call timed out after 75 seconds`

**可能原因**:
- 网络代理延迟
- DashScope API 响应慢
- 模型处理大上下文需要更长时间

**解决方案**:
- 检查网络代理配置
- 尝试使用更快的模型
- 增加 LLM 超时配置

### 2. Browser-Use Agent 执行失败

**错误信息**: `Result failed X/6 times`

**排查步骤**:
1. 启用 DEBUG 日志查看完整错误堆栈
2. 检查 LLM 配置是否正确
3. 检查浏览器是否正常启动
4. 检查目标网站是否可访问

### 3. SSE 连接问题

**错误信息**: SSE 客户端无法接收事件

**排查步骤**:
1. 检查 run_id 是否正确
2. 确认任务已启动
3. 检查网络连接
4. 查看后端日志确认事件已发布

## 调试技巧

### 启用 DEBUG 日志

修改 `backend/api/main.py`:

```python
import logging

# 启用 DEBUG 日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# 专门为 browser_use 启用 DEBUG
logging.getLogger('browser_use').setLevel(logging.DEBUG)
```

### 直接测试 Agent

不通过后端 API，直接测试 Agent:

```bash
source .venv/bin/activate
python -c "
import asyncio
from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI

async def test():
    llm = ChatOpenAI(model='qwen3.5-plus', ...)
    agent = Agent(task='测试任务', llm=llm)
    result = await agent.run(max_steps=3)
    print(result)

asyncio.run(test())
"
```
