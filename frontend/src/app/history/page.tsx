'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Clock, 
  Search, 
  FlaskConical, 
  Calendar,
  Download,
  Trash2,
  Filter,
  ArrowUpRight
} from 'lucide-react';
import Link from 'next/link';
import { Navigation } from '@/components/Navigation';
import { Card, CardHeader, CardContent, Badge, Button, Input } from '@/components/ui';

// Mock history data
const historyData = [
  {
    id: 'analysis-001',
    molecule: 'Aspirin (Acetylsalicylic acid)',
    date: '2024-01-15T10:30:00Z',
    status: 'completed',
    analysisTypes: ['market', 'clinical', 'regulatory'],
    insights: 12,
    sources: 8
  },
  {
    id: 'analysis-002',
    molecule: 'Metformin Hydrochloride',
    date: '2024-01-14T14:45:00Z',
    status: 'completed',
    analysisTypes: ['market', 'competitive'],
    insights: 8,
    sources: 6
  },
  {
    id: 'analysis-003',
    molecule: 'Ozempic (Semaglutide)',
    date: '2024-01-13T09:15:00Z',
    status: 'completed',
    analysisTypes: ['market', 'clinical', 'regulatory', 'competitive'],
    insights: 15,
    sources: 12
  },
  {
    id: 'analysis-004',
    molecule: 'Keytruda (Pembrolizumab)',
    date: '2024-01-12T16:20:00Z',
    status: 'completed',
    analysisTypes: ['clinical', 'regulatory'],
    insights: 10,
    sources: 7
  },
  {
    id: 'analysis-005',
    molecule: 'Humira (Adalimumab)',
    date: '2024-01-11T11:00:00Z',
    status: 'completed',
    analysisTypes: ['market', 'competitive'],
    insights: 9,
    sources: 5
  },
  {
    id: 'analysis-006',
    molecule: 'Lipitor (Atorvastatin)',
    date: '2024-01-10T08:30:00Z',
    status: 'completed',
    analysisTypes: ['market', 'regulatory'],
    insights: 7,
    sources: 4
  }
];

const analysisTypeLabels: Record<string, string> = {
  market: 'Market',
  clinical: 'Clinical',
  regulatory: 'Regulatory',
  competitive: 'Competitive'
};

export default function HistoryPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null);
  
  const filteredHistory = historyData.filter(item => {
    const matchesSearch = item.molecule.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = !selectedFilter || item.analysisTypes.includes(selectedFilter);
    return matchesSearch && matchesFilter;
  });
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Analysis History</h1>
            <p className="text-gray-500 mt-1">View and manage your past pharmaceutical analyses</p>
          </div>
          <Link href="/">
            <Button>
              <FlaskConical className="w-4 h-4 mr-2" />
              New Analysis
            </Button>
          </Link>
        </div>
        
        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="py-4">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search analyses..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all"
                />
              </div>
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <div className="flex gap-2">
                  {['market', 'clinical', 'regulatory', 'competitive'].map((type) => (
                    <button
                      key={type}
                      onClick={() => setSelectedFilter(selectedFilter === type ? null : type)}
                      className={`px-3 py-1.5 text-sm rounded-lg border transition-all ${
                        selectedFilter === type
                          ? 'bg-indigo-50 border-indigo-500 text-indigo-600'
                          : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      {analysisTypeLabels[type]}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        {/* History List */}
        <div className="space-y-4">
          {filteredHistory.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card className="hover:shadow-md transition-shadow">
                <CardContent className="py-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-xl overflow-hidden shadow-md">
                        <img src="/pharmaAssist-logo.png" alt="PharmaAssist AI" className="w-full h-full object-cover" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{item.molecule}</h3>
                        <div className="flex items-center gap-4 mt-1">
                          <span className="flex items-center gap-1 text-sm text-gray-500">
                            <Calendar className="w-4 h-4" />
                            {new Date(item.date).toLocaleDateString()}
                          </span>
                          <span className="flex items-center gap-1 text-sm text-gray-500">
                            <Clock className="w-4 h-4" />
                            {new Date(item.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-6">
                      {/* Analysis Types */}
                      <div className="hidden md:flex items-center gap-2">
                        {item.analysisTypes.map((type) => (
                          <Badge key={type} variant="info" className="text-xs">
                            {analysisTypeLabels[type]}
                          </Badge>
                        ))}
                      </div>
                      
                      {/* Stats */}
                      <div className="hidden lg:flex items-center gap-4 text-sm text-gray-500">
                        <span>{item.insights} insights</span>
                        <span>{item.sources} sources</span>
                      </div>
                      
                      {/* Actions */}
                      <div className="flex items-center gap-2">
                        <Link href={`/results/${item.id}`}>
                          <button className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors">
                            <ArrowUpRight className="w-5 h-5" />
                          </button>
                        </Link>
                        <button className="p-2 text-gray-400 hover:bg-gray-50 hover:text-gray-600 rounded-lg transition-colors">
                          <Download className="w-5 h-5" />
                        </button>
                        <button className="p-2 text-gray-400 hover:bg-red-50 hover:text-red-500 rounded-lg transition-colors">
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
        
        {/* Empty State */}
        {filteredHistory.length === 0 && (
          <div className="text-center py-16">
            <div className="w-16 h-16 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-4">
              <Clock className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">No analyses found</h3>
            <p className="text-gray-500 mb-6">
              {searchQuery || selectedFilter
                ? 'Try adjusting your search or filters'
                : 'Start your first analysis to see it here'
              }
            </p>
            <Link href="/">
              <Button>
                <FlaskConical className="w-4 h-4 mr-2" />
                Start New Analysis
              </Button>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
