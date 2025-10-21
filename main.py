from logs_config import *
from wishme import wishme
from actions import actions
from speak import speak

def main():
    logging.info("=" * 50 + f"{Name} is starting" + "=" * 50)

    messages.info("=" * 50 + f"{Name} is starting" + "=" * 50)
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