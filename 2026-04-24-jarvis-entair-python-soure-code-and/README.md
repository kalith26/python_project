# Jarvis Entair Python Source Code

An advanced, friendly Python assistant inspired by Jarvis.

## Features

- Text mode and voice mode
- Friendly human-style replies
- System information commands
- Open websites, apps, and folders
- Reminder support during the current session
- Local knowledge answers for common questions
- Optional AI provider hook for future upgrades
- Safe self-update helper for Git-based projects

## Project Structure

- `main.py` - app entry point
- `jarvis/assistant.py` - main assistant loop
- `jarvis/brain.py` - response generation and AI fallback
- `jarvis/commands.py` - command parsing and actions
- `jarvis/system_tools.py` - system and OS helpers
- `jarvis/voice.py` - speech input and speech output
- `jarvis/config.py` - runtime settings

## Install

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If `PyAudio` fails on your machine, you can still use text mode.

## Run

Multi-file version:

```powershell
python main.py
```

Single-file version:

```powershell
python jarvis_single.py
```

## Google AI Setup

Set your API key in the environment before starting Jarvis:

```powershell
$env:JARVIS_AI_API_KEY="your_google_api_key"
python jarvis_single.py
```

Optional model override:

```powershell
$env:JARVIS_GOOGLE_MODEL="gemini-2.5-flash"
python jarvis_single.py
```

Choose:

- `1` for text mode
- `2` for voice mode

## Example Commands

- `hello`
- `what can you do`
- `system status`
- `battery status`
- `open notepad`
- `open youtube`
- `open folder downloads`
- `remember buy milk`
- `show reminders`
- `time`
- `date`
- `search python voice recognition`
- `update yourself`
- `exit`

## Notes

- "Access all system" is not implemented as unrestricted control. The assistant includes practical local helpers and can be extended safely.
- For real cloud AI, add your own provider inside `jarvis/brain.py`.
