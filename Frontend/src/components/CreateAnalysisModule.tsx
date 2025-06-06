
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, Upload, Plus, X, CheckCircle, Loader2, Database, Bot, TrendingUp, DollarSign, Activity, BarChart3, FileText, Brain } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

interface CreateAnalysisModuleProps {
  onBack: () => void;
  onAnalysisGenerated: (analysis: any) => void;
}

interface Competitor {
  name: string;
  documents: File[];
}

export const CreateAnalysisModule = ({ onBack, onAnalysisGenerated }: CreateAnalysisModuleProps) => {
  const [analysisName, setAnalysisName] = useState('');
  const [period, setPeriod] = useState('');
  const [description, setDescription] = useState('');
  const [dataWarehouse, setDataWarehouse] = useState('');
  const [internalDocs, setInternalDocs] = useState<File[]>([]);
  const [competitors, setCompetitors] = useState<Competitor[]>([]);
  const [newCompetitorName, setNewCompetitorName] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [currentTask, setCurrentTask] = useState('');

  const analysisAgents = [
    { name: 'Document Processing Agent', icon: FileText },
    { name: 'Income Statement Agent', icon: TrendingUp },
    { name: 'Balance Sheet Agent', icon: BarChart3 },
    { name: 'Cash Flow Agent', icon: Activity },
    { name: 'KPIs Agent', icon: DollarSign },
    { name: 'MD&A Agent', icon: Brain },
    { name: 'Report Generation Agent', icon: Bot }
  ];

  const addCompetitor = () => {
    if (newCompetitorName.trim()) {
      setCompetitors([...competitors, { name: newCompetitorName.trim(), documents: [] }]);
      setNewCompetitorName('');
    }
  };

  const removeCompetitor = (index: number) => {
    setCompetitors(competitors.filter((_, i) => i !== index));
  };

  const handleCompetitorFileUpload = (competitorIndex: number, files: FileList | null) => {
    if (files) {
      const newCompetitors = [...competitors];
      newCompetitors[competitorIndex].documents = [...newCompetitors[competitorIndex].documents, ...Array.from(files)];
      setCompetitors(newCompetitors);
    }
  };

  const handleInternalFileUpload = (files: FileList | null) => {
    if (files) {
      setInternalDocs([...internalDocs, ...Array.from(files)]);
    }
  };

  const generateAnalysis = async () => {
    setIsGenerating(true);
    setGenerationProgress(0);

    // Simulate analysis generation with progress
    for (let i = 0; i < analysisAgents.length; i++) {
      setCurrentTask(analysisAgents[i].name);
      setGenerationProgress(((i + 1) / analysisAgents.length) * 100);
      await new Promise(resolve => setTimeout(resolve, 1500));
    }

    // Create mock analysis result
    const newAnalysis = {
      id: Date.now().toString(),
      name: analysisName,
      description,
      period,
      dateCreated: new Date().toISOString().split('T')[0],
      status: 'completed',
      competitors: competitors.map(c => c.name)
    };

    setIsGenerating(false);
    onAnalysisGenerated(newAnalysis);
  };

  const canGenerate = analysisName && period && description && dataWarehouse && 
                     internalDocs.length > 0 && competitors.length > 0 &&
                     competitors.every(c => c.documents.length > 0);

  if (isGenerating) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl text-slate-900">AI Agents Processing Analysis</CardTitle>
            <CardDescription>Specialized AI agents are analyzing your documents and performing competitive analysis</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <Bot className="h-8 w-8 text-blue-600 animate-spin" />
              </div>
              <h3 className="text-lg font-medium text-slate-900 mb-2">{currentTask}</h3>
              <Progress value={generationProgress} className="w-full max-w-md mx-auto" />
              <p className="text-sm text-slate-600 mt-2">{Math.round(generationProgress)}% Complete</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-8">
              {analysisAgents.map((agent, index) => {
                const isCompleted = index < (generationProgress / 100) * analysisAgents.length;
                const isCurrent = index === Math.floor((generationProgress / 100) * analysisAgents.length);
                const IconComponent = agent.icon;
                
                return (
                  <div key={agent.name} className={`p-4 rounded-lg border ${
                    isCompleted ? 'bg-emerald-50 border-emerald-200' : 
                    isCurrent ? 'bg-blue-50 border-blue-200' : 'bg-slate-50 border-slate-200'
                  }`}>
                    <div className="flex items-center space-x-3">
                      {isCompleted ? (
                        <CheckCircle className="h-6 w-6 text-emerald-600" />
                      ) : isCurrent ? (
                        <IconComponent className="h-6 w-6 text-blue-600 animate-pulse" />
                      ) : (
                        <IconComponent className="h-6 w-6 text-slate-400" />
                      )}
                      <span className={`text-sm font-medium ${
                        isCompleted ? 'text-emerald-900' : 
                        isCurrent ? 'text-blue-900' : 'text-slate-600'
                      }`}>
                        {agent.name}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" onClick={onBack} className="text-slate-600">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Analyses
        </Button>
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Create New Analysis</h2>
          <p className="text-slate-600">Set up a competitive financial analysis with AI-powered insights</p>
        </div>
      </div>

      {/* Analysis Details */}
      <Card>
        <CardHeader>
          <CardTitle>Analysis Details</CardTitle>
          <CardDescription>Basic information about your competitive analysis</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="analysisName">Analysis Name *</Label>
              <Input
                id="analysisName"
                value={analysisName}
                onChange={(e) => setAnalysisName(e.target.value)}
                placeholder="e.g., Q1 2024 Competitive Analysis"
              />
            </div>
            <div>
              <Label htmlFor="period">Period *</Label>
              <Select value={period} onValueChange={setPeriod}>
                <SelectTrigger>
                  <SelectValue placeholder="Select quarter" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Q1 2024">Q1 2024</SelectItem>
                  <SelectItem value="Q2 2024">Q2 2024</SelectItem>
                  <SelectItem value="Q3 2024">Q3 2024</SelectItem>
                  <SelectItem value="Q4 2024">Q4 2024</SelectItem>
                  <SelectItem value="Q1 2025">Q1 2025</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <Label htmlFor="description">Description *</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the focus and objectives of this analysis..."
              rows={3}
            />
          </div>
        </CardContent>
      </Card>

      {/* Internal Data */}
      <Card>
        <CardHeader>
          <CardTitle>Internal Data</CardTitle>
          <CardDescription>Upload your bank's financial documents and select data warehouse</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="dataWarehouse">Data Warehouse *</Label>
            <Select value={dataWarehouse} onValueChange={setDataWarehouse}>
              <SelectTrigger>
                <Database className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Select data warehouse" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="primary">Primary Data Warehouse</SelectItem>
                <SelectItem value="reporting">Reporting Data Mart</SelectItem>
                <SelectItem value="risk">Risk Data Warehouse</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <Label>Upload Documents *</Label>
            <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center">
              <Upload className="h-8 w-8 text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-600 mb-2">Upload earnings reports, balance sheets, transcripts</p>
              <input
                type="file"
                multiple
                accept=".pdf,.doc,.docx,.xls,.xlsx"
                onChange={(e) => handleInternalFileUpload(e.target.files)}
                className="hidden"
                id="internal-upload"
              />
              <Button variant="outline" asChild>
                <label htmlFor="internal-upload">Choose Files</label>
              </Button>
            </div>
            {internalDocs.length > 0 && (
              <div className="mt-2 space-y-1">
                {internalDocs.map((file, index) => (
                  <div key={index} className="flex items-center text-sm text-slate-600">
                    <CheckCircle className="h-4 w-4 text-emerald-600 mr-2" />
                    {file.name}
                  </div>
                ))}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Competitor Data */}
      <Card>
        <CardHeader>
          <CardTitle>Competitor Data</CardTitle>
          <CardDescription>Add competitors and upload their financial documents</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input
              value={newCompetitorName}
              onChange={(e) => setNewCompetitorName(e.target.value)}
              placeholder="Competitor name (e.g., Bank of America)"
              onKeyPress={(e) => e.key === 'Enter' && addCompetitor()}
            />
            <Button onClick={addCompetitor} variant="outline">
              <Plus className="h-4 w-4" />
            </Button>
          </div>

          {competitors.map((competitor, index) => (
            <Card key={index} className="border-slate-200">
              <CardContent className="pt-4">
                <div className="flex justify-between items-start mb-3">
                  <h4 className="font-medium text-slate-900">{competitor.name}</h4>
                  <Button variant="ghost" size="sm" onClick={() => removeCompetitor(index)}>
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="border-2 border-dashed border-slate-300 rounded-lg p-4 text-center">
                  <Upload className="h-6 w-6 text-slate-400 mx-auto mb-1" />
                  <p className="text-xs text-slate-600 mb-2">Upload 10K, 10Q, earnings reports</p>
                  <input
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.xls,.xlsx"
                    onChange={(e) => handleCompetitorFileUpload(index, e.target.files)}
                    className="hidden"
                    id={`competitor-upload-${index}`}
                  />
                  <Button variant="outline" size="sm" asChild>
                    <label htmlFor={`competitor-upload-${index}`}>Choose Files</label>
                  </Button>
                </div>
                
                {competitor.documents.length > 0 && (
                  <div className="mt-2 space-y-1">
                    {competitor.documents.map((file, fileIndex) => (
                      <div key={fileIndex} className="flex items-center text-xs text-slate-600">
                        <CheckCircle className="h-3 w-3 text-emerald-600 mr-2" />
                        {file.name}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}

          {competitors.length === 0 && (
            <div className="text-center py-8 text-slate-500">
              <p>No competitors added yet. Add at least one competitor to continue.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Generate Analysis */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-medium text-slate-900">Ready to generate analysis?</h3>
              <p className="text-sm text-slate-600">AI will analyze all documents and create comprehensive reports</p>
            </div>
            <Button 
              onClick={generateAnalysis} 
              disabled={!canGenerate}
              className="bg-slate-700 hover:bg-slate-800"
            >
              Generate Analysis
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
