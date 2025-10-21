"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Source } from "@/types";
import { Plus, Rss, Twitter, Youtube, Check } from "lucide-react";

interface SourcePreset {
  id: string;
  name: string;
  description: string;
  category: string;
  sources: Omit<Source, 'id'>[];
}

interface SourcePresetsProps {
  onApplyPreset: (sources: Omit<Source, 'id'>[]) => void;
}

const PRESET_COLLECTIONS: SourcePreset[] = [
  {
    id: "tech-leaders",
    name: "Tech Leaders",
    description: "Follow the thoughts of top tech entrepreneurs and investors",
    category: "Entrepreneurship",
    sources: [
      { type: "twitter", value: "@elonmusk", label: "Elon Musk" },
      { type: "twitter", value: "@naval", label: "Naval Ravikant" },
      { type: "twitter", value: "@paulg", label: "Paul Graham" },
      { type: "twitter", value: "@sama", label: "Sam Altman" },
      { type: "youtube", value: "UCBJycsmduvYEL83R_U4JriQ", label: "Marques Brownlee" }
    ]
  },
  {
    id: "tech-news",
    name: "Tech News",
    description: "Stay updated with the latest tech news and analysis",
    category: "News",
    sources: [
      { type: "rss", value: "https://techcrunch.com/feed/", label: "TechCrunch" },
      { type: "rss", value: "https://venturebeat.com/feed/", label: "VentureBeat" },
      { type: "rss", value: "https://www.wired.com/feed/rss", label: "Wired" },
      { type: "rss", value: "https://feeds.feedburner.com/oreilly/radar", label: "O'Reilly Radar" }
    ]
  },
  {
    id: "ai-ml",
    name: "AI & Machine Learning",
    description: "Cutting-edge AI research and developments",
    category: "Technology",
    sources: [
      { type: "rss", value: "https://openai.com/blog/rss.xml", label: "OpenAI Blog" },
      { type: "rss", value: "https://blog.google/technology/ai/", label: "Google AI Blog" },
      { type: "twitter", value: "@karpathy", label: "Andrej Karpathy" },
      { type: "twitter", value: "@sama", label: "Sam Altman" },
      { type: "youtube", value: "UCbfYPyITQ-7l4upoX8nvctg", label: "Two Minute Papers" }
    ]
  },
  {
    id: "startup-ecosystem",
    name: "Startup Ecosystem",
    description: "Startup news, funding, and ecosystem insights",
    category: "Business",
    sources: [
      { type: "rss", value: "https://techcrunch.com/category/startups/feed/", label: "TechCrunch Startups" },
      { type: "rss", value: "https://www.crunchbase.com/news/feed/", label: "Crunchbase News" },
      { type: "twitter", value: "@jason", label: "Jason Calacanis" },
      { type: "twitter", value: "@paulg", label: "Paul Graham" },
      { type: "youtube", value: "UCeB_OpLspKJGiKjSdL1uWZA", label: "Y Combinator" }
    ]
  },
  {
    id: "developer-tools",
    name: "Developer Tools",
    description: "Latest in software development and tools",
    category: "Development",
    sources: [
      { type: "rss", value: "https://github.blog/feed/", label: "GitHub Blog" },
      { type: "rss", value: "https://stackoverflow.blog/feed/", label: "Stack Overflow Blog" },
      { type: "twitter", value: "@github", label: "GitHub" },
      { type: "twitter", value: "@stackoverflow", label: "Stack Overflow" },
      { type: "youtube", value: "UC8butISFwT-Wl7EV0hUK0BQ", label: "freeCodeCamp" }
    ]
  },
  {
    id: "crypto-web3",
    name: "Crypto & Web3",
    description: "Blockchain, cryptocurrency, and Web3 developments",
    category: "Technology",
    sources: [
      { type: "rss", value: "https://blog.coinbase.com/feed", label: "Coinbase Blog" },
      { type: "rss", value: "https://consensys.net/blog/feed/", label: "ConsenSys Blog" },
      { type: "twitter", value: "@vitalikbuterin", label: "Vitalik Buterin" },
      { type: "twitter", value: "@naval", label: "Naval Ravikant" },
      { type: "youtube", value: "UCdUSSt-IEUg2eq46rD7lu_g", label: "aantonop" }
    ]
  }
];

export function SourcePresets({ onApplyPreset }: SourcePresetsProps) {
  const [selectedPresets, setSelectedPresets] = useState<Set<string>>(new Set());
  const [showPresets, setShowPresets] = useState(false);

  const handlePresetToggle = (presetId: string) => {
    const newSelected = new Set(selectedPresets);
    if (newSelected.has(presetId)) {
      newSelected.delete(presetId);
    } else {
      newSelected.add(presetId);
    }
    setSelectedPresets(newSelected);
  };

  const handleApplySelected = () => {
    const allSources: Omit<Source, 'id'>[] = [];
    
    selectedPresets.forEach(presetId => {
      const preset = PRESET_COLLECTIONS.find(p => p.id === presetId);
      if (preset) {
        allSources.push(...preset.sources);
      }
    });

    onApplyPreset(allSources);
    setSelectedPresets(new Set());
    setShowPresets(false);
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
        return null;
    }
  };

  const getSourceTypeColor = (type: string) => {
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

  return (
    <div className="space-y-4">
      <Button
        variant="outline"
        onClick={() => setShowPresets(!showPresets)}
        className="w-full"
      >
        <Plus className="h-4 w-4 mr-2" />
        {showPresets ? 'Hide' : 'Show'} Preset Collections
      </Button>

      {showPresets && (
        <Card>
          <CardHeader>
            <CardTitle>Popular Source Collections</CardTitle>
            <p className="text-sm text-muted">
              Choose from curated collections of sources for different topics
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              {PRESET_COLLECTIONS.map((preset) => (
                <Card
                  key={preset.id}
                  className={`cursor-pointer transition-colors ${
                    selectedPresets.has(preset.id)
                      ? 'border-primary bg-primary/5'
                      : 'hover:border-primary/50'
                  }`}
                  onClick={() => handlePresetToggle(preset.id)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="font-semibold">{preset.name}</h4>
                        <p className="text-sm text-muted">{preset.description}</p>
                      </div>
                      {selectedPresets.has(preset.id) && (
                        <Check className="h-5 w-5 text-primary" />
                      )}
                    </div>
                    
                    <div className="flex items-center gap-2 mb-3">
                      <Badge variant="outline">{preset.category}</Badge>
                      <Badge variant="secondary">{preset.sources.length} sources</Badge>
                    </div>

                    <div className="space-y-2">
                      {preset.sources.slice(0, 3).map((source, index) => (
                        <div key={index} className="flex items-center gap-2">
                          {getSourceIcon(source.type)}
                          <span className="text-sm">{source.label}</span>
                          <Badge 
                            size="sm" 
                            className={getSourceTypeColor(source.type)}
                          >
                            {source.type.toUpperCase()}
                          </Badge>
                        </div>
                      ))}
                      {preset.sources.length > 3 && (
                        <p className="text-xs text-muted">
                          +{preset.sources.length - 3} more sources
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {selectedPresets.size > 0 && (
              <div className="flex items-center justify-between pt-4 border-t">
                <div className="text-sm text-muted">
                  {selectedPresets.size} collection{selectedPresets.size > 1 ? 's' : ''} selected
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setSelectedPresets(new Set())}
                  >
                    Clear Selection
                  </Button>
                  <Button onClick={handleApplySelected}>
                    Add Selected Sources
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
