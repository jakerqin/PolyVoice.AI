import tempfile
from pathlib import Path

import edge_tts


class EdgeTTS:
    """使用 Edge TTS 进行语音合成的类"""
    
    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural"):
        """
        初始化 EdgeTTS
        
        Args:
            voice: 语音名称，默认为中文女声
        """
        self.voice = voice
    
    async def synthesize(self, text: str) -> bytes:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
        
        Returns:
            音频字节数据
        """
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # 使用 Edge TTS 合成语音
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(temp_path)
            
            # 读取音频文件
            with open(temp_path, "rb") as f:
                audio_bytes = f.read()
            
            return audio_bytes
        finally:
            # 删除临时文件
            Path(temp_path).unlink() 