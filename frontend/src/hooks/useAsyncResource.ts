import { getDict } from '../i18n/i18n'
import { useCallback, useEffect, useRef, useState } from 'react'

export function useAsyncResource<T>(loader: () => Promise<T>, dependencies: unknown[] = []) {
  const mounted = useRef(false)
  const requestId = useRef(0)
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    const currentRequest = ++requestId.current
    setLoading(true)
    setError(null)
    try {
      const result = await loader()
      if (mounted.current && currentRequest === requestId.current) setData(result)
    } catch (reason) {
      if (mounted.current && currentRequest === requestId.current) setError(reason instanceof Error ? reason.message : getDict().common.loadError)
    } finally {
      if (mounted.current && currentRequest === requestId.current) setLoading(false)
    }
  }, dependencies)

  useEffect(() => {
    mounted.current = true
    void load()
    return () => { mounted.current = false; requestId.current += 1 }
  }, [load])

  return { data, loading, error, refetch: load }
}
