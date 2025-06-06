
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowLeft, TrendingUp, TrendingDown, AlertCircle, ExternalLink, FileText, MessageSquare, Download } from 'lucide-react';
import { IncomeStatementDashboard } from '@/components/dashboards/IncomeStatementDashboard';
import { BalanceSheetDashboard } from '@/components/dashboards/BalanceSheetDashboard';
import { CashFlowDashboard } from '@/components/dashboards/CashFlowDashboard';
import { KPIDashboard } from '@/components/dashboards/KPIDashboard';
import { MDADashboard } from '@/components/dashboards/MDADashboard';

interface AnalysisDashboardProps {
  analysis: any;
  onBack: () => void;
}

export const AnalysisDashboard = ({ analysis, onBack }: AnalysisDashboardProps) => {
  const [activeTab, setActiveTab] = useState('income');

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-600">No analysis selected</p>
        <Button onClick={onBack} className="mt-4">Back to Analyses</Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={onBack} className="text-slate-600">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Analyses
          </Button>
          <div>
            <h2 className="text-3xl font-bold text-slate-900">{analysis.name}</h2>
            <p className="text-slate-600 mt-1">{analysis.description}</p>
            <div className="flex items-center space-x-4 mt-2">
              <Badge variant="outline">{analysis.period}</Badge>
              <span className="text-sm text-slate-500">
                Created {new Date(analysis.dateCreated).toLocaleDateString()}
              </span>
              <Badge className="bg-emerald-100 text-emerald-700 border-emerald-200">
                {analysis.status.toUpperCase()}
              </Badge>
            </div>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export PDF
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export Excel
          </Button>
        </div>
      </div>

      {/* Competitors Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Analysis Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <h4 className="font-medium text-slate-900">Period</h4>
              <p className="text-2xl font-bold text-slate-700 mt-1">{analysis.period}</p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <h4 className="font-medium text-slate-900">Competitors</h4>
              <p className="text-2xl font-bold text-slate-700 mt-1">{analysis.competitors.length}</p>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <h4 className="font-medium text-slate-900">Reports Generated</h4>
              <p className="text-2xl font-bold text-slate-700 mt-1">15</p>
            </div>
          </div>
          
          <div className="mt-4">
            <h4 className="font-medium text-slate-900 mb-2">Analyzed Competitors</h4>
            <div className="flex flex-wrap gap-2">
              {analysis.competitors.map((competitor: string) => (
                <Badge key={competitor} variant="outline" className="text-sm">
                  {competitor}
                </Badge>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Dashboard Tabs */}
      <Card>
        <CardContent className="p-0">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <div className="border-b">
              <TabsList className="grid w-full grid-cols-5 h-auto p-1">
                <TabsTrigger value="income" className="data-[state=active]:bg-slate-100 py-3 px-4">
                  <div className="text-center">
                    <TrendingUp className="h-4 w-4 mx-auto mb-1" />
                    <span className="text-xs">Income Statement</span>
                  </div>
                </TabsTrigger>
                <TabsTrigger value="balance" className="data-[state=active]:bg-slate-100 py-3 px-4">
                  <div className="text-center">
                    <FileText className="h-4 w-4 mx-auto mb-1" />
                    <span className="text-xs">Balance Sheet</span>
                  </div>
                </TabsTrigger>
                <TabsTrigger value="cashflow" className="data-[state=active]:bg-slate-100 py-3 px-4">
                  <div className="text-center">
                    <TrendingDown className="h-4 w-4 mx-auto mb-1" />
                    <span className="text-xs">Cash Flow</span>
                  </div>
                </TabsTrigger>
                <TabsTrigger value="kpis" className="data-[state=active]:bg-slate-100 py-3 px-4">
                  <div className="text-center">
                    <TrendingUp className="h-4 w-4 mx-auto mb-1" />
                    <span className="text-xs">KPIs & Ratios</span>
                  </div>
                </TabsTrigger>
                <TabsTrigger value="mda" className="data-[state=active]:bg-slate-100 py-3 px-4">
                  <div className="text-center">
                    <MessageSquare className="h-4 w-4 mx-auto mb-1" />
                    <span className="text-xs">MD&A</span>
                  </div>
                </TabsTrigger>
              </TabsList>
            </div>

            <div className="p-6">
              <TabsContent value="income" className="m-0">
                <IncomeStatementDashboard analysis={analysis} />
              </TabsContent>
              <TabsContent value="balance" className="m-0">
                <BalanceSheetDashboard analysis={analysis} />
              </TabsContent>
              <TabsContent value="cashflow" className="m-0">
                <CashFlowDashboard analysis={analysis} />
              </TabsContent>
              <TabsContent value="kpis" className="m-0">
                <KPIDashboard analysis={analysis} />
              </TabsContent>
              <TabsContent value="mda" className="m-0">
                <MDADashboard analysis={analysis} />
              </TabsContent>
            </div>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};
