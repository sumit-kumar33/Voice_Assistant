from config_files.logs_config import *
from features.wishme import wishme
from actions import actions
from speech.speak import speak

def main():
    logging.info("=" * 50 + f"{Name} is starting" + "=" * 50)

    messages.info("=" * 50 + f"{Name} is starting" + "=" * 50)
    try:
        speak(wishme())
        while True:
            response: str = actions()
            if "exit" in response or "stop listening" in response or "goodbye" in response:
                speak("Goodbye")
                break
            else:
                speak(response)
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        speak("An unexpected error occurred. Shutting down.")

if __name__ == '__main__':
    main()