export function MediaControls() {
  return (
    <div className="media-controls">
      <button type="button" className="btn btn--icon">▶</button>
      <button type="button" className="btn btn--sm">+15s</button>
      <span className="media-controls__time">00:00 / 00:00</span>
    </div>
  )
}
