# Transcriber Project Instructions (GEMINI.md)

This file provides architectural context, conventions, and operational guidelines for AI agents working within this repository.

## Overview
The Transcriber application is an interactive Python-based console REPL built around the Command pattern. It utilizes the Google Gemini API to split and transcribe video/audio files, and translate transcriptions between languages.

## Running the App
```bash
python main.py
```

### Available Commands in REPL
```
load                    # Load GEMINI_API_KEY from .env into session state
transcribe <path>       # Split video -> transcribe to text -> write .txt output
translate <path>        # Translate a transcription .txt file -> write .txt output
models                  # List available Gemini models and their capabilities
use <model_name>        # Switch the active Gemini model (supports short names like 'gemini-1.5-flash')
usage                   # Display the total tokens used in the current session and rate limit status
help                    # Show the help message
exit                    # Exit the application cleanly
```

## Setup & Environment
**Dependencies:**
```bash
pip install -r requirements.txt
brew install ffmpeg  # Required for pydub video splitting
```

**Environment Variables:**
Create a `.env` file in the project root:
```
GEMINI_API_KEY=<your_key>
```

## Architecture & Logic Flow

### 1. Entry & Console Layer (`main.py` -> `console/`)
- **`Session`**: Runs the REPL loop. Captures `KeyboardInterrupt` (Ctrl+C) and `EOFError` (Ctrl+D) to prevent raw crashes, allowing the user to return to the prompt or exit cleanly.
- **`AppState`**: Holds shared mutable state passed to every command. Tracks:
  - `api_key`
  - `current_model` (e.g., `models/gemini-1.5-flash`)
  - `total_tokens_used`
  - Rate limiting logic (`is_rate_limited`, `retry_after`)
- **`CommandFactory`**: Centralizes command instantiation. `Session` loads all commands dynamically from this factory.
- **Commands**: Encapsulate specific workflows (`TranscribeCommand`, `TranslateCommand`, `UseCommand`, etc.). Protected by a `@requires_key` decorator where API access is needed.

### 2. Agents & Models Layer (`agents/`)
- **`Model`**: Core wrapper for the Gemini SDK (`google-genai`). 
  - Handles file uploads and polling (`PROCESSING` state).
  - Implements **Rate Limit Handling**: Catches `429 RESOURCE_EXHAUSTED` errors, parses the retry delay, pauses execution, and automatically retries (up to 3 times) before bubbling the error up.
  - Auto-deletes uploaded files from the Gemini API after generating content to maintain cleanliness.
- **`ModelFactory`**: Initializes the `Model` using the API key, prompt path, and the dynamically selected `model_type` from `AppState`.
- **`Transcriber` / `Translator`**: Thin wrappers around `Model` that map the correct processor type (`audio` vs `text`).

### 3. Utils Layer (`utils/`)
- **`VideoSplitter`**: Uses `pydub` to slice large MP4 files into smaller MP3 chunks (default 20 mins) to respect API payload limits.
- **`TextWriter`**: Manages output file creation in the `output/` directory.
- **Cleanup Guarantee**: Commands utilizing `VideoSplitter` (like `TranscribeCommand`) wrap the execution in a `try...finally` block to guarantee the deletion of local temporary `.mp3` chunks, even if the user issues a `KeyboardInterrupt`.

### 4. Prompts (`agents/prompts/`)
*Note: A multi-language overhaul is currently underway (see `.gemini/stages.md`).*
- Currently holds Markdown instructions dictating how the Gemini models format their output (e.g., preserving timestamps like `[MM:SS]`, using specific speaker labels).

## Development Conventions
- **Typing**: Strict Python type hinting is required across all new and modified code.
- **Error Handling**: 
  - Catch known issues and raise `CommandError` for clean console output.
  - Anticipate API limits. If modifying API calls, integrate with the existing rate-limit tracking in `AppState`.
  - Always clean up temporary resources (files, API uploads) using `finally` blocks.
- **Command Addition**: When adding a new feature to the REPL, create a new class inheriting from `Command` in `console/commands/`, and register it in `console/commands/command_factory.py`. Do *not* bloat `session.py` with command imports.
- **Idiomatic Python**: Prefer decorators (like `@requires_key`), factories, and explicit object composition.
