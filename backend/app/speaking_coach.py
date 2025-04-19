import json
import os
from typing import List, Optional, Tuple

from loguru import logger

from app.llm import DeepSeekLLM
from app.speech_recognition import WhisperRecognizer
from app.speech_synthesis import CoquiTTS
from app.config import Config
from app.prompt.coach import SYSTEM_PROMPT
# 加载配置
config = Config()

class SpeakingCoach:
    """口语教练类，整合语音识别、语音合成和大语言模型"""

    def __init__(
        self,
        language: str = "en",
        system_prompt: Optional[str] = None
    ):
        """
        初始化口语教练
        
        Args:
            llm_model: 大语言模型名称
            tts_model: 语音合成模型名称
            language: 默认语言
            system_prompt: 系统提示
        """
        self.language = config.tts.language
        self.system_prompt = SYSTEM_PROMPT
        
        # 获取模型路径
        tts_model_name = config.tts.model
        tts_model_path = config.TTS_MODEL_DIR
        whisper_model_path = config.WHISPER_MODEL_DIR
        
        # 检查模型路径是否存在
        if os.path.exists(tts_model_path):
            logger.info(f"使用本地TTS模型: {tts_model_path}")
        else:
            logger.warning(f"本地TTS模型未找到: {tts_model_path}，将尝试使用模型名称: {tts_model_name}")
            tts_model_path = None
        
        # 初始化各个组件
        self.llm = DeepSeekLLM()
        self.recognizer = WhisperRecognizer(whisper_model_path)
        self.synthesizer = CoquiTTS(model_name=tts_model_name, model_path=tts_model_path)
        
        # 对话历史
        self.conversation_history: List[dict] = []
        
        logger.info("SpeakingCoach initialized")

    async def process_audio_input(self, audio_bytes: bytes) -> Tuple[str, bytes]:
        """
        处理音频输入，返回文本响应和音频响应
        
        Args:
            audio_bytes: 用户音频输入
            
        Returns:
            文本响应和音频响应
        """
        try:
            # 1. 语音识别：将音频转换为文本
            user_text = self.recognizer.transcribe_from_bytes(audio_bytes)
            return await self.process_text_input(user_text)
        except Exception as e:
            logger.error(f"Error processing audio input: {e}")
            raise

    async def process_text_input(self, text: str) -> Tuple[str, bytes]:
        """
        处理文本输入，返回文本响应和音频响应
        
        Args:
            text: 用户文本输入
            
        Returns:
            文本响应和音频响应
        """
        try:
            # 1. 添加到对话历史
            self.conversation_history.append({"role": "user", "content": text})
            
            # 2. 生成响应
            # 创建包含系统提示的消息列表
            messages_with_system = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
            response_text = await self.llm.generate_with_history(
                messages_with_system
            )
            logger.info(f"Generated response: {response_text}")
            
            # 3. 添加到对话历史
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            # 4. 语音合成：将文本转换为音频
            response_audio = await self.synthesizer.synthesize(response_text)
            
            return response_text, response_audio
        except Exception as e:
            logger.error(f"Error processing text input: {e}")
            raise

    async def get_conversation_history(self) -> List[dict]:
        """
        获取对话历史
        
        Returns:
            对话历史
        """
        return self.conversation_history

    async def clear_conversation_history(self) -> None:
        """清空对话历史"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    async def save_conversation_history(self, file_path: str) -> None:
        """
        保存对话历史到文件
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            logger.info(f"Conversation history saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving conversation history: {e}")
            raise

    async def load_conversation_history(self, file_path: str) -> None:
        """
        从文件加载对话历史
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.conversation_history = json.load(f)
            logger.info(f"Conversation history loaded from {file_path}")
        except Exception as e:
            logger.error(f"Error loading conversation history: {e}")
            raise 