from __future__ import annotations

import datetime as dt
import os
import platform
import subprocess
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import psutil

try:
    import pyttsx3
except ImportError:  # pragma: no cover
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover
    sr = None


@dataclass
class Settings:
    assistant_name: str = "Jarvis Entair"
    default_mode: str = "text"
    voice_enabled: bool = True
    speech_rate: int = 180
    ai_provider: str = os.getenv("AIzaSyDIpbCluIE5ihPRkLCC06OpxHdIbyWRRrw", "local")
    ai_api_key: str = os.getenv("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", "")


@dataclass
class SessionState:
    reminders: List[str] = field(default_factory=list)


class VoiceInterface:
    def __init__(self, rate: int = 180) -> None:
        self.engine = None
        self.recognizer = None
        self.microphone = None

        if pyttsx3:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", rate)

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


class Brain:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
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
                f"I am {self.settings.assistant_name}, a friendly Python assistant built to help "
                "with system tasks, information, and voice interaction."
            ),
        }

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

        if self.settings.ai_provider != "local" and self.settings.ai_api_key:
            return (
                "An external AI provider is configured, but the cloud integration still needs "
                "to be added inside this file."
            )

        return (
            "I do not have a full answer for that yet, but I can still help with system commands, "
            "web search, voice use, reminders, and basic AI concepts."
        )


def get_system_status() -> Dict[str, str]:
    battery = psutil.sensors_battery()
    battery_text = "Not available"
    if battery:
        battery_text = f"{battery.percent}%"
        if battery.power_plugged:
            battery_text += " (charging)"

    return {
        "os": f"{platform.system()} {platform.release()}",
        "machine": platform.machine(),
        "processor": platform.processor() or "Unknown",
        "cpu_usage": f"{psutil.cpu_percent(interval=0.5)}%",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "battery": battery_text,
        "time": dt.datetime.now().strftime("%I:%M %p"),
        "date": dt.datetime.now().strftime("%d %B %Y"),
    }


def open_app(name: str) -> str:
    known_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "explorer": "explorer.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
    }
    app = known_apps.get(name.lower(), name)

    try:
        subprocess.Popen([app], shell=False)
        return f"Opening {name}."
    except FileNotFoundError:
        return f"I could not find an app named {name}."
    except Exception as exc:
        return f"I could not open {name}: {exc}"


def open_website(target: str) -> str:
    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com",
        "instagram"   : "https://www.instagram.com",
        "whatsapp"    : "https://web.whatsapp.com",
        "stackoverflow": "https://stackoverflow.com",
        "wikipedia"   : "https://www.wikipedia.org",
        "twitter"     : "https://www.twitter.com",
        "linkedin"    : "https://www.linkedin.com",
        "reddit"      : "https://www.reddit.com",
        "netflix"     : "https://www.netflix.com",
        "chatgpt"     : "https://chat.openai.com",
    }
    url = websites.get(target.lower(), target)
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    webbrowser.open(url)
    return f"Opening {url}."


def open_folder(name: str) -> str:
    home = Path.home()
    known_folders = {
        "desktop": home / "Desktop",
        "documents": home / "Documents",
        "downloads": home / "Downloads",
        "music": home / "Music",
        "pictures": home / "Pictures",
        "videos": home / "Videos",
    }
    folder = known_folders.get(name.lower())
    if not folder or not folder.exists():
        return f"I could not find the folder named {name}."

    os.startfile(str(folder))
    return f"Opening {folder}."


def search_web(query: str) -> str:
    safe_query = query.strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={safe_query}"
    webbrowser.open(url)
    return f"Searching the web for {query}."


def try_self_update() -> str:
    if not Path(".git").exists():
        return "This project is not a Git repository, so self-update is unavailable."

    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        return f"Self-update failed: {exc}"

    if result.returncode == 0:
        message = result.stdout.strip() or "Update completed."
        return f"Self-update finished successfully. {message}"

    return f"Self-update failed. {result.stderr.strip() or result.stdout.strip()}"


class CommandRouter:
    def __init__(self, brain: Brain, state: SessionState) -> None:
        self.brain = brain
        self.state = state

    def handle(self, raw_text: str) -> str:
        text = raw_text.strip()
        normalized = text.lower()

        if not text:
            return "Please say or type something."

        if normalized in {"exit", "quit", "stop"}:
            return "__exit__"

        if normalized in {"hello", "hi", "hey"}:
            return "Hello. I am ready to help you."

        if normalized in {"time", "what time is it"}:
            return f"The current time is {dt.datetime.now().strftime('%I:%M %p')}."

        if normalized in {"date", "today date", "what is the date"}:
            return f"Today is {dt.datetime.now().strftime('%d %B %Y')}."

        if normalized in {"system status", "status", "pc status"}:
            info = get_system_status()
            return (
                f"OS: {info['os']}, CPU usage: {info['cpu_usage']}, memory usage: {info['memory_usage']}, "
                f"battery: {info['battery']}."
            )

        if normalized == "battery status":
            info = get_system_status()
            return f"Battery status is {info['battery']}."

        if normalized.startswith("open folder "):
            return open_folder(text[12:].strip())

        if normalized.startswith("open ") and len(text.split()) >= 2:
            target = text[5:].strip()
            if "." in target or target.lower() in {"youtube", "google", "github", "gmail"}:
                return open_website(target)
            return open_app(target)

        if normalized.startswith("search "):
            return search_web(text[7:].strip())

        if normalized.startswith("remember "):
            reminder = text[9:].strip()
            self.state.reminders.append(reminder)
            return f"I will remember this for now: {reminder}"

        if normalized == "show reminders":
            if not self.state.reminders:
                return "You do not have any reminders in this session."
            return "Your reminders are: " + "; ".join(self.state.reminders)

        if normalized in {"update yourself", "self update"}:
            return try_self_update()

        if normalized in {"help", "commands", "what can you do"}:
            return (
                "Try commands like hello, system status, battery status, open notepad, open youtube, "
                "open folder downloads, search python tutorials, remember buy milk, show reminders, time, date, and exit."
            )

        return self.brain.answer(text)


class JarvisAssistant:
    def __init__(self) -> None:
        self.settings = Settings()
        self.brain = Brain(self.settings)
        self.state = SessionState()
        self.router = CommandRouter(self.brain, self.state)
        self.voice = VoiceInterface(rate=self.settings.speech_rate)
        self.mode = self.settings.default_mode

    def run(self) -> None:
        print(f"{self.settings.assistant_name} starting...")
        self.select_mode()
        greeting = (
            f"Hello, I am {self.settings.assistant_name}. "
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

    def get_input(self) -> Optional[str]:
        if self.mode == "voice":
            print("Listening...")
            heard = self.voice.listen()
            if heard:
                print(f"You said: {heard}")
            return heard
        return input("You: ")

    def respond(self, message: str) -> None:
        print(f"{self.settings.assistant_name}: {message}")
        if self.mode == "voice" and self.voice.can_speak:
            self.voice.speak(message)


def main() -> None:
    assistant = JarvisAssistant()
    assistant.run()


if __name__ == "__main__":
    main()