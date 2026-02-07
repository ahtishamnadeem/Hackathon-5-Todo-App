/**
 * TodoList component to display a list of todos.
 */

import { Todo } from '@/lib/types';
import TodoItem from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  isLoading?: boolean;
}

export default function TodoList({ todos, isLoading = false }: TodoListProps) {
  if (isLoading) {
    return (
      <div style={styles.loadingContainer}>
        <p>Loading todos...</p>
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <div style={styles.emptyContainer}>
        <p>No todos yet. Add one to get started!</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.list}>
        {todos.map(todo => (
          <TodoItem key={todo.id} todo={todo} />
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    width: '100%',
    maxWidth: '600px',
    margin: '0 auto',
  },
  list: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
  },
  loadingContainer: {
    textAlign: 'center' as const,
    padding: '40px',
    color: '#718096',
  },
  emptyContainer: {
    textAlign: 'center' as const,
    padding: '40px',
    color: '#718096',
    backgroundColor: '#f7fafc',
    borderRadius: '8px',
    border: '1px dashed #e2e8f0',
  },
};
