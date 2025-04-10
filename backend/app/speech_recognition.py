import os
import tempfile
from typing import Optional

import openai
from loguru import logger

from app.config import config


class WhisperRecognizer:
    """使用Whisper进行语音识别的类"""

    def __init__(self):
        """初始化Whisper识别器"""
        self.api_key = config.llm["default"].api_key
        self.base_url = config.llm["default"].base_url
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        logger.info("WhisperRecognizer initialized")

    async def transcribe(self, audio_file_path: str, language: Optional[str] = None) -> str:
        """
        将音频文件转录为文本
        
        Args:
            audio_file_path: 音频文件路径
            language: 音频语言，如果为None则自动检测
            
        Returns:
            转录的文本
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
                return transcript.text
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise

    async def transcribe_from_bytes(self, audio_bytes: bytes, language: Optional[str] = None) -> str:
        """
        将音频字节转录为文本
        
        Args:
            audio_bytes: 音频字节
            language: 音频语言，如果为None则自动检测
            
        Returns:
            转录的文本
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            # 转录临时文件
            result = await self.transcribe(temp_file_path, language)
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
            return result
        except Exception as e:
            logger.error(f"Error transcribing audio bytes: {e}")
            raise 