/**
 * Custom hook for todo state management.
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { todoApi, ApiError } from '@/lib/api';
import type { Todo, TodoFormData } from '@/lib/types';

interface TodoState {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;
}

export function useTodos() {
  const [todoState, setTodoState] = useState<TodoState>({
    todos: [],
    isLoading: false,
    error: null,
  });

  const fetchTodos = useCallback(async () => {
    setTodoState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await todoApi.getAll();
      setTodoState({
        todos: response.data,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Failed to load todos. Please try again.';

      setTodoState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  }, []);

  // Load todos on mount
  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const createTodo = async (formData: TodoFormData) => {
    setTodoState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await todoApi.create(
        formData.title,
        formData.description,
        formData.priority
      );
      const newTodo = response.data;

      setTodoState(prev => ({
        todos: [newTodo, ...prev.todos], // Add to beginning of list (newest first)
        isLoading: false,
        error: null,
      }));

      return { success: true, todo: newTodo };
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Failed to create todo. Please try again.';

      setTodoState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  };

  const getTodo = async (id: number) => {
    try {
      const response = await todoApi.getById(id);
      return response.data;
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Failed to load todo. Please try again.';

      setTodoState(prev => ({
        ...prev,
        error: errorMessage,
      }));

      return null;
    }
  };

  const updateTodo = async (id: number, updates: Partial<Todo>) => {
    setTodoState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await todoApi.update(id, updates);
      const updatedTodo = response.data;

      setTodoState(prev => ({
        todos: prev.todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ),
        isLoading: false,
        error: null,
      }));

      return { success: true, todo: updatedTodo };
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Failed to update todo. Please try again.';

      setTodoState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  };

  const toggleComplete = async (id: number) => {
    setTodoState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Get the current todo directly from the API to determine its state
      const response = await todoApi.getById(id);
      const currentTodo = response.data;

      if (!currentTodo) {
        throw new Error('Todo not found');
      }

      const updateResponse = await todoApi.update(id, { completed: !currentTodo.completed });
      const updatedTodo = updateResponse.data;

      setTodoState(prev => ({
        todos: prev.todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ),
        isLoading: false,
        error: null,
      }));

      return { success: true, todo: updatedTodo };
    } catch (error) {
      const errorMessage = error instanceof Error
        ? error.message
        : 'Failed to update todo status. Please try again.';

      setTodoState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  };

  const deleteTodo = async (id: number) => {
    setTodoState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await todoApi.delete(id);

      setTodoState(prev => ({
        todos: prev.todos.filter(todo => todo.id !== id),
        isLoading: false,
        error: null,
      }));

      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Failed to delete todo. Please try again.';

      setTodoState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  };

  return {
    todos: todoState.todos,
    isLoading: todoState.isLoading,
    error: todoState.error,
    fetchTodos,
    createTodo,
    getTodo,
    updateTodo,
    toggleComplete,
    deleteTodo,
  };
}
