// frontend/src/api/mock/runStream.ts
import type { Run, Step } from '../../types'

export type RunEventType = 'started' | 'step' | 'finished' | 'error'

export interface RunEvent {
  type: RunEventType
  data: {
    run_id: string
    status?: Run['status']
    step?: Step
    error?: string
  }
}

const ACTIONS = [
  '打开目标页面',
  '等待页面加载完成',
  '识别登录表单',
  '填写用户名',
  '填写密码',
  '点击登录按钮',
  '等待登录响应',
  '验证登录状态',
  '截图保存',
  '检查页面元素',
]

const REASONINGS = [
  'AI 分析：当前页面状态正常，准备执行下一步操作',
  '检测到目标元素，正在进行交互',
  '页面加载中，等待响应...',
  '元素定位成功，准备执行点击操作',
  '表单填写完成，准备提交',
  '验证操作结果，确认执行状态',
]

const SCREENSHOTS = [
  'https://picsum.photos/seed/step1/800/600',
  'https://picsum.photos/seed/step2/800/600',
  'https://picsum.photos/seed/step3/800/600',
  'https://picsum.photos/seed/step4/800/600',
  'https://picsum.photos/seed/step5/800/600',
  'https://picsum.photos/seed/step6/800/600',
  'https://picsum.photos/seed/step7/800/600',
  'https://picsum.photos/seed/step8/800/600',
  'https://picsum.photos/seed/step9/800/600',
  'https://picsum.photos/seed/step10/800/600',
]

export interface MockRunStreamOptions {
  runId: string
  onEvent: (event: RunEvent) => void
  stepCount?: number
  stepInterval?: number
  failureIndex?: number | null
}

export function createMockRunStream(options: MockRunStreamOptions): {
  start: () => void
  stop: () => void
} {
  const {
    runId,
    onEvent,
    stepCount = Math.floor(Math.random() * 6) + 5, // 5-10 步
    stepInterval = 2000,
    failureIndex = Math.random() > 0.8 ? Math.floor(Math.random() * (stepCount - 2)) + 1 : null, // 80% 成功率
  } = options

  let currentStep = 0
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  let stopped = false

  const generateStep = (index: number): Step => {
    const isFailed = failureIndex !== null && index === failureIndex
    return {
      index: index + 1,
      action: ACTIONS[index % ACTIONS.length] || `执行操作 ${index + 1}`,
      reasoning: REASONINGS[index % REASONINGS.length],
      screenshot: SCREENSHOTS[index % SCREENSHOTS.length],
      status: isFailed ? 'failed' : 'success',
      error: isFailed ? '元素定位超时：未找到目标按钮' : undefined,
      duration_ms: Math.floor(Math.random() * 2000) + 500,
    }
  }

  const sendStep = () => {
    if (stopped) return

    if (currentStep === 0) {
      onEvent({
        type: 'started',
        data: { run_id: runId, status: 'running' },
      })
    }

    if (currentStep < stepCount) {
      const step = generateStep(currentStep)
      onEvent({
        type: 'step',
        data: { run_id: runId, step },
      })
      currentStep++
      timeoutId = setTimeout(sendStep, stepInterval)
    } else {
      const finalStatus = failureIndex !== null ? 'failed' : 'success'
      onEvent({
        type: 'finished',
        data: { run_id: runId, status: finalStatus },
      })
    }
  }

  return {
    start: () => {
      stopped = false
      currentStep = 0
      timeoutId = setTimeout(sendStep, 500)
    },
    stop: () => {
      stopped = true
      if (timeoutId) {
        clearTimeout(timeoutId)
        timeoutId = null
      }
      onEvent({
        type: 'finished',
        data: { run_id: runId, status: 'stopped' },
      })
    },
  }
}
