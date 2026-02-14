'use client';

import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  tool_calls?: Array<{
    id?: string;
    name?: string;
    arguments?: string;
    function?: {name: string, arguments: string};
  }>;
}

interface ChatProps {
  token: string;
  username: string;
}

export default function ChatComponent({ token, username }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call backend API using username instead of userId
      const response = await sendChatMessage( input, token, conversationId);

      // Update conversation ID if new conversation was created
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Process tool calls for display formatting
      let assistantContent = response.response;
      if (response.tool_calls && response.tool_calls.length > 0) {
        const toolCallsText = response.tool_calls.map(tool_call => {
          // Safely access the function properties with fallbacks
          const functionName = tool_call.function?.name || tool_call.name || 'unknown';
          const functionArgs = tool_call.function?.arguments || tool_call.arguments || '()';
          return `${functionName}(${functionArgs})`;
        }).join(', ');

        // Format as specified: "AI used tools: add_task('buy clothes')"
        assistantContent += `\n\nAI used tools: ${toolCallsText}`;
      }

      // Add assistant response to messages
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: assistantContent,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Add error message to UI
      let errorMessageContent = error.message || 'Sorry, I encountered an error processing your request. Please try again.';

      // Handle specific error codes
      if (error.message && error.message.includes('401')) {
        errorMessageContent = 'Invalid token. Please check your JWT token.';
      } else if (error.message && error.message.includes('404')) {
        errorMessageContent = 'Not found. Please check your username.';
      }

      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'system',
        content: errorMessageContent,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-auto mb-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <p>Start a conversation with the AI assistant!</p>
            <p className="text-sm mt-2">Try: "Add a task to buy groceries" or "Show my tasks"</p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white ml-auto'
                    : message.role === 'assistant'
                      ? 'bg-gray-200 text-gray-800 mr-auto'
                      : 'bg-yellow-100 mr-auto text-sm'
                }`}
              >
                <div>{message.content}</div>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            ))}
            {isLoading && (
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800 mr-auto">
                <p>AI thinking...</p>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t pt-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            placeholder="Type your message..."
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}