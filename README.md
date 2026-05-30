# Transcriber

```
+--------------------------------------------------------------+
|                                                              |
|  _____                              _ _                      |
| |_   _| __ __ _ _ __  ___  ___ _ __(_) |__   ___ _ __        |
|   | || '__/ _` | '_ \/ __|/ __| '__| | '_ \ / _ \ '__|       |
|   | || | | (_| | | | \__ \ (__| |  | | |_) |  __/ |          |
|   |_||_|  \__,_|_| |_|___/\___|_|  |_|_.__/ \___|_|          |
|                                                              |
+--------------------------------------------------------------+
```

> AI-powered lecture transcription and translation — built to help students review university lectures with multi-language support and smart resource management.

---

## Overview

Transcriber is an interactive CLI tool that transforms video lectures into structured, timestamped transcriptions. Powered by Google Gemini, it handles large video files by intelligently splitting them into chunks and processing them with specialized AI agents.

The tool features a robust interactive REPL with automated rate-limit handling, dynamic model switching, and graceful interrupt support.

---

## Features

- **Multi-Language Support**: Transcribe or translate into English or Hebrew.
- **Automatic Video Splitting**: Handles long lectures by splitting them into 20-minute MP3 chunks.
- **Rate-Limit Handling**: Automatically detects `429 RESOURCE_EXHAUSTED` errors and retries with backoff.
- **Dynamic Model Selection**: List and switch between Gemini models (Flash/Pro) mid-session.
- **Session Tracking**: Monitor token usage across multiple commands.
- **Graceful Interrupts**: Cleanly handle `Ctrl+C` with guaranteed cleanup of temporary files.
- **Professional Architecture**: Clean Command pattern with a centralized Orchestrator and package facades.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/avivper/Transcriber.git
   cd Transcriber
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   brew install ffmpeg  # Required for audio processing
   ```

3. **Set up API Key**
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

---

## Usage

Start the interactive session:
```bash
python main.py
```

### Commands

| Command | Description |
|---|---|
| `load` | Load the Gemini API key from `.env` |
| `transcribe <path> [lang]` | Transcribe video. Default: English (`en`), supports Hebrew (`he`) |
| `translate <path> [lang]` | Translate text. Default: Hebrew (`he`), supports English (`en`) |
| `models` | List all available Gemini models |
| `use <model>` | Switch the active model (e.g., `gemini-1.5-flash`) |
| `usage` | Show session token count and API status |
| `help` | Show all available commands |
| `exit` | Exit the application |

### Example Workflow

```
>>> load
API Key loaded successfully!
>>> transcribe lecture.mp4 he
Splitting 'lecture.mp4'...
Transcribing into HEBREW...
Created the output at output/lecture_heb.txt
>>> usage
Total session usage so far: 15420 tokens.
```

---

## Output Format

Transcriptions include `[MM:SS]` timestamps and speaker labels (`**Lecturer:**` or `**מרצה:**`). 

**English Example:**
```
**Lecturer:** `[02:15]`
As we discussed last week, the scheduler is responsible for...
```

---

## Architecture

Transcriber is built with a clean, extensible architecture:
- **Command Pattern**: Every action is a standalone class.
- **Orchestrator Layer**: Manages language-specific prompts and agent coordination.
- **Facade Pattern**: Uses `__init__.py` files for clean, consolidated imports.
- **State Management**: A global `AppState` tracks tokens, rate limits, and model choices.

For deeper technical details, see [GEMINI.md](./GEMINI.md).

---

## Tech Stack

| Component | Technology |
|---|---|
| **LLM Engine** | Google Gemini (via `google-genai` SDK) |
| **Audio/Video** | `pydub` + `ffmpeg` |
| **Config** | `python-dotenv` |
| **CLI** | Interactive Python REPL |
