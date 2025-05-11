"""
浏览器智能体模块

使用browser-use框架进行网络搜索和内容提取
"""

import traceback
from typing import List
from browser_use import Agent
from app.logger import logger
from app.config import config
from langchain_openai import ChatOpenAI

class BrowserAgent:
    """
    浏览器智能体，负责执行网络搜索和内容提取任务
    """
    
    async def search_content(self, keywords: List[str], query_type: str):
        """
        搜索相关教学内容
        
        Args:
            keywords: 关键词列表
            query_type: 查询类型（pronunciation, grammar, etc）
            
        Yields:
            搜索状态更新和结果
        """
        # 构建搜索查询
        search_query = f"{' '.join(keywords)} {query_type} 教学视频"
        
        # 记录日志
        log_message = f"🔍 浏览器智能体开始搜索: {search_query}"
        logger.info(log_message)
        yield {"type": "log", "data": log_message}
        
        try:
            # 创建一个browser-use的Agent实例
            agent = Agent(
                task=f"搜索并获取有关'{search_query}'的信息。找到至少5个相关结果，提取标题、URL和摘要。",
                llm=ChatOpenAI(**config.default_llm)
            )
            
            # 运行代理，获取搜索结果
            search_result = await agent.run()
            
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
            
            yield {
                "type": "complete", 
                "data": results
            }
            
        except Exception as e:
            # 获取完整的调用栈信息
            stack_trace = traceback.format_exc()
            error_message = f"❌ 浏览器搜索失败: {str(e)}"
            logger.error(error_message)
            logger.error(f"调用栈信息:\n{stack_trace}")
            yield {"type": "error", "data": error_message}