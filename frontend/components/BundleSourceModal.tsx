"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GroupedSourceManager } from "./GroupedSourceManager";
import { Source } from "@/types";
import { X, Rss, Twitter, Youtube, Clock, CheckCircle, AlertCircle } from "lucide-react";
import { addSourceToBundle, removeSourceFromBundle, getBundleSources } from "@/lib/api-client";

interface BundleSourceModalProps {
  bundleId: string;
  bundleName: string;
  isOpen: boolean;
  onClose: () => void;
}

export function BundleSourceModal({ bundleId, bundleName, isOpen, onClose }: BundleSourceModalProps) {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadSources();
    }
  }, [isOpen, bundleId]);

  const loadSources = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getBundleSources(bundleId);
      setSources(response || []);
    } catch (err) {
      setError("Failed to load sources");
      console.error("Error loading sources:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSource = async (source: Omit<Source, 'id'>) => {
    try {
      console.log("Adding source:", source);
      const response = await addSourceToBundle(bundleId, source);
      console.log("Add source response:", response);
      
      // Handle both direct response and data wrapper
      const data = response.data || response;
      
      if (data && data.success) {
        const newSource: Source = {
          ...source,
          id: data.source_id
        };
        setSources([...sources, newSource]);
        console.log("Source added successfully:", newSource);
        setError(null); // Clear any previous errors
      } else if (response.error) {
        console.error("Failed to add source:", response.error);
        setError("Failed to add source: " + response.error.detail);
      } else {
        console.error("Unexpected response:", response);
        setError("Failed to add source");
      }
    } catch (err) {
      setError("Failed to add source");
      console.error("Error adding source:", err);
    }
  };

  const handleRemoveSource = async (sourceId: string) => {
    try {
      await removeSourceFromBundle(bundleId, sourceId);
      setSources(sources.filter(s => s.id !== sourceId));
    } catch (err) {
      setError("Failed to remove source");
      console.error("Error removing source:", err);
    }
  };

  const handleBulkAdd = async (newSources: Omit<Source, 'id'>[]) => {
    try {
      console.log("Bulk adding sources:", newSources);
      setError(null); // Clear any previous errors
      
      let successCount = 0;
      for (const source of newSources) {
        try {
          await handleAddSource(source);
          successCount++;
        } catch (err) {
          console.error("Failed to add source:", source, err);
        }
      }
      
      console.log(`Successfully added ${successCount}/${newSources.length} sources`);
      
      // Reload sources from server to ensure UI is in sync
      await loadSources();
      
      if (successCount === newSources.length) {
        console.log("All sources added successfully");
      } else if (successCount > 0) {
        setError(`Added ${successCount}/${newSources.length} sources. Some may have failed.`);
      } else {
        setError("Failed to add any sources");
      }
    } catch (err) {
      setError("Failed to add sources");
      console.error("Error bulk adding sources:", err);
    }
  };

  const getSourceStats = () => {
    if (!Array.isArray(sources)) {
      return {};
    }
    
    const stats = sources.reduce((acc, source) => {
      acc[source.type] = (acc[source.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return stats;
  };

  const getSourceIcon = (type: string) => {
    switch (type) {
      case 'rss':
        return <Rss className="h-4 w-4" />;
      case 'twitter':
        return <Twitter className="h-4 w-4" />;
      case 'youtube':
        return <Youtube className="h-4 w-4" />;
      default:
        return <AlertCircle className="h-4 w-4" />;
    }
  };

  if (!isOpen) return null;

  const stats = getSourceStats();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div>
            <h2 className="text-xl font-semibold">Manage Sources</h2>
            <p className="text-sm text-muted">{bundleName}</p>
          </div>
          <Button variant="ghost" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Stats */}
        <div className="p-6 border-b bg-gray-50 dark:bg-gray-800">
          <div className="flex items-center gap-4">
            <div className="text-sm text-muted">Total Sources:</div>
            <Badge variant="secondary">{sources.length}</Badge>
            {Object.entries(stats).map(([type, count]) => (
              <div key={type} className="flex items-center gap-1">
                {getSourceIcon(type)}
                <span className="text-sm">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : error ? (
            <div className="flex items-center justify-center py-8 text-red-600">
              <AlertCircle className="h-5 w-5 mr-2" />
              {error}
            </div>
          ) : (
            <GroupedSourceManager
              bundleId={bundleId}
              sources={sources}
              onAddSource={handleAddSource}
              onRemoveSource={handleRemoveSource}
              onBulkAdd={handleBulkAdd}
            />
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t">
          <div className="text-sm text-muted">
            Sources will be crawled every 6 hours
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose}>
              Close
            </Button>
            <Button onClick={onClose}>
              Save Changes
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
