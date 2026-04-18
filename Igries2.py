import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import psutil
import pyautogui
import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread

# --- CORE ENGINE CONFIGURATION ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 185)

# Language Data Map
LANG_DATA = {
    "english": {"code": "en-IN", "voice_keyword": "Zira", "msg": "System Online."},
    "hindi": {"code": "hi-IN", "voice_keyword": "Hemant", "msg": "नमस्ते, मैं इग्रीस हूँ।"},
    "tamil": {"code": "ta-IN", "voice_keyword": "Valluvar", "msg": "வணக்கம், நான் இக்ரிஸ்."}
}

class MegaIgries:
    def __init__(self, root):
        self.root = root
        self.root.title("IGRIES - MEGA ASSISTANT V4.0")
        self.root.geometry("700x800")
        self.root.configure(bg="#020d18")
        self.current_lang = "english"
        self.memory_file = "igries_master_log.txt"

        self.setup_gui()
        self.set_voice("english")
        self.speak("Mega Systems Initialized. All protocols active.")

    # --- GUI INTERFACE ---
    def setup_gui(self):
        # Header Area
        self.header = tk.Label(self.root, text="I G R I E S", font=("Impact", 40), bg="#020d18", fg="#00d9ff")
        self.header.pack(pady=10)

        # Status Bar
        self.status = tk.Label(self.root, text="● STANDBY", font=("Consolas", 10), bg="#020d18", fg="#00ff00")
        self.status.pack()

        # Main Display Console
        self.console = scrolledtext.ScrolledText(self.root, font=("Consolas", 11), bg="#011627", fg="#00d9ff", state='disabled', wrap=tk.WORD)
        self.console.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Writing Input Model
        self.input_box = tk.Entry(self.root, font=("Arial", 14), bg="#0b243b", fg="white", insertbackground="white", borderwidth=0)
        self.input_box.pack(padx=20, pady=10, fill=tk.X)
        self.input_box.bind("<Return>", lambda e: self.process_text())

        # Control Buttons
        btn_frame = tk.Frame(self.root, bg="#020d18")
        btn_frame.pack(pady=10)

        self.v_btn = tk.Button(btn_frame, text="🎤 VOICE ACCESS", font=("Arial", 10, "bold"), bg="#00d9ff", command=self.start_voice_thread)
        self.v_btn.grid(row=0, column=0, padx=10)

        self.m_btn = tk.Button(btn_frame, text="📋 GENERATE REPORT", font=("Arial", 10, "bold"), bg="#555", fg="white", command=self.generate_report)
        self.m_btn.grid(row=0, column=1, padx=10)

    # --- CORE FUNCTIONS ---
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
        # Save to permanent memory
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(f"{sender}: {text} ({datetime.datetime.now()})\n")

    def speak(self, text):
        self.log("IGRIES", text)
        engine.say(text)
        engine.runAndWait()

    def start_voice_thread(self):
        Thread(target=self.voice_input, daemon=True).start()

    # --- INPUT MODEL 1: VOICE ---
    def voice_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.status.config(text="● LISTENING", fg="red")
            r.adjust_for_ambient_noise(source, duration=0.6)
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

    # --- INPUT MODEL 2: WRITING ---
    def process_text(self):
        query = self.input_box.get()
        if query:
            self.log("YOU (Text)", query)
            self.input_box.delete(0, tk.END)
            self.handle_logic(query.lower())

    # --- BRAIN: ADVANCED LOGIC ---
    def handle_logic(self, query):
        # 1. DATABASE/WIKI SEARCH
        if 'wikipedia' in query:
            topic = query.replace("wikipedia", "").strip()
            self.speak(f"Accessing archives for {topic}...")
            try:
                info = wikipedia.summary(topic, sentences=2)
                self.speak(info)
            except: self.speak("No data found.")

        # 2. WEB NAVIGATION
        elif 'google search' in query:
            term = query.replace("google search", "").strip()
            self.speak(f"Searching Google for {term}")
            webbrowser.open(f"https://google.com{term}")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        # 3. SYSTEM UTILITIES
        elif 'battery' in query:
            batt = psutil.sensors_battery()
            self.speak(f"System battery is at {batt.percent} percent.")

        elif 'cpu' in query:
            use = psutil.cpu_percent()
            self.speak(f"Current processor load is {use} percent.")

        elif 'screenshot' in query:
            pyautogui.screenshot("igries_capture.png")
            self.speak("Screenshot saved to root folder.")

        # 4. MEMORY REPOSTING
        elif 'report' in query or 'repost' in query:
            self.generate_report()

        # 5. LANGUAGE MODES
        elif 'tamil mode' in query:
            if self.set_voice("tamil"): self.speak(LANG_DATA["tamil"]["msg"])
        elif 'hindi mode' in query:
            if self.set_voice("hindi"): self.speak(LANG_DATA["hindi"]["msg"])
        elif 'english mode' in query:
            self.set_voice("english")
            self.speak("Restored English protocols.")

        # 6. TIME
        elif 'the time' in query:
            self.speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")

        # 7. EXIT
        elif 'shutdown' in query or 'exit' in query:
            self.speak("Mega Systems powering down. Goodbye.")
            self.root.destroy()

    def generate_report(self):
        """Displays and speaks all user commands from memory."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                data = f.readlines()
                last_items = "".join(data[-5:]) # Last 5 commands
                self.speak("Displaying recent system instructions.")
                messagebox.showinfo("Igries Memory Report", last_items)
        else:
            self.speak("No historical data found.")

# --- EXECUTION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MegaIgries(root)
    root.mainloop()