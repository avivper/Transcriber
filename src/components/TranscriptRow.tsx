import type { TranscriptSegment } from '../core/types'

interface TranscriptRowProps {
  segment: TranscriptSegment
  current: boolean
  onSeek: (time: number) => void
}

function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
  const rest = Math.floor(seconds % 60)
  return `${minutes}:${rest.toString().padStart(2, '0')}`
}

export function TranscriptRow({ segment, current, onSeek }: TranscriptRowProps) {
  return (
    <div className={`transcript-row${current ? ' transcript-row--current' : ''}`}>
      <button
        type="button"
        className="timestamp"
        onClick={() => onSeek(segment.start)}
      >
        {formatTime(segment.start)}
      </button>
      <span>{segment.text}</span>
    </div>
  )
}
