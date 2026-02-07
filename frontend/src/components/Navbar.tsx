'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function Navbar() {
  const { user, logout, isLoading } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    setIsMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link href="/" className="navbar-logo">
          📝 Todo App
        </Link>

        {/* Desktop Navigation */}
        <div className="navbar-desktop-nav">
          {user ? (
            <div className="navbar-authenticated-nav">
              <span className="navbar-user-name">{user.email}</span>
              <button onClick={handleLogout} className="navbar-logout-button">
                Logout
              </button>
            </div>
          ) : (
            <div className="navbar-unauthenticated-nav">
              <Link href="/login" className="navbar-login-link">
                Login
              </Link>
              <Link href="/register" className="navbar-register-button">
                Sign Up
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="navbar-menu-button"
          aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
        >
          ☰
        </button>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="navbar-mobile-nav">
          {user ? (
            <div className="navbar-mobile-authenticated-nav">
              <span className="navbar-mobile-user-name">{user.email}</span>
              <button onClick={handleLogout} className="navbar-mobile-logout-button">
                Logout
              </button>
            </div>
          ) : (
            <div className="navbar-mobile-unauthenticated-nav">
              <Link
                href="/login"
                className="navbar-mobile-login-link"
                onClick={() => setIsMenuOpen(false)}
              >
                Login
              </Link>
              <Link
                href="/register"
                className="navbar-mobile-register-button"
                onClick={() => setIsMenuOpen(false)}
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .navbar {
          background-color: white;
          border-bottom: 1px solid #e2e8f0;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
          position: sticky;
          top: 0;
          z-index: 100;
        }

        .navbar-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          height: 64px;
        }

        .navbar-logo {
          font-size: 20px;
          font-weight: 700;
          color: #2d3748;
          text-decoration: none;
        }

        .navbar-desktop-nav {
          display: flex;
          align-items: center;
          gap: 20px;
        }

        .navbar-authenticated-nav {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .navbar-user-name {
          font-size: 14px;
          color: #4a5568;
        }

        .navbar-logout-button {
          padding: 8px 16px;
          font-size: 14px;
          font-weight: 600;
          color: #e53e3e;
          background-color: transparent;
          border: 2px solid #e53e3e;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .navbar-logout-button:hover {
          background-color: #feebee;
          border-color: #c53030;
          color: #c53030;
        }

        .navbar-unauthenticated-nav {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .navbar-login-link {
          font-size: 16px;
          color: #4a5568;
          text-decoration: none;
          padding: 8px 12px;
          border-radius: 6px;
          transition: all 0.2s;
        }

        .navbar-login-link:hover {
          background-color: #f7fafc;
          color: #2d3748;
        }

        .navbar-register-button {
          padding: 8px 16px;
          font-size: 14px;
          font-weight: 600;
          color: white;
          background-color: #667eea;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .navbar-register-button:hover {
          background-color: #5a67d8;
          transform: translateY(-1px);
        }

        .navbar-menu-button {
          display: none;
          font-size: 24px;
          background: none;
          border: none;
          cursor: pointer;
          color: #4a5568;
        }

        .navbar-mobile-nav {
          display: none;
          background-color: white;
          border-bottom: 1px solid #e2e8f0;
        }

        .navbar-mobile-authenticated-nav {
          display: flex;
          flex-direction: column;
          gap: 12px;
          padding: 16px;
          align-items: flex-start;
        }

        .navbar-mobile-unauthenticated-nav {
          display: flex;
          flex-direction: column;
          gap: 12px;
          padding: 16px;
        }

        .navbar-mobile-user-name {
          font-size: 16px;
          font-weight: 600;
          color: #2d3748;
        }

        .navbar-mobile-logout-button {
          padding: 12px 16px;
          font-size: 14px;
          font-weight: 600;
          color: #e53e3e;
          background-color: transparent;
          border: 2px solid #e53e3e;
          border-radius: 6px;
          cursor: pointer;
          width: 100%;
        }

        .navbar-mobile-logout-button:hover {
          background-color: #feebee;
          border-color: #c53030;
          color: #c53030;
        }

        .navbar-mobile-login-link {
          font-size: 16px;
          color: #4a5568;
          text-decoration: none;
          padding: 12px 16px;
          border-radius: 6px;
          transition: all 0.2s;
          width: 100%;
        }

        .navbar-mobile-login-link:hover {
          background-color: #f7fafc;
          color: #2d3748;
        }

        .navbar-mobile-register-button {
          padding: 12px 16px;
          font-size: 14px;
          font-weight: 600;
          color: white;
          background-color: #667eea;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          width: 100%;
          transition: all 0.2s;
        }

        .navbar-mobile-register-button:hover {
          background-color: #5a67d8;
        }

        @media (max-width: 768px) {
          .navbar-menu-button {
            display: block;
          }

          .navbar-desktop-nav {
            display: none;
          }

          .navbar-mobile-nav {
            display: block;
          }

          .navbar-container {
            justify-content: space-between;
          }
        }
      `}</style>
    </nav>
  );
}