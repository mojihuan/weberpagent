import type { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  title?: string;
  action?: ReactNode;
  className?: string;
}

export function Card({ children, title, action, className = '' }: CardProps) {
  return (
    <div className={`bg-background rounded-lg border border-border ${className}`}>
      {(title || action) && (
        <div className="flex items-center justify-between p-5 border-b border-border">
          {title && <h3 className="font-semibold text-foreground">{title}</h3>}
          {action}
        </div>
      )}
      <div className="p-5">{children}</div>
    </div>
  );
}