"""记忆模块 - 存储最近 N 步的操作历史，用于 LLM 决策上下文"""

from backend.agent_simple.types import Step, Action


class Memory:
    """短记忆模块 - 存储最近 N 步的操作历史"""

    def __init__(self, max_steps: int = 5):
        """初始化记忆模块

        Args:
            max_steps: 最大记忆步数，默认 5 步
        """
        self.max_steps = max_steps
        self.steps: list[Step] = []

    def add_step(self, step: Step) -> None:
        """添加步骤，超出容量时移除最旧的

        Args:
            step: 要添加的步骤记录
        """
        self.steps.append(step)
        # 超出容量时移除最旧的
        if len(self.steps) > self.max_steps:
            self.steps.pop(0)

    def get_recent_steps(self) -> list[Step]:
        """获取最近的步骤（最多 max_steps 个）

        Returns:
            最近步骤列表
        """
        return self.steps.copy()

    def get_failed_actions(self) -> list[tuple[Action, str]]:
        """获取失败的动作及其错误信息

        Returns:
            列表，每项为 (Action, 错误信息) 元组
        """
        return [
            (step.action, step.result.error or "未知错误")
            for step in self.steps
            if not step.result.success
        ]

    def format_for_prompt(self) -> str:
        """格式化为 Prompt 文本

        Returns:
            格式化的记忆文本，包含操作记录和失败警告
        """
        if not self.steps:
            return "## 📋 操作记录\n（这是第一步）"

        parts = []

        # 1. 最近操作记录
        parts.append("## 📋 最近操作记录")
        for step in self.steps:
            status = "✅ 成功" if step.result.success else f"❌ {step.result.error or '失败'}"

            # 动作描述
            action_desc = f"{step.action.action}"
            if step.action.target:
                action_desc += f" \"{step.action.target}\""
            if step.action.value:
                action_desc += f" = \"{step.action.value}\""

            parts.append(f"Step {step.step_num}: {action_desc}")
            parts.append(f"  思考: {step.action.thought}")
            parts.append(f"  结果: {status}")

        # 2. 失败动作警告
        failed_actions = self.get_failed_actions()
        if failed_actions:
            parts.append("\n## ⚠️ 失败动作警告")
            for action, error in failed_actions:
                target_desc = f"目标=\"{action.target}\"" if action.target else ""
                parts.append(f"- {action.action} {target_desc} → {error}")
                parts.append(f"  建议: {self._generate_suggestion(error)}")

        return "\n".join(parts)

    def _generate_suggestion(self, error: str) -> str:
        """根据错误信息生成替代建议

        Args:
            error: 错误信息

        Returns:
            建议文本
        """
        error_lower = error.lower()

        if "元素未找到" in error or "not found" in error_lower:
            return "尝试使用 ID、placeholder、aria-label 或 name 属性定位"
        elif "超时" in error or "timeout" in error_lower:
            return "等待页面加载完成后再操作，或使用 wait 动作"
        elif "不可见" in error or "not visible" in error_lower:
            return "先滚动页面使元素可见，或展开隐藏的菜单"
        elif "被禁用" in error or "disabled" in error_lower:
            return "检查是否需要先完成前置操作"
        else:
            return "尝试换一种定位方式或操作顺序"
