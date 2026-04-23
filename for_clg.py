import os, threading, queue, datetime, webbrowser, subprocess, platform, shutil, json
import tkinter as tk
from tkinter import scrolledtext

# Optional modules
try:
    import pyttsx3
    engine = pyttsx3.init()
    TTS = True
except:
    TTS = False

try:
    import speech_recognition as sr
    SR = True
except:
    SR = False

try:
    import psutil
    PSUTIL = True
except:
    PSUTIL = False

try:
    import wikipedia
    WIKI = True
except:
    WIKI = False


# ==============================
# MEMORY SYSTEM
# ==============================
class Memory:
    def __init__(self):
        self.file = "memory.json"
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            return json.load(open(self.file))
        return {}

    def save(self):
        json.dump(self.data, open(self.file, "w"))

    def set(self, k, v):
        self.data[k] = v
        self.save()

    def get(self, k):
        return self.data.get(k, "No memory found")


# ==============================
# ENGINE
# ==============================
class Engine:
    def __init__(self, app):
        self.app = app
        self.mode = "V7"

    def run(self, q):

        # -------- V5 --------
        if self.mode == "V5":
            if "time" in q:
                return datetime.datetime.now().strftime("%H:%M:%S")
            if "date" in q:
                return datetime.datetime.now().strftime("%d %B %Y")
            return "V5: command not found"

        # -------- V6 --------
        if self.mode == "V6":
            if "cpu" in q and PSUTIL:
                return f"CPU {psutil.cpu_percent()}%"
            if "list files" in q:
                return "\n".join(os.listdir(".")[:20])

        # -------- V7 --------
        # Memory
        if q.startswith("remember"):
            try:
                k, v = q.replace("remember", "").split("=")
                self.app.memory.set(k.strip(), v.strip())
                return "Saved"
            except:
                return "Use: remember key=value"

        if q.startswith("recall"):
            return self.app.memory.get(q.replace("recall", "").strip())

        # Web
        if q.startswith("google"):
            webbrowser.open(f"https://google.com/search?q={q[7:]}")
            return "Searching Google"

        # Wiki
        if q.startswith("wiki") and WIKI:
            try:
                return wikipedia.summary(q[5:], 2)
            except:
                return "No result found"

        # System
        if "system info" in q:
            return platform.system()

        # File
        if "list files" in q:
            return "\n".join(os.listdir("."))

        if q.startswith("create file"):
            name = q.replace("create file", "").strip()
            open(name, "w").close()
            return "File created"

        # Mode switch
        if "mode v5" in q:
            self.mode = "V5"
            return "Switched to V5"

        if "mode v6" in q:
            self.mode = "V6"
            return "Switched to V6"

        if "mode v7" in q:
            self.mode = "V7"
            return "Switched to V7"

        if "exit" in q:
            self.app.root.quit()

        return "Command not recognized"


# ==============================
# MAIN APP
# ==============================
class Igries:
    def __init__(self, root):
        self.root = root
        self.root.title("IGRIES V7 ULTRA SUITE")
        self.root.geometry("900x950")

        self.queue = queue.Queue()
        self.memory = Memory()
        self.engine = Engine(self)

        self.voice_active = False

        self.build_ui()
        self.speak("Igries ready")

        self.root.after(100, self.update_ui)

    # ---------------- UI SAFE ----------------
    def update_ui(self):
        while not self.queue.empty():
            self.queue.get()()
        self.root.after(100, self.update_ui)

    def safe(self, f):
        self.queue.put(f)

    # ---------------- UI ----------------
    def build_ui(self):

        # TOP BAR
        top = tk.Frame(self.root)
        top.pack(fill=tk.X)

        tk.Label(top, text="IGRIES ULTRA SUITE", font=("Impact", 30)).pack(side=tk.LEFT)

        self.status_label = tk.Label(top, text="VOICE: OFF", fg="red", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=5)

        self.toggle_btn = tk.Button(top, text="START VOICE", bg="red",
                                    command=self.toggle_voice)
        self.toggle_btn.pack(side=tk.RIGHT, padx=10)

        # CONSOLE
        self.console = scrolledtext.ScrolledText(self.root, font=("Consolas", 11))
        self.console.pack(fill=tk.BOTH, expand=True)

        # INPUT LABEL
        tk.Label(self.root, text="Enter Command:", font=("Arial", 10)).pack()

        # INPUT
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)

        self.input = tk.Entry(frame, font=("Arial", 12))
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input.bind("<Return>", lambda e: self.start())

        tk.Button(frame, text="SEND", command=self.start).pack(side=tk.LEFT)
        tk.Button(frame, text="🎤 ONE", command=self.voice_once).pack(side=tk.LEFT)

    # ---------------- LOG ----------------
    def log(self, sender, text):
        def f():
            self.console.insert(tk.END, f"{sender}: {text}\n")
            self.console.see(tk.END)
        self.safe(f)

    def speak(self, text):
        self.log("IGRIES", text)
        if TTS:
            threading.Thread(target=lambda: engine.say(text) or engine.runAndWait(), daemon=True).start()

    # ---------------- COMMAND ----------------
    def start(self):
        q = self.input.get()
        self.input.delete(0, tk.END)
        self.log("YOU", q)
        threading.Thread(target=self.process, args=(q.lower(),), daemon=True).start()

    def process(self, q):
        res = self.engine.run(q)
        if res:
            self.speak(res)

    # ---------------- VOICE ----------------
    def toggle_voice(self):
        self.voice_active = not self.voice_active

        if self.voice_active:
            self.toggle_btn.config(text="STOP VOICE", bg="green")
            self.status_label.config(text="VOICE: ON", fg="green")
            threading.Thread(target=self.voice_loop, daemon=True).start()
            self.speak("Voice mode activated")
        else:
            self.toggle_btn.config(text="START VOICE", bg="red")
            self.status_label.config(text="VOICE: OFF", fg="red")
            self.speak("Voice mode stopped")

    def voice_loop(self):
        if not SR:
            self.speak("SpeechRecognition not installed")
            return

        r = sr.Recognizer()

        while self.voice_active:
            try:
                with sr.Microphone() as src:
                    self.log("SYSTEM", "Listening...")
                    audio = r.listen(src, timeout=5)
                    q = r.recognize_google(audio)

                    self.log("VOICE", q)
                    self.process(q.lower())

            except sr.WaitTimeoutError:
                self.log("SYSTEM", "No voice detected")

            except Exception as e:
                self.log("ERROR", str(e))

    def voice_once(self):
        if not SR:
            self.speak("Install SpeechRecognition")
            return

        threading.Thread(target=self._voice_once, daemon=True).start()

    def _voice_once(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as src:
                self.speak("Listening")
                audio = r.listen(src)
                q = r.recognize_google(audio)
                self.log("VOICE", q)
                self.process(q.lower())
        except Exception as e:
            self.log("ERROR", str(e))


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = Igries(root)
    root.mainloop()