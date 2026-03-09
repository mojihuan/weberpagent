import { useState } from 'react'
import { ChevronRight, ChevronDown } from 'lucide-react'
import type { Task } from '../../types'

interface ConfigPanelProps {
  task: Task
}

export function ConfigPanel({ task }: ConfigPanelProps) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-white rounded-xl border border-gray-200 mb-4 overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-5 py-4 flex items-center gap-2 hover:bg-gray-50 transition-colors"
      >
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-gray-400" />
        ) : (
          <ChevronRight className="w-4 h-4 text-gray-400" />
        )}
        <span className="font-medium text-gray-900">配置详情</span>
      </button>

      {expanded && (
        <div className="px-5 pb-4 border-t border-gray-100">
          <div className="pt-4 space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">任务 ID</span>
              <span className="text-gray-900 font-mono">{task.id}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">状态</span>
              <span className="text-gray-900">{task.status === 'ready' ? '就绪' : '草稿'}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">超时设置</span>
              <span className="text-gray-900">30 秒/步</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">重试次数</span>
              <span className="text-gray-900">3 次</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">截图保存</span>
              <span className="text-gray-900">开启</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
