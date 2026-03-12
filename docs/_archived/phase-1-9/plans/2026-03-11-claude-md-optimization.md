# CLAUDE.md 优化设计

## 背景

当前 CLAUDE.md 文件约 460 行，过于臃肿。根据 CLAUDE.md 最佳实践：
- **Less is more**: < 300 行最佳，理想情况 60-150 行
- **普遍适用性**: 内容应对每个任务都相关
- **渐进式披露**: 详细内容放在单独文件

## 目标

将 CLAUDE.md 精简至 ~80 行，只保留核心信息。

## 设计方案

### 保留内容 (~80 行)

```
CLAUDE.md
│
├── 1. Project Overview (~10 行)
│   └── 一句话说明项目目的 + 解决什么问题
│
├── 2. Tech Stack (~15 行)
│   └── Backend + Frontend 技术列表
│
├── 3. Architecture (~25 行)
│   ├── 简化版架构图（ASCII）
│   ├── 模块职责表（4 行）
│   └── 反思策略表（3 行）
│
├── 4. Key Commands (~20 行)
│   ├── Backend: venv, install, test
│   ├── Frontend: install, dev, build
│   └── Agent: 运行命令（1-2 个）
│
└── 5. Reference (~10 行)
    └── 指向详细文档的链接列表
```

### 移出/删除内容

| 原内容 | 处理方式 |
|--------|----------|
| 技术方向变更 (2026-03-09) | 删除 - 历史信息，已过时 |
| 架构升级 (2026-03-11) | 删除 - 历史信息，已过时 |
| 详细项目结构 (~50 行) | 删除 - Claude 可以自己探索 |
| LLM Integration 代码示例 | 移到 `docs/llm-integration.md` |
| Implementation Phases | 删除 - 已有 `docs/progress.md` |
| 阶段完成规则 | 移到 `docs/workflow.md` |
| 工时记录规则 | 移到 `docs/workflow.md` |
| Agent 调优记录规则 | 删除 - 已有 `docs/3_agent调优.md` |
| POC Acceptance Criteria | 删除 - 不是每次编码都需要 |
| Test Scenarios | 删除 - 不是每次编码都需要 |

### 新建文件

```
docs/
├── workflow.md          # 阶段完成规则 + 工时记录规则
└── llm-integration.md   # LLM 接口 + 代码示例
```

## 实施步骤

1. 创建 `docs/workflow.md` - 移入阶段完成规则 + 工时记录规则
2. 创建 `docs/llm-integration.md` - 移入 LLM 集成相关内容
3. 重写 `CLAUDE.md` - 按新结构精简
4. 验证新文件内容完整

## 参考资料

- [CLAUDE.md Best Practices - UX Planet](https://uxplanet.org/claude-md-best-practices-1ef4f861ce7c)
- [Writing a good CLAUDE.md - HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [CLAUDE.md Best Practices - Arize](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
