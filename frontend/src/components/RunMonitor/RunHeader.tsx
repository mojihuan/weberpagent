import { Square } from 'lucide-react'
import type { Run } from '../../types'
import { Button } from '../Button'
import { StatusBadge } from '../shared'

interface RunHeaderProps {
  taskName: string
  status: Run['status']
  currentStep: number
  totalSteps: number
  onStop: () => void
}

export function RunHeader({
  taskName,
  status,
  currentStep,
  totalSteps,
  onStop,
}: RunHeaderProps) {
  const progress = totalSteps > 0 ? (currentStep / totalSteps) * 100 : 0
  const isRunning = status === 'running'

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-semibold text-gray-900">{taskName}</h1>
          <StatusBadge status={status} />
        </div>
        {isRunning && (
          <Button variant="secondary" onClick={onStop} className="text-red-600 hover:bg-red-50">
            <Square className="w-4 h-4 mr-1" />
            停止执行
          </Button>
        )}
      </div>

      <div className="flex items-center gap-3">
        <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className="h-full bg-blue-500 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-sm text-gray-500 min-w-[60px] text-right">
          {currentStep} / {totalSteps} 步
        </span>
      </div>
    </div>
  )
}
