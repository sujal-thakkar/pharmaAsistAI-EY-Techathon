'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';
import { clsx } from 'clsx';

// Button Component
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  icon?: LucideIcon;
  iconPosition?: 'left' | 'right';
  loading?: boolean;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconPosition = 'left',
  loading = false,
  fullWidth = false,
  className,
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500 active:bg-indigo-800',
    secondary: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 hover:border-gray-400 focus:ring-indigo-500',
    ghost: 'bg-transparent text-gray-600 hover:bg-gray-100 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm gap-1.5',
    md: 'px-4 py-2.5 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2.5'
  };
  
  return (
    <button
      className={clsx(
        baseStyles,
        variants[variant],
        sizes[size],
        fullWidth && 'w-full',
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      ) : Icon && iconPosition === 'left' ? (
        <Icon className="w-4 h-4" />
      ) : null}
      {children}
      {!loading && Icon && iconPosition === 'right' && <Icon className="w-4 h-4" />}
    </button>
  );
};

// Card Component
interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  padding = 'md',
  hover = false,
  onClick
}) => {
  const paddings = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };
  
  return (
    <div
      className={clsx(
        'bg-white rounded-xl border border-gray-200 shadow-sm',
        paddings[padding],
        hover && 'hover:shadow-md hover:border-gray-300 transition-all duration-200 cursor-pointer',
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

// Input Component
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  icon?: LucideIcon;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  hint,
  icon: Icon,
  className,
  ...props
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1.5">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon className="h-5 w-5 text-gray-400" />
          </div>
        )}
        <input
          className={clsx(
            'w-full rounded-lg border bg-white px-4 py-2.5 text-sm text-gray-900 placeholder:text-gray-400',
            'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'transition-all duration-200',
            error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300',
            Icon && 'pl-10',
            className
          )}
          {...props}
        />
      </div>
      {hint && !error && (
        <p className="mt-1.5 text-sm text-gray-500">{hint}</p>
      )}
      {error && (
        <p className="mt-1.5 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

// Select Component
interface SelectOption {
  value: string;
  label: string;
  description?: string;
}

interface SelectProps {
  label?: string;
  options: SelectOption[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
}

export const Select: React.FC<SelectProps> = ({
  label,
  options,
  value,
  onChange,
  placeholder = 'Select an option',
  error
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1.5">
          {label}
        </label>
      )}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={clsx(
          'w-full rounded-lg border bg-white px-4 py-2.5 text-sm text-gray-900',
          'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
          'transition-all duration-200 cursor-pointer',
          error ? 'border-red-500' : 'border-gray-300'
        )}
      >
        <option value="" disabled>{placeholder}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1.5 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

// Badge/Pill Component
export interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'primary' | 'info';
  size?: 'sm' | 'md';
  className?: string;
  onClick?: () => void;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  size = 'md',
  className,
  onClick
}) => {
  const variants = {
    default: 'bg-gray-100 text-gray-700',
    success: 'bg-emerald-100 text-emerald-700',
    warning: 'bg-amber-100 text-amber-700',
    error: 'bg-red-100 text-red-700',
    primary: 'bg-indigo-100 text-indigo-700',
    info: 'bg-cyan-100 text-cyan-700'
  };
  
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-xs'
  };
  
  return (
    <span 
      className={clsx(
        'inline-flex items-center font-medium rounded-full',
        variants[variant],
        sizes[size],
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </span>
  );
};

// Progress Bar Component
interface ProgressBarProps {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  color?: 'primary' | 'success' | 'warning' | 'error';
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  size = 'md',
  showLabel = false,
  color = 'primary'
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  
  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3'
  };
  
  const colors = {
    primary: 'bg-indigo-600',
    success: 'bg-emerald-500',
    warning: 'bg-amber-500',
    error: 'bg-red-500'
  };
  
  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between mb-1">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm text-gray-500">{Math.round(percentage)}%</span>
        </div>
      )}
      <div className={clsx('w-full bg-gray-200 rounded-full overflow-hidden', sizes[size])}>
        <div
          className={clsx('h-full rounded-full transition-all duration-500 ease-out', colors[color])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

// Card Header Component
interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, className }) => (
  <div className={clsx('px-6 py-4 border-b border-gray-100', className)}>
    {children}
  </div>
);

// Card Content Component
interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

export const CardContent: React.FC<CardContentProps> = ({ children, className }) => (
  <div className={clsx('p-6', className)}>
    {children}
  </div>
);

// Card Footer Component
interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

export const CardFooter: React.FC<CardFooterProps> = ({ children, className }) => (
  <div className={clsx('px-6 py-4 border-t border-gray-100 bg-gray-50 rounded-b-xl', className)}>
    {children}
  </div>
);

// Glass Card Component
interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
}

export const GlassCard: React.FC<GlassCardProps> = ({ children, className }) => (
  <div className={clsx(
    'bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 shadow-xl',
    className
  )}>
    {children}
  </div>
);

// Metric Card Component
interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: number;
  trendLabel?: string;
  variant?: 'default' | 'success' | 'warning' | 'error';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  trendLabel,
  variant = 'default'
}) => {
  const iconColors = {
    default: 'bg-gray-100 text-gray-600',
    success: 'bg-emerald-100 text-emerald-600',
    warning: 'bg-amber-100 text-amber-600',
    error: 'bg-red-100 text-red-600'
  };
  
  return (
    <Card className="relative overflow-hidden" padding="md">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="mt-2 text-2xl font-bold text-gray-900">{value}</p>
          {subtitle && (
            <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
          )}
          {trend !== undefined && (
            <div className={clsx(
              'mt-2 inline-flex items-center text-sm font-medium',
              trend >= 0 ? 'text-emerald-600' : 'text-red-600'
            )}>
              <span>{trend >= 0 ? '↑' : '↓'}</span>
              <span className="ml-1">{Math.abs(trend)}%</span>
              {trendLabel && <span className="ml-1 text-gray-500 font-normal">{trendLabel}</span>}
            </div>
          )}
        </div>
        {icon && (
          <div className={clsx('p-3 rounded-lg', iconColors[variant])}>
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
};

// Skeleton Loader Component
interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className,
  variant = 'text',
  width,
  height
}) => {
  const variants = {
    text: 'rounded',
    circular: 'rounded-full',
    rectangular: 'rounded-lg'
  };
  
  return (
    <div
      className={clsx(
        'skeleton',
        variants[variant],
        className
      )}
      style={{
        width: width || '100%',
        height: height || (variant === 'text' ? '1em' : 'auto')
      }}
    />
  );
};

// Divider Component
export const Divider: React.FC<{ className?: string }> = ({ className }) => (
  <hr className={clsx('border-t border-gray-200', className)} />
);

// Modal Component
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md'
}) => {
  if (!isOpen) return null;

  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div 
          className={clsx(
            'relative w-full bg-white rounded-2xl shadow-2xl transform transition-all',
            sizes[size]
          )}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          {title && (
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
              <button
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}
          
          {/* Content */}
          <div className="px-6 py-4 max-h-[70vh] overflow-y-auto">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

// Empty State Component
interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  action
}) => (
  <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
    {Icon && (
      <div className="mb-4 p-4 bg-gray-100 rounded-full">
        <Icon className="w-8 h-8 text-gray-400" />
      </div>
    )}
    <h3 className="text-lg font-medium text-gray-900 mb-1">{title}</h3>
    {description && (
      <p className="text-sm text-gray-500 max-w-sm mb-4">{description}</p>
    )}
    {action}
  </div>
);
