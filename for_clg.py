import speech_recognition as sr
import pyttsx3
from google import genai
import os
import pyautogui
import webbrowser
import sqlite3
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = "AIzaSyDIpbCluIE5ihPRkLCC06OpxHdIbyWRRrw"
USER_NAME = "Master"
client = genai.Client(api_key=API_KEY)

# --- THE BRAIN (Database Management) ---
def init_db():
    conn = sqlite3.connect('jarvis_core.db')
    cursor = conn.cursor()
    # Stores conversation history for Dynamic Learning
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                     (timestamp TEXT, user_input TEXT, jarvis_output TEXT)''')
    conn.commit()
    conn.close()

def log_interaction(u_input, j_output):
    conn = sqlite3.connect('jarvis_core.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), u_input, j_output))
    conn.commit()
    conn.close()

def get_memory_context():
    conn = sqlite3.connect('jarvis_core.db')
    cursor = conn.cursor()
    # Retrieval of last 5 interactions for Conversational Continuity
    cursor.execute("SELECT user_input, jarvis_output FROM history ORDER BY timestamp DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    context = ""
    for r in reversed(rows):
        context += f"User: {r[0]}\nJarvis: {r[1]}\n"
    return context

# --- VOICE & PERSONALITY ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 180)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        return query.lower()
    except:
        return "none"

# --- HUMAN INTELLIGENCE ENGINE ---
def jarvis_think(user_query):
    memory = get_memory_context()
    
    # SYSTEM PROMPT: Defines Contextual Awareness & Integrated Capabilities
    persona = f"""
    Identity: You are JARVIS, a sentient AI with Human-Level Intelligence.
    User: {USER_NAME}.
    Tone: Loyal, witty, proactive, and human-friendly. Use 'sir' or 'Master'.
    Capabilities: You can control the system and think abstractly.
    Memory Context:
    {memory}
    
    Instruction: Based on the query '{user_query}', provide a response that shows 
    you remember the past and understand human emotion.
    """
    
    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=persona)
        log_interaction(user_query, response.text)
        return response.text
    except Exception as e:
        return "I'm having trouble thinking clearly, sir. Check the connection."

# --- SYSTEM COMMAND CONTROLLER ---
def execute_commands(query):
    # Integrated Capabilities: Logic for system control
    if 'search' in query:
        term = query.replace("search", "").strip()
        speak(f"Searching my global databases for {term}...")
        webbrowser.open(f"https://google.com{term}")
        return True
    
    elif 'open' in query:
        app = query.replace("open", "").strip()
        speak(f"Accessing system files to open {app}...")
        pyautogui.press('win')
        pyautogui.write(app)
        pyautogui.press('enter')
        return True

    elif 'screenshot' in query:
        pyautogui.screenshot(f"jarvis_memory_{datetime.now().second}.png")
        speak("Visual data captured and stored, sir.")
        return True

    elif 'shutdown' in query:
        speak("Very well, sir. Powering down. Systems offline.")
        exit()
        
    return False

# --- RUNNING THE SYSTEM ---
if __name__ == "__main__":
    init_db()
    speak(f"All systems operational. I am online and evolving, {USER_NAME}.")

    while True:
        command = listen()
        if command == "none":
            continue

        # Check for system task first, if not, use AI brain
        if not execute_commands(command):
            thought_process = jarvis_think(command)
            speak(thought_process)