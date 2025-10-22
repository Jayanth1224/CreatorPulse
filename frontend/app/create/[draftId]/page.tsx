"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { Navigation } from "@/components/layout/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { getDraft, updateDraft, sendDraft } from "@/lib/api-client";
import { supabase } from "@/lib/supabase-client";
import { Draft } from "@/types";
import { SectionEditor } from "@/components/SectionEditor";
import { NewsletterSection, parseNewsletterSections, reassembleNewsletterSections } from "@/lib/newsletter-parser";
import {
  Save,
  Send,
  ArrowLeft,
  Undo2,
  Loader2,
  Check,
  Eye,
  X,
} from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { VoiceTrainingStatus } from "@/components/VoiceTrainingStatus";

export default function EditorPage() {
  return (
    <ProtectedRoute>
      <EditorContent />
    </ProtectedRoute>
  );
}

function EditorContent() {
  const params = useParams();
  const router = useRouter();
  const draftId = params.draftId as string;

  const [draft, setDraft] = useState<Draft | null>(null);
  const [content, setContent] = useState("");
  const [originalContent, setOriginalContent] = useState(""); // Store original generated content
  const [subject, setSubject] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recipients, setRecipients] = useState("");
  const [previewMode, setPreviewMode] = useState(false);
  const [previewHtml, setPreviewHtml] = useState("");
  const [sections, setSections] = useState<NewsletterSection[]>([]);
  
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    loadDraft();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draftId]);

  async function loadDraft() {
    const response = await getDraft(draftId);
    
    if (response.error) {
      setError(response.error.detail);
      return;
    }
    
    if (response.data) {
      const data = response.data as any; // Type assertion for API response
      // Transform snake_case to camelCase
      const transformedDraft = {
        ...data,
        bundleName: data.bundle_name || data.bundleName,
        generatedHtml: data.generated_html || data.generatedHtml,
        editedHtml: data.edited_html || data.editedHtml,
        readinessScore: data.readiness_score || data.readinessScore,
        createdAt: data.created_at ? new Date(data.created_at) : new Date(),
        updatedAt: data.updated_at ? new Date(data.updated_at) : new Date(),
        sentAt: data.sent_at ? new Date(data.sent_at) : null,
        scheduledFor: data.scheduled_for ? new Date(data.scheduled_for) : null,
        // Voice training metadata
        voiceTrainingUsed: data.voice_training_used || data.voiceTrainingUsed,
        voiceSamplesCount: data.voice_samples_count || data.voiceSamplesCount,
        generationMetadata: data.generation_metadata || data.generationMetadata,
      };
      setDraft(transformedDraft as Draft);
      
      const htmlContent = data.edited_html || data.generated_html;
      const generatedContent = data.generated_html;
      
      setContent(htmlContent);
      setOriginalContent(generatedContent); // Store original for revert
      
      // Parse content into sections
      const parsedSections = parseNewsletterSections(htmlContent);
      setSections(parsedSections);
      
      
      setSubject(data.topic || `${data.bundle_name} Newsletter`);
    }
  }
  

  // Autosave with debouncing
  const saveContent = useCallback(async (htmlContent: string) => {
    if (!draftId) return;
    
    setIsSaving(true);
    
    const response = await updateDraft(draftId, {
      edited_html: htmlContent,
    });
    
    setIsSaving(false);
    
    if (response.error) {
      console.error("Autosave failed:", response.error);
    } else {
      setLastSaved(new Date());
    }
  }, [draftId]);

  useEffect(() => {
    if (!content || !draft) return;
    
    // Clear existing timeout
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }
    
    // Set new timeout for debounced save
    saveTimeoutRef.current = setTimeout(() => {
      saveContent(content);
    }, 2000); // Save 2 seconds after user stops typing
    
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, [content, draft, saveContent]);

  const handleSend = async () => {
    if (!recipients.trim()) {
      alert("Please enter at least one recipient email");
      return;
    }
    
    setIsSending(true);
    
    const emailList = recipients.split(",").map(email => email.trim());
    const response = await sendDraft(draftId, emailList);
    
    setIsSending(false);
    
    if (response.error) {
      alert(`Failed to send: ${response.error.detail}`);
    } else {
      alert("Newsletter sent successfully!");
      router.push("/dashboard");
    }
  };



  const handleRevert = () => {
    if (!originalContent) return;
    
    const confirmRevert = window.confirm(
      "Are you sure you want to revert to the original AI-generated content? All your edits will be lost."
    );
    
    if (confirmRevert) {
      setContent(originalContent);
      // Re-parse sections from original content
      const parsedSections = parseNewsletterSections(originalContent);
      setSections(parsedSections);
      // Save the reverted content
      saveContent(originalContent);
    }
  };

  const handleManualSave = async () => {
    if (!content) return;
    await saveContent(content);
  };

  const handlePreview = async () => {
    if (!draftId) return;
    
    try {
      // Get the Supabase session token
      const { data: { session } } = await supabase.auth.getSession();
      if (!session?.access_token) {
        alert('Please log in to preview drafts');
        return;
      }
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/drafts/${draftId}/preview`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`
        }
      });
      
      if (response.ok) {
        const previewData = await response.json();
        // Remove clickable links from preview content
        const processedHtml = previewData.html_content
          .replace(/<a[^>]*>/gi, '<span style="color: #666; text-decoration: none; cursor: default;">')
          .replace(/<\/a>/gi, '</span>');
        setPreviewHtml(processedHtml);
        setPreviewMode(true);
      } else {
        const errorData = await response.json();
        console.error('Preview error:', errorData);
        alert(`Failed to load preview: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Preview error:', error);
      alert('Failed to load preview');
    }
  };

  const handleClosePreview = () => {
    setPreviewMode(false);
    setPreviewHtml("");
  };

  // Section management functions
  const handleSectionUpdate = (sectionId: string, updates: Partial<NewsletterSection>) => {
    setSections(prev => {
      const updated = prev.map(section => 
        section.id === sectionId ? { ...section, ...updates } : section
      );
      
      // Update main content when sections change
      const newContent = reassembleNewsletterSections(updated);
      setContent(newContent);
      
      return updated;
    });
  };

  const handleSectionDelete = (sectionId: string) => {
    setSections(prev => {
      const updated = prev.filter(section => section.id !== sectionId);
      const newContent = reassembleNewsletterSections(updated);
      setContent(newContent);
      return updated;
    });
  };


  const handleSectionReorder = (sectionId: string, direction: 'up' | 'down') => {
    setSections(prev => {
      const currentIndex = prev.findIndex(s => s.id === sectionId);
      if (currentIndex === -1) return prev;
      
      const newIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
      if (newIndex < 0 || newIndex >= prev.length) return prev;
      
      const updated = [...prev];
      [updated[currentIndex], updated[newIndex]] = [updated[newIndex], updated[currentIndex]];
      
      // Update order values
      updated.forEach((section, index) => {
        section.order = index;
      });
      
      const newContent = reassembleNewsletterSections(updated);
      setContent(newContent);
      
      return updated;
    });
  };

  if (error) {
    return (
      <>
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
            <h2 className="text-2xl font-bold text-destructive">Error Loading Draft</h2>
            <p className="text-muted">{error}</p>
            <Button onClick={() => router.push("/dashboard")}>
              Back to Dashboard
            </Button>
          </div>
        </main>
      </>
    );
  }

  if (!draft) {
    return (
      <>
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center min-h-[60vh]">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Navigation />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => router.push("/dashboard")}
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="text-2xl font-bold">Edit Draft</h1>
              <p className="text-sm text-muted">
                {isSaving ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="h-3 w-3 animate-spin" />
                    Saving...
                  </span>
                ) : lastSaved ? (
                  `Last saved ${lastSaved.toLocaleTimeString()}`
                ) : (
                  "Auto-save enabled"
                )}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={handlePreview}
              title="Preview newsletter"
            >
              <Eye className="h-4 w-4 mr-1" />
              Preview
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleRevert}
              disabled={!originalContent || content === originalContent}
              title="Revert to original AI-generated content"
            >
              <Undo2 className="h-4 w-4 mr-1" />
              Revert
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleManualSave}
              disabled={isSaving}
            >
              {isSaving ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-1" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-1" />
                  Save
                </>
              )}
            </Button>
            <Button size="sm" onClick={handleSend} disabled={isSending}>
              {isSending ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-1" />
                  Sending...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4 mr-1" />
                  Send
                </>
              )}
            </Button>
          </div>
        </div>

        {/* Draft Info */}
        <div className="bg-surface border border-border rounded-lg p-4 mb-6 flex flex-wrap items-center gap-3">
          <Badge>{draft.bundleName}</Badge>
          <Badge variant="secondary">{draft.tone} tone</Badge>
          {draft.readinessScore && (
            <Badge variant="success">{draft.readinessScore}% Ready</Badge>
          )}
          <span className="text-sm text-muted">
            Created {draft.createdAt ? draft.createdAt.toLocaleDateString() : 'Recently'}
          </span>
        </div>

        {/* Voice Training Status */}
        <VoiceTrainingStatus 
          voiceTrainingUsed={draft.voiceTrainingUsed}
          voiceSamplesCount={draft.voiceSamplesCount}
          tone={draft.tone}
          generationMetadata={draft.generationMetadata}
          className="mb-6"
        />

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Editor */}
          <div className="lg:col-span-2 space-y-6">
            {/* Subject Line */}
            <div>
              <Label htmlFor="subject" className="text-base font-semibold mb-2">
                Subject Line
              </Label>
              <Input
                id="subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="text-lg font-medium"
                placeholder="Enter newsletter subject..."
              />
            </div>

            {/* Content Editor */}
            <div>
              <Label htmlFor="content" className="text-base font-semibold mb-4">
                Newsletter Content
              </Label>
              
              <div className="space-y-4">
                {sections.map((section, index) => (
                  <SectionEditor
                    key={section.id}
                    section={section}
                    onUpdate={handleSectionUpdate}
                    onDelete={handleSectionDelete}
                    onReorder={handleSectionReorder}
                    canMoveUp={index > 0}
                    canMoveDown={index < sections.length - 1}
                  />
                ))}
                {sections.length === 0 && (
                  <div className="bg-surface border border-border rounded-lg p-8 text-center">
                    <p className="text-muted">No sections found in this draft.</p>
                  </div>
                )}
              </div>
              
              <p className="text-xs text-muted mt-2">
                Edit individual sections. Changes are automatically saved.
              </p>
            </div>

          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Send Recipients */}
            <div className="bg-surface border border-border rounded-lg p-4">
              <h3 className="font-semibold mb-3">Send Newsletter</h3>
              <Input
                placeholder="email@example.com, another@example.com"
                value={recipients}
                onChange={(e) => setRecipients(e.target.value)}
                className="mb-3"
              />
              <p className="text-xs text-muted mb-3">
                Enter email addresses separated by commas
              </p>
              <Button 
                size="sm" 
                className="w-full" 
                onClick={handleSend}
                disabled={isSending || !recipients.trim()}
              >
                {isSending ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    Sending...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4 mr-2" />
                    Send Now
                  </>
                )}
              </Button>
            </div>


            {/* Source Bundle */}
            <div className="bg-surface border border-border rounded-lg p-4">
              <h3 className="font-semibold mb-3 text-sm">Source Bundle</h3>
              <div className="max-h-64 overflow-y-auto space-y-3">
                {draft.sources.map((source, idx) => {
                  // Extract domain name from URL for display
                  const getDomainName = (url: string) => {
                    try {
                      const domain = new URL(url).hostname;
                      return domain.replace('www.', '');
                    } catch {
                      return 'Source';
                    }
                  };
                  
                  // Generate a brief description based on the source
                  const getSourceDescription = (url: string) => {
                    const domain = getDomainName(url).toLowerCase();
                    if (domain.includes('techcrunch')) {
                      return 'AI is revolutionizing content creation...';
                    } else if (domain.includes('verge')) {
                      return 'Creators must navigate the ethical considerations...';
                    } else if (domain.includes('wired')) {
                      return 'Latest insights on technology trends...';
                    } else if (domain.includes('medium')) {
                      return 'Thought leadership and industry analysis...';
                    } else {
                      return 'Latest updates and insights...';
                    }
                  };

                  return (
                    <div key={idx} className="border-b border-border/50 pb-3 last:border-b-0 last:pb-0">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-sm text-foreground mb-1 truncate">
                            {getDomainName(source)}
                          </h4>
                          <p className="text-xs text-muted-foreground mb-2 leading-relaxed">
                            {getSourceDescription(source)}
                          </p>
                        </div>
                      </div>
                      <a
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-primary hover:text-primary/80 hover:underline inline-flex items-center gap-1"
                      >
                        Open original
                        <svg 
                          className="w-3 h-3" 
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                        >
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={2} 
                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" 
                          />
                        </svg>
                      </a>
                    </div>
                  );
                })}
              </div>
              {draft.sources.length > 6 && (
                <div className="mt-3 pt-2 border-t border-border/50">
                  <p className="text-xs text-muted-foreground text-center">
                    Showing all {draft.sources.length} sources
                  </p>
                </div>
              )}
            </div>

            {/* Tips */}
            <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-sm">💡 Pro Tips</h3>
              <ul className="text-xs text-muted space-y-1">
                <li>• Keep your intro under 2 sentences</li>
                <li>• Use bullet points for scanability</li>
                <li>• Add a clear call-to-action</li>
                <li>• Test your subject line length</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Preview Modal */}
      {previewMode && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b bg-gray-50">
              <div className="flex items-center gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleClosePreview}
                  className="flex items-center gap-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back to Editor
                </Button>
                <h3 className="text-lg font-semibold text-gray-700">Newsletter Preview</h3>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={handleClosePreview}
                className="text-gray-500 hover:text-gray-700"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="overflow-auto max-h-[calc(90vh-80px)]">
              <iframe
                srcDoc={previewHtml}
                className="w-full h-[600px] border-0"
                title="Newsletter Preview"
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}

