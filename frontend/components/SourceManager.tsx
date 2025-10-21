"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Source, SourceType } from "@/types";
import { Plus, X, Rss, Twitter, Youtube, ExternalLink } from "lucide-react";

interface SourceManagerProps {
  sources: Source[];
  onAddSource: (source: Omit<Source, 'id'>) => void;
  onRemoveSource: (sourceId: string) => void;
  bundleId?: string;
}

export function SourceManager({ sources, onAddSource, onRemoveSource, bundleId }: SourceManagerProps) {
  const [newSource, setNewSource] = useState<Omit<Source, 'id'>>({
    type: 'rss',
    value: '',
    label: ''
  });
  const [isAdding, setIsAdding] = useState(false);

  const handleAddSource = () => {
    if (!newSource.value.trim()) return;
    
    onAddSource(newSource);
    setNewSource({ type: 'rss', value: '', label: '' });
    setIsAdding(false);
  };

  const handleRemoveSource = (sourceId: string) => {
    onRemoveSource(sourceId);
  };

  const getSourceIcon = (type: SourceType) => {
    switch (type) {
      case 'rss':
        return <Rss className="h-4 w-4" />;
      case 'twitter':
        return <Twitter className="h-4 w-4" />;
      case 'youtube':
        return <Youtube className="h-4 w-4" />;
      default:
        return <ExternalLink className="h-4 w-4" />;
    }
  };

  const getSourceTypeColor = (type: SourceType) => {
    switch (type) {
      case 'rss':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
      case 'twitter':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'youtube':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getPlaceholder = (type: SourceType) => {
    switch (type) {
      case 'rss':
        return 'https://example.com/feed.xml';
      case 'twitter':
        return '@username or username';
      case 'youtube':
        return 'Channel ID or YouTube URL';
      default:
        return 'Enter source...';
    }
  };

  const validateSource = (source: Omit<Source, 'id'>) => {
    if (!source.value.trim()) return false;
    
    switch (source.type) {
      case 'rss':
        return /^https?:\/\/.+/.test(source.value);
      case 'twitter':
        const cleanHandle = source.value.replace('@', '');
        return /^[a-zA-Z0-9_]{1,15}$/.test(cleanHandle);
      case 'youtube':
        return /^[a-zA-Z0-9_-]{24}$/.test(source.value) || 
               /youtube\.com\/(channel|c|@|user)\/[a-zA-Z0-9_-]+/.test(source.value);
      default:
        return false;
    }
  };

  const isValid = validateSource(newSource);

  return (
    <div className="space-y-4">
      {/* Existing Sources */}
      {sources.length > 0 && (
        <div className="space-y-2">
          <Label>Current Sources ({sources.length})</Label>
          <div className="grid gap-2">
            {sources.map((source, index) => (
              <Card key={source.id || index} className="p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getSourceIcon(source.type)}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <Badge className={getSourceTypeColor(source.type)}>
                          {source.type.toUpperCase()}
                        </Badge>
                        {source.label && (
                          <span className="font-medium text-sm">{source.label}</span>
                        )}
                      </div>
                      <p className="text-sm text-muted truncate">{source.value}</p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleRemoveSource(source.id || index.toString())}
                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Add New Source */}
      {!isAdding ? (
        <Button
          variant="outline"
          onClick={() => setIsAdding(true)}
          className="w-full"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Source
        </Button>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Add New Source</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="source-type">Source Type</Label>
              <Select
                id="source-type"
                value={newSource.type}
                onChange={(e) => setNewSource({ ...newSource, type: e.target.value as SourceType })}
              >
                <option value="rss">RSS Feed</option>
                <option value="twitter">Twitter Handle</option>
                <option value="youtube">YouTube Channel</option>
              </Select>
            </div>

            <div>
              <Label htmlFor="source-value">Source Value</Label>
              <Input
                id="source-value"
                value={newSource.value}
                onChange={(e) => setNewSource({ ...newSource, value: e.target.value })}
                placeholder={getPlaceholder(newSource.type)}
                className={!isValid && newSource.value ? 'border-red-300' : ''}
              />
              {!isValid && newSource.value && (
                <p className="text-sm text-red-600 mt-1">
                  Invalid {newSource.type} format
                </p>
              )}
            </div>

            <div>
              <Label htmlFor="source-label">Display Name (Optional)</Label>
              <Input
                id="source-label"
                value={newSource.label}
                onChange={(e) => setNewSource({ ...newSource, label: e.target.value })}
                placeholder="e.g., TechCrunch, @elonmusk, Veritasium"
              />
            </div>

            <div className="flex gap-2">
              <Button
                onClick={handleAddSource}
                disabled={!isValid}
                className="flex-1"
              >
                Add Source
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setIsAdding(false);
                  setNewSource({ type: 'rss', value: '', label: '' });
                }}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
