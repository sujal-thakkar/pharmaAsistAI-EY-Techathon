'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  Loader2,
  Maximize2,
  Minimize2,
  X,
  MessageSquare
} from 'lucide-react';
import { Button, Badge } from '@/components/ui';
import { ChatMessage } from '@/types';
import { useAppStore } from '@/store/useAppStore';

interface ChatPanelProps {
  isOpen: boolean;
  onToggle: () => void;
  moleculeName?: string;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ isOpen, onToggle, moleculeName }) => {
  const { chatMessages, addChatMessage } = useAppStore();
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);
  
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };
    
    addChatMessage(userMessage);
    setInput('');
    setIsTyping(true);
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponses: Record<string, string> = {
        'market': `Based on my analysis of ${moleculeName || 'the molecule'}, the current market shows strong growth potential with a CAGR of 8.5%. Key drivers include increasing demand in emerging markets and recent regulatory approvals.`,
        'trial': `There are currently 12 active clinical trials for ${moleculeName || 'this compound'}. The most advanced is a Phase 3 study with promising efficacy data showing 72% response rates.`,
        'patent': `The core patent for ${moleculeName || 'this molecule'} expires in 2027. However, there are 3 secondary patents that provide extended protection until 2031.`,
        'competitor': `The main competitors include 4 branded products and 2 biosimilars in development. The market leader holds approximately 35% market share.`
      };
      
      const queryLower = input.toLowerCase();
      let response = `I've analyzed your question about ${moleculeName || 'the molecule'}. `;
      
      if (queryLower.includes('market') || queryLower.includes('growth') || queryLower.includes('size')) {
        response = aiResponses['market'];
      } else if (queryLower.includes('trial') || queryLower.includes('clinical') || queryLower.includes('study')) {
        response = aiResponses['trial'];
      } else if (queryLower.includes('patent') || queryLower.includes('expire') || queryLower.includes('protection')) {
        response = aiResponses['patent'];
      } else if (queryLower.includes('competitor') || queryLower.includes('competition') || queryLower.includes('alternative')) {
        response = aiResponses['competitor'];
      } else {
        response += `Based on my comprehensive research across clinical, market, and regulatory data, I can provide detailed insights on market trends, clinical trial progress, patent landscape, and competitive positioning. What specific aspect would you like to explore further?`;
      }
      
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString()
      };
      
      addChatMessage(aiMessage);
      setIsTyping(false);
    }, 1500);
  };
  
  const suggestedQuestions = [
    'What is the market growth projection?',
    'Are there any ongoing clinical trials?',
    'When does the patent expire?',
    'Who are the main competitors?'
  ];
  
  if (!isOpen) {
    return (
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        onClick={onToggle}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 shadow-lg shadow-indigo-500/30 flex items-center justify-center text-white hover:shadow-xl hover:shadow-indigo-500/40 transition-shadow z-50"
      >
        <MessageSquare className="w-6 h-6" />
      </motion.button>
    );
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 20, scale: 0.95 }}
      className={`fixed z-50 bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden ${
        isExpanded 
          ? 'inset-6' 
          : 'bottom-6 right-6 w-96 h-[600px]'
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100 bg-gradient-to-r from-indigo-500 to-cyan-500">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg overflow-hidden bg-white/20">
            <img src="/pharmaAssist-logo.png" alt="PharmaAssist AI" className="w-full h-full object-cover" />
          </div>
          <div>
            <h3 className="font-semibold text-white">AI Research Assistant</h3>
            <p className="text-xs text-white/70">Powered by multi-agent intelligence</p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
          <button
            onClick={onToggle}
            className="p-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Welcome Message */}
        {chatMessages.length === 0 && (
          <div className="text-center py-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-100 to-cyan-100 mb-4">
              <Bot className="w-8 h-8 text-indigo-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">
              Ask me anything about {moleculeName || 'your analysis'}
            </h4>
            <p className="text-sm text-gray-500 mb-6">
              I can help with market insights, clinical data, regulatory information, and more.
            </p>
            
            {/* Suggested Questions */}
            <div className="space-y-2">
              {suggestedQuestions.map((question) => (
                <button
                  key={question}
                  onClick={() => setInput(question)}
                  className="w-full px-4 py-2 text-left text-sm bg-gray-50 hover:bg-indigo-50 rounded-lg transition-colors text-gray-700 hover:text-indigo-700"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {/* Chat Messages */}
        <AnimatePresence>
          {chatMessages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className={`flex items-start gap-3 ${
                message.role === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              {/* Avatar */}
              <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
                message.role === 'user' 
                  ? 'bg-indigo-500' 
                  : 'bg-gradient-to-br from-indigo-100 to-cyan-100'
              }`}>
                {message.role === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-indigo-600" />
                )}
              </div>
              
              {/* Message Bubble */}
              <div className={`max-w-[75%] px-4 py-3 rounded-2xl ${
                message.role === 'user'
                  ? 'bg-indigo-500 text-white rounded-tr-sm'
                  : 'bg-gray-100 text-gray-800 rounded-tl-sm'
              }`}>
                <p className="text-sm leading-relaxed">{message.content}</p>
                <p className={`text-xs mt-1 ${
                  message.role === 'user' ? 'text-indigo-200' : 'text-gray-400'
                }`}>
                  {new Date(message.timestamp).toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Typing Indicator */}
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-start gap-3"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-100 to-cyan-100 flex items-center justify-center">
              <Bot className="w-4 h-4 text-indigo-600" />
            </div>
            <div className="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex items-center gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="border-t border-gray-100 p-4">
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about the analysis..."
            className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all text-sm"
            disabled={isTyping}
          />
          <Button
            type="submit"
            size="md"
            disabled={!input.trim() || isTyping}
            className="!px-4"
          >
            {isTyping ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </form>
        <p className="text-xs text-gray-400 text-center mt-2">
          AI responses are generated based on analyzed data
        </p>
      </div>
    </motion.div>
  );
};
