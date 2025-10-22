/**
 * API Client for CreatorPulse
 * Handles all API requests to the backend
 */

import { supabase } from './supabase-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types
export interface ApiError {
  detail: string;
  status?: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

// Voice Training Types
export interface VoiceSample {
  id: string;
  user_id: string;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface VoiceSampleCreate {
  title: string;
  content: string;
}

export interface VoiceSamplesUploadRequest {
  samples: VoiceSampleCreate[];
}

export interface VoiceSamplesUploadResponse {
  created_count: number;
  sample_ids: string[];
  message: string;
}

export interface VoiceTrainingStatus {
  has_samples: boolean;
  sample_count: number;
  last_updated?: string;
  is_active: boolean;
}

// Auth helpers
export async function getAuthToken(): Promise<string | null> {
  const { data: { session } } = await supabase.auth.getSession();
  return session?.access_token ?? null;
}

export function setAuthToken(token: string) {
  // No-op: Supabase manages tokens automatically
  // Keeping for backward compatibility
}

export function clearAuthToken() {
  // No-op: Supabase manages tokens automatically
  // Keeping for backward compatibility
}

export async function getAuthHeaders(): Promise<HeadersInit> {
  const token = await getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
}

// Generic API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const authHeaders = await getAuthHeaders();
    const headers = {
      ...authHeaders,
      ...options.headers,
    };
    
    const response = await fetch(url, {
      ...options,
      headers,
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      return {
        error: {
          detail: data.detail || 'An error occurred',
          status: response.status,
        },
      };
    }
    
    return { data };
  } catch (error) {
    console.error('API request failed:', error);
    return {
      error: {
        detail: error instanceof Error ? error.message : 'Network error',
      },
    };
  }
}

// ============= Auth API =============

export async function signup(email: string, name: string, timezone?: string) {
  const response = await apiRequest('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify({ email, name, timezone }),
  });
  
  if (response.data && typeof response.data === 'object' && response.data !== null && 'access_token' in response.data) {
    setAuthToken((response.data as any).access_token);
  }
  
  return response;
}

export async function login(email: string, password: string) {
  const response = await apiRequest('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  
  if (response.data && typeof response.data === 'object' && response.data !== null && 'access_token' in response.data) {
    setAuthToken((response.data as any).access_token);
  }
  
  return response;
}

export async function logout() {
  clearAuthToken();
  return await apiRequest('/api/auth/logout', {
    method: 'POST',
  });
}

export async function getCurrentUser() {
  return await apiRequest('/api/auth/me');
}

export async function updateProfile(name?: string, timezone?: string) {
  const params = new URLSearchParams();
  if (name) params.append('name', name);
  if (timezone) params.append('timezone', timezone);
  
  return await apiRequest(`/api/auth/me?${params.toString()}`, {
    method: 'PUT',
  });
}

// ============= Bundles API =============

export async function getBundles() {
  return await apiRequest('/api/bundles/');
}

export async function getPresetBundles() {
  return await apiRequest('/api/bundles/presets');
}

export async function getBundle(bundleId: string) {
  return await apiRequest(`/api/bundles/${bundleId}`);
}

// ============= Drafts API =============

export async function getDrafts(status?: string, page?: number, limit?: number) {
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  if (page) params.append('page', page.toString());
  if (limit) params.append('limit', limit.toString());
  
  const queryString = params.toString();
  return await apiRequest(`/api/drafts/${queryString ? `?${queryString}` : ''}`);
}

export async function getDraft(draftId: string) {
  return await apiRequest(`/api/drafts/${draftId}`);
}

export async function generateDraft(
  bundleId: string,
  topic?: string,
  tone?: string
) {
  return await apiRequest('/api/drafts/generate', {
    method: 'POST',
    body: JSON.stringify({
      bundle_id: bundleId,
      topic,
      tone,
    }),
  });
}

export async function updateDraft(
  draftId: string,
  updates: {
    edited_html?: string;
    status?: string;
    scheduled_for?: string;
  }
) {
  return await apiRequest(`/api/drafts/${draftId}`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  });
}

export async function deleteDraft(draftId: string) {
  return await apiRequest(`/api/drafts/${draftId}`, {
    method: 'DELETE',
  });
}

export async function sendDraft(draftId: string, recipients: string[]) {
  return await apiRequest(`/api/drafts/${draftId}/send`, {
    method: 'POST',
    body: JSON.stringify({ recipients }),
  });
}

export async function regenerateSection(draftId: string, section: string) {
  return await apiRequest(`/api/drafts/${draftId}/regenerate?section=${section}`, {
    method: 'POST',
  });
}


// ============= Analytics API =============

export async function getAnalytics() {
  return await apiRequest('/api/analytics/');
}

export async function getDraftAnalytics(draftId: string) {
  return await apiRequest(`/api/analytics/drafts/${draftId}`);
}

// ============= LinkedIn API =============

export async function getLinkedInAuthUrl(redirectUri: string) {
  return await apiRequest(`/api/linkedin/auth/url?redirect_uri=${encodeURIComponent(redirectUri)}`);
}

export async function handleLinkedInCallback(
  code: string,
  state: string,
  redirectUri: string
) {
  return await apiRequest(
    `/api/linkedin/auth/callback?code=${code}&state=${state}&redirect_uri=${encodeURIComponent(redirectUri)}`,
    { method: 'POST' }
  );
}

export async function postToLinkedIn(
  draftId: string,
  content: string,
  visibility: string = 'PUBLIC'
) {
  return await apiRequest('/api/linkedin/post', {
    method: 'POST',
    body: JSON.stringify({
      draft_id: draftId,
      content,
      visibility,
    }),
  });
}

export async function getLinkedInStatus() {
  return await apiRequest('/api/linkedin/status');
}

export async function disconnectLinkedIn() {
  return await apiRequest('/api/linkedin/disconnect', {
    method: 'DELETE',
  });
}

// Source Management API
export async function addSourceToBundle(bundleId: string, source: { type: string; value: string; label?: string; metadata?: any }) {
  return await apiRequest(`/api/bundles/${bundleId}/sources`, {
    method: 'POST',
    body: JSON.stringify(source),
  });
}

export async function removeSourceFromBundle(bundleId: string, sourceId: string) {
  return await apiRequest(`/api/bundles/${bundleId}/sources/${sourceId}`, {
    method: 'DELETE',
  });
}

export async function getBundleSources(bundleId: string) {
  return await apiRequest(`/api/bundles/${bundleId}/sources`);
}

export async function validateSource(source: { type: string; value: string; label?: string; metadata?: any }) {
  return await apiRequest('/api/bundles/sources/validate', {
    method: 'POST',
    body: JSON.stringify(source),
  });
}

// ============= Auto-Newsletter API =============

export interface AutoNewsletter {
  id: string;
  user_id: string;
  bundle_id: string;
  is_active: boolean;
  schedule_time: string;
  schedule_frequency: 'daily' | 'weekly' | 'monthly';
  schedule_day?: number | null;
  email_recipients: string[];
  last_generated?: string | null;
  created_at: string;
  updated_at: string;
}

export async function listAutoNewsletters() {
  return await apiRequest<AutoNewsletter[]>('/api/auto-newsletters/');
}

export async function createAutoNewsletter(payload: {
  bundle_id: string;
  schedule_time?: string;
  schedule_frequency?: 'daily' | 'weekly' | 'monthly';
  schedule_day?: number | null;
  email_recipients?: string[];
}) {
  return await apiRequest<AutoNewsletter>('/api/auto-newsletters/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateAutoNewsletter(id: string, updates: Partial<{
  is_active: boolean;
  schedule_time: string;
  schedule_frequency: 'daily' | 'weekly' | 'monthly';
  schedule_day: number | null;
  email_recipients: string[];
}>) {
  return await apiRequest<AutoNewsletter>(`/api/auto-newsletters/${id}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

export async function deleteAutoNewsletter(id: string) {
  return await apiRequest(`/api/auto-newsletters/${id}`, {
    method: 'DELETE',
  });
}

// Voice Training API functions
export async function getVoiceSamples(limit: number = 20) {
  return await apiRequest<VoiceSample[]>(`/api/voice-training/samples?limit=${limit}`);
}

export async function createVoiceSample(sample: VoiceSampleCreate) {
  return await apiRequest<VoiceSample>('/api/voice-training/samples', {
    method: 'POST',
    body: JSON.stringify(sample),
  });
}

export async function uploadVoiceSamples(samples: VoiceSampleCreate[]) {
  return await apiRequest<VoiceSamplesUploadResponse>('/api/voice-training/samples/upload', {
    method: 'POST',
    body: JSON.stringify({ samples }),
  });
}

export async function updateVoiceSample(id: string, updates: Partial<VoiceSampleCreate>) {
  return await apiRequest<VoiceSample>(`/api/voice-training/samples/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  });
}

export async function deleteVoiceSample(id: string) {
  return await apiRequest<void>(`/api/voice-training/samples/${id}`, {
    method: 'DELETE',
  });
}

export async function getVoiceTrainingStatus() {
  return await apiRequest<VoiceTrainingStatus>('/api/voice-training/status');
}

export async function clearAllVoiceSamples() {
  return await apiRequest<{ message: string; cleared_count: number }>('/api/voice-training/samples/clear', {
    method: 'POST',
  });
}

export async function generateAutoNewsletterNow(id: string) {
  return await apiRequest(`/api/auto-newsletters/${id}/generate`, {
    method: 'POST',
  });
}

