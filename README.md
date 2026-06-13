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

> A fully **on-device** lecture transcription web app — decode, transcribe, and
> summarise audio entirely in your browser. **Your audio never leaves your machine.**

---

## Overview

Transcriber turns lecture recordings into structured, timestamped transcripts
**without sending a single byte of audio over the network.** Every stage —
decoding, voice-activity detection, speech recognition, and summarisation — runs
locally in the browser using WebAssembly and WebGPU.

It is built on React 19 + TypeScript + Vite, with the heavy lifting pushed into
Web Workers and a custom C++/WebAssembly DSP module, so the UI stays responsive
while models run on-device.

---

## The Privacy Invariant

This is the whole point of the project, not a footnote:

- **Audio never crosses the network.** Decoding and transcription happen in your
  browser tab.
- The only thing that could ever touch a server is **text** (e.g. an optional
  `/api` endpoint) — never the source media.
- Models are fetched once and cached in the browser's `CacheStorage`; subsequent
  runs are fully offline.

---

## Features

- **100% On-Device Processing**: FFmpeg.wasm, Whisper, and an LLM all run client-side.
- **Timestamped Transcripts**: Segment-level timing with click-to-seek playback.
- **Multi-Stage Pipeline**: Decode → Segment (VAD) → Transcribe → Summarise → Export.
- **WebGPU Acceleration**: Whisper and the summariser use WebGPU when available.
- **Custom C++ DSP**: High-pass filtering, normalization, waveform peaks, and
  voice-activity detection compiled to WebAssembly.
- **Export Options**: Download results as `.txt` or `.pdf`.
- **Wide Format Support**: `mp3 · wav · m4a · mp4 · mov · webm`.
- **Distinctive UI**: A token-driven "Tape Room" design system — a warm, offline
  studio-console aesthetic with self-hosted fonts (no CDN calls).

---

## Pipeline

| # | Stage | Engine |
|---|---|---|
| 1 | **Decode** | FFmpeg.wasm → 16 kHz mono PCM |
| 2 | **Segment (VAD)** | C++/WASM conditioning + voice-activity detection + waveform peaks |
| 3 | **Transcribe** | Whisper (small) via Transformers.js (WebGPU) → timestamped segments |
| 4 | **Summarise** | WebLLM (`Qwen2.5-1.5B`) |
| 5 | **Export** | `.txt` / `.pdf` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **UI** | React 19 + TypeScript + Vite |
| **Audio Decode** | FFmpeg.wasm (`@ffmpeg/ffmpeg`, `@ffmpeg/util`) |
| **Transcription** | Whisper small via Transformers.js (`@huggingface/transformers`) |
| **Summarisation** | WebLLM (`@mlc-ai/web-llm`), `Qwen2.5-1.5B` |
| **DSP / VAD** | C++ → WebAssembly (Emscripten) |
| **Concurrency** | Web Workers bridged via Comlink |
| **Export** | `.txt` + `.pdf` (jsPDF) |
| **Styling** | Token-driven CSS design system ("Tape Room") |

---

## Getting Started

### Prerequisites

- **Node.js** 20+ and **npm**
- A **WebGPU-capable browser** (recent Chrome/Edge recommended)
- *(Optional)* The **Emscripten SDK** — only needed to rebuild the C++/WASM
  audio-processor module

### Installation

```bash
git clone https://github.com/avivper/Transcriber.git
cd Transcriber/transcriber
npm install
```

> All npm/build commands are run from inside the `transcriber/` directory.

### Run the dev server

```bash
npm run dev
```

Then open the printed local URL. The dev server sets the COOP/COEP headers
required for on-device processing (see below).

---

## Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start the Vite dev server (with COOP/COEP headers) |
| `npm run build` | Type-check and build for production (`tsc -b && vite build`) |
| `npm run lint` | Run ESLint over the project |
| `npm run preview` | Preview the production build locally |

---

## Cross-Origin Isolation (Important)

FFmpeg.wasm relies on `SharedArrayBuffer`, which requires the page to be
**cross-origin isolated** (`crossOriginIsolated === true`). That in turn requires
two HTTP response headers:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Because some static hosts (e.g. GitHub Pages) can't set custom headers, isolation
is enforced in **three independent layers**:

1. `vite.config.ts` — dev and preview servers.
2. `vercel.json` — Vercel production.
3. `public/coi-serviceworker.js` — a vendored service worker that injects the
   headers client-side, loaded as the first script in `index.html`.

If isolation is off, the app detects it and surfaces a clear blocking message
instead of failing silently.

---

## Architecture

Transcriber enforces a strict separation between presentation and logic.

- **Hard wall**: components in `src/components/` are **presentational** (props +
  callbacks only). All business logic lives in `src/core/`.
- **Single source of truth**: a `PipelineOrchestrator` owns pipeline state and is
  exposed to React through the `usePipeline` hook.
- **Heavy work in workers**: the `AudioEngine` and `Transcriber` run inside Web
  Workers, bridged via Comlink, so model inference never blocks the UI thread.
- **Native DSP in C++**: the `audio-processor/` module compiles to WebAssembly
  and handles filtering, normalization, waveform peak extraction, and VAD.

### Project Structure

```
transcriber/
├── audio-processor/      # C++ DSP/VAD → WebAssembly (Emscripten)
│   ├── audio_processor.hpp
│   ├── voice_activity_detector.hpp
│   └── ... (biquad, normalizer, peaks, resampler, buffer, types)
├── public/
│   ├── coi-serviceworker.js   # client-side COOP/COEP injection
│   └── fonts/                 # self-hosted woff2 (no CDN)
├── src/
│   ├── components/       # presentational UI (props + callbacks only)
│   ├── core/            # PipelineOrchestrator, engines, types, capabilities
│   ├── hooks/           # React ↔ core bridges (usePipeline, useCapabilities)
│   ├── App.tsx          # composition root
│   └── index.css        # the design system
├── vercel.json          # COOP/COEP headers (production)
└── vite.config.ts       # COOP/COEP headers (dev/preview)
```

---

## Browser Requirements

- **Cross-origin isolation** must be active (handled automatically — see above).
- **WebGPU** is recommended for fast transcription/summarisation; the app falls
  back to WASM where possible.
- Models download once (cached in `CacheStorage`), then run offline.

---

## Project Status

🚧 **Active development.** The UI, design system, and the
components/core/hooks/workers architecture are in place, and the C++ audio-processor
API headers are defined. Engine wiring — FFmpeg decode, Whisper transcription,
WebLLM summarisation, and the C++/WASM build — is being implemented stage by stage.
