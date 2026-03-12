# 登录场景验证设计

## 概述

验证 AI + Playwright 登录场景的完整闭环，包含渐进式测试和统计报告。

## 测试目标

- **网站**: https://erptest.epbox.cn/
- **账号**: Y59800075 / Aa123456
- **成功指标**: 页面出现 "首页"、"欢迎"、"用户"、"工作台" 之一

## 文件结构

```
backend/tests/
├── test_login.py              # 基础测试（已存在）
├── test_login_progressive.py  # 渐进式测试（新建）
└── run_validation.py          # 统计运行脚本（新建）
```

## 渐进式测试用例

### Level 1: 页面打开
- 任务: 打开登录页面
- 成功标准: 页面加载完成，steps >= 1

### Level 2: 输入填写
- 任务: 填写用户名和密码
- 成功标准: 两个字段都填写，steps >= 2

### Level 3: 完整登录
- 任务: 完整登录流程
- 成功标准: 登录成功，页面出现成功指标

## 统计报告格式

```json
{
  "test_date": "2026-03-09",
  "total_runs": 15,
  "results": {
    "level1_open_page": { "success_rate": 1.0, "avg_steps": 1.2, "avg_duration": 8.5 },
    "level2_fill_inputs": { "success_rate": 0.8, "avg_steps": 3.5, "avg_duration": 25.0 },
    "level3_full_login": { "success_rate": 0.6, "avg_steps": 5.0, "avg_duration": 45.0 }
  }
}
```

## 验收标准

| 指标 | 目标值 |
|------|--------|
| Level 1 成功率 | 100% |
| Level 2 成功率 | ≥ 80% |
| Level 3 成功率 | ≥ 60% |
| 单步推理耗时 | ≤ 10s |
| 截图完整率 | 100% |

## 实现任务

1. 编写 `test_login_progressive.py`
2. 编写 `run_validation.py`
3. 运行验证并收集数据
4. 分析结果、更新进度文档
