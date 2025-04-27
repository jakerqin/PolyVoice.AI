from fastapi import APIRouter, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
import json
import uuid

from app.speaking_coach import SpeakingCoach
from app.logger import logger

router = APIRouter()

# 全局字典存储会话数据
audio_sessions = {}

# 创建口语教练实例
speaking_coach = SpeakingCoach()

class ConversationMessage(BaseModel):
    """对话消息模型"""
    type: str = Field(..., description="消息类型，可以是'text'、'audio'、'error'或'recognized_text'")
    text: str = Field(..., description="文本内容，对于文本类型消息存储文本内容")
    # mp3 音频字节转成base64
    audio: str = Field("", description="音频内容，存储为base64编码的字符串，仅当type为'audio'时有值")


@router.post("/stream_audio_chat")
async def upload_audio(
    audio: UploadFile = File(...)
):
    """
    上传音频文件接口
    
    Args:
        audio: 音频文件
        
    Returns:
        会话ID
    """
    try:
        # 读取音频文件
        audio_bytes = await audio.read()
        
        # 生成一个唯一的会话ID
        session_id = str(uuid.uuid4())
        
        # 存储音频数据以供后续处理
        audio_sessions[session_id] = audio_bytes
        
        return {"session_id": session_id}
    except Exception as e:
        logger.error(f"处理音频文件上传出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream_audio_chat/{session_id}")
async def stream_audio_chat(
    request: Request,
    session_id: str
):
    """
    流式音频聊天接口
    
    Args:
        session_id: 会话ID
        
    Returns:
        流式响应
    """
    try:
        # 获取之前上传的音频数据
        if session_id not in audio_sessions:
            raise HTTPException(status_code=404, detail="会话不存在或已过期")
            
        audio_bytes = audio_sessions[session_id]
        
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
                
                # 处理完成后删除会话数据
                if session_id in audio_sessions:
                    del audio_sessions[session_id]
                    
            except Exception as e:
                logger.error(f"流式音频聊天出错: {str(e)}")
                yield json.dumps({"type": "error", "text": str(e)})
                
                # 发生错误时也需要清理
                if session_id in audio_sessions:
                    del audio_sessions[session_id]
        
        return EventSourceResponse(event_generator())
    except Exception as e:
        logger.error(f"处理流式响应出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
