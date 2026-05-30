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
load                      # Load GEMINI_API_KEY from .env into session state
transcribe <path> [lang]  # Transcribe video (lang: en|he, default: en)
translate <path> [lang]   # Translate text (lang: en|he, default: he)
models                    # List available Gemini models and their capabilities
use <model_name>          # Switch active model (e.g., 'gemini-1.5-flash')
usage                     # Display session tokens and rate limit status
help                      # Show the help message
exit                      # Exit the application cleanly
```

## Architecture & Logic Flow

### 1. Console Layer (`console/`)
- **`Session`**: The REPL loop. Handles `KeyboardInterrupt` and `EOFError` gracefully.
- **`AppState`**: Shared state (API key, model choice, token usage, rate limit status).
- **`CommandFactory`**: Central registry for all commands to keep `Session` clean.
- **`Orchestrator`**: A decorator-based middleware (`language_prompt`) that injects language-specific request prompts into agent methods.

### 2. Agents & Models Layer (`agents/`)
- **`Model`**: Gemini SDK wrapper with built-in **429 Rate Limit Handling** (auto-retry with backoff).
- **`Transcriber` / `Translator`**: Language-aware agents. Use `@language_prompt` to dynamically select request templates.
- **`Prompts`**: Located in `agents/models/prompts/`. Named by task and language (e.g., `transcription_he.md`).

### 3. Utils Layer (`utils/`)
- **`VideoSplitter`**: Slices video into MP3 chunks (default 20 mins).
- **Cleanup**: `TranscribeCommand` uses `try...finally` to ensure local chunk deletion.

## Development Conventions
- **Multi-Language**: When adding a language, create the `.md` prompt in `prompts/` and update the `language_prompt` decorator in `orchestrator.py`.
- **Typing**: Use strict Python type hints.
- **Command Structure**: Follow the helper-method pattern (`_get_args`, `_rate_limit_checks`, etc.) in Command classes.
- **Cleanup**: Always use `finally` for resource cleanup (files, API uploads).
