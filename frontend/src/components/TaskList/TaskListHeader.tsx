import { Plus } from 'lucide-react'
import { Button } from '../Button'

interface TaskListHeaderProps {
  onCreateClick: () => void
}

export function TaskListHeader({ onCreateClick }: TaskListHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">任务管理</h1>
        <p className="text-gray-500 mt-1">创建和管理 UI 自动化测试任务</p>
      </div>
      <Button onClick={onCreateClick}>
        <Plus className="w-4 h-4 mr-1" />
        新建任务
      </Button>
    </div>
  )
}
