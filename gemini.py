from google import genai
from config import *
from google.genai import types
from speak import speak
from logs_config import *

# genai configuration it automatically takes "GEMINI-API-KEY" from environment variables
client = genai.Client()
config = types.GenerateContentConfig(
    system_instruction=f"Your name is {Name} and you are a voice assistant. Try to keep responses within 300 characters.",
)

def gemini(query):
    try:
        instruction = "Please provide a brief and helpful response."
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            config=config,
            contents=query + instruction
        )
        if response and response.text:
            # Clean up response text
            cleaned_response = response.text.replace("*", "").replace("#", "").strip()
            speak(cleaned_response)
        else:
            speak("I'm sorry, I couldn't generate a response for that")
    except Exception as e:
        speak("Sorry, I'm having trouble connecting to my AI service right now")
        logging.exception(f"Gemini API error: {e}")