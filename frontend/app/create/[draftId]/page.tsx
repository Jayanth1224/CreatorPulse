"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Navigation } from "@/components/layout/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { getMockDraft } from "@/lib/mock-data";
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
} from "lucide-react";

export default function EditorPage() {
  const params = useParams();
  const router = useRouter();
  const draftId = params.draftId as string;

  const [draft, setDraft] = useState<Draft | null>(null);
  const [content, setContent] = useState("");
  const [subject, setSubject] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  useEffect(() => {
    // Fetch draft from backend API
    fetch(`http://localhost:8000/api/drafts/${draftId}`)
      .then(res => {
        if (!res.ok) throw new Error('Draft not found');
        return res.json();
      })
      .then((data) => {
        // Transform backend response (snake_case) to match frontend types
        const transformedDraft = {
          ...data,
          bundleName: data.bundle_name || data.bundleName,
          generatedHtml: data.generated_html || data.generatedHtml,
          editedHtml: data.edited_html || data.editedHtml,
          readinessScore: data.readiness_score || data.readinessScore,
          createdAt: data.created_at ? new Date(data.created_at) : (data.createdAt ? new Date(data.createdAt) : new Date()),
          updatedAt: data.updated_at ? new Date(data.updated_at) : (data.updatedAt ? new Date(data.updatedAt) : new Date()),
          sentAt: data.sent_at ? new Date(data.sent_at) : (data.sentAt ? new Date(data.sentAt) : null),
          scheduledFor: data.scheduled_for ? new Date(data.scheduled_for) : (data.scheduledFor ? new Date(data.scheduledFor) : null),
        };
        setDraft(transformedDraft as Draft);
        setContent(data.edited_html || data.generated_html || data.editedHtml || data.generatedHtml);
        setSubject(data.topic || `${data.bundle_name || data.bundleName} Newsletter`);
      })
      .catch(err => {
        console.error('Error loading draft:', err);
        // Fallback to mock data
        getMockDraft(draftId).then((data) => {
          if (data) {
            setDraft(data);
            setContent(data.editedHtml || data.generatedHtml);
            setSubject(data.topic || `${data.bundleName} Newsletter`);
          }
        });
      });
  }, [draftId]);

  // Autosave simulation
  useEffect(() => {
    if (!content || !draft) return;
    
    const timer = setTimeout(() => {
      setIsSaving(true);
      setTimeout(() => {
        setIsSaving(false);
        setLastSaved(new Date());
      }, 500);
    }, 2000);

    return () => clearTimeout(timer);
  }, [content, draft]);

  const handleSend = () => {
    setIsSending(true);
    setTimeout(() => {
      alert("Newsletter sent successfully! (Mock)");
      router.push("/dashboard");
    }, 1500);
  };

  const handleRegenerate = (section: string) => {
    alert(`Regenerating ${section} section... (Mock)`);
  };

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
            <Button variant="outline" size="sm">
              <Undo2 className="h-4 w-4" />
              Revert
            </Button>
            <Button variant="outline" size="sm">
              <Save className="h-4 w-4" />
              Save
            </Button>
            <Button size="sm" onClick={handleSend} disabled={isSending}>
              {isSending ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
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
                  contentEditable
                  suppressContentEditableWarning
                  onInput={(e) => setContent(e.currentTarget.innerHTML)}
                  dangerouslySetInnerHTML={{ __html: content }}
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

