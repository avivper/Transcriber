import { useEffect, useState } from 'react'
import { detectCapabilities } from '../core/capabilities'
import type { Capabilities } from '../core/types'

export function useCapabilities(): Capabilities | null {
  const [caps, setCaps] = useState<Capabilities | null>(null)

  useEffect(() => {
    detectCapabilities().then(setCaps)
  }, [])

  return caps
}
