"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { Navigation } from "@/components/layout/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { getDraft, updateDraft, sendDraft, regenerateSection, saveFeedback } from "@/lib/api-client";
import { Draft } from "@/types";
import {
  Save,
  Send,
  RefreshCw,
  ArrowLeft,
  ThumbsUp,
  ThumbsDown,
  Undo2,
  Loader2,
  Check,
} from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";

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
  
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const editorRef = useRef<HTMLDivElement>(null);
  const isUserEditingRef = useRef(false);

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
      const data = response.data;
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
      };
      setDraft(transformedDraft as Draft);
      
      const htmlContent = data.edited_html || data.generated_html;
      const generatedContent = data.generated_html;
      
      setContent(htmlContent);
      setOriginalContent(generatedContent); // Store original for revert
      
      // Set initial content only if editor is not being edited by user
      if (editorRef.current && !isUserEditingRef.current) {
        editorRef.current.innerHTML = htmlContent;
      }
      
      setSubject(data.topic || `${data.bundle_name} Newsletter`);
    }
  }
  
  // Effect to update editor when content changes from outside (e.g., initial load)
  useEffect(() => {
    if (editorRef.current && content && !isUserEditingRef.current) {
      editorRef.current.innerHTML = content;
    }
  }, [content]);

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

  const handleRegenerate = async (section: string) => {
    const response = await regenerateSection(draftId, section);
    
    if (response.data) {
      // Update content with regenerated section
      // This is simplified - in production you'd merge the new section
      alert(`${section} section regenerated!`);
    }
  };

  const handleFeedback = async (sectionId: string, reaction: 'thumbs_up' | 'thumbs_down') => {
    await saveFeedback(draftId, sectionId, reaction);
  };

  const handleRevert = () => {
    if (!originalContent) return;
    
    const confirmRevert = window.confirm(
      "Are you sure you want to revert to the original AI-generated content? All your edits will be lost."
    );
    
    if (confirmRevert) {
      setContent(originalContent);
      if (editorRef.current) {
        editorRef.current.innerHTML = originalContent;
      }
      // Trigger autosave to update the database
      saveContent(originalContent);
    }
  };

  const handleManualSave = async () => {
    if (!content) return;
    await saveContent(content);
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
              <Label htmlFor="content" className="text-base font-semibold mb-2">
                Newsletter Content
              </Label>
              <div className="bg-surface border border-border rounded-lg p-6 min-h-[600px]">
                <div
                  ref={editorRef}
                  contentEditable
                  suppressContentEditableWarning
                  onInput={(e) => {
                    isUserEditingRef.current = true;
                    setContent(e.currentTarget.innerHTML);
                  }}
                  onBlur={() => {
                    isUserEditingRef.current = false;
                  }}
                  className="prose prose-sm max-w-none focus:outline-none"
                  style={{
                    minHeight: "500px",
                  }}
                />
              </div>
              <p className="text-xs text-muted mt-2">
                Click to edit. Changes are automatically saved.
              </p>
            </div>

            {/* Section Actions */}
            <div className="flex flex-wrap gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleRegenerate("intro")}
              >
                <RefreshCw className="h-4 w-4" />
                Regenerate Intro
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleRegenerate("insights")}
              >
                <RefreshCw className="h-4 w-4" />
                Regenerate Insights
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleRegenerate("trends")}
              >
                <RefreshCw className="h-4 w-4" />
                Regenerate Trends
              </Button>
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

            {/* Feedback */}
            <div className="bg-surface border border-border rounded-lg p-4">
              <h3 className="font-semibold mb-4">How's this draft?</h3>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="flex-1">
                  <ThumbsUp className="h-4 w-4" />
                  Good
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  <ThumbsDown className="h-4 w-4" />
                  Needs Work
                </Button>
              </div>
            </div>

            {/* Sources */}
            <div className="bg-surface border border-border rounded-lg p-4">
              <h3 className="font-semibold mb-3">Sources ({draft.sources.length})</h3>
              <div className="space-y-2">
                {draft.sources.slice(0, 5).map((source, idx) => (
                  <a
                    key={idx}
                    href={source}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-primary hover:underline block truncate"
                  >
                    {source}
                  </a>
                ))}
              </div>
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
    </>
  );
}

