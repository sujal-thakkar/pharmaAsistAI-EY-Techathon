/**
 * API Service for connecting to PharmaAssist AI Backend
 */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

// API-specific request types (snake_case to match backend)
export interface AnalysisRequest {
  molecule_name: string;
  analysis_types: string[];  // Required: market, clinical, regulatory, competitive
  additional_context?: string;
}

export interface ChatRequest {
  message: string;
  analysis_id?: string;
  conversation_id?: string;
}

export interface FeedbackRequest {
  message_id: string;
  rating: number;
  feedback_text?: string;
}

/**
 * Helper function for API calls
 */
async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_V1}${endpoint}`;
  
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `API Error: ${response.status}`);
  }

  return response.json();
}

/**
 * Health check (at root, not API v1)
 */
export const healthAPI = {
  async check(): Promise<{
    status: string;
    timestamp: string;
    version: string;
  }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }
};

/**
 * Analysis API
 */
export const analysisAPI = {
  /**
   * Start a new analysis
   */
  async start(request: AnalysisRequest): Promise<{ analysis_id: string; status: string; message: string }> {
    return fetchAPI('/analysis/start', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Get analysis by ID
   */
  async get(analysisId: string): Promise<any> {
    return fetchAPI(`/analysis/${analysisId}`);
  },

  /**
   * Get analysis results
   */
  async getResults(analysisId: string): Promise<any> {
    return fetchAPI(`/analysis/${analysisId}/results`);
  },

  /**
   * Stream analysis progress using SSE
   */
  streamProgress(analysisId: string, onMessage: (data: any) => void, onError?: (error: Error) => void): () => void {
    const eventSource = new EventSource(`${API_V1}/analysis/${analysisId}/stream`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.error('Error parsing SSE data:', e);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      if (onError) {
        onError(new Error('Stream connection error'));
      }
      eventSource.close();
    };

    // Return cleanup function
    return () => eventSource.close();
  },

  /**
   * List all analyses
   */
  async list(limit = 20, offset = 0): Promise<any[]> {
    return fetchAPI(`/analyses?limit=${limit}&offset=${offset}`);
  },
};

/**
 * Chat API
 */
export const chatAPI = {
  /**
   * Send a chat message
   */
  async send(request: ChatRequest): Promise<{
    content: string;
    sources: any[];
    suggested_questions: string[];
    conversation_id: string;
  }> {
    return fetchAPI('/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Stream chat response
   */
  async *streamResponse(request: ChatRequest): AsyncGenerator<string, void, unknown> {
    const response = await fetch(`${API_V1}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Chat stream error: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      yield chunk;
    }
  },

  /**
   * Get conversation history
   */
  async getHistory(conversationId: string): Promise<any> {
    return fetchAPI(`/chat/history/${conversationId}`);
  },

  /**
   * Submit feedback
   */
  async submitFeedback(feedback: FeedbackRequest): Promise<{ success: boolean }> {
    return fetchAPI('/chat/feedback', {
      method: 'POST',
      body: JSON.stringify(feedback),
    });
  },
};

/**
 * Molecules API
 */
export const moleculesAPI = {
  /**
   * List molecules
   */
  async list(params?: {
    page?: number;
    page_size?: number;
    category?: string;
    search?: string;
  }): Promise<any> {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', params.page.toString());
    if (params?.page_size) searchParams.set('page_size', params.page_size.toString());
    if (params?.category) searchParams.set('category', params.category);
    if (params?.search) searchParams.set('search', params.search);
    
    return fetchAPI(`/molecules?${searchParams.toString()}`);
  },

  /**
   * Get molecule by ID
   */
  async get(moleculeId: string): Promise<any> {
    return fetchAPI(`/molecules/${moleculeId}`);
  },

  /**
   * Get molecule categories
   */
  async getCategories(): Promise<any[]> {
    return fetchAPI('/molecules/categories');
  },
};

/**
 * Knowledge Base API
 */
export const knowledgeBaseAPI = {
  /**
   * Get knowledge base status
   */
  async getStatus(): Promise<{
    status: string;
    vectorStore: { count: number; status: string };
    pdfDirectory: { count: number; files: any[] };
  }> {
    return fetchAPI('/knowledge-base/status');
  },

  /**
   * List all PDFs
   */
  async listPDFs(): Promise<{
    count: number;
    files: Array<{
      name: string;
      path: string;
      size: number;
      modified: string;
    }>;
  }> {
    return fetchAPI('/knowledge-base/pdfs');
  },

  /**
   * Search knowledge base
   */
  async search(query: string, nResults = 5): Promise<any> {
    return fetchAPI('/knowledge-base/search', {
      method: 'POST',
      body: JSON.stringify({ query, n_results: nResults }),
    });
  },

  /**
   * Upload a PDF
   */
  async uploadPDF(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_V1}/knowledge-base/upload-pdf`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Failed to upload PDF');
    }
    
    return response.json();
  },
};

/**
 * Analysis History API
 */
export const historyAPI = {
  /**
   * Get all analyses (search history)
   */
  async getAnalyses(limit = 20, offset = 0): Promise<any[]> {
    return fetchAPI(`/analyses?limit=${limit}&offset=${offset}`);
  },
};
