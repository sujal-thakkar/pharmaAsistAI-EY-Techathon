'use client';

import React, { useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Navigation } from '@/components/Navigation';
import { ResultDashboard } from '@/components/ResultDashboard';
import { ChatPanel } from '@/components/ChatPanel';
import { EvidenceGraph } from '@/components/EvidenceGraph';
import { useAppStore } from '@/store/useAppStore';
import { SAMPLE_ANALYSIS_RESULT, SAMPLE_EVIDENCE_NODES, SAMPLE_EVIDENCE_EDGES } from '@/data/mockData';

export default function ResultsPage() {
  const router = useRouter();
  const params = useParams();
  const { currentResult } = useAppStore();
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  
  const result = currentResult || SAMPLE_ANALYSIS_RESULT;
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      {/* Tab Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center gap-1 py-2">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-indigo-50 text-indigo-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('evidence')}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                activeTab === 'evidence'
                  ? 'bg-indigo-50 text-indigo-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              Evidence Graph
            </button>
          </div>
        </div>
      </div>
      
      {/* Content */}
      {activeTab === 'dashboard' ? (
        <ResultDashboard result={result} />
      ) : (
        <div className="max-w-7xl mx-auto px-6 py-8">
          <EvidenceGraph 
            nodes={SAMPLE_EVIDENCE_NODES} 
            edges={SAMPLE_EVIDENCE_EDGES} 
          />
        </div>
      )}
      
      {/* Chat Panel */}
      <ChatPanel 
        isOpen={isChatOpen} 
        onToggle={() => setIsChatOpen(!isChatOpen)}
        moleculeName={result.moleculeData.name}
      />
    </div>
  );
}
