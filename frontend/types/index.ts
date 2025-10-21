export interface User {
  id: string;
  email: string;
  name: string;
  timezone: string;
  createdAt: Date;
}

export type SourceType = 'rss' | 'twitter' | 'youtube';

export interface Source {
  id?: string;
  type: SourceType;
  value: string;  // URL, @handle, or channel_id
  label?: string;
  metadata?: Record<string, any>;
}

export interface Bundle {
  id: string;
  key: string;
  label: string;
  description: string;
  isPreset: boolean;
  sources: (string | Source)[];  // Support both old string format and new Source objects
}

export interface Draft {
  id: string;
  userId: string;
  bundleId: string;
  bundleName: string;
  topic?: string;
  tone: "professional" | "conversational" | "analytical" | "friendly";
  generatedHtml: string;
  editedHtml?: string;
  status: "draft" | "sent" | "scheduled";
  readinessScore?: number;
  sources: string[];
  createdAt: Date | null;
  updatedAt: Date | null;
  sentAt?: Date | null;
  scheduledFor?: Date | null;
}

export interface DraftSection {
  id: string;
  type: "intro" | "insight" | "trends" | "outro";
  content: string;
  order: number;
}

export interface Feedback {
  id: string;
  draftId: string;
  sectionId?: string;
  reaction: "thumbs_up" | "thumbs_down";
  editDiff?: string;
  createdAt: Date;
}

export interface Analytics {
  id: string;
  draftId: string;
  openedAt?: Date;
  clickedAt?: Date;
  sentAt: Date;
}

export interface AnalyticsSummary {
  openRate: number;
  clickThroughRate: number;
  avgReviewTime: number;
  draftAcceptanceRate: number;
  totalDrafts: number;
  totalSent: number;
}

export interface ESPCredential {
  id: string;
  userId: string;
  provider: "sendgrid" | "mailgun" | "smtp";
  apiKey: string;
  verified: boolean;
  createdAt: Date;
}

export interface TonePreset {
  value: "professional" | "conversational" | "analytical" | "friendly";
  label: string;
  description: string;
}

export interface CreateDraftRequest {
  bundleId: string;
  topic?: string;
  tone?: string;
}

export interface SendDraftRequest {
  draftId: string;
  recipients: string[];
  subject?: string;
}

