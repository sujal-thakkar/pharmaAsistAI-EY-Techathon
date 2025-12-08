'use client';

import React, { useCallback, useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Handle,
  Position,
  Connection,
  Edge,
  NodeProps,
  BackgroundVariant
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { 
  FlaskConical, 
  FileText, 
  TrendingUp, 
  Shield, 
  Building2,
  Database,
  Globe,
  BookOpen
} from 'lucide-react';
import { Card, CardHeader, CardContent, Badge } from '@/components/ui';
import { EvidenceNode, EvidenceEdge } from '@/types';

interface EvidenceGraphProps {
  nodes: EvidenceNode[];
  edges: EvidenceEdge[];
}

// Icon mapping for node types
const iconMap: Record<string, React.ElementType> = {
  molecule: FlaskConical,
  clinical: FileText,
  market: TrendingUp,
  patent: Shield,
  competitor: Building2,
  database: Database,
  web: Globe,
  publication: BookOpen
};

// Color mapping for node types
const colorMap: Record<string, { bg: string; border: string; text: string }> = {
  molecule: { bg: 'bg-indigo-100', border: 'border-indigo-500', text: 'text-indigo-700' },
  clinical: { bg: 'bg-emerald-100', border: 'border-emerald-500', text: 'text-emerald-700' },
  market: { bg: 'bg-amber-100', border: 'border-amber-500', text: 'text-amber-700' },
  patent: { bg: 'bg-purple-100', border: 'border-purple-500', text: 'text-purple-700' },
  competitor: { bg: 'bg-red-100', border: 'border-red-500', text: 'text-red-700' },
  database: { bg: 'bg-cyan-100', border: 'border-cyan-500', text: 'text-cyan-700' },
  web: { bg: 'bg-blue-100', border: 'border-blue-500', text: 'text-blue-700' },
  publication: { bg: 'bg-pink-100', border: 'border-pink-500', text: 'text-pink-700' },
  trial: { bg: 'bg-emerald-100', border: 'border-emerald-500', text: 'text-emerald-700' },
  regulatory: { bg: 'bg-orange-100', border: 'border-orange-500', text: 'text-orange-700' },
  insight: { bg: 'bg-violet-100', border: 'border-violet-500', text: 'text-violet-700' }
};

// Node data type
interface CustomNodeData {
  label: string;
  type: string;
  description?: string;
  confidence?: number;
}

// Custom Node Component
const CustomNode = ({ data }: { data: CustomNodeData }) => {
  const Icon = iconMap[data.type] || Database;
  const colors = colorMap[data.type] || colorMap.database;
  
  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`px-4 py-3 rounded-xl border-2 shadow-lg ${colors.bg} ${colors.border} min-w-[180px]`}
    >
      <Handle 
        type="target" 
        position={Position.Top} 
        className="!bg-gray-400 !w-3 !h-3 !border-2 !border-white" 
      />
      
      <div className="flex items-center gap-3">
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${colors.bg} border ${colors.border}`}>
          <Icon className={`w-5 h-5 ${colors.text}`} />
        </div>
        <div>
          <p className={`font-semibold text-sm ${colors.text}`}>{data.label}</p>
          {data.description && (
            <p className="text-xs text-gray-500 mt-0.5">{data.description}</p>
          )}
        </div>
      </div>
      
      {data.confidence && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">Confidence</span>
            <Badge 
              variant={data.confidence > 80 ? 'success' : data.confidence > 60 ? 'warning' : 'default'}
              className="text-xs"
            >
              {data.confidence}%
            </Badge>
          </div>
        </div>
      )}
      
      <Handle 
        type="source" 
        position={Position.Bottom} 
        className="!bg-gray-400 !w-3 !h-3 !border-2 !border-white" 
      />
    </motion.div>
  );
};

const nodeTypes = {
  custom: CustomNode
};

export const EvidenceGraph: React.FC<EvidenceGraphProps> = ({ nodes: initialNodes, edges: initialEdges }) => {
  // Transform nodes to React Flow format
  const flowNodes = useMemo(() => 
    initialNodes.map(node => ({
      id: node.id,
      type: 'custom',
      position: node.position,
      data: {
        label: node.data.label,
        type: node.type,
        description: node.data.description,
        confidence: node.data.confidence
      }
    })),
    [initialNodes]
  );
  
  // Transform edges to React Flow format
  const flowEdges = useMemo(() => 
    initialEdges.map(edge => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      animated: edge.animated,
      style: { 
        stroke: '#6366f1',
        strokeWidth: 2
      },
      labelStyle: {
        fill: '#4b5563',
        fontSize: 12,
        fontWeight: 500
      },
      labelBgStyle: {
        fill: 'white',
        fillOpacity: 0.9
      }
    })),
    [initialEdges]
  );
  
  const [nodes, setNodes, onNodesChange] = useNodesState(flowNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(flowEdges);
  
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );
  
  return (
    <Card className="h-[500px]">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-500" />
            <h3 className="font-semibold text-gray-900">Evidence Graph</h3>
          </div>
          <Badge variant="info">
            {nodes.length} sources connected
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="h-[400px] p-0">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.2 }}
          attributionPosition="bottom-left"
        >
          <Controls 
            className="!bg-white !border !border-gray-200 !rounded-lg !shadow-lg"
          />
          <MiniMap 
            className="!bg-white !border !border-gray-200 !rounded-lg !shadow-lg"
            nodeColor={(node) => {
              const type = node.data?.type as string;
              const colors: Record<string, string> = {
                molecule: '#6366f1',
                clinical: '#10b981',
                market: '#f59e0b',
                patent: '#8b5cf6',
                competitor: '#ef4444',
                database: '#06b6d4',
                web: '#3b82f6',
                publication: '#ec4899'
              };
              return colors[type] || '#94a3b8';
            }}
            maskColor="rgba(255, 255, 255, 0.8)"
          />
          <Background 
            variant={BackgroundVariant.Dots} 
            gap={16} 
            size={1} 
            color="#e5e7eb"
          />
        </ReactFlow>
      </CardContent>
    </Card>
  );
};
