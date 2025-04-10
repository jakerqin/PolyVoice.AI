import os
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.speaking_coach import SpeakingCoach

router = APIRouter()

# 创建口语教练实例
speaking_coach = SpeakingCoach()


class TextResponse(BaseModel):
    """文本响应模型"""
    text: str


class ConversationMessage(BaseModel):
    """对话消息模型"""
    role: str
    content: str


class ConversationHistory(BaseModel):
    """对话历史模型"""
    messages: List[ConversationMessage]


@router.post("/speak", response_class=JSONResponse)
async def speak(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    """
    处理语音输入，返回文本和音频响应
    
    Args:
        audio: 音频文件
        language: 语言代码
        
    Returns:
        文本和音频响应
    """
    try:
        # 读取音频文件
        audio_bytes = await audio.read()
        
        # 处理音频输入
        response_text, response_audio = await speaking_coach.process_audio_input(audio_bytes)
        
        # 返回响应
        return {
            "text": response_text,
            "audio": response_audio.hex()  # 将字节转换为十六进制字符串
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_class=JSONResponse)
async def chat(
    text: str = Form(...),
    language: Optional[str] = Form(None)
):
    """
    处理文本输入，返回文本和音频响应
    
    Args:
        text: 文本输入
        language: 语言代码
        
    Returns:
        文本和音频响应
    """
    try:
        # 处理文本输入
        response_text, response_audio = await speaking_coach.process_text_input(text)
        
        # 返回响应
        return {
            "text": response_text,
            "audio": response_audio.hex()  # 将字节转换为十六进制字符串
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=ConversationHistory)
async def get_history():
    """
    获取对话历史
    
    Returns:
        对话历史
    """
    try:
        history = await speaking_coach.get_conversation_history()
        return ConversationHistory(messages=[
            ConversationMessage(role=msg["role"], content=msg["content"])
            for msg in history
        ])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history/clear")
async def clear_history():
    """清空对话历史"""
    try:
        await speaking_coach.clear_conversation_history()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history/save")
async def save_history(file_path: str = Form(...)):
    """
    保存对话历史到文件
    
    Args:
        file_path: 文件路径
    """
    try:
        await speaking_coach.save_conversation_history(file_path)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history/load")
async def load_history(file_path: str = Form(...)):
    """
    从文件加载对话历史
    
    Args:
        file_path: 文件路径
    """
    try:
        await speaking_coach.load_conversation_history(file_path)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 