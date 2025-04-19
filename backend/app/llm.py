from typing import Dict, List, Optional, Union

import openai
from app.logger import logger

from app.config import config


class DeepSeekLLM:
    """使用DeepSeek-V3的大语言模型类"""

    def __init__(self):
        """
        初始化DeepSeek-V3模型
        
        Args:
            model_name: 模型名称，默认为deepseek-chat
        """
        self.model_name = config.llm["default"].model
        self.api_key = config.llm["default"].api_key
        self.base_url = config.llm["default"].base_url
        self.max_tokens = config.llm["default"].max_tokens
        self.temperature = config.llm["default"].temperature
        
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        logger.info(f"DeepSeekLLM initialized with model: {self.model_name}")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        stop: Optional[Union[str, List[str]]] = None
    ) -> str:
        """
        生成文本响应
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成令牌数
            stop: 停止序列
            
        Returns:
            生成的文本响应
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature= self.temperature,
                max_tokens= self.max_tokens,
                stop=stop
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def generate_with_history(
        self,
        messages: List[Dict[str, str]],
        stop: Optional[Union[str, List[str]]] = None
    ) -> str:
        """
        使用对话历史生成文本响应
        
        Args:
            messages: 对话历史消息列表
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成令牌数
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
            logger.error(f"Error generating response with history: {e}")
            raise 