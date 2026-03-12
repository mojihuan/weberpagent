# Phase 4: 场景验证实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 验证自研简化版 Agent 在真实 ERP 系统中的登录和新增采购单场景

**Architecture:** 使用 SimpleAgent + Playwright + 通义千问 qwen-vl-max，通过端到端测试验证 AI 决策和执行能力

**Tech Stack:** Python 3.11, Playwright, pytest, asyncio, 通义千问 API

---

## Task 1: 更新测试配置

**Files:**
- Modify: `backend/config/test_targets.yaml`

**Step 1: 更新配置文件**

将现有配置更新为：

```yaml
# 测试目标配置
# 用于 POC 场景验证

# 基础 URL
base_url: "https://erptest.epbox.cn/"

# 登录场景配置
login:
  url: "/"
  account: "Y96230027"
  password: "Aa123456"
  success_indicators:
    - "商品采购"
    - "采购管理"
    - "欢迎"

# 采购单场景配置
purchase:
  # 导航路径
  navigation:
    - "商品采购"
    - "采购管理"
    - "新增采购单"
  # 新增按钮
  add_button: "新增"
  # 设备类型选项
  device_types:
    - "手机"
    - "平板电脑"
    - "笔记本电脑"
    - "智能手表"
  # 成功标志
  success_indicator: "记录出现在列表中"
```

**Step 2: 验证配置格式**

Run: `python -c "import yaml; yaml.safe_load(open('backend/config/test_targets.yaml'))"`

Expected: 无错误输出

**Step 3: Commit**

```bash
git add backend/config/test_targets.yaml
git commit -m "config: 更新 Phase 4 测试目标配置"
```

---

## Task 2: 创建 pytest fixtures

**Files:**
- Create: `backend/tests/conftest.py`

**Step 1: 创建 conftest.py**

```python
"""pytest fixtures for Phase 4 scenario tests"""

import asyncio
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, Browser, Page

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.llm.qwen import QwenChat
from backend.config.settings import settings


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def browser():
    """创建浏览器实例（session 级别）"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 调试时使用非 headless
            slow_mo=100,     # 稍微放慢便于观察
        )
        yield browser
        await browser.close()


@pytest.fixture
async def page(browser):
    """创建页面实例"""
    page = await browser.new_page()
    yield page
    await page.close()


@pytest.fixture
def llm():
    """创建 LLM 实例"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        pytest.skip("DASHSCOPE_API_KEY 未配置")
    return QwenChat(model="qwen-vl-max")


@pytest.fixture
def test_config():
    """加载测试配置"""
    import yaml
    config_path = Path(__file__).parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def output_dir():
    """创建输出目录"""
    output_path = Path("outputs/tests/phase4")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
```

**Step 2: 验证 fixtures 可导入**

Run: `python -c "from backend.tests.conftest import *; print('OK')"`

Expected: 输出 `OK`

**Step 3: Commit**

```bash
git add backend/tests/conftest.py
git commit -m "test: 添加 Phase 4 pytest fixtures"
```

---

## Task 3: 创建测试结果数据结构

**Files:**
- Create: `backend/tests/reporter.py`

**Step 1: 创建 reporter.py**

```python
"""Phase 4 测试报告模块"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class TestResult:
    """单个测试结果"""
    scenario: str
    success: bool
    steps: int
    duration: float
    error: Optional[str]
    screenshots: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Phase4Report:
    """Phase 4 测试报告"""
    date: str
    results: list[TestResult]

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total > 0 else 0

    @property
    def avg_steps(self) -> float:
        return sum(r.steps for r in self.results) / self.total if self.total > 0 else 0

    @property
    def avg_duration(self) -> float:
        return sum(r.duration for r in self.results) / self.total if self.total > 0 else 0

    def print_summary(self):
        """打印报告摘要"""
        print("\n" + "=" * 50)
        print("Phase 4 测试报告")
        print("=" * 50)
        print()
        print(f"{'场景':<20} {'成功':<6} {'步数':<6} {'耗时':<8}")
        print("-" * 50)

        for r in self.results:
            status = "✅" if r.success else "❌"
            print(f"{r.scenario:<20} {status:<6} {r.steps:<6} {r.duration:.1f}s")

        print("-" * 50)
        print(f"总计通过率: {self.pass_rate:.0%} ({self.passed}/{self.total})")
        print(f"平均步数: {self.avg_steps:.1f}")
        print(f"平均耗时: {self.avg_duration:.1f}s")
        print("=" * 50)

    def to_json(self) -> dict:
        """转换为 JSON 格式"""
        return {
            "phase": "Phase 4",
            "date": self.date,
            "results": [r.to_dict() for r in self.results],
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "pass_rate": self.pass_rate,
                "avg_steps": self.avg_steps,
                "avg_duration": self.avg_duration,
            }
        }

    def save(self, path: Path):
        """保存报告到文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {path}")
```

**Step 2: 验证模块可导入**

Run: `python -c "from backend.tests.reporter import TestResult, Phase4Report; print('OK')"`

Expected: 输出 `OK`

**Step 3: Commit**

```bash
git add backend/tests/reporter.py
git commit -m "test: 添加 Phase 4 测试报告模块"
```

---

## Task 4: 编写登录场景测试

**Files:**
- Create: `backend/tests/test_login_e2e.py`

**Step 1: 创建登录测试文件**

```python
"""登录场景端到端测试"""

import asyncio
import time
from pathlib import Path

import pytest

from backend.agent_simple.agent import SimpleAgent
from backend.tests.reporter import TestResult


@pytest.mark.asyncio
async def test_login_e2e(page, llm, test_config, output_dir):
    """端到端登录测试

    测试流程：
    1. 打开 ERP 登录页
    2. 输入账号密码
    3. 点击登录
    4. 验证登录成功
    """
    config = test_config["login"]

    # 创建任务输出目录
    task_output = output_dir / "login"
    task_output.mkdir(parents=True, exist_ok=True)

    # 构建任务描述
    task = f"""
    在 ERP 系统执行登录操作：
    1. 打开 {test_config['base_url']}{config['url']}
    2. 在账号输入框输入 {config['account']}
    3. 在密码输入框输入 {config['password']}
    4. 点击登录按钮
    5. 确认登录成功（检测"商品采购"或"欢迎"等元素出现）
    """

    # 创建 Agent
    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=10,
        max_retries=3,
    )

    # 执行测试并计时
    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    # 收集截图
    screenshots = [
        str(s) for s in task_output.glob("*.png")
    ]

    # 创建测试结果
    test_result = TestResult(
        scenario="登录场景",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )

    # 打印结果
    print(f"\n{'='*50}")
    print(f"场景: {test_result.scenario}")
    print(f"成功: {'✅' if test_result.success else '❌'}")
    print(f"步数: {test_result.steps}")
    print(f"耗时: {test_result.duration:.1f}s")
    if test_result.error:
        print(f"错误: {test_result.error}")
    print(f"{'='*50}")

    # 验证基本成功指标
    assert test_result.steps > 0, "没有执行任何步骤"
    assert test_result.steps <= 10, f"步数过多: {test_result.steps}"

    return test_result


if __name__ == "__main__":
    # 直接运行测试
    asyncio.run(test_login_e2e())
```

**Step 2: 验证语法正确**

Run: `python -m py_compile backend/tests/test_login_e2e.py`

Expected: 无错误输出

**Step 3: Commit**

```bash
git add backend/tests/test_login_e2e.py
git commit -m "test: 添加登录场景端到端测试"
```

---

## Task 5: 编写采购单场景测试

**Files:**
- Create: `backend/tests/test_purchase_e2e.py`

**Step 1: 创建采购单测试文件**

```python
"""新增采购单场景端到端测试"""

import asyncio
import time
from pathlib import Path

import pytest

from backend.agent_simple.agent import SimpleAgent
from backend.tests.reporter import TestResult


@pytest.mark.asyncio
async def test_purchase_e2e(page, llm, test_config, output_dir):
    """端到端新增采购单测试

    测试流程：
    1. 登录 ERP 系统
    2. 导航到采购管理页面
    3. 点击新增采购单
    4. 填写表单
    5. 提交并验证
    """
    login_config = test_config["login"]
    purchase_config = test_config["purchase"]

    # 创建任务输出目录
    task_output = output_dir / "purchase"
    task_output.mkdir(parents=True, exist_ok=True)

    # 构建任务描述
    nav_steps = " → ".join(purchase_config["navigation"])
    device_types = "、".join(purchase_config["device_types"])

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {test_config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，点击侧边栏"{purchase_config['navigation'][0]}"
    6. 点击"{purchase_config['navigation'][1]}"
    7. 点击"{purchase_config['navigation'][2]}"
    8. 点击"{purchase_config['add_button']}"按钮
    9. 选择设备类型（可选：{device_types}）
    10. 填写表单中的必填字段（根据页面实际情况填写，可以自由发挥）
    11. 点击提交或保存按钮
    12. 确认成功（检测按钮下方是否出现新记录）
    """

    # 创建 Agent
    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=25,  # 采购单流程较长，增加步数
        max_retries=3,
    )

    # 执行测试并计时
    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    # 收集截图
    screenshots = [
        str(s) for s in task_output.glob("*.png")
    ]

    # 创建测试结果
    test_result = TestResult(
        scenario="新增采购单",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )

    # 打印结果
    print(f"\n{'='*50}")
    print(f"场景: {test_result.scenario}")
    print(f"成功: {'✅' if test_result.success else '❌'}")
    print(f"步数: {test_result.steps}")
    print(f"耗时: {test_result.duration:.1f}s")
    if test_result.error:
        print(f"错误: {test_result.error}")
    print(f"{'='*50}")

    # 打印每一步详情
    print(f"\n执行步骤详情:")
    for step in result.steps:
        action = step.action
        print(f"  Step {step.step_num}: {action.action} -> {action.target or action.value or ''}")

    return test_result


if __name__ == "__main__":
    # 直接运行测试
    asyncio.run(test_purchase_e2e())
```

**Step 2: 验证语法正确**

Run: `python -m py_compile backend/tests/test_purchase_e2e.py`

Expected: 无错误输出

**Step 3: Commit**

```bash
git add backend/tests/test_purchase_e2e.py
git commit -m "test: 添加新增采购单场景端到端测试"
```

---

## Task 6: 创建批量运行脚本

**Files:**
- Create: `backend/tests/run_phase4.py`

**Step 1: 创建运行脚本**

```python
"""Phase 4 批量运行脚本

运行所有场景测试并生成报告
"""

import asyncio
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
from backend.tests.reporter import TestResult, Phase4Report
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_login_test(page, llm, config, output_dir) -> TestResult:
    """运行登录测试"""
    login_config = config["login"]
    task_output = output_dir / "login"
    task_output.mkdir(parents=True, exist_ok=True)

    task = f"""
    在 ERP 系统执行登录操作：
    1. 打开 {config['base_url']}{login_config['url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 确认登录成功（检测"商品采购"或"欢迎"等元素出现）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=10,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    screenshots = [str(s) for s in task_output.glob("*.png")]

    return TestResult(
        scenario="登录场景",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )


async def run_purchase_test(page, llm, config, output_dir) -> TestResult:
    """运行采购单测试"""
    login_config = config["login"]
    purchase_config = config["purchase"]

    task_output = output_dir / "purchase"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，点击侧边栏"{purchase_config['navigation'][0]}"
    6. 点击"{purchase_config['navigation'][1]}"
    7. 点击"{purchase_config['navigation'][2]}"
    8. 点击"{purchase_config['add_button']}"按钮
    9. 选择设备类型（可选：{device_types}）
    10. 填写表单中的必填字段（根据页面实际情况填写，可以自由发挥）
    11. 点击提交或保存按钮
    12. 确认成功（检测按钮下方是否出现新记录）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=25,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    screenshots = [str(s) for s in task_output.glob("*.png")]

    return TestResult(
        scenario="新增采购单",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )


async def main():
    """运行所有测试"""
    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return

    print("=" * 50)
    print("Phase 4: 场景验证")
    print("=" * 50)

    # 加载配置
    config = load_config()
    output_dir = Path("outputs/tests/phase4")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 创建 LLM
    llm = QwenChat(model="qwen-vl-max")

    results: list[TestResult] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=100,
        )

        # 测试 1: 登录场景
        print("\n>>> 测试 1/2: 登录场景")
        page = await browser.new_page()
        try:
            result = await run_login_test(page, llm, config, output_dir)
            results.append(result)
            print(f"    结果: {'✅ 成功' if result.success else '❌ 失败'}")
            print(f"    步数: {result.steps}, 耗时: {result.duration:.1f}s")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
            results.append(TestResult(
                scenario="登录场景",
                success=False,
                steps=0,
                duration=0,
                error=str(e),
                screenshots=[],
            ))
        finally:
            await page.close()

        # 测试 2: 新增采购单场景
        print("\n>>> 测试 2/2: 新增采购单")
        page = await browser.new_page()
        try:
            result = await run_purchase_test(page, llm, config, output_dir)
            results.append(result)
            print(f"    结果: {'✅ 成功' if result.success else '❌ 失败'}")
            print(f"    步数: {result.steps}, 耗时: {result.duration:.1f}s")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
            results.append(TestResult(
                scenario="新增采购单",
                success=False,
                steps=0,
                duration=0,
                error=str(e),
                screenshots=[],
            ))
        finally:
            await page.close()

        await browser.close()

    # 生成报告
    report = Phase4Report(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        results=results,
    )

    # 打印摘要
    report.print_summary()

    # 保存 JSON 报告
    report_path = output_dir / "phase4_report.json"
    report.save(report_path)

    # 返回是否全部通过
    return report.pass_rate == 1.0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
```

**Step 2: 验证语法正确**

Run: `python -m py_compile backend/tests/run_phase4.py`

Expected: 无错误输出

**Step 3: Commit**

```bash
git add backend/tests/run_phase4.py
git commit -m "test: 添加 Phase 4 批量运行脚本"
```

---

## Task 7: 更新进度文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/1_后端主计划.md`

**Step 1: 更新 progress.md**

在 Phase 3' 后面添加 Phase 4 进行中的状态：

```markdown
### Phase 4: 场景验证 🔄
- **开始日期**: 2026-03-10
- **设计文档**: `docs/plans/2026-03-10-phase4-scenario-validation-design.md`
- **任务清单**:
  - [x] 4.1 更新测试配置 ✅
  - [x] 4.2 创建 pytest fixtures ✅
  - [x] 4.3 编写登录场景测试 ✅
  - [x] 4.4 编写采购单场景测试 ✅
  - [x] 4.5 实现统计报告模块 ✅
  - [ ] 4.6 运行测试并生成报告 ⏳
```

**Step 2: 更新 1_后端主计划.md**

更新 Phase 4 的任务勾选状态。

**Step 3: Commit**

```bash
git add docs/progress.md docs/1_后端主计划.md
git commit -m "docs: 记录 Phase 4 开始 - 场景验证"
```

---

## Task 8: 运行测试验证

**Step 1: 运行登录场景测试**

Run: `cd /Users/huhu/project/weberpagent && source venv/bin/activate && python -m backend.tests.test_login_e2e`

Expected: 测试执行完成，输出结果

**Step 2: 运行采购单场景测试**

Run: `cd /Users/huhu/project/weberpagent && source venv/bin/activate && python -m backend.tests.test_purchase_e2e`

Expected: 测试执行完成，输出结果

**Step 3: 运行批量测试脚本**

Run: `cd /Users/huhu/project/weberpagent && source venv/bin/activate && python -m backend.tests.run_phase4`

Expected: 生成完整报告

**Step 4: 检查输出**

- 查看 `outputs/tests/phase4/` 目录下的截图
- 查看 `outputs/tests/phase4/phase4_report.json` 报告

---

## 验收检查清单

- [ ] 配置文件更新完成
- [ ] pytest fixtures 可正常使用
- [ ] 登录场景测试可运行
- [ ] 采购单场景测试可运行
- [ ] 批量运行脚本生成报告
- [ ] 截图完整保存
- [ ] 报告 JSON 格式正确
- [ ] 进度文档已更新

---

## 执行顺序

1. Task 1 → Task 2 → Task 3 (可并行：配置、fixtures、报告模块)
2. Task 4 → Task 5 (可并行：登录测试、采购单测试)
3. Task 6 (批量运行脚本)
4. Task 7 (更新文档)
5. Task 8 (运行验证)
