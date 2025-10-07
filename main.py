import datetime
import webbrowser
import urllib.parse
import pyttsx3
import speech_recognition
import wikipedia
import pyjokes
import os
from google import genai
from google.genai import types

Name = "Voice Assistant" # Enter  the name for this AI Assistant
search_engine = "duckduckgo"

# genai configuration it automatically takes "GEMINI-API-KEY" from environment variables
client = genai.Client()
config = types.GenerateContentConfig(
    system_instruction=f"Your name is {Name} and you are a voice assistant.",
)

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
    speak(f"I am {Name}. How may I help you today? You can speak *exit* anytime for me to stop listening")

# Get current date
def get_current_date():
    now = datetime.datetime.now()
    date_string = now.strftime("%B %d, %Y")
    day_name = now.strftime("%A")
    return (f"Today is {day_name}, {date_string}")

# Converts Speech to Text
def take_command():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        speak("Listening")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)
    try:
        speak("Recognising")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
    except Exception:
        return None
    return query.lower()

# Actions based on the query
def actions():
    while True:
        query = take_command().lower()
        # Logic for executing tasks based on query
        # Wikipedia search
        if not query:
            continue
        # Wikipedia search
        elif 'wikipedia' in query:
            try:
                speak('Searching Wikipedia')
                query = query.replace("wikipedia", "").strip()
                if query:
                    results = wikipedia.summary(query, sentences=2)
                    speak(f"According to Wikipedia: {results}")
                else:
                    speak("Please specify what you want to search on Wikipedia")
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Multiple results found. Please be more specific. Options include: {', '.join(e.options[:3])}")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any information on that topic")
            except Exception as e:
                speak("Sorry, there was an error searching Wikipedia")

        # Search on preffered search_engine
        elif 'search' in query:
            speak(f"I found this on {search_engine}")
            query = query.replace("search", "").replace(search_engine, "").strip()
            if query:
                webbrowser.open(f"https://{search_engine}.com/search?q=" + urllib.parse.quote_plus(query))
            else:
                speak("Please specify what you want to search for")

        # Open ChatGPT
        elif 'open chat gpt' in query or 'open chatgpt' in query:
            speak("Opening Chat GPT")
            webbrowser.open("https://chat.openai.com")

        # Tell a joke
        elif 'joke' in query:
            try:
                joke = pyjokes.get_joke(language='en', category='neutral')
                speak(joke)
            except Exception:
                speak("Sorry, I couldn't fetch a joke right now")

        # Open YouTube (with rick roll easter egg)
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # Open Google
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        # Open default browser
        elif 'open browser' in query:
            speak("Opening browser")
            webbrowser.open(f"https://{search_engine}.com")

        # Play music/songs
        elif query.startswith("play"):
            query = query.replace("play", "").replace("song", "").replace("music", "").strip()
            if query:
                webbrowser.open("https://music.youtube.com/search?q=" + urllib.parse.quote_plus(query))
                speak(f"results for {query} on YouTube Music")
            else:
                webbrowser.open("https://music.youtube.com")
                speak("Opening YouTube Music")

        # Get current time
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # Get current date
        elif 'date' in query or 'today' in query:
            speak(get_current_date())

        # Exit commands
        elif "exit" in query or "stop listening" in query or "goodbye" in query:
            speak("Roger that! Goodbye!")
            break

        # Handle unrecognized input
        elif "none" in query:
            speak("I couldn't understand that, Please repeat")

        # AI-powered responses using Gemini
        else:
            try:
                instruction = "Please provide a brief and helpful response."
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    config=config,
                    contents=query + instruction
                )
                if response and response.text:
                    # Clean up response text
                    cleaned_response = response.text.replace("*", "").replace("#", "").strip()
                    # Limit response length for speech
                    if len(cleaned_response) > 300:
                        cleaned_response = cleaned_response[:300] + "..."
                    speak(cleaned_response)
                else:
                    speak("I'm sorry, I couldn't generate a response for that")
            except Exception as e:
                speak("Sorry, I'm having trouble connecting to my AI service right now")
                print(f"Gemini API error: {e}")

def main():
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("Warning: GEMINI_API_KEY environment variable not found!")
        print("Please set your Gemini API key as GEMINI_API_KEY environment variable.")
        return
    try:
        wishme()
        actions()
    except KeyboardInterrupt:
        speak("Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("An unexpected error occurred. Shutting down.")

if __name__ == '__main__':
    main()