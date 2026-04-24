from __future__ import annotations

from typing import Optional

try:
    import pyttsx3
except ImportError:  # pragma: no cover
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover
    sr = None


class VoiceInterface:
    def __init__(self, rate: int = 180) -> None:
        self.engine = None
        self.recognizer = None
        self.microphone = None
        self.rate = rate

        if pyttsx3:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", self.rate)

        if sr:
            self.recognizer = sr.Recognizer()
            try:
                self.microphone = sr.Microphone()
            except Exception:
                self.microphone = None

    @property
    def can_speak(self) -> bool:
        return self.engine is not None

    @property
    def can_listen(self) -> bool:
        return self.recognizer is not None and self.microphone is not None

    def speak(self, text: str) -> None:
        if not self.engine:
            return
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 8) -> Optional[str]:
        if not self.can_listen:
            return None

        assert self.recognizer is not None
        assert self.microphone is not None

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        try:
            return self.recognizer.recognize_google(audio)
        except Exception:
            return None
