# -*- coding: utf-8 -*-
import sys
import trace
import os

# 配置 trace 选项
tracer = trace.Trace(
    count=False,  # 不统计执行次数
    trace=True,  # 显示每行执行的代码
    outfile=sys.stdout  # 输出到标准输出
)

# 将项目根目录添加到Python路径中
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
