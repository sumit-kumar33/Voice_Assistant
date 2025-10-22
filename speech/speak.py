from config_files.config import *
from config_files.logs_config import *
import pyttsx3

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
def speak(audio):
    messages.info(f"{Name}: {audio}")
    try:
        engine.say(audio)
        engine.runAndWait()
    except KeyboardInterrupt:
        return