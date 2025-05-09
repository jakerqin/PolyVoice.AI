"""
高级诊断智能体系统

使用AutoGen框架构建的多智能体系统，用于处理语言诊断任务：
1. 内容提取智能体：分析诊断内容，提取关键信息
2. 浏览器智能体：搜索并获取相关教学资源
"""

from .diagnosis_agents import start_diagnosis_session 