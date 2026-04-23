import os
import sys
import subprocess
import datetime
import webbrowser
import platform
import shutil
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from threading import Thread

# ── Optional imports ───────────────────────────────────────────────────────
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  pip install pyttsx3")

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    print("⚠️  pip install SpeechRecognition pyaudio")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  pip install psutil")

try:
    import wikipedia
    WIKI_AVAILABLE = True
except ImportError:
    WIKI_AVAILABLE = False
    print("⚠️  pip install wikipedia")

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  pip install pyautogui")

try:
    from googlesearch import search as google_search
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("⚠️  pip install googlesearch-python")

# ── Language Configuration ─────────────────────────────────────────────────
LANG_DATA = {
    "english": {"code": "en-IN", "voice_keyword": "Zira",    "msg": "System Online. IGRIES V5 Ready."},
    "hindi":   {"code": "hi-IN", "voice_keyword": "Hemant",  "msg": "नमस्ते, मैं इग्रीस हूँ।"},
    "tamil":   {"code": "ta-IN", "voice_keyword": "Valluvar","msg": "வணக்கம், நான் இக்ரிஸ்."}
}

# Website shortcuts (expanded from both codebases)
WEBSITES = {
    "google"       : "https://www.google.com",
    "youtube"      : "https://www.youtube.com",
    "github"       : "https://www.github.com",
    "facebook"     : "https://www.facebook.com",
    "instagram"    : "https://www.instagram.com",
    "whatsapp"     : "https://web.whatsapp.com",
    "gmail"        : "https://mail.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "wikipedia"    : "https://www.wikipedia.org",
    "twitter"      : "https://www.twitter.com",
    "linkedin"     : "https://www.linkedin.com",
    "reddit"       : "https://www.reddit.com",
    "netflix"      : "https://www.netflix.com",
    "chatgpt"      : "https://chat.openai.com",
}

# ── TTS Engine Setup ───────────────────────────────────────────────────────
engine = None
voices = []
if TTS_AVAILABLE:
    engine = pyttsx3.init('sapi5' if platform.system() == 'Windows' else None)
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    for v in voices:
        if 'female' in v.name.lower() or 'zira' in v.name.lower():
            engine.setProperty('voice', v.id)
            break


# ══════════════════════════════════════════════════════════════════════════
#  IGRIES MEGA V5 — UNIFIED GUI + FULL SYSTEM ACCESS
# ══════════════════════════════════════════════════════════════════════════
class IgriesMegaV5:
    def __init__(self, root):
        self.root = root
        self.root.title("IGRIES — MEGA ASSISTANT V5.0 | UNIFIED SYSTEM")
        self.root.geometry("860x960")
        self.root.configure(bg="#020d18")
        self.root.resizable(True, True)

        self.current_lang    = "english"
        self.memory_file     = "igries_master_log.txt"
        self.listening_active = False

        self._setup_gui()
        self._set_voice("english")
        self.speak("Mega Systems Initialized. IGRIES Version 5 online. Full system access protocols active.")

    # ─────────────────────────────────────────────
    #  GUI SETUP
    # ─────────────────────────────────────────────
    def _setup_gui(self):
        # ── Header ──
        header_frame = tk.Frame(self.root, bg="#020d18")
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 0))

        tk.Label(header_frame, text="I G R I E S", font=("Impact", 44),
                 bg="#020d18", fg="#00d9ff").pack(side=tk.LEFT)
        tk.Label(header_frame, text="V5.0", font=("Consolas", 13),
                 bg="#020d18", fg="#ff6b35").pack(side=tk.LEFT, padx=10, anchor="s", pady=8)

        # ── Status bar ──
        status_frame = tk.Frame(self.root, bg="#020d18")
        status_frame.pack(fill=tk.X, padx=20)

        self.status_label = tk.Label(status_frame, text="● STANDBY",
                                     font=("Consolas", 10), bg="#020d18", fg="#00ff00")
        self.status_label.pack(side=tk.LEFT)

        self.lang_label = tk.Label(status_frame, text="[ENGLISH]",
                                   font=("Consolas", 10), bg="#020d18", fg="#aaaaaa")
        self.lang_label.pack(side=tk.LEFT, padx=20)

        self.time_label = tk.Label(status_frame, text="",
                                   font=("Consolas", 10), bg="#020d18", fg="#555555")
        self.time_label.pack(side=tk.RIGHT)
        self._update_clock()

        # ── Tab system ──
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook",          background="#020d18", borderwidth=0)
        style.configure("TNotebook.Tab",      background="#0b243b", foreground="#aaaaaa",
                        padding=[12, 5], font=("Consolas", 9))
        style.map("TNotebook.Tab",
                  background=[("selected","#00d9ff")],
                  foreground=[("selected","#020d18")])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # Tab 1 – Console
        tab_console = tk.Frame(notebook, bg="#020d18")
        notebook.add(tab_console, text="  🖥  CONSOLE  ")

        self.console = scrolledtext.ScrolledText(
            tab_console, font=("Consolas", 11), bg="#011627", fg="#00d9ff",
            state="disabled", wrap=tk.WORD, insertbackground="white",
            selectbackground="#00d9ff", selectforeground="#020d18")
        self.console.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Tab 2 – System Info
        tab_sys = tk.Frame(notebook, bg="#020d18")
        notebook.add(tab_sys, text="  📊  SYSTEM  ")

        self.sys_text = scrolledtext.ScrolledText(
            tab_sys, font=("Consolas", 10), bg="#011627", fg="#00ff99",
            state="disabled", wrap=tk.WORD)
        self.sys_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        sys_btn_frame = tk.Frame(tab_sys, bg="#020d18")
        sys_btn_frame.pack(fill=tk.X, padx=5, pady=4)
        tk.Button(sys_btn_frame, text="🔄 Refresh System Info", bg="#0b243b", fg="#00d9ff",
                  font=("Consolas", 9), command=self._refresh_system_info,
                  relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=4)

        # Tab 3 – Help
        tab_help = tk.Frame(notebook, bg="#011627")
        notebook.add(tab_help, text="  📋  HELP  ")
        self._build_help_tab(tab_help)

        # ── Input row ──
        input_frame = tk.Frame(self.root, bg="#020d18")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 6))

        self.input_box = tk.Entry(
            input_frame, font=("Arial", 14), bg="#0b243b", fg="white",
            insertbackground="white", borderwidth=0, relief=tk.FLAT)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
        self.input_box.bind("<Return>", lambda e: self._process_text())

        tk.Button(input_frame, text="▶ SEND", font=("Arial", 10, "bold"),
                  bg="#00d9ff", fg="#020d18", relief=tk.FLAT, cursor="hand2",
                  command=self._process_text).pack(side=tk.LEFT, ipady=8, ipadx=10)

        # ── Bottom button row ──
        btn_frame = tk.Frame(self.root, bg="#020d18")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 14))

        buttons = [
            ("🎤 VOICE", "#00d9ff", "#020d18", self._start_voice_thread),
            ("📋 REPORT", "#555555", "white",   self._generate_report),
            ("🇮🇳 HINDI", "#ff6b35", "white",   lambda: self._switch_lang("hindi")),
            ("🇮🇳 TAMIL", "#b026ff", "white",   lambda: self._switch_lang("tamil")),
            ("🇬🇧 ENG",   "#00d9ff", "#020d18", lambda: self._switch_lang("english")),
            ("❌ EXIT",   "#cc0000", "white",   self._exit_app),
        ]
        for label, bg, fg, cmd in buttons:
            tk.Button(btn_frame, text=label, font=("Arial", 9, "bold"),
                      bg=bg, fg=fg, relief=tk.FLAT, cursor="hand2",
                      command=cmd, padx=8, pady=4).pack(side=tk.LEFT, padx=5)

    def _build_help_tab(self, parent):
        help_text = scrolledtext.ScrolledText(
            parent, font=("Consolas", 10), bg="#011627", fg="#aaffaa",
            state="normal", wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        content = """
══════════════════════════════════════════════════
  IGRIES V5 — COMMAND REFERENCE
══════════════════════════════════════════════════

🕐 TIME & DATE
   "what is the time"  →  Current time
   "what is the date"  →  Current date

🌐 SEARCH & WEB
   "wikipedia <topic>"    →  Wikipedia summary
   "google <query>"       →  Google search
   "search <query>"       →  Google search
   "open <site/app>"      →  Open website or app

📁 FILE & FOLDER OPERATIONS
   "show files [path]"    →  List directory contents
   "open folder <path>"   →  Open folder in explorer
   "create file <name>"   →  Create a new file
   "delete <name>"        →  Delete a file or folder
   "search file <name>"   →  Find files recursively
   "run python <file>"    →  Execute a Python script

💻 SYSTEM
   "system info"          →  OS, CPU, RAM, Disk stats
   "list apps"            →  Show running processes
   "battery"              →  Battery percentage & status
   "cpu"                  →  CPU usage
   "screenshot"           →  Take a screenshot

🌍 LANGUAGE MODES
   "hindi mode"           →  Switch to Hindi
   "tamil mode"           →  Switch to Tamil
   "english mode"         →  Switch to English

⚙️  OTHER
   "help"                 →  Show this help panel
   "generate report"      →  View session log
   "shutdown" / "exit"    →  Close IGRIES
══════════════════════════════════════════════════
"""
        help_text.insert(tk.END, content)
        help_text.config(state="disabled")

    def _update_clock(self):
        self.time_label.config(text=datetime.datetime.now().strftime("🕐 %H:%M:%S  %d %b %Y"))
        self.root.after(1000, self._update_clock)

    # ─────────────────────────────────────────────
    #  VOICE & SPEECH ENGINE
    # ─────────────────────────────────────────────
    def _set_voice(self, lang):
        if not TTS_AVAILABLE:
            return False
        target = LANG_DATA[lang]["voice_keyword"]
        for v in voices:
            if target.lower() in v.name.lower():
                engine.setProperty('voice', v.id)
                self.current_lang = lang
                self.lang_label.config(text=f"[{lang.upper()}]")
                return True
        self.current_lang = lang
        self.lang_label.config(text=f"[{lang.upper()}]")
        return False

    def _switch_lang(self, lang):
        self._set_voice(lang)
        self.speak(LANG_DATA[lang]["msg"])

    def log(self, sender, text):
        self.console.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        tag_color = "#00d9ff" if "IGRIES" in sender else "#ffaa00"
        self.console.insert(tk.END, f"[{timestamp}] {sender}: {text}\n\n")
        self.console.config(state="disabled")
        self.console.see(tk.END)
        # Persist to log file
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {sender}: {text}\n")

    def speak(self, text):
        print(f"\n🤖 IGRIES: {text}")
        self.log("IGRIES", text)
        if TTS_AVAILABLE and engine:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

    def _start_voice_thread(self):
        if not SR_AVAILABLE:
            self.speak("Voice recognition not available. Please install SpeechRecognition and pyaudio.")
            return
        Thread(target=self._voice_input, daemon=True).start()

    def _voice_input(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.status_label.config(text="● LISTENING", fg="red")
                r.adjust_for_ambient_noise(source, duration=0.6)
                audio = r.listen(source, timeout=6, phrase_time_limit=10)
            self.status_label.config(text="● RECOGNIZING", fg="yellow")
            query = r.recognize_google(audio, language=LANG_DATA[self.current_lang]["code"])
            self.log("YOU (Voice)", query)
            self._handle_logic(query.lower())
        except sr.WaitTimeoutError:
            self.speak("No voice detected. Please try again.")
        except sr.UnknownValueError:
            self.speak("Signal unclear. Please repeat.")
        except sr.RequestError:
            self.speak("Speech service unavailable. Use text mode.")
        except Exception as e:
            self.speak(f"Voice error: {e}")
        finally:
            self.status_label.config(text="● STANDBY", fg="#00ff00")

    def _process_text(self):
        query = self.input_box.get().strip()
        if query:
            self.log("YOU (Text)", query)
            self.input_box.delete(0, tk.END)
            Thread(target=self._handle_logic, args=(query.lower(),), daemon=True).start()

    # ─────────────────────────────────────────────
    #  SYSTEM TOOLS
    # ─────────────────────────────────────────────
    def _list_running_apps(self):
        if not PSUTIL_AVAILABLE:
            self.speak("psutil not installed. Run: pip install psutil")
            return
        apps = set()
        for proc in psutil.process_iter(['name']):
            try:
                apps.add(proc.info['name'])
            except Exception:
                continue
        self.speak(f"System is currently running {len(apps)} active processes. Logging to console.")
        self.log("SYSTEM", f"Active Processes ({len(apps)}): {', '.join(sorted(apps)[:30])} ...")

    def _list_directory(self, path="."):
        try:
            target = os.path.expanduser(path) if path else "."
            items  = os.listdir(target)
            folders = [i for i in items if os.path.isdir(os.path.join(target, i))]
            files   = [i for i in items if os.path.isfile(os.path.join(target, i))]
            summary = f"Contents of {os.path.abspath(target)}: {len(folders)} folder(s), {len(files)} file(s)."
            self.speak(summary)
            details = []
            for d in sorted(folders)[:15]:
                details.append(f"📁 {d}/")
            for f in sorted(files)[:20]:
                size = os.path.getsize(os.path.join(target, f))
                details.append(f"📄 {f}  ({size} bytes)")
            self.log("DIR", "\n".join(details))
        except PermissionError:
            self.speak("Permission denied to access that path.")
        except FileNotFoundError:
            self.speak("Directory not found.")
        except Exception as e:
            self.speak(f"Error: {e}")

    def _open_folder(self, path):
        try:
            abs_path = os.path.abspath(os.path.expanduser(path)) if path else os.getcwd()
            if not os.path.exists(abs_path):
                self.speak("Folder not found.")
                return
            if platform.system() == "Windows":
                os.startfile(abs_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", abs_path])
            else:
                subprocess.Popen(["xdg-open", abs_path])
            self.speak(f"Opening folder: {abs_path}")
        except Exception as e:
            self.speak(f"Could not open folder: {e}")

    def _open_app_or_website(self, name):
        if name in WEBSITES:
            webbrowser.open(WEBSITES[name])
            self.speak(f"Opening {name} in your browser.")
            return
        try:
            self.speak(f"Launching {name}...")
            if platform.system() == "Windows":
                os.system(f'start {name}')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", name])
            else:
                subprocess.Popen([name])
        except Exception as e:
            self.speak(f"Could not open {name}: {e}")

    def _file_manager(self, action, filename):
        try:
            if action == "create":
                with open(filename, 'w') as f:
                    f.write("")
                self.speak(f"File '{filename}' created successfully.")
            elif action == "delete":
                if os.path.isfile(filename):
                    os.remove(filename)
                    self.speak(f"File '{filename}' deleted.")
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
                    self.speak(f"Folder '{filename}' deleted.")
                else:
                    self.speak("File or folder not found.")
        except Exception as e:
            self.speak(f"File operation error: {e}")

    def _search_files(self, name, path="."):
        self.speak(f"Searching for '{name}'...")
        results = []
        for root_dir, dirs, files in os.walk(path):
            for item in files + dirs:
                if name.lower() in item.lower():
                    results.append(os.path.join(root_dir, item))
        if results:
            self.speak(f"Found {len(results)} result(s).")
            display = []
            for r in results[:12]:
                tag = "📁" if os.path.isdir(r) else "📄"
                display.append(f"{tag} {r}")
            self.log("SEARCH", "\n".join(display))
        else:
            self.speak("No matching files found.")

    def _run_python_file(self, filename):
        filename = filename.strip()
        if not filename.endswith(".py"):
            filename += ".py"
        if os.path.exists(filename):
            self.speak(f"Running {filename}...")
            Thread(target=lambda: os.system(f'python "{filename}"'), daemon=True).start()
        else:
            self.speak(f"Python file '{filename}' not found.")

    def _battery_status(self):
        if not PSUTIL_AVAILABLE:
            self.speak("psutil not installed.")
            return
        battery = psutil.sensors_battery()
        if battery:
            status = "Charging" if battery.power_plugged else "On battery"
            self.speak(f"Battery is at {int(battery.percent)} percent. {status}.")
        else:
            self.speak("Battery information not available on this device.")

    def _cpu_status(self):
        if not PSUTIL_AVAILABLE:
            self.speak("psutil not installed.")
            return
        self.speak(f"Processor load is at {psutil.cpu_percent(interval=0.5)} percent.")

    def _take_screenshot(self):
        if not PYAUTOGUI_AVAILABLE:
            self.speak("pyautogui not installed. Run: pip install pyautogui")
            return
        fname = f"igries_capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(fname)
        self.speak(f"Screenshot saved as {fname}.")

    def _refresh_system_info(self):
        self.sys_text.config(state="normal")
        self.sys_text.delete("1.0", tk.END)
        lines = [
            "═" * 48,
            "  IGRIES V5 — SYSTEM DIAGNOSTICS",
            "═" * 48,
            f"  OS        : {platform.system()} {platform.release()}",
            f"  Machine   : {platform.machine()}",
            f"  Node      : {platform.node()}",
            f"  Processor : {platform.processor()[:50]}",
            f"  Python    : {platform.python_version()}",
        ]
        if PSUTIL_AVAILABLE:
            ram  = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            cpu  = psutil.cpu_percent(interval=0.5)