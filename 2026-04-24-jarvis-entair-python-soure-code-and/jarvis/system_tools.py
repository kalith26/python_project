from __future__ import annotations

import datetime as dt
import os
import platform
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict

import psutil


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
    git_dir = Path(".git")
    if not git_dir.exists():
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
