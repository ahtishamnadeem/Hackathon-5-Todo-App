/**
 * Dashboard page - main todo management interface.
 */

'use client';

import { useEffect } from 'react';
import { useTodos } from '@/hooks/useTodos';
import CreateTodoForm from '@/components/CreateTodoForm';
import TodoList from '@/components/TodoList';

export default function DashboardPage() {
  const { todos, isLoading, fetchTodos } = useTodos();

  // Refresh todos when component mounts/reloads
  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Todo Dashboard</h1>
        <p style={styles.subtitle}>Manage your tasks efficiently</p>
      </div>

      <div style={styles.content}>
        <CreateTodoForm onTodoCreated={fetchTodos} />

        <section style={styles.todosSection}>
          <h2 style={styles.sectionTitle}>Your Todos</h2>
          <TodoList todos={todos} isLoading={isLoading} />
        </section>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '40px 20px',
    minHeight: 'calc(100vh - 200px)',
  },
  header: {
    textAlign: 'center' as const,
    marginBottom: '40px',
  },
  title: {
    fontSize: '32px',
    fontWeight: '700',
    color: '#1a202c',
    marginBottom: '8px',
  },
  subtitle: {
    fontSize: '18px',
    color: '#718096',
    margin: 0,
  },
  content: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '40px',
  },
  todosSection: {
    marginTop: '20px',
  },
  sectionTitle: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#2d3748',
    marginBottom: '20px',
  },
};
