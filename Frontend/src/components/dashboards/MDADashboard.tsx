
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExternalLink, Edit, AlertTriangle, Target, TrendingUp, Shield } from 'lucide-react';

interface MDADashboardProps {
  analysis: any;
}

export const MDADashboard = ({ analysis }: MDADashboardProps) => {
  const strategicPriorities = [
    {
      bank: 'Our Bank',
      priorities: [
        'Digital transformation and mobile banking expansion',
        'Commercial lending growth in mid-market segment',
        'Enhanced cybersecurity and risk management',
        'Branch optimization and cost reduction'
      ]
    },
    {
      bank: 'Bank of America',
      priorities: [
        'Technology infrastructure modernization',
        'ESG initiatives and sustainable finance',
        'Wealth management expansion',
        'Credit card portfolio growth'
      ]
    },
    {
      bank: 'Wells Fargo',
      priorities: [
        'Regulatory compliance and risk remediation',
        'Digital platform enhancement',
        'Customer experience improvement',
        'Operational efficiency programs'
      ]
    }
  ];

  const riskFactors = [
    {
      bank: 'Our Bank',
      risks: [
        { risk: 'Interest rate volatility', mitigation: 'Active ALM and hedging strategies' },
        { risk: 'Credit risk in commercial portfolio', mitigation: 'Enhanced underwriting standards' },
        { risk: 'Cybersecurity threats', mitigation: 'Multi-layered security framework' }
      ]
    },
    {
      bank: 'Bank of America',
      risks: [
        { risk: 'Regulatory capital requirements', mitigation: 'Capital optimization initiatives' },
        { risk: 'Market volatility impact', mitigation: 'Diversified revenue streams' }
      ]
    }
  ];

  const outlooks = [
    {
      bank: 'Our Bank',
      outlook: 'Positive',
      description: 'Strong fundamentals with projected 8-10% loan growth and continued NIM expansion',
      keyPoints: [
        'Expect continued market share gains in commercial lending',
        'Digital transformation driving efficiency improvements',
        'Credit quality expected to remain strong'
      ]
    },
    {
      bank: 'Bank of America',
      outlook: 'Stable',
      description: 'Steady performance expected with focus on operational efficiency',
      keyPoints: [
        'Technology investments showing returns',
        'Wealth management driving fee income growth'
      ]
    }
  ];

  return (
    <div className="space-y-6">
      {/* Strategic Priorities */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="flex items-center">
                <Target className="h-5 w-5 mr-2 text-slate-700" />
                Strategic Priorities
              </CardTitle>
              <CardDescription>Key strategic focus areas by institution</CardDescription>
            </div>
            <Button variant="ghost" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Suggest Correction
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {strategicPriorities.map((item, index) => (
              <div key={index} className="border-l-4 border-slate-200 pl-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-slate-900">{item.bank}</h4>
                  <button className="text-blue-600 hover:text-blue-800 flex items-center text-sm">
                    <ExternalLink className="h-3 w-3 mr-1" />
                    Source: Q4 Earnings Call
                  </button>
                </div>
                <ul className="space-y-2">
                  {item.priorities.map((priority, pIndex) => (
                    <li key={pIndex} className="flex items-start">
                      <div className="h-1.5 w-1.5 bg-slate-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                      <span className="text-slate-700 text-sm">{priority}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Risk Factors & Mitigations */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="flex items-center">
                <Shield className="h-5 w-5 mr-2 text-slate-700" />
                Risk Factors & Mitigations
              </CardTitle>
              <CardDescription>Key risks identified and management responses</CardDescription>
            </div>
            <Button variant="ghost" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Suggest Correction
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {riskFactors.map((item, index) => (
              <div key={index} className="border rounded-lg p-4 bg-slate-50">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-slate-900">{item.bank}</h4>
                  <button className="text-blue-600 hover:text-blue-800 flex items-center text-sm">
                    <ExternalLink className="h-3 w-3 mr-1" />
                    Source: 10-K Filing
                  </button>
                </div>
                <div className="space-y-3">
                  {item.risks.map((riskItem, rIndex) => (
                    <div key={rIndex} className="bg-white p-3 rounded border-l-4 border-orange-200">
                      <div className="flex items-start">
                        <AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 mr-2 flex-shrink-0" />
                        <div className="flex-1">
                          <h5 className="font-medium text-slate-900 text-sm">{riskItem.risk}</h5>
                          <p className="text-slate-600 text-sm mt-1">
                            <span className="font-medium">Mitigation:</span> {riskItem.mitigation}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Bank Outlook */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-slate-700" />
                Management Outlook
              </CardTitle>
              <CardDescription>Forward-looking statements and guidance</CardDescription>
            </div>
            <Button variant="ghost" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Suggest Correction
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {outlooks.map((item, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <h4 className="font-semibold text-slate-900">{item.bank}</h4>
                    <Badge 
                      className={`
                        ${item.outlook === 'Positive' ? 'bg-emerald-100 text-emerald-700 border-emerald-200' : 
                          item.outlook === 'Stable' ? 'bg-blue-100 text-blue-700 border-blue-200' : 
                          'bg-orange-100 text-orange-700 border-orange-200'}
                      `}
                    >
                      {item.outlook}
                    </Badge>
                  </div>
                  <button className="text-blue-600 hover:text-blue-800 flex items-center text-sm">
                    <ExternalLink className="h-3 w-3 mr-1" />
                    Source: Management Discussion
                  </button>
                </div>
                <p className="text-slate-700 mb-3">{item.description}</p>
                <ul className="space-y-1">
                  {item.keyPoints.map((point, pIndex) => (
                    <li key={pIndex} className="flex items-start">
                      <div className="h-1.5 w-1.5 bg-slate-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                      <span className="text-slate-600 text-sm">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Legal Issues */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2 text-slate-700" />
                Significant Legal Issues
              </CardTitle>
              <CardDescription>Ongoing legal matters and regulatory actions</CardDescription>
            </div>
            <Button variant="ghost" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Suggest Correction
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="border rounded-lg p-4 border-orange-200 bg-orange-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-slate-900">Wells Fargo</h4>
                <button className="text-blue-600 hover:text-blue-800 flex items-center text-sm">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  Source: Legal Disclosures
                </button>
              </div>
              <p className="text-slate-700 text-sm">
                Ongoing regulatory consent orders related to risk management and operational controls. 
                Estimated remediation costs of $2-3B over next 2 years.
              </p>
            </div>
            
            <div className="border rounded-lg p-4 border-slate-200 bg-slate-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-slate-900">Our Bank</h4>
                <button className="text-blue-600 hover:text-blue-800 flex items-center text-sm">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  Source: Quarterly Report
                </button>
              </div>
              <p className="text-slate-700 text-sm">
                No material legal proceedings or regulatory actions. Routine examination findings 
                addressed within normal business operations.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
