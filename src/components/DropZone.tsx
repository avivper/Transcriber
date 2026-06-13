import { useCallback, useRef, useState } from 'react'

interface DropZoneProps {
  fileName: string | null
  onFiles: (file: File) => void
}

export function DropZone({ fileName, onFiles }: DropZoneProps) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFiles = useCallback(
    (files: FileList | null) => {
      const file = files?.[0]
      if (file) onFiles(file)
    },
    [onFiles]
  )

  const open = useCallback(() => inputRef.current?.click(), [])

  return (
    <div
      className={`drop-zone${dragging ? ' drop-zone--active' : ''}`}
      role="button"
      tabIndex={0}
      onClick={open}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          open()
        }
      }}
      onDragOver={(e) => {
        e.preventDefault()
        setDragging(true)
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDragging(false)
        handleFiles(e.dataTransfer.files)
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="audio/*,video/*"
        hidden
        onChange={(e) => handleFiles(e.target.files)}
      />
      <div className="drop-zone__icon">🎧</div>
      <div className="drop-zone__title">
        {fileName ?? 'Drop a lecture file or click to browse'}
      </div>
      <div className="drop-zone__formats">mp3 · wav · m4a · mp4 · mov · webm</div>
    </div>
  )
}
