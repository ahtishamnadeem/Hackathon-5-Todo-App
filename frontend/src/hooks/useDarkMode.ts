/**
 * Custom hook for dark mode management with localStorage persistence.
 */

'use client';

import { useState, useEffect } from 'react';

export function useDarkMode() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Check localStorage on mount - default to dark mode
    const savedTheme = localStorage.getItem('theme');

    // Dark mode is default unless explicitly set to 'light'
    if (savedTheme !== 'light') {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
      // Set default theme in localStorage if not set
      if (!savedTheme) {
        localStorage.setItem('theme', 'dark');
      }
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove('dark');
    }

    setIsLoaded(true);
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode((prev) => {
      const newValue = !prev;

      if (newValue) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }

      return newValue;
    });
  };

  return { isDarkMode, toggleDarkMode, isLoaded };
}
