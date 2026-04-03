import { useState } from 'react'
import { ChevronLeft, ChevronRight, ZoomIn, Download } from 'lucide-react'
import type { Step } from '../../types'

interface ScreenshotPanelProps {
  steps: Step[]
  currentViewIndex: number
  onViewChange: (index: number) => void
  onZoom: () => void
}

export function ScreenshotPanel({
  steps,
  currentViewIndex,
  onViewChange,
  onZoom,
}: ScreenshotPanelProps) {
  const [imageLoaded, setImageLoaded] = useState(false)

  const safeIndex = steps.length > 0 ? Math.min(currentViewIndex, steps.length - 1) : -1
  const currentStep = safeIndex >= 0 ? steps[safeIndex] : undefined
  const hasSteps = steps.length > 0 && safeIndex >= 0
  const canGoPrev = currentViewIndex > 0
  const canGoNext = currentViewIndex < steps.length - 1

  const handlePrev = () => {
    if (canGoPrev) {
      setImageLoaded(false)
      onViewChange(currentViewIndex - 1)
    }
  }

  const handleNext = () => {
    if (canGoNext) {
      setImageLoaded(false)
      onViewChange(currentViewIndex + 1)
    }
  }

  const handleDownload = () => {
    if (!currentStep) return
    const link = document.createElement('a')
    link.href = currentStep.screenshot
    link.download = `step-${currentStep.index}.png`
    link.click()
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      <div className="px-4 py-3 border-b border-gray-200 bg-white flex items-center justify-between">
        <h3 className="font-medium text-gray-900">截图预览</h3>
        {hasSteps && (
          <span className="text-sm text-gray-500">
            {currentViewIndex + 1} / {steps.length}
          </span>
        )}
      </div>

      <div className="flex-1 relative flex items-center justify-center p-4">
        {!hasSteps ? (
          <div className="text-gray-400 text-center">
            <p>等待执行开始...</p>
          </div>
        ) : (
          <>
            {!imageLoaded && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
                <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              </div>
            )}
            <img
              src={currentStep!.screenshot}
              alt={`步骤 ${currentStep!.index}`}
              className={`max-w-full max-h-full object-contain rounded-lg shadow-lg transition-opacity ${
                imageLoaded ? 'opacity-100' : 'opacity-0'
              }`}
              onLoad={() => setImageLoaded(true)}
            />

            {/* 左箭头 */}
            <button
              onClick={handlePrev}
              disabled={!canGoPrev}
              className={`absolute left-2 p-2 rounded-full bg-white shadow-md transition ${
                canGoPrev
                  ? 'hover:bg-gray-100 text-gray-700'
                  : 'opacity-50 cursor-not-allowed text-gray-400'
              }`}
            >
              <ChevronLeft className="w-5 h-5" />
            </button>

            {/* 右箭头 */}
            <button
              onClick={handleNext}
              disabled={!canGoNext}
              className={`absolute right-2 p-2 rounded-full bg-white shadow-md transition ${
                canGoNext
                  ? 'hover:bg-gray-100 text-gray-700'
                  : 'opacity-50 cursor-not-allowed text-gray-400'
              }`}
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </>
        )}
      </div>

      {/* 工具栏 */}
      {hasSteps && (
        <div className="px-4 py-2 border-t border-gray-200 bg-white flex items-center justify-center gap-2">
          <button
            onClick={onZoom}
            className="p-2 rounded hover:bg-gray-100 text-gray-600"
            title="放大查看"
          >
            <ZoomIn className="w-5 h-5" />
          </button>
          <button
            onClick={handleDownload}
            className="p-2 rounded hover:bg-gray-100 text-gray-600"
            title="下载截图"
          >
            <Download className="w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  )
}
