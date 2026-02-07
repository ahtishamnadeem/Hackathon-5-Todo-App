/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './{layout,page}.{js,ts,jsx,tsx}',
    './app/**/{layout,page}.{js,ts,jsx,tsx}',
    // Specific paths for our file structure
    './app/app/**/*.{js,ts,jsx,tsx,mdx}',  // Nested app directory
    './app/chat/**/*.{js,ts,jsx,tsx,mdx}', // Chat directory
    './app/**/**/*.{js,ts,jsx,tsx,mdx}',   // Recursive for any nested directories
    './app/**/**/**/*.{js,ts,jsx,tsx,mdx}', // Even deeper nesting
  ],
  theme: {
    extend: {
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  darkMode: 'class', // Enable dark mode with class strategy
  plugins: [],
}