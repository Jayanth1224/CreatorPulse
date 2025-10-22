"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Upload, 
  FileText, 
  Trash2, 
  Check, 
  AlertCircle, 
  Loader2,
  Plus,
  Edit,
  Save,
  X
} from 'lucide-react';
import { 
  getVoiceSamples, 
  uploadVoiceSamples, 
  deleteVoiceSample, 
  getVoiceTrainingStatus,
  clearAllVoiceSamples,
  VoiceSample,
  VoiceSampleCreate,
  VoiceTrainingStatus
} from '@/lib/api-client';

interface VoiceTrainingSectionProps {
  className?: string;
}

export function VoiceTrainingSection({ className }: VoiceTrainingSectionProps) {
  const [samples, setSamples] = useState<VoiceSample[]>([]);
  const [status, setStatus] = useState<VoiceTrainingStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [editingSample, setEditingSample] = useState<string | null>(null);
  const [newSample, setNewSample] = useState<VoiceSampleCreate>({ title: '', content: '' });
  const [csvText, setCsvText] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load data on mount
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [samplesResponse, statusResponse] = await Promise.all([
        getVoiceSamples(),
        getVoiceTrainingStatus()
      ]);

      if (samplesResponse.data) {
        setSamples(samplesResponse.data);
      }
      if (statusResponse.data) {
        setStatus(statusResponse.data);
      }
    } catch (err) {
      setError('Failed to load voice training data');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (files: FileList) => {
    if (!files.length) return;

    setUploading(true);
    setError(null);

    try {
      const samples: VoiceSampleCreate[] = [];
      
      for (const file of files) {
        const content = await file.text();
        const title = file.name.replace(/\.[^/.]+$/, "");
        
        samples.push({
          title,
          content: content.trim()
        });
      }

      const response = await uploadVoiceSamples(samples);
      
      if (response.data) {
        setSuccess(`Successfully uploaded ${response.data.created_count} voice samples`);
        await loadData();
        setShowUploadForm(false);
      } else {
        setError(response.error?.detail || 'Upload failed');
      }
    } catch (err) {
      setError('Failed to upload files');
    } finally {
      setUploading(false);
    }
  };

  const handleCSVUpload = async () => {
    if (!csvText.trim()) return;

    setUploading(true);
    setError(null);

    try {
      const lines = csvText.split('\n').filter(line => line.trim());
      const samples: VoiceSampleCreate[] = lines.map((line, index) => ({
        title: `Sample ${index + 1}`,
        content: line.trim()
      }));

      const response = await uploadVoiceSamples(samples);
      
      if (response.data) {
        setSuccess(`Successfully uploaded ${response.data.created_count} voice samples`);
        await loadData();
        setCsvText('');
        setShowUploadForm(false);
      } else {
        setError(response.error?.detail || 'Upload failed');
      }
    } catch (err) {
      setError('Failed to upload CSV data');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteSample = async (id: string) => {
    try {
      const response = await deleteVoiceSample(id);
      if (response.data !== undefined) {
        setSamples(samples.filter(s => s.id !== id));
        await loadData(); // Refresh status
      } else {
        setError(response.error?.detail || 'Delete failed');
      }
    } catch (err) {
      setError('Failed to delete sample');
    }
  };

  const handleClearAll = async () => {
    if (!confirm('Are you sure you want to delete all voice samples? This cannot be undone.')) {
      return;
    }

    try {
      const response = await clearAllVoiceSamples();
      if (response.data) {
        setSuccess(`Cleared ${response.data.cleared_count} voice samples`);
        await loadData();
      } else {
        setError(response.error?.detail || 'Clear failed');
      }
    } catch (err) {
      setError('Failed to clear samples');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const truncateContent = (content: string, maxLength: number = 100) => {
    return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
  };

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle>Voice Training</CardTitle>
          <CardDescription>
            Upload samples of your writing to train a custom voice model using in-context learning
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Status */}
          {status && (
            <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
              <div className="flex items-center gap-2">
                <Badge variant={status.is_active ? "default" : "secondary"}>
                  {status.is_active ? "Active" : "Inactive"}
                </Badge>
                <span className="text-sm text-muted-foreground">
                  {status.sample_count} samples
                </span>
              </div>
              {status.last_updated && (
                <span className="text-xs text-muted-foreground">
                  Last updated: {formatDate(status.last_updated)}
                </span>
              )}
            </div>
          )}

          {/* Upload Section */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Upload Writing Samples</h3>
              <Button 
                onClick={() => setShowUploadForm(!showUploadForm)}
                variant="outline"
                size="sm"
              >
                {showUploadForm ? <X className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
                {showUploadForm ? 'Cancel' : 'Add Samples'}
              </Button>
            </div>

            {showUploadForm && (
              <div className="space-y-4 p-4 border rounded-lg">
                {/* File Upload */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Upload Files</label>
                  <div 
                    className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-primary/50 transition-colors cursor-pointer"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Upload className="h-8 w-8 text-muted mx-auto mb-3" />
                    <p className="font-medium mb-1">Choose Files</p>
                    <p className="text-xs text-muted mb-3">
                      Upload text files, markdown, or CSV files with your writing samples
                    </p>
                    <input
                      ref={fileInputRef}
                      type="file"
                      multiple
                      accept=".txt,.md,.csv"
                      onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
                      className="hidden"
                    />
                  </div>
                </div>

                {/* CSV Upload */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Or Paste Text/CSV</label>
                  <Textarea
                    placeholder="Paste your writing samples here, one per line..."
                    value={csvText}
                    onChange={(e) => setCsvText(e.target.value)}
                    rows={6}
                  />
                  <Button 
                    onClick={handleCSVUpload}
                    disabled={!csvText.trim() || uploading}
                    size="sm"
                  >
                    {uploading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
                    Upload Text
                  </Button>
                </div>
              </div>
            )}

            {/* File Upload Button */}
            {!showUploadForm && (
              <div 
                className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="h-8 w-8 text-muted mx-auto mb-3" />
                <p className="font-medium mb-1">Upload Writing Samples</p>
                <p className="text-xs text-muted mb-3">
                  Upload at least 3 examples of your best newsletters or articles
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".txt,.md,.csv"
                  onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
                  className="hidden"
                />
                <Button variant="outline" size="sm">
                  Choose Files
                </Button>
              </div>
            )}
          </div>

          {/* Samples List */}
          {samples.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Your Voice Samples</h3>
                <Button 
                  onClick={handleClearAll}
                  variant="outline"
                  size="sm"
                  className="text-destructive hover:text-destructive"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Clear All
                </Button>
              </div>

              <div className="space-y-2">
                {samples.map((sample) => (
                  <div key={sample.id} className="flex items-start gap-3 p-3 border rounded-lg">
                    <FileText className="h-5 w-5 text-muted mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-medium truncate">{sample.title}</h4>
                        <Badge variant="outline" className="text-xs">
                          {sample.content.length} chars
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-2">
                        {truncateContent(sample.content)}
                      </p>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <span>Created: {formatDate(sample.created_at)}</span>
                      </div>
                    </div>
                    <Button
                      onClick={() => handleDeleteSample(sample.id)}
                      variant="ghost"
                      size="sm"
                      className="text-destructive hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert>
              <Check className="h-4 w-4" />
              <AlertDescription>{success}</AlertDescription>
            </Alert>
          )}

          {/* Info */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-blue-900 dark:text-blue-100">
                  How Voice Training Works
                </p>
                <p className="text-xs text-blue-700 dark:text-blue-300 mt-1">
                  We use in-context learning to match your writing style. Upload 3+ samples of your best work, 
                  and our AI will learn your voice, tone, and writing patterns to generate more personalized drafts.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
