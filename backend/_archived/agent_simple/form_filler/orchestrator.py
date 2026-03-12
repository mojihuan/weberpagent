"""表单填写编排器 - 协调多 Agent 工作流程"""

import logging

from playwright.async_api import Page

from backend.llm.base import BaseLLM
from backend.llm.factory import LLMFactory
from backend.agent_simple.types import PageState
from backend.agent_simple.form_filler.types import FillResult, ReviewResult, GeneratedCode
from backend.agent_simple.form_filler.code_generator import CodeGenerator
from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.form_filler.code_optimizer import CodeOptimizer
from backend.agent_simple.form_filler.sandbox import execute_code

logger = logging.getLogger(__name__)


class FormFiller:
    """表单填写编排器 - 协调 CodeGenerator、CodeReviewer、CodeOptimizer"""

    MAX_REVIEW_ROUNDS = 3

    def __init__(
        self,
        page: Page,
        llm: BaseLLM | None = None,
        generator_llm: BaseLLM | None = None,
        optimizer_llm: BaseLLM | None = None,
        reviewer_llm: BaseLLM | None = None,
    ):
        """初始化表单填写编排器

        Args:
            page: Playwright 页面对象
            llm: 通用 LLM 实例（向后兼容，用于所有模块）
            generator_llm: 代码生成专用 LLM
            optimizer_llm: 代码优化专用 LLM
            reviewer_llm: 代码审查专用 LLM

        优先级：专用 LLM > 通用 LLM > 工厂创建
        """
        self.page = page

        # 确定各模块使用的 LLM（优先级：专用 > 通用 > 工厂）
        if generator_llm:
            gen_llm = generator_llm
        elif llm:
            gen_llm = llm
        else:
            gen_llm = LLMFactory.get_code_generator_llm()

        if optimizer_llm:
            opt_llm = optimizer_llm
        elif llm:
            opt_llm = llm
        else:
            opt_llm = LLMFactory.get_code_optimizer_llm()

        if reviewer_llm:
            rev_llm = reviewer_llm
        elif llm:
            rev_llm = llm
        else:
            rev_llm = LLMFactory.get_code_reviewer_llm()

        # 初始化子模块
        self.code_generator = CodeGenerator(gen_llm)
        self.code_reviewer = CodeReviewer(rev_llm)
        self.code_optimizer = CodeOptimizer(opt_llm)

        # 保留通用 LLM 引用（向后兼容）
        self.llm = gen_llm

        logger.info(
            f"FormFiller 初始化完成: "
            f"generator={gen_llm.model_name}, "
            f"optimizer={opt_llm.model_name}, "
            f"reviewer={rev_llm.model_name}"
        )

    async def fill_form(self, state: PageState, task: str) -> FillResult:
        """填写表单

        流程：
        1. 生成代码
        2. 审查循环（最多 3 轮）
        3. 执行代码
        4. 返回结果
        """
        logger.info(f"开始表单填写流程，任务: {task[:50]}...")

        # 1. 生成代码
        try:
            generated = await self.code_generator.generate(state, task)
        except Exception as e:
            logger.error(f"代码生成失败: {e}")
            return FillResult(success=False, error=f"代码生成失败: {str(e)}")

        code = generated.code

        # 2. 审查循环
        for round_num in range(self.MAX_REVIEW_ROUNDS):
            review_result = await self.code_reviewer.review(code, state.elements)

            if review_result.approved:
                logger.info(f"代码审查通过（第 {round_num + 1} 轮）")
                break

            logger.info(f"代码审查未通过（第 {round_num + 1} 轮），尝试优化...")

            try:
                code = await self.code_optimizer.optimize(
                    code, state.elements, review_result.issues
                )
            except Exception as e:
                logger.error(f"代码优化失败: {e}")

        # 3. 执行代码
        logger.info("=" * 60)
        logger.info("📝 准备执行生成的代码:")
        logger.info("-" * 60)
        for line_num, line in enumerate(code.split('\n'), 1):
            logger.info(f"{line_num:3d} | {line}")
        logger.info("-" * 60)
        logger.info("=" * 60)

        try:
            result = await self._execute_code(code)
            logger.info("✅ 代码执行成功")
            if result.get("stdout"):
                logger.info(f"📤 标准输出:\n{result['stdout']}")
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ 代码执行失败: {error_msg}")

            # 尝试一次优化后重新执行
            logger.info("🔄 尝试优化代码后重新执行...")
            try:
                optimized_code = await self.code_optimizer.optimize(
                    code, state.elements, execution_error=error_msg
                )
                logger.info("📝 优化后的代码:")
                logger.info("-" * 60)
                for line_num, line in enumerate(optimized_code.split('\n'), 1):
                    logger.info(f"{line_num:3d} | {line}")
                logger.info("-" * 60)

                result = await self._execute_code(optimized_code)
                code = optimized_code
                logger.info("✅ 优化后执行成功")
                if result.get("stdout"):
                    logger.info(f"📤 标准输出:\n{result['stdout']}")
            except Exception as retry_error:
                return FillResult(
                    success=False,
                    error=f"执行失败: {error_msg}，重试失败: {str(retry_error)}",
                )

        return FillResult(success=True, code=code)

    async def _execute_code(self, code: str) -> dict:
        """执行代码

        Returns:
            执行结果字典，包含 success, stdout, locals 等
        """
        result = await execute_code(code, {"page": self.page})
        if not result["success"]:
            raise Exception(result.get("error", "未知执行错误"))
        return result