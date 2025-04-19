import tempfile
from pathlib import Path
import os
import torch
from typing import Optional, Union

from TTS.api import TTS
from loguru import logger


class CoquiTTS:
    """使用 Coqui TTS 进行语音合成的类
    
    这个类提供了使用 Coqui TTS 进行文本到语音转换的功能。
    支持多语言合成，并提供了灵活的配置选项。
    
    Attributes:
        model_name (str): 使用的TTS模型名称
        tts (TTS): TTS模型实例
        sample_rate (int): 音频采样率
        speaker_wav (Optional[str]): 说话人参考音频文件路径
    """
    
    def __init__(
        self,
        model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
        model_path: Optional[str] = None,
        sample_rate: int = 24000,
        speaker_wav: Optional[str] = None
    ):
        """
        初始化 CoquiTTS
        
        Args:
            model_name: 模型名称，默认为高质量多语言模型
            model_path: 本地模型路径，如果提供则使用本地模型
            sample_rate: 音频采样率，默认24000Hz
            speaker_wav: 说话人参考音频文件路径，用于声音克隆
        """
        try:
            self.model_name = model_name
            self.model_path = model_path
            self.sample_rate = sample_rate
            self.speaker_wav = speaker_wav
            
            # 如果指定了本地路径，使用本地模型
            if model_path and os.path.exists(model_path):
                # 检查模型目录是否已经包含模型文件和配置文件
                model_config_path = os.path.join(model_path, "config.json")
                model_file_path = os.path.join(model_path, "model.pth")
                
                logger.info(f"从本地路径加载TTS模型: 目录={model_path}, 配置文件={model_config_path}")
                
                # 检查文件是否存在
                if not os.path.exists(model_config_path):
                    logger.warning(f"配置文件不存在: {model_config_path}")
                    raise FileNotFoundError(f"配置文件不存在: {model_config_path}")
                
                # 尝试只使用目录路径
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.tts = TTS(config_path=model_config_path, model_path=model_path, progress_bar=True).to(device)
            else:
                # 否则使用模型名称（触发下载）
                logger.info(f"使用模型名称加载TTS模型: {model_name}")
                # 设置模型目录环境变量
                models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
                os.environ["TTS_HOME"] = models_dir
                self.tts = TTS(model_name)
                
            logger.info(f"成功初始化 CoquiTTS，使用模型: {model_name}")
        except Exception as e:
            logger.error(f"初始化 CoquiTTS 失败: {str(e)}")
            raise
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        speaker_wav: Optional[str] = None
    ) -> bytes:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            language: 语言代码，默认为英语
            speaker_wav: 可选的说话人参考音频文件路径，用于声音克隆
        
        Returns:
            音频字节数据
            
        Raises:
            RuntimeError: 当语音合成失败时抛出
        """
        temp_path = None
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
            
            # 使用提供的speaker_wav或实例的speaker_wav
            reference_wav = speaker_wav or self.speaker_wav
            
            # 检查当前模型是否是 XTTS 模型
            is_xtts = "xtts" in self.model_name.lower()
            
            # XTTS 模型特别处理
            if is_xtts:
                logger.info(f"检测到 XTTS 模型: {self.model_name}")
                
                # 检查是否有参考音频
                if not reference_wav:
                    # 寻找默认参考音频
                    reference_wav = os.path.join(os.path.dirname(__file__), "..", "assets", "speakers", "default.wav")
                    if os.path.exists(reference_wav):
                        logger.info(f"使用默认参考音频: {reference_wav}")
                    else:
                        logger.error("XTTS 模型需要参考音频，但未提供")
                        raise ValueError("XTTS 模型需要参考音频文件用于语音克隆")
                
                # 直接使用 TTS 方法合成音频（XTTS 特定参数）
                logger.info(f"使用 XTTS 合成音频: text={text}, language={language}, speaker_wav={reference_wav}")
                wav_bytes = self.tts.synthesize(
                    text=text,
                    speaker_wav=reference_wav,
                    language=language,
                    stream=True  # todo: LLM 需要流式输出, 语音需要流式播放
                )
                
                # 将音频字节写入临时文件
                import numpy as np
                import soundfile as sf
                sf.write(temp_path, np.array(wav_bytes), self.sample_rate)
            else:
                # 非 XTTS 模型使用 tts_to_file 方法
                logger.info(f"使用标准 TTS 合成音频: text={text}, language={language}")
                self.tts.tts_to_file(text=text, file_path=temp_path)
            
            # 读取音频文件
            with open(temp_path, "rb") as f:
                audio_bytes = f.read()
            
            logger.info(f"成功合成语音，文本长度: {len(text)}，语言: {language}")
            return audio_bytes
            
        except Exception as e:
            error_msg = f"语音合成失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
        finally:
            # 清理临时文件
            if temp_path and Path(temp_path).exists():
                try:
                    Path(temp_path).unlink()
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")
    
    def get_available_models(self) -> list[str]:
        """
        获取可用的TTS模型列表
        
        Returns:
            可用模型名称列表
        """
        try:
            return TTS().list_models()
        except Exception as e:
            logger.error(f"获取可用模型列表失败: {str(e)}")
            return []
    
    def get_supported_languages(self) -> list[str]:
        """
        获取当前模型支持的语言列表
        
        Returns:
            支持的语言代码列表
        """
        try:
            return self.tts.languages
        except Exception as e:
            logger.error(f"获取支持的语言列表失败: {str(e)}")
            return [] 