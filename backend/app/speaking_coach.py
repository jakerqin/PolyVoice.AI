import json
import os
import tempfile
from typing import Dict, List, Optional, Tuple

from loguru import logger

from app.llm import DeepSeekLLM
from app.speech_recognition import WhisperRecognizer
from app.speech_synthesis import VALLESynthesizer


class SpeakingCoach:
    """口语教练类，整合语音识别、语音合成和大语言模型"""

    def __init__(
        self,
        llm_model: str = "deepseek-chat",
        tts_model: str = "tts_models/multilingual/multi-dataset/your_tts",
        language: str = "zh",
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
        self.language = language
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
        # 初始化各个组件
        self.llm = DeepSeekLLM(model_name=llm_model)
        self.recognizer = WhisperRecognizer()
        self.synthesizer = VALLESynthesizer(model_name=tts_model)
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
        
        logger.info("SpeakingCoach initialized")

    def _get_default_system_prompt(self) -> str:
        """获取默认系统提示"""
        return """你是一位专业的口语教练，擅长帮助学生提高口语水平。
                    你的任务是：
                    1. 评估学生的口语表达，指出语法、发音和表达方式上的问题
                    2. 提供改进建议和练习方法
                    3. 根据学生的水平调整对话难度
                    4. 鼓励学生多说，建立自信
                    5. 在适当的时候提供相关词汇和表达方式

                请用中文回复，除非学生要求使用其他语言。"""

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
            user_text = await self.recognizer.transcribe_from_bytes(audio_bytes, self.language)
            logger.info(f"Recognized text: {user_text}")
            
            # 2. 添加到对话历史
            self.conversation_history.append({"role": "user", "content": user_text})
            
            # 3. 生成响应
            response_text = await self.llm.generate_with_history(
                self.conversation_history,
                system_prompt=self.system_prompt
            )
            logger.info(f"Generated response: {response_text}")
            
            # 4. 添加到对话历史
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            # 5. 语音合成：将文本转换为音频
            response_audio = await self.synthesizer.synthesize(response_text, self.language)
            
            return response_text, response_audio
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
            response_text = await self.llm.generate_with_history(
                self.conversation_history,
                system_prompt=self.system_prompt
            )
            logger.info(f"Generated response: {response_text}")
            
            # 3. 添加到对话历史
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            # 4. 语音合成：将文本转换为音频
            response_audio = await self.synthesizer.synthesize(response_text, self.language)
            
            return response_text, response_audio
        except Exception as e:
            logger.error(f"Error processing text input: {e}")
            raise

    async def get_conversation_history(self) -> List[Dict[str, str]]:
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