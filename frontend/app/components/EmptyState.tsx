/**
 * Enhanced empty state component with illustration and actions.
 */

'use client';

import { motion } from 'framer-motion';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export default function EmptyState({
  title,
  description,
  icon = '📝',
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="text-center py-12 px-4"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
        className="text-8xl mb-6"
      >
        {icon}
      </motion.div>

      <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">
        {title}
      </h3>

      <p className="text-slate-600 dark:text-slate-400 mb-6 max-w-md mx-auto">
        {description}
      </p>

      {actionLabel && onAction && (
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onAction}
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl"
        >
          {actionLabel}
        </motion.button>
      )}

      <div className="mt-8 space-y-2">
        <p className="text-sm text-slate-500 dark:text-slate-400">💡 Quick tips:</p>
        <ul className="text-sm text-slate-600 dark:text-slate-300 space-y-1">
          <li>• Use the chat assistant to add tasks quickly</li>
          <li>• Press Ctrl+K to open the chat (coming soon)</li>
          <li>• Stay organized and boost your productivity!</li>
        </ul>
      </div>
    </motion.div>
  );
}
