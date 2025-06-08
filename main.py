import subprocess
import datetime
import webbrowser
import pyttsx3
import speech_recognition
import wikipedia
import pyjokes
import google.generativeai as genai

Name = "Ai Assistant" # Enter  the name for this AI Assistant

# genai configuration
API_KEY = "YOUR-API-KEY" # Enter your API KEY here if the api key is not provided it'll search it on google
genai.configure(api_key={API_KEY})
model = genai.GenerativeModel('gemini')
chat = model.start_chat(history=[])

# pyttsx3 Configuration 
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice)


def speak(audio):
    engine.say(audio)
    print(f"{Name}: ",audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak(f"I am your {Name}. How may I help you today?")


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
    return query

def main():
    wishme()
    while True:
        query = take_command().lower()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia", results)

        elif 'search' in query:
            speak("I found this on google")
            query = query.replace("search", "")
            query = query.replace("google", "")
            webbrowser.open("google.com/search?q=" + query)

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
            webbrowser.open("https://duckduckgo.com")

        elif 'open chat gpt' in query:
            speak("opening Chat GPT")
            webbrowser.open("chat.openai.com")

        elif "music" in query or "song" in query:
            webbrowser.open("https://spotify.com/")
            speak("opening spotify")

        elif 'time' in query:
            srtTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {srtTime}")


        elif 'open' in query:
            action = query.replace("open", "").strip()
            
            # Check if trying to open a specific application
            common_apps = {
                "python": "python",
                "cmd": "cmd",
                "command prompt": "cmd",
                "terminal": "cmd"
            }
            
            if action in common_apps:
                # Use command prompt for specific tools that need it
                try:
                    subprocess.Popen(f"start cmd /k {common_apps[action]}", shell=True)
                    speak(f"Opening {action}")
                except Exception as e:
                    speak(f"An error occurred: {e}")
            else:
                # Try to open directly without command prompt
                try:
                    # Use startfile for applications or open the program directly
                    subprocess.Popen(f"start {action}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speak(f"Opening {action}")
                except Exception as e:
                    speak(f"An error occurred: {e}")

        elif "exit" in query:
            speak("Roger that!")
            break

        else:
            if API_KEY != "YOUR-API-KEY":
                instruction = "in short"
                response = str(chat.send_message(query+instruction).text)
                response1 = response.splitlines()
                response2 = "\n".join(response1[:7])
                response3 = response2.replace("*", "")
                speak(response3)
            else:
                speak("I found this on google")
                query = query.replace("search", "")
                query = query.replace("google", "")
                webbrowser.open("google.com/search?q=" + query)


if __name__ == '__main__':
    main()