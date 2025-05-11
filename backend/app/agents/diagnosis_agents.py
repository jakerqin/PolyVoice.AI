"""
诊断智能体系统

使用AutoGen构建的多智能体协作系统，负责提取诊断内容并调用浏览器智能体
"""

import json
from app.logger import logger
from app.prompt.diagnosis import DIAGNOSIS_SYSTEM_PROMPT
from app.prompt.browser import BROWSER_SYSTEM_PROMPT
from app.prompt.diagnosis_extract import DIAGNOSIS_EXTRACT_SYSTEM_PROMPT
from autogen import AssistantAgent, UserProxyAgent
from app.config import config

from .browser_agent import BrowserAgent

class DiagnosisAgents:
    """
    诊断智能体系统，使用AutoGen框架构建
    """
    
    def __init__(self):
        """
        初始化诊断智能体系统
        
        """
        self.browser_agent = BrowserAgent()
        
        # 配置LLM，这里使用系统环境变量中的API密钥
        self.llm_config = {
            "config_list": [{
                "model": config.default_llm.model,
                "api_key": config.default_llm.api_key,
                "base_url": config.default_llm.base_url,
                "api_type": config.default_llm.api_type or "",
                "max_tokens": config.default_llm.max_tokens or 4096
            }],
            "temperature": config.default_llm.temperature or 0.7
        }
        
        # 创建内容提取智能体
        self.content_extractor = AssistantAgent(
            name="ContentExtractor",
            system_message=DIAGNOSIS_SYSTEM_PROMPT,
            llm_config=self.llm_config,
        )
        
    
    async def analyze_content(self, diagnosis_content: str, diagnosis_type: str):
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
        
        yield {"type": "log", "data": log_message}
        
        try:
            # 创建一个任务，让内容提取智能体分析诊断内容
            extractor_prompt = DIAGNOSIS_EXTRACT_SYSTEM_PROMPT.format(diagnosis_type=diagnosis_type, diagnosis_content=diagnosis_content)
            
            # 创建一个简单的用户代理来接收回复，不启动完整的对话
            temp_user = UserProxyAgent(
                name="TempUser",
                human_input_mode="NEVER",
                code_execution_config=False
            )
            
            # 让ContentExtractor回复一次消息
            await self.content_extractor.a_initiate_chat(
                temp_user,
                message=extractor_prompt
            )
            
            # 从内容提取智能体的最后一条消息中获取内容
            messages = self.content_extractor.chat_messages[temp_user]
            if messages and len(messages) > 0:
                result_content = messages[-1]["content"]
            else:
                raise Exception("未能获取到内容提取智能体的响应")
            
            # 尝试从消息中提取JSON
            try:
                # 查找消息中的JSON部分
                json_start = result_content.find("{")
                json_end = result_content.rfind("}") + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = result_content[json_start:json_end]
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
            log_message = f"extract_agent: 📑 提取了关键内容: {extracted_data}"
            yield {
                "type": "log", 
                "data": f"📑 提取了关键内容: {', '.join(extracted_data.get('search_keywords', []))}",
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
            
            yield {"type": "error", "data": error_message}
    
    async def close(self):
        """清理资源"""
        await self.browser_agent.close()


async def start_diagnosis_session(diagnosis_content: str, diagnosis_type: str):
    """
    启动诊断会话
    
    Args:
        diagnosis_content: 诊断内容
        diagnosis_type: 诊断类型（pronunciation, grammar, etc）
        
    Yields:
        处理状态和结果
    """
    agents = DiagnosisAgents()
    
    async for result in agents.analyze_content(diagnosis_content, diagnosis_type):
        yield result
