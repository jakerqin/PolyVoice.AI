"""
浏览器智能体模块

使用browser-use框架进行网络搜索和内容提取
"""

import traceback
import json
from typing import Callable
from browser_use import Agent
from app.logger import logger
from app.config import config as app_config
from langchain_openai import ChatOpenAI
from autogen import AssistantAgent

# 定义一个辅助函数，在新线程中运行异步任务
def run_async_in_thread(async_func, *args, **kwargs):
    """
    在单独的线程中运行异步函数并返回结果
    
    Args:
        async_func: 要运行的异步函数
        *args, **kwargs: 传递给异步函数的参数
        
    Returns:
        异步函数的结果
    """
    import asyncio
    import threading
    
    # 创建一个事件用于线程间同步
    result_ready = threading.Event()
    result = [None, None]  # [成功/失败标志, 结果/异常]
    
    # 在新线程中运行异步代码
    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # 运行异步函数并保存结果
            result[0] = True
            result[1] = loop.run_until_complete(async_func(*args, **kwargs))
        except Exception as e:
            # 保存异常
            result[0] = False
            result[1] = e
        finally:
            # 通知主线程结果已就绪
            result_ready.set()
            loop.close()
    
    # 启动线程
    thread = threading.Thread(target=run_async)
    thread.start()
    
    # 等待异步操作完成
    result_ready.wait()
    
    # 检查结果
    if result[0]:
        return result[1]  # 成功，返回结果
    else:
        raise result[1]  # 失败，重新抛出异常

class BrowserAgent(AssistantAgent):

    def __init__(self, message_callback: Callable = None):
        super().__init__(
            name='BrowserOperatorAgent',
            human_input_mode='NEVER',
            code_execution_config=False,
            llm_config=False
        )
        
        # 消息回调函数
        self.message_callback = message_callback

        # 注册消息回复函数（关键代码）
        self.register_reply(
            trigger=lambda msg: True,  # 使用lambda函数响应任何消息
            reply_func=self.execute_steps,
            position=0
        )

    def set_message_callback(self, callback: Callable):
        """
        设置消息回调函数
        
        Args:
            callback: 回调函数，将消息添加到列表中
        """
        self.message_callback = callback
        

    def execute_steps(self, recipient, messages, sender, config):
        """
        处理前一个智能体的返回值，构建搜索查询并执行搜索任务
        返回的格式需要是 (final: bool, reply: str)
        """
        # 获取最后一条消息内容
        last_message = messages[-1]["content"]
        
        # 如果设置了回调函数，记录接收到的消息
        self.message_callback(f"🔍 浏览器智能体收到消息: {last_message}")
        
        # 提取关键词
        keywords = json.loads(last_message).get("search_keywords", [])
        # 提取诊断摘要
        diagnosis_summary = json.loads(last_message).get("summary", "")
        self.message_callback(f"🔍 诊断摘要: {diagnosis_summary}")
        
        # 执行任务
        # 构建搜索查询
        search_query = ' '.join(keywords)
        
        # 记录日志
        log_message = f"🔍 浏览器智能体开始搜索: {search_query}"
        logger.info(log_message)
        self.message_callback(log_message)
        
        try:
            # 每次搜索创建新的Agent实例
            task = f"从www.bilibili.com网址搜索'{search_query}'的信息。找到至少3个相关结果，提取标题、URL和摘要。"
            browser_agent = Agent(
                task=task,
                llm=ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=app_config.default_llm.api_key,
                    base_url=app_config.default_llm.base_url,
                    temperature=app_config.default_llm.temperature
                ),
                use_vision=False,
                enable_memory=False
            )
            
            # 在新线程中运行异步代码
            search_result = run_async_in_thread(browser_agent.run)
            
            # 记录完成信息
            log_message = f"✅ 搜索完成，获取到结果"
            logger.info(log_message)
            
            # 处理结果并返回
            # 注意：实际结果格式取决于agent.run()返回的数据结构
            # 这里假设结果可以解析为我们需要的格式
            if isinstance(search_result, list):
                results = search_result[:5]  # 只取前5个结果
            elif isinstance(search_result, dict) and "results" in search_result:
                results = search_result["results"][:5]
            else:
                # 如果返回格式不符合预期，尝试解析或返回原始结果
                results = [{"title": "搜索结果", "url": "", "snippet": str(search_result)}]
            
            # 格式化搜索结果为字符串
            formatted_results = "我找到了以下相关资源：\n\n"
            for i, result in enumerate(results, 1):
                title = result.get("title", "无标题")
                url = result.get("url", "")
                snippet = result.get("snippet", "")
                
                formatted_results += f"{i}. **{title}**\n"
                formatted_results += f"   链接: {url}\n"
                formatted_results += f"   摘要: {snippet}\n\n"
            
            return True, formatted_results
            
        except Exception as e:
            # 获取完整的调用栈信息
            stack_trace = traceback.format_exc()
            error_message = f"❌ 浏览器搜索失败: {str(e)}"
            logger.error(error_message)
            logger.error(f"调用栈信息:\n{stack_trace}")
            
            if self.message_callback:
                self.message_callback(error_message)
                
            return False, error_message
    
    