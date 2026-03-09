export const ENABLE_MOCK = true

export function delay(ms: number = 300) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
