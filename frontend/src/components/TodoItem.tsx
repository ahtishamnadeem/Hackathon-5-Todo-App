/**
 * TodoItem component to display an individual todo.
 */

import { useState } from 'react';
import { useTodos } from '@/hooks/useTodos';
import { Todo } from '@/lib/types';
import EditTodoForm from './EditTodoForm';

interface TodoItemProps {
  todo: Todo;
}

export default function TodoItem({ todo }: TodoItemProps) {
  const { toggleComplete, deleteTodo } = useTodos();
  const [isEditing, setIsEditing] = useState(false);

  const handleToggleComplete = async () => {
    await toggleComplete(todo.id);
  };

  const handleSave = () => {
    setIsEditing(false);
  };

  return (
    <div style={{
      ...styles.container,
      ...(todo.completed ? styles.completedContainer : {})
    }}>
      {isEditing ? (
        <EditTodoForm
          todo={todo}
          onSave={handleSave}
          onCancel={() => setIsEditing(false)}
        />
      ) : (
        <>
          <div style={styles.row}>
            <div style={styles.checkboxContainer}>
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={handleToggleComplete}
                style={styles.checkbox}
                id={`toggle-${todo.id}`}
              />
              <label htmlFor={`toggle-${todo.id}`} style={styles.checkboxLabel}>
                {todo.completed ? '✓' : '○'}
              </label>
            </div>

            <div style={styles.content}>
              <h3 style={{
                ...styles.title,
                ...(todo.completed ? styles.completedTitle : {})
              }}>
                {todo.title}
              </h3>
              {todo.description && (
                <p style={{
                  ...styles.description,
                  ...(todo.completed ? styles.completedDescription : {})
                }}>
                  {todo.description}
                </p>
              )}
            </div>

            <div style={styles.actions}>
              <button
                onClick={() => setIsEditing(true)}
                style={styles.editButton}
              >
                Edit
              </button>
              <button
                onClick={async () => {
                  if (window.confirm(`Are you sure you want to delete "${todo.title}"?`)) {
                    await deleteTodo(todo.id);
                  }
                }}
                style={styles.deleteButton}
              >
                Delete
              </button>
            </div>
          </div>

          <div style={styles.meta}>
            <span style={styles.status}>
              {todo.completed ? 'Completed' : 'Pending'}
            </span>
            <span style={styles.date}>
              {new Date(todo.created_at).toLocaleDateString()}
            </span>
          </div>
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '16px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
    border: '1px solid #e2e8f0',
  },
  completedContainer: {
    opacity: 0.7,
    backgroundColor: '#f7fafc',
  },
  row: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    marginBottom: '8px',
  },
  checkboxContainer: {
    display: 'flex',
    alignItems: 'center',
    marginTop: '4px',
  },
  checkbox: {
    display: 'none',
  },
  checkboxLabel: {
    display: 'inline-block',
    width: '20px',
    height: '20px',
    border: '2px solid #cbd5e0',
    borderRadius: '4px',
    textAlign: 'center' as const,
    lineHeight: '16px',
    fontSize: '12px',
    cursor: 'pointer',
    userSelect: 'none' as const,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#2d3748',
    margin: 0,
    marginBottom: '4px',
  },
  completedTitle: {
    textDecoration: 'line-through',
    color: '#a0aec0',
  },
  description: {
    fontSize: '14px',
    color: '#718096',
    margin: 0,
    lineHeight: '1.5',
  },
  completedDescription: {
    textDecoration: 'line-through',
    color: '#cbd5e0',
  },
  actions: {
    display: 'flex',
    gap: '8px',
  },
  editButton: {
    padding: '4px 8px',
    fontSize: '12px',
    fontWeight: '600',
    color: '#667eea',
    backgroundColor: 'transparent',
    border: '1px solid #cbd5e0',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  deleteButton: {
    padding: '4px 8px',
    fontSize: '12px',
    fontWeight: '600',
    color: '#e53e3e',
    backgroundColor: 'transparent',
    border: '1px solid #feb2b2',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  meta: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: '12px',
    color: '#a0aec0',
    borderTop: '1px solid #e2e8f0',
    paddingTop: '8px',
    marginTop: '8px',
  },
  status: {
    fontWeight: '500',
  },
  date: {
    fontStyle: 'italic' as const,
  },
};
