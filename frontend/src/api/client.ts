import { toast } from 'sonner'
import { sleep, isNetworkError } from '../utils/retry'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:11002/api'
const MAX_RETRIES = 3

export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
  retries = MAX_RETRIES
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      // Try to parse error details from response
      const errorData = await response.json().catch(() => ({}))
      const message = errorData.detail || errorData.error || `API Error: ${response.status}`

      // Show toast for all errors
      toast.error(message, { duration: 5000 })
      throw new ApiError(response.status, message)
    }

    return response.json()
  } catch (error) {
    // Network error - retry with exponential backoff
    if (retries > 0 && isNetworkError(error)) {
      const attempt = MAX_RETRIES - retries + 1
      toast.loading(`网络错误，正在重试... (${attempt}/${MAX_RETRIES})`, { id: 'network-retry' })

      await sleep(1000 * attempt) // Exponential backoff: 1s, 2s, 3s
      return apiClient<T>(endpoint, options, retries - 1)
    }

    toast.dismiss('network-retry')

    // If not a network error and not already shown via toast, show generic error
    if (!isNetworkError(error) && !(error instanceof ApiError)) {
      toast.error('请求失败，请稍后重试', { duration: 5000 })
    }

    throw error
  }
}
