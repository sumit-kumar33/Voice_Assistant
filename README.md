# AI Voice Assistant

This repository contains a simple Python voice assistant that uses the Gemini API for AI responses and local libraries for speech I/O.

## Quick links

- Source: [main.py](main.py)
- Python dependencies: [requirements.txt](requirements.txt)
- Git ignore: [.gitignore](.gitignore)

## Features

- Wake and greet: [`main.wishme`](main.py)
- Speech-to-text input (Google Web Speech, default language: en-IN): [`main.take_command`](main.py)
- Text-to-speech output (uses first available voice): [`main.speak`](main.py)
- Actions and command routing loop: [`main.actions`](main.py)
  - Wikipedia summaries
  - Web search via specified search engine (default: DuckDuckGo)
  - Open YouTube, Google, default browser
  - Open ChatGPT
  - “Play …” via YouTube Music
  - Current time and date via [`main.get_current_date`](main.py)
  - Exit using “exit”, “stop listening”, or “goodbye”
- AI responses from Gemini (requires API key): [`main.client`](main.py)
  - Model: gemini-2.0-flash-exp
  - System prompt includes the assistant name and instruction to keep the responses short.

## Requirements

- Python 3.8+
- System audio (microphone + speakers)
- Optional but recommended: `GEMINI_API_KEY`
  - If missing, the assistant runs but AI answers will be unavailable. A warning is logged.
- Install Python deps:

```sh
pip install -r requirements.txt
```

## Run

1. Ensure `GEMINI_API_KEY` is set in your environment.
2. Start the assistant:

```sh
python main.py
```

## Configuration

Edit the top of [main.py](main.py):

- Assistant name (affects greetings, logs, and Gemini system prompt):
  - `Name = "Voice Assistant"`
- Default search engine for “search”:
  - `search_engine = "duckduckgo"`
- TTS backend and voice:
  - Windows uses `pyttsx3.init('sapi5')` and sets the first voice: `voices[0].id`
  - To change voices, adjust the selected index or choose a different voice ID
- Speech recognition locale:
  - Default is `r.recognize_google(..., language='en-in')`. Change to e.g. `en-US` as and when needed.

## Logging

- Logs are written to:
  - `<Name>.log` (e.g., “Voice Assistant.log”)
  - `<Name> messages.log` (e.g., “Voice Assistant messages.log”)
- Messages log also stream to the console. Review these files for debugging and usage history.

## Typical usage

- Say:
  - “wikipedia alan turing”
  - “search python decorators”
  - “open youtube” / “open google” / “open browser”
  - “open chat gpt”
  - “play lo-fi music”
  - “what’s the time”
  - “what’s the date” / “today”
- Stop with: “exit”, “stop listening”, or “goodbye”.

## Cross-OS limitations and notes

- Text-to-speech backend:
  - The code calls `pyttsx3.init('sapi5')` which is Windows-specific. On macOS use `'nsss'`, on many Linux systems use `'espeak'`. If you run on a non-Windows OS, change the backend when initializing the engine in [`main.py`](main.py).
- Voice selection:
  - `engine.getProperty('voices')` returns a list; setting `engine.setProperty('voice', voice)` may be incorrect if `voice` is the list. Behavior differs by OS and available voice engines.
- PyAudio / microphone:
  - PyAudio needs system PortAudio libs. Install system packages first:
    - Debian/Ubuntu: `sudo apt-get install portaudio19-dev python3-dev`
    - macOS: `brew install portaudio`
    - Windows: prefer installing a PyAudio wheel if pip fails.
  - Microphone permissions may be required on macOS and some Linux desktops.
- Speech recognition:
  - `speech_recognition.Recognizer().recognize_google(...)` uses Google’s web API and requires network access; rate limits may apply.
- Timing and noise:
  - The recognizer uses a `pause_threshold` of 1.5s. In noisy environments or with low-volume mics, adjust thresholds in [`main.take_command`](main.py).
- Browser behavior:
  - `webbrowser.open(...)` uses the system default browser; results may vary across environments or on headless servers.
- Gemini & privacy:
  - AI queries are sent to Google’s Gemini API when enabled. Understand privacy and billing for your account.

## Troubleshooting

- Speech not recognized:
  - Check microphone permissions and input device; consider increasing `pause_threshold` in [`main.take_command`](main.py).
- TTS fails on macOS/Linux:
  - Switch the `pyttsx3` backend from `'sapi5'` to the OS-appropriate backend.
- PyAudio installation fails:
  - Install system PortAudio package and retry, or use prebuilt wheels on Windows.
- No AI responses:
  - Set `GEMINI_API_KEY` in your environment. Without it, the app will run but won’t generate AI answers.

## Technologies

- Python standard library: `datetime`, `webbrowser`, `urllib.parse`, `os`
- Speech and audio:
  - `speechrecognition` — speech-to-text
  - `pyaudio` — microphone input (PortAudio)
  - `pyttsx3` — text-to-speech
- Online knowledge & jokes:
  - `wikipedia` — fetch summaries
  - `pyjokes` — jokes
- AI:
  - `google.generativeai` — Gemini client (requires `GEMINI_API_KEY`)

## Where to look in the code

- Entry point: [`main.main`](main.py)
- Greeting and startup: [`main.wishme`](main.py)
- Speech/TTS helpers: [`main.speak`](main.py), [`main.take_command`](main.py)
- Action routing + Gemini usage: [`main.actions`](main.py), [`main.client`](main.py)
- Date helper: [`main.get_current_date`](main.py)

## Limitations

- Backend-specific TTS initialization and voice handling cause OS-specific bugs.
- Requires network connectivity for both speech recognition (Google) and Gemini API calls.
- Real-time performance depends on microphone quality, network latency, and Gemini response time.
- Not hardened for production: limited error handling and concurrency; running long sessions may surface unhandled exceptions.
- Possible costs from Gemini usage depending on your account and model.

For code details, inspect [main.py](main.py) and the dependency list in [requirements.txt](requirements.txt).
