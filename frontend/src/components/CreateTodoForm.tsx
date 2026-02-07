/**
 * CreateTodoForm component for adding new todos.
 */

import { useState } from 'react';
import { useTodos } from '@/hooks/useTodos';
import { TodoFormData } from '@/lib/types';

interface CreateTodoFormProps {
  onTodoCreated?: () => void;
}

export default function CreateTodoForm({ onTodoCreated }: CreateTodoFormProps) {
  const { createTodo, isLoading } = useTodos();
  const [formData, setFormData] = useState<TodoFormData>({
    title: '',
    description: '',
  });
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validate title
    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const result = await createTodo(formData);

      if (result.success) {
        // Reset form
        setFormData({ title: '', description: '' });

        // Call callback if provided
        if (onTodoCreated) {
          onTodoCreated();
        }
      } else {
        setError(result.error || 'Failed to create todo');
      }
    } catch (err) {
      setError('An error occurred while creating the todo');
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Add New Todo</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label htmlFor="title" style={styles.label}>Title *</label>
          <input
            id="title"
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            style={styles.input}
            placeholder="What needs to be done?"
            required
            maxLength={500}
          />
        </div>

        <div style={styles.formGroup}>
          <label htmlFor="description" style={styles.label}>Description (optional)</label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            style={{
              ...styles.input,
              minHeight: '80px',
              resize: 'vertical' as const,
            }}
            placeholder="Additional details..."
            maxLength={10000}
          />
        </div>

        {error && (
          <div style={styles.error}>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          style={{
            ...styles.button,
            ...(isLoading ? styles.buttonDisabled : {}),
          }}
        >
          {isLoading ? 'Adding...' : 'Add Todo'}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '24px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
    border: '1px solid #e2e8f0',
    maxWidth: '600px',
    margin: '0 auto 24px',
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#2d3748',
    marginBottom: '16px',
    marginTop: 0,
  },
  form: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '16px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '8px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#4a5568',
  },
  input: {
    padding: '12px 16px',
    fontSize: '16px',
    border: '2px solid #e2e8f0',
    borderRadius: '6px',
    outline: 'none',
  },
  error: {
    padding: '12px',
    backgroundColor: '#fed7d7',
    color: '#c53030',
    borderRadius: '6px',
    fontSize: '14px',
  },
  button: {
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#667eea',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    alignSelf: 'flex-start',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
};
