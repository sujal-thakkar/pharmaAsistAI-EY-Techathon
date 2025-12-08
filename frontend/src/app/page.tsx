'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ResearchInput } from '@/components/ResearchInput';
import { useAppStore } from '@/store/useAppStore';
import { AnalysisType } from '@/types';

export default function HomePage() {
  const router = useRouter();
  const startAnalysis = useAppStore((state) => state.startAnalysis);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSubmit = (moleculeName: string, analysisTypes: AnalysisType[]) => {
    setIsLoading(true);
    
    // Start the analysis (this sets currentRequest immediately)
    // Don't await - let it run in the background
    startAnalysis({
      moleculeName,
      analysisTypes,
      additionalContext: ''
    });
    
    // Navigate to the analysis page
    router.push('/analyze');
  };
  
  return (
    <main>
      <ResearchInput onSubmit={handleSubmit} isLoading={isLoading} />
    </main>
  );
}
