import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, Form, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import json

from app.speaking_coach import SpeakingCoach
from app.logger import logger

router = APIRouter()

# 创建口语教练实例
speaking_coach = SpeakingCoach()

# 存储任务状态
tasks = {}


class TextResponse(BaseModel):
    """文本响应模型"""
    text: str


class ConversationMessage(BaseModel):
    """对话消息模型"""
    role: str
    content: str
    audio: bytes


class ConversationHistory(BaseModel):
    """对话历史模型"""
    messages: List[ConversationMessage]


@router.post("/stream_audio_chat")
async def stream_audio_chat(
    request: Request,
    audio: UploadFile = File(...)
):
    """
    流式音频聊天接口
    
    Args:
        audio: 音频文件
        
    Returns:
        流式响应
    """
    try:
        # 读取音频文件
        audio_bytes = await audio.read()
        
        async def event_generator():
            try:
                # 使用流式处理音频输入
                async for response in speaking_coach.process_audio_input_stream(audio_bytes):
                    if await request.is_disconnected():
                        logger.info("客户端断开连接")
                        break
                        
                    # 将响应转换为JSON字符串
                    yield json.dumps(response)
                    
            except Exception as e:
                logger.error(f"流式音频聊天出错: {str(e)}")
                yield json.dumps({"type": "error", "data": str(e)})
        
        return EventSourceResponse(event_generator())
    except Exception as e:
        logger.error(f"处理音频文件出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

