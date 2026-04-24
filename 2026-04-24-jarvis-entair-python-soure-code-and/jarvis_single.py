from __future__ import annotations

import datetime as dt
import json
import os
import platform
import subprocess
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import psutil
import requests

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
    ai_provider: str = os.getenv("JARVIS_AI_PROVIDER", "google")
    ai_api_key: str = os.getenv("JARVIS_AI_API_KEY", "")
    google_model: str = os.getenv("JARVIS_GOOGLE_MODEL", "gemini-2.5-flash")


@dataclass
class SessionState:
    reminders: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    history: List[str] = field(default_factory=list)
    profile: Dict[str, str] = field(default_factory=dict)


class SessionStorage:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.base_dir / "jarvis_memory.json"

    def load_state(self) -> SessionState:
        if not self.memory_file.exists():
            return SessionState()

        try:
            payload = json.loads(self.memory_file.read_text(encoding="utf-8"))
        except Exception:
            return SessionState()

        return SessionState(
            reminders=payload.get("reminders", []),
            notes=payload.get("notes", []),
            history=payload.get("history", []),
            profile=payload.get("profile", {}),
        )

    def save_state(self, state: SessionState) -> None:
        payload = {
            "reminders": state.reminders[-100:],
            "notes": state.notes[-100:],
            "history": state.history[-200:],
            "profile": state.profile,
        }
        self.memory_file.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )


class HumanSupport:
    def __init__(self) -> None:
        self.motivations = [
            "You are doing better than you think. One step at a time is enough.",
            "Small progress still counts. We can keep this simple.",
            "You can give me one short command and I will work from there.",
            "Stay calm. We can break the task into easy pieces.",
        ]
        self.productivity_tips = [
            "Close extra windows and keep only the task you care about in front.",
            "Use short commands like 'open notepad' or 'save note buy groceries'.",
            "If you feel stuck, ask for help, summary, or next step.",
        ]
        self.greetings = {
            "good morning": "Good morning. I hope your day starts smoothly.",
            "good afternoon": "Good afternoon. I am ready to help with your tasks.",
            "good evening": "Good evening. Let us make the rest of your day easier.",
        }

    def motivation(self) -> str:
        minute = dt.datetime.now().minute
        return self.motivations[minute % len(self.motivations)]

    def productivity(self) -> str:
        second = dt.datetime.now().second
        return self.productivity_tips[second % len(self.productivity_tips)]

    def greeting_reply(self, normalized: str) -> Optional[str]:
        return self.greetings.get(normalized)


class UtilityToolkit:
    def __init__(self) -> None:
        self.allowed_expression_chars = set("0123456789+-*/().% ")

    def calculate(self, expression: str) -> str:
        if not expression:
            return "Please give me an expression like calculate 25 * 12."

        if any(char not in self.allowed_expression_chars for char in expression):
            return "Only simple math expressions are allowed."

        try:
            result = eval(expression, {"__builtins__": {}}, {})
        except Exception as exc:
            return f"I could not calculate that: {exc}"

        return f"The answer is {result}."

    def make_summary(self, state: SessionState) -> str:
        profile_name = state.profile.get("name", "friend")
        reminder_count = len(state.reminders)
        note_count = len(state.notes)
        history_count = len(state.history)
        return (
            f"Session summary for {profile_name}: {reminder_count} reminders, "
            f"{note_count} notes, and {history_count} recent interactions saved."
        )

    def list_examples(self) -> str:
        return (
            "Examples: open notepad, open youtube, open folder downloads, system status, "
            "save note meeting at 5, show notes, remember call mom, show reminders, "
            "set name Alex, profile, calculate 45 / 9, history, motivate me, and exit."
        )

    def build_detailed_help(self) -> str:
        return (
            "Available command groups: greetings, time/date, system status, open app, open website, "
            "open folder, search web, reminders, notes, profile, calculator, history, session summary, "
            "motivation, productivity advice, Google AI chat, and self update."
        )


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
            "help me focus": (
                "Start with one small action, remove distractions, and ask me for the next step when ready."
            ),
            "how can i learn ai": (
                "Learn Python, math basics, machine learning concepts, and practice by building small projects."
            ),
            "what is human intelligence": (
                "Human intelligence includes reasoning, emotional understanding, creativity, memory, and adaptation."
            ),
        }
        self.system_prompt = (
            "You are Jarvis Entair, a friendly advanced AI assistant for a human user. "
            "Reply clearly, briefly, and helpfully. Give practical steps when useful."
        )

    def ask_google_ai(self, message: str) -> Optional[str]:
        if self.settings.ai_provider != "google" or not self.settings.ai_api_key:
            return None

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.settings.google_model}:generateContent"
        )
        payload = {
            "systemInstruction": {
                "parts": [
                    {
                        "text": self.system_prompt,
                    }
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": message,
                        }
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 300,
            },
        }

        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": self.settings.ai_api_key,
                },
                json=payload,
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
        except Exception:
            return None

        candidates = data.get("candidates", [])
        if not candidates:
            return None

        parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [part.get("text", "").strip() for part in parts if part.get("text")]
        if not text_parts:
            return None

        return "\n".join(text_parts)

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

        ai_response = self.ask_google_ai(message)
        if ai_response:
            return ai_response

        return (
            "I do not have a full answer for that yet, but I can still help with system commands, "
            "web search, voice use, reminders, and basic AI concepts. "
            "Set JARVIS_AI_API_KEY to enable Google Gemini answers."
        )


def format_system_status() -> str:
    info = get_system_status()
    return (
        f"OS: {info['os']}, machine: {info['machine']}, processor: {info['processor']}, "
        f"CPU usage: {info['cpu_usage']}, memory usage: {info['memory_usage']}, "
        f"battery: {info['battery']}, time: {info['time']}, date: {info['date']}."
    )


def get_disk_status() -> str:
    usage = psutil.disk_usage(Path.home().anchor)
    total_gb = round(usage.total / (1024 ** 3), 2)
    used_gb = round(usage.used / (1024 ** 3), 2)
    free_gb = round(usage.free / (1024 ** 3), 2)
    return (
        f"Disk usage on the main drive is {usage.percent} percent. "
        f"Used {used_gb} GB of {total_gb} GB, free space {free_gb} GB."
    )


def get_network_status() -> str:
    counters = psutil.net_io_counters()
    sent_mb = round(counters.bytes_sent / (1024 ** 2), 2)
    recv_mb = round(counters.bytes_recv / (1024 ** 2), 2)
    return f"Network summary: sent {sent_mb} MB and received {recv_mb} MB since boot."


def normalize_profile_key(raw_key: str) -> str:
    return raw_key.strip().lower().replace(" ", "_")


def ensure_text_after_prefix(text: str, prefix: str) -> str:
    return text[len(prefix):].strip()


def format_list(title: str, values: List[str]) -> str:
    if not values:
        return f"No {title.lower()} available."
    numbered = [f"{index + 1}. {value}" for index, value in enumerate(values)]
    return f"{title}:\n" + "\n".join(numbered)


class PersonalOrganizer:
    def __init__(self, state: SessionState, storage: SessionStorage) -> None:
        self.state = state
        self.storage = storage

    def remember(self, reminder: str) -> str:
        if not reminder:
            return "Please tell me what you want to remember."
        self.state.reminders.append(reminder)
        self.storage.save_state(self.state)
        return f"I will remember this: {reminder}"

    def show_reminders(self) -> str:
        return format_list("Reminders", self.state.reminders)

    def clear_reminders(self) -> str:
        self.state.reminders.clear()
        self.storage.save_state(self.state)
        return "All reminders were cleared."

    def save_note(self, note: str) -> str:
        if not note:
            return "Please give me a note to save."
        timestamp = dt.datetime.now().strftime("%d %b %Y %I:%M %p")
        entry = f"[{timestamp}] {note}"
        self.state.notes.append(entry)
        self.storage.save_state(self.state)
        return "Your note has been saved."

    def show_notes(self) -> str:
        return format_list("Notes", self.state.notes)

    def clear_notes(self) -> str:
        self.state.notes.clear()
        self.storage.save_state(self.state)
        return "All saved notes were cleared."

    def set_profile_field(self, key: str, value: str) -> str:
        if not key or not value:
            return "Use set profile <field> = <value>."
        safe_key = normalize_profile_key(key)
        self.state.profile[safe_key] = value.strip()
        self.storage.save_state(self.state)
        return f"Profile updated: {safe_key} = {value.strip()}"

    def set_name(self, name: str) -> str:
        if not name:
            return "Please give me a name to save."
        self.state.profile["name"] = name.strip()
        self.storage.save_state(self.state)
        return f"Nice to meet you, {name.strip()}."

    def show_profile(self) -> str:
        if not self.state.profile:
            return "Your profile is empty. Use set name or set profile."
        profile_lines = [f"{key}: {value}" for key, value in sorted(self.state.profile.items())]
        return "Profile:\n" + "\n".join(profile_lines)

    def clear_profile(self) -> str:
        self.state.profile.clear()
        self.storage.save_state(self.state)
        return "Your profile has been cleared."

    def add_history(self, command: str) -> None:
        clean_command = command.strip()
        if not clean_command:
            return
        timestamp = dt.datetime.now().strftime("%H:%M:%S")
        self.state.history.append(f"[{timestamp}] {clean_command}")
        self.storage.save_state(self.state)

    def show_history(self) -> str:
        recent = self.state.history[-20:]
        return format_list("History", recent)


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
    def __init__(
        self,
        brain: Brain,
        state: SessionState,
        organizer: PersonalOrganizer,
        support: HumanSupport,
        toolkit: UtilityToolkit,
    ) -> None:
        self.brain = brain
        self.state = state
        self.organizer = organizer
        self.support = support
        self.toolkit = toolkit

    def handle(self, raw_text: str) -> str:
        text = raw_text.strip()
        normalized = text.lower()
        self.organizer.add_history(text)

        if not text:
            return "Please say or type something."

        if normalized in {"exit", "quit", "stop"}:
            return "__exit__"

        greeting_reply = self.support.greeting_reply(normalized)
        if greeting_reply:
            return greeting_reply

        if normalized in {"hello", "hi", "hey"}:
            return "Hello. I am ready to help you."

        if normalized in {"time", "what time is it"}:
            return f"The current time is {dt.datetime.now().strftime('%I:%M %p')}."

        if normalized in {"date", "today date", "what is the date"}:
            return f"Today is {dt.datetime.now().strftime('%d %B %Y')}."

        if normalized in {"system status", "status", "pc status"}:
            return format_system_status()

        if normalized == "battery status":
            info = get_system_status()
            return f"Battery status is {info['battery']}."

        if normalized in {"disk status", "storage status"}:
            return get_disk_status()

        if normalized in {"network status", "internet status"}:
            return get_network_status()

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
            return self.organizer.remember(ensure_text_after_prefix(text, "remember "))

        if normalized == "show reminders":
            return self.organizer.show_reminders()

        if normalized == "clear reminders":
            return self.organizer.clear_reminders()

        if normalized.startswith("save note "):
            return self.organizer.save_note(ensure_text_after_prefix(text, "save note "))

        if normalized == "show notes":
            return self.organizer.show_notes()

        if normalized == "clear notes":
            return self.organizer.clear_notes()

        if normalized.startswith("set name "):
            return self.organizer.set_name(ensure_text_after_prefix(text, "set name "))

        if normalized.startswith("set profile ") and "=" in text:
            profile_text = ensure_text_after_prefix(text, "set profile ")
            key, value = profile_text.split("=", 1)
            return self.organizer.set_profile_field(key, value)

        if normalized == "profile":
            return self.organizer.show_profile()

        if normalized == "clear profile":
            return self.organizer.clear_profile()

        if normalized == "history":
            return self.organizer.show_history()

        if normalized.startswith("calculate "):
            return self.toolkit.calculate(ensure_text_after_prefix(text, "calculate "))

        if normalized in {"summary", "session summary"}:
            return self.toolkit.make_summary(self.state)

        if normalized in {"motivate me", "motivation"}:
            return self.support.motivation()

        if normalized in {"productivity tip", "focus tip"}:
            return self.support.productivity()

        if normalized == "examples":
            return self.toolkit.list_examples()

        if normalized in {"update yourself", "self update"}:
            return try_self_update()

        if normalized in {"help", "commands"}:
            return self.toolkit.build_detailed_help()

        if normalized == "what can you do":
            return (
                "I can chat, answer AI questions, use Google Gemini, open apps and websites, read system status, "
                "save notes, manage reminders, remember profile information, calculate expressions, and support voice mode."
            )

        return self.brain.answer(text)


class JarvisAssistant:
    def __init__(self) -> None:
        self.settings = Settings()
        self.storage = SessionStorage(Path.cwd())
        self.brain = Brain(self.settings)
        self.state = self.storage.load_state()
        self.organizer = PersonalOrganizer(self.state, self.storage)
        self.support = HumanSupport()
        self.toolkit = UtilityToolkit()
        self.router = CommandRouter(
            self.brain,
            self.state,
            self.organizer,
            self.support,
            self.toolkit,
        )
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
        self.respond(self.startup_snapshot())

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

    def startup_snapshot(self) -> str:
        name = self.state.profile.get("name", "friend")
        return (
            f"Welcome back, {name}. "
            f"I currently remember {len(self.state.reminders)} reminders and {len(self.state.notes)} notes. "
            "Say help for commands or examples for sample prompts."
        )

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
