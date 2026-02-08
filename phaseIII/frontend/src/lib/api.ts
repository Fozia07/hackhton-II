/**
 * API client for the Todo AI Chatbot backend
 */

interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

interface ChatResponse {
  success: boolean;
  conversation_id: string;
  response: string;
  tool_calls: Array<any>;
  error?: string;
}

/**
 * Send a chat message to the backend API
 */
export async function sendChatMessage(
  message: string,
  token: string,
  conversationId: string | null = null
): Promise<ChatResponse> {
  const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

  const response = await fetch(`${BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Invalid token. Please check your JWT token.');
    } else if (response.status === 403) {
      throw new Error('Not authorized to access chat.');
    } else if (response.status === 404) {
      throw new Error('Chat API endpoint not found.');
    } else {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }

  return response.json();
}

/**
 * Get conversation history
 */
export async function getConversationHistory(
  token: string,
  conversationId: string
): Promise<any[]> {
  const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

  const response = await fetch(`${BASE_URL}/api/conversation/${conversationId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Invalid token. Please check your JWT token.');
    } else if (response.status === 403) {
      throw new Error('Not authorized to access conversation.');
    } else if (response.status === 404) {
      throw new Error('Conversation endpoint not found.');
    } else {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  }

  return response.json();
}
