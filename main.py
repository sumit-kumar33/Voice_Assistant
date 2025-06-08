import subprocess
import datetime
import webbrowser
import pyttsx3
import speech_recognition
import wikipedia
import pyjokes
import google.generativeai as genai

Name = "Voice Assistant" # Enter  the name for this AI Assistant
search_engine = "duckduckgo"
# genai configuration
# Enter your API KEY here if the api key if not then leave as is it'll search it on google
API_KEY = "YOUR-API-KEY"
genai.configure(api_key={API_KEY})
model = genai.GenerativeModel('gemini')
chat = model.start_chat(history=[])

# pyttsx3 Configuration 
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice)

# Converts text to speech
def speak(audio):
    engine.say(audio)
    print(f"{Name}: ",audio)
    engine.runAndWait()

# Wishes Good Morning, Afternoon, Evening according to time
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak(f"I am your {Name}. How may I help you today?")

# Converts Speech to Text
def take_command():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        speak("Listening")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        speak("Recognising")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        return "None"
    return query.lower()

# Actions based on the query
def actions():
    while True:
        query = take_command()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia", results)

        elif 'search' in query:
            speak(f"I found this on {search_engine}")
            query = query.replace("search", "")
            query = query.replace(search_engine, "")
            webbrowser.open(f"{search_engine}.com/search?q=" + query)

        elif 'open chat gpt' in query:
            speak("opening Chat GPT")
            webbrowser.open("chat.openai.com")

        elif 'joke' in query:
            jokes = pyjokes.get_joke(language='en', category='neutral')
            speak(jokes)

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("bit.ly/rickoll")
            speak("I am sorry for this. But my creator want me to rick roll you.")

        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")

        elif 'open browser' in query:
            speak("opening browser")
            webbrowser.open(f"https://{search_engine}.com")

        elif 'open chat gpt' in query:
            speak("opening Chat GPT")
            webbrowser.open("chat.openai.com")

        elif "music" in query or "song" in query:
            webbrowser.open("https://spotify.com/")
            speak("opening spotify")

        elif 'time' in query:
            srtTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {srtTime}")

        # opens a program with startfile and cmd as reqired
        elif 'open' in query:
            app_name = query.replace("open", "").strip()
            common_apps = ["python", "cmd", "command prompt", "py", "pi"]
            if app_name in common_apps:
                try:
                    subprocess.Popen(f"start cmd /k {app_name}", shell=True)
                    speak(f"Opening {app_name}")
                except Exception as e:
                    speak(f"An error occurred: {e}")
            else:
                try:
                    subprocess.Popen(f"start {app_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speak(f"Opening {app_name}")
                except Exception as e:
                    speak(f"An error occurred: {e}")

        elif "exit" in query:
            speak("Roger that!")
            break

        elif query=="none":
            speak("I couldn't understand that, Please repeat")

        else:
            if API_KEY != "YOUR-API-KEY":
                instruction = "in short"
                response = str(chat.send_message(query+instruction).text)
                response1 = response.splitlines()
                response2 = "\n".join(response1[:7])
                response3 = response2.replace("*", "")
                speak(response3)
                break
            else:
                speak(f"I found this on {search_engine}")
                query = query.replace("search", "")
                query = query.replace(search_engine, "")
                webbrowser.open(f"{search_engine}.com/search?q=" + query)
                break

def main():
    wishme()
    actions()

if __name__ == '__main__':
    main()