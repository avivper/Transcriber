export type StageId = 'decode' | 'segment' | 'transcribe' | 'summarise' | 'export'

export type StageStatus = 'pending' | 'active' | 'done' | 'error'

export interface Stage {
  id: StageId
  name: string
  status: StageStatus
  progress: number
}

export interface TranscriptSegment {
  id: string
  start: number
  end: number
  text: string
}

export interface MediaInfo {
  name: string
  duration: number
  sampleRate: number
  channels: number
  peaks: number[]
}

export type PipelineStatus = 'idle' | 'running' | 'done' | 'error'

export interface PipelineState {
  status: PipelineStatus
  stages: Stage[]
  media: MediaInfo | null
  segments: TranscriptSegment[]
  summary: string | null
  error: string | null
}

export interface Capabilities {
  webGPU: boolean
  crossOriginIsolated: boolean
  whisperCached: boolean
  webLLMModelCached: boolean
}
