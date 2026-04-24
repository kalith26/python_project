from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import List

from jarvis.brain import Brain
from jarvis.system_tools import (
    get_system_status,
    open_app,
    open_folder,
    open_website,
    search_web,
    try_self_update,
)


@dataclass
class SessionState:
    reminders: List[str] = field(default_factory=list)


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
