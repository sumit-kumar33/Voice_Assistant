import speech_recognition
from config_files.logs_config import *
def take_command():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        logging.info("Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        logging.info("Recognizing...")
        query = r.recognize_google(audio, language='en-in') # pyright: ignore[reportAttributeAccessIssue]
    except Exception:
        logging.exception("Failed to run take_command() function")
        return None
    return query.lower()