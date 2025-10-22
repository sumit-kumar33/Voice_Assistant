import speech_recognition
from config_files.logs_config import *
from speech.speak import *
def take_command():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        speak("Listening")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        speak("Recognising")
        query = r.recognize_google(audio, language='en-in') # pyright: ignore[reportAttributeAccessIssue]
    except Exception:
        logging.exception("Failed to run take_command() function")
        messages.info(f"You: None")
        return None
    messages.info(f"You: {query.lower()}")
    return query.lower()