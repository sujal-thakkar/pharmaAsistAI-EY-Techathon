/**
 * React Query hooks for PharmaAssist AI
 */
'use client';

import { useState, useCallback, useEffect } from 'react';
import { analysisAPI, chatAPI, moleculesAPI } from './api';
import type { AnalysisRequest, ChatRequest } from './api';

/**
 * Hook for starting and tracking an analysis
 */
export function useAnalysis() {
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'starting' | 'processing' | 'completed' | 'error'>('idle');
  const [progress, setProgress] = useState(0);
  const [steps, setSteps] = useState<any[]>([]);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const startAnalysis = useCallback(async (request: AnalysisRequest) => {
    try {
      setStatus('starting');
      setError(null);
      setProgress(0);
      setSteps([]);
      setResults(null);

      const response = await analysisAPI.start(request);
      setAnalysisId(response.analysis_id);
      setStatus('processing');

      // Start streaming progress
      const cleanup = analysisAPI.streamProgress(
        response.analysis_id,
        (data) => {
          setProgress(data.progress || 0);
          setSteps(data.steps || []);
          
          if (data.status === 'completed') {
            setStatus('completed');
            setResults(data.results);
          } else if (data.status === 'error') {
            setStatus('error');
            setError(data.error || 'Analysis failed');
          }
        },
        (err) => {
          setStatus('error');
          setError(err.message);
        }
      );

      return { analysisId: response.analysis_id, cleanup };
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'Failed to start analysis');
      return null;
    }
  }, []);

  const reset = useCallback(() => {
    setAnalysisId(null);
    setStatus('idle');
    setProgress(0);
    setSteps([]);
    setResults(null);
    setError(null);
  }, []);

  return {
    analysisId,
    status,
    progress,
    steps,
    results,
    error,
    startAnalysis,
    reset,
  };
}

/**
 * Hook for chat functionality
 */
export function useChat(initialConversationId?: string) {
  const [conversationId, setConversationId] = useState<string | undefined>(initialConversationId);
  const [messages, setMessages] = useState<Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    sources?: any[];
    timestamp: Date;
  }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (message: string, analysisId?: string) => {
    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user' as const,
      content: message,
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatAPI.send({
        message,
        analysis_id: analysisId,
        conversation_id: conversationId,
      });

      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant' as const,
        content: response.content,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);
      setSuggestedQuestions(response.suggested_questions || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  }, [conversationId]);

  const submitFeedback = useCallback(async (messageId: string, rating: number, feedbackText?: string) => {
    try {
      await chatAPI.submitFeedback({
        message_id: messageId,
        rating,
        feedback_text: feedbackText,
      });
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId(undefined);
    setSuggestedQuestions([]);
  }, []);

  return {
    conversationId,
    messages,
    isLoading,
    suggestedQuestions,
    error,
    sendMessage,
    submitFeedback,
    clearMessages,
  };
}

/**
 * Hook for fetching molecules
 */
export function useMolecules(params?: {
  page?: number;
  pageSize?: number;
  category?: string;
  search?: string;
}) {
  const [molecules, setMolecules] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({ page: 1, totalPages: 1, total: 0 });

  const fetchMolecules = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await moleculesAPI.list({
        page: params?.page,
        page_size: params?.pageSize,
        category: params?.category,
        search: params?.search,
      });

      setMolecules(response.items || response);
      if (response.pagination) {
        setPagination(response.pagination);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch molecules');
    } finally {
      setIsLoading(false);
    }
  }, [params?.page, params?.pageSize, params?.category, params?.search]);

  const fetchCategories = useCallback(async () => {
    try {
      const response = await moleculesAPI.getCategories();
      setCategories(response);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
    }
  }, []);

  useEffect(() => {
    fetchMolecules();
    fetchCategories();
  }, [fetchMolecules, fetchCategories]);

  return {
    molecules,
    categories,
    isLoading,
    error,
    pagination,
    refetch: fetchMolecules,
  };
}

/**
 * Hook for fetching analysis history
 */
export function useAnalysisHistory(limit = 20) {
  const [analyses, setAnalyses] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await analysisAPI.list(limit);
      setAnalyses(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch history');
    } finally {
      setIsLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    analyses,
    isLoading,
    error,
    refetch: fetchHistory,
  };
}

/**
 * Hook for fetching a single analysis
 */
export function useAnalysisDetails(analysisId: string | null) {
  const [analysis, setAnalysis] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = useCallback(async () => {
    if (!analysisId) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await analysisAPI.get(analysisId);
      setAnalysis(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analysis');
    } finally {
      setIsLoading(false);
    }
  }, [analysisId]);

  useEffect(() => {
    fetchAnalysis();
  }, [fetchAnalysis]);

  return {
    analysis,
    isLoading,
    error,
    refetch: fetchAnalysis,
  };
}
