import { useState, useEffect, useCallback } from 'react';
import { apiService, ChatResponse, Thread, ThreadMessage } from '@/services/apiservice';

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: Array<{
    title: string;
    url: string;
    snippet: string;
  }>;
  audioUrl?: string;
  flags?: {
    confidence_score?: number;
    category?: string;
    sentiment?: string;
  };
}

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  currentConversationId: string | null;
  isConnected: boolean;
}

export interface UseChatOptions {
  userId: string;
  language?: string;
}

export const useChat = ({ userId, language = 'en' }: UseChatOptions) => {
  const [state, setState] = useState<ChatState>({
    messages: [
      {
        id: 'welcome',
        text: "Hi! I'm Manny, your SLCM assistant. I can help you with library, cafeteria, admission, hostel, fees, transport, placement, and academic queries. What would you like to know today?",
        sender: 'bot',
        timestamp: new Date(),
      }
    ],
    isLoading: false,
    error: null,
    currentConversationId: null,
    isConnected: false,
  });

  const [threads, setThreads] = useState<Thread[]>([]);

  // Test API connection on mount
  useEffect(() => {
    const testConnection = async () => {
      try {
        const isConnected = await apiService.testConnection();
        setState(prev => ({ ...prev, isConnected }));
        
        if (isConnected) {
          // Load user's existing threads
          try {
            const userThreads = await apiService.getUserThreads(userId);
            setThreads(userThreads);
          } catch (error) {
            console.error('Failed to load threads:', error);
          }
        }
      } catch (error) {
        console.error('Connection test failed:', error);
        setState(prev => ({ 
          ...prev, 
          isConnected: false,
          error: 'Failed to connect to backend server. Please ensure the server is running on http://localhost:8000'
        }));
      }
    };

    testConnection();
  }, [userId]);

  // Load user's threads
  const loadUserThreads = useCallback(async () => {
    try {
      const userThreads = await apiService.getUserThreads(userId);
      setThreads(userThreads);
    } catch (error) {
      console.error('Failed to load threads:', error);
    }
  }, [userId]);

  // Load messages from a specific thread
  const loadThread = useCallback(async (conversationId: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      const threadData = await apiService.getThreadMessages(conversationId);
      
      // Convert backend messages to frontend format
      const convertedMessages: ChatMessage[] = threadData.messages.map((msg: ThreadMessage) => ({
        id: msg.log_id,
        text: msg.sender === 'user' ? msg.user_query : msg.response_text,
        sender: msg.sender === 'assistant' ? 'bot' : msg.sender,
        timestamp: new Date(msg.timestamp),
        sources: msg.sources || undefined,
        audioUrl: msg.tts_audio_path !== 'None' ? apiService.getAudioUrl(msg.tts_audio_path) : undefined,
        flags: 'confidence_score' in msg.flags ? {
          confidence_score: msg.flags.confidence_score,
          category: msg.flags.category,
          sentiment: msg.flags.sentiment,
        } : undefined,
      }));

      setState(prev => ({
        ...prev,
        messages: convertedMessages,
        currentConversationId: conversationId,
        isLoading: false,
      }));
    } catch (error) {
      console.error('Failed to load thread:', error);
      setState(prev => ({
        ...prev,
        error: 'Failed to load conversation thread',
        isLoading: false,
      }));
    }
  }, []);

  // Send a message
  const sendMessage = useCallback(async (messageText: string) => {
    if (!messageText.trim() || state.isLoading || !state.isConnected) {
      return;
    }

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      text: messageText.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      // Send to backend
      const response: ChatResponse = await apiService.sendMessage({
        user_id: userId,
        message: messageText.trim(),
        language,
        ...(state.currentConversationId && { conversation_id: state.currentConversationId }),
      });

      // Create bot response message
      const botMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        sources: response.sources,
        audioUrl: response.tts_audio_url ? apiService.getAudioUrl(response.tts_audio_url) : undefined,
        flags: {
          confidence_score: response.flags.confidence_score,
          category: response.flags.category,
          sentiment: response.flags.sentiment,
        },
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, botMessage],
        currentConversationId: response.conversation_id,
        isLoading: false,
      }));

      // Reload threads to update the list
      await loadUserThreads();

    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        text: '❌ Sorry, I encountered an error. Please try again or check your connection.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isLoading: false,
        error: 'Failed to send message. Please try again.',
      }));
    }
  }, [userId, language, state.isLoading, state.isConnected, state.currentConversationId, loadUserThreads]);

  // Create a new thread/conversation
  const createNewThread = useCallback(async (title?: string) => {
    try {
      const threadTitle = title || `Chat Session ${new Date().toLocaleDateString()}`;
      const newThread = await apiService.createThread(userId, threadTitle);
      
      // Reset chat to new conversation
      setState(prev => ({
        ...prev,
        messages: [
          {
            id: 'welcome-new',
            text: "Hi! I'm Manny, your SLCM assistant. How can I help you today?",
            sender: 'bot',
            timestamp: new Date(),
          }
        ],
        currentConversationId: newThread.conversation_id,
        error: null,
      }));

      // Reload threads
      await loadUserThreads();
      
      return newThread.conversation_id;
    } catch (error) {
      console.error('Failed to create thread:', error);
      setState(prev => ({
        ...prev,
        error: 'Failed to create new conversation',
      }));
      return null;
    }
  }, [userId, loadUserThreads]);

  // Clear current chat (start fresh without creating thread)
  const clearChat = useCallback(() => {
    setState(prev => ({
      ...prev,
      messages: [
        {
          id: 'welcome-clear',
          text: "Chat cleared! I'm Manny, your SLCM assistant. How can I help you today?",
          sender: 'bot',
          timestamp: new Date(),
        }
      ],
      currentConversationId: null,
      error: null,
    }));
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Play TTS audio
  const playAudio = useCallback((audioUrl: string) => {
    try {
      const audio = new Audio(audioUrl);
      audio.play().catch(error => {
        console.error('Failed to play audio:', error);
      });
    } catch (error) {
      console.error('Audio playback error:', error);
    }
  }, []);

  return {
    // State
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    currentConversationId: state.currentConversationId,
    isConnected: state.isConnected,
    threads,
    
    // Actions
    sendMessage,
    loadThread,
    createNewThread,
    clearChat,
    clearError,
    playAudio,
    loadUserThreads,
  };
};
