from config_files.logs_config import *
from features.wishme import wishme
from features.actions import actions
from speech.take_command import take_command
from speech.speak import speak

def main():
    startup_log()

    flag = False  # start in sleep mode
    while True:
        activation = take_command()
        logging.info(f"You (in sleep mode): {activation}")
        if activation:
            activation = activation.lower().strip()
            if "hey " + Name.lower() in activation or Name.lower() in activation:
                flag = True

        while flag:
            speak(wishme())
            while True:
                try:
                    query = take_command()
                    if query:
                        messages.info(f"You: {query.lower()}")
                        query = query.lower().strip()
                        if "exit" in query or "goodbye" in query:
                            speak("Goodbye")
                            return
                        elif "stop listening" in query or "sleep" in query:
                            flag = False
                            speak("Going to sleep mode. Say 'Hey " + Name + "' to wake me up.")
                            break
                        else:
                            speak(actions(query))
                    else:
                        speak("I couldn't understand that, Please repeat")
                except KeyboardInterrupt:
                    # treat Ctrl+C while active as "stop listening" (sleep)
                    flag = False
                    speak("Going to sleep mode. Say 'Hey " + Name + "' to wake me up.")
                    break
                except Exception as e:
                    logging.exception(f"An unexpected error occurred: {e}")
                    speak("An unexpected error occurred. Shutting down.")
                    return

if __name__ == '__main__':
    main()