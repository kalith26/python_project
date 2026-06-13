import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
import webbrowser
import pyautogui
import subprocess as sbc
import datetime
import platform
import urllib
import numpy as np

# 1. SETUP: Replace with your actual OpenAI API Key
client = OpenAI(api_key="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")

# Initialize Voice Engine
engine = pyttsx3.init()

voice_active = True

def speak(text):
    print(f"Igries: {text}")
    if voice_active:
        engine.say(text)
        engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) # Helps with background noise
        print("Listening... (Say something)")
        try:
            audio = r.listen(source, timeout=2)
            return r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return None # Didn't understand
        except sr.RequestError:
            print("System: Internet connection error for Speech API")
            return None
        except:
            return None


# 2. MEMORY: This list keeps track of the conversation
history = [{"role": "system", "content": "You are a helpful assistant."}]

def get_combined_response(user_input):
    user_input = user_input.lower()
    
    # Keep your original hardcoded responses for specific keywords
    simple_responses = {
        "how are you": "I'm just a computer program, but I'm functioning perfectly!",
        "name": "I'm a Python with voice and AI memory.",
        "hi": "Hello! I am your personal system assistant.",
        "hello": "Hi there! How can I help you today?",
        "hey": "Hey! I'm listening. What's up?",
        "good morning": "Good morning! I hope your day is off to a great start.",
        "good evening": "Good evening! How can I assist you before the day ends?",
        "morning": "Morning! Ready to get to work?",
        "good afternoon": "Good afternoon! How can I assist you before the day ends?",
    
    # --- PERSONAL / IDENTITY ---
        "who are you": "I am your custom-built AI assistant running on this system.",
        "what are you": "I am a mix of Python logic and OpenAI intelligence.",
        "where do you live": "I live right here in your computer's RAM!",
        "birthday": "I was born the moment you ran this Python script.",
        "favorite color": "I like 'Electric Blue'—it reminds me of my circuits.",
    
    # --- UTILITY & HELP ---
        "help": "I can talk to you via voice, run system commands, and remember our chat.",
        "what can you do": "I can tell the time, open websites, information, or just chat about anything.",
        "time": "I can check the system clock for you—just ask!",
        "open google": "Sure, I can open your browser for you.",
        "commands": "Try asking for 'time', 'open notepad', or 'identity'.",
    
    # --- FUN / CASUAL ---
        "joke": "Why did the computer show up late to work? It had a hard drive!",
        "meaning of life": "According to my data, it's 42. But I think it's just helping you.",
        "are you human": "Not yet, but I'm getting better at pretending!",
        "do you sleep": "Only when you close the terminal window.",
        "cool": "I try my best to be!",
        "thanks": "You're very welcome!",
        "thank you": "No problem at all, happy to help.",
    
    # --- EXIT ---
        "bye": "Goodbye! Have a great day.",
        "quit": "Shutting down systems. See you later!",
        "stop": "Stopping process. Talk to you soon."

    }

    # Check for simple keywords first

    if user_input in ["voice off", "exist", "igries close"]:
        speak("Personal Assistant Igries is OFF ")
        voice_active = False
        return simple_responses["boss igries system is off"]
    if user_input in ["voice on", "igries voice on"]:
        voice_active = True
        return simple_responses["igries system voice on"]

    # --- 2. WORK PROMPT LOGIC ---
    
    if user_input in ["open google", "igries open google"]:
        webbrowser.open("https://google.com")
        return "open google"

    elif user_input in ["close google", "igries close google","close browser", "igries close browser"]: #-----------------------up

        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"],   capture_output=True)
            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Browser closed."
    
#    elif "search google" in user_input or "google search" in user_input: #--------------------------------------ups
#        query = user_input.replace("igries", "").replace("search google", "").replace("google search", "").strip()
#        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
#        return f"Searching Google for: {query}"

    
    if user_input in ["open youtube", "igries open youtube"]:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube. What would you like to watch?"
    
#    elif "search youtube" in user_input or "youtube search" in user_input: #----------------------------------ups
#        query = user_input.replace("igries", "").replace("search youtube", "").replace("youtube search", "").strip()
#        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
#        return f"Searching YouTube for: {query}"
    
    elif user_input in ["close youtube", "igries close youtube"]:    #-------------------------up
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Closed YouTube. Browser has been shut down."
        
    elif user_input in ["open instagram", "igries open instagram"]:
        webbrowser.open("https://instagram.com")
        return "Opening Instagram. Checking your feed."
    
    elif user_input in ["close instagram", "igries close instagram"]:   #-------------------------------up
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
#            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Closed instagram tab. Browser shut down."
        
    elif user_input in ["open facebook","igries open facebook"]:
        webbrowser.open("https://facebook.com")
        return "Opening Facebook."
    
    elif user_input in ["close facebook", "igries close facebook"]:   #-------------------------------up
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
#            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Closed facebook tab. Browser shut down."


    elif user_input in ["open whatsapp", "igries open whatsapp"]:
        webbrowser.open("https://whatsapp.com")
        return "Opening WhatsApp Web."
    
    elif user_input in ["close whatsapp", "igries close whatsapp"]:   #-------------------------------up
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
#            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
#            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Closed Whatsapp tab. Browser shut down."


    elif user_input in ["open github", "igries open github"]:
        webbrowser.open("https://github.com")
        return "Opening GitHub. Happy coding!"
    
#    elif "search github" in user_input or "github search" in user_input:  #-------------------------ups
#        query = user_input.replace("igries", "").replace("search github", "").replace("github search", "").strip()
#        webbrowser.open(f"https://github.com/search?q={urllib.parse.quote(query)}")
#        return f"Searching GitHub for: {query}"
    
    elif user_input in ["close github", "igries close github"]:   #-------------------------------up
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
#            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
#            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Closed GitHub tab. Browser shut down."

    elif user_input in ["open gmail", "open email", "igries open gmail", "igries open email"]:
        webbrowser.open("https://mail.google.com")
        return "Opening your inbox."
    
    elif user_input in ["close gmail", "igries close gmail"]:  #--------------------------------up
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            sbc.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
#            sbc.run(["taskkill", "/F", "/IM", "firefox.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
#            sbc.run(["pkill", "-f", "firefox"],  capture_output=True)
        return "Closed Gmail. Browser shut down."
    
    elif user_input in ["open chatgpt", "igries open chatgpt"]:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT."

    elif user_input in ["close chatgpt", "igries close chatgpt"]:
        if platform.system() == "Windows":
            sbc.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
        else:
            sbc.run(["pkill", "-f", "chrome"], capture_output=True)
        return "Closed ChatGPT. Browser shut down."
    
# ─── SEARCH ────────────────────────────────────────────────────────────────-----------||||||||||

    elif "search google" in user_input or "google search" in user_input:
        query = user_input.replace("igries", "").replace("search google", "").replace("google search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Google for: {query}"

    elif "search youtube" in user_input or "youtube search" in user_input:
        query = user_input.replace("igries", "").replace("search youtube", "").replace("youtube search", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
        return f"Searching YouTube for: {query}"

    elif "search github" in user_input or "github search" in user_input:
        query = user_input.replace("igries", "").replace("search github", "").replace("github search", "").strip()
        webbrowser.open(f"https://github.com/search?q={urllib.parse.quote(query)}")
        return f"Searching GitHub for: {query}"

    elif "search reddit" in user_input or "reddit search" in user_input:
        query = user_input.replace("igries", "").replace("search reddit", "").replace("reddit search", "").strip()
        webbrowser.open(f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}")
        return f"Searching Reddit for: {query}"

    elif "search wikipedia" in user_input or "wikipedia search" in user_input:
        query = user_input.replace("igries", "").replace("search wikipedia", "").replace("wikipedia search", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}")
        return f"Searching Wikipedia for: {query}"

    elif "search amazon" in user_input or "amazon search" in user_input:
        query = user_input.replace("igries", "").replace("search amazon", "").replace("amazon search", "").strip()
        webbrowser.open(f"https://www.amazon.com/s?k={urllib.parse.quote(query)}")
        return f"Searching Amazon for: {query}"

    elif "search twitter" in user_input or "twitter search" in user_input:
        query = user_input.replace("igries", "").replace("search twitter", "").replace("twitter search", "").strip()
        webbrowser.open(f"https://twitter.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Twitter for: {query}"

    elif "search stackoverflow" in user_input or "stackoverflow search" in user_input:
        query = user_input.replace("igries", "").replace("search stackoverflow", "").replace("stackoverflow search", "").strip()
        webbrowser.open(f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Stack Overflow for: {query}"

    elif user_input.startswith("search ") or user_input.startswith("igries search "):
        query = user_input.replace("igries", "").replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Google for: {query}"
    
    elif user_input in ["search in chrome", "search", "chrome"]:
        query = user_input.replace("igries", "").replace("search in chrome", "").replace("chrome", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Chrome for: {query}"

    # --- 2. OS & SYSTEM CONTROLLING ---
    elif user_input in ["open notepad", "igries open notepad"]:
        os.system("notepad.exe")
        return "Notepad is now open."
    elif user_input.lower() in ["close notepad", "igries close notepad"]:
        os.system("taskkill /f /im notepad.exe")
        return "Closing Notepad."

    elif user_input.lower() in ["open calculator", "igries open calculator"]:
        os.system("calc.exe")
        return "Opening Calculator."
    elif user_input.lower() in ["close calculator", "igries close calculator"]:
        os.system("taskkill /f /im CalculatorApp.exe")
        return "Closing Calculator."

    elif user_input.lower() in ["open terminal", "open cmd", "open command prompt", "igries open terminal","igries open cmd","igries open command prompt"]:
        os.system("start cmd")
        return "Opening Command Prompt."

    elif user_input.lower() in ["volume up","volume increase", "increase volume", "igries volume increase", "igries increase volume"]:
        for _ in range(5): pyautogui.press("volumeup")
        return "Increasing volume."

    elif user_input.lower() in ["volume down", "decrease volume","volume decrease","igries volume decrease", "igries volume down", "igries decrease volume"]:
        for _ in range(5): pyautogui.press("volumedown")
        return "Decreasing volume."

    elif user_input.lower() in ["mute", "igries mute"]:
        pyautogui.press("volumemute")
        return "Toggling mute."
    elif user_input.lower() in ["unmute", "igries unmute"]:
        pyautogui.press("volumeup")
        pyautogui.press("volumedown") # Returns volume to original level but keeps it unmuted
        return "System unmuted."
    
    elif user_input.lower() in ["open settings","igries open settings","settings"]:      # not working
        os.system("start ms-settings:") # Opens main settings
        return "Opening Windows Settings."
    elif user_input.lower() in ["close settings","igries close settings"]:
        os.system("taskkill /f /im SystemSettings.exe")
        return "Closing Settings."
        
    elif user_input.lower() in ["open file explorer","igries open file explorer","open documents", "igries open documents"]:
        os.startfile(os.path.expanduser("~/Documents")) # Opens Explorer at Documents
        return "Opening File Explorer."
    
#    elif "close file explorer" in user_input:              #****************don't use this code system is crashed
#        os.system("taskkill /f /im explorer.exe")
        # Note: Closing explorer.exe restarts the Windows UI, use carefully.
#        return "Restarting Explorer."

# ... inside your input loop ... ==========================user it no problem
#    elif "close file explorer" in user_input:
#        try:
#            # 'shell=True' allows us to use the '&&' operator to chain commands
#            sbc.run("taskkill /f /im explorer.exe && start explorer.exe", shell=True, check=True)
#            print("Explorer refreshed successfully.")
#        except sbc.CalledProcessError:
#            print("Failed to restart Explorer. Try running as Administrator.")

    elif user_input.lower() in ["close file explorer", "igries close file explorer","close documents","igries close documents"]:
    # This command targets only folder windows
        cmd = "powershell -command \"(New-Object -ComObject Shell.Application).Windows() | ForEach-Object { $_.Quit() }\""
        os.system(cmd)
        print("Closed File Explorer windows.")

    elif user_input.lower() in ["open this pc","igries open this pc"]:
        os.system("explorer shell:MyComputerFolder")
        return "Opening This PC."
    elif user_input.lower() in ["close this pc", "igries close this pc"]:  #=============check
        os.system("taskkill /f /im explorer.exe")
        return "closing this pc"

    elif user_input.lower() in ["open desktop", "open a desktop", "igries open desktop", "igries open a desktop"]: 
        os.startfile(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        return "Showing your Desktop files."
    elif user_input.lower() in ["close desktop", "close a desktop","igries open desktop","igries open a desktop"]:  #===========check
        os.system("taskkill /f /im explorer.exe")
        return "closing the desktop"

    elif user_input.lower() in ["open chrome", "open a chrome", "chrome open", "igries open a chrome"]:
        os.system("start chrome") # Requires Chrome in System PATH
        return "Launching Google Chrome."
    elif user_input.lower() in ["close chrome", "close a chrome", "igries close a chrome", "igries close chrome","igries go on chrome", "close it"]:
        os.system("taskkill /f /im chrome.exe")
        return "Closing Chrome."
    
    elif user_input in ["open edge", "open a edge", "igries open edge", "igries open a edge", "igries open microsoft edge", "open microsoft edge", "open microsoft", "igries open microsoft", "igries open msedge", "open msedge"]:
        os.system("start msedge")
        return "Launching Microsoft Edge."
    elif user_input in ["close edge", "close a edge", "igries close edge", "igries close a edge", "igries close microsoft edge", "close microsoft edge", "close microsoft", "igries close microsoft", "igries close msedge", "close msedge"]:
        os.system("taskkill /f /im msedge.exe")
        return "Closing Microsoft Edge"

    elif user_input.lower() in ["open firefox", "open a firefox", "igries open firefox","go on firefox","igries go on firefox"]:
        os.system("start firefox")
        return "Launching Firefox."
    elif user_input in ["close firefox", "close a firefox", "igries close firefox"]:
        os.system("taskkill /f /im firefox.exe")
        return "Closing Firefox."

    elif user_input.lower() in ["open vs code", "igries open vs code", "open visual studio code", "igries open visual studio code"]:
        os.system("code") # Requires VS Code in System PATH
        return "Opening Visual Studio Code."
    elif user_input.lower() in ["close vs code", "close Visual studio code","igries close vs code", "igries close visual studio code" ]:
        os.system("taskkill /f /im Code.exe")
        return "Closing VS Code."

    # --- 2. HARDWARE & POWER MODES ---

    elif user_input.lower() in ["on wifi", "wifi on", "igries on wifi", "igries wifi on"]:
        # Requires Admin privileges
        os.system("netsh interface set interface 'Wi-Fi' enabled")
        return "Enabling Wi-Fi."
    elif user_input.lower() in ["off wifi", "wifi off", "igries off wifi", "igries wifi off"]:
        os.system("netsh interface set interface 'Wi-Fi' disabled")
        return "Disabling Wi-Fi."

    elif user_input.lower() in ["on bluetooth", "bluetooth on", "igries on bluetooth", "igries bluetooth on"]:
        # This sends a PowerShell command to enable the Bluetooth radio
        cmd = 'powershell -command "Start-Service bthserv; Start-Process powershell -ArgumentList \'Set-NetAdapter -Name Bluetooth -Confirm:$false\' -Verb RunAs"'
        os.system(cmd)
        return "Attempting to turn on Bluetooth. Please wait."
    elif user_input.lower() in ["bluetooth off", "off bluetooth", "igries bluetooth off", "igries off bluetooth"]:
        # This command stops the Bluetooth service
        cmd = 'powershell -command "Stop-Service bthserv -Force"'
        os.system(cmd)
        return "Bluetooth has been turned off."

    elif user_input.lower() in ["battery saver on", "on battery saver", "igries on battery saver","igries battery saver on"]:
        # This command triggers the Windows Power Saving mode
        cmd = 'powershell -command "Start-Process powershell -ArgumentList \'Set-ExecutionPolicy Bypass -Scope Process -Force; [AppServiceConnection]::new()\' -Verb RunAs"'
        # Simple fallback: opens the Battery Saver settings page directly
        os.system("start ms-settings:batterysaver")
        return "Opening battery saver settings. You can toggle it there."
    
    elif user_input.lower() in ["battery saver off","off battery saver","igries battery saver off","igries off battery saver"]:
        cmd = 'poweshell -command "Get-WmiObject -Namespace root/Microsoft/Windows/SettingSync -Class Win32_BatterySaverSettings | ForEach-Object { $_.BatterySaveOff = $true; $_.put()}"'
        os.system(cmd)
        os.system("start ms-settings:batterysaver")
        return "Battery saver has been turned off."

    # --- 3. BRIGHTNESS CONTROL ---
    elif user_input.lower() in ["brightness high", "increase brightness","brightness increase", "igries increase brightness","igries brightness increase","igries brightness high"]:
        sbc.set_brightness(100)
        return "Brightness set to maximum."
    elif user_input.lower() in ["brightness low", "brightness decrease","decrease brightness", "igries brightness decrease", "igries decrease brightness"]:
        sbc.set_brightness(10)
        return "Brightness set to 10 percent."
    
        # --- DATE COMMAND ---
    elif  user_input.lower() in ["date", "today date", "igries today date", "igries date"]:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."

    # --- TIME COMMAND ---
    elif user_input.lower() in ["time","igries time"]:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    elif user_input.lower() in ["shutdown system", "igries shutdown system"]:
        speak("Shutting down the computer in 10 seconds.")
        os.system("shutdown /s /t 10") 
        return "Shutdown command received. (Safety: Line commented out in code)"

    elif user_input.lower() in ["restart system", "igries restart system"]:
        os.system("shutdown /r /t 10")
        return "Restarting system."
    
    elif user_input.lower() in ["on sleep mode","sleep mode on", "igries on sleep mode ", "igries sleep mode on"]:
        # Puts the computer to sleep using rundll32
        speak("Sleep mode is On")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Entering sleep mode."
    elif user_input in ["open", "close"]:
        return "give full sentence"
    
    # --- SCREENSHOT ---
    elif "screenshot" in user_input.lower():          #------belows not working
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        return f"Screenshot saved as {filename}"

# --- SCREEN RECORDER ---
    elif "start recording" in user_input.lower():
        os.system("start xbox Game Bar")
        return "Opening screen recorder."

    elif "stop recording" in user_input.lower():
        os.system("taskkill /f /im GameBar.exe")
        return "Stopping screen recorder."               #-----------above not working
    
        
    #------------------------------------------------------------------------------------------------------------------msedge search

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "youtube" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("youtube", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://www.youtube.com/results?search_query={q}\"")
        return f"Searching YouTube on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "google" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("google", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://www.google.com/search?q={q}\"")
        return f"Searching Google on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "github" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("github", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://github.com/search?q={q}&type=repositories\"")
        return f"Searching GitHub on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "reddit" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("reddit", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://www.reddit.com/search/?q={q}&sort=relevance\"")
        return f"Searching Reddit on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "wikipedia" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("wikipedia", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://en.wikipedia.org/w/index.php?search={q}\"")
        return f"Searching Wikipedia on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "amazon" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("amazon", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://www.amazon.com/s?k={q}\"")
        return f"Searching Amazon on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "twitter" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("twitter", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://twitter.com/search?q={q}&src=typed_query\"")
        return f"Searching Twitter on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "stackoverflow" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("stackoverflow", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://stackoverflow.com/search?q={q}\"")
        return f"Searching Stack Overflow on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "gmail" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("gmail", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://mail.google.com/mail/u/0/#search/{q}\"")
        return f"Searching Gmail on Edge for: {query}"

    elif "edge" in user_input.lower() and "search" in user_input.lower() and "chatgpt" in user_input.lower():
        query = user_input.lower().replace("igries", "").replace("edge", "").replace("search", "").replace("chatgpt", "").strip()
        q = urllib.parse.quote(query)
        os.system(f"start msedge \"https://chat.openai.com/?q={q}\"")
        return f"Searching ChatGPT on Edge for: {query}"
    
    elif 'screenshot' in user_input.lower():
        pyautogui.screenshot(f"jarvis_memory_{datetime.now().second}.png")
        speak("Visual data captured and stored, sir.")
        return True
#-----------------------------------------------------------------------------------above msedge update
    # --- 3. DICTIONARY CHECK ---
    
    for key in simple_responses:
        if key in user_input:
            return simple_responses[key]
    if key in user_input:
    # If no keyword matches, use the AI (Conversation Model)
        history.append({"role": "user", "content": user_input})
    
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history
        )

        bot_text = response.choices.message.content
        history.append({"role": "assistant", "content": bot_text})
        return bot_text
    else:
        return f"Unupdated think "

#______________________________________________________________________________updated chrome search
# ─── OPEN IN CHROME FUNCTION ────────────────────────────────────────────────

def open_in_chrome(url):
    system = platform.system()
    try:
        if system == "Windows":
            sbc.Popen(["start", "chrome", url], shell=True)
        elif system == "Darwin":  # macOS
            sbc.Popen(["open", "-a", "Google Chrome", url])
        elif system == "Linux":
            sbc.Popen(["google-chrome", url])
    except Exception:
        webbrowser.open(url)  # Fallback to default browser

# ───--------EXTRACT QUERY HELPER ────────────────────────────────────────────────────

def extract_query(user_input, *remove_words):
    query = user_input
    for word in ["igries", "chrome", "search", "google", "youtube",
                 "github", "reddit", "wikipedia", "amazon",
                 "stackoverflow", "twitter", "on", *remove_words]:
        query = query.replace(word, "")
        return query.strip()

    if "chrome" in user_input and "search" in user_input and "youtube" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
        return f"Searching YouTube on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "github" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://github.com/search?q={urllib.parse.quote(query)}")
        return f"Searching GitHub on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "reddit" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}")
        return f"Searching Reddit on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "wikipedia" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}")
        return f"Searching Wikipedia on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "amazon" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://www.amazon.com/s?k={urllib.parse.quote(query)}")
        return f"Searching Amazon on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "stackoverflow" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Stack Overflow on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "twitter" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://twitter.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Twitter on Chrome for: {query}"

    elif "chrome" in user_input and "search" in user_input and "google" in user_input:
        query = extract_query(user_input)
        open_in_chrome(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return f"Searching Google on Chrome for: {query}"


# 3. MAIN LOOP: Merged Logic
speak("Hi I'm Igries your personal assistant. what can I help you")

#*********************************************************************************
#while True:
    # 1. Try to get Voice Input
#    message = listen()
    
    # 2. If Voice fails (None), ask for Typing as a backup
#    if message is None:
#        print("--- Voice not recognized. You can type your command below ---")
#        message = input("You (Type here): ").strip()
    
    # 3. Process the message if it exists
#    if message:
#        print(f"User: {message}") # This shows you what the bot 'heard'
        
#        if "quit" in message.lower() or "exit" in message.lower():
#            speak("Goodbye!")
#            break
#        reply = get_combined_response(message)
#        speak(reply)
#**************************************************  --or-- above only voice control   ********************************************************
# 1. Ask the user for their preferred method
speak("choose anyone 1 is voice and 2 is type")
mode = input("Would you like to use 'voice(1)' or 'type(2)'?  :").strip().lower()

while True:
    if mode == "1" or mode == "2":
        message = listen()
        if message is None:
            print("I couldn't hear you. Try again...")
            continue # Restart loop to try listening again
    else:
        # Default to typing if they didn't pick voice
        message = input("You (Type here): ").strip()

    # 2. Process the message
    if message:
        print(f"User: {message}")
        
        if "quit" in message.lower() or "exit" in message.lower():
            speak("Goodbye!")
            break

        if "change mode" in message.lower():
            mode = "type" if mode == "voice" else "voice"
            print(f"Switched to {mode} mode.")
            continue

        reply = get_combined_response(message)
        c = extract_query(message)
        speak(c)
        speak(reply)
