# Phase 7 实施计划：采购单场景分模块突破

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 通过分模块测试方式，让采购单场景端到端成功（从登录到表单提交完成）

**Architecture:** 将采购单场景拆分为 5 个独立模块（登录→侧边栏一级→侧边栏二级→表单填写→提交验证），每个模块独立测试通过后进行整合测试。新增 hover 动作支持解决菜单展开问题。

**Tech Stack:** Python, Playwright, pytest, 通义千问 qwen-vl-max

---

## Task 1: 创建测试目录结构和运行脚本

**Files:**
- Create: `backend/tests/modules/__init__.py`
- Create: `backend/tests/run_phase7.py`

**Step 1: 创建模块目录**

```bash
mkdir -p backend/tests/modules
```

**Step 2: 创建 `backend/tests/modules/__init__.py`**

```python
"""Phase 7 模块测试"""
```

**Step 3: 创建 `backend/tests/run_phase7.py`**

```python
"""Phase 7 运行入口 - 采购单场景分模块测试

用法:
    python -m backend.tests.run_phase7 --module m1
    python -m backend.tests.run_phase7 --all
    python -m backend.tests.run_phase7 --integration
"""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


async def run_module(module: str):
    """运行单个模块测试"""
    print(f"\n{'='*50}")
    print(f"运行模块: {module.upper()}")
    print(f"{'='*50}\n")

    if module == "m1":
        from backend.tests.modules.test_m1_login import run_test
        await run_test()
    elif module == "m2":
        from backend.tests.modules.test_m2_sidebar_l1 import run_test
        await run_test()
    elif module == "m3":
        from backend.tests.modules.test_m3_sidebar_l2 import run_test
        await run_test()
    elif module == "m4":
        from backend.tests.modules.test_m4_form import run_test
        await run_test()
    elif module == "m5":
        from backend.tests.modules.test_m5_submit import run_test
        await run_test()
    else:
        print(f"未知模块: {module}")
        return False

    return True


async def run_all_modules():
    """按顺序运行所有模块"""
    modules = ["m1", "m2", "m3", "m4", "m5"]
    results = {}

    for module in modules:
        try:
            success = await run_module(module)
            results[module] = success
            if not success:
                print(f"\n❌ 模块 {module.upper()} 失败，停止后续测试")
                break
        except Exception as e:
            print(f"\n❌ 模块 {module.upper()} 异常: {e}")
            results[module] = False
            break

    # 打印汇总
    print(f"\n{'='*50}")
    print("模块测试汇总")
    print(f"{'='*50}")
    for module, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {module.upper()}: {status}")

    return all(results.values())


async def run_integration():
    """运行整合测试"""
    print(f"\n{'='*50}")
    print("运行整合测试")
    print(f"{'='*50}\n")

    from backend.tests.modules.test_integration import run_test
    await run_test()


def main():
    parser = argparse.ArgumentParser(description="Phase 7 模块测试")
    parser.add_argument("--module", "-m", help="运行指定模块 (m1-m5)")
    parser.add_argument("--all", "-a", action="store_true", help="运行所有模块")
    parser.add_argument("--integration", "-i", action="store_true", help="运行整合测试")

    args = parser.parse_args()

    if args.module:
        asyncio.run(run_module(args.module))
    elif args.all:
        asyncio.run(run_all_modules())
    elif args.integration:
        asyncio.run(run_integration())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

**Step 4: 验证目录结构**

```bash
ls -la backend/tests/modules/
```

Expected: 显示 `__init__.py` 文件

**Step 5: 提交**

```bash
git add backend/tests/modules/ backend/tests/run_phase7.py
git commit -m "feat(phase7): 创建模块测试目录和运行脚本"
```

---

## Task 2: 实现 hover 动作支持

**Files:**
- Modify: `backend/agent_simple/types.py:7-15`
- Modify: `backend/agent_simple/executor.py:59-75`

**Step 1: 在 types.py 添加 HOVER 动作类型**

在 `ActionType` 枚举中添加 `HOVER`：

```python
class ActionType(str, Enum):
    """支持的动作类型"""

    NAVIGATE = "navigate"
    CLICK = "click"
    INPUT = "input"
    HOVER = "hover"  # 新增：悬停动作
    WAIT = "wait"
    DONE = "done"
```

**Step 2: 验证类型修改**

```bash
python -c "from backend.agent_simple.types import ActionType; print(ActionType.HOVER)"
```

Expected: 输出 `ActionType.HOVER`

**Step 3: 在 executor.py 添加 hover 处理**

在 `execute` 方法的动作分发中添加 hover 分支（约第 59-75 行）：

```python
async def execute(
    self,
    action: Action,
    elements: list[InteractiveElement],
) -> ActionResult:
    """执行动作"""
    logger.info(f"执行动作: {action.action}, 目标: {action.target}, 值: {action.value}")

    try:
        if action.action == "navigate":
            return await self._navigate(action.value or "")
        elif action.action == "click":
            return await self._click(action.target, elements)
        elif action.action == "input":
            return await self._input(action.target, action.value, elements)
        elif action.action == "hover":
            return await self._hover(action.target, elements)  # 新增
        elif action.action == "wait":
            return await self._wait()
        elif action.action == "done":
            return ActionResult(success=True, error=None)
        else:
            return ActionResult(
                success=False,
                error=f"未知动作类型: {action.action}",
            )
    # ... 其余代码不变
```

**Step 4: 在 executor.py 添加 `_hover` 方法**

在 `_wait` 方法之前添加：

```python
async def _hover(
    self,
    target: str | None,
    elements: list[InteractiveElement],
) -> ActionResult:
    """悬停在目标元素上（用于菜单展开）

    Args:
        target: 目标元素描述
        elements: 可交互元素列表

    Returns:
        ActionResult: 执行结果
    """
    if not target:
        return ActionResult(success=False, error="悬停目标不能为空")

    # 尝试定位元素
    locator = await self._locate_element(target, elements)

    if locator:
        try:
            await locator.hover(timeout=self.timeout)
            logger.info(f"悬停成功: {target}")
            # 等待子菜单展开
            await self.page.wait_for_timeout(500)
            return ActionResult(success=True)
        except Exception as e:
            logger.warning(f"悬停失败: {target}, 错误: {e}")
            return ActionResult(success=False, error=f"悬停失败: {str(e)[:100]}")
    else:
        # 直接尝试通过文本悬停
        try:
            await self.page.get_by_text(target).hover(timeout=self.timeout)
            logger.info(f"通过文本悬停成功: {target}")
            await self.page.wait_for_timeout(500)
            return ActionResult(success=True)
        except Exception as e:
            return ActionResult(success=False, error=f"无法找到元素: {target}")
```

**Step 5: 更新 prompts.py 添加 hover 动作说明**

在 `SYSTEM_PROMPT` 的动作表格中添加 hover：

```markdown
| 动作 | target | value | 说明 |
|------|--------|-------|------|
| navigate | null | URL | 打开指定网页，URL 放在 value 字段 |
| click | 元素标识 | null | 点击目标元素 |
| input | 元素标识 | 输入内容 | 在目标元素中输入文本 |
| hover | 元素标识 | null | 悬停在目标元素上（用于展开菜单） |
| wait | null | null | 等待页面加载完成 |
| done | null | null | 标记任务完成 |
```

**Step 6: 验证 hover 功能**

```bash
python -c "
from backend.agent_simple.executor import Executor
from backend.agent_simple.types import Action, InteractiveElement
print('Executor 有 _hover 方法:', hasattr(Executor, '_hover'))
"
```

Expected: 输出 `Executor 有 _hover 方法: True`

**Step 7: 提交**

```bash
git add backend/agent_simple/types.py backend/agent_simple/executor.py backend/agent_simple/prompts.py
git commit -m "feat(agent): 添加 hover 动作支持用于菜单展开"
```

---

## Task 3: 编写 M1 登录验证测试

**Files:**
- Create: `backend/tests/modules/test_m1_login.py`

**Step 1: 创建测试文件**

```python
"""M1: 登录验证测试

任务: 登录系统
成功标准: 单次通过
验证点:
  - URL 变为首页/仪表盘
  - 页面包含用户名或退出按钮
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_test():
    """运行 M1 登录验证测试"""
    print("=" * 50)
    print("M1: 登录验证测试")
    print("=" * 50)

    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    # 加载配置
    config = load_config()
    login_config = config["login"]

    # 创建输出目录
    output_dir = Path("outputs/tests/phase7/m1_login")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化 LLM
    llm = QwenChat(model="qwen-vl-max")

    # 构建任务
    task = f"""
    在 ERP 系统执行登录操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 确认登录成功（检测页面标题变化或出现用户信息）
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page()

        agent = SimpleAgent(
            task=task,
            llm=llm,
            page=page,
            output_dir=str(output_dir),
            max_steps=15,
            max_retries=3,
        )

        start_time = time.time()
        result = await agent.run()
        duration = time.time() - start_time

        await browser.close()

    # 打印结果
    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"\n结果: {status}")
    print(f"步数: {len(result.steps)}")
    print(f"耗时: {duration:.1f}s")

    if not result.success and result.error:
        print(f"错误: {result.error}")

    return result.success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
```

**Step 2: 运行测试验证**

```bash
python -m backend.tests.run_phase7 --module m1
```

Expected: 测试运行，输出结果

**Step 3: 提交**

```bash
git add backend/tests/modules/test_m1_login.py
git commit -m "feat(phase7): 添加 M1 登录验证测试"
```

---

## Task 4: 编写 M2 侧边栏一级菜单测试

**Files:**
- Create: `backend/tests/modules/test_m2_sidebar_l1.py`

**Step 1: 创建测试文件**

```python
"""M2: 侧边栏一级菜单测试

任务: 点击侧边栏"采购管理"菜单并验证子菜单展开
起点: 登录成功后的首页
成功标准: 连续 2 次通过
验证点:
  - "采购管理"菜单展开
  - 子菜单项可见（如"采购订单"）
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_single_test(page, llm, config, output_dir: Path) -> bool:
    """运行单次测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    # 任务：登录后点击一级菜单
    task = f"""
    在 ERP 系统执行以下操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，点击侧边栏"{purchase_config['navigation'][0]}"菜单
    5. 确认子菜单已展开（如果点击后子菜单未展开，尝试悬停在菜单上）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=15,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M2 侧边栏一级菜单测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M2: 侧边栏一级菜单测试")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/m2_sidebar_l1/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success = await run_single_test(page, llm, config, output_dir)
            await page.close()

            if success:
                consecutive_success += 1
                print(f"  ✅ 连续成功: {consecutive_success}/{required_success}")
            else:
                consecutive_success = 0
                print(f"  ❌ 重置连续成功计数")

            run_num += 1

            # 防止无限循环（最多 10 次）
            if run_num > 10:
                print("\n⚠️ 达到最大尝试次数 10 次")
                break

        await browser.close()

    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
```

**Step 2: 运行测试验证**

```bash
python -m backend.tests.run_phase7 --module m2
```

Expected: 测试运行，尝试连续 2 次通过

**Step 3: 提交**

```bash
git add backend/tests/modules/test_m2_sidebar_l1.py
git commit -m "feat(phase7): 添加 M2 侧边栏一级菜单测试"
```

---

## Task 5: 编写 M3 侧边栏二级菜单测试

**Files:**
- Create: `backend/tests/modules/test_m3_sidebar_l2.py`

**Step 1: 创建测试文件**

```python
"""M3: 侧边栏二级菜单测试

任务: 依次点击"采购订单" → "商品采购"
起点: M2 完成后的状态（采购管理已展开）
成功标准: 连续 2 次通过
验证点:
  - URL 变为商品采购页面
  - 页面包含"新增"按钮或采购列表
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_single_test(page, llm, config, output_dir: Path) -> bool:
    """运行单次测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    # 任务：登录后导航到商品采购页面
    nav_steps = " → ".join(purchase_config["navigation"])
    task = f"""
    在 ERP 系统执行以下操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    5. 确认已进入商品采购页面（检测 URL 变化或页面标题）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=20,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M3 侧边栏二级菜单测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M3: 侧边栏二级菜单测试")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/m3_sidebar_l2/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success = await run_single_test(page, llm, config, output_dir)
            await page.close()

            if success:
                consecutive_success += 1
                print(f"  ✅ 连续成功: {consecutive_success}/{required_success}")
            else:
                consecutive_success = 0
                print(f"  ❌ 重置连续成功计数")

            run_num += 1

            if run_num > 10:
                print("\n⚠️ 达到最大尝试次数 10 次")
                break

        await browser.close()

    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
```

**Step 2: 运行测试验证**

```bash
python -m backend.tests.run_phase7 --module m3
```

Expected: 测试运行

**Step 3: 提交**

```bash
git add backend/tests/modules/test_m3_sidebar_l2.py
git commit -m "feat(phase7): 添加 M3 侧边栏二级菜单测试"
```

---

## Task 6: 编写 M4 表单填写测试

**Files:**
- Create: `backend/tests/modules/test_m4_form.py`

**Step 1: 创建测试文件**

```python
"""M4: 表单填写测试

任务: 点击新增按钮，填写采购表单
起点: M3 完成后的商品采购页面
成功标准: 连续 2 次通过
验证点:
  - 表单页面打开
  - 必填字段已填写
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_single_test(page, llm, config, output_dir: Path) -> bool:
    """运行单次测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])
    nav_steps = " → ".join(purchase_config["navigation"])

    # 任务：导航到商品采购页面并填写表单
    task = f"""
    在 ERP 系统执行以下操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    5. 点击"{purchase_config['add_button']}"按钮
    6. 在表单中填写必填字段（设备类型可选：{device_types}，其他字段根据页面实际情况填写）
    7. 确认表单已填写完整（检查必填字段是否有值）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=25,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M4 表单填写测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M4: 表单填写测试")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/m4_form/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success = await run_single_test(page, llm, config, output_dir)
            await page.close()

            if success:
                consecutive_success += 1
                print(f"  ✅ 连续成功: {consecutive_success}/{required_success}")
            else:
                consecutive_success = 0
                print(f"  ❌ 重置连续成功计数")

            run_num += 1

            if run_num > 10:
                print("\n⚠️ 达到最大尝试次数 10 次")
                break

        await browser.close()

    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
```

**Step 2: 运行测试验证**

```bash
python -m backend.tests.run_phase7 --module m4
```

Expected: 测试运行

**Step 3: 提交**

```bash
git add backend/tests/modules/test_m4_form.py
git commit -m "feat(phase7): 添加 M4 表单填写测试"
```

---

## Task 7: 编写 M5 提交验证测试

**Files:**
- Create: `backend/tests/modules/test_m5_submit.py`

**Step 1: 创建测试文件**

```python
"""M5: 提交验证测试

任务: 提交表单并验证成功
起点: M4 完成后的表单页面
成功标准: 连续 2 次通过
验证点:
  - 成功提示出现，或
  - 列表页出现新记录
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_single_test(page, llm, config, output_dir: Path) -> bool:
    """运行单次测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])
    nav_steps = " → ".join(purchase_config["navigation"])

    # 任务：完整的采购单流程
    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {config['base_url']}
    2. 输入账号 {login_config['account']} 和密码 {login_config['password']}
    3. 点击登录按钮
    4. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    5. 点击"{purchase_config['add_button']}"按钮
    6. 在表单中填写必填字段（设备类型可选：{device_types}）
    7. 点击提交或保存按钮
    8. 确认成功（检测成功提示或新记录出现在列表中）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=30,
        max_retries=3,
    )

    result = await agent.run()

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}")

    return result.success


async def run_test():
    """运行 M5 提交验证测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("M5: 提交验证测试")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/m5_submit/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success = await run_single_test(page, llm, config, output_dir)
            await page.close()

            if success:
                consecutive_success += 1
                print(f"  ✅ 连续成功: {consecutive_success}/{required_success}")
            else:
                consecutive_success = 0
                print(f"  ❌ 重置连续成功计数")

            run_num += 1

            if run_num > 10:
                print("\n⚠️ 达到最大尝试次数 10 次")
                break

        await browser.close()

    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
```

**Step 2: 运行测试验证**

```bash
python -m backend.tests.run_phase7 --module m5
```

Expected: 测试运行

**Step 3: 提交**

```bash
git add backend/tests/modules/test_m5_submit.py
git commit -m "feat(phase7): 添加 M5 提交验证测试"
```

---

## Task 8: 编写整合测试

**Files:**
- Create: `backend/tests/modules/test_integration.py`

**Step 1: 创建测试文件**

```python
"""整合测试: 完整采购单流程

任务: M1→M2→M3→M4→M5 完整流程
成功标准: 连续 2 次通过
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_single_test(page, llm, config, output_dir: Path) -> tuple[bool, int, float]:
    """运行单次整合测试

    Returns:
        (success, steps, duration)
    """
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "test"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])
    nav_steps = " → ".join(purchase_config["navigation"])

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，依次点击侧边栏菜单：{nav_steps}
    6. 点击"{purchase_config['add_button']}"按钮
    7. 选择设备类型（可选：{device_types}）
    8. 填写表单中的必填字段（根据页面实际情况填写）
    9. 点击提交或保存按钮
    10. 确认成功（检测按钮下方是否出现新记录或成功提示）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=30,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    status = "✅ 通过" if result.success else "❌ 失败"
    print(f"  结果: {status}, 步数: {len(result.steps)}, 耗时: {duration:.1f}s")

    return result.success, len(result.steps), duration


async def run_test():
    """运行整合测试（需要连续 2 次通过）"""
    print("=" * 50)
    print("整合测试: 完整采购单流程")
    print("成功标准: 连续 2 次通过")
    print("=" * 50)

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    config = load_config()
    llm = QwenChat(model="qwen-vl-max")

    consecutive_success = 0
    required_success = 2
    all_results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)

        run_num = 1
        while consecutive_success < required_success:
            print(f"\n第 {run_num} 次测试:")

            output_dir = Path(f"outputs/tests/phase7/integration/run{run_num}")
            output_dir.mkdir(parents=True, exist_ok=True)

            page = await browser.new_page()
            success, steps, duration = await run_single_test(page, llm, config, output_dir)
            await page.close()

            all_results.append({
                "run": run_num,
                "success": success,
                "steps": steps,
                "duration": duration,
            })

            if success:
                consecutive_success += 1
                print(f"  ✅ 连续成功: {consecutive_success}/{required_success}")
            else:
                consecutive_success = 0
                print(f"  ❌ 重置连续成功计数")

            run_num += 1

            if run_num > 10:
                print("\n⚠️ 达到最大尝试次数 10 次")
                break

        await browser.close()

    # 生成汇总报告
    final_status = "✅ 通过" if consecutive_success >= required_success else "❌ 失败"
    print(f"\n最终结果: {final_status} (连续成功 {consecutive_success}/{required_success})")

    # 保存报告
    report = {
        "phase": "Phase 7 整合测试",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": "采购单场景连续 2 次通过",
        "consecutive_success": consecutive_success,
        "target_achieved": consecutive_success >= required_success,
        "results": all_results,
    }

    report_path = Path("outputs/tests/phase7/integration/summary.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"报告已保存: {report_path}")

    return consecutive_success >= required_success


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
```

**Step 2: 运行整合测试**

```bash
python -m backend.tests.run_phase7 --integration
```

Expected: 测试运行

**Step 3: 提交**

```bash
git add backend/tests/modules/test_integration.py
git commit -m "feat(phase7): 添加整合测试"
```

---

## Task 9: 更新文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/1_后端主计划.md`

**Step 1: 更新 progress.md**

在 `## 后端进度` 部分添加 Phase 7 记录：

```markdown
### Phase 7: 采购单场景分模块突破 🔄
- **开始日期**: 2026-03-10
- **设计文档**: `docs/plans/2026-03-10-phase7-modular-breakthrough-design.md`
- **实施计划**: `docs/plans/2026-03-10-phase7-implementation-plan.md`
- **目标**: 5 个模块全部通过，整合测试连续 2 次通过
- **任务清单**:
  - [ ] 7.1 创建测试目录结构和运行脚本
  - [ ] 7.2 实现 hover 动作支持
  - [ ] 7.3 编写 M1 登录验证测试
  - [ ] 7.4 编写 M2 侧边栏一级菜单测试
  - [ ] 7.5 编写 M3 侧边栏二级菜单测试
  - [ ] 7.6 编写 M4 表单填写测试
  - [ ] 7.7 编写 M5 提交验证测试
  - [ ] 7.8 编写整合测试
  - [ ] 7.9 更新文档
```

**Step 2: 提交**

```bash
git add docs/progress.md docs/1_后端主计划.md
git commit -m "docs: 更新 Phase 7 进度记录"
```

---

## 完成标准

- [ ] hover 动作支持已实现
- [ ] M1 登录验证：单次通过
- [ ] M2 侧边栏一级菜单：连续 2 次通过
- [ ] M3 侧边栏二级菜单：连续 2 次通过
- [ ] M4 表单填写：连续 2 次通过
- [ ] M5 提交验证：连续 2 次通过
- [ ] 整合测试：连续 2 次通过
- [ ] 生成 Phase 7 测试报告
- [ ] 更新 `docs/progress.md`
