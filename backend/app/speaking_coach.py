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
            - 响应类型: {"type": "response", "data": 响应文本}
            - 发音建议类型: {"type": "pronunciationSuggestion", "data": 发音建议文本}
            - 语法建议类型: {"type": "grammarSuggestion", "data": 语法建议文本}
            - 用户响应建议类型: {"type": "userResponseSuggestion", "data": 用户响应建议文本}
            - 音频类型: {"type": "audio", "data": 音频字节的base64编码字符串, "format": "mp3"}
        """
        try:
            # 1. 添加到对话历史
            self.conversation_history.append({"role": "user", "content": text})
            
            # 2. 生成流式响应
            messages_with_system = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
            
            # 用于保存完整响应的缓冲区
            full_response = ""
            
            # XML解析状态和缓冲区
            current_tag = None
            content_buffer = ""
            tag_start_pattern = re.compile(r'<(response|pronunciationSuggestion|grammarSuggestion|userResponseSuggestion)>')
            tag_end_pattern = re.compile(r'</(response|pronunciationSuggestion|grammarSuggestion|userResponseSuggestion)>')
            
            # 从LLM获取流式响应
            async for text_chunk in self.llm.generate_stream(messages_with_system):
                full_response += text_chunk
                
                # 处理当前文本块
                i = 0
                while i < len(text_chunk):
                    char = text_chunk[i]
                    
                    # 检查开始标签
                    if char == '<' and current_tag is None:
                        # 尝试匹配开始标签
                        tag_match = None
                        for j in range(i, min(i + 35, len(text_chunk))):
                            partial_tag = text_chunk[i:j+1]
                            start_match = tag_start_pattern.match(partial_tag)
                            if start_match:
                                tag_match = start_match
                                current_tag = start_match.group(1)
                                i = j + 1
                                break
                        
                        if tag_match:
                            content_buffer = ""  # 重置内容缓冲区
                            continue
                    
                    # 检查结束标签
                    if char == '<' and current_tag is not None:
                        # 尝试匹配结束标签
                        for j in range(i, min(i + 36, len(text_chunk))):
                            partial_tag = text_chunk[i:j+1]
                            end_match = tag_end_pattern.match(partial_tag)
                            if end_match and end_match.group(1) == current_tag:
                                # 发送标签内容
                                if content_buffer:
                                    clean_content = content_buffer.strip()
                                    if clean_content:
                                        yield {"type": current_tag, "data": clean_content}
                                        
                                        # 为response生成音频
                                        if current_tag == "response":
                                            clean_text = self._clean_text_for_audio(clean_content)
                                            audio_bytes = await self.synthesizer.synthesize(clean_text, language=self.language)
                                            yield {"type": "audio", "data": base64.b64encode(audio_bytes).decode('utf-8'), "format": "mp3"}
                                
                                current_tag = None
                                content_buffer = ""
                                i = j + 1
                                break
                        
                        if current_tag is None:  # 如果找到结束标签
                            continue
                    
                    # 在标签内部收集内容
                    if current_tag is not None:
                        content_buffer += char
                    else:
                        # 不在任何标签内，可能是其他文本或未完成的标签
                        yield {"type": "text", "data": char}
                    
                    i += 1
            
            # 异常情况兜底
            if current_tag is not None and content_buffer:
                clean_content = content_buffer.strip()
                if clean_content:
                    yield {"type": current_tag, "data": clean_content}
                    
                    # 为response生成音频
                    if current_tag == "response":
                        clean_text = self._clean_text_for_audio(clean_content)
                        audio_bytes = await self.synthesizer.synthesize(clean_text, language=self.language)
                        yield {"type": "audio", "data": base64.b64encode(audio_bytes).decode('utf-8'), "format": "mp3"}
            
            # 3. 添加完整响应到对话历史
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            logger.error(f"流式处理文本输入失败: {str(e)}")
            # 输出错误信息
            yield {"type": "error", "data": str(e)}
            raise
    
    def _clean_text_for_audio(self, text: str) -> str:
        """
        处理文本，移除markdown标记和特殊字符，保留原始纯文本用于语音合成
        
        Args:
            text: 输入文本，可能包含markdown标记
            
        Returns:
            清理后的文本
        """
        # 移除markdown链接，保留链接文本
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # 移除markdown标题标记
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        
        # 移除markdown加粗和斜体
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # 加粗
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # 斜体
        text = re.sub(r'__([^_]+)__', r'\1', text)      # 加粗
        text = re.sub(r'_([^_]+)_', r'\1', text)        # 斜体
        
        # 移除markdown代码块和行内代码
        text = re.sub(r'```[a-zA-Z]*\n([\s\S]*?)\n```', r'\1', text)  # 代码块
        text = re.sub(r'`([^`]+)`', r'\1', text)                      # 行内代码
        
        # 移除markdown列表标记
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # 无序列表
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # 有序列表
        
        # 移除markdown引用标记
        text = re.sub(r'^\s*>\s+', '', text, flags=re.MULTILINE)
        
        # 处理HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 处理特殊转义字符
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    
    