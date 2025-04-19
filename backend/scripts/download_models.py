import os
import sys
import tomllib
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent.parent))

from TTS.utils.manage import ModelManager
from loguru import logger
from faster_whisper import download_model

# 可用的Whisper模型列表
WHISPER_MODELS = {
    "tiny": "Systran/faster-whisper-tiny",      # 最小的模型，速度最快，但准确度较低
    "base": "Systran/faster-whisper-base",      # 基础模型，平衡了速度和准确度
    "small": "Systran/faster-whisper-small",     # 小型模型，比base更准确
    "medium": "Systran/faster-whisper-medium",    # 中型模型，准确度更高
    "large": "Systran/faster-whisper-large",     # 大型模型，准确度最高，但需要更多计算资源
    "large-v2": "Systran/faster-whisper-large-v2",  # 大型模型的改进版本
    "large-v3": "Systran/faster-whisper-large-v3"   # 最新的大型模型版本，性能最好
}

def load_config():
    try:
        config_path = Path(__file__).parent / "config" / "config.toml"
        default_config = {"whisper_model": "base", "whisper_model_local": "models/whisper", "tts_model_local": "models/tts", "tts_model": "tts_models/multilingual/multi-dataset/xtts_v2"}

        if not config_path.exists():
            return default_config

        with open(config_path, "rb") as f:
            config = tomllib.load(f)

        return {"whisper_model": config["whisper"]["model"], "whisper_model_local": config["whisper"]["whisper_path"], "tts_model_local": config["tts"]["model_path"], "tts_model": config["tts"]["model"]}
    except FileNotFoundError:
        return default_config
    except KeyError as e:
        return default_config

def download_models():
    """下载所有需要的模型到本地
    
    Args:
        whisper_model: Whisper模型大小，可选值: tiny, base, small, medium, large, large-v2, large-v3
    """
    # 使用国内镜像
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"  
    logger.info("开始下载模型...")
    
    # 获取模型目录
    config = load_config()
    PROJECT_PATH = Path(__file__).resolve().parent.parent
    tts_model_dir = PROJECT_PATH / config["tts_model_local"]
    whisper_model_dir = PROJECT_PATH / config["whisper_model_local"]
    # 获取Whisper模型
    whisper_model = config["whisper_model"]
    if whisper_model not in WHISPER_MODELS:
        raise ValueError(f"不支持的Whisper模型: {whisper_model}，可用选项: {', '.join(WHISPER_MODELS)}")
    
    # 确保模型目录存在
    tts_model_dir.mkdir(parents=True, exist_ok=True)
    whisper_model_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置环境变量，指定模型下载目录
    os.environ["TTS_HOME"] = str(tts_model_dir)
    
    # 下载Whisper模型
    # logger.info(f"下载Whisper模型: {whisper_model}...")
    # try:
    #     whisper_model_path = download_model(
    #         WHISPER_MODELS[whisper_model],
    #         output_dir=str(whisper_model_dir),
    #         local_files_only=False
    #     )
    #     logger.info(f"Whisper模型已下载到: {whisper_model_path}")
    # except Exception as e:
    #     logger.error(f"下载Whisper模型失败: {str(e)}")
    #     raise RuntimeError(f"Whisper模型下载失败: {str(e)}")
    
    # 使用ModelManager下载TTS模型
    manager = ModelManager()
    
    # 下载主要模型
    model_name = config['tts_model']
    
    logger.info(f"下载TTS模型: {model_name}")
    try:
        # 使用ModelManager下载模型
        model_path = manager.download_model(model_name)
        logger.info(f"TTS模型 {model_name} 已下载到: {model_path}")
    except Exception as e:
        logger.error(f"下载TTS模型 {model_name} 失败: {str(e)}")
        raise RuntimeError(f"TTS模型下载失败: {str(e)}")
    
    logger.info("所有模型下载完成!")

if __name__ == "__main__":
    download_models()