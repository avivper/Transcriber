export function IsolationAlert() {
  return (
    <div className="alert alert--error">
      <span>⚠️</span>
      <div>
        Cross-origin isolation is disabled. FFmpeg.wasm cannot run. Ensure
        COOP/COEP headers are configured, then reload.
      </div>
    </div>
  )
}
