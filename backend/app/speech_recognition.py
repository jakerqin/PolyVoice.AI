import os
import logging
from typing import Optional
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


class WhisperRecognizer:
    """使用 Whisper 进行语音识别的类"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        初始化 WhisperRecognizer
        
        Args:
            model_path: Whisper 模型路径，如果为 None 则使用默认模型
        """
        if model_path is None:
            # 使用默认模型路径
            model_path = os.path.join(os.path.dirname(__file__), "..", "models", "whisper", "base")
        
        # 针对 M4 芯片优化配置
        self.model = WhisperModel(
            model_path,
            device="mps",  # 使用 Metal Performance Shaders
            compute_type="float16",  # 使用 float16 精度，在 32GB 内存下可以保证性能
            cpu_threads=8,  # 设置 CPU 线程数
            num_workers=2   # 设置工作线程数
        )
        logger.info(f"Initialized Whisper model from {model_path}")
    
    def transcribe_from_file(self, audio_path: str) -> str:
        """
        从音频文件转录文本
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            转录的文本
        """
        try:
            # 使用批处理大小 16 提高吞吐量
            segments, _ = self.model.transcribe(
                audio_path,
                batch_size=16,
                vad_filter=True,  # 使用语音活动检测过滤
                vad_parameters=dict(min_silence_duration_ms=500)  # 设置静音检测参数
            )
            
            # 合并所有片段
            text = " ".join([segment.text for segment in segments])
            logger.info(f"Transcribed text from {audio_path}: {text}")
            return text
        except Exception as e:
            logger.error(f"Error transcribing audio file {audio_path}: {str(e)}")
            raise
    
    def transcribe_from_bytes(self, audio_bytes: bytes) -> str:
        """
        将音频字节数据转换为文本
        
        Args:
            audio_bytes: 音频字节数据
        
        Returns:
            识别出的文本
        """
        try:
            # 使用批处理大小 16 提高吞吐量
            segments, _ = self.model.transcribe(
                audio_bytes,
                batch_size=16,
                vad_filter=True,  # 使用语音活动检测过滤
                vad_parameters=dict(min_silence_duration_ms=500)  # 设置静音检测参数
            )
            
            # 合并所有片段
            text = " ".join([segment.text for segment in segments])
            logger.info(f"Transcribed text from audio bytes: {text}")
            return text
        except Exception as e:
            logger.error(f"Error transcribing audio bytes: {str(e)}")
            raise 