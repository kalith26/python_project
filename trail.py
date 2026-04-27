import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
import webbrowser
import pyautogui
import subprocess as sbc
import datetime

# 1. SETUP: Replace with your actual OpenAI API Key
client = OpenAI(api_key="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")

# Initialize Voice Engine
engine = pyttsx3.init()

voice_active = True

def speak(text):
    print(f"Chatbot: {text}")
    if voice_active:
        engine.say(text)
        engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) # Helps with background noise
        print("Listening... (Say something)")
        try:
            audio = r.listen(source, timeout=5)
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
        "name": "I'm a Python chatbot with voice and AI memory.",
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
        "what can you do": "I can tell the time, open websites, or just chat about anything.",
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

    if "voice off" in user_input:
        voice_active = False
        return simple_responses["voice off"]
    if "voice on" in user_input:
        voice_active = True
        return simple_responses["voice on"]

    # --- 2. WORK PROMPT LOGIC ---
    if "open notepad" in user_input:
        os.system("notepad.exe")
        return simple_responses["open notepad"]
    
    if "open google" in user_input:
        webbrowser.open("https://google.com")
        return simple_responses["open google"]
    
    if "open youtube" in user_input:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube. What would you like to watch?"
        
    elif "open instagram" in user_input:
        webbrowser.open("https://instagram.com")
        return "Opening Instagram. Checking your feed."
        
    elif "open facebook" in user_input:
        webbrowser.open("https://facebook.com")
        return "Opening Facebook."

    elif "open whatsapp" in user_input:
        webbrowser.open("https://whatsapp.com")
        return "Opening WhatsApp Web."

    elif "open github" in user_input:
        webbrowser.open("https://github.com")
        return "Opening GitHub. Happy coding!"

    elif "open email" in user_input or "open gmail" in user_input:
        webbrowser.open("https://mail.google.com")
        return "Opening your inbox."

    # --- 2. OS & SYSTEM CONTROLLING ---
    elif "open notepad" in user_input:
        os.system("notepad.exe")
        return "Notepad is now open."
    elif "close notepad" in user_input:
        os.system("taskkill /f /im notepad.exe")
        return "Closing Notepad."

    elif "open calculator" in user_input:
        os.system("calc.exe")
        return "Opening Calculator."
    elif "close calculator" in user_input:
        os.system("taskkill /f /im CalculatorApp.exe")
        return "Closing Calculator."

    elif "open command prompt" in user_input or "open terminal" in user_input:
        os.system("start cmd")
        return "Opening Command Prompt."

    elif "volume up" in user_input:
        for _ in range(5): pyautogui.press("volumeup")
        return "Increasing volume."

    elif "volume down" in user_input:
        for _ in range(5): pyautogui.press("volumedown")
        return "Decreasing volume."

    elif "mute" in user_input:
        pyautogui.press("volumemute")
        return "Toggling mute."
    elif "unmute" in user_input:
        pyautogui.press("volumeup")
        pyautogui.press("volumedown") # Returns volume to original level but keeps it unmuted
        return "System unmuted."
    
    elif "open settings" in user_input:
        os.open("ms-settings:") # Opens main settings
        return "Opening Windows Settings."
    elif "close settings" in user_input:
        os.system("taskkill /f /im SystemSettings.exe")
        return "Closing Settings."
        
    elif "open file explorer" in user_input or "open documents" in user_input:
        os.startfile(os.path.expanduser("~/Documents")) # Opens Explorer at Documents
        return "Opening File Explorer."
    
#    elif "close file explorer" in user_input:              #****************don't use this code system crashed
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

    elif "close file explorer" in user_input.lower():
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

    elif user_input.lower() in ["battery saver on", "on battery saver", "igries on battery saver"]:
        # This command triggers the Windows Power Saving mode
        cmd = 'powershell -command "Start-Process powershell -ArgumentList \'Set-ExecutionPolicy Bypass -Scope Process -Force; [AppServiceConnection]::new()\' -Verb RunAs"'
        # Simple fallback: opens the Battery Saver settings page directly
        os.system("start ms-settings:batterysaver")
        return "Opening battery saver settings. You can toggle it there."

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
    
    elif "shutdown system" in user_input:
        # speak("Shutting down the computer in 10 seconds.")
        # os.system("shutdown /s /t 10") 
        return "Shutdown command received. (Safety: Line commented out in code)"

    elif "restart system" in user_input:
        os.system("shutdown /r /t 10")
        return "Restarting system."
    
    elif "sleep mode" in user_input:
        # Puts the computer to sleep using rundll32
        speak("Sleep mode is On")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Entering sleep mode."
    elif "" in user_input:
        return "It not update"
        

    # --- 3. DICTIONARY CHECK ---
    
    for key in simple_responses:
        if key in user_input:
            return simple_responses[key]

    # If no keyword matches, use the AI (Conversation Model)
    history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    
    bot_text = response.choices.message.content
    history.append({"role": "assistant", "content": bot_text})
    return bot_text

# 3. MAIN LOOP: Merged Logic
speak("Hi I'm Igries your personal assistant.")

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
#**************************************************  --or--   ********************************************************
# 1. Ask the user for their preferred method
mode = input("Would you like to use 'voice(1)' or 'type(2)'? ").strip().lower()

while True:
    if mode == "1" or mode == "voice":
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
        speak(reply)
