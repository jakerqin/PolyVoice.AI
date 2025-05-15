"""
诊断智能体系统

使用AutoGen构建的多智能体协作系统，负责提取诊断内容并调用浏览器智能体
"""
import traceback
from app.logger import logger
from app.prompt.diagnosis import DIAGNOSIS_SYSTEM_PROMPT
from app.prompt.diagnosis_extract import DIAGNOSIS_EXTRACT_SYSTEM_PROMPT
from autogen import AssistantAgent, GroupChat, GroupChatManager
from app.config import config

from .browser_agent import BrowserAgent

class ContentExtractorAgent(AssistantAgent):
    """
    自定义内容提取智能体，可以将LLM的响应发送到前端
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加回调函数属性，用于向外部传递消息
        self.message_callback = None
    
    def set_message_callback(self, callback):
        """设置消息回调函数，用于将LLM响应传递给外部处理"""
        self.message_callback = callback
    
    def _generate_reply(self, messages=None, sender=None, config=None):
        """
        重写_generate_reply方法以捕获LLM响应
        注意：这里使用同步方法，不是异步方法
        """
        # 调用父类方法获取LLM响应
        reply = super()._generate_reply(messages, sender, config)
        
        if reply and self.message_callback:
            # 记录日志
            log_message = f"💬 ContentExtractor响应: {reply}"
            logger.info(log_message)
            
            # 通过回调函数发送到前端
            self.message_callback(log_message)
        
        return reply

class DiagnosisAgents:
    """
    诊断智能体系统，使用AutoGen框架构建
    """
    
    def __init__(self):
        """
        初始化诊断智能体系统
        
        """
        # 配置LLM，这里使用系统环境变量中的API密钥
        self.llm_config = {
            "config_list": [{
                "model": config.default_llm.model,
                "api_key": config.default_llm.api_key,
                "base_url": config.default_llm.base_url,
                "api_type": config.default_llm.api_type or "openai",
                "max_tokens": config.default_llm.max_tokens or 4096,
            }],
            "temperature": config.default_llm.temperature or 0.7
        }

        # 创建内容提取智能体，使用自定义的ContentExtractorAgent
        self.contentExtractor = ContentExtractorAgent(
            name="ContentExtractor",
            system_message=DIAGNOSIS_SYSTEM_PROMPT,
            llm_config=self.llm_config,
        )
        self.browserAgent = BrowserAgent()
        
        # 存储要发送到前端的消息
        self.frontend_messages = []
    
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
        
        # 清空之前的消息
        self.frontend_messages = []
        
        # 设置回调函数，用于收集LLM回复
        def collect_message(message):
            """普通函数，将消息添加到列表中"""
            self.frontend_messages.append({"type": "log", "data": message})
            
        # 将回调函数设置到ContentExtractor
        self.contentExtractor.set_message_callback(collect_message)
        self.browserAgent.set_message_callback(collect_message)
        
        try:
            extractor_prompt = DIAGNOSIS_EXTRACT_SYSTEM_PROMPT.format(diagnosis_type=diagnosis_type, diagnosis_content=diagnosis_content)
            
            groupchat = GroupChat(
                agents=[
                    self.contentExtractor,
                    self.browserAgent
                ],
                messages=[],
                max_round=2,
                speaker_selection_method="round_robin"  # 使用轮流发言模式，确保每个智能体都有机会发言
            )
            manager = GroupChatManager(
                groupchat=groupchat,
                llm_config=self.llm_config
            )
            
            # 启动对话 - 注意这里要同步调用，不需要await
            manager.initiate_chat(
                recipient=self.contentExtractor,  # 发送给内容提取智能体
                message=extractor_prompt
            )
            
            # 将收集到的消息发送到前端
            for message in self.frontend_messages:
                yield message
            
            # 完成处理
            yield {"type": "complete", "data": "诊断分析完成"}
            
        except Exception as e:
            error_message = f"❌ 处理诊断内容失败: {str(e)}"
            logger.error(error_message)
            logger.error(f"调用栈信息:\n{traceback.format_exc()}")
            yield {"type": "error", "data": error_message}
    

agents = DiagnosisAgents()

async def start_diagnosis_session(diagnosis_content: str, diagnosis_type: str):
    """
    启动诊断会话
    
    Args:
        diagnosis_content: 诊断内容
        diagnosis_type: 诊断类型（pronunciation, grammar, etc）
        
    Yields:
        处理状态和结果
    """
    async for result in agents.analyze_content(diagnosis_content, diagnosis_type):
        yield result
