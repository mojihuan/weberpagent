/**
 * Login role labels for UI display.
 * Keys match backend AccountService.ROLE_MAP keys (English).
 * Values are Chinese display names per D-01.
 */
export const ROLE_LABELS: Record<string, string> = {
  main: '主账号',
  special: '特殊账号',
  vice: '副账号',
  camera: '摄像头账号',
  platform: '平台账号',
  super: '超级管理员',
  idle: '闲置账号',
} as const

export const ROLE_OPTIONS = [
  { value: '', label: '未指定' },
  ...Object.entries(ROLE_LABELS).map(([value, label]) => ({ value, label })),
]
