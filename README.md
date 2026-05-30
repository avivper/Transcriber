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
- **Automated Organization**: Output files are automatically categorized into `output/English/` or `output/Hebrew/`.
- **Automatic Video Splitting**: Handles long lectures by splitting them into 20-minute MP3 chunks.
- **Rate-Limit Handling**: Automatically detects `429 RESOURCE_EXHAUSTED` errors and retries with backoff.
- **Dynamic Model Selection**: List and switch between Gemini models (Flash/Pro) mid-session.
- **Smart Launcher**: Custom `./Transcriber` script that checks dependencies and activates your virtual environment automatically.

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

3. **Make it a Global Command (Optional but Recommended)**
   To run `Transcriber` from any directory on your system:
   ```bash
   chmod +x Transcriber
   sudo ln -sf "$(pwd)/Transcriber" /usr/local/bin/Transcriber
   ```
   Now you can simply type `Transcriber` in any terminal window to start the app.

---

## Configuration

### API Setup Guide

To use Transcriber, you need a Google Gemini API key.

1. **Get your API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Sign in with your Google account.
   - Click **"Create API key"**.
   - Copy your unique API key.

2. **Create the .env file**:
   - In the project's root directory, create a new file named `.env`.
   - Add your key to the file using this exact format:
     ```env
     GEMINI_API_KEY=your_actual_key_here
     ```
   - Save and close the file.

---

## Usage

Start the interactive session using the global launcher:
```bash
./Transcriber
```

### Commands

| Command | Description |
|---|---|
| `load` | Load the Gemini API key from `.env` |
| `transcribe <path> [lang]` | Transcribe video. Default: English (`en`), supports Hebrew (`he`) |
| `translate <path> [lang]` | Translate text. Default: Hebrew (`he`), supports English (`en`) |
| `models` | List all available Gemini models |
| `use <model>` | Switch the active model (e.g., `gemini-1.5-flash`) |
| `current` | Show the currently active Gemini model |
| `usage` | Show session token count and API status |
| `clear` | Clear the console screen and redisplay the banner |
| `help` | Show all available commands |
| `exit` | Exit the application |

---

## Architecture

Transcriber follows a highly modular, professional architecture designed for stability and extensibility.

### Core Design Patterns
- **Command Pattern**: Every CLI operation (`transcribe`, `translate`, etc.) is encapsulated as a standalone class inheriting from a base `Command`. This keeps the main logic loop decoupled from specific feature implementations.
- **Orchestrator Middleware**: A dedicated `Orchestrator` layer uses Python decorators to dynamically inject language-specific request prompts into agent methods based on user selection.
- **Facade Pattern**: All packages (`console`, `agents`, `utils`) utilize `__init__.py` files to expose a clean, high-level interface while hiding internal implementation details and preventing circular dependencies.
- **Factory Pattern**: Centralized factories manage the instantiation of AI Agents and Gemini Model wrappers, ensuring consistent configuration across the app.

### Technical Components
- **State Management**: A global `AppState` object tracks cumulative token usage, active model selection, and real-time rate limit status across the entire session.
- **Resource Management**: The `VideoSplitter` utility handles large files by slicing them into optimized MP3 chunks. All operations utilize `try...finally` blocks to guarantee the cleanup of temporary local files and API-side uploads.
- **Error Resilience**: Built-in 429 `RESOURCE_EXHAUSTED` handling automatically parses retry headers from the Gemini API and performs smart backoff retries.

---

## Tech Stack

| Component | Technology |
|---|---|
| **LLM Engine** | Google Gemini (via `google-genai` SDK) |
| **Audio/Video** | `pydub` + `ffmpeg` |
| **Config** | `python-dotenv` |
| **CLI** | Interactive Python REPL |
