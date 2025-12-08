'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AgentLoadingScreen } from '@/components/AgentLoadingScreen';
import { useAppStore } from '@/store/useAppStore';

export default function AnalyzePage() {
  const router = useRouter();
  const [hasRedirected, setHasRedirected] = useState(false);
  const [mounted, setMounted] = useState(false);
  
  const isAnalyzing = useAppStore((state) => state.isAnalyzing);
  const currentResult = useAppStore((state) => state.currentResult);
  const currentRequest = useAppStore((state) => state.currentRequest);
  
  // Wait for component to mount before checking state
  useEffect(() => {
    setMounted(true);
  }, []);
  
  useEffect(() => {
    // Wait for mount and give a small delay for store to sync
    if (!mounted) return;
    
    const timer = setTimeout(() => {
      // If no request and not analyzing after delay, redirect to home
      if (!currentRequest && !isAnalyzing) {
        router.push('/');
      }
    }, 500);
    
    return () => clearTimeout(timer);
  }, [mounted, currentRequest, isAnalyzing, router]);
  
  useEffect(() => {
    // When analysis is complete and we have results, navigate to results page
    if (!isAnalyzing && currentResult && !hasRedirected) {
      setHasRedirected(true);
      router.push(`/results/${currentResult.id}`);
    }
  }, [isAnalyzing, currentResult, router, hasRedirected]);
  
  return (
    <main>
      <AgentLoadingScreen />
    </main>
  );
}
