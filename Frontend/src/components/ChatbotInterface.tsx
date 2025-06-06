
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { X, Send, MessageSquare, Bot, User, FileText, ExternalLink } from 'lucide-react';

interface ChatbotInterfaceProps {
  onClose: () => void;
  analysis: any;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: Array<{
    document: string;
    page: number;
    snippet: string;
  }>;
}

const initialMessages: Message[] = [
  {
    id: '1',
    type: 'assistant',
    content: 'Hello! I\'m your AI assistant for financial analysis. I can help you explore your data, answer questions about your analyses, and provide insights from your documents. What would you like to know?',
    timestamp: new Date().toISOString()
  }
];

export const ChatbotInterface = ({ onClose, analysis }: ChatbotInterfaceProps) => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: newMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setNewMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: getAIResponse(newMessage),
        timestamp: new Date().toISOString(),
        sources: [
          {
            document: 'Q4 2024 Earnings Report',
            page: 15,
            snippet: 'Revenue grew 12.5% year-over-year driven by strong commercial lending activity...'
          },
          {
            document: 'Competitor Analysis - JPMorgan',
            page: 8,
            snippet: 'JPMorgan\'s net interest margin improved to 5.7% in Q4 2024...'
          }
        ]
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const getAIResponse = (userInput: string): string => {
    const input = userInput.toLowerCase();
    
    if (input.includes('revenue') || input.includes('growth')) {
      return 'Based on your Q4 2024 analysis, your bank\'s revenue growth of 12.5% outperformed the industry average of 8.2%. This was primarily driven by commercial lending expansion and improved net interest margins. Compared to competitors, you\'re performing well - JPMorgan achieved 10.8% growth while Wells Fargo saw 7.3%.';
    } else if (input.includes('efficiency') || input.includes('ratio')) {
      return 'Your efficiency ratio of 62% shows room for improvement compared to the peer average of 59%. However, the trend is positive with a 200 basis point improvement over the last 6 quarters. JPMorgan leads with 57%, suggesting opportunities in operational optimization.';
    } else if (input.includes('npl') || input.includes('credit')) {
      return 'Your NPL ratio of 0.7% is excellent, well below the peer average of 1.2%. This indicates strong credit quality and risk management. Your conservative underwriting standards have paid off, especially compared to some competitors who are seeing credit stress.';
    } else {
      return 'I can help you analyze various aspects of your financial performance. You can ask me about revenue growth, profitability metrics, efficiency ratios, credit quality, or comparisons with specific competitors. What specific area would you like to explore?';
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-end z-50">
      <div className="w-96 h-full bg-white shadow-xl flex flex-col">
        {/* Header */}
        <div className="border-b border-slate-200 p-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Bot className="h-5 w-5 text-slate-700" />
              <h3 className="font-semibold text-slate-900">AI Assistant</h3>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
          {analysis && (
            <div className="mt-2">
              <Badge variant="outline" className="text-xs">{analysis.name}</Badge>
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] rounded-lg p-3 ${
                message.type === 'user' 
                  ? 'bg-slate-700 text-white' 
                  : 'bg-slate-100 text-slate-900'
              }`}>
                <div className="flex items-start space-x-2">
                  {message.type === 'assistant' && (
                    <Bot className="h-4 w-4 mt-0.5 text-slate-600" />
                  )}
                  {message.type === 'user' && (
                    <User className="h-4 w-4 mt-0.5 text-white" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm">{message.content}</p>
                    <span className={`text-xs mt-2 block ${
                      message.type === 'user' ? 'text-slate-300' : 'text-slate-500'
                    }`}>
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
                
                {/* Sources */}
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-200">
                    <p className="text-xs font-medium text-slate-600 mb-2">Sources:</p>
                    <div className="space-y-2">
                      {message.sources.map((source, index) => (
                        <div key={index} className="bg-white border border-slate-200 rounded p-2">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-medium text-slate-700">{source.document}</span>
                            <button className="text-blue-600 hover:text-blue-800">
                              <ExternalLink className="h-3 w-3" />
                            </button>
                          </div>
                          <p className="text-xs text-slate-600">Page {source.page}</p>
                          <p className="text-xs text-slate-500 mt-1 italic">"{source.snippet}"</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-slate-100 rounded-lg p-3 max-w-[80%]">
                <div className="flex items-center space-x-2">
                  <Bot className="h-4 w-4 text-slate-600" />
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-pulse delay-75"></div>
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-pulse delay-150"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-slate-200 p-4">
          <div className="flex space-x-2">
            <Input
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Ask about your analysis..."
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1"
            />
            <Button onClick={sendMessage} disabled={!newMessage.trim() || isTyping} size="sm">
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p className="text-xs text-slate-500 mt-2">
            Ask me about revenue trends, efficiency ratios, competitor comparisons, or any insights from your documents.
          </p>
        </div>
      </div>
    </div>
  );
};
