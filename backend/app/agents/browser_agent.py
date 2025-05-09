"""
浏览器智能体模块

使用browser-use框架进行网络搜索和内容提取
"""

import asyncio
import logging
from typing import List, Dict, Any, AsyncGenerator, Callable

from browser_use import BrowserUse

logger = logging.getLogger(__name__)

class BrowserAgent:
    """
    浏览器智能体，负责执行网络搜索和内容提取任务
    """
    
    def __init__(self, callback: Callable[[str], None] = None):
        """
        初始化浏览器智能体
        
        Args:
            callback: 回调函数，用于流式返回日志
        """
        self.browser = BrowserUse()
        self.callback = callback
    
    async def search_content(self, keywords: List[str], query_type: str) -> AsyncGenerator[Dict[str, Any], None]:
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
        
        # 记录日志并通过回调发送
        log_message = f"🔍 浏览器智能体开始搜索: {search_query}"
        logger.info(log_message)
        if self.callback:
            self.callback(log_message)
        
        yield {"status": "searching", "message": log_message}
        
        try:
            # 使用browser-use执行搜索
            search_result = await self.browser.search(search_query)
            
            log_message = f"✅ 搜索完成，找到 {len(search_result.snippets)} 条结果"
            logger.info(log_message)
            if self.callback:
                self.callback(log_message)
            
            # 返回搜索结果
            yield {
                "status": "complete", 
                "message": log_message,
                "results": [
                    {
                        "title": item.title,
                        "url": item.url,
                        "snippet": item.snippet
                    } for item in search_result.snippets[:5]  # 仅返回前5个结果
                ]
            }
            
            # 为前3个结果提取更丰富的内容
            for i, item in enumerate(search_result.snippets[:3]):
                if i > 0:
                    # 添加延迟以避免过快请求
                    await asyncio.sleep(1)  
                
                log_message = f"🌐 正在获取详情: {item.title}"
                logger.info(log_message)
                if self.callback:
                    self.callback(log_message)
                
                try:
                    # 提取页面内容
                    content = await self.browser.scrape_text(item.url)
                    
                    # 返回提取的内容
                    yield {
                        "status": "content", 
                        "message": f"📄 已获取 '{item.title}' 的内容",
                        "title": item.title,
                        "url": item.url,
                        "content": content[:1000]  # 限制内容长度
                    }
                except Exception as e:
                    logger.error(f"提取内容失败: {str(e)}")
                    if self.callback:
                        self.callback(f"❌ 提取 '{item.title}' 内容失败: {str(e)}")
        
        except Exception as e:
            error_message = f"❌ 浏览器搜索失败: {str(e)}"
            logger.error(error_message)
            if self.callback:
                self.callback(error_message)
            
            yield {"status": "error", "message": error_message}
    
    async def close(self):
        """关闭浏览器"""
        await self.browser.close() 