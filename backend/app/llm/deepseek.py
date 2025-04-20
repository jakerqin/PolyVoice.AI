import openai
from typing import Dict, List, Optional, Union, AsyncGenerator

from app.logger import logger
from app.llm.base import BaseLLM
from app.config import config

# 从配置文件中获取DeepSeek的配置
LLM_KEY = 'default'

class DeepSeekLLM(BaseLLM):
    """使用DeepSeek的大语言模型类"""

    def __init__(self):
        """
        初始化DeepSeek模型

        """
        # 调用父类初始化
        super().__init__(config.llm[LLM_KEY])

    def _initialize_client(self):
        """初始化OpenAI客户端"""
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        logger.info(f"DeepSeekLLM 已初始化客户端，模型: {self.model_name}")

    async def generate(
        self,
        messages: List[Dict[str, str]],
        stop: Optional[Union[str, List[str]]] = None
    ) -> str:
        """
        根据消息列表生成文本响应
        
        Args:
            messages: 消息列表，包含角色和内容
            stop: 停止序列
            
        Returns:
            生成的文本响应
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop=stop
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"生成响应失败: {e}")
            raise
    
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
        try:
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop=stop,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    logger.debug(f"流式生成块: {content}")
                    yield content
        except Exception as e:
            logger.error(f"流式生成响应失败: {e}")
            raise 