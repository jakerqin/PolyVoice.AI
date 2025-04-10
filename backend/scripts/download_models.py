import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent.parent))

from TTS.utils.manage import ModelManager
from app.config import config

def download_models():
    """下载所有需要的模型到本地"""
    print("开始下载模型...")
    
    # 获取模型目录
    model_dir = config.TTS_MODEL_DIR
    
    # 确保模型目录存在
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置环境变量，指定模型下载目录
    os.environ["COQUI_TTS_MODEL_DIR"] = str(model_dir)
    
    # 使用ModelManager下载模型
    manager = ModelManager()
    
    # 下载主要模型
    models_to_download = [
        "tts_models/multilingual/multi-dataset/your_tts",
        "tts_models/multilingual/multi-dataset/xtts_v2"  # 备用模型
    ]
    
    for model_name in models_to_download:
        print(f"下载模型: {model_name}")
        try:
            model_path = manager.download_model(model_name)
            print(f"模型已下载到: {model_path}")
        except Exception as e:
            print(f"下载模型 {model_name} 失败: {e}")
    
    print("所有模型下载完成!")

if __name__ == "__main__":
    download_models() 