"""
PolyVoice.AI 应用包
"""

from app.speaking_coach import SpeakingCoach
from app.config import Config
from app.api import router

__all__ = [
    'SpeakingCoach',
    'Config',
    'router'
]
