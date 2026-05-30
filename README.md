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

> AI-powered lecture transcription and translation — verbatim English output with Hebrew translation, built to help students review university lectures.

---

## Overview

Transcriber takes a video file of a lecture and produces a full verbatim transcription in English, along with a Hebrew translation. It was built to help students review and summarize lectures using LLM agent models powered by the Google Gemini API.

The tool runs as an interactive console session — load your API key, transcribe a video, and translate the result in sequence.

---

## Features

- Splits long video files into audio chunks automatically
- Transcribes speech to English with `[MM:SS]` timestamps and speaker labels
- Translates transcriptions from English to Hebrew, preserving formatting
- Outputs `.txt` files ready for review and study
- Lightweight interactive console — no GUI required

---

## Requirements

- Python 3.11+
- [ffmpeg](https://ffmpeg.org/) installed on your system
- A [Google Gemini API key](https://ai.google.dev/)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/avivper/Transcriber.git
   cd Transcriber
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg**
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu / Debian
   sudo apt install ffmpeg
   ```

4. **Set up your API key** — create a `.env` file in the project root:
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
| `transcribe <path>` | Split the video and transcribe it to English |
| `translate <path>` | Translate a transcription file to Hebrew |
| `exit` | Exit the session |

### Workflow

```
>>> load
API Key loaded successfully!
>>> transcribe lectures/lecture01.mp4
>>> translate output/lecture01.mp4.txt
Created the output at output/lecture01.mp4.txt
```

Output files are saved to the `output/` directory.

---

## Output Format

**English transcription** (`output/<filename>.txt`):
```
## Audio Transcription: lecture01.mp4_part1

---

**Lecturer:** `[00:00]`
Welcome to today's session on operating systems...

**Lecturer:** `[02:15]`
As we discussed last week, the scheduler is responsible for...
```

**Hebrew translation** — same structure with translated content and `**מרצה:**` speaker labels.

---

## Tech Stack

| | |
|---|---|
| [Google Gemini](https://ai.google.dev/) | LLM transcription and translation via Gemini Files API |
| [pydub](https://github.com/jiaaro/pydub) | Audio/video splitting and processing |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment and API key management |
