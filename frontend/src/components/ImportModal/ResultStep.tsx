import { useEffect, useRef } from 'react'
import { CheckCircle } from 'lucide-react'

interface ResultStepProps {
  count: number
  onComplete: () => void
}

export function ResultStep({ count, onComplete }: ResultStepProps) {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    timerRef.current = setTimeout(onComplete, 1500)
    return () => {
      if (timerRef.current !== null) {
        clearTimeout(timerRef.current)
      }
    }
  }, [onComplete])

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <CheckCircle className="w-16 h-16 text-green-500" />
      <h3 className="text-lg font-semibold text-gray-900 mt-4">导入完成</h3>
      <p className="text-sm text-gray-500 mt-2">
        已成功创建 {count} 个任务
      </p>
    </div>
  )
}
