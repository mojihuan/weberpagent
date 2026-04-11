import { Globe, Hash, Clock, Calendar, UserCircle } from 'lucide-react'
import type { Task } from '../../types'
import { ROLE_LABELS } from '../../constants/roleLabels'

interface TaskInfoProps {
  task: Task
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function TaskInfo({ task }: TaskInfoProps) {
  const infoItems = [
    {
      icon: UserCircle,
      label: '登录角色',
      value: task.login_role ? ROLE_LABELS[task.login_role] || task.login_role : '未指定',
    },
    { icon: Globe, label: '目标 URL', value: task.target_url },
    { icon: Hash, label: '最大步数', value: task.max_steps.toString() },
    { icon: Calendar, label: '创建时间', value: formatDate(task.created_at) },
    { icon: Clock, label: '更新时间', value: formatDate(task.updated_at) },
  ]

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 mb-4">
      <h3 className="text-base font-medium text-gray-900 mb-4">基本信息</h3>
      <div className="grid grid-cols-2 gap-4">
        {infoItems.map(({ icon: Icon, label, value }) => (
          <div key={label} className="flex items-start gap-3">
            <Icon className="w-4 h-4 text-gray-400 mt-0.5" />
            <div>
              <div className="text-sm text-gray-500">{label}</div>
              <div className="text-gray-900 break-all">{value}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
