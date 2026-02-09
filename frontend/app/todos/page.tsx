'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useTodos } from '@/hooks/useTodos';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import DarkModeToggle from '../components/DarkModeToggle';
import EmptyState from '../components/EmptyState';
import { TaskListSkeleton } from '../components/SkeletonLoaders';
import ConfirmDialog from '../components/ConfirmDialog';
import PrioritySelector, { PriorityBadge } from '../components/PrioritySelector';

export default function TodosPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const { todos, isLoading, createTodo, toggleComplete, deleteTodo: deleteTodoApi } = useTodos();

  const [newTodo, setNewTodo] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<number | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Check authentication
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const addTodo = async () => {
    if (newTodo.trim()) {
      const result = await createTodo({
        title: newTodo,
        description: description || undefined,
        priority,
      });

      if (result.success) {
        setNewTodo('');
        setDescription('');
        setPriority('medium');
      }
    }
  };

  const handleToggleTodo = async (id: number) => {
    await toggleComplete(id);
  };

  const handleDeleteClick = (id: number) => {
    setTaskToDelete(id);
    setShowDeleteConfirm(true);
  };

  const confirmDelete = async () => {
    if (taskToDelete) {
      await deleteTodoApi(taskToDelete);
      setTaskToDelete(null);
    }
  };

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-600 dark:text-slate-300">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white dark:bg-slate-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                TodoApp
              </Link>
            </div>

            <nav className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link href="/dashboard" className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link href="/todos" className="bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 px-3 py-2 rounded-md text-sm font-medium">
                  My Tasks
                </Link>
              </div>
            </nav>

            <div className="hidden md:flex items-center space-x-2 sm:space-x-4">
              <DarkModeToggle />
              <Link
                href="/dashboard"
                className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-2 sm:px-4 py-2 text-xs sm:text-sm font-medium"
              >
                My Profile
              </Link>
            </div>

            {/* Mobile menu button */}
            <div className="flex md:hidden items-center space-x-2">
              <DarkModeToggle />
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="text-slate-700 dark:text-slate-300 p-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-700"
                aria-label="Toggle menu"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {isMobileMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="md:hidden border-t border-slate-200 dark:border-slate-700 overflow-hidden"
            >
              <div className="px-4 py-3 space-y-2">
                <Link
                  href="/dashboard"
                  className="block text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  href="/todos"
                  className="block bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 px-3 py-2 rounded-md text-sm font-medium"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  My Tasks
                </Link>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-4">
            Your <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Tasks</span>
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-300">
            Manage and organize your daily tasks efficiently
          </p>
        </motion.div>

        {/* Add Todo Form */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 mb-8 border border-slate-200 dark:border-slate-700">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Add New Task</h2>

          <div className="space-y-4">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="What needs to be done?"
              className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500"
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && addTodo()}
            />

            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Description (optional)"
              rows={2}
              className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 resize-none"
            />

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Priority
              </label>
              <PrioritySelector value={priority} onChange={setPriority} />
            </div>

            <button
              onClick={addTodo}
              disabled={isLoading || !newTodo.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-[1.02] shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? 'Adding...' : 'Add Task'}
            </button>
          </div>
        </div>

        {/* Todo List */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 border border-slate-200 dark:border-slate-700">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">
              My Tasks ({todos.length})
            </h2>
          </div>

          {isLoading ? (
            <TaskListSkeleton count={5} />
          ) : todos.length === 0 ? (
            <EmptyState
              title="No tasks yet"
              description="Start organizing your day by adding your first task! Use the form above or ask the AI assistant for help."
              icon="📝"
            />
          ) : (
            <div className="space-y-3">
              {todos.map((todo, index) => (
                <motion.div
                  key={todo.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="flex items-start gap-3 p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600 hover:shadow-md transition-shadow"
                >
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => handleToggleTodo(todo.id)}
                    className="mt-1 w-5 h-5 text-blue-600 bg-slate-100 dark:bg-slate-600 border-slate-300 dark:border-slate-500 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer"
                  />

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3
                        className={`font-medium text-slate-900 dark:text-white ${
                          todo.completed ? 'line-through text-slate-500 dark:text-slate-400' : ''
                        }`}
                      >
                        {todo.title}
                      </h3>
                      <PriorityBadge priority={todo.priority} />
                    </div>

                    {todo.description && (
                      <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                        {todo.description}
                      </p>
                    )}

                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      {new Date(todo.created_at).toLocaleDateString()}
                    </p>
                  </div>

                  <button
                    onClick={() => handleDeleteClick(todo.id)}
                    className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 p-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                    aria-label="Delete task"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        onConfirm={confirmDelete}
        title="Delete Task?"
        message="This action cannot be undone. Are you sure you want to delete this task?"
        confirmLabel="Delete"
        cancelLabel="Cancel"
        type="danger"
      />
    </div>
  );
}
