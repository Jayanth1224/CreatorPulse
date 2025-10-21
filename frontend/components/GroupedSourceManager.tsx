"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Source, SourceType } from "@/types";
import { Plus, X, Rss, Twitter, Youtube, ExternalLink, Copy, Upload } from "lucide-react";
import { SourcePresets } from "./SourcePresets";

interface GroupedSourceManagerProps {
  bundleId: string;
  sources: Source[];
  onAddSource: (source: Omit<Source, 'id'>) => void;
  onRemoveSource: (sourceId: string) => void;
  onBulkAdd: (sources: Omit<Source, 'id'>[]) => void;
}

export function GroupedSourceManager({ 
  bundleId, 
  sources, 
  onAddSource, 
  onRemoveSource, 
  onBulkAdd 
}: GroupedSourceManagerProps) {
  const [bulkInput, setBulkInput] = useState("");
  const [showBulkAdd, setShowBulkAdd] = useState(false);

  // Group sources by type
  const groupedSources = (Array.isArray(sources) ? sources : []).reduce((acc, source) => {
    if (!acc[source.type]) {
      acc[source.type] = [];
    }
    acc[source.type].push(source);
    return acc;
  }, {} as Record<SourceType, Source[]>);

  const handleBulkAdd = (type: SourceType) => {
    const lines = bulkInput.split('\n').filter(line => line.trim());
    const newSources = lines.map(line => ({
      type,
      value: line.trim(),
      label: extractLabel(line.trim(), type)
    }));
    
    onBulkAdd(newSources);
    setBulkInput("");
    setShowBulkAdd(false);
  };

  const extractLabel = (value: string, type: SourceType): string => {
    switch (type) {
      case 'rss':
        try {
          const url = new URL(value);
          return url.hostname.replace('www.', '');
        } catch {
          return value;
        }
      case 'twitter':
        return value.replace('@', '');
      case 'youtube':
        if (value.includes('youtube.com')) {
          return 'YouTube Channel';
        }
        return value;
      default:
        return value;
    }
  };

  return (
    <div className="space-y-6">
      {/* Preset Collections */}
      <SourcePresets onApplyPreset={onBulkAdd} />

      {/* Bulk Operations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plus className="h-5 w-5" />
            Quick Add Sources
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              variant="outline"
              onClick={() => setShowBulkAdd(!showBulkAdd)}
              className="flex items-center gap-2"
            >
              <Upload className="h-4 w-4" />
              Bulk Add
            </Button>
            <Button
              variant="outline"
              className="flex items-center gap-2"
            >
              <Copy className="h-4 w-4" />
              Copy from Bundle
            </Button>
            <Button
              variant="outline"
              className="flex items-center gap-2"
            >
              Import CSV
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Bulk Add Modal */}
      {showBulkAdd && (
        <Card>
          <CardHeader>
            <CardTitle>Bulk Add Sources</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Enter sources (one per line)</Label>
              <textarea
                value={bulkInput}
                onChange={(e) => setBulkInput(e.target.value)}
                placeholder="https://techcrunch.com/feed/&#10;https://venturebeat.com/feed/&#10;https://wired.com/feed/"
                className="w-full h-32 p-3 border rounded-md"
              />
            </div>
            <div className="flex gap-2">
              <Button onClick={() => handleBulkAdd('rss')}>
                Add as RSS
              </Button>
              <Button onClick={() => handleBulkAdd('twitter')}>
                Add as Twitter
              </Button>
              <Button onClick={() => handleBulkAdd('youtube')}>
                Add as YouTube
              </Button>
              <Button variant="outline" onClick={() => setShowBulkAdd(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Source Groups */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <SourceGroup
          type="rss"
          title="RSS Feeds"
          sources={groupedSources.rss || []}
          onAdd={onAddSource}
          onRemove={onRemoveSource}
          icon={<Rss className="h-5 w-5" />}
          placeholder="https://example.com/feed.xml"
        />
        
        <SourceGroup
          type="twitter"
          title="Twitter Handles"
          sources={groupedSources.twitter || []}
          onAdd={onAddSource}
          onRemove={onRemoveSource}
          icon={<Twitter className="h-5 w-5" />}
          placeholder="@username"
        />
        
        <SourceGroup
          type="youtube"
          title="YouTube Channels"
          sources={groupedSources.youtube || []}
          onAdd={onAddSource}
          onRemove={onRemoveSource}
          icon={<Youtube className="h-5 w-5" />}
          placeholder="Channel ID or URL"
        />
      </div>
    </div>
  );
}

interface SourceGroupProps {
  type: SourceType;
  title: string;
  sources: Source[];
  onAdd: (source: Omit<Source, 'id'>) => void;
  onRemove: (sourceId: string) => void;
  icon: React.ReactNode;
  placeholder: string;
}

function SourceGroup({ 
  type, 
  title, 
  sources, 
  onAdd, 
  onRemove, 
  icon, 
  placeholder 
}: SourceGroupProps) {
  const [newSource, setNewSource] = useState("");
  const [isAdding, setIsAdding] = useState(false);

  const handleAdd = () => {
    if (!newSource.trim()) return;
    
    onAdd({
      type,
      value: newSource.trim(),
      label: extractLabel(newSource.trim(), type)
    });
    
    setNewSource("");
    setIsAdding(false);
  };

  const extractLabel = (value: string, type: SourceType): string => {
    switch (type) {
      case 'rss':
        try {
          const url = new URL(value);
          return url.hostname.replace('www.', '');
        } catch {
          return value;
        }
      case 'twitter':
        return value.replace('@', '');
      case 'youtube':
        if (value.includes('youtube.com')) {
          return 'YouTube Channel';
        }
        return value;
      default:
        return value;
    }
  };

  const validateSource = (value: string, type: SourceType): boolean => {
    switch (type) {
      case 'rss':
        return /^https?:\/\/.+/.test(value);
      case 'twitter':
        const cleanHandle = value.replace('@', '');
        return /^[a-zA-Z0-9_]{1,15}$/.test(cleanHandle);
      case 'youtube':
        return /^[a-zA-Z0-9_-]{24}$/.test(value) || 
               /youtube\.com\/(channel|c|@|user)\/[a-zA-Z0-9_-]+/.test(value);
      default:
        return false;
    }
  };

  const isValid = validateSource(newSource, type);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {icon}
            {title} ({sources.length})
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsAdding(!isAdding)}
          >
            <Plus className="h-4 w-4" />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Existing Sources */}
        {sources.map((source, index) => (
          <div key={source.id || index} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm">{source.label}</div>
              <div className="text-xs text-muted truncate">{source.value}</div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onRemove(source.id || index.toString())}
              className="text-red-600 hover:text-red-700"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        ))}

        {/* Add New Source */}
        {isAdding && (
          <div className="space-y-2">
            <Input
              value={newSource}
              onChange={(e) => setNewSource(e.target.value)}
              placeholder={placeholder}
              className={!isValid && newSource ? 'border-red-300' : ''}
            />
            {!isValid && newSource && (
              <p className="text-xs text-red-600">
                Invalid {type} format
              </p>
            )}
            <div className="flex gap-2">
              <Button
                size="sm"
                onClick={handleAdd}
                disabled={!isValid}
                className="flex-1"
              >
                Add
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  setIsAdding(false);
                  setNewSource("");
                }}
              >
                Cancel
              </Button>
            </div>
          </div>
        )}

        {/* Empty State */}
        {sources.length === 0 && !isAdding && (
          <div className="text-center py-4 text-muted">
            <p className="text-sm">No {type} sources yet</p>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsAdding(true)}
              className="mt-2"
            >
              Add your first {type} source
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
