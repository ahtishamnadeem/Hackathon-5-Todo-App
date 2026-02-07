/**
 * EditTodoForm component for updating existing todos.
 */

import { useState, useEffect } from 'react';
import { useTodos } from '@/hooks/useTodos';
import { Todo } from '@/lib/types';

interface EditTodoFormProps {
  todo: Todo;
  onSave?: () => void;
  onCancel?: () => void;
}

export default function EditTodoForm({ todo, onSave, onCancel }: EditTodoFormProps) {
  const { updateTodo } = useTodos();
  const [formData, setFormData] = useState({
    title: todo.title,
    description: todo.description || '',
  });
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Update form data when todo prop changes
    setFormData({
      title: todo.title,
      description: todo.description || '',
    });
  }, [todo]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    // Validate title
    if (!formData.title.trim()) {
      setError('Title is required');
      setIsLoading(false);
      return;
    }

    try {
      const result = await updateTodo(todo.id, {
        title: formData.title,
        description: formData.description || null,
      });

      if (result.success) {
        if (onSave) {
          onSave();
        }
      } else {
        setError(result.error || 'Failed to update todo');
      }
    } catch (err) {
      setError('An error occurred while updating the todo');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Edit Todo</h3>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label htmlFor="title" style={styles.label}>Title *</label>
          <input
            id="title"
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
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
            name="description"
            value={formData.description}
            onChange={handleChange}
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

        <div style={styles.buttonGroup}>
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            style={{
              ...styles.cancelButton,
              ...(isLoading ? styles.buttonDisabled : {}),
            }}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isLoading}
            style={{
              ...styles.saveButton,
              ...(isLoading ? styles.buttonDisabled : {}),
            }}
          >
            {isLoading ? 'Saving...' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#f7fafc',
    borderRadius: '8px',
    padding: '20px',
    border: '1px solid #e2e8f0',
    maxWidth: '600px',
    margin: '0 auto 16px',
  },
  title: {
    fontSize: '18px',
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
  buttonGroup: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'flex-end',
  },
  cancelButton: {
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#4a5568',
    backgroundColor: 'transparent',
    border: '2px solid #cbd5e0',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  saveButton: {
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#667eea',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
};
