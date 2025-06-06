
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, ExternalLink, Edit } from 'lucide-react';
import { Button } from '@/components/ui/button';

const kpiData = [
  { quarter: 'Q1 2023', npl: 1.2, lcr: 115, cac: 250, customerGrowth: 5.2 },
  { quarter: 'Q2 2023', npl: 1.1, lcr: 118, cac: 245, customerGrowth: 5.8 },
  { quarter: 'Q3 2023', npl: 1.0, lcr: 122, cac: 240, customerGrowth: 6.1 },
  { quarter: 'Q4 2023', npl: 0.9, lcr: 125, cac: 235, customerGrowth: 6.5 },
  { quarter: 'Q1 2024', npl: 0.8, lcr: 128, cac: 230, customerGrowth: 7.2 },
  { quarter: 'Q2 2024', npl: 0.7, lcr: 132, cac: 225, customerGrowth: 7.8 }
];

interface KPIDashboardProps {
  analysis: any;
}

export const KPIDashboard = ({ analysis }: KPIDashboardProps) => {
  return (
    <div className="space-y-6">
      {/* Key KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">NPL Ratio</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-emerald-700">0.7%</span>
              <TrendingDown className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">vs. 1.2% peer avg</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Credit Risk Report
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
            <CardTitle className="text-base">Customer Acq. Cost</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-emerald-700">$225</span>
              <TrendingDown className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">-10% YoY improvement</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Marketing Analytics
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
            <CardTitle className="text-base">LCR</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-emerald-700">132%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Well above requirement</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Liquidity Report
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
            <CardTitle className="text-base">Customer Growth</CardTitle>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-emerald-700">7.8%</span>
              <TrendingUp className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Strong acquisition</p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex justify-between items-center text-xs">
              <button className="text-blue-600 hover:text-blue-800 flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Customer Metrics
              </button>
              <Button variant="ghost" size="sm" className="text-xs h-6 px-2">
                <Edit className="h-3 w-3 mr-1" />
                Correct
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Customer Growth Trend */}
      <Card>
        <CardHeader>
          <CardTitle>Customer Growth Trends</CardTitle>
          <CardDescription>Customer acquisition and retention metrics over 6 quarters (%)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={kpiData}>
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
                <Area type="monotone" dataKey="customerGrowth" stroke="#0d9488" fill="#0d9488" fillOpacity={0.6} name="Customer Growth %" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
