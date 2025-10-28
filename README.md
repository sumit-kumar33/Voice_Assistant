# AI Voice Assistant

This repository contains a simple Python voice assistant that uses the Gemini API for AI responses and local libraries for speech I/O.

## Quick links

- Source: [main.py](main.py)
- Python dependencies: [requirements.txt](requirements.txt)
- Git ignore: [.gitignore](.gitignore)

## Features

- Wake and greet: [`features.wishme.wishme`](features/wishme.py)

- Speech-to-text input (Google Web Speech, default language: en-IN): [`take_command.py`](speech/take_command.py)

- Text-to-speech output (uses first available voice): [`speak.py`](speech/speak.py)

- Activation (wake) phrase
  - The assistant now waits for a wake phrase before accepting a command. Say "hey Voice Assistant" or "voice assistant" to activate. See [`main.py`](main.py) and the greeting helper [`features.wishme.wishme`](features/wishme.py).
  - You can include a command inline with the wake phrase (e.g. "hey Voice Assistant, open youtube") or say the wake phrase and then speak the command when prompted.

- Actions and command routing loop: [`actions.py`](features/actions.py)
  - Wikipedia summaries
  - Web search via specified search engine (default: DuckDuckGo)
  - Open YouTube, Google, default browser
  - Open ChatGPT
  - “Play …” via YouTube Music
  - Current time and date via [`get_current_date.py`](features/get_current_date.py)

- Graceful sleep / wake
  - The assistant supports a sleep mode (enter with "stop listening" or "sleep") and wakes only on the activation phrase again.

- AI responses from Gemini (requires API key): [`gemini.py`](features/gemini.py)
  - Model: gemini-2.0-flash-exp
  - System prompt includes the assistant name and instruction to keep the responses short.

## Requirements

- Python 3.8+
- System audio (microphone + speakers)
- Optional but recommended: `GEMINI_API_KEY`
  - If missing, the assistant runs but AI answers will be unavailable and the query will be searched in the specified search engine and A warning is logged.
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

Edit the [config.py](config_files/config.py):

- Assistant name (affects greetings, logs, and Gemini system prompt):
  - `Name = "Voice Assistant"`
- Default search engine for “search”:
  - `search_engine = "duckduckgo"`

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
  - The code calls `pyttsx3.init('sapi5')` which is Windows-specific. On macOS use `'nsss'`, on many Linux systems use `'espeak'`. If you run on a non-Windows OS, change the backend when initializing the engine in [`speak.py`](speech/speak.py).
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
  - The recognizer uses a `pause_threshold` of 1.5s. In noisy environments or with low-volume mics, adjust thresholds in [`take_command.py`](speech/take_command.py).
- Browser behavior:
  - `webbrowser.open(...)` uses the system default browser; results may vary across environments or on headless servers.
- Gemini & privacy:
  - AI queries are sent to Google’s Gemini API when enabled. Understand privacy and billing for your account.

## Troubleshooting

- Speech not recognized:
  - Check microphone permissions and input device; consider increasing `pause_threshold` in [`take_command.py`](speech/take_command.py).
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
  - `google-genai` — Gemini client (requires `GEMINI_API_KEY`)

## Where to look in the code

- Entry point: [`main.main`](main.py)
- Greeting and startup: [`wishme.py`](features/wishme.py)
- Speech/TTS helpers: [`speak.py`](speech/speak.py), [`take_command.py`](speech/take_command.py)
- Action routing: [`actions.py`](features/actions.py)
- Gemini usage: [`gemini.py`](features/gemini.py)
- Date helper: [`get_current_date.py`](features/get_current_date.py)

## Limitations

- Backend-specific TTS initialization and voice handling cause OS-specific bugs.
- Requires network connectivity for both speech recognition (Google) and Gemini API calls.
- Real-time performance depends on microphone quality, network latency, and Gemini response time.
- Not hardened for production: limited error handling and concurrency; running long sessions may surface unhandled exceptions.
- Possible costs from Gemini usage depending on your account and model.