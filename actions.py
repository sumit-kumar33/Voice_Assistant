from config_files.config import *
from config_files.logs_config import *
from speech.speak import speak
from speech.take_command import take_command
from features.get_current_date import get_current_date
from features.gemini import gemini
from features.search import search
from features.wikipedia_search import wikipedia_search
import webbrowser
import os
import pyjokes
import urllib.parse
import datetime

#TODO: Refactor this function and make a dictionary mapping commands to functions for better scalability

def get_text_command():
    try:
        return input("Type your command: ").strip().lower()
    except EOFError:
        return None

def actions():
    use_voice = True
    try:
        if use_voice:
            query = take_command()
            if not query:
                return "I couldn't understand that, Please repeat or press Ctrl+C to type."
        else:
            try:
                query = get_text_command()
                if query == "voice":
                    use_voice = True
                    return "Switching to voice mode. You can speak your command now. Press Ctrl+C to return to typing mode."
                elif not query:
                    return "No input received. Please try again."
            except KeyboardInterrupt:
                query = "exit"
    except KeyboardInterrupt:
        use_voice = False
        return "Switching to typing mode. Please type your command below. Type 'voice' to switch back to voice mode. Type 'exit' to quit."
    if not query:
        return "I couldn't understand that, Please repeat"
    # Wikipedia search
    elif 'wikipedia' in query:
        return wikipedia_search(query)
    # Search on preffered search_engine
    elif 'search' in query:
        return search(query)
    # Open ChatGPT
    elif 'open chat gpt' in query or 'open chatgpt' in query:
        webbrowser.open("https://chat.openai.com")
        return "Opening Chat GPT"
    # Tell a joke
    elif 'joke' in query:
            joke = pyjokes.get_joke(language='en', category='neutral')
            return joke
    # Open YouTube
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"
    # Open Google
    elif 'open google' in query:
        webbrowser.open("https://google.com")
        return "Opening Google"
    # Open default browser
    elif 'open browser' in query:
        webbrowser.open(f"https://{search_engine}.com")
        return "Opening browser"
    # Play music/songs
    elif query.startswith("play"):
        query = query.replace("play", "").replace("song", "").replace("music", "").strip()
        if query:
            webbrowser.open("https://music.youtube.com/search?q=" + urllib.parse.quote_plus(query))
            return f"results for {query} on YouTube Music"
        else:
            webbrowser.open("https://music.youtube.com")
            return "Opening YouTube Music"
    # Get current time
    elif 'time' in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}"
    # Get current date
    elif 'date' in query or 'today' in query:
        return get_current_date()
    # AI-powered responses using Gemini
    else:
        # Check if API key is set
        if os.getenv('GEMINI_API_KEY'):
            return gemini(query)
        else:
            logging.warning("Warning: GEMINI_API_KEY environment variable not found!")
            logging.info("Please set your GEMINI_API_KEY environment variable. Otherwise you won't be able to get AI responses.")
            return search(query)