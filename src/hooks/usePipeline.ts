import { useEffect, useMemo, useState } from 'react'
import { PipelineOrchestrator } from '../core/PipelineOrchestrator'
import type { PipelineState } from '../core/types'

export interface UsePipeline {
  state: PipelineState
  loadFile: (file: File) => Promise<void>
  run: () => Promise<void>
}

export function usePipeline(): UsePipeline {
  const orchestrator = useMemo(() => new PipelineOrchestrator(), [])
  const [state, setState] = useState<PipelineState>(() => orchestrator.getState())

  useEffect(() => orchestrator.subscribe(setState), [orchestrator])

  return {
    state,
    loadFile: (file) => orchestrator.loadFile(file),
    run: () => orchestrator.run(),
  }
}
