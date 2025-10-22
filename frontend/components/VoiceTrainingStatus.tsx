"use client";

import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Mic, MicOff, Settings, FileText } from 'lucide-react';

interface VoiceTrainingStatusProps {
  voiceTrainingUsed?: boolean;
  voiceSamplesCount?: number;
  tone?: string;
  generationMetadata?: {
    voiceTrainingActive: boolean;
    samplesUsed: number;
    tonePreset: string;
    voiceSamplesTitles: string[];
  };
  className?: string;
}

export function VoiceTrainingStatus({ 
  voiceTrainingUsed = false, 
  voiceSamplesCount = 0, 
  tone = "professional",
  generationMetadata,
  className 
}: VoiceTrainingStatusProps) {
  
  const isVoiceTrainingActive = voiceTrainingUsed || (generationMetadata?.voiceTrainingActive ?? false);
  const samplesUsed = voiceSamplesCount || generationMetadata?.samplesUsed || 0;
  const tonePreset = tone || generationMetadata?.tonePreset || "professional";
  const sampleTitles = generationMetadata?.voiceSamplesTitles || [];

  return (
    <div className={className}>
      <Card className="border-dashed">
        <CardContent className="p-4">
          <div className="flex items-center gap-3 flex-wrap">
            {/* Voice Training Status */}
            {isVoiceTrainingActive ? (
              <Badge variant="default" className="flex items-center gap-1">
                <Mic className="h-3 w-3" />
                Using Your Voice ({samplesUsed} samples)
              </Badge>
            ) : (
              <Badge variant="outline" className="flex items-center gap-1">
                <MicOff className="h-3 w-3" />
                Voice Training Inactive
              </Badge>
            )}

            {/* Tone Preset */}
            <Badge variant="secondary" className="flex items-center gap-1">
              <Settings className="h-3 w-3" />
              Tone: {tonePreset.charAt(0).toUpperCase() + tonePreset.slice(1)}
            </Badge>

            {/* Sample Titles (if available) */}
            {isVoiceTrainingActive && sampleTitles.length > 0 && (
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <FileText className="h-3 w-3" />
                <span>Based on: {sampleTitles.slice(0, 2).join(', ')}{sampleTitles.length > 2 ? '...' : ''}</span>
              </div>
            )}
          </div>

          {/* Detailed Info */}
          {isVoiceTrainingActive && (
            <div className="mt-2 text-xs text-muted-foreground">
              ✨ This draft was generated using your personal writing style from {samplesUsed} voice training samples
            </div>
          )}

          {!isVoiceTrainingActive && samplesUsed < 3 && (
            <div className="mt-2 text-xs text-muted-foreground">
              💡 Upload 3+ writing samples in Settings → Voice Training to enable personalized drafts
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
