import { type ReactNode } from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  label: string;
  value: string;
  trend?: {
    value: string;
    isPositive: boolean;
  };
  icon: ReactNode;
  iconColor?: string;
}

export function StatCard({ label, value, trend, icon, iconColor = 'text-primary' }: StatCardProps) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-foreground-secondary">{label}</span>
        <div className={iconColor}>{icon}</div>
      </div>
      <div className="text-3xl font-semibold text-foreground mb-2">{value}</div>
      {trend && (
        <div className="flex items-center gap-1">
          {trend.isPositive ? (
            <TrendingUp className="w-3.5 h-3.5 text-success" />
          ) : (
            <TrendingDown className="w-3.5 h-3.5 text-danger" />
          )}
          <span className={trend.isPositive ? 'text-xs text-success' : 'text-xs text-danger'}>
            {trend.value}
          </span>
        </div>
      )}
    </div>
  );
}