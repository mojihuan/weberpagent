import type { Task } from '../../types'
import { TaskRow } from './TaskRow'

interface TaskTableProps {
  tasks: Task[]
  selectedIds: string[]
  onSelectAll: () => void
  onToggleSelect: (id: string) => void
  onEdit: (task: Task) => void
  onDelete: (task: Task) => void
}

export function TaskTable({
  tasks,
  selectedIds,
  onSelectAll,
  onToggleSelect,
  onEdit,
  onDelete,
}: TaskTableProps) {
  const allSelected = tasks.length > 0 && selectedIds.length === tasks.length
  const someSelected = selectedIds.length > 0 && selectedIds.length < tasks.length

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-4 py-3 text-left">
              <input
                type="checkbox"
                checked={allSelected}
                ref={el => {
                  if (el) el.indeterminate = someSelected
                }}
                onChange={onSelectAll}
                className="w-4 h-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500"
              />
            </th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">名称</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">目标 URL</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">状态</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">步数</th>
            <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(task => (
            <TaskRow
              key={task.id}
              task={task}
              selected={selectedIds.includes(task.id)}
              onSelect={() => onToggleSelect(task.id)}
              onEdit={() => onEdit(task)}
              onDelete={() => onDelete(task)}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}
