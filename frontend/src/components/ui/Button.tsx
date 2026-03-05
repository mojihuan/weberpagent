import type { ReactNode } from 'react';

interface ButtonProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  icon?: ReactNode;
  onClick?: () => void;
  className?: string;
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  onClick,
  className = '',
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors';

  const variantStyles = {
    primary: 'bg-primary text-white hover:bg-primary-600',
    secondary: 'bg-background-tertiary text-foreground-secondary hover:bg-border',
    success: 'bg-success text-white hover:bg-green-600',
    danger: 'bg-danger text-white hover:bg-red-600',
    ghost: 'bg-transparent text-foreground-secondary hover:bg-background-tertiary',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  return (
    <button
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
    >
      {icon}
      {children}
    </button>
  );
}