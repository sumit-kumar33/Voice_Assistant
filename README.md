# AI Voice Assistant

This repository contains a simple Python voice assistant that uses the Gemini API for AI responses and local libraries for speech I/O.

## Quick links

- Source: [main.py](main.py)
- Python dependencies: [requirements.txt](requirements.txt)
- Git ignore: [.gitignore](.gitignore)

## Features

- Wake and greet: [`main.wishme`](main.py)
- Speech-to-text input: [`main.take_command`](main.py)
- Text-to-speech output: [`main.speak`](main.py)
- Action loop and command routing: [`main.actions`](main.py)
- AI responses from Gemini (requires API key): [`main.client`](main.py)

## Requirements

- Python 3.8+
- System audio (microphone + speakers)
- Set environment variable: `GEMINI_API_KEY` (the program exits if missing)
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

## Typical usage

- Speak commands like "search python decorators", "open youtube", "what's the time", "wikipedia machine learning", or "tell me a joke".
- Say "exit" or "stop listening" or "goodbye" to stop the assistant.
- The AI response pipeline is in [`main.actions`](main.py) and will call Gemini when the query isn't matched to a built-in action.

## Cross-OS limitations and notes

- Text-to-speech backend:
  - The code calls `pyttsx3.init('sapi5')` which is Windows-specific. On macOS, use `'nsss'`, on many Linux systems, use `'espeak'`. If you run on a non-Windows OS, change the backend when initialising the engine in [`main.py`](main.py).
- Voice selection:
  - `engine.getProperty('voices')` returns a list; setting `engine.setProperty('voice', voice)` may be incorrect if `voice` is the list. Behaviour differs by OS and available voice engines.
- PyAudio / microphone:
  - PyAudio needs the system PortAudio libs. Install system packages first:
    - Debian/Ubuntu: `sudo apt-get install portaudio19-dev python3-dev`
    - macOS: `brew install portaudio`
    - Windows: prefer installing a PyAudio wheel if pip fails.
  - Microphone permissions: macOS and some Linux desktops require granting microphone access to the terminal/IDE.
- Speech recognition:
  - `speech_recognition.Recognizer().recognize_google(...)` uses Google's web API (network access). It may be rate-limited or require connectivity.
- Timing and noise:
  - `timeout` and `phrase_time_limit` are set; noisy environments or low-volume mics may cause missed input. Adjust thresholds and phrase limits in [`main.take_command`](main.py).
- Browser behavior:
  - `webbrowser.open(...)` uses the system default browser; results may vary across environments and headless servers.
- Gemini & privacy:
  - AI queries are sent to Google’s Gemini API. Ensure you understand privacy and billing. The code expects `GEMINI_API_KEY` in the environment.
- Virtual environment paths:
  - Example activation scripts exist under `env/Scripts` (Windows). On Unix systems use `env/bin/activate` if you create a venv there.

## Troubleshooting

- If speech isn't recognized: check mic permissions, test microphone with another app, increase `pause_threshold` or `phrase_time_limit`.
- If TTS fails on macOS/Linux: change the `pyttsx3` backend from `'sapi5'` to the OS-appropriate backend.
- If PyAudio installation fails: install PortAudio system package and retry, or use prebuilt wheels on Windows.

## Where to look in the code

- Main entry and overall flow: [`main.main`](main.py)
- Greeting and startup: [`main.wishme`](main.py)
- Speech/TTS helpers: [`main.speak`](main.py) and [`main.take_command`](main.py)
- Action routing + Gemini usage: [`main.actions`](main.py)

## Limitations

- Backend-specific TTS initialisation and voice handling cause OS-specific bugs.
- Requires network connectivity for both speech recognition (Google) and Gemini API calls.
- Real-time performance depends on microphone quality, network latency, and Gemini response time.
- Not hardened for production: limited error handling and concurrency; running long sessions may surface unhandled exceptions.
- Possible costs from Gemini usage depending on your account and model.

For code details, inspect [main.py](main.py) and the dependency list in [requirements.txt](requirements.txt).

## Technologies

- Python standard library: `datetime`, `webbrowser`, `urllib.parse`, `os`, `logging`
- Speech and audio:
  - `speechrecognition` — speech-to-text
  - `pyaudio` — microphone input (PortAudio)
  - `pyttsx3` — text-to-speech
- Online knowledge & jokes:
  - `wikipedia` — fetch summaries
  - `pyjokes` — jokes
- AI:
  - `google-genai` — Gemini client (requires `GEMINI_API_KEY`)
