const PLACEHOLDER_BARS = Array.from({ length: 48 }, (_, i) =>
  18 + Math.round(Math.abs(Math.sin(i * 0.7)) * 44)
)

interface WaveformProps {
  peaks: number[]
}

export function Waveform({ peaks }: WaveformProps) {
  const bars = peaks.length > 0 ? peaks : PLACEHOLDER_BARS
  return (
    <div className="waveform">
      {bars.map((height, i) => (
        <span
          key={i}
          className="waveform__bar"
          style={{ height: `${height}px` }}
        />
      ))}
    </div>
  )
}
