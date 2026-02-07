/**
 * TypeScript type definitions for the Todo application.
 */

// User types
export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  success: boolean;
  data: {
    message: string;
    token: string;
    user: User;
  };
  error: ErrorDetail | null;
}

// Error types
export interface ErrorDetail {
  code: string;
  message: string;
  details: Record<string, any>;
}

export interface ErrorResponse {
  success: false;
  data: null;
  error: ErrorDetail;
}

// Todo types
export interface Todo {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  updated_at: string;
}

export interface TodoResponse {
  success: boolean;
  data: Todo | Todo[];
  error: ErrorDetail | null;
}

// Form types
export interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword?: string;
}

export interface LoginFormData {
  email: string;
  password: string;
}

export interface TodoFormData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
}
