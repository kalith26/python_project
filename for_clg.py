import os
import sys
import subprocess
import datetime
import webbrowser
import platform
import shutil
import time

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
    from googlesearch import search as google_search
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("⚠️  pip install googlesearch-python")

# ── Text-to-Speech Setup ───────────────────────────────────────────────────
engine = None
if TTS_AVAILABLE:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    voices = engine.getProperty('voices')
    for v in voices:
        if 'female' in v.name.lower() or 'zira' in v.name.lower():
            engine.setProperty('voice', v.id)
            break

def speak(text):
    print(f"\n🤖 Assistant: {text}")
    if TTS_AVAILABLE and engine:
        engine.say(text)
        engine.runAndWait()

# ── Voice Recognition ──────────────────────────────────────────────────────
def listen():
    if not SR_AVAILABLE:
        speak("Voice not available. Please type your command.")
        return None
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)
            print(f"🗣️  You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            speak("Speech service unavailable. Use text mode.")
            return None

# ── Wikipedia ──────────────────────────────────────────────────────────────
def search_wikipedia(query):
    if not WIKI_AVAILABLE:
        speak("Wikipedia not installed. Run: pip install wikipedia")
        return
    try:
        speak(f"Searching Wikipedia for {query}...")
        result = wikipedia.summary(query, sentences=4)
        speak("Here is what I found:")
        print(f"\n{'─'*50}")
        print(f"📖 Wikipedia: {query.title()}")
        print(f"{'─'*50}")
        print(f"{result}")
        print(f"{'─'*50}")
        url = wikipedia.page(query).url
        print(f"🔗 Read more: {url}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Multiple results found. Please be more specific.")
        print(f"   Suggestions: {e.options[:5]}")
    except wikipedia.exceptions.PageError:
        speak("No Wikipedia page found for that topic.")
    except Exception as e:
        speak(f"Wikipedia error: {e}")

# ── Google Search ──────────────────────────────────────────────────────────
def search_google(query):
    if not GOOGLE_AVAILABLE:
        # Fallback: open in browser
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Opened Google search for {query} in browser.")
        return
    try:
        speak(f"Googling {query}...")
        print(f"\n{'─'*50}")
        print(f"🔍 Google Results: {query}")
        print(f"{'─'*50}")
        results = list(google_search(query, num_results=5))
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result}")
        print(f"{'─'*50}")
        speak(f"Found {len(results)} results. Shown on screen!")
        open_browser = input("\n   Open in browser? (y/n): ").strip().lower()
        if open_browser == 'y':
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
    except Exception as e:
        speak(f"Google search failed: {e}")
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)

# ── File & Folder Operations ───────────────────────────────────────────────
def list_directory(path="."):
    try:
        items = os.listdir(path)
        if not items:
            speak(f"The folder is empty.")
            return
        speak(f"Contents of {os.path.abspath(path)}:")
        print(f"\n{'─'*50}")
        folders = [i for i in items if os.path.isdir(os.path.join(path, i))]
        files   = [i for i in items if os.path.isfile(os.path.join(path, i))]
        for folder in sorted(folders):
            print(f"   📁 {folder}/")
        for file in sorted(files):
            size = os.path.getsize(os.path.join(path, file))
            print(f"   📄 {file}  ({size} bytes)")
        print(f"{'─'*50}")
        print(f"   {len(folders)} folder(s), {len(files)} file(s)")
    except PermissionError:
        speak("Permission denied.")
    except FileNotFoundError:
        speak("Folder not found.")

def open_folder(path):
    try:
        if not os.path.exists(path):
            speak("Folder not found.")
            return
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        speak(f"Opening folder: {path}")
    except Exception as e:
        speak(f"Could not open folder: {e}")

def open_app_or_website(name):
    # Website shortcuts
    websites = {
        "google"      : "https://www.google.com",
        "youtube"     : "https://www.youtube.com",
        "github"      : "https://www.github.com",
        "facebook"    : "https://www.facebook.com",
        "instagram"   : "https://www.instagram.com",
        "whatsapp"    : "https://web.whatsapp.com",
        "gmail"       : "https://mail.google.com",
        "stackoverflow": "https://stackoverflow.com",
        "wikipedia"   : "https://www.wikipedia.org",
        "twitter"     : "https://www.twitter.com",
        "linkedin"    : "https://www.linkedin.com",
        "reddit"      : "https://www.reddit.com",
        "netflix"     : "https://www.netflix.com",
        "chatgpt"     : "https://chat.openai.com",
    }
    if name in websites:
        webbrowser.open(websites[name])
        speak(f"Opening {name} in your browser!")
        return
    # Try as system app
    try:
        speak(f"Trying to open {name}...")
        if platform.system() == "Windows":
            os.system(f'start {name}')
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            subprocess.Popen([name])
    except Exception as e:
        speak(f"Could not open {name}: {e}")

def create_file_cmd(filename):
    try:
        with open(filename, 'w') as f:
            f.write("")
        speak(f"File '{filename}' created successfully.")
    except Exception as e:
        speak(f"Error creating file: {e}")

def delete_file_cmd(filename):
    try:
        if os.path.isfile(filename):
            os.remove(filename)
            speak(f"File '{filename}' deleted.")
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
            speak(f"Folder '{filename}' deleted.")
        else:
            speak("File or folder not found.")
    except Exception as e:
        speak(f"Error: {e}")

def search_files(name, path="."):
    speak(f"Searching for '{name}'...")
    results = []
    for root, dirs, files in os.walk(path):
        for f in files + dirs:
            if name.lower() in f.lower():
                results.append(os.path.join(root, f))
    if results:
        speak(f"Found {len(results)} result(s):")
        print(f"\n{'─'*50}")
        for r in results[:10]:
            tag = "📁" if os.path.isdir(r) else "📄"
            print(f"   {tag} {r}")
        print(f"{'─'*50}")
    else:
        speak("No matching files found.")

def run_python_file(filename):
    filename = filename.strip()
    if not filename.endswith(".py"):
        filename += ".py"
    if os.path.exists(filename):
        speak(f"Running {filename}...")
        os.system(f'python "{filename}"')
    else:
        speak(f"Python file '{filename}' not found.")

# ── System Info ────────────────────────────────────────────────────────────
def system_info():
    speak("Here is your system information:")
    print(f"\n{'─'*50}")
    print(f"   🖥️  OS       : {platform.system()} {platform.release()}")
    print(f"   💻 Machine  : {platform.machine()}")
    print(f"   ⚙️  Processor: {platform.processor()}")
    if PSUTIL_AVAILABLE:
        ram  = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu  = psutil.cpu_percent(interval=1)
        print(f"   📊 CPU Usage: {cpu}%")
        print(f"   🧠 RAM      : {ram.used // (1024**2)} MB / {ram.total // (1024**2)} MB")
        print(f"   💾 Disk     : {disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB")
    print(f"{'─'*50}")

def battery_status():
    if not PSUTIL_AVAILABLE:
        speak("psutil not installed. Run: pip install psutil")
        return
    battery = psutil.sensors_battery()
    if battery:
        status = "Charging 🔌" if battery.power_plugged else "Not charging 🔋"
        speak(f"Battery is at {int(battery.percent)}%. {status}")
    else:
        speak("Battery info not available on this device.")

# ── Time ───────────────────────────────────────────────────────────────────
def get_time():
    now = datetime.datetime.now()
    speak(f"Current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d %Y')}.")

# ── Help ───────────────────────────────────────────────────────────────────
def show_help():
    speak("Here is everything I can do:")
    print(f"""
{'═'*55}
  📋  COMMAND LIST
{'═'*55}
  🕐 time / date              → Current time and date
  📁 list [path]              → List files in folder
  📂 open folder [path]       → Open folder in explorer
  🌐 open google/youtube/...  → Open websites
  🚀 open [appname]           → Open any application
  📄 create file [name]       → Create a new file
  🗑️  delete [name]            → Delete file or folder
  🔍 search file [name]       → Find files by name
  🐍 run [file.py]            → Run a Python script
  💻 system info              → CPU, RAM, Disk info
  🔋 battery                  → Check battery status
  📖 wiki [topic]             → Wikipedia search
  🔎 google [query]           → Google search results
  📍 current directory        → Show current path
  📁 go to [path]             → Change directory
  👋 exit / quit              → Close assistant
{'═'*55}
    """)

# ── Command Processor ──────────────────────────────────────────────────────
def process_command(cmd):
    cmd = cmd.lower().strip()
    if not cmd:
        return

    # Exit
    if any(w in cmd for w in ["exit", "quit", "bye", "goodbye"]):
        speak("Goodbye! Have a great day!")
        sys.exit(0)

    # Help
    elif any(w in cmd for w in ["help", "what can you do", "commands"]):
        show_help()

    # Time & Date
    elif any(w in cmd for w in ["time", "date", "day", "today"]):
        get_time()

    # Wikipedia
    elif any(w in cmd for w in ["wikipedia", "wiki", "who is", "what is", "tell me about"]):
        query = (cmd.replace("wikipedia", "")
                    .replace("wiki", "")
                    .replace("who is", "")
                    .replace("what is", "")
                    .replace("tell me about", "")
                    .strip())
        if query:
            search_wikipedia(query)
        else:
            speak("What do you want to search on Wikipedia?")

    # Google search
    elif "google" in cmd and "open" not in cmd:
        query = cmd.replace("google", "").strip()
        if query:
            search_google(query)
        else:
            speak("What do you want to Google?")

    # Search web (generic)
    elif cmd.startswith("search ") and "file" not in cmd:
        query = cmd.replace("search", "").strip()
        search_google(query)

    # List directory
    elif any(w in cmd for w in ["list", "show files", "show folder"]):
        parts = cmd.split()
        path = parts[-1] if len(parts) > 1 and os.path.exists(parts[-1]) else "."
        list_directory(path)

    # Open folder
    elif "open folder" in cmd:
        path = cmd.replace("open folder", "").strip() or "."
        open_folder(path)

    # Open app or website
    elif cmd.startswith("open "):
        name = cmd.replace("open", "").strip()
        open_app_or_website(name)

    # Create file
    elif "create file" in cmd:
        fname = cmd.replace("create file", "").strip()
        if fname:
            create_file_cmd(fname)
        else:
            speak("Please say: create file filename.txt")

    # Delete
    elif "delete" in cmd:
        fname = cmd.replace("delete", "").strip()
        if fname:
            delete_file_cmd(fname)
        else:
            speak("What do you want to delete?")

    # Search files
    elif any(w in cmd for w in ["search file", "find file", "find"]):
        name = (cmd.replace("search file", "")
                   .replace("find file", "")
                   .replace("find", "")
                   .strip())
        if name:
            search_files(name)
        else:
            speak("What file do you want to find?")

    # Run Python file
    elif "run" in cmd and ".py" in cmd:
        fname = cmd.replace("run", "").strip()
        run_python_file(fname)

    # System info
    elif any(w in cmd for w in ["system info", "system information", "pc info"]):
        system_info()

    # Battery
    elif "battery" in cmd:
        battery_status()

    # Current directory
    elif any(w in cmd for w in ["where am i", "current directory", "current folder", "pwd"]):
        speak(f"You are in: {os.getcwd()}")

    # Change directory
    elif any(w in cmd for w in ["go to", "cd ", "change directory"]):
        path = (cmd.replace("go to", "")
                   .replace("change directory", "")
                   .replace("cd", "")
                   .strip())
        try:
            os.chdir(path)
            speak(f"Moved to {os.getcwd()}")
        except Exception as e:
            speak(f"Cannot change directory: {e}")

    else:
        speak(f"I don't understand '{cmd}'. Say 'help' to see commands.")

# ── Main Loop ──────────────────────────────────────────────────────────────
def main():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print("═" * 55)
    print("        🤖  PYTHON AI ASSISTANT  🤖")
    print("═" * 55)
    print("  Voice + Text | Files | Google | Wikipedia")
    print("═" * 55)

    speak("Hello! I am your personal assistant. Say help to see what I can do.")

    while True:
        print("\n" + "─" * 45)
        print("  [1] Type a command")
        print("  [2] Speak a command")
        print("─" * 45)
        choice = input("  Choose (1/2) or type command directly: ").strip()

        if choice == "2":
            command = listen()
            if command:
                process_command(command)
        elif choice == "1":
            command = input("  📝 Enter command: ").strip()
            process_command(command)
        elif choice == "":
            continue
        else:
            # They typed a full command directly
            process_command(choice)

if __name__ == "__main__":
    main()