from dataclasses import dataclass
import os


@dataclass
class Settings:
    assistant_name: str = "Jarvis Entair"
    default_mode: str = "text"
    voice_enabled: bool = True
    speech_rate: int = 180
    ai_provider: str = os.getenv("JARVIS_AI_PROVIDER", "local")
    ai_api_key: str = os.getenv("JARVIS_AI_API_KEY", "")


SETTINGS = Settings()
