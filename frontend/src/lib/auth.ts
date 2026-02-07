/**
 * Better Auth configuration for JWT authentication.
 * This file configures the authentication client for the frontend.
 */

// Note: Better Auth integration will be configured here
// For now, we're using a simple token-based approach with our API client

export const AUTH_CONFIG = {
  secret: process.env.BETTER_AUTH_SECRET || '',
  baseUrl: process.env.BETTER_AUTH_URL || 'http://localhost:3000/api/auth',
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
};

/**
 * Check if user is authenticated by verifying token existence.
 */
export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false;
  const token = localStorage.getItem('access_token');
  return !!token;
}

/**
 * Get current authentication token.
 */
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

/**
 * Clear authentication token.
 */
export function clearAuthToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
}
