import datetime as dt
import subprocess
import sys
import webbrowser

import pyttsx3
import speech_recognition as sr


class VoiceAssistant:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "chatgpt": "https://chat.openai.com",
        }

        self.desktop_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "command prompt": "cmd.exe",
        }

    def speak(self, text: str) -> None:
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str | None:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)

            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            self.speak("I did not hear anything.")
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand that.")
            return None
        except sr.RequestError:
            self.speak("Speech service is unavailable right now.")
            return None

    def open_website(self, command: str) -> bool:
        for name, url in self.websites.items():
            if f"open {name}" in command:
                webbrowser.open(url)
                self.speak(f"Opening {name}.")
                return True
        return False

    def open_desktop_app(self, command: str) -> bool:
        for name, executable in self.desktop_apps.items():
            if f"open {name}" in command:
                subprocess.Popen(executable, shell=True)
                self.speak(f"Opening {name}.")
                return True
        return False

    def tell_time(self) -> bool:
        now = dt.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {now}.")
        return True

    def tell_date(self) -> bool:
        today = dt.datetime.now().strftime("%A, %d %B %Y")
        self.speak(f"Today is {today}.")
        return True

    def search_web(self, command: str) -> bool:
        prefixes = ("search ", "google ")
        for prefix in prefixes:
            if command.startswith(prefix):
                query = command.removeprefix(prefix).strip()
                if query:
                    webbrowser.open(
                        f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    )
                    self.speak(f"Searching for {query}.")
                    return True
        return False

    def type_text(self, command: str) -> bool:
        prefix = "type "
        if command.startswith(prefix):
            text = command.removeprefix(prefix).strip()
            if text:
                self.speak(
                    "Typing text requires pyautogui. Add it if you want keyboard control."
                )
                print(text)
                return True
        return False

    def run_custom_command(self, command: str) -> bool:
        if command == "shutdown":
            self.speak("Shutdown command is blocked for safety. Edit the code to allow it.")
            return True

        if command.startswith("run "):
            system_command = command.removeprefix("run ").strip()
            if system_command:
                subprocess.Popen(system_command, shell=True)
                self.speak(f"Running {system_command}.")
                return True
        return False

    def handle_command(self, command: str) -> bool:
        if any(word in command for word in ("exit", "quit", "stop")):
            self.speak("Goodbye.")
            return False

        if "time" in command:
            self.tell_time()
            return True

        if "date" in command or "day" in command:
            self.tell_date()
            return True

        if self.open_website(command):
            return True

        if self.open_desktop_app(command):
            return True

        if self.search_web(command):
            return True

        if self.type_text(command):
            return True

        if self.run_custom_command(command):
            return True

        self.speak("I heard you, but I do not know that command yet.")
        return True

    def run(self) -> None:
        self.speak("Voice assistant started. Say a command.")
        while True:
            try:
                command = self.listen()
                if not command:
                    continue

                should_continue = self.handle_command(command)
                if not should_continue:
                    break
            except KeyboardInterrupt:
                self.speak("Stopping assistant.")
                break
            except Exception as exc:
                self.speak("An unexpected error happened.")
                print(f"Error: {exc}", file=sys.stderr)


if __name__ == "__main__":
    VoiceAssistant().run()
