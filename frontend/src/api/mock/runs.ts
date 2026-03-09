import type { Run, Step } from '../../types'

function generateSteps(count: number, hasError: boolean): Step[] {
  const actions = [
    '打开目标页面',
    '等待页面加载完成',
    '识别登录表单',
    '填写用户名',
    '填写密码',
    '点击登录按钮',
    '等待登录响应',
    '验证登录状态',
    '截图保存',
  ]

  return Array.from({ length: count }, (_, i) => {
    const isFailed = hasError && i === count - 2
    return {
      index: i + 1,
      action: actions[i % actions.length] || `执行操作 ${i + 1}`,
      reasoning: `AI 分析：当前页面状态正常，准备执行 ${actions[i % actions.length] || `操作 ${i + 1}`}`,
      screenshot: `/screenshots/step-${i + 1}.png`,
      status: isFailed ? 'failed' : 'success',
      error: isFailed ? '元素定位超时：未找到目标按钮' : undefined,
      duration_ms: Math.floor(Math.random() * 3000) + 500,
    }
  })
}

export const mockRuns: Run[] = [
  {
    id: 'r1',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-08T14:30:00Z',
    finished_at: '2026-03-08T14:30:45Z',
    steps: generateSteps(8, false),
  },
  {
    id: 'r2',
    task_id: '1',
    status: 'failed',
    started_at: '2026-03-08T10:15:00Z',
    finished_at: '2026-03-08T10:15:32Z',
    steps: generateSteps(5, true),
  },
  {
    id: 'r3',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-07T16:00:00Z',
    finished_at: '2026-03-07T16:01:15Z',
    steps: generateSteps(9, false),
  },
  {
    id: 'r4',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-06T09:00:00Z',
    finished_at: '2026-03-06T09:00:38Z',
    steps: generateSteps(7, false),
  },
  {
    id: 'r5',
    task_id: '1',
    status: 'success',
    started_at: '2026-03-05T14:00:00Z',
    finished_at: '2026-03-05T14:00:52Z',
    steps: generateSteps(10, false),
  },
  {
    id: 'r6',
    task_id: '2',
    status: 'success',
    started_at: '2026-03-07T11:00:00Z',
    finished_at: '2026-03-07T11:01:20Z',
    steps: generateSteps(12, false),
  },
  {
    id: 'r7',
    task_id: '4',
    status: 'success',
    started_at: '2026-03-05T16:00:00Z',
    finished_at: '2026-03-05T16:02:30Z',
    steps: generateSteps(18, false),
  },
]

export function getTaskStats(taskId: string) {
  const last7Days = ['03/03', '03/04', '03/05', '03/06', '03/07', '03/08', '03/09']

  return last7Days.map(date => {
    const runs = Math.floor(Math.random() * 5) + 1
    const successRate = Math.floor(Math.random() * 40) + 60
    return { date, runs, successRate }
  })
}
