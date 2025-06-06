import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ArrowLeft, MessageSquare, User, Clock, FileText, Send, Search, Filter, Loader2, AlertCircle } from 'lucide-react';
import { useAnalysesDemo } from '@/hooks/useAnalyses';
import { useMarketQuestionsDemo } from '@/hooks/useMarketResearch';
import { MarketQuestion } from '@/lib/api';

interface MarketResearchModuleProps {
  onBack: () => void;
}

const dashboardOptions = [
  'Income Statement',
  'Balance Sheet',
  'Cash Flow',
  'KPIs & Ratios',
  'MD&A'
];

const reportOptions = {
  'Income Statement': ['Revenue Growth', 'Expense Ratios', 'Net Interest Margin', 'Profitability Ratios'],
  'Balance Sheet': ['Asset Growth', 'Liability Structure', 'Capital Ratios', 'Loan-to-Deposit Ratio'],
  'Cash Flow': ['Operating Cash Flow', 'Investment Cash Flow', 'Financing Cash Flow'],
  'KPIs & Ratios': ['NPL Ratio', 'Customer Acquisition Cost', 'Liquidity Coverage Ratio', 'Customer Growth'],
  'MD&A': ['Strategic Priorities', 'Risk Factors', 'Bank Outlook', 'Legal Issues']
};

export const MarketResearchModule = ({ onBack }: MarketResearchModuleProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('date');
  const [newQuestion, setNewQuestion] = useState('');
  const [selectedAnalysis, setSelectedAnalysis] = useState('');
  const [selectedDashboard, setSelectedDashboard] = useState('');
  const [selectedReport, setSelectedReport] = useState('');

  // Fetch data from the backend
  const { data: questionsData, isLoading: questionsLoading, error: questionsError } = useMarketQuestionsDemo();
  const { data: analysesData, isLoading: analysesLoading } = useAnalysesDemo();

  const questions: MarketQuestion[] = questionsData?.questions || [];
  const analyses = analysesData?.analyses || [];
  const analysisOptions = analyses.map(analysis => analysis.name);

  const filteredQuestions = questions.filter(q => 
    q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    q.analysis_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    q.report.toLowerCase().includes(searchTerm.toLowerCase())
  ).sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime(); // Most recent first
      case 'status':
        // Custom order: pending -> answered
        const statusOrder = { 'pending': 0, 'in-progress': 1, 'answered': 2, 'draft': 3 };
        return statusOrder[a.status] - statusOrder[b.status];
      case 'analysis':
        return a.analysis_name.localeCompare(b.analysis_name); // Alphabetical order
      default:
        return 0;
    }
  });

  const availableReports = selectedDashboard ? reportOptions[selectedDashboard as keyof typeof reportOptions] || [] : [];

  const submitQuestion = () => {
    if (newQuestion.trim() && selectedAnalysis && selectedDashboard && selectedReport) {
      // Logic to submit new question (will be implemented when API endpoints are ready)
      console.log('Submitting question:', { 
        question: newQuestion, 
        analysis: selectedAnalysis,
        dashboard: selectedDashboard,
        report: selectedReport
      });
      setNewQuestion('');
      setSelectedAnalysis('');
      setSelectedDashboard('');
      setSelectedReport('');
    }
  };

  const handleDashboardChange = (dashboard: string) => {
    setSelectedDashboard(dashboard);
    setSelectedReport(''); // Reset report when dashboard changes
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'answered': return 'bg-emerald-100 text-emerald-700 border-emerald-200';
      case 'in-progress': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'pending': return 'bg-amber-100 text-amber-700 border-amber-200';
      case 'draft': return 'bg-gray-100 text-gray-700 border-gray-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-700 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-700 border-green-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  // Error state
  if (questionsError) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={onBack} className="text-slate-600">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Analyses
          </Button>
          <div>
            <h2 className="text-3xl font-bold text-slate-900">Market Research Q&A</h2>
            <p className="text-slate-600">Questions sent to external analysts and their responses</p>
          </div>
        </div>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-center p-8">
              <div className="text-center">
                <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-slate-900 mb-2">Failed to Load Questions</h3>
                <p className="text-slate-600 mb-4">
                  Unable to connect to the backend. Please make sure the backend server is running on localhost:5000.
                </p>
                <p className="text-sm text-slate-500">
                  Error: {questionsError?.message || 'Unknown error'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Button variant="ghost" onClick={onBack} className="text-slate-600">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Analyses
        </Button>
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Market Research Q&A</h2>
          <p className="text-slate-600">Questions sent to external analysts and their responses</p>
        </div>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <Input
                placeholder="Search questions, analyses, or reports..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-40">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="date">Date</SelectItem>
                <SelectItem value="status">Status</SelectItem>
                <SelectItem value="analysis">Analysis</SelectItem>
                <SelectItem value="user">User</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Submit New Question */}
      <Card>
        <CardHeader>
          <CardTitle>Submit New Research Question</CardTitle>
          <CardDescription>Send a question to external market research analysts</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium text-slate-900 mb-2 block">Related Analysis *</label>
              <Select value={selectedAnalysis} onValueChange={setSelectedAnalysis}>
                <SelectTrigger>
                  <SelectValue placeholder="Select analysis..." />
                </SelectTrigger>
                <SelectContent>
                  {analysisOptions.map((analysis) => (
                    <SelectItem key={analysis} value={analysis}>{analysis}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium text-slate-900 mb-2 block">Dashboard *</label>
              <Select value={selectedDashboard} onValueChange={handleDashboardChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select dashboard..." />
                </SelectTrigger>
                <SelectContent>
                  {dashboardOptions.map((dashboard) => (
                    <SelectItem key={dashboard} value={dashboard}>{dashboard}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium text-slate-900 mb-2 block">Report *</label>
              <Select value={selectedReport} onValueChange={setSelectedReport} disabled={!selectedDashboard}>
                <SelectTrigger>
                  <SelectValue placeholder="Select report..." />
                </SelectTrigger>
                <SelectContent>
                  {availableReports.map((report) => (
                    <SelectItem key={report} value={report}>{report}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div>
            <label className="text-sm font-medium text-slate-900 mb-2 block">Question *</label>
            <Textarea
              value={newQuestion}
              onChange={(e) => setNewQuestion(e.target.value)}
              placeholder="What specific information do you need from external researchers?"
              rows={3}
            />
          </div>
          <Button 
            onClick={submitQuestion}
            disabled={!newQuestion.trim() || !selectedAnalysis || !selectedDashboard || !selectedReport}
            className="bg-slate-700 hover:bg-slate-800"
          >
            <Send className="h-4 w-4 mr-2" />
            Submit Question
          </Button>
        </CardContent>
      </Card>

      {/* Loading state */}
      {questionsLoading && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-center p-8">
              <Loader2 className="h-8 w-8 animate-spin text-slate-500" />
              <span className="ml-2 text-slate-600">Loading questions...</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Questions List */}
      {!questionsLoading && (
        <div className="space-y-4">
          {filteredQuestions.map((question) => (
            <Card key={question.id} className="border-slate-200">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant="outline">{question.analysis_name}</Badge>
                      <Badge variant="secondary">{question.dashboard}</Badge>
                      <Badge variant="secondary">{question.report}</Badge>
                      <Badge className={getStatusColor(question.status)}>
                        {question.status}
                      </Badge>
                    </div>
                    <CardTitle className="text-base text-slate-900 mb-2">{question.question}</CardTitle>
                    <div className="flex items-center text-sm text-slate-600 space-x-4">
                      <div className="flex items-center">
                        <User className="h-4 w-4 mr-1" />
                        External Analyst
                      </div>
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 mr-1" />
                        {formatDate(question.created_at)}
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              
              {question.responses.length > 0 && (
                <CardContent>
                  <div className="space-y-4">
                    {question.responses.map((response, index) => (
                      <div key={index} className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                        <div className="flex justify-between items-center mb-2">
                          <div className="flex items-center space-x-2">
                            <User className="h-4 w-4 text-slate-600" />
                            <span className="font-medium text-slate-900">{response.analyst}</span>
                            <span className="text-sm text-slate-500">
                              {formatTime(response.timestamp)}
                            </span>
                          </div>
                        </div>
                        <p className="text-slate-700 text-sm mb-3">{response.response}</p>
                        
                        {response.attachments && response.attachments.length > 0 && (
                          <div className="flex flex-wrap gap-2">
                            {response.attachments.map((attachment, aIndex) => (
                              <div key={aIndex} className="flex items-center text-xs text-blue-600 hover:text-blue-800 cursor-pointer">
                                <FileText className="h-3 w-3 mr-1" />
                                {attachment}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              )}
            </Card>
          ))}

          {filteredQuestions.length === 0 && (
            <Card className="text-center py-12">
              <CardContent>
                <MessageSquare className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-slate-900 mb-2">No questions found</h3>
                <p className="text-slate-600">Submit your first research question to get started</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};
