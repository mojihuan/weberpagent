import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { RunHeader, StepTimeline, ScreenshotPanel, ReasoningLog } from '../components/RunMonitor'
import { ImageViewer } from '../components/shared'
import { useRunStream } from '../hooks/useRunStream'
import { mockTasks } from '../api/mock/tasks'

export function RunMonitor() {
  const { id } = useParams<{ id: string }>()

  const { run, disconnect } = useRunStream({
    runId: id || '',
    autoConnect: true,
  })

  const [viewIndex, setViewIndex] = useState(0)
  const [viewerOpen, setViewerOpen] = useState(false)

  // 自动跟随最新步骤
  useEffect(() => {
    if (run?.steps.length) {
      setViewIndex(run.steps.length - 1)
    }
  }, [run?.steps.length])

  const handleStop = () => {
    disconnect()
  }

  const handleStepClick = (index: number) => {
    setViewIndex(index)
  }

  const handleViewChange = (index: number) => {
    setViewIndex(index)
  }

  const handleZoom = () => {
    setViewerOpen(true)
  }

  // 获取任务名称（从 Mock 数据）
  const taskName = run?.task_id
    ? mockTasks.find(t => t.id === run.task_id)?.name || '未知任务'
    : '执行监控'

  const currentStep = run?.steps[viewIndex]

  if (!run) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500">正在连接...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <RunHeader
        taskName={taskName}
        status={run.status}
        currentStep={run.steps.length}
        totalSteps={run.steps.length > 0 ? run.steps.length : 10}
        onStop={handleStop}
      />

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Screenshot */}
        <div className="w-1/2 border-r border-gray-200">
          <ScreenshotPanel
            steps={run.steps}
            currentViewIndex={viewIndex}
            onViewChange={handleViewChange}
            onZoom={handleZoom}
          />
        </div>

        {/* Right: Timeline + Log */}
        <div className="w-1/2 flex flex-col">
          <div className="h-1/2 border-b border-gray-200">
            <StepTimeline
              steps={run.steps}
              currentStepIndex={run.steps.length - 1}
              onStepClick={handleStepClick}
            />
          </div>
          <div className="h-1/2">
            <ReasoningLog steps={run.steps} autoScroll />
          </div>
        </div>
      </div>

      {/* ImageViewer Modal */}
      {currentStep && (
        <ImageViewer
          src={currentStep.screenshot}
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
        />
      )}
    </div>
  )
}
