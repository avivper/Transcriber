import { useCapabilities } from './hooks/useCapabilities'
import { usePipeline } from './hooks/usePipeline'
import { AppHeader } from './components/AppHeader'
import { IsolationAlert } from './components/IsolationAlert'
import { DropZone } from './components/DropZone'
import { RunControls } from './components/RunControls'
import { PipelinePanel } from './components/PipelinePanel'
import { TranscriptPanel } from './components/TranscriptPanel'
import { MediaPanel } from './components/MediaPanel'

export default function App() {
  const caps = useCapabilities()
  const { state, loadFile, run } = usePipeline()

  const blocked = caps != null && !caps.crossOriginIsolated
  const hasFile = state.media != null

  return (
    <div className="app-shell">
      <AppHeader />

      {blocked && <IsolationAlert />}

      <DropZone fileName={state.media?.name ?? null} onFiles={loadFile} />

      <RunControls canRun={hasFile && !blocked} hasFile={hasFile} onRun={run} />

      <PipelinePanel stages={state.stages} />

      <div className="workspace">
        <TranscriptPanel
          segments={state.segments}
          currentTime={0}
          onSeek={() => undefined}
          onExport={() => undefined}
        />
        <MediaPanel media={state.media} />
      </div>
    </div>
  )
}
