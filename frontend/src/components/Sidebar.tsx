import { LayoutDashboard, ListTodo, Play, FileText } from 'lucide-react'
import { NavItem } from './NavItem'

export function Sidebar() {
  return (
    <aside className="w-60 bg-gray-50 p-4 flex flex-col h-screen">
      {/* Logo */}
      <div className="flex items-center gap-3 h-10">
        <div className="w-8 h-8 bg-blue-500 rounded-lg" />
        <span className="text-lg font-semibold text-gray-900">UI Test</span>
      </div>

      {/* Navigation */}
      <nav className="mt-4 space-y-1">
        <NavItem icon={LayoutDashboard} label="仪表盘" to="/" />
        <NavItem icon={ListTodo} label="任务管理" to="/tasks" />
        <NavItem icon={Play} label="执行监控" to="/runs" />
        <NavItem icon={FileText} label="报告查看" to="/reports" />
      </nav>
    </aside>
  )
}
