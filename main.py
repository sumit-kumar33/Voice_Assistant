import datetime
import webbrowser
import urllib.parse
import pyttsx3
import speech_recognition
import wikipedia
import pyjokes
import os
import logging
from google import genai
from google.genai import types

Name = "Voice Assistant" # Enter  the name for this AI Assistant
search_engine = "duckduckgo" # Enter your preferred search engine here (e.g., google, duckduckgo, bing)

# Logs Configuration
logging.basicConfig(
    level=logging.INFO,
    filename=f"{Name}.log",
    format='%(asctime)s %(levelname)s: %(message)s'
    )

messages: logging.Logger = logging.getLogger(__name__)

handler = logging.FileHandler(f"{Name} messages.log")
formatter = logging.Formatter("%(asctime)s: %(message)s")
console_handler = logging.StreamHandler()

handler.setFormatter(formatter)
messages.addHandler(handler)
messages.addHandler(console_handler)

# Gemini API call function
def gemini(query: str)  -> str:
    # genai configuration it automatically takes "GEMINI-API-KEY" from environment variables
    client = genai.Client()
    config = types.GenerateContentConfig(
        system_instruction=f"Your name is {Name} and you are a voice assistant. Try to keep responses within 300 characters.",
    )
    try:
        instruction = "Please provide a brief and helpful response."
        response: types.GenerateContentResponse = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            config=config,
            contents=query + instruction
        )
        if response and response.text:
            # Clean up response text
            cleaned_response: str = response.text.replace("*", "").replace("#", "").strip()
            return cleaned_response
        else:
            return "I'm sorry, I couldn't generate a response for that"
    except Exception as e:
        logging.exception(f"Gemini API error: {e}")
        return "Sorry, I'm having trouble connecting to google"

# pyttsx3 Configuration 
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
try:
    if voices:
        # set to first available voice id (safe)
       engine.setProperty('voice', voices[0].id)
except Exception as e:
    logging.exception("Failed to set TTS voice property")

# Converts text to speech
def speak(audio) -> None:
    messages.info(f"{Name}: {audio}")
    engine.say(audio)
    engine.runAndWait()

# Wishes Good Morning, Afternoon, Evening according to time
def wishme() -> str:
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        salutation = "Good Morning!"
    elif 12 <= hour < 18:
        salutation = "Good Afternoon!"
    else:
        salutation = "Good Evening!"
    return f"{salutation}\n I am {Name}. How may I help you today? You can speak *exit* anytime for me to stop listening"

# Get current date
def get_current_date() -> str:
    now: datetime.datetime = datetime.datetime.now()
    date_string: str = now.strftime("%B %d, %Y")
    day_name: str = now.strftime("%A")
    return (f"Today is {day_name}, {date_string}")

# Converts Speech to Text
def take_command() -> str | None:
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        speak("Listening")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        speak("Recognising")
        query = r.recognize_google(audio, language='en-in')  # type: ignore
    except Exception as e:
        logging.exception(f"Failed to run take_command() function : {e}")
        messages.info(f"You: None")
        return None
    messages.info(f"You: {query.lower()}")
    return query.lower()

# Actions based on the query
def actions() -> None:
    while True:
        query: str | None = take_command()

        # Check if query is None
        if not query:
            speak("I couldn't understand that, Please repeat")
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
                joke: str = pyjokes.get_joke(language='en', category='neutral')
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
            current_time: str = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # Get current date
        elif 'date' in query or 'today' in query:
            speak(get_current_date())

        # Exit commands
        elif "exit" in query or "stop listening" in query or "goodbye" in query:
            speak("Roger that! Goodbye!")
            break

        # AI-powered responses using Gemini
        else:
            # Check if API key is set
            if os.getenv('GEMINI_API_KEY'):
                speak(gemini(query))
            else:
                speak(f"I found this on {search_engine}")
                query = query.replace("search", "").replace(search_engine, "").strip()
                webbrowser.open(f"https://{search_engine}.com/search?q=" + urllib.parse.quote_plus(query))
                logging.warning("Warning: GEMINI_API_KEY environment variable not found!")
                logging.info("Please set your GEMINI_API_KEY environment variable. Otherwise you won't get AI responses.")
                

def main() -> None:
    logging.info("=" * 50)
    logging.info(f"{Name} is starting")
    logging.info("=" * 50)

    messages.info("=" * 50)
    messages.info(f"{Name} is starting")
    messages.info("=" * 50)
    try:
        speak(wishme())
        actions()
    except KeyboardInterrupt:
        speak("Goodbye!")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        speak("An unexpected error occurred. Shutting down.")

if __name__ == '__main__':
    main()