interface RunControlsProps {
  canRun: boolean
  hasFile: boolean
  onRun: () => void
}

export function RunControls({ canRun, hasFile, onRun }: RunControlsProps) {
  return (
    <div className="action-bar">
      <button
        type="button"
        className="btn btn--primary btn--run"
        disabled={!canRun}
        onClick={onRun}
      >
        Transcribe
      </button>
      <span className="action-bar__hint">
        {hasFile ? 'Ready to process.' : 'Load a file to begin.'}
      </span>
    </div>
  )
}
