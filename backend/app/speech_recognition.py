import os
import logging
import io
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
            model_path = os.path.join(os.path.dirname(__file__), "..", "models", "whisper")
        
        # 使用支持的设备配置
        # 注意：faster-whisper 只支持 "cpu", "cuda", 或 "auto" 作为设备类型
        self.model = WhisperModel(
            model_path,
            device="auto",  # 自动选择最佳设备 (CPU 或 CUDA)
            compute_type="int8", 
            cpu_threads=8,  # 设置 CPU 线程数
            num_workers=2   # 设置工作线程数
        )
        logger.info(f"Initialized Whisper model from {model_path}")
    

    
    def transcribe_from_bytes(self, audio_bytes: bytes) -> str:
        """
        将音频字节数据转换为文本
        
        Args:
            audio_bytes: 音频字节数据
        
        Returns:
            识别出的文本
        """
        try:
            # 将字节流转换为 BytesIO 对象
            audio_io = io.BytesIO(audio_bytes)
            
            # 直接使用 BytesIO 对象作为输入进行转录
            segments, _ = self.model.transcribe(
                audio_io,
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