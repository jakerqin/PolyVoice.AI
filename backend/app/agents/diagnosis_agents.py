"""
诊断智能体系统

使用AutoGen构建的多智能体协作系统，负责提取诊断内容并调用浏览器智能体
"""

import json
from typing import Dict, Any, AsyncGenerator, Callable
from app.logger import logger
from app.prompt.diagnosis import DIAGNOSIS_SYSTEM_PROMPT
from app.prompt.browser import BROWSER_SYSTEM_PROMPT
from autogen import Agent, AssistantAgent, UserProxyAgent, config_list_from_json

from .browser_agent import BrowserAgent

class DiagnosisAgents:
    """
    诊断智能体系统，使用AutoGen框架构建
    """
    
    def __init__(self, callback: Callable[[str], None] = None):
        """
        初始化诊断智能体系统
        
        Args:
            callback: 回调函数，用于流式返回日志
        """
        self.callback = callback
        self.browser_agent = BrowserAgent(callback)
        
        # 配置LLM，这里使用系统环境变量中的API密钥
        self.llm_config = {
            "config_list": config_list_from_json(env_or_file="OPENAI_API_KEY"),
            "temperature": 0.2,
        }
        
        # 创建内容提取智能体
        self.content_extractor = AssistantAgent(
            name="ContentExtractor",
            system_message=DIAGNOSIS_SYSTEM_PROMPT,
            llm_config=self.llm_config,
        )
        
        # 创建浏览器代理智能体
        self.browser_proxy = UserProxyAgent(
            name="BrowserProxy",
            system_message=BROWSER_SYSTEM_PROMPT,
            human_input_mode="NEVER",
            llm_config=self.llm_config,
        )
        
        # 注册消息处理函数
        self._register_message_handlers()
    
    def _register_message_handlers(self):
        """注册智能体的消息处理函数，以便捕获并流式输出对话内容"""
        
        # 原始发送消息方法
        original_send = Agent.send
        
        # 包装发送方法以捕获消息
        def send_with_logging(self, message, recipient, request_reply=None, silent=False):
            if not silent and self.callback and isinstance(message, str):
                sender_name = self.name if hasattr(self, "name") else "Agent"
                log_message = f"🤖 {sender_name}: {message[:100]}..."
                self.callback(log_message)
            
            return original_send(self, message, recipient, request_reply, silent)
        
        # 应用包装后的方法
        Agent.send = send_with_logging
    
    async def analyze_content(self, diagnosis_content: str, diagnosis_type: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        分析诊断内容并搜索相关资源
        
        Args:
            diagnosis_content: 诊断内容
            diagnosis_type: 诊断类型（pronunciation, grammar, etc）
            
        Yields:
            处理状态和结果
        """
        # 记录开始处理
        log_message = f"🚀 开始处理{diagnosis_type}诊断内容"
        logger.info(log_message)
        if self.callback:
            self.callback(log_message)
        
        yield {"status": "start", "message": log_message}
        
        try:
            # 创建一个任务，让内容提取智能体分析诊断内容
            extractor_prompt = f"""
            请分析以下{diagnosis_type}诊断内容，提取关键问题和搜索关键词：

            ```
            {diagnosis_content}
            ```

            请提取最重要的语言学术语和问题，以便搜索相关教学资源。
            """
            
            # 发送消息给内容提取智能体
            await self.content_extractor.a_initiate_chat(
                self.browser_proxy,
                message=extractor_prompt
            )
            
            # 从内容提取智能体的最后一条消息中解析JSON
            last_message = self.content_extractor.last_message()
            
            # 尝试从消息中提取JSON
            try:
                # 查找消息中的JSON部分
                json_start = last_message["content"].find("{")
                json_end = last_message["content"].rfind("}") + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = last_message["content"][json_start:json_end]
                    extracted_data = json.loads(json_str)
                else:
                    # 如果没有找到JSON，则手动构建
                    extracted_data = {
                        "key_issues": [diagnosis_type + " issues"],
                        "search_keywords": [diagnosis_content.split()[:3]],
                        "summary": diagnosis_content[:100]
                    }
            except Exception as e:
                logger.error(f"解析JSON失败: {str(e)}")
                # 构建一个默认的提取结果
                extracted_data = {
                    "key_issues": [diagnosis_type + " problems"],
                    "search_keywords": [w for w in diagnosis_content.split()[:5] if len(w) > 3],
                    "summary": diagnosis_content[:100]
                }
            
            # 返回提取的数据
            yield {
                "status": "extracted", 
                "message": f"📑 提取了关键内容: {', '.join(extracted_data.get('search_keywords', []))}",
                "data": extracted_data
            }
            
            # 使用提取的关键词调用浏览器智能体
            search_keywords = extracted_data.get("search_keywords", [])
            if not search_keywords:
                search_keywords = [w for w in diagnosis_content.split()[:5] if len(w) > 3]
            
            # 执行搜索
            async for result in self.browser_agent.search_content(search_keywords, diagnosis_type):
                yield result
                
        except Exception as e:
            error_message = f"❌ 处理诊断内容失败: {str(e)}"
            logger.error(error_message)
            if self.callback:
                self.callback(error_message)
            
            yield {"status": "error", "message": error_message}
    
    async def close(self):
        """清理资源"""
        await self.browser_agent.close()


async def start_diagnosis_session(diagnosis_content: str, diagnosis_type: str, callback: Callable[[str], None] = None) -> AsyncGenerator[Dict[str, Any], None]:
    """
    启动诊断会话
    
    Args:
        diagnosis_content: 诊断内容
        diagnosis_type: 诊断类型（pronunciation, grammar, etc）
        callback: 回调函数，用于流式返回日志
        
    Yields:
        处理状态和结果
    """
    agents = DiagnosisAgents(callback)
    
    try:
        async for result in agents.analyze_content(diagnosis_content, diagnosis_type):
            yield result
    finally:
        await agents.close() 