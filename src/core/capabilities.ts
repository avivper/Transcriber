import type { Capabilities } from './types'

async function checkCacheStorage(key: string): Promise<boolean> {
  if (!('caches' in window)) return false
  try {
    const names = await caches.keys()
    return names.some((name) => name.includes(key))
  } catch {
    return false
  }
}

export async function detectCapabilities(): Promise<Capabilities> {
  return {
    webGPU: !!navigator.gpu,
    crossOriginIsolated: crossOriginIsolated,
    whisperCached: await checkCacheStorage('whisper-small'),
    webLLMModelCached: await checkCacheStorage('Qwen2.5-1.5B'),
  }
}
