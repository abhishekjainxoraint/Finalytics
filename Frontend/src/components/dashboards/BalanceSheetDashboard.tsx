
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, ExternalLink, Edit } from 'lucide-react';
import { Button } from '@/components/ui/button';

const assetData = [
  { quarter: 'Q1 2023', loans: 85, securities: 10, cash: 5 },
  { quarter: 'Q2 2023', loans: 87, securities: 9, cash: 4 },
  { quarter: 'Q3 2023', loans: 89, securities: 8, cash: 3 },
  { quarter: 'Q4 2023', loans: 91, securities: 7, cash: 2 },
  { quarter: 'Q1 2024', loans: 93, securities: 6, cash: 1 },
  { quarter: 'Q2 2024', loans: 94, securities: 5, cash: 1 }
];

interface BalanceSheetDashboardProps {
  analysis: any;
}

export const BalanceSheetDashboard = ({ analysis }: BalanceSheetDashboardProps) => {
  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Asset Growth</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">8.2%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">vs. 6.1% peer avg</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Balance Sheet, Page 8
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
            <CardTitle className="text-base">Capital Ratio</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">14.8%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Well-capitalized</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Regulatory Report
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
            <CardTitle className="text-base">Loan-to-Deposit</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">78%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Optimal range</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Q4 Earnings Report
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
            <CardTitle className="text-base">Deposit Growth</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-slate-900">5.4%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">vs. 3.2% peer avg</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Deposit Analysis
              </button>
              <Button variant="ghost" size="sm" className="text-xs h-6 px-2">
                <Edit className="h-3 w-3 mr-1" />
                Correct
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Asset Composition Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Asset Composition Trends</CardTitle>
          <CardDescription>Portfolio composition over the last 6 quarters</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={assetData}>
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
                <Bar dataKey="loans" stackId="a" fill="#1e293b" name="Loans" />
                <Bar dataKey="securities" stackId="a" fill="#0d9488" name="Securities" />
                <Bar dataKey="cash" stackId="a" fill="#64748b" name="Cash & Equivalents" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
