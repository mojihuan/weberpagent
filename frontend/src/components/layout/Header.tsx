import { Search, Bell } from 'lucide-react';
import type { ReactNode } from 'react';

interface HeaderProps {
  title: string;
  subtitle?: string;
  action?: ReactNode;
}

export function Header({ title, subtitle, action }: HeaderProps) {
  return (
    <header className="h-12 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">{title}</h1>
        {subtitle && (
          <p className="text-sm text-foreground-secondary">{subtitle}</p>
        )}
      </div>

      <div className="flex items-center gap-3">
        {action}

        {/* Search */}
        <div className="flex items-center gap-2 w-60 h-9 px-3 bg-background-tertiary rounded-md">
          <Search className="w-4 h-4 text-foreground-muted" />
          <input
            type="text"
            placeholder="搜索测试用例..."
            className="flex-1 bg-transparent text-sm text-foreground placeholder:text-foreground-muted focus:outline-none"
          />
        </div>

        {/* Notifications */}
        <button className="w-9 h-9 flex items-center justify-center bg-background-tertiary rounded-md hover:bg-border transition-colors">
          <Bell className="w-[18px] h-[18px] text-foreground-secondary" />
        </button>

        {/* Avatar */}
        <div className="w-9 h-9 bg-primary rounded-full flex items-center justify-center">
          <span className="text-white text-sm font-semibold">U</span>
        </div>
      </div>
    </header>
  );
}