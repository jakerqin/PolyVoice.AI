from fastapi import APIRouter, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
import json

from app.speaking_coach import SpeakingCoach
from app.logger import logger

router = APIRouter()

# 创建口语教练实例
speaking_coach = SpeakingCoach()

class ConversationMessage(BaseModel):
    """对话消息模型"""
    type: str = Field(..., description="消息类型，可以是'text'、'audio'、'error'或'recognized_text'")
    text: str = Field(..., description="文本内容，对于文本类型消息存储文本内容")
    # mp3 音频字节转成base64
    audio: str = Field("", description="音频内容，存储为base64编码的字符串，仅当type为'audio'时有值")


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
                        
                    # 将响应转换为ConversationMessage格式
                    conversation_message = ConversationMessage(
                        type=response["type"],
                        text=response.get("data", ""),
                        audio=response.get("data", "") if response["type"] == "audio" else ""
                    )
                    
                    # 将ConversationMessage转换为JSON字符串
                    yield json.dumps(conversation_message.model_dump())
                    
            except Exception as e:
                logger.error(f"流式音频聊天出错: {str(e)}")
                yield json.dumps({"type": "error", "data": str(e)})
        
        return EventSourceResponse(event_generator())
    except Exception as e:
        logger.error(f"处理音频文件出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

