'use client';

import { useState, useEffect } from 'react';
import ChatComponent from '../../components/ChatComponent';

export default function ChatPage() {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  // Check authentication on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('jwtToken');
    const savedUsername = localStorage.getItem('username');

    if (savedToken && savedUsername) {
      setToken(savedToken);
      setUsername(savedUsername);
      setIsAuthenticated(true);
    } else {
      // Redirect to login if not authenticated by changing window location
      window.location.href = '/login';
    }

    setIsCheckingAuth(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username');
    setToken(null);
    setUsername(null);
    setIsAuthenticated(false);
    window.location.href = '/login'; // Redirect to login after logout
  };

  // Show nothing while checking authentication
  if (isCheckingAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">Checking authentication...</p>
      </div>
    );
  }

  // If not authenticated, show nothing (redirect handled above)
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm py-4 px-6">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Todo AI Chatbot</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">Username: {username}</span>
            <button
              onClick={handleLogout}
              className="text-sm text-red-600 hover:text-red-800"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 container mx-auto p-4 max-w-4xl">
        <div className="bg-white rounded-lg shadow-md h-[calc(100vh-150px)] flex flex-col">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold">Chat with your AI Assistant</h2>
            <p className="text-sm text-gray-600">Manage your tasks using natural language</p>
          </div>

          <div className="flex-1 overflow-auto p-4">
            <ChatComponent token={token!} username={username!} />
          </div>
        </div>
      </main>
    </div>
  );
}