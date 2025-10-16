"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Navigation } from "@/components/layout/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getMockDrafts } from "@/lib/mock-data";
import { formatDateTime } from "@/lib/utils";
import { Draft } from "@/types";
import { FileEdit, RefreshCw, Send, Clock, CheckCircle2 } from "lucide-react";

type TabType = "all" | "sent" | "scheduled" | "bundles";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<TabType>("all");
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMockDrafts().then((data) => {
      setDrafts(data);
      setLoading(false);
    });
  }, []);

  const filteredDrafts = drafts.filter((draft) => {
    if (activeTab === "all") return true;
    if (activeTab === "sent") return draft.status === "sent";
    if (activeTab === "scheduled") return draft.status === "scheduled";
    return false;
  });

  return (
    <>
      <Navigation />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold mb-2">Dashboard</h1>
          <p className="text-muted">
            Manage your drafts, track sent newsletters, and review your content.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-2 border-b border-border mb-6 overflow-x-auto">
          <TabButton
            active={activeTab === "all"}
            onClick={() => setActiveTab("all")}
          >
            All Drafts
          </TabButton>
          <TabButton
            active={activeTab === "sent"}
            onClick={() => setActiveTab("sent")}
          >
            Sent
          </TabButton>
          <TabButton
            active={activeTab === "scheduled"}
            onClick={() => setActiveTab("scheduled")}
          >
            Scheduled
          </TabButton>
          <TabButton
            active={activeTab === "bundles"}
            onClick={() => setActiveTab("bundles")}
          >
            Bundles
          </TabButton>
        </div>

        {/* Drafts List */}
        {loading ? (
          <div className="grid gap-4">
            {[1, 2, 3].map((i) => (
              <Card key={i} className="p-6 animate-pulse">
                <div className="h-6 bg-border rounded w-1/3 mb-4"></div>
                <div className="h-4 bg-border rounded w-full mb-2"></div>
                <div className="h-4 bg-border rounded w-2/3"></div>
              </Card>
            ))}
          </div>
        ) : filteredDrafts.length === 0 ? (
          <Card className="p-12 text-center">
            <FileEdit className="h-12 w-12 text-muted mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No drafts found</h3>
            <p className="text-muted mb-6">
              {activeTab === "all"
                ? "Create your first newsletter draft to get started."
                : `You don't have any ${activeTab} drafts yet.`}
            </p>
            <Link href="/create">
              <Button>Create New Draft</Button>
            </Link>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredDrafts.map((draft) => (
              <DraftCard key={draft.id} draft={draft} />
            ))}
          </div>
        )}
      </main>
    </>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
        active
          ? "border-primary text-primary"
          : "border-transparent text-muted hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

function DraftCard({ draft }: { draft: Draft }) {
  const statusConfig = {
    draft: {
      icon: <Clock className="h-4 w-4" />,
      label: "Draft",
      variant: "default" as const,
    },
    sent: {
      icon: <CheckCircle2 className="h-4 w-4" />,
      label: "Sent",
      variant: "success" as const,
    },
    scheduled: {
      icon: <Clock className="h-4 w-4" />,
      label: "Scheduled",
      variant: "warning" as const,
    },
  };

  const status = statusConfig[draft.status];

  return (
    <Card className="p-6 hover:border-primary/50 transition-colors">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="font-semibold text-lg">
              {draft.topic || `${draft.bundleName} Newsletter`}
            </h3>
            <Badge variant={status.variant} className="flex items-center gap-1">
              {status.icon}
              {status.label}
            </Badge>
            {draft.readinessScore && (
              <Badge variant="secondary">{draft.readinessScore}% Ready</Badge>
            )}
          </div>
          
          <p className="text-sm text-muted mb-3">
            {draft.bundleName} • {draft.tone} tone • {formatDateTime(draft.createdAt)}
          </p>

          <div
            className="text-sm text-foreground line-clamp-2 prose prose-sm max-w-none"
            dangerouslySetInnerHTML={{
              __html: draft.generatedHtml.substring(0, 200) + "...",
            }}
          />
        </div>

        <div className="flex items-center gap-2 lg:flex-col lg:items-stretch">
          <Link href={`/create/${draft.id}`} className="flex-1 lg:flex-initial">
            <Button variant="default" size="sm" className="w-full">
              <FileEdit className="h-4 w-4" />
              {draft.status === "draft" ? "Edit" : "View"}
            </Button>
          </Link>
          {draft.status === "draft" && (
            <>
              <Button variant="outline" size="sm" className="flex-1 lg:flex-initial">
                <RefreshCw className="h-4 w-4" />
                Regenerate
              </Button>
              <Button variant="ghost" size="sm" className="flex-1 lg:flex-initial">
                <Send className="h-4 w-4" />
                Send
              </Button>
            </>
          )}
        </div>
      </div>
    </Card>
  );
}

