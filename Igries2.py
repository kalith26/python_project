import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import psutil
import pyautogui
import tkinter as tk
import platform
import subprocess
import shutil
from tkinter import scrolledtext, messagebox
from threading import Thread

# --- CORE ENGINE CONFIGURATION ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 185)

# Setting default female voice if available
for v in voices:
    if 'female' in v.name.lower() or 'zira' in v.name.lower():
        engine.setProperty('voice', v.id)
        break

LANG_DATA = {
    "english": {"code": "en-IN", "voice_keyword": "Zira", "msg": "System Online."},
    "hindi": {"code": "hi-IN", "voice_keyword": "Hemant", "msg": "नमस्ते, मैं इग्रीस हूँ।"},
    "tamil": {"code": "ta-IN", "voice_keyword": "Valluvar", "msg": "வணக்கம், நான் இக்ரிஸ்."}
}

class MegaIgries:
    def __init__(self, root):
        self.root = root
        self.root.title("IGRIES - MEGA ASSISTANT V4.0 (FULL SYSTEM ACCESS)")
        self.root.geometry("700x850")
        self.root.configure(bg="#020d18")
        self.current_lang = "english"
        self.memory_file = "igries_master_log.txt"

        self.setup_gui()
        self.set_voice("english")
        self.speak("Mega Systems Initialized. Full system access protocols active.")

    def setup_gui(self):
        self.header = tk.Label(self.root, text="I G R I E S", font=("Impact", 40), bg="#020d18", fg="#00d9ff")
        self.header.pack(pady=10)
        self.status = tk.Label(self.root, text="● STANDBY", font=("Consolas", 10), bg="#020d18", fg="#00ff00")
        self.status.pack()
        self.console = scrolledtext.ScrolledText(self.root, font=("Consolas", 11), bg="#011627", fg="#00d9ff", state='disabled', wrap=tk.WORD)
        self.console.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.input_box = tk.Entry(self.root, font=("Arial", 14), bg="#0b243b", fg="white", insertbackground="white", borderwidth=0)
        self.input_box.pack(padx=20, pady=10, fill=tk.X)
        self.input_box.bind("<Return>", lambda e: self.process_text())
        btn_frame = tk.Frame(self.root, bg="#020d18")
        btn_frame.pack(pady=10)
        self.v_btn = tk.Button(btn_frame, text="🎤 VOICE ACCESS", font=("Arial", 10, "bold"), bg="#00d9ff", command=self.start_voice_thread)
        self.v_btn.grid(row=0, column=0, padx=10)
        self.m_btn = tk.Button(btn_frame, text="📋 GENERATE REPORT", font=("Arial", 10, "bold"), bg="#555", fg="white", command=self.generate_report)
        self.m_btn.grid(row=0, column=1, padx=10)

    def set_voice(self, lang):
        target = LANG_DATA[lang]["voice_keyword"]
        for v in voices:
            if target.lower() in v.name.lower():
                engine.setProperty('voice', v.id)
                self.current_lang = lang
                return True
        return False

    def log(self, sender, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {sender}: {text}\n\n")
        self.console.config(state='disabled')
        self.console.see(tk.END)
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(f"{sender}: {text} ({datetime.datetime.now()})\n")

    def speak(self, text):
        self.log("IGRIES", text)
        engine.say(text)
        engine.runAndWait()

    def start_voice_thread(self):
        Thread(target=self.voice_input, daemon=True).start()

    def voice_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.status.config(text="● LISTENING", fg="red")
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio = r.listen(source)
        try:
            self.status.config(text="● RECOGNIZING", fg="yellow")
            query = r.recognize_google(audio, language=LANG_DATA[self.current_lang]["code"])
            self.log("YOU (Voice)", query)
            self.handle_logic(query.lower())
        except:
            self.speak("Signal weak. Please repeat.")
        finally:
            self.status.config(text="● STANDBY", fg="#00ff00")

    def process_text(self):
        query = self.input_box.get()
        if query:
            self.log("YOU (Text)", query)
            self.input_box.delete(0, tk.END)
            self.handle_logic(query.lower())

    # --- SYSTEM ACCESS UTILITIES ---
    def list_running_apps(self):
        apps = set()
        for proc in psutil.process_iter(['name']):
            try: apps.add(proc.info['name'])
            except: continue
        self.speak(f"System is currently running {len(apps)} processes. Check console for list.")
        print(f"ACTIVE APPS: {list(apps)}")

    def list_directory(self, path="."):
        try:
            target = os.path.expanduser(path)
            items = os.listdir(target)
            self.speak(f"Directory contains {len(items)} items. Logging results.")
            self.log("SYSTEM", f"Contents of {target}: {items[:20]}")
        except Exception as e:
            self.speak(f"Error accessing path: {e}")

    def open_app_or_website(self, name):
        websites = {
            "google": "https://www.google.com", "youtube": "https://www.youtube.com",
            "github": "https://www.github.com", "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com", "whatsapp": "https://web.whatsapp.com",
            "gmail": "https://mail.google.com", "stackoverflow": "https://stackoverflow.com"
        }
        if name in websites:
            webbrowser.open(websites[name])
            self.speak(f"Opening {name}!")
            return
        try:
            self.speak(f"Launching {name}...")
            if platform.system() == "Windows": os.system(f'start {name}')
            else: subprocess.Popen([name])
        except: self.speak(f"Could not open {name}.")

    def file_manager(self, action, filename):
        try:
            if action == "create":
                with open(filename, 'w') as f: f.write("")
                self.speak(f"File {filename} created.")
            elif action == "delete":
                if os.path.exists(filename):
                    if os.path.isfile(filename): os.remove(filename)
                    else: shutil.rmtree(filename)
                    self.speak(f"Item {filename} deleted.")
                else: self.speak("File not found.")
        except Exception as e: self.speak(f"File error: {e}")

    # --- BRAIN: UPDATED LOGIC ---
    def handle_logic(self, query):
        # 1. System Access Commands
        if 'list apps' in query or 'running processes' in query:
            self.list_running_apps()
        
        elif 'show files' in query:
            path = query.replace("show files", "").replace("in", "").strip()
            self.list_directory(path if path else ".")

        elif 'open folder' in query:
            path = query.replace("open folder", "").strip()
            if not path: path = "."
            os.startfile(os.path.abspath(path))
            self.speak(f"Opening folder at {path}")

        # 2. Existing Navigation & Search
        elif 'wikipedia' in query:
            topic = query.replace("wikipedia", "").strip()
            self.speak(f"Searching Wikipedia for {topic}...")
            try: self.speak(wikipedia.summary(topic, sentences=2))
            except: self.speak("No data found.")

        elif 'open' in query:
            target = query.replace("open", "").strip()
            self.open_app_or_website(target)

        elif 'google' in query or 'search' in query:
            term = query.replace("google", "").replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={term}")
            self.speak(f"Searching for {term}")

        # 3. File Operations
        elif 'create file' in query:
            fname = query.replace("create file", "").strip()
            self.file_manager("create", fname if fname else "new_file.txt")
        
        elif 'delete' in query:
            fname = query.replace("delete", "").strip()
            self.file_manager("delete", fname)

        # 4. Utilities
        elif 'battery' in query:
            self.speak(f"Battery is at {psutil.sensors_battery().percent} percent.")
        elif 'cpu' in query:
            self.speak(f"Processor load is {psutil.cpu_percent()} percent.")
        elif 'screenshot' in query:
            pyautogui.screenshot("igries_capture.png")
            self.speak("Screenshot saved.")
        elif 'the time' in query:
            self.speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")

        # 5. Language Modes
        elif 'tamil mode' in query:
            if self.set_voice("tamil"): self.speak(LANG_DATA["tamil"]["msg"])
        elif 'hindi mode' in query:
            if self.set_voice("hindi"): self.speak(LANG_DATA["hindi"]["msg"])
        elif 'english mode' in query:
            self.set_voice("english")
            self.speak("English mode active.")

        # 6. Exit
        elif 'shutdown' in query or 'exit' in query:
            self.speak("IGRIES powering down. Goodbye.")
            self.root.destroy()

    def generate_report(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                last_items = "".join(f.readlines()[-10:])
                messagebox.showinfo("Igries System Report", last_items)
        else: self.speak("No data found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MegaIgries(root)
    root.mainloop()