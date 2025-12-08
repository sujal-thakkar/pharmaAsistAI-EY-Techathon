// Zustand Store for PharmaAssist AI State Management
import { create } from 'zustand';
import { 
  AnalysisRequest, 
  AnalysisResult, 
  AgentStep, 
  ChatMessage,
  MoleculeData 
} from '@/types';
import { AGENT_STEPS, MOLECULE_DATABASE, SAMPLE_ANALYSIS_RESULT, SAMPLE_METRICS } from '@/data/mockData';
import { analysisAPI, chatAPI, AnalysisRequest as APIAnalysisRequest } from '@/services/api';

// Flag to enable/disable backend integration (set to true when backend is fully configured)
const USE_BACKEND = process.env.NEXT_PUBLIC_USE_BACKEND === 'true';

interface AppState {
  // Current Analysis State
  currentRequest: AnalysisRequest | null;
  currentResult: AnalysisResult | null;
  isAnalyzing: boolean;
  analysisProgress: number;
  
  // Agent Steps
  agentSteps: AgentStep[];
  currentStepIndex: number;
  
  // Chat State
  chatMessages: ChatMessage[];
  isChatLoading: boolean;
  
  // UI State
  activeTab: 'overview' | 'clinical' | 'market' | 'safety' | 'patents';
  sidebarExpanded: boolean;
  
  // Actions
  startAnalysis: (request: AnalysisRequest) => Promise<void>;
  resetAnalysis: () => void;
  sendChatMessage: (message: string) => Promise<void>;
  addChatMessage: (message: ChatMessage) => void;
  setActiveTab: (tab: 'overview' | 'clinical' | 'market' | 'safety' | 'patents') => void;
  toggleSidebar: () => void;
}

// Simulate agent processing with delays
const simulateAgentStep = async (
  stepIndex: number,
  updateStep: (index: number, updates: Partial<AgentStep>) => void
): Promise<void> => {
  const durations = [1500, 2000, 1800, 1500, 1700, 1600, 2200];
  const duration = durations[stepIndex] || 1500;
  
  updateStep(stepIndex, { status: 'in-progress', progress: 0 });
  
  // Simulate progress updates
  const progressSteps = 10;
  for (let i = 1; i <= progressSteps; i++) {
    await new Promise(resolve => setTimeout(resolve, duration / progressSteps));
    updateStep(stepIndex, { progress: (i / progressSteps) * 100 });
  }
  
  updateStep(stepIndex, { 
    status: 'completed', 
    progress: 100,
    endTime: new Date()
  });
};

export const useAppStore = create<AppState>((set, get) => ({
  // Initial State
  currentRequest: null,
  currentResult: null,
  isAnalyzing: false,
  analysisProgress: 0,
  agentSteps: AGENT_STEPS.map(step => ({ ...step })),
  currentStepIndex: -1,
  chatMessages: [],
  isChatLoading: false,
  activeTab: 'overview',
  sidebarExpanded: true,
  
  // Actions
  startAnalysis: async (request: AnalysisRequest) => {
    set({ 
      currentRequest: request, 
      isAnalyzing: true,
      analysisProgress: 0,
      agentSteps: AGENT_STEPS.map(step => ({ ...step, status: 'pending', progress: 0 })),
      currentStepIndex: 0
    });
    
    const updateStep = (index: number, updates: Partial<AgentStep>) => {
      set(state => ({
        agentSteps: state.agentSteps.map((step, i) => 
          i === index ? { ...step, ...updates } : step
        ),
        currentStepIndex: updates.status === 'completed' ? index + 1 : index,
        analysisProgress: ((index + (updates.progress || 0) / 100) / AGENT_STEPS.length) * 100
      }));
    };
    
    if (USE_BACKEND) {
      // Real backend integration
      try {
        const apiRequest: APIAnalysisRequest = {
          molecule_name: request.moleculeName,
          analysis_types: request.analysisTypes || ['clinical', 'market', 'regulatory'],
        };
        
        const response = await analysisAPI.start(apiRequest);
        
        // Poll for progress instead of SSE (more reliable)
        const pollInterval = setInterval(async () => {
          try {
            const data = await analysisAPI.get(response.analysis_id);
            
            // Update progress from backend
            set({ analysisProgress: data.progress || 0 });
            
            // Map backend steps to our agent steps
            if (data.steps) {
              const mappedSteps = AGENT_STEPS.map((step, index) => {
                const backendStep = data.steps.find((s: any) => 
                  s.name?.toLowerCase().includes(step.name.split(' ')[0].toLowerCase())
                );
                if (backendStep) {
                  return {
                    ...step,
                    status: backendStep.status || 'pending',
                    progress: backendStep.progress || 0,
                    output: backendStep.output,
                  };
                }
                return step;
              });
              set({ agentSteps: mappedSteps });
            }
            
            if (data.status === 'completed' && data.results) {
              clearInterval(pollInterval);
              
              // Use backend molecule data directly, with fallback for missing fields
              // Backend returns moleculeData.data with the actual data nested
              const rawMoleculeData = data.results.moleculeData || {};
              const backendMoleculeData = rawMoleculeData.data || rawMoleculeData || {};
              const moleculeName = data.results.moleculeName || request.moleculeName;
              
              // Get regulatory data from backend
              const backendRegulatoryStatus = data.results.regulatoryStatus || {};
              const backendPatentInfo = data.results.patentInfo || {};
              
              // Create molecule data from backend response
              const moleculeData: MoleculeData = {
                id: backendMoleculeData.id || `mol-${Date.now()}`,
                name: backendMoleculeData.name || moleculeName,
                category: backendMoleculeData.category || backendMoleculeData.therapeutic_class || 'Unknown',
                molecularWeight: backendMoleculeData.molecular_weight || backendMoleculeData.molecularWeight || 0,
                formula: backendMoleculeData.formula || backendMoleculeData.molecular_formula || 'N/A',
                mechanism: backendMoleculeData.mechanism || backendMoleculeData.mechanismOfAction || backendMoleculeData.mechanism_of_action || 'Not available',
                indications: backendMoleculeData.indications || backendRegulatoryStatus.approvedIndications || backendMoleculeData.therapeutic_applications || []
              };
              
              // Map regulatory status with proper fields
              const regulatoryStatus = {
                fda: backendRegulatoryStatus.fda || 'Pending',
                ema: backendRegulatoryStatus.ema || 'Pending',
                approvalDate: backendRegulatoryStatus.approvalDate || backendRegulatoryStatus.approval_date,
                approvedIndications: backendRegulatoryStatus.approvedIndications || backendRegulatoryStatus.approved_indications || [],
                labelWarnings: backendRegulatoryStatus.labelWarnings || backendRegulatoryStatus.label_warnings || []
              };
              
              // Map patent info with proper fields
              const patentInfo = {
                status: backendPatentInfo.status || 'Unknown',
                expiryDate: backendPatentInfo.expiryDate || backendPatentInfo.expiry_date || '',
                patentNumber: backendPatentInfo.patentNumber || backendPatentInfo.patent_number || '',
              };
              
              // Build result - spread data.results FIRST, then override with our properly mapped data
              const result: AnalysisResult = {
                ...SAMPLE_ANALYSIS_RESULT,
                ...data.results,
                id: response.analysis_id,
                moleculeData,
                regulatoryStatus,
                patentInfo,
                generatedAt: new Date().toISOString()
              };
              
              set({ 
                currentResult: result, 
                isAnalyzing: false,
                analysisProgress: 100,
                chatMessages: [{
                  id: 'welcome-msg',
                  role: 'assistant',
                  content: `I've completed the analysis of **${moleculeData.name}**. I found ${result.insights?.length || 0} key insights across clinical, market, regulatory, and safety domains. Feel free to ask me any questions about the findings!`,
                  timestamp: new Date().toISOString()
                }]
              });
            } else if (data.status === 'error') {
              clearInterval(pollInterval);
              console.error('Analysis failed:', data.error);
              runMockAnalysis();
            }
          } catch (pollError) {
            console.error('Polling error:', pollError);
            // Continue polling unless it's a fatal error
          }
        }, 1000); // Poll every second
        
        // Timeout after 2 minutes
        setTimeout(() => {
          clearInterval(pollInterval);
          const state = get();
          if (state.isAnalyzing) {
            console.warn('Analysis timed out, using mock data');
            runMockAnalysis();
          }
        }, 120000);
        
      } catch (error) {
        console.error('Failed to start analysis:', error);
        // Fall back to mock on error
        runMockAnalysis();
      }
      
      async function runMockAnalysis() {
        // Run through each agent step with mock data
        for (let i = 0; i < AGENT_STEPS.length; i++) {
          await simulateAgentStep(i, updateStep);
        }
        completeWithMockData();
      }
    } else {
      // Run through each agent step with mock data
      for (let i = 0; i < AGENT_STEPS.length; i++) {
        await simulateAgentStep(i, updateStep);
      }
      completeWithMockData();
    }
    
    function completeWithMockData() {
      // Find molecule in database or create dynamic molecule data for the requested molecule
      const foundMolecule = MOLECULE_DATABASE.find(
        m => m.name.toLowerCase() === request.moleculeName.toLowerCase()
      );
      
      // If molecule not in database, create dynamic entry with the actual requested name
      const moleculeData: MoleculeData = foundMolecule || {
        id: `mol-${Date.now()}`,
        name: request.moleculeName,
        category: 'Pharmaceutical',
        molecularWeight: 0,
        formula: 'N/A',
        mechanism: 'Information pending from analysis',
        indications: []
      };
      
      // Create analysis result using sample data structure
      const result: AnalysisResult = {
        ...SAMPLE_ANALYSIS_RESULT,
        id: `analysis-${Date.now()}`,
        moleculeData,
        generatedAt: new Date().toISOString()
      };
      
      set({ 
        currentResult: result, 
        isAnalyzing: false,
        analysisProgress: 100,
        chatMessages: [{
          id: 'welcome-msg',
          role: 'assistant',
          content: `I've completed the analysis of **${moleculeData.name}**. I found ${result.insights.length} key insights across clinical, market, regulatory, and safety domains. Feel free to ask me any questions about the findings!`,
          timestamp: new Date().toISOString()
        }]
      });
    }
  },
  
  resetAnalysis: () => {
    set({
      currentRequest: null,
      currentResult: null,
      isAnalyzing: false,
      analysisProgress: 0,
      agentSteps: AGENT_STEPS.map(step => ({ ...step, status: 'pending', progress: 0 })),
      currentStepIndex: -1,
      chatMessages: [],
      activeTab: 'overview'
    });
  },
  
  sendChatMessage: async (message: string) => {
    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };
    
    set(state => ({
      chatMessages: [...state.chatMessages, userMessage],
      isChatLoading: true
    }));
    
    const result = get().currentResult;
    
    if (USE_BACKEND) {
      // Real backend integration
      try {
        const response = await chatAPI.send({
          message,
          analysis_id: result?.id,
        });
        
        const assistantMessage: ChatMessage = {
          id: `msg-${Date.now() + 1}`,
          role: 'assistant',
          content: response.content,
          timestamp: new Date().toISOString(),
          sources: response.sources
        };
        
        set(state => ({
          chatMessages: [...state.chatMessages, assistantMessage],
          isChatLoading: false
        }));
      } catch (error) {
        console.error('Chat error, using mock response:', error);
        await generateMockResponse();
      }
    } else {
      await generateMockResponse();
    }
    
    async function generateMockResponse() {
      // Simulate AI response delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Generate contextual response based on current result
      let responseContent = "I'm here to help you understand the analysis results. Could you please be more specific about what you'd like to know?";
      
      const lowerMessage = message.toLowerCase();
      
      if (lowerMessage.includes('clinical') || lowerMessage.includes('trial')) {
        responseContent = `Based on my analysis, **${result?.moleculeData?.name}** has ${result?.clinicalTrials?.length || 0} major clinical trials. The drug is currently being studied in various phases to evaluate efficacy and long-term outcomes.`;
      } else if (lowerMessage.includes('market') || lowerMessage.includes('revenue')) {
        const marketSize = result?.marketData?.marketSize || 0;
        responseContent = `The market data shows **${result?.moleculeData?.name}** operates in a market worth approximately **$${(marketSize / 1000000000).toFixed(1)}B** with a **${result?.marketData?.growthRate || 0}% growth rate**. Current market share is **${result?.marketData?.marketShare || 0}%**.`;
      } else if (lowerMessage.includes('patent') || lowerMessage.includes('ip')) {
        responseContent = `The patent **${result?.patentInfo?.patentNumber}** (${result?.patentInfo?.title}) is currently **${result?.patentInfo?.status}** and expires on **${result?.patentInfo?.expiryDate}**. Filed by ${result?.patentInfo?.holder}.`;
      } else if (lowerMessage.includes('safety') || lowerMessage.includes('side effect')) {
        responseContent = `The regulatory status shows FDA approval: **${result?.regulatoryStatus?.fda}**, EMA approval: **${result?.regulatoryStatus?.ema}**. Approved indications include: ${result?.regulatoryStatus?.approvedIndications?.join(', ')}.`;
      } else if (lowerMessage.includes('competitor') || lowerMessage.includes('competition')) {
        const competitors = result?.marketData?.competitors || [];
        const competitorList = competitors.map(c => `${c.name} (${c.marketShare}%)`).join(', ');
        responseContent = `Key competitors include: ${competitorList}. The competitive landscape shows **${competitors.length}** active players in this market.`;
      }
      
      const assistantMessage: ChatMessage = {
        id: `msg-${Date.now() + 1}`,
        role: 'assistant',
        content: responseContent,
        timestamp: new Date().toISOString(),
        sources: result?.sources?.slice(0, 2)
      };
      
      set(state => ({
        chatMessages: [...state.chatMessages, assistantMessage],
        isChatLoading: false
      }));
    }
  },
  
  addChatMessage: (message: ChatMessage) => {
    set(state => ({
      chatMessages: [...state.chatMessages, message]
    }));
  },
  
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  toggleSidebar: () => set(state => ({ sidebarExpanded: !state.sidebarExpanded }))
}));
