
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { TrendingUp, TrendingDown, AlertCircle, ExternalLink, Edit, CheckCircle } from 'lucide-react';
import { CorrectionDialog } from '@/components/CorrectionDialog';

const mockData = [
  { quarter: 'Q1 2023', ourBank: 4.2, bankOfAmerica: 4.8, wellsFargo: 4.1, jpmorgan: 5.2 },
  { quarter: 'Q2 2023', ourBank: 4.5, bankOfAmerica: 4.9, wellsFargo: 4.3, jpmorgan: 5.1 },
  { quarter: 'Q3 2023', ourBank: 4.8, bankOfAmerica: 5.1, wellsFargo: 4.5, jpmorgan: 5.3 },
  { quarter: 'Q4 2023', ourBank: 5.1, bankOfAmerica: 5.3, wellsFargo: 4.7, jpmorgan: 5.5 },
  { quarter: 'Q1 2024', ourBank: 5.3, bankOfAmerica: 5.4, wellsFargo: 4.9, jpmorgan: 5.7 },
  { quarter: 'Q2 2024', ourBank: 5.6, bankOfAmerica: 5.6, wellsFargo: 5.1, jpmorgan: 5.9 }
];

const expenseData = [
  { quarter: 'Q1 2023', ourBank: 67, bankOfAmerica: 65, wellsFargo: 69, jpmorgan: 62 },
  { quarter: 'Q2 2023', ourBank: 66, bankOfAmerica: 64, wellsFargo: 68, jpmorgan: 61 },
  { quarter: 'Q3 2023', ourBank: 65, bankOfAmerica: 63, wellsFargo: 67, jpmorgan: 60 },
  { quarter: 'Q4 2023', ourBank: 64, bankOfAmerica: 62, wellsFargo: 66, jpmorgan: 59 },
  { quarter: 'Q1 2024', ourBank: 63, bankOfAmerica: 61, wellsFargo: 65, jpmorgan: 58 },
  { quarter: 'Q2 2024', ourBank: 62, bankOfAmerica: 60, wellsFargo: 64, jpmorgan: 57 }
];

interface Report {
  id: string;
  title: string;
  description: string;
  trend: 'up' | 'down' | 'neutral';
  value: string;
  comparison: string;
  citation: string;
  hasCorrection: boolean;
}

const reports: Report[] = [
  {
    id: '1',
    title: 'Revenue Growth',
    description: 'Year-over-year revenue growth trending positively against competitors',
    trend: 'up',
    value: '12.5%',
    comparison: 'vs. 8.2% industry avg',
    citation: 'Q4 2024 Earnings Report, Page 15',
    hasCorrection: false
  },
  {
    id: '2', 
    title: 'Net Interest Margin',
    description: 'NIM performance showing steady improvement over 6 quarters',
    trend: 'up',
    value: '5.6%',
    comparison: 'vs. 5.4% competitor avg',
    citation: 'Q4 2024 10-K Filing, Page 42',
    hasCorrection: true
  },
  {
    id: '3',
    title: 'Efficiency Ratio',
    description: 'Operating efficiency improved but still above peer average',
    trend: 'down',
    value: '62%',
    comparison: 'vs. 59% peer avg',
    citation: 'Q4 2024 Earnings Call Transcript',
    hasCorrection: false
  }
];

interface IncomeStatementDashboardProps {
  analysis: any;
}

export const IncomeStatementDashboard = ({ analysis }: IncomeStatementDashboardProps) => {
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [showCorrectionDialog, setShowCorrectionDialog] = useState(false);

  const handleSuggestCorrection = (report: Report) => {
    setSelectedReport(report);
    setShowCorrectionDialog(true);
  };

  return (
    <div className="space-y-6">
      {/* Key Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {reports.map((report) => (
          <Card key={report.id} className="relative">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <CardTitle className="text-base text-slate-900 mb-1">{report.title}</CardTitle>
                  <div className="flex items-center space-x-2">
                    <span className="text-2xl font-bold text-slate-900">{report.value}</span>
                    {report.trend === 'up' ? (
                      <TrendingUp className="h-4 w-4 text-emerald-600" />
                    ) : report.trend === 'down' ? (
                      <TrendingDown className="h-4 w-4 text-red-500" />
                    ) : (
                      <div className="h-4 w-4" />
                    )}
                  </div>
                  <p className="text-sm text-slate-600">{report.comparison}</p>
                </div>
                {report.hasCorrection && (
                  <Badge variant="secondary" className="bg-orange-100 text-orange-700 text-xs">
                    Corrected
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              <p className="text-sm text-slate-600 mb-3">{report.description}</p>
              <div className="flex justify-between items-center text-xs">
                <button className="text-blue-600 hover:text-blue-800 flex items-center">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  {report.citation}
                </button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => handleSuggestCorrection(report)}
                  className="text-xs h-6 px-2"
                >
                  <Edit className="h-3 w-3 mr-1" />
                  Correct
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Revenue Growth Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Revenue Growth Trend</CardTitle>
          <CardDescription>6-quarter revenue performance comparison</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockData}>
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

      {/* Expense Ratios Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Efficiency Ratio Trends</CardTitle>
          <CardDescription>Operating expense ratios - lower is better</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={expenseData}>
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
                <Area type="monotone" dataKey="ourBank" stackId="1" stroke="#1e293b" fill="#1e293b" fillOpacity={0.8} name="Our Bank" />
                <Area type="monotone" dataKey="bankOfAmerica" stackId="2" stroke="#64748b" fill="#64748b" fillOpacity={0.6} name="Bank of America" />
                <Area type="monotone" dataKey="wellsFargo" stackId="3" stroke="#94a3b8" fill="#94a3b8" fillOpacity={0.6} name="Wells Fargo" />
                <Area type="monotone" dataKey="jpmorgan" stackId="4" stroke="#cbd5e1" fill="#cbd5e1" fillOpacity={0.6} name="JPMorgan Chase" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Net Interest Margin Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>Net Interest Margin Analysis</CardTitle>
          <CardDescription>Quarterly NIM performance vs. peer banks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockData}>
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
                <Bar dataKey="ourBank" fill="#0d9488" name="Our Bank" />
                <Bar dataKey="bankOfAmerica" fill="#64748b" name="Bank of America" />
                <Bar dataKey="wellsFargo" fill="#94a3b8" name="Wells Fargo" />
                <Bar dataKey="jpmorgan" fill="#cbd5e1" name="JPMorgan Chase" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Correction Dialog */}
      {showCorrectionDialog && selectedReport && (
        <CorrectionDialog
          report={selectedReport}
          onClose={() => setShowCorrectionDialog(false)}
          onSubmit={(correction) => {
            console.log('Correction submitted:', correction);
            setShowCorrectionDialog(false);
          }}
        />
      )}
    </div>
  );
};
