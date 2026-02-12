'use client';

import { useState, useEffect } from 'react';

export default function DebugPage() {
  const [debugInfo, setDebugInfo] = useState<any>({});
  const [testResult, setTestResult] = useState<string>('');

  useEffect(() => {
    // Gather debug information
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user_data');
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    setDebugInfo({
      hasToken: !!token,
      tokenPreview: token ? `${token.substring(0, 20)}...` : 'No token',
      hasUserData: !!userData,
      userData: userData ? JSON.parse(userData) : null,
      apiUrl: apiUrl,
    });
  }, []);

  const testAuth = async () => {
    setTestResult('Testing...');

    const token = localStorage.getItem('access_token');
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    try {
      const response = await fetch(`${apiUrl}/api/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      setTestResult(JSON.stringify({
        status: response.status,
        ok: response.ok,
        data: data,
      }, null, 2));
    } catch (error) {
      setTestResult(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const testCreateTodo = async () => {
    setTestResult('Testing todo creation...');

    const token = localStorage.getItem('access_token');
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${apiUrl}/api/todos`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'Test Task',
          description: 'Debug test',
          priority: 'medium',
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const data = await response.json();
      setTestResult(JSON.stringify({
        status: response.status,
        ok: response.ok,
        data: data,
      }, null, 2));
    } catch (error) {
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          setTestResult(`Error: Request timed out after 30 seconds. The backend might be sleeping or overloaded.`);
        } else {
          setTestResult(`Error: ${error.message}\n\nThis usually means:\n- Network connection issue\n- Backend is not responding\n- CORS blocking the request\n- Backend crashed\n\nCheck your Hugging Face Space logs.`);
        }
      } else {
        setTestResult(`Unknown error: ${JSON.stringify(error)}`);
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Authentication Debug Page</h1>

        <div className="bg-slate-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Current State</h2>
          <pre className="bg-slate-900 p-4 rounded overflow-auto">
            {JSON.stringify(debugInfo, null, 2)}
          </pre>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Test Authentication</h2>
          <div className="space-x-4 mb-4">
            <button
              onClick={testAuth}
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
            >
              Test /api/auth/me
            </button>
            <button
              onClick={testCreateTodo}
              className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded"
            >
              Test Create Todo
            </button>
          </div>
          {testResult && (
            <pre className="bg-slate-900 p-4 rounded overflow-auto text-sm">
              {testResult}
            </pre>
          )}
        </div>

        <div className="bg-slate-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">Instructions</h2>
          <ol className="list-decimal list-inside space-y-2">
            <li>Check if "hasToken" is true above</li>
            <li>If false, go to /login and log in first</li>
            <li>Click "Test /api/auth/me" to verify authentication</li>
            <li>Click "Test Create Todo" to test task creation</li>
            <li>Share the test results with support</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
