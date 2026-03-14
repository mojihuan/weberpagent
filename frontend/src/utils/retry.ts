/**
 * Sleep for a specified duration
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Check if an error is a network error (fetch failed)
 */
export function isNetworkError(error: unknown): boolean {
  if (error instanceof TypeError) {
    // Network errors from fetch are TypeErrors
    const message = error.message.toLowerCase()
    return (
      message.includes('failed to fetch') ||
      message.includes('network request failed') ||
      message.includes('networkerror')
    )
  }
  return false
}
