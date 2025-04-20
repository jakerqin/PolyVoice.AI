"""
大语言模型模块
提供了基础接口和多种模型实现
"""

from app.llm.base import BaseLLM
from app.llm.deepseek import DeepSeekLLM

__all__ = [
    'BaseLLM',
    'DeepSeekLLM',
] 