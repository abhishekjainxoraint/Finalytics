
import React, { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { FileText, Upload, CheckCircle } from 'lucide-react';

interface CorrectionDialogProps {
  report: {
    id: string;
    title: string;
    citation: string;
  };
  onClose: () => void;
  onSubmit: (correction: any) => void;
}

export const CorrectionDialog = ({ report, onClose, onSubmit }: CorrectionDialogProps) => {
  const [selectedPages, setSelectedPages] = useState<number[]>([]);
  const [correctionNotes, setCorrectionNotes] = useState('');
  const [pageInput, setPageInput] = useState('');

  const addPage = () => {
    const pageNum = parseInt(pageInput);
    if (pageNum && !selectedPages.includes(pageNum)) {
      setSelectedPages([...selectedPages, pageNum].sort((a, b) => a - b));
      setPageInput('');
    }
  };

  const removePage = (pageNum: number) => {
    setSelectedPages(selectedPages.filter(p => p !== pageNum));
  };

  const handleSubmit = () => {
    onSubmit({
      reportId: report.id,
      pages: selectedPages,
      notes: correctionNotes,
      timestamp: new Date().toISOString(),
      user: 'John Analyst'
    });
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Suggest Correction</DialogTitle>
          <DialogDescription>
            Review and correct the source information for "{report.title}"
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Document Viewer */}
          <div>
            <Label className="text-sm font-medium text-slate-900">Source Document</Label>
            <div className="mt-2 border border-slate-200 rounded-lg p-4 bg-slate-50">
              <div className="flex items-center space-x-2 mb-3">
                <FileText className="h-4 w-4 text-slate-600" />
                <span className="text-sm text-slate-900">{report.citation}</span>
              </div>
              <div className="bg-white border border-slate-200 rounded h-48 flex items-center justify-center">
                <div className="text-center">
                  <FileText className="h-12 w-12 text-slate-400 mx-auto mb-2" />
                  <p className="text-sm text-slate-600">PDF Viewer</p>
                  <p className="text-xs text-slate-500">Document would be displayed here</p>
                </div>
              </div>
            </div>
          </div>

          {/* Page Selection */}
          <div>
            <Label className="text-sm font-medium text-slate-900">Select Relevant Pages</Label>
            <div className="mt-2 flex gap-2">
              <Input
                value={pageInput}
                onChange={(e) => setPageInput(e.target.value)}
                placeholder="Page number"
                type="number"
                className="w-32"
              />
              <Button onClick={addPage} variant="outline" size="sm">
                Add Page
              </Button>
            </div>
            {selectedPages.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {selectedPages.map(page => (
                  <Badge 
                    key={page} 
                    variant="secondary" 
                    className="cursor-pointer hover:bg-red-100 hover:text-red-700"
                    onClick={() => removePage(page)}
                  >
                    Page {page} ×
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Correction Instructions */}
          <div>
            <Label htmlFor="correction-notes" className="text-sm font-medium text-slate-900">
              Correction Instructions
            </Label>
            <Textarea
              id="correction-notes"
              value={correctionNotes}
              onChange={(e) => setCorrectionNotes(e.target.value)}
              placeholder="Describe what needs to be corrected and provide the accurate information..."
              rows={4}
              className="mt-2"
            />
          </div>

          {/* Additional Documents */}
          <div>
            <Label className="text-sm font-medium text-slate-900">Additional Supporting Documents</Label>
            <div className="mt-2 border-2 border-dashed border-slate-300 rounded-lg p-4 text-center">
              <Upload className="h-6 w-6 text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-600 mb-2">Upload additional documents to support the correction</p>
              <Button variant="outline" size="sm">
                Choose Files
              </Button>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-3 pt-4 border-t">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              onClick={handleSubmit}
              disabled={selectedPages.length === 0 || !correctionNotes.trim()}
              className="bg-slate-700 hover:bg-slate-800"
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Submit Correction
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
