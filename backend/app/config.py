import threading
import tomllib
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent.parent


PROJECT_ROOT = get_project_root()
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
MODELS_DIR = PROJECT_ROOT / "models"


class LLMSettings(BaseModel):
    model: str = Field(..., description="Model name")
    base_url: str = Field(..., description="API base URL")
    api_key: str = Field(..., description="API key")
    max_tokens: int = Field(4096, description="Maximum number of tokens per request")
    temperature: float = Field(1.0, description="Sampling temperature")
    api_type: str = Field(..., description="AzureOpenai or Openai")
    api_version: str = Field(..., description="Azure Openai version if AzureOpenai")

class TTSSettings(BaseModel):
    model: str = Field(..., description="Model name")
    language: str = Field(..., description="speak language")



class AppConfig(BaseModel):
    """存储LLM的配置"""
    llm: Dict[str, LLMSettings]
    tts: Dict[str, TTSSettings]

class Config:
    """单例模式：获取LLM的配置，把AppConfig保存进_instance中"""
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        """double check 保证单例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Load the initial configuration. 在实例创建之后调用"""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._config = None
                    self._load_initial_config()
                    self._initialized = True

    @staticmethod
    def _get_config_path() -> Path:
        root = PROJECT_ROOT
        config_path = root / "config" / "config.toml"
        if config_path.exists():
            return config_path
        example_path = root / "config" / "config.example.toml"
        if example_path.exists():
            return example_path
        raise FileNotFoundError("No configuration file found in config directory")

    def _load_config(self) -> dict:
        config_path = self._get_config_path()
        with config_path.open("rb") as f:
            return tomllib.load(f)

    def _load_initial_config(self):
        """Load the configuration"""
        raw_config = self._load_config()
        base_llm = raw_config.get("llm", {})
        base_tts = raw_config.get("tts", {})
        # [llm.openai] 会被解析为 {llm: {openai: {}}} 
        llm_overrides = {
            k: v for k, v in raw_config.get("llm", {}).items() if isinstance(v, dict)
        }
        # [llm] 的配置作为默认配置
        default_settings = {
            "model": base_llm.get("model"),
            "base_url": base_llm.get("base_url"),
            "api_key": base_llm.get("api_key"),
            "max_tokens": base_llm.get("max_tokens", 4096),
            "temperature": base_llm.get("temperature", 1.0),
            "api_type": base_llm.get("api_type", ""),
            "api_version": base_llm.get("api_version", "")
        }
        # 合并默认配置和每个模型的配置
        config_dict = {
            "llm": {
                "default": default_settings,
                **{
                    # 每个模型的配置会覆盖默认配置
                    name: {**default_settings, **override_config}
                    for name, override_config in llm_overrides.items()
                },
            },
            "tts": base_tts
        }

        self._config = AppConfig(**config_dict)

    @property
    def llm(self) -> Dict[str, LLMSettings]:
        return self._config.llm
    
    @property
    def tts(self) -> Dict[str, TTSSettings]:
        return self._config.tts
        
    @property
    def TTS_MODEL_DIR(self) -> Path:
        """获取TTS模型目录"""
        return MODELS_DIR / "tts"


config = Config()
