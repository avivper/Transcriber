import type { TranscriptSegment } from '../core/types'
import { TranscriptRow } from './TranscriptRow'

interface TranscriptPanelProps {
  segments: TranscriptSegment[]
  currentTime: number
  onSeek: (time: number) => void
  onExport: (format: 'txt' | 'pdf') => void
}

export function TranscriptPanel({
  segments,
  currentTime,
  onSeek,
  onExport,
}: TranscriptPanelProps) {
  const hasResult = segments.length > 0

  return (
    <section className="panel workspace__transcript">
      <div className="panel__header">
        <div className="panel__title">Transcript</div>
        <div className="panel__actions">
          <button
            type="button"
            className="btn btn--sm"
            disabled={!hasResult}
            onClick={() => onExport('txt')}
          >
            Download .txt
          </button>
          <button
            type="button"
            className="btn btn--sm"
            disabled={!hasResult}
            onClick={() => onExport('pdf')}
          >
            Download .pdf
          </button>
        </div>
      </div>
      {hasResult ? (
        <div className="transcript">
          {segments.map((segment) => (
            <TranscriptRow
              key={segment.id}
              segment={segment}
              current={currentTime >= segment.start && currentTime < segment.end}
              onSeek={onSeek}
            />
          ))}
        </div>
      ) : (
        <div className="workspace__empty">
          <span className="workspace__empty-dot" />
          Your timestamped transcript will appear here.
        </div>
      )}
    </section>
  )
}
