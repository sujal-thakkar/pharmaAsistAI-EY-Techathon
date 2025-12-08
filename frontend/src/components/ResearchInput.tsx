'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, 
  Mic, 
  MicOff, 
  Sparkles, 
  FlaskConical, 
  TrendingUp, 
  FileSearch,
  ArrowRight,
  Loader2,
  X,
  BarChart3
} from 'lucide-react';
import { Button, Badge } from '@/components/ui';
import { AnalysisType } from '@/types';

interface ResearchInputProps {
  onSubmit: (moleculeName: string, analysisTypes: AnalysisType[]) => void;
  isLoading?: boolean;
}

const analysisOptions: { type: AnalysisType; label: string; icon: React.ElementType; description: string }[] = [
  { 
    type: 'market', 
    label: 'Market Intelligence', 
    icon: TrendingUp,
    description: 'Market size, growth projections, competitive landscape'
  },
  { 
    type: 'clinical', 
    label: 'Clinical Trials', 
    icon: FlaskConical,
    description: 'Active trials, phases, efficacy data, outcomes'
  },
  { 
    type: 'regulatory', 
    label: 'Regulatory Status', 
    icon: FileSearch,
    description: 'FDA approvals, EMA status, patent expiry'
  },
  { 
    type: 'competitive', 
    label: 'Competitive Analysis', 
    icon: BarChart3,
    description: 'Competitor drugs, market share, pipeline comparison'
  }
];

const suggestedMolecules = [
  'Aspirin',
  'Metformin',
  'Ozempic',
  'Wegovy',
  'Humira',
  'Keytruda',
  'Lipitor',
  'Omeprazole'
];

export const ResearchInput: React.FC<ResearchInputProps> = ({ onSubmit, isLoading = false }) => {
  const [query, setQuery] = useState('');
  const [selectedTypes, setSelectedTypes] = useState<AnalysisType[]>(['market', 'clinical', 'regulatory', 'competitive']);
  const [isListening, setIsListening] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Speech recognition
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  
  useEffect(() => {
    if (typeof window !== 'undefined' && ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      
      recognitionRef.current.onresult = (event: SpeechRecognitionEvent) => {
        const transcript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        setQuery(transcript);
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
    
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);
  
  const toggleListening = () => {
    if (!recognitionRef.current) return;
    
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };
  
  const toggleAnalysisType = (type: AnalysisType) => {
    setSelectedTypes(prev => 
      prev.includes(type)
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && selectedTypes.length > 0) {
      onSubmit(query.trim(), selectedTypes);
    }
  };
  
  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
    inputRef.current?.focus();
  };
  
  const filteredSuggestions = suggestedMolecules.filter(
    mol => mol.toLowerCase().includes(query.toLowerCase()) && query.length > 0
  );
  
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <img
              src="/pharmaAssist-logo.png"
              alt="PharmaAssist AI"
              className="h-10 w-auto object-contain"
            />
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="success">Beta</Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-2xl"
        >
          {/* Hero Section */}
          <div className="text-center mb-10">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
              className="inline-flex items-center justify-center gap-4 mb-6"
            >
              <img
                src="/pharmaAssist-logo.png"
                alt="PharmaAssist AI"
                className="h-16 w-auto object-contain"
              />
              <div className="w-16 h-16 rounded-2xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-600/25">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
            </motion.div>
            <h1 className="text-3xl font-bold text-gray-900 mb-3">
              Pharmaceutical Intelligence Platform
            </h1>
            <p className="text-base text-gray-600 max-w-md mx-auto leading-relaxed">
              Get comprehensive drug insights powered by multi-agent AI research and real-time data analysis.
            </p>
          </div>
          
          {/* Search Card */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
            <form onSubmit={handleSubmit}>
              {/* Search Input */}
              <div className="relative mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter Molecule or Drug Name
                </label>
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    ref={inputRef}
                    type="text"
                    value={query}
                    onChange={(e) => {
                      setQuery(e.target.value);
                      setShowSuggestions(true);
                    }}
                    onFocus={() => setShowSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    placeholder="e.g., Aspirin, Metformin, Ozempic..."
                    className="w-full pl-12 pr-20 py-3.5 text-base bg-gray-50 border border-gray-300 rounded-xl focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-500/20 transition-all outline-none"
                    disabled={isLoading}
                  />
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                    {query && (
                      <button
                        type="button"
                        onClick={() => setQuery('')}
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={toggleListening}
                      className={`p-2 rounded-lg transition-all ${
                        isListening 
                          ? 'bg-red-100 text-red-500' 
                          : 'text-gray-400 hover:text-indigo-600 hover:bg-indigo-50'
                      }`}
                      disabled={isLoading}
                      title={isListening ? 'Stop listening' : 'Voice input'}
                    >
                      {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                    </button>
                  </div>
                </div>
                
                {/* Suggestions Dropdown */}
                <AnimatePresence>
                  {showSuggestions && filteredSuggestions.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: -8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="absolute z-20 w-full mt-2 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden"
                    >
                      {filteredSuggestions.map((suggestion) => (
                        <button
                          key={suggestion}
                          type="button"
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors flex items-center gap-3 border-b border-gray-100 last:border-b-0"
                        >
                          <FlaskConical className="w-4 h-4 text-indigo-500" />
                          <span className="text-gray-700">{suggestion}</span>
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              
              {/* Analysis Type Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Analysis Types <span className="text-gray-400 font-normal">({selectedTypes.length} of {analysisOptions.length} selected)</span>
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {analysisOptions.map((option) => {
                    const Icon = option.icon;
                    const isSelected = selectedTypes.includes(option.type);
                    
                    return (
                      <button
                        key={option.type}
                        type="button"
                        onClick={() => toggleAnalysisType(option.type)}
                        disabled={isLoading}
                        className={`flex items-start gap-3 p-4 rounded-xl border-2 transition-all text-left ${
                          isSelected
                            ? 'border-indigo-500 bg-indigo-50'
                            : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        <div className={`shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${
                          isSelected ? 'bg-indigo-600' : 'bg-gray-100'
                        }`}>
                          <Icon className={`w-5 h-5 ${isSelected ? 'text-white' : 'text-gray-500'}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <span className={`block font-medium text-sm ${isSelected ? 'text-indigo-900' : 'text-gray-800'}`}>
                            {option.label}
                          </span>
                          <p className="text-xs text-gray-500 mt-0.5 leading-relaxed">{option.description}</p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
              
              {/* Submit Button */}
              <Button
                type="submit"
                size="lg"
                className="w-full"
                disabled={!query.trim() || selectedTypes.length === 0 || isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Initiating Analysis...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Start AI Analysis
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </>
                )}
              </Button>
            </form>
          </div>
          
          {/* Quick Access Suggestions */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500 mb-3">Popular searches</p>
            <div className="flex flex-wrap justify-center gap-2">
              {suggestedMolecules.slice(0, 6).map((molecule) => (
                <button
                  key={molecule}
                  type="button"
                  onClick={() => setQuery(molecule)}
                  className="px-3 py-1.5 text-sm font-medium text-gray-600 bg-white border border-gray-200 rounded-full hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 transition-all"
                >
                  {molecule}
                </button>
              ))}
            </div>
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <p className="text-sm text-gray-500">
            Powered by Multi-Agent AI • EY Techathon 6.0
          </p>
        </div>
      </footer>
    </div>
  );
};
