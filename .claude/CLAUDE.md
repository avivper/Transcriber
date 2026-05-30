# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
python main.py
```

Inside the interactive session, available commands are:
```
load                    # load GEMINI_API_KEY from .env into session state
transcribe <path>       # split video → transcribe → write .txt output
translate <path>        # translate a transcription .txt file → write .txt output
exit
```

List available Gemini models (utility):
```bash
python llm/models.py
```

## Setup

**Dependencies:**
```bash
pip install -r requirements.txt
brew install ffmpeg
```

**Environment:** create a `.env` file in the project root:
```
GEMINI_API_KEY=<your_key>
```

## Architecture

The app is an interactive console REPL built with a Command pattern.

**Entry → Console layer** (`main.py` → `console/`):
- `Session` runs the REPL loop and dispatches input to registered `Command` objects
- `AppState` holds shared mutable state (api_key, running flag) passed to every command
- Commands: `LoadCommand`, `TranscribeCommand`, `TranslateCommand`, `ExitCommand`
- `requires_key` decorator (in `command.py`) guards commands that need an API key

**TranscribeCommand flow**: `VideoSplitter` splits the MP4 into MP3 chunks → `Transcriber` uploads each chunk to Gemini Files API and fetches transcription → `TextWriter` writes results to `/output`

**TranslateCommand flow**: `Translator` uploads a text file to Gemini Files API → fetches Hebrew translation → `TextWriter` writes results to `/output`

**Agents layer** (`agents/`):
- `Model` — core Gemini wrapper: uploads files, polls until ready (`PROCESSING` state), calls `generate_content` with a system prompt, auto-deletes uploaded files after response
- `Transcriber` / `Translator` — thin wrappers over `Model` that select the right prompt and processor type (`audio` vs `text`)

**Utils layer** (`utils/`):
- `VideoSplitter` — splits MP4 → MP3 chunks; default chunk size is 20 min; lazy-loads audio via pydub
- `TextWriter` — writes `list[str]` or `dict[str,str]` to a `.txt` file; creates output dir if missing

**Prompts** (`prompts/`):
- `transcription_agent.md` — verbatim English transcription; `[MM:SS]` timestamps; `**Lecturer:**` speaker labels
- `translation_agent.md` — English → Hebrew; preserves formatting; replaces `**Lecturer:**` with `**מרצה:**`

## Known Issues

- `console/session.py` imports use bare module names (`from app_state import AppState`) — only works if the console is run from within `console/`; running from root via `main.py` will fail
- `agents/model.py`: model name is `"gemini-3.5-flash"` — verify this is a valid model ID via `python llm/models.py`
- `console/commands/transcribe_command.py:31`: `_transcribe_audios` is missing `self`; line 42 signature doesn't match its only callsite
- `console/commands/translate_command.py:27`: `_create_translated_data` calls itself recursively (infinite loop)
- `utils/textwriter.py:18`: typo `data.valeues()` → `data.values()`

## Collaboration Rules

- **Suggestion mode**: always suggest code first, do NOT write to files unless the user explicitly confirms
- Follow instructions step by step; wait for confirmation before creating or modifying any file
