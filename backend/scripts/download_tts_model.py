import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent.parent))

from TTS.utils.manage import ModelManager
from app.config import Config

def download_tts_model():
    """下载TTS模型到本地"""
    print("开始下载TTS模型...")
    
    # 获取配置
    config = Config()
    model_dir = Path(config.TTS_MODEL_DIR)
    
    # 确保模型目录存在
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置环境变量，指定模型下载目录
    os.environ["COQUI_TTS_MODEL_DIR"] = str(model_dir)
    
    # 使用ModelManager下载模型
    manager = ModelManager()
    model_path = manager.download_model("tts_models/multilingual/multi-dataset/your_tts")
    
    print(f"模型已下载到: {model_path}")
    print("下载完成!")

if __name__ == "__main__":
    download_tts_model() 