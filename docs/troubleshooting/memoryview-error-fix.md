# Memoryview 错误修复记录

## 错误描述

在后端 API 调用 Browser-Use Agent 时，出现以下错误：

```
WARNING  [Agent] ❌ Result failed 1/6 times: memoryview: a bytes-like object is required, not 'str'
```

**触发条件**:
- 通过后端 API 触发任务执行时出现
- 直接命令行运行 pytest 测试不会出现

## 错误原因

错误发生在 `backend/core/agent_service.py` 的 `save_screenshot` 函数中：

```python
# 问题代码
filepath.write_bytes(screenshot_bytes)  # screenshot_bytes 是字符串，不是字节！
```

**根本原因**:
- `browser_state.screenshot` 返回的是 **base64 编码的字符串**
- `filepath.write_bytes()` 需要 **bytes** 类型的数据
- 直接传入字符串导致了 memoryview 错误

## 完整错误堆栈

```
Traceback (most recent call last):
  File "browser_use/agent/service.py", line 1050, in step
    await self._get_next_action(browser_state_summary)
  File "browser_use/agent/service.py", line 1182, in _get_next_action
    await self._handle_post_llm_processing(browser_state_summary, input_messages)
  File "browser_use/agent/service.py", line 1687, in _handle_post_llm_processing
    await self.register_new_step_callback(
  File "backend/core/agent_service.py", line 115, in step_callback
    screenshot_path = await self.save_screenshot(
  File "backend/core/agent_service.py", line 42, in save_screenshot
    filepath.write_bytes(screenshot_bytes)
  File "pathlib.py", line 1066, in write_bytes
    view = memoryview(data)
TypeError: memoryview: a bytes-like object is required, not 'str'
```

## 解决方案

修改 `backend/core/agent_service.py` 的 `save_screenshot` 函数：

```python
import base64
from typing import Union

async def save_screenshot(
    self, screenshot_data: Union[bytes, str], run_id: str, step_index: int
) -> str:
    """保存截图到本地文件

    Args:
        screenshot_data: 截图数据（可以是 bytes 或 base64 编的字符串）
        run_id: 执行 ID
        step_index: 步骤索引

    Returns:
        截图文件路径
    """
    filename = f"{run_id}_{step_index}.png"
    filepath = self.screenshots_dir / filename

    # 处理不同类型的输入
    if isinstance(screenshot_data, str):
        # 如果是字符串，尝试 base64 解码
        try:
            screenshot_bytes = base64.b64decode(screenshot_data)
        except Exception as e:
            logger.warning(f"[{run_id}] base64 解码失败，尝试直接编码: {e}")
            screenshot_bytes = screenshot_data.encode('utf-8')
    else:
        screenshot_bytes = screenshot_data

    filepath.write_bytes(screenshot_bytes)
    return str(filepath)
```

## 修复验证

| 测试场景 | 修复前 | 修复后 |
|---------|--------|--------|
| 直接命令行运行 | ✅ 成功 | ✅ 成功 |
| 后端 API 调用 | ❌ memoryview 错误 | ✅ 无 memoryview 错误 |

## 日期

- **发现问题**: 2026-03-13
- **修复日期**: 2026-03-13
- **修复版本**: main 分支

## 相关文件

- `backend/core/agent_service.py` - 主要修复文件
- `backend/api/main.py` - 添加 DEBUG 日志以帮助诊断

## 经验教训

1. **类型检查**: 处理外部数据时，应该检查数据类型而不是假设
2. **日志级别**: 在调试时启用 DEBUG 日志可以帮助捕获完整错误堆栈
3. **测试覆盖**: 直接命令行测试和后端 API 调用可能有不同的行为，需要分别测试
