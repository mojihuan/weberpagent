import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  TestTube,
  Sparkles,
  Play,
  Eye,
  BarChart3,
  RefreshCw,
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: '仪表盘' },
  { to: '/test-cases', icon: TestTube, label: '测试用例' },
  { to: '/ai-generate', icon: Sparkles, label: 'AI生成' },
  { to: '/test-execution', icon: Play, label: '测试执行' },
  { to: '/visual-test', icon: Eye, label: '视觉测试' },
  { to: '/reports', icon: BarChart3, label: '测试报告' },
  { to: '/self-healing', icon: RefreshCw, label: '自愈记录' },
];

export function Sidebar() {
  return (
    <aside className="w-60 h-screen bg-background-secondary border-r border-border flex flex-col">
      {/* Logo */}
      <div className="p-6 flex items-center gap-3">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <span className="font-semibold text-foreground">二手通AI测试</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-2">
        <ul className="space-y-1">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-2.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-primary text-white'
                      : 'text-foreground-secondary hover:bg-background-tertiary hover:text-foreground'
                  }`
                }
              >
                <item.icon className="w-[18px] h-[18px]" />
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* User Info */}
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-primary rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-semibold">U</span>
          </div>
          <div>
            <p className="text-sm font-medium text-foreground">测试用户</p>
            <p className="text-xs text-foreground-muted">test@example.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}