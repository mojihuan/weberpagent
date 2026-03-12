export const ENABLE_MOCK = false  // 禁用 mock，使用真实后端 API

export function delay(ms: number = 300) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export * from './dashboard'
