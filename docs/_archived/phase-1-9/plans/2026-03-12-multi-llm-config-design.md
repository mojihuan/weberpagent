# 多模型配置方案设计

## 概述

为不同 Agent 模块配置不同的大模型，优化成本和性能。

## 模型分配

| 模块 | 模型 | 说明 |
|------|------|------|
| SimpleAgent._reflect | glm-5 | 反思功能，需要视觉能力 |
| Decision | qwen3.5-plus | 决策模块，需要视觉能力 |
| FormFiller/CodeGenerator | glm-5 | 生成 Playwright 代码 |
| FormFiller/CodeOptimizer | glm-5 | 优化失败代码 |
| FormFiller/CodeReviewer | qwen3-coder-next | LLM 语义审查（新增） |

## 技术方案

### 配置文件结构

```yaml
# config/llm_config.yaml
llm:
  api_key: ${DASHSCOPE_API_KEY}
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1

  agents:
    simple_agent:
      reflect: glm-5
    decision:
      model: qwen3.5-plus
    form_filler:
      code_generator: glm-5
      code_optimizer: glm-5
      code_reviewer: qwen3-coder-next
```

### 核心组件

1. **LLMConfig** - 配置加载类
   - 从 YAML 文件加载配置
   - 支持环境变量替换
   - 提供默认值

2. **LLMFactory** - LLM 实例工厂
   - 根据模块名称创建对应的 LLM 实例
   - 缓存已创建的实例（单例模式）

3. **CodeReviewer 改造**
   - 新增 LLM 语义审查能力
   - 保留现有规则检查
   - 两阶段审查：规则检查 → LLM 审查

### 代码改动

1. 新增文件：
   - `config/llm_config.yaml` - 配置文件
   - `backend/llm/config.py` - 配置加载
   - `backend/llm/factory.py` - LLM 工厂

2. 修改文件：
   - `backend/agent_simple/agent.py` - 使用工厂获取反思 LLM
   - `backend/agent_simple/decision.py` - 使用工厂获取决策 LLM
   - `backend/agent_simple/form_filler/orchestrator.py` - 传递不同的 LLM 实例
   - `backend/agent_simple/form_filler/code_generator.py` - 接收专用 LLM
   - `backend/agent_simple/form_filler/code_optimizer.py` - 接收专用 LLM
   - `backend/agent_simple/form_filler/code_reviewer.py` - 新增 LLM 审查

## API 兼容性

使用百炼按量付费 API：
- API Key 格式：`sk-xxxxx`
- Base URL：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 兼容 OpenAI API 格式

## 测试计划

1. 单元测试：配置加载、工厂创建
2. 集成测试：各模块使用正确的模型
3. 端到端测试：完整流程验证

## 风险

- glm-5 视觉能力需验证
- qwen3-coder-next 审查效果需评估
