from config import *
from logs_config import *
from speak import speak
from take_command import take_command
from get_current_date import get_current_date
from gemini import gemini
from search import search
import webbrowser
import os
import pyjokes
import urllib.parse
import wikipedia
import datetime

#TODO: Refactor this function and make a dictionary mapping commands to functions for better scalability

def get_text_command():
    try:
        return input("Type your command: ").strip().lower()
    except EOFError:
        return None

def actions():
    use_voice = True
    while True:
        try:
            if use_voice:
                query = take_command()
                if not query:
                    speak("I couldn't understand that, Please repeat or press Ctrl+C to type.")
                    continue
            else:
                try:
                    query = get_text_command()
                    if query == "voice":
                        speak("Switching to voice mode. You can speak your command now. Press Ctrl+C to return to typing mode.")
                        use_voice = True
                        continue
                    elif not query:
                        speak("No input received. Please try again.")
                        continue
                except KeyboardInterrupt:
                    query = "exit"
        except KeyboardInterrupt:
            speak("Switching to typing mode. Please type your command below. Type 'voice' to switch back to voice mode. Type 'exit' to quit.")
            use_voice = False
            continue

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
            speak(search(query))

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

        # Open YouTube
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
            speak("Goodbye")
            break

        # AI-powered responses using Gemini
        else:
            # Check if API key is set
            if os.getenv('GEMINI_API_KEY'):
                speak(gemini(query))
            else:
                speak(search(query))
                logging.warning("Warning: GEMINI_API_KEY environment variable not found!")
                logging.info("Please set your GEMINI_API_KEY environment variable. Otherwise you won't be able to use features that rely on Gemini.")