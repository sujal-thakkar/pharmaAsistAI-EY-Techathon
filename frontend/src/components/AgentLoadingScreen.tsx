'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  FlaskConical, 
  BarChart3, 
  FileText, 
  Shield, 
  AlertTriangle, 
  Sparkles,
  CheckCircle2,
  Loader2
} from 'lucide-react';
import { AgentStep } from '@/types';
import { useAppStore } from '@/store/useAppStore';
import { ProgressBar } from '@/components/ui';

const iconMap: Record<string, React.ElementType> = {
  brain: Brain,
  flask: FlaskConical,
  chart: BarChart3,
  file: FileText,
  shield: Shield,
  alert: AlertTriangle,
  sparkles: Sparkles
};

interface AgentStepCardProps {
  step: AgentStep;
  index: number;
  isActive: boolean;
}

const AgentStepCard: React.FC<AgentStepCardProps> = ({ step, index, isActive }) => {
  const Icon = iconMap[step.icon] || Brain;
  
  const getStatusColor = () => {
    switch (step.status) {
      case 'completed':
        return 'border-emerald-500 bg-emerald-50';
      case 'in-progress':
        return 'border-indigo-500 bg-indigo-50';
      case 'error':
        return 'border-red-500 bg-red-50';
      default:
        return 'border-gray-200 bg-white';
    }
  };
  
  const getIconBgColor = () => {
    switch (step.status) {
      case 'completed':
        return 'bg-emerald-500';
      case 'in-progress':
        return 'bg-indigo-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-300';
    }
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      className={`relative flex items-start gap-4 p-4 rounded-xl border-2 transition-all duration-300 ${getStatusColor()} ${isActive ? 'step-active' : ''}`}
    >
      {/* Icon */}
      <div className={`flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center ${getIconBgColor()} transition-colors duration-300`}>
        {step.status === 'completed' ? (
          <CheckCircle2 className="w-6 h-6 text-white" />
        ) : step.status === 'in-progress' ? (
          <Loader2 className="w-6 h-6 text-white animate-spin" />
        ) : (
          <Icon className="w-6 h-6 text-white" />
        )}
      </div>
      
      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <h3 className="font-semibold text-gray-900">{step.name}</h3>
          {step.status === 'completed' && (
            <span className="text-xs font-medium text-emerald-600 bg-emerald-100 px-2 py-0.5 rounded-full">
              Complete
            </span>
          )}
          {step.status === 'in-progress' && (
            <span className="text-xs font-medium text-indigo-600 bg-indigo-100 px-2 py-0.5 rounded-full animate-pulse">
              Processing
            </span>
          )}
        </div>
        <p className="mt-1 text-sm text-gray-600">{step.description}</p>
        
        {/* Progress Bar for Active Step */}
        {step.status === 'in-progress' && (
          <div className="mt-3">
            <ProgressBar value={step.progress} color="primary" size="sm" />
          </div>
        )}
      </div>
      
      {/* Step Number */}
      <div className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-white border-2 border-gray-200 flex items-center justify-center">
        <span className="text-xs font-bold text-gray-500">{index + 1}</span>
      </div>
    </motion.div>
  );
};

interface AgentLoadingScreenProps {
  onComplete?: () => void;
}

export const AgentLoadingScreen: React.FC<AgentLoadingScreenProps> = ({ onComplete }) => {
  const { agentSteps, analysisProgress, currentRequest, isAnalyzing } = useAppStore();
  const [dots, setDots] = useState('');
  
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 500);
    return () => clearInterval(interval);
  }, []);
  
  useEffect(() => {
    if (!isAnalyzing && analysisProgress >= 100 && onComplete) {
      const timer = setTimeout(onComplete, 500);
      return () => clearTimeout(timer);
    }
  }, [isAnalyzing, analysisProgress, onComplete]);
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          {/* Render the text logo alone (not in square box) */}
          <img src="/pharmaAssist-logo.png" alt="PharmaAssist AI" className="mx-auto mb-6 h-20 w-auto object-contain" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Analyzing {currentRequest?.moleculeName || 'molecule'}{dots}
          </h1>
          <p className="text-gray-600">
            Our AI agents are gathering intelligence from multiple sources
          </p>
        </motion.div>
        
        {/* Overall Progress */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <span className="font-medium text-gray-700">Overall Progress</span>
            <span className="text-2xl font-bold text-indigo-600">{Math.round(analysisProgress)}%</span>
          </div>
          <ProgressBar value={analysisProgress} color="primary" size="lg" />
          <p className="mt-4 text-sm text-gray-500 text-center">
            Estimated time remaining: ~{Math.max(1, Math.round((100 - analysisProgress) / 10))} seconds
          </p>
        </motion.div>
        
        {/* Agent Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <AnimatePresence mode="wait">
            {agentSteps.map((step, index) => (
              <AgentStepCard
                key={step.id}
                step={step}
                index={index}
                isActive={step.status === 'in-progress'}
              />
            ))}
          </AnimatePresence>
        </div>
        
        {/* Animated Background Elements */}
        <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.5, 0.3]
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
            className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-200 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1.2, 1, 1.2],
              opacity: [0.3, 0.5, 0.3]
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
            className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-200 rounded-full blur-3xl"
          />
        </div>
      </div>
    </div>
  );
};
