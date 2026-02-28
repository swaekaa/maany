// API Service for Manny Campus Chatbot Backend Integration

const API_BASE_URL = 'http://localhost:8000';

// Types matching the backend API contract
export interface ChatMessage {
  user_id: string;
  message: string;
  language: string;
  conversation_id?: string;
}

export interface Source {
  title: string;
  url: string;
  snippet: string;
}

export interface ResponseFlags {
  contains_personal_info: boolean;
  requires_followup: boolean;
  confidence_score: number;
  category: string;
  language_detected: string;
  sentiment: string;
  response_type: string;
  urgency_level: string;
  topic_continuation: boolean;
  contains_numbers: boolean;
  actionable: boolean;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  sources: Source[];
  language: string;
  flags: ResponseFlags;
  tts_audio_url?: string;
}

export interface Thread {
  conversation_id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ThreadMessage {
  log_id: string;
  sender: 'user' | 'assistant';
  user_query: string;
  response_text: string;
  language: string;
  sources: Source[] | null;
  flags: ResponseFlags | { type: string; safe: boolean };
  timestamp: string;
  tts_audio_path: string;
}

export interface ThreadMessagesResponse {
  conversation_id: string;
  thread_title: string;
  messages: ThreadMessage[];
  total_messages: number;
}

export interface TTSRequest {
  text: string;
  language: string;
  voice?: string;
}

export interface TTSResponse {
  audio_url: string;
  duration: number;
  language: string;
  voice: string;
}

export interface AppInfo {
  app_name: string;
  version: string;
  description: string;
  docs_url: string;
  health_check: string;
  chat_endpoint: string;
  message: string;
}

export interface TTSVoice {
  id: string;
  name: string;
  gender: string;
  sample_url: string;
}

export interface TTSVoicesResponse {
  voices: {
    [language: string]: TTSVoice[];
  };
  note: string;
}

export interface TTSHealthResponse {
  status: string;
  directory_accessible: boolean;
  file_write_ok: boolean;
  tts_directory: string;
  supported_formats: string[];
  supported_languages: string[];
}

export interface TTSTestResponse {
  status: string;
  test_audio_url: string;
  sample_text: string;
  instructions: string;
}

export interface DemoUser {
  user_id: string;
  password: string;
  role: string;
  full_name: string;
}

export interface DemoUsersResponse {
  demo_users: DemoUser[];
  note: string;
}
  user_id: string;
  email: string;
  full_name: string;
  department: string;
  year: number;
  phone: string;
  created_at: string;
  last_login: string;
  conversation_count: number;
}

export interface LoginRequest {
  user_id: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// API Service Class
class ApiService {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('auth_token');
  }

  // Helper method to make HTTP requests
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API Error - ${endpoint}:`, error);
      throw error;
    }
  }

  // Health and Info endpoints
  async ping(): Promise<{ status: string; message: string; version: string }> {
    return this.request('/ping');
  }

  async getInfo(): Promise<any> {
    return this.request('/');
  }

  // Chat endpoints
  async sendMessage(message: ChatMessage): Promise<ChatResponse> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify(message),
    });
  }

  // Thread management endpoints
  async createThread(userId: string, title: string): Promise<{ conversation_id: string; message: string }> {
    return this.request('/api/threads', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, title }),
    });
  }

  async getUserThreads(userId: string): Promise<Thread[]> {
    return this.request(`/api/threads/${userId}`);
  }

  async getThreadMessages(conversationId: string): Promise<ThreadMessagesResponse> {
    return this.request(`/api/threads/${conversationId}/messages`);
  }

  // TTS endpoints
  async generateTTS(request: TTSRequest): Promise<TTSResponse> {
    return this.request('/api/tts/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getTTSVoices(): Promise<any> {
    return this.request('/api/tts/voices');
  }

  async getTTSHealth(): Promise<any> {
    return this.request('/api/tts/health');
  }

  async getTTSTest(): Promise<any> {
    return this.request('/api/tts/test');
  }

  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    // Store token
    this.token = response.access_token;
    localStorage.setItem('auth_token', this.token);
    
    return response;
  }

  async getProfile(): Promise<User> {
    return this.request('/auth/profile');
  }

  async getDemoUsers(): Promise<any> {
    return this.request('/auth/demo-users');
  }

  // Utility methods
  logout() {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  getAudioUrl(audioPath: string): string {
    return `${this.baseUrl}${audioPath}`;
  }

  // Connection test
  async testConnection(): Promise<boolean> {
    try {
      await this.ping();
      return true;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }
}

// Create and export singleton instance
export const apiService = new ApiService();

// Export the class for testing or custom instances
export default ApiService;
