/**
 * Custom hook for authentication state management.
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { authApi, ApiError } from '@/lib/api';
import { isAuthenticated, clearAuthToken } from '@/lib/auth';
import type { User } from '@/lib/types';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

export function useAuth() {
  const router = useRouter();
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isLoading: true,
    error: null,
  });

  // Check authentication status on mount
  useEffect(() => {
    const checkAuth = () => {
      const authenticated = isAuthenticated();

      if (authenticated && typeof window !== 'undefined') {
        // Get user data from localStorage
        const userDataStr = localStorage.getItem('user_data');
        if (userDataStr) {
          try {
            const userData = JSON.parse(userDataStr);
            setAuthState({
              user: userData,
              isLoading: false,
              error: null,
            });
          } catch (error) {
            console.error('Failed to parse user data:', error);
            setAuthState({
              user: null,
              isLoading: false,
              error: null,
            });
          }
        } else {
          // No user data in localStorage - treat as not authenticated
          setAuthState({
            user: null,
            isLoading: false,
            error: null,
          });
        }
      } else {
        setAuthState({
          user: null,
          isLoading: false,
          error: null,
        });
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response: any = await authApi.login(email, password);
      const user = response.data.user;

      // Store user data in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('user_data', JSON.stringify(user));
      }

      setAuthState({
        user,
        isLoading: false,
        error: null,
      });

      // Redirect to dashboard
      router.push('/dashboard');
      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Login failed. Please try again.';

      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  }, [router]);

  const register = useCallback(async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response: any = await authApi.register(email, password);
      const user = response.data.user;

      // Store user data in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('user_data', JSON.stringify(user));
      }

      setAuthState({
        user,
        isLoading: false,
        error: null,
      });

      // Redirect to dashboard
      router.push('/dashboard');
      return { success: true };
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Registration failed. Please try again.';

      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      return { success: false, error: errorMessage };
    }
  }, [router]);

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      clearAuthToken();
      // Clear user data from localStorage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user_data');
      }
      setAuthState({
        user: null,
        isLoading: false,
        error: null,
      });
      router.push('/login');
    }
  }, [router]);

  return {
    user: authState.user,
    isLoading: authState.isLoading,
    error: authState.error,
    isAuthenticated: !!authState.user,
    login,
    register,
    logout,
  };
}
