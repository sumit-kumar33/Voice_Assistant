from config_files.logs_config import *
from features.wishme import wishme
from features.actions import actions
from speech.take_command import take_command
from speech.speak import speak

def main():
    logging.info("=" * 50 + f"{Name} is starting" + "=" * 50)
    messages.info("=" * 50 + f"{Name} is starting" + "=" * 50)
    speak(wishme())
    while True:
        try:
            query = take_command()
            if query != None:
                query = query.lower().strip()
                if "exit" in query or "stop listening" in query or "goodbye" in query:
                    speak("Goodbye")
                    break
                else:
                    speak(actions(query))
            else:
                speak("I couldn't understand that, Please repeat")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            speak("An unexpected error occurred. Shutting down.")
            break

if __name__ == '__main__':
    main()