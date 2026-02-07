/**
 * API client for communicating with the backend.
 * Handles authentication, error responses, and request formatting.
 */

import type { ErrorResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public details: Record<string, any> = {}
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Make an API request with automatic error handling.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  // Get token from localStorage if available
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    credentials: 'include', // Include cookies for httpOnly tokens
  };

  try {
    const response = await fetch(url, config);

    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new ApiError(
        'INVALID_RESPONSE',
        `Expected JSON response but got ${contentType}`,
        { status: response.status }
      );
    }

    const data = await response.json();

    // Handle error responses
    if (!response.ok || !data.success) {
      const errorData = data as ErrorResponse;
      throw new ApiError(
        errorData.error?.code || 'UNKNOWN_ERROR',
        errorData.error?.message || 'An error occurred',
        errorData.error?.details || {}
      );
    }

    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    // Network or other errors
    throw new ApiError(
      'NETWORK_ERROR',
      error instanceof Error ? error.message : 'An unexpected error occurred',
      {}
    );
  }
}

// Authentication API
export const authApi = {
  async register(email: string, password: string) {
    const response = await apiRequest('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    // Store token in localStorage
    if (response.data?.token) {
      localStorage.setItem('access_token', response.data.token);
    }

    return response;
  },

  async login(email: string, password: string) {
    const response = await apiRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    // Store token in localStorage
    if (response.data?.token) {
      localStorage.setItem('access_token', response.data.token);
    }

    return response;
  },

  async logout() {
    const response = await apiRequest('/api/auth/logout', {
      method: 'POST',
    });

    // Clear token from localStorage
    localStorage.removeItem('access_token');

    return response;
  },

  async getCurrentUser() {
    return apiRequest('/api/auth/me', {
      method: 'GET',
    });
  },
};

// Todo API
export const todoApi = {
  async getAll() {
    return apiRequest('/api/todos', {
      method: 'GET',
    });
  },

  async getById(id: number) {
    return apiRequest(`/api/todos/${id}`, {
      method: 'GET',
    });
  },

  async create(
    title: string,
    description?: string,
    priority?: 'low' | 'medium' | 'high'
  ) {
    return apiRequest('/api/todos', {
      method: 'POST',
      body: JSON.stringify({
        title,
        description,
        priority: priority || 'medium',
      }),
    });
  },

  async update(
    id: number,
    data: {
      title?: string;
      description?: string;
      completed?: boolean;
      priority?: 'low' | 'medium' | 'high';
    }
  ) {
    return apiRequest(`/api/todos/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  async delete(id: number) {
    return apiRequest(`/api/todos/${id}`, {
      method: 'DELETE',
    });
  },
};
