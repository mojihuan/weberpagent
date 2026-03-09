// Mock: 启动执行
export async function startRun(taskId: string): Promise<{ runId: string }> {
  // 模拟 API 延迟
  await new Promise(resolve => setTimeout(resolve, 300))

  // 生成随机 runId
  const runId = `r_${Math.random().toString(36).substring(2, 10)}`
  return { runId }
}
