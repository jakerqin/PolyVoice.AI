from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, AsyncGenerator

from app.logger import logger


class BaseLLM(ABC):
    """大语言模型基类
    
    所有具体的大语言模型实现都应该继承自这个基类，并实现其抽象方法。
    这个基类定义了所有 LLM 接口应该具备的基本方法和属性。
    """
    
    def __init__(self, config):
        """
        初始化大语言模型基类
        """
        self.model_name=config.model
        self.api_key=config.api_key
        self.base_url=config.base_url
        self.max_tokens=config.max_tokens
        self.temperature=config.temperature
        
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self):
        """
        初始化底层客户端
        
        这个方法应该由子类实现，用于初始化模型客户端。
        """
        pass
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        stop: Optional[Union[str, List[str]]] = None
    ) -> str:
        """
        根据消息列表生成文本响应
        
        Args:
            messages: 消息列表，包含角色和内容，如 [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
            stop: 停止序列
            
        Returns:
            生成的文本响应
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        stop: Optional[Union[str, List[str]]] = None
    ) -> AsyncGenerator[str, None]:
        """
        根据消息列表流式生成文本响应
        
        Args:
            messages: 消息列表，包含角色和内容
            stop: 停止序列
            
        Yields:
            生成的文本片段
        """
        pass 