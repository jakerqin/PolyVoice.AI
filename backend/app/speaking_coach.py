import os
import re
from typing import List, Dict, Any, AsyncGenerator

from loguru import logger
import base64
from app.llm.openaiLLM import OpenaiLLM
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
        language: str = "en"
    ):
        """
        初始化口语教练
        
        Args:
            llm_model: 大语言模型名称
            tts_model: 语音合成模型名称
            language: 默认语言
            system_prompt: 系统提示
        """
        self.language = config.tts.language or language
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
        self.llm = OpenaiLLM()
        self.recognizer = WhisperRecognizer(whisper_model_path)
        self.synthesizer = CoquiTTS(model_name=tts_model_name, model_path=tts_model_path)
        
        # 对话历史
        self.conversation_history: List[dict] = []
        
        logger.info("SpeakingCoach initialized")

    async def process_audio_input_stream(self, audio_bytes: bytes) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式处理音频输入
        
        Args:
            audio_bytes: 音频字节数据
        
        Yields:
            包含类型和数据的字典
        """
        try:
            # 1. 语音识别：将音频转换为文本
            user_text = self.recognizer.transcribe_from_bytes(audio_bytes)
            logger.info(f"识别的文本: {user_text}")
            
            # 输出识别的文本
            yield {"type": "recognized_text", "data": user_text}
            
            # 2. 流式处理文本输入
            async for response in self.process_text_input_stream(user_text):
                yield response
                
        except Exception as e:
            logger.error(f"流式处理音频输入失败: {str(e)}")
            yield {"type": "error", "data": str(e)}
            raise

    
    
    async def process_text_input_stream(self, text: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式处理文本输入
        
        Args:
            text: 用户输入的文本
        
        Yields:
            包含类型和数据的字典：
            - 文本类型: {"type": "text", "data": 文本块}
            - 音频类型: {"type": "audio", "data": 音频字节的base64编码字符串, "format": "mp3"}
        """
        try:
            # 1. 添加到对话历史
            self.conversation_history.append({"role": "user", "content": text})
            
            # 2. 生成流式响应
            messages_with_system = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
            
            # 用于保存完整响应的缓冲区
            full_response = ""
            text_buffer = ""
            
            # 从LLM获取流式响应
            async for text_chunk in self.llm.generate_stream(messages_with_system):
                full_response += text_chunk
                text_buffer += text_chunk
                
                # 输出文本块
                yield {"type": "text", "data": text_chunk}
                
                # 当文本缓冲区达到一定大小或包含完整句子时，生成音频
                if len(text_buffer) > 50 and text_buffer[-1] in '.!?。！？':
                    logger.info(f"生成音频的文本: {text_buffer}") 
                    # 异步生成音频并发送
                    audio_bytes = await self.synthesizer.synthesize(text_buffer, language=self.language)
                    yield {"type": "audio", "data": base64.b64encode(audio_bytes).decode('utf-8'), "format": "mp3"}
                    text_buffer = ""  # 清空缓冲区
            
            # 处理剩余的文本缓冲区
            if text_buffer:
                audio_bytes = await self.synthesizer.synthesize(text_buffer, language=self.language)
                yield {"type": "audio", "data": base64.b64encode(audio_bytes).decode('utf-8'), "format": "mp3"}
            
            # 3. 添加完整响应到对话历史
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            logger.error(f"流式处理文本输入失败: {str(e)}")
            # 输出错误信息
            yield {"type": "error", "data": str(e)}
            raise
    
    
    