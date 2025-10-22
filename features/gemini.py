from google import genai
from google.genai import types
from config_files.config import Name
from config_files.logs_config import *

# Gemini API call function
def gemini(query: str) -> str:
    # genai configuration it automatically takes "GEMINI-API-KEY" from environment variables
    client = genai.Client()
    config = types.GenerateContentConfig(
        system_instruction=f"Your name is {Name} and you are a voice assistant. Try to keep responses within 300 characters.",
    )
    try:
        instruction = "Please provide a brief and helpful response."
        response: types.GenerateContentResponse = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            config=config,
            contents=query + instruction
        )
        if response and response.text:
            # Clean up response text
            cleaned_response: str = response.text.replace("*", "").replace("#", "").strip()
            return cleaned_response
        else:
            return "Could not get a valid response from Gemini."
    except Exception as e:
        logging.exception(f"Gemini API error: {e}")
        return "Trouble connecting to Gemini API"