/**
 * Priority selector component with visual indicators.
 */

'use client';

interface PrioritySelectorProps {
  value: 'low' | 'medium' | 'high';
  onChange: (priority: 'low' | 'medium' | 'high') => void;
  size?: 'sm' | 'md';
}

export default function PrioritySelector({ value, onChange, size = 'md' }: PrioritySelectorProps) {
  const priorities = [
    { value: 'low' as const, label: 'Low', color: 'bg-green-500', icon: '🟢' },
    { value: 'medium' as const, label: 'Medium', color: 'bg-yellow-500', icon: '🟡' },
    { value: 'high' as const, label: 'High', color: 'bg-red-500', icon: '🔴' },
  ];

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-2 text-sm',
  };

  return (
    <div className="flex gap-2">
      {priorities.map((priority) => (
        <button
          key={priority.value}
          type="button"
          onClick={() => onChange(priority.value)}
          className={`${sizeClasses[size]} rounded-lg font-medium transition-all ${
            value === priority.value
              ? `${priority.color} text-white shadow-lg scale-105`
              : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600'
          }`}
        >
          <span className="mr-1">{priority.icon}</span>
          {priority.label}
        </button>
      ))}
    </div>
  );
}

export function PriorityBadge({ priority }: { priority: 'low' | 'medium' | 'high' }) {
  const config = {
    low: { color: 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400', icon: '🟢', label: 'Low' },
    medium: { color: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400', icon: '🟡', label: 'Medium' },
    high: { color: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400', icon: '🔴', label: 'High' },
  };

  const { color, icon, label } = config[priority];

  return (
    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${color}`}>
      <span className="mr-1">{icon}</span>
      {label}
    </span>
  );
}
