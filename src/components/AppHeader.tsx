export function AppHeader() {
  return (
    <header className="app-header">
      <div className="app-header__brand">
        <div className="app-header__brand-mark">T</div>
        <div className="app-header__titles">
          <h1>Transcriber</h1>
          <span className="app-header__kicker">Lecture transcription</span>
        </div>
      </div>
      <button type="button" className="btn btn--coffee" aria-label="Buy me a coffee">
        <span className="btn__emoji">☕</span>
        Buy me a coffee
      </button>
    </header>
  )
}
