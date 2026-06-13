import type { PipelineState, Stage } from './types'

const INITIAL_STAGES: Stage[] = [
  { id: 'decode', name: 'Decode audio', status: 'pending', progress: 0 },
  { id: 'segment', name: 'Segment (VAD)', status: 'pending', progress: 0 },
  { id: 'transcribe', name: 'Transcribe', status: 'pending', progress: 0 },
  { id: 'summarise', name: 'Summarise', status: 'pending', progress: 0 },
  { id: 'export', name: 'Export', status: 'pending', progress: 0 },
]

type Listener = (state: PipelineState) => void

function createInitialState(): PipelineState {
  return {
    status: 'idle',
    stages: INITIAL_STAGES.map((stage) => ({ ...stage })),
    media: null,
    segments: [],
    summary: null,
    error: null,
  }
}

export class PipelineOrchestrator {
  private state: PipelineState = createInitialState()
  private readonly listeners = new Set<Listener>()

  getState(): PipelineState {
    return this.state
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => {
      this.listeners.delete(listener)
    }
  }

  async loadFile(file: File): Promise<void> {
    this.setState({
      ...createInitialState(),
      media: {
        name: file.name,
        duration: 0,
        sampleRate: 16000,
        channels: 1,
        peaks: [],
      },
    })
  }

  async run(): Promise<void> {
    return
  }

  reset(): void {
    this.setState(createInitialState())
  }

  private setState(patch: Partial<PipelineState>): void {
    this.state = { ...this.state, ...patch }
    this.emit()
  }

  private emit(): void {
    for (const listener of this.listeners) {
      listener(this.state)
    }
  }
}
