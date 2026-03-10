"""Agent 类型定义"""

from enum import Enum
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """支持的动作类型"""

    NAVIGATE = "navigate"
    CLICK = "click"
    INPUT = "input"
    HOVER = "hover"
    WAIT = "wait"
    DONE = "done"


class InteractiveElement(BaseModel):
    """可交互元素"""

    index: int = Field(description="元素索引")
    tag: str = Field(description="标签名 (BUTTON, INPUT, A, ...)")
    text: str = Field(default="", description="显示文本（截取前 50 字符）")
    type: str | None = Field(default=None, description="input 类型")
    id: str | None = Field(default=None, description="元素 id")
    placeholder: str | None = Field(default=None, description="占位文本")
    name: str | None = Field(default=None, description="元素 name 属性")
    aria_label: str | None = Field(default=None, description="aria-label 属性")
    title: str | None = Field(default=None, description="title 属性（悬停提示）")


class PageState(BaseModel):
    """页面状态快照"""

    screenshot_base64: str = Field(description="截图 base64 编码")
    url: str = Field(description="当前页面 URL")
    title: str = Field(description="页面标题")
    elements: list[InteractiveElement] = Field(
        default_factory=list, description="可交互元素列表"
    )
    state_hash: str | None = Field(default=None, description="页面状态哈希")


class Action(BaseModel):
    """LLM 输出的动作"""

    thought: str = Field(description="AI 的思考过程")
    action: str = Field(description="动作类型 (navigate/click/input/wait/done)")
    target: str | None = Field(default=None, description="目标元素描述")
    value: str | None = Field(default=None, description="输入值 (input 时使用)")
    done: bool = Field(default=False, description="任务是否完成")
    result: str | None = Field(default=None, description="任务结果 (done 时使用)")


class ActionResult(BaseModel):
    """动作执行结果"""

    success: bool = Field(description="执行是否成功")
    error: str | None = Field(default=None, description="错误信息")
    screenshot_path: str | None = Field(default=None, description="截图保存路径")


class Step(BaseModel):
    """单步执行记录"""

    step_num: int = Field(description="步骤编号")
    state: PageState = Field(description="页面状态快照")
    action: Action = Field(description="执行的动作")
    result: ActionResult = Field(description="执行结果")


class AgentResult(BaseModel):
    """Agent 执行结果"""

    success: bool = Field(description="任务是否成功")
    result: str | None = Field(default=None, description="任务结果描述")
    error: str | None = Field(default=None, description="错误信息")
    steps: list[Step] = Field(default_factory=list, description="执行步骤记录")


class ReflectionStrategy(str, Enum):
    """反思策略"""

    RETRY = "retry"  # 原样重试
    ALTERNATIVE = "alternative"  # 替代方案
    SKIP = "skip"  # 跳过当前步骤
    ROLLBACK = "rollback"  # 回退到上一步


class Reflection(BaseModel):
    """反思结果"""

    reason: str = Field(description="失败原因分析")
    strategy: ReflectionStrategy = Field(description="修复策略")
    adjusted_action: Action | None = Field(
        default=None, description="调整后的动作（alternative 策略时使用）"
    )
