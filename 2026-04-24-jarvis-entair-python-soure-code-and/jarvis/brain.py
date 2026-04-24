from __future__ import annotations

from typing import Dict, List

from jarvis.config import SETTINGS


class Brain:
    def __init__(self) -> None:
        self.knowledge_base: Dict[str, str] = {
            "what is ai": (
                "Artificial intelligence is the ability of software to perform tasks "
                "that usually need human-style reasoning, prediction, or understanding."
            ),
            "what is machine learning": (
                "Machine learning is a branch of AI where systems learn patterns from data "
                "instead of being fully programmed with fixed rules."
            ),
            "what can you do": (
                "I can chat with you, answer common questions, open apps or websites, "
                "show system status, manage simple reminders, and listen to voice commands."
            ),
            "who are you": (
                f"I am {SETTINGS.assistant_name}, a friendly Python assistant built to help "
                "with system tasks, information, and voice interaction."
            ),
        }

        self.human_style_tips: List[str] = [
            "I am here with you. Tell me the task in a simple sentence.",
            "We can do this step by step if you want.",
            "If you prefer, switch to voice mode and talk naturally.",
        ]

    def answer(self, message: str) -> str:
        normalized = message.strip().lower()
        if normalized in self.knowledge_base:
            return self.knowledge_base[normalized]

        if "human intelligence" in normalized:
            return (
                "Human intelligence includes creativity, empathy, judgment, and learning from "
                "experience. AI can assist with some reasoning, but people still lead with values and context."
            )

        if "friendly" in normalized:
            return "I am designed to stay calm, respectful, and easy to work with."

        if SETTINGS.ai_provider != "local" and SETTINGS.ai_api_key:
            return (
                "An external AI provider is configured in settings, but the cloud integration "
                "still needs to be added in jarvis/brain.py."
            )

        return (
            "I do not have a strong answer for that yet, but I can still help with system commands, "
            "web search, voice use, reminders, and basic AI concepts."
        )

    def coaching_tip(self) -> str:
        return self.human_style_tips[0]
