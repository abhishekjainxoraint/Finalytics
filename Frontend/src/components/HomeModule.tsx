import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Plus, Search, Calendar, FileText, TrendingUp, MoreHorizontal, Filter, Loader2, AlertCircle } from 'lucide-react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { useAnalysesDemo } from '@/hooks/useAnalyses';
import { Analysis } from '@/lib/api';

interface HomeModuleProps {
  onCreateNew: () => void;
  onViewAnalysis: (analysis: Analysis) => void;
}

export const HomeModule = ({ onCreateNew, onViewAnalysis }: HomeModuleProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  // Fetch analyses from the backend
  const { data, isLoading, error, isError } = useAnalysesDemo();

  // Transform backend data to match frontend interface
  const analyses: Analysis[] = data?.analyses || [];

  const filteredAnalyses = analyses.filter(analysis => {
    const matchesSearch = analysis.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         analysis.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || analysis.status === statusFilter;
    return matchesSearch && matchesStatus;
  }).sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime(); // Most recent first
      case 'name':
        return a.name.localeCompare(b.name); // Alphabetical order
      case 'status':
        // Custom order: completed -> in-progress -> draft
        const statusOrder = { 'completed': 0, 'in-progress': 1, 'draft': 2 };
        return statusOrder[a.status] - statusOrder[b.status];
      default:
        return 0;
    }
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-emerald-100 text-emerald-700 border-emerald-200';
      case 'in-progress': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'draft': return 'bg-gray-100 text-gray-700 border-gray-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  // Error state
  if (isError) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-3xl font-bold text-slate-900">Financial Analyses</h2>
            <p className="text-slate-600 mt-1">Compare your bank's performance with competitors using AI-powered insights</p>
          </div>
          <Button onClick={onCreateNew} className="bg-slate-700 hover:bg-slate-800 text-white">
            <Plus className="h-4 w-4 mr-2" />
            Create New Analysis
          </Button>
        </div>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-center p-8">
              <div className="text-center">
                <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-slate-900 mb-2">Failed to Load Analyses</h3>
                <p className="text-slate-600 mb-4">
                  Unable to connect to the backend. Please make sure the backend server is running on localhost:5000.
                </p>
                <p className="text-sm text-slate-500">
                  Error: {error?.message || 'Unknown error'}
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
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold text-slate-900">Financial Analyses</h2>
          <p className="text-slate-600 mt-1">Compare your bank's performance with competitors using AI-powered insights</p>
        </div>
        <Button onClick={onCreateNew} className="bg-slate-700 hover:bg-slate-800 text-white">
          <Plus className="h-4 w-4 mr-2" />
          Create New Analysis
        </Button>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                <Input
                  placeholder="Search analyses..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-40">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="in-progress">In Progress</SelectItem>
                  <SelectItem value="draft">Draft</SelectItem>
                </SelectContent>
              </Select>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="date">Date Created</SelectItem>
                  <SelectItem value="name">Name</SelectItem>
                  <SelectItem value="status">Status</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Loading state */}
      {isLoading && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-center p-8">
              <Loader2 className="h-8 w-8 animate-spin text-slate-500" />
              <span className="ml-2 text-slate-600">Loading analyses...</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Analyses Grid */}
      {!isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAnalyses.length === 0 ? (
            <div className="col-span-full">
              <Card>
                <CardContent className="pt-6">
                  <div className="text-center p-8">
                    <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-slate-900 mb-2">No Analyses Found</h3>
                    <p className="text-slate-600 mb-4">
                      {searchTerm || statusFilter !== 'all' 
                        ? 'No analyses match your current filters.' 
                        : 'Get started by creating your first analysis.'}
                    </p>
                    <Button onClick={onCreateNew} className="bg-slate-700 hover:bg-slate-800 text-white">
                      <Plus className="h-4 w-4 mr-2" />
                      Create New Analysis
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          ) : (
            filteredAnalyses.map((analysis) => (
              <Card key={analysis.id} className="hover:shadow-lg transition-shadow cursor-pointer border-slate-200">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-lg text-slate-900 mb-2">{analysis.name}</CardTitle>
                      <Badge className={`text-xs ${getStatusColor(analysis.status)}`}>
                        {analysis.status.replace('-', ' ').toUpperCase()}
                      </Badge>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => onViewAnalysis(analysis)}>
                          View Analysis
                        </DropdownMenuItem>
                        <DropdownMenuItem>Edit Metadata</DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600">Delete</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-slate-600 mb-4 line-clamp-2">
                    {analysis.description}
                  </CardDescription>
                  
                  <div className="space-y-3">
                    <div className="flex items-center text-sm text-slate-500">
                      <Calendar className="h-4 w-4 mr-2" />
                      <span>{analysis.period}</span>
                    </div>
                    
                    <div className="flex items-center text-sm text-slate-500">
                      <FileText className="h-4 w-4 mr-2" />
                      <span>Created {formatDate(analysis.created_at)}</span>
                    </div>

                    {analysis.competitors && analysis.competitors.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-3">
                        <span className="text-xs text-slate-500 mr-2">Competitors:</span>
                        {analysis.competitors.slice(0, 2).map((competitor) => (
                          <Badge key={competitor.name} variant="outline" className="text-xs">
                            {competitor.name}
                          </Badge>
                        ))}
                        {analysis.competitors.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{analysis.competitors.length - 2} more
                          </Badge>
                        )}
                      </div>
                    )}

                    {analysis.status === 'in-progress' && analysis.progress && (
                      <div className="mt-3">
                        <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                          <span>Progress</span>
                          <span>{analysis.progress}%</span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full transition-all duration-300" 
                            style={{ width: `${analysis.progress}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100">
                    <Button 
                      onClick={() => onViewAnalysis(analysis)} 
                      variant="outline" 
                      size="sm" 
                      className="w-full"
                    >
                      <TrendingUp className="h-4 w-4 mr-2" />
                      View Analysis
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
};
