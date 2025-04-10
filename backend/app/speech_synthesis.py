import os
import tempfile
from pathlib import Path
from typing import Optional

import torch
import torchaudio
from loguru import logger
from TTS.api import TTS

from app.config import config


class VALLESynthesizer:
    """使用VALL-E进行语音合成的类"""

    def __init__(self, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"):
        """
        初始化VALL-E合成器
        
        Args:
            model_name: TTS模型名称，默认使用较小的英文模型
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # 设置模型目录
        model_dir = config.TTS_MODEL_DIR
        os.environ["COQUI_TTS_MODEL_DIR"] = str(model_dir)
        
        # 检查模型是否已下载
        model_path = model_dir / model_name.replace("/", "_")
        if not model_path.exists():
            logger.warning(f"Model not found at {model_path}, will download from remote")
        
        try:
            self.tts = TTS(model_name=model_name).to(self.device)
            logger.info(f"VALLESynthesizer initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Error initializing TTS model: {e}")
            # 尝试使用备用模型
            try:
                self.tts = TTS(model_name="tts_models/en/ljspeech/glow-tts").to(self.device)
                logger.info("Using fallback model: glow-tts")
            except Exception as e2:
                logger.error(f"Error initializing fallback model: {e2}")
                raise

    async def synthesize(self, text: str, language: str = "en", speaker_wav: Optional[str] = None) -> bytes:
        """
        将文本合成为语音
        
        Args:
            text: 要合成的文本
            language: 文本语言，默认为英文
            speaker_wav: 参考音频文件路径，用于声音克隆
            
        Returns:
            合成的音频字节
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file_path = temp_file.name
            
            # 合成语音
            if speaker_wav and os.path.exists(speaker_wav):
                self.tts.tts_to_file(
                    text=text,
                    file_path=temp_file_path,
                    speaker_wav=speaker_wav,
                    language=language
                )
            else:
                self.tts.tts_to_file(
                    text=text,
                    file_path=temp_file_path,
                    language=language
                )
            
            # 读取合成的音频文件
            with open(temp_file_path, "rb") as f:
                audio_bytes = f.read()
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
            return audio_bytes
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            raise

    async def get_available_voices(self) -> list:
        """
        获取可用的声音列表
        
        Returns:
            可用声音列表
        """
        try:
            return self.tts.speakers
        except Exception as e:
            logger.error(f"Error getting available voices: {e}")
            return []

    async def get_available_languages(self) -> list:
        """
        获取可用的语言列表
        
        Returns:
            可用语言列表
        """
        try:
            return self.tts.languages
        except Exception as e:
            logger.error(f"Error getting available languages: {e}")
            return [] 