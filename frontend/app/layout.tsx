import './globals.css';
import FloatingChatWidget from './components/FloatingChatWidget';

export const metadata = {
  title: 'Todo App – Manage Your Daily Tasks Smartly',
  description: 'A modern, AI-powered todo application to help you stay organized and productive',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-gray-50 dark:bg-slate-900">
        <div className="flex flex-col min-h-screen">
          {children}
        </div>
        <FloatingChatWidget />
      </body>
    </html>
  );
}