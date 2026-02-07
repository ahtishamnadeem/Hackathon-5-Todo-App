'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
}

export default function TodoDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [todo, setTodo] = useState<Todo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching todo data
    const fetchTodo = () => {
      // In a real app, this would be an API call
      const mockTodo: Todo = {
        id: id,
        title: 'Sample Task Title',
        description: 'This is a sample task description. In a real application, this would come from an API based on the task ID.',
        completed: false,
        createdAt: '2026-02-05',
        updatedAt: '2026-02-05',
        priority: 'medium',
        dueDate: '2026-02-10'
      };

      setTimeout(() => {
        setTodo(mockTodo);
        setLoading(false);
      }, 500);
    };

    fetchTodo();
  }, [id]);

  const toggleTodo = () => {
    if (todo) {
      setTodo({ ...todo, completed: !todo.completed });
    }
  };

  const getPriorityColor = (priority: 'low' | 'medium' | 'high') => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      default: return 'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-slate-600 dark:text-slate-400">Loading task...</p>
        </div>
      </div>
    );
  }

  if (!todo) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Task Not Found</h2>
          <p className="text-slate-600 dark:text-slate-400 mb-4">The task you're looking for doesn't exist.</p>
          <Link
            href="/todos"
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all"
          >
            Back to Tasks
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white dark:bg-slate-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                TodoApp
              </Link>
            </div>

            <nav className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link href="/dashboard" className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link href="/todos" className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium">
                  My Tasks
                </Link>
              </div>
            </nav>

            <div className="flex items-center space-x-4">
              <Link
                href="/dashboard"
                className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-4 py-2 text-sm font-medium"
              >
                My Profile
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
              Task Details
            </h1>
            <Link
              href="/todos"
              className="text-blue-600 dark:text-blue-400 hover:underline text-sm"
            >
              ← Back to Tasks
            </Link>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 border border-slate-200 dark:border-slate-700">
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={toggleTodo}
                  className="h-6 w-6 text-blue-600 rounded focus:ring-blue-500 border-slate-300"
                />
                <h2 className={`ml-4 text-2xl font-bold ${todo.completed ? 'text-slate-500 dark:text-slate-500 line-through' : 'text-slate-900 dark:text-white'}`}>
                  {todo.title}
                </h2>
              </div>

              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(todo.priority)}`}>
                {todo.priority.charAt(0).toUpperCase() + todo.priority.slice(1)} Priority
              </span>
            </div>

            {todo.description && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">Description</h3>
                <p className="text-slate-600 dark:text-slate-300 whitespace-pre-line">
                  {todo.description}
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Created</h3>
                <p className="text-slate-900 dark:text-white">{todo.createdAt}</p>
              </div>

              <div>
                <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Updated</h3>
                <p className="text-slate-900 dark:text-white">{todo.updatedAt}</p>
              </div>

              {todo.dueDate && (
                <div>
                  <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Due Date</h3>
                  <p className="text-slate-900 dark:text-white">{todo.dueDate}</p>
                </div>
              )}

              <div>
                <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Status</h3>
                <p className={`font-medium ${todo.completed ? 'text-green-600 dark:text-green-400' : 'text-orange-600 dark:text-orange-400'}`}>
                  {todo.completed ? 'Completed' : 'Pending'}
                </p>
              </div>
            </div>

            <div className="flex space-x-4 pt-6 border-t border-slate-200 dark:border-slate-700">
              <Link
                href={`/todos/${todo.id}/edit`}
                className="bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 py-2 px-4 rounded-lg font-medium hover:bg-slate-50 dark:hover:bg-slate-600 transition-colors"
              >
                Edit Task
              </Link>

              <button
                onClick={toggleTodo}
                className={`py-2 px-4 rounded-lg font-medium transition-colors ${
                  todo.completed
                    ? 'bg-orange-100 text-orange-800 hover:bg-orange-200 dark:bg-orange-900/30 dark:text-orange-400 dark:hover:bg-orange-800/40'
                    : 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-400 dark:hover:bg-green-800/40'
                }`}
              >
                {todo.completed ? 'Mark as Incomplete' : 'Mark as Complete'}
              </button>

              <button className="bg-red-100 text-red-800 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-800/40 py-2 px-4 rounded-lg font-medium transition-colors">
                Delete Task
              </button>
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}