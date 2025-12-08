'use client';

import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import {
  TrendingUp,
  TrendingDown,
  FlaskConical,
  Shield,
  FileText,
  Calendar,
  Building2,
  DollarSign,
  Users,
  Activity,
  AlertCircle,
  CheckCircle2,
  Clock,
  BarChart3,
  PieChart as PieChartIcon,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Card, CardHeader, CardContent, Badge, MetricCard, GlassCard, Modal } from '@/components/ui';
import { AnalysisResult, ClinicalTrial, Insight } from '@/types';

// Helper function to format chemical formulas with subscripts
const FormulaDisplay: React.FC<{ formula: string; className?: string }> = ({ formula, className = '' }) => {
  // Convert numbers in formula to subscript characters
  const subscriptMap: { [key: string]: string } = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
  };
  
  const formattedFormula = formula.replace(/\d+/g, (match) => 
    match.split('').map(d => subscriptMap[d] || d).join('')
  );
  
  return <span className={className}>{formattedFormula}</span>;
};

interface ResultDashboardProps {
  result: AnalysisResult;
}

// Market Analysis Chart Data
const generateMarketChartData = (result: AnalysisResult) => {
  const baseValue = result.marketData.marketSize;
  const growth = result.marketData.growthRate / 100;
  const years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030];
  
  return years.map((year, index) => ({
    year,
    actual: index <= 4 ? Math.round(baseValue * Math.pow(1 + growth * 0.8, index - 4)) : null,
    projected: index >= 4 ? Math.round(baseValue * Math.pow(1 + growth, index - 4)) : null
  }));
};

// Clinical Trials by Phase
const generateTrialsByPhase = (trials: ClinicalTrial[]) => {
  const phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'];
  return phases.map(phase => ({
    name: phase,
    value: trials.filter(t => t.phase === phase).length,
    active: trials.filter(t => t.phase === phase && t.status === 'Active').length
  }));
};

// Competitor Market Share
const generateMarketShare = (result: AnalysisResult) => {
  const totalShare = result.marketData.marketShare + 
    result.marketData.competitors.reduce((sum, c) => sum + c.marketShare, 0);
  
  const data = [
    { name: result.moleculeData.name, value: result.marketData.marketShare, color: '#6366f1' },
    ...result.marketData.competitors.map((comp, i) => ({
      name: comp.name,
      value: comp.marketShare,
      color: ['#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][i % 4]
    }))
  ];
  
  // Add "Others" if total is less than 100
  if (totalShare < 100) {
    data.push({ name: 'Others', value: 100 - totalShare, color: '#94a3b8' });
  }
  
  return data;
};

// Insight Card Component
const InsightCard: React.FC<{ insight: Insight; index: number }> = ({ insight, index }) => {
  const getTypeIcon = () => {
    switch (insight.type) {
      case 'positive':
        return <TrendingUp className="w-4 h-4 text-emerald-500" />;
      case 'negative':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      case 'neutral':
        return <Minus className="w-4 h-4 text-amber-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-indigo-500" />;
    }
  };
  
  const getTypeBg = () => {
    switch (insight.type) {
      case 'positive':
        return 'bg-emerald-50 border-emerald-200';
      case 'negative':
        return 'bg-red-50 border-red-200';
      case 'neutral':
        return 'bg-amber-50 border-amber-200';
      default:
        return 'bg-indigo-50 border-indigo-200';
    }
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`p-4 rounded-xl border ${getTypeBg()}`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-0.5">{getTypeIcon()}</div>
        <div>
          <p className="text-sm font-medium text-gray-900">{insight.title}</p>
          <p className="text-xs text-gray-600 mt-1">{insight.description}</p>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant="info" className="text-xs">
              Confidence: {insight.confidence}%
            </Badge>
            <span className="text-xs text-gray-400">
              Source: {insight.source}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Trial Status Badge
const TrialStatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const getVariant = () => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'success';
      case 'completed':
        return 'info';
      case 'recruiting':
        return 'warning';
      default:
        return 'default';
    }
  };
  
  return <Badge variant={getVariant()}>{status}</Badge>;
};

export const ResultDashboard: React.FC<ResultDashboardProps> = ({ result }) => {
  // State for modals
  const [selectedTrial, setSelectedTrial] = useState<any>(null);
  const [showAllTrials, setShowAllTrials] = useState(false);
  
  // Safe defaults for potentially missing data from backend
  const safeResult = useMemo(() => ({
    ...result,
    moleculeData: {
      id: result.moleculeData?.id || `mol-${Date.now()}`,
      name: result.moleculeData?.name || 'Unknown',
      formula: result.moleculeData?.formula || 'N/A',
      category: result.moleculeData?.category || 'Unknown',
      molecularWeight: result.moleculeData?.molecularWeight || 0,
      mechanism: result.moleculeData?.mechanism || 'Not available',
      indications: result.moleculeData?.indications || [],
    },
    marketData: {
      marketSize: result.marketData?.marketSize || 10000000000,
      growthRate: result.marketData?.growthRate || 5,
      marketShare: result.marketData?.marketShare || 15,
      competitors: result.marketData?.competitors || [],
    },
    clinicalTrials: result.clinicalTrials || [],
    regulatoryStatus: {
      fda: result.regulatoryStatus?.fda || 'Pending',
      ema: result.regulatoryStatus?.ema || 'Pending',
      approvedIndications: result.regulatoryStatus?.approvedIndications || [],
    },
    patentInfo: result.patentInfo || { status: 'Unknown', expiryDate: '' },
    insights: result.insights || [],
    sources: result.sources || [],
  }), [result]);

  const marketChartData = useMemo(() => generateMarketChartData(safeResult as unknown as AnalysisResult), [safeResult]);
  const trialsByPhase = useMemo(() => generateTrialsByPhase(safeResult.clinicalTrials || []), [safeResult]);
  const marketShareData = useMemo(() => generateMarketShare(safeResult as unknown as AnalysisResult), [safeResult]);
  
  const formatCurrency = (value: number) => {
    if (value >= 1000000000) {
      return `$${(value / 1000000000).toFixed(1)}B`;
    }
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    }
    return `$${value.toLocaleString()}`;
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-indigo-50">
      {/* Header Section */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {safeResult.moleculeData.name}
                </h1>
                <p className="text-sm text-gray-500">
                  <FormulaDisplay formula={safeResult.moleculeData.formula} /> • {safeResult.moleculeData.category}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Badge variant="success" className="flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" />
                Analysis Complete
              </Badge>
              <span className="text-sm text-gray-500">
                Generated {new Date(safeResult.generatedAt || new Date()).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* KPI Metrics Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard
            title="Market Size"
            value={formatCurrency(safeResult.marketData.marketSize)}
            trend={safeResult.marketData.growthRate}
            trendLabel="YoY Growth"
            icon={<DollarSign className="w-5 h-5" />}
          />
          <MetricCard
            title="Active Trials"
            value={(safeResult.clinicalTrials.filter((t: any) => t.status === 'Active').length || 0).toString()}
            subtitle={`${safeResult.clinicalTrials.length} total trials`}
            icon={<Activity className="w-5 h-5" />}
          />
          <MetricCard
            title="Market Share"
            value={`${safeResult.marketData.marketShare}%`}
            trend={2.5}
            trendLabel="vs last year"
            icon={<PieChartIcon className="w-5 h-5" />}
          />
          <MetricCard
            title="Patent Status"
            value={safeResult.patentInfo?.status || 'Unknown'}
            subtitle={safeResult.patentInfo?.expiryDate ? `Expires: ${new Date(safeResult.patentInfo.expiryDate).getFullYear()}` : 'N/A'}
            icon={<Shield className="w-5 h-5" />}
          />
        </div>
        
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Charts */}
          <div className="lg:col-span-2 space-y-6">
            {/* Market Trend Chart */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <BarChart3 className="w-5 h-5 text-indigo-500" />
                    <h3 className="font-semibold text-gray-900">Market Trend & Projections</h3>
                  </div>
                  <Badge variant="info">10-Year Forecast</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={marketChartData}>
                      <defs>
                        <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorProjected" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="year" stroke="#9ca3af" fontSize={12} />
                      <YAxis 
                        stroke="#9ca3af" 
                        fontSize={12}
                        tickFormatter={(value) => `$${(value / 1000000000).toFixed(0)}B`}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'white',
                          border: '1px solid #e5e7eb',
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                        }}
                        formatter={(value: number) => [formatCurrency(value), '']}
                      />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="actual"
                        stroke="#6366f1"
                        strokeWidth={2}
                        fillOpacity={1}
                        fill="url(#colorActual)"
                        name="Historical"
                      />
                      <Area
                        type="monotone"
                        dataKey="projected"
                        stroke="#06b6d4"
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        fillOpacity={1}
                        fill="url(#colorProjected)"
                        name="Projected"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
            
            {/* Clinical Trials Section */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <FlaskConical className="w-5 h-5 text-indigo-500" />
                    <h3 className="font-semibold text-gray-900">Clinical Trials Overview</h3>
                  </div>
                  {(safeResult.clinicalTrials || []).length > 4 && (
                    <button
                      onClick={() => setShowAllTrials(true)}
                      className="text-sm text-indigo-600 hover:text-indigo-700 font-medium flex items-center gap-1"
                    >
                      View All ({safeResult.clinicalTrials.length})
                      <ArrowUpRight className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Trials by Phase Chart */}
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={trialsByPhase} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis type="number" stroke="#9ca3af" fontSize={12} />
                        <YAxis type="category" dataKey="name" stroke="#9ca3af" fontSize={12} width={70} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: 'white',
                            border: '1px solid #e5e7eb',
                            borderRadius: '8px'
                          }}
                        />
                        <Bar dataKey="value" fill="#6366f1" radius={[0, 4, 4, 0]} name="Total" />
                        <Bar dataKey="active" fill="#10b981" radius={[0, 4, 4, 0]} name="Active" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  
                  {/* Trials List */}
                  <div className="space-y-3 max-h-64 overflow-y-auto pr-2">
                    {(safeResult.clinicalTrials || []).slice(0, 4).map((trial: any, index: number) => (
                      <motion.div
                        key={trial.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="p-3 bg-gray-50 rounded-lg hover:bg-indigo-50 transition-colors cursor-pointer group"
                        onClick={() => setSelectedTrial(trial)}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div className="min-w-0 flex-1">
                            <p className="text-sm font-medium text-gray-900 truncate group-hover:text-indigo-700">
                              {trial.title}
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                              {trial.sponsor} • {trial.phase}
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            <TrialStatusBadge status={trial.status} />
                            <ArrowUpRight className="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
            
            {/* Competitive Landscape */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Building2 className="w-5 h-5 text-indigo-500" />
                  <h3 className="font-semibold text-gray-900">Competitive Landscape</h3>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Market Share Pie Chart */}
                  <div>
                    <div className="h-48">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={marketShareData}
                            cx="50%"
                            cy="50%"
                            innerRadius={35}
                            outerRadius={65}
                            paddingAngle={2}
                            dataKey="value"
                          >
                            {marketShareData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip 
                            formatter={(value: number, name: string) => [`${value}%`, name]}
                            contentStyle={{
                              backgroundColor: 'white',
                              border: '1px solid #e5e7eb',
                              borderRadius: '8px',
                              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                            }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    {/* Legend */}
                    <div className="mt-4 grid grid-cols-2 gap-2">
                      {marketShareData.map((entry, index) => (
                        <div key={index} className="flex items-center gap-2 text-xs">
                          <div 
                            className="w-3 h-3 rounded-full shrink-0"
                            style={{ backgroundColor: entry.color }}
                          />
                          <span className="text-gray-600 truncate" title={entry.name}>
                            {entry.name}: {entry.value}%
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* Competitors List */}
                  <div className="space-y-3">
                    {(safeResult.marketData?.competitors || []).map((competitor: any, index: number) => (
                      <motion.div
                        key={competitor.name}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex items-center gap-3">
                          <div 
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index % 4] }}
                          />
                          <div>
                            <p className="text-sm font-medium text-gray-900">{competitor.name}</p>
                            <p className="text-xs text-gray-500">{competitor.company}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold text-gray-900">{competitor.marketShare}%</p>
                          <p className="text-xs text-gray-500">market share</p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
          
          {/* Right Column - Insights & Info */}
          <div className="space-y-6">
            {/* Molecule Information */}
            <GlassCard className="p-6">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-500" />
                Molecule Profile
              </h3>
              <div className="space-y-4">
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide">Chemical Formula</p>
                  <p className="font-mono text-lg font-semibold text-gray-900">
                    <FormulaDisplay formula={safeResult.moleculeData.formula} />
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide">Molecular Weight</p>
                  <p className="font-medium text-gray-900">
                    {safeResult.moleculeData.molecularWeight} g/mol
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide">Mechanism</p>
                  <p className="text-sm text-gray-700">
                    {safeResult.moleculeData.mechanism}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Indications</p>
                  <div className="flex flex-wrap gap-2">
                    {(safeResult.moleculeData.indications || []).map((indication: string) => (
                      <Badge key={indication} variant="default" className="text-xs">
                        {indication}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </GlassCard>
            
            {/* Patent Information */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Shield className="w-5 h-5 text-indigo-500" />
                  <h3 className="font-semibold text-gray-900">Patent & Regulatory</h3>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Patent Status</span>
                    <Badge variant={safeResult.patentInfo?.status === 'Active' ? 'success' : 'warning'}>
                      {safeResult.patentInfo?.status || 'Unknown'}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Expiry Date</span>
                    <span className="text-sm font-medium text-gray-900">
                      {safeResult.patentInfo?.expiryDate ? new Date(safeResult.patentInfo.expiryDate).toLocaleDateString() : 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">FDA Status</span>
                    <Badge variant={safeResult.regulatoryStatus?.fda === 'Approved' ? 'success' : 'info'}>
                      {safeResult.regulatoryStatus?.fda || 'Pending'}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">EMA Status</span>
                    <Badge variant={safeResult.regulatoryStatus?.ema === 'Approved' ? 'success' : 'info'}>
                      {safeResult.regulatoryStatus?.ema || 'Pending'}
                    </Badge>
                  </div>
                  
                  {/* Approved Indications */}
                  <div className="pt-3 border-t border-gray-100">
                    <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Approved Indications</p>
                    <div className="flex flex-wrap gap-1">
                      {(safeResult.regulatoryStatus?.approvedIndications || []).map((ind: string) => (
                        <Badge key={ind} variant="success" className="text-xs">
                          {ind}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            {/* AI Insights */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-indigo-500" />
                  <h3 className="font-semibold text-gray-900">AI-Generated Insights</h3>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {(safeResult.insights || []).map((insight: any, index: number) => (
                    <InsightCard key={insight.id || index} insight={insight} index={index} />
                  ))}
                </div>
              </CardContent>
            </Card>
            
            {/* Sources */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-indigo-500" />
                  <h3 className="font-semibold text-gray-900">Data Sources</h3>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {(safeResult.sources || []).map((source: any) => (
                    <a
                      key={source.id}
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-indigo-50 transition-colors group"
                    >
                      <div>
                        <p className="text-sm font-medium text-gray-900 group-hover:text-indigo-600">
                          {source.name}
                        </p>
                        <p className="text-xs text-gray-500">{source.type}</p>
                      </div>
                      <ArrowUpRight className="w-4 h-4 text-gray-400 group-hover:text-indigo-500" />
                    </a>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Individual Trial Detail Modal */}
      <Modal
        isOpen={!!selectedTrial}
        onClose={() => setSelectedTrial(null)}
        title={selectedTrial?.title || 'Trial Details'}
        size="lg"
      >
        {selectedTrial && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-1">Phase</p>
                <p className="font-semibold text-indigo-600">{selectedTrial.phase}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-1">Status</p>
                <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  selectedTrial.status === 'Recruiting' 
                    ? 'bg-green-100 text-green-700'
                    : selectedTrial.status === 'Completed'
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {selectedTrial.status}
                </span>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500 mb-1">Sponsor</p>
              <p className="font-medium text-gray-900">{selectedTrial.sponsor || 'Not specified'}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-1">Enrollment</p>
                <p className="font-medium text-gray-900">{selectedTrial.enrollment || 'N/A'} participants</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-1">Start Date</p>
                <p className="font-medium text-gray-900">{selectedTrial.startDate || 'Not specified'}</p>
              </div>
            </div>

            {selectedTrial.description && (
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-1">Description</p>
                <p className="text-sm text-gray-700 leading-relaxed">{selectedTrial.description}</p>
              </div>
            )}

            {selectedTrial.url && (
              <a
                href={selectedTrial.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 w-full py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                View on ClinicalTrials.gov
              </a>
            )}
          </div>
        )}
      </Modal>

      {/* All Trials Modal */}
      <Modal
        isOpen={showAllTrials}
        onClose={() => setShowAllTrials(false)}
        title="All Clinical Trials"
        size="xl"
      >
        <div className="space-y-3 max-h-[60vh] overflow-y-auto">
          {(safeResult.clinicalTrials || []).map((trial: any, index: number) => (
            <motion.div
              key={trial.id || index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="p-4 bg-gray-50 rounded-lg hover:bg-indigo-50 cursor-pointer transition-colors"
              onClick={() => {
                setShowAllTrials(false);
                setSelectedTrial(trial);
              }}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <h4 className="font-medium text-gray-900 mb-1">{trial.title}</h4>
                  <p className="text-sm text-gray-500">{trial.sponsor}</p>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-medium">
                    {trial.phase}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    trial.status === 'Recruiting' 
                      ? 'bg-green-100 text-green-700'
                      : trial.status === 'Completed'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {trial.status}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
          
          {(safeResult.clinicalTrials || []).length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No clinical trials found for this drug.
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
};
