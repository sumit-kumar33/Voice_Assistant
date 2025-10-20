import datetime
from speak import speak
from config import *
# Wishes Good Morning, Afternoon, Evening according to time
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak(f"I am {Name}. How may I help you today? You can speak *exit* anytime for me to stop listening")