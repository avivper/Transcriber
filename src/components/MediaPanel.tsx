import type { MediaInfo } from '../core/types'
import { Waveform } from './Waveform'
import { MediaControls } from './MediaControls'

interface MediaPanelProps {
  media: MediaInfo | null
}

export function MediaPanel({ media }: MediaPanelProps) {
  return (
    <section className="panel workspace__media">
      <div className="panel__title">Media</div>
      {media ? (
        <>
          <div className="media-meta">
            <span className="media-meta__name">{media.name}</span>
            <span className="media-meta__sub">16 kHz mono · 00:00</span>
          </div>
          <Waveform peaks={media.peaks} />
          <MediaControls />
        </>
      ) : (
        <div className="workspace__empty">
          <span className="workspace__empty-dot" />
          Load a file to preview audio and scrub by timestamp.
        </div>
      )}
    </section>
  )
}
