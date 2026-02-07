/**
 * Public landing page for the Todo application.
 * Shows marketing content to unauthenticated users and redirects authenticated users to dashboard.
 */

'use client';

import { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';

export default function HomePage() {
  const { user, isLoading } = useAuth();

  // Redirect authenticated users to dashboard
  useEffect(() => {
    if (user) {
      // We'll use a programmatic redirect to the dashboard
      window.location.href = '/dashboard';
    }
  }, [user]);

  if (isLoading) {
    return (
      <div style={styles.pageContainer}>
        <div style={styles.loadingSpinner}></div>
        <p style={styles.loadingText}>Checking authentication status...</p>
      </div>
    );
  }

  if (user) {
    // If user is authenticated, show loading while redirecting
    return (
      <div style={styles.pageContainer}>
        <div style={styles.loadingSpinner}></div>
        <p style={styles.loadingText}>Redirecting to dashboard...</p>
      </div>
    );
  }

  // Show public landing page for unauthenticated users
  return (
    <div style={styles.pageContainer}>
      <div style={styles.heroSection}>
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>Stay Organized, Stay Productive</h1>
          <p style={styles.heroSubtitle}>
            A secure, multi-user todo management application with real-time synchronization
          </p>

          <div style={styles.ctaButtons}>
            <Link href="/login" style={styles.loginButton}>
              Login to Account
            </Link>
            <Link href="/register" style={styles.signupButton}>
              Create Account
            </Link>
          </div>
        </div>

        <div style={styles.heroImage}>
          <div style={styles.todoMockup}>
            <div style={styles.todoHeader}>
              <h3>Your Todos</h3>
            </div>
            <div style={styles.todoList}>
              <div style={styles.todoItem}>
                <div style={styles.todoCheckbox}></div>
                <span>Complete project proposal</span>
              </div>
              <div style={styles.todoItem}>
                <div style={styles.todoCheckboxIncomplete}></div>
                <span>Buy groceries</span>
              </div>
              <div style={styles.todoItem}>
                <div style={styles.todoCheckboxIncomplete}></div>
                <span>Schedule team meeting</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={styles.featuresSection}>
        <div style={styles.featuresGrid}>
          <div style={styles.featureCard}>
            <div style={styles.featureIcon}>🔒</div>
            <h3 style={styles.featureTitle}>Secure & Private</h3>
            <p style={styles.featureDescription}>
              Military-grade encryption keeps your tasks safe and private
            </p>
          </div>

          <div style={styles.featureCard}>
            <div style={styles.featureIcon}>📱</div>
            <h3 style={styles.featureTitle}>Always Synced</h3>
            <p style={styles.featureDescription}>
              Access your todos from any device, anywhere
            </p>
          </div>

          <div style={styles.featureCard}>
            <div style={styles.featureIcon}>⚡</div>
            <h3 style={styles.featureTitle}>Lightning Fast</h3>
            <p style={styles.featureDescription}>
              Optimized for speed and performance
            </p>
          </div>
        </div>
      </div>

      <footer style={styles.footer}>
        <p style={styles.footerText}>© 2026 Todo App. All rights reserved.</p>
      </footer>
    </div>
  );
}

const styles = {
  pageContainer: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    display: 'flex',
    flexDirection: 'column' as const,
  },
  heroSection: {
    backgroundColor: 'white',
    padding: '60px 20px',
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    textAlign: 'center' as const,
  },
  heroContent: {
    maxWidth: '800px',
    marginBottom: '40px',
  },
  heroTitle: {
    fontSize: '48px',
    fontWeight: '700',
    color: '#1a202c',
    marginBottom: '16px',
    lineHeight: '1.2',
  },
  heroSubtitle: {
    fontSize: '20px',
    color: '#718096',
    marginBottom: '32px',
    lineHeight: '1.6',
  },
  ctaButtons: {
    display: 'flex',
    gap: '16px',
    justifyContent: 'center' as const,
    flexWrap: 'wrap' as const,
  },
  loginButton: {
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#4a5568',
    backgroundColor: 'white',
    border: '2px solid #cbd5e0',
    borderRadius: '8px',
    textDecoration: 'none',
    transition: 'all 0.2s',
  },
  signupButton: {
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#667eea',
    border: '2px solid #667eea',
    borderRadius: '8px',
    textDecoration: 'none',
    transition: 'all 0.2s',
  },
  heroImage: {
    maxWidth: '800px',
    margin: '40px 0',
  },
  todoMockup: {
    backgroundColor: 'white',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)',
  },
  todoHeader: {
    borderBottom: '1px solid #e2e8f0',
    paddingBottom: '12px',
    marginBottom: '16px',
  },
  todoList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
  },
  todoItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '8px',
    borderRadius: '4px',
  },
  todoCheckbox: {
    width: '20px',
    height: '20px',
    border: '2px solid #48bb78',
    borderRadius: '4px',
    backgroundColor: '#48bb78',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'white',
    fontSize: '12px',
  },
  todoCheckboxIncomplete: {
    width: '20px',
    height: '20px',
    border: '2px solid #cbd5e0',
    borderRadius: '4px',
  },
  featuresSection: {
    padding: '80px 20px',
    backgroundColor: '#f7fafc',
  },
  featuresGrid: {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'grid' as const,
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '30px',
  },
  featureCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    textAlign: 'center' as const,
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
  },
  featureIcon: {
    fontSize: '40px',
    marginBottom: '16px',
  },
  featureTitle: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#2d3748',
    marginBottom: '8px',
  },
  featureDescription: {
    fontSize: '16px',
    color: '#718096',
    lineHeight: '1.6',
  },
  footer: {
    backgroundColor: '#2d3748',
    color: 'white',
    padding: '40px 20px',
    textAlign: 'center' as const,
    marginTop: 'auto',
  },
  footerText: {
    fontSize: '14px',
    color: '#a0aec0',
  },
  loadingSpinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #e2e8f0',
    borderTop: '4px solid #667eea',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    margin: '0 auto 16px',
  },
  loadingText: {
    color: '#718096',
    textAlign: 'center' as const,
  },
};

// Add the spinner animation to the page
if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(style);
}