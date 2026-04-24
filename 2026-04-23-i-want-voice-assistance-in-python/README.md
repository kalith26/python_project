# Python Voice Assistant

This is a simple voice assistant you can use in your Python project.

## Features

- Listens to your microphone
- Speaks responses
- Opens websites
- Opens Windows apps
- Tells time and date
- Runs custom shell commands with `run ...`

## Files

- `voice_assistant.py` - main assistant code
- `requirements.txt` - Python packages

## Install

Install Python 3.11+ first and make sure it is added to PATH.

```powershell
python -m pip install -r requirements.txt
```

If `PyAudio` fails to install on Windows, install it with:

```powershell
python -m pip install pipwin
python -m pipwin install pyaudio
```

## Run

```powershell
python voice_assistant.py
```

## Example voice commands

- `open google`
- `open youtube`
- `open notepad`
- `what is the time`
- `what is the date`
- `search python tutorials`
- `run dir`
- `stop`

## Add your own controls

Open `voice_assistant.py` and edit these dictionaries:

- `self.websites`
- `self.desktop_apps`

You can also add your own logic inside `handle_command()`.

## Important note

The `run ...` command can execute system commands. Keep it only if you trust the microphone input and want that behavior.
