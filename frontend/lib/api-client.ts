/**
 * API Client for CreatorPulse
 * Handles all API requests to the backend
 */

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

// Auth helpers
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

export function setAuthToken(token: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('auth_token', token);
}

export function clearAuthToken() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('auth_token');
}

export function getAuthHeaders(): HeadersInit {
  const token = getAuthToken();
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
    const headers = {
      ...getAuthHeaders(),
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
  
  if (response.data) {
    setAuthToken(response.data.access_token);
  }
  
  return response;
}

export async function login(email: string, password: string) {
  const response = await apiRequest('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  
  if (response.data) {
    setAuthToken(response.data.access_token);
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

export async function getDrafts(status?: string) {
  const params = status ? `?status=${status}` : '';
  return await apiRequest(`/api/drafts/${params}`);
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

export async function saveFeedback(
  draftId: string,
  sectionId: string,
  reaction: 'thumbs_up' | 'thumbs_down'
) {
  return await apiRequest(`/api/drafts/${draftId}/reactions?section_id=${sectionId}&reaction=${reaction}`, {
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

