
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, ExternalLink, Edit } from 'lucide-react';
import { Button } from '@/components/ui/button';

const cashFlowData = [
  { quarter: 'Q1 2023', ourBank: 2.1, bankOfAmerica: 1.8, wellsFargo: 1.9, jpmorgan: 2.3 },
  { quarter: 'Q2 2023', ourBank: 2.3, bankOfAmerica: 2.0, wellsFargo: 2.1, jpmorgan: 2.5 },
  { quarter: 'Q3 2023', ourBank: 2.5, bankOfAmerica: 2.2, wellsFargo: 2.3, jpmorgan: 2.7 },
  { quarter: 'Q4 2023', ourBank: 2.8, bankOfAmerica: 2.4, wellsFargo: 2.5, jpmorgan: 2.9 },
  { quarter: 'Q1 2024', ourBank: 3.0, bankOfAmerica: 2.6, wellsFargo: 2.7, jpmorgan: 3.1 },
  { quarter: 'Q2 2024', ourBank: 3.2, bankOfAmerica: 2.8, wellsFargo: 2.9, jpmorgan: 3.3 }
];

interface CashFlowDashboardProps {
  analysis: any;
}

export const CashFlowDashboard = ({ analysis }: CashFlowDashboardProps) => {
  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Operating Cash Flow</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">$3.2B</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">+18% YoY growth</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Cash Flow Statement
              </button>
              <Button variant="ghost" size="sm" className="text-xs h-6 px-2">
                <Edit className="h-3 w-3 mr-1" />
                Correct
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Free Cash Flow</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">$2.8B</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Strong generation</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Financial Analysis
              </button>
              <Button variant="ghost" size="sm" className="text-xs h-6 px-2">
                <Edit className="h-3 w-3 mr-1" />
                Correct
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Cash Conversion</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">92%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Excellent efficiency</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Operational Metrics
              </button>
              <Button variant="ghost" size="sm" className="text-xs h-6 px-2">
                <Edit className="h-3 w-3 mr-1" />
                Correct
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Operating Cash Flow Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Operating Cash Flow Comparison</CardTitle>
          <CardDescription>6-quarter operating cash flow trends vs. competitors ($B)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={cashFlowData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="quarter" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }} 
                />
                <Legend />
                <Line type="monotone" dataKey="ourBank" stroke="#1e293b" strokeWidth={3} name="Our Bank" />
                <Line type="monotone" dataKey="bankOfAmerica" stroke="#64748b" strokeWidth={2} name="Bank of America" />
                <Line type="monotone" dataKey="wellsFargo" stroke="#94a3b8" strokeWidth={2} name="Wells Fargo" />
                <Line type="monotone" dataKey="jpmorgan" stroke="#cbd5e1" strokeWidth={2} name="JPMorgan Chase" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
