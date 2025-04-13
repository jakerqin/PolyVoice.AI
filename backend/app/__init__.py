"""
PolyVoice.AI 应用包
"""

from app.speaking_coach import SpeakingCoach
from app.speech_recognition import WhisperRecognizer
from app.speech_synthesis import EdgeTTS as SpeechSynthesizer
from app.llm import DeepSeekLLM
from app.config import Config
from app.api import router

__all__ = [
    'SpeakingCoach',
    'WhisperRecognizer',
    'SpeechSynthesizer',
    'DeepSeekLLM',
    'Config',
    'router'
]
