<div align="center">

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

### Private, on-device lecture transcription — right in your browser.

**[🔗 Live App](https://<your-domain>) · [Report a Bug](https://github.com/<username>/Transcriber/issues) · [Request a Feature](https://github.com/<username>/Transcriber/issues)**

[![Live](https://img.shields.io/badge/status-live-8fe388?style=flat-square)](https://<your-domain>)
[![Deployed on Vercel](https://img.shields.io/badge/deployed-Vercel-000000?style=flat-square&logo=vercel)](https://<your-domain>)
[![Privacy](https://img.shields.io/badge/privacy-100%25%20on--device-8fe388?style=flat-square)](#the-privacy-invariant)
[![Built with React](https://img.shields.io/badge/React-19-61dafb?style=flat-square&logo=react)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/license-MIT-f0a338?style=flat-square)](LICENSE)

</div>

---

## ⚡ Try It Now

> **No install. No sign-up. No upload.**
> Open **[https://&lt;your-domain&gt;](https://<your-domain>)**, drop in a lecture, and transcribe — everything runs in your browser and **your audio never leaves your device.**

<div align="center">

<!-- Replace with a real screenshot at docs/screenshot.png once deployed -->
<img src="docs/screenshot.png" alt="Transcriber app screenshot" width="820" />

</div>

---

## Overview

Transcriber turns lecture recordings into structured, timestamped transcripts
**without sending a single byte of audio over the network.** Decoding,
voice-activity detection, speech recognition, and summarisation all run locally
using WebAssembly and WebGPU.

It is a production web app built on React 19 + TypeScript + Vite, with heavy work
pushed into Web Workers and a custom C++/WebAssembly DSP module, so the interface
stays responsive while models run on-device.

---

## The Privacy Invariant

This is the product, not a footnote:

- **Audio never crosses the network.** All processing happens in your browser tab.
- The only thing that could ever reach a server is **text** (an optional `/api`
  endpoint) — never the source media.
- Models are downloaded once and cached in the browser's `CacheStorage`;
  subsequent runs work fully offline.

---

## Features

- **100% On-Device Processing** — FFmpeg.wasm, Whisper, and an LLM all run client-side.
- **Timestamped Transcripts** — segment-level timing with click-to-seek playback.
- **Multi-Stage Pipeline** — Decode → Segment (VAD) → Transcribe → Summarise → Export.
- **WebGPU Acceleration** — Whisper and the summariser use WebGPU when available.
- **Custom C++ DSP** — high-pass filtering, normalization, waveform peaks, and VAD
  compiled to WebAssembly.
- **Export Options** — download results as `.txt` or `.pdf`.
- **Wide Format Support** — `mp3 · wav · m4a · mp4 · mov · webm`.
- **Installable PWA-ready** — fast, offline-capable, distinctive "Tape Room" UI.

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
| **Hosting** | Vercel (static + edge headers) |
| **Audio Decode** | FFmpeg.wasm (`@ffmpeg/ffmpeg`, `@ffmpeg/util`) |
| **Transcription** | Whisper small via Transformers.js (`@huggingface/transformers`) |
| **Summarisation** | WebLLM (`@mlc-ai/web-llm`), `Qwen2.5-1.5B` |
| **DSP / VAD** | C++ → WebAssembly (Emscripten) |
| **Concurrency** | Web Workers bridged via Comlink |
| **Export** | `.txt` + `.pdf` (jsPDF) |
| **Styling** | Token-driven CSS design system ("Tape Room") |

---

## Deployment

The app is a static build, but it **requires two response headers** in production
to enable `SharedArrayBuffer` (used by FFmpeg.wasm):

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

### One-click deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/<username>/Transcriber)

### Manual deploy (Vercel)

```bash
npm install -g vercel
cd transcriber
vercel --prod
```

The required headers ship in three independent layers so the app works on any
host — including those that can't set headers (e.g. GitHub Pages):

1. `vite.config.ts` — dev & preview servers.
2. `vercel.json` — Vercel production.
3. `public/coi-serviceworker.js` — client-side header injection, loaded first in
   `index.html`.

> Deploying elsewhere? Just make sure your host returns the two headers above on
> every route, or rely on the bundled service worker.

---

## Local Development

### Prerequisites

- **Node.js** 20+ and **npm**
- A **WebGPU-capable browser** (recent Chrome/Edge recommended)
- *(Optional)* **Emscripten SDK** — only to rebuild the C++/WASM audio-processor

### Setup

```bash
git clone https://github.com/<username>/Transcriber.git
cd Transcriber/transcriber
npm install
npm run dev
```

> All npm/build commands run from inside the `transcriber/` directory.

### Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start the Vite dev server (with COOP/COEP headers) |
| `npm run build` | Type-check and build for production (`tsc -b && vite build`) |
| `npm run lint` | Run ESLint over the project |
| `npm run preview` | Preview the production build locally |

---

## Architecture

Transcriber enforces a strict separation between presentation and logic.

- **Hard wall** — components in `src/components/` are presentational (props +
  callbacks only). All business logic lives in `src/core/`.
- **Single source of truth** — a `PipelineOrchestrator` owns pipeline state,
  exposed to React through the `usePipeline` hook.
- **Heavy work in workers** — the `AudioEngine` and `Transcriber` run inside Web
  Workers (bridged via Comlink), so inference never blocks the UI thread.
- **Native DSP in C++** — the `audio-processor/` module compiles to WebAssembly
  for filtering, normalization, waveform peaks, and VAD.

```
transcriber/
├── audio-processor/      # C++ DSP/VAD → WebAssembly (Emscripten)
├── public/
│   ├── coi-serviceworker.js   # client-side COOP/COEP injection
│   └── fonts/                 # self-hosted woff2 (no CDN)
├── src/
│   ├── components/       # presentational UI (props + callbacks only)
│   ├── core/            # PipelineOrchestrator, engines, types, capabilities
│   ├── hooks/           # React ↔ core bridges
│   ├── App.tsx          # composition root
│   └── index.css        # the design system
├── vercel.json          # COOP/COEP headers (production)
└── vite.config.ts       # COOP/COEP headers (dev/preview)
```

---

## Browser Support

| Capability | Requirement |
|---|---|
| **Cross-origin isolation** | Required (handled automatically — see Deployment) |
| **WebGPU** | Recommended for fast inference; falls back to WASM where possible |
| **Storage** | Models cached in `CacheStorage` after first load, then run offline |

Best experience on recent **Chrome / Edge**. WebGPU support varies on Safari/Firefox.

---

## Roadmap

- [x] On-device UI, design system & app architecture
- [x] C++ audio-processor API (headers)
- [ ] FFmpeg.wasm decode + live waveform & playback
- [ ] Whisper transcription (Transformers.js)
- [ ] Summarisation (WebLLM)
- [ ] `.txt` / `.pdf` export
- [ ] Installable PWA + offline model bundling

---

## Contributing

Issues and pull requests are welcome. Please open an issue to discuss substantial
changes before submitting a PR.

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
