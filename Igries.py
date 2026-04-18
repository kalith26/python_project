import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import subprocess

LANG_MAP = {
    "english": {"code": "en-IN", "voice_keyword": "Zira"},
    "hindi": {"code": "hi-IN", "voice_keyword": "Hemant"},
    "tamil": {"code": "ta-IN", "voice_keyword": "Valluvar"},
}

current_lang = "english"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('rate', 190)

def set_voice(lang_name):
    """Switch the voice engine to the requested language."""
    global current_lang
    target_keyword = LANG_MAP[lang_name]["voice_keyword"]

    voice_found = False

    for voice in voices:
        if target_keyword.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            current_lang = lang_name
            voice_found = True
            break

    if not voice_found:
        print(f"voice for {lang_name} not found. Using default.")
        return False
    return True

def speak(audio):
    """prints and speaks the text."""

    print(f"Igries ({current_lang}): {audio}")
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    """greats user based on time."""
    hour = int(datetime.datetime.now().hour)
    greeting = "Good Morning!" if hour< 12 else "Good Afternoon!" if hour>18 else "Good Evening!"

    set_voice("english")
    speak(f"{greeting} I am Igries. System online.")

def takeCommand():
    """Listing for audio and converts to text based on current language."""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print(f"Listing ({current_lang})...")
        r.adjust_for_ambient_noise(source, duration= 0.5)
        r.pause_threshold = 1.5
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language= LANG_MAP[current_lang]["code"])
            print(f"User: {query}\n")
        except Exception:
            print("I didn't catch that. please speak again ")
            return "None"
        return query
    
def sendEmail(to, content):
    """Sends email via gmail smtp,"""

    server = smtplib.SMTP('://gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_app_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.closer()

def write_run_code():
    """Allows Igries to write and execute python files."""

    speak("What should I name the file?")
    name = takeCommand().lower().replace(" ","_")
    if name == "none": 
        return
    filename = f"{name}.py"

    speak("Please dictate the code. say 'finish' when done.")
    code_lines = []
    while True:
        line = takeCommand()
        if 'finish' in line.lower() or 'done' in line.lower():
            break
        if line != "None":
            print(f"Writing: {line}")
            code_lines.append(line)

        with open(filename, "w") as f:
            f.write("\n".join(code_lines))
        
        speak(f"saved {filename}. Do you want me to run it?")
        if 'yes' in takeCommand().lower():
            speak("Executing code...")

            try:
                subprocess.run(["python", filename])
            except Exception as e:
                speak("Error executing file.")
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()
#language
        if 'change to tamil' in query or 'tamil mode' in query:
            if set_voice("tamil"):
                speak("மொழி மாற்றப்பட்டது. நான் இப்போது தமிழில் பேசுவேன்.") # Lang changed to Tamil
            else:
                speak("Tamil voice pack is not installed on this Windows system.")

        elif 'change to hindi' in query or 'hindi mode' in query:
            if set_voice("hindi"):
                speak("ठीक है, अब मैं हिंदी में बात करूँगा।") # Okay, I will speak in Hindi
            else:
                speak("Hindi voice pack not found.")

        elif 'english mode' in query or 'switch to english' in query:
            set_voice("english")
            speak("Back to English mode.") 
#tasks
        elif 'wikipedia' in query:
            speak('Searching...')
            query= query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences = 2)
                speak(results)
            except: 
                speak("No result found.")
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"the time is {strTime}")

        elif 'google search' in query:
            speak("What should I search for?")
            term = takeCommand().lower()
            if term != "none":
                webbrowser.open(f"https://google.com{term}")
                speak(f"Searching Google for {term}")

        elif 'open youtuble' in query:
            webbrowser.open("youtube.com")

        elif 'open gmail' in query:
            webbrowser.open("mail.google.com")

        elif 'where is' in query:
            loc = query.replace("Where is", "").strip()
            webbrowser.open(f"https://google.com{loc}")
            speak(f"Location {loc}")

        elif 'write a program' in query or 'create code' in query:
            write_run_code()
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye")
            break
