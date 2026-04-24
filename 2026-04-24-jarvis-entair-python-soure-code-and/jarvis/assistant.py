from __future__ import annotations

from jarvis.brain import Brain
from jarvis.commands import CommandRouter, SessionState
from jarvis.config import SETTINGS
from jarvis.voice import VoiceInterface


class JarvisAssistant:
    def __init__(self) -> None:
        self.brain = Brain()
        self.state = SessionState()
        self.router = CommandRouter(self.brain, self.state)
        self.voice = VoiceInterface(rate=SETTINGS.speech_rate)
        self.mode = SETTINGS.default_mode

    def run(self) -> None:
        print(f"{SETTINGS.assistant_name} starting...")
        self.select_mode()
        greeting = (
            f"Hello, I am {SETTINGS.assistant_name}. "
            "I am friendly, voice-ready, and built to help with your computer tasks."
        )
        self.respond(greeting)

        while True:
            user_input = self.get_input()
            if user_input is None:
                self.respond("I could not hear you clearly. Please try again.")
                continue

            reply = self.router.handle(user_input)
            if reply == "__exit__":
                self.respond("Goodbye. I will be ready when you need me again.")
                break

            self.respond(reply)

    def select_mode(self) -> None:
        print("Choose input mode:")
        print("1. Text")
        print("2. Voice")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "2" and self.voice.can_listen:
            self.mode = "voice"
            print("Voice mode enabled.")
        elif choice == "2":
            self.mode = "text"
            print("Voice mode is unavailable, so text mode is enabled.")
        else:
            self.mode = "text"

    def get_input(self) -> str | None:
        if self.mode == "voice":
            print("Listening...")
            heard = self.voice.listen()
            if heard:
                print(f"You said: {heard}")
            return heard
        return input("You: ")

    def respond(self, message: str) -> None:
        print(f"{SETTINGS.assistant_name}: {message}")
        if self.mode == "voice" and self.voice.can_speak:
            self.voice.speak(message)
