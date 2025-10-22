"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Navigation } from "@/components/layout/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getDrafts } from "@/lib/api-client";
import { formatDateTime } from "@/lib/utils";
import { Draft, Bundle } from "@/types";
import { FileEdit, RefreshCw, Send, Clock, CheckCircle2, Rss, Twitter, Youtube, Settings } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { BundleSourceModal } from "@/components/BundleSourceModal";
import { CreateBundleModal } from "@/components/CreateBundleModal";
import { getBundles } from "@/lib/api-client";

type TabType = "all" | "sent" | "scheduled" | "bundles";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}

function DashboardContent() {
  const [activeTab, setActiveTab] = useState<TabType>("all");
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDrafts();
  }, []);

  async function loadDrafts() {
    setLoading(true);
    setError(null);
    
    const response = await getDrafts();
    
    if (response.error) {
      setError(response.error.detail);
      setLoading(false);
      return;
    }
    
    if (response.data && Array.isArray(response.data)) {
      // Transform snake_case to camelCase for dates
      const transformedDrafts = response.data.map((draft: any) => ({
        ...draft,
        userId: draft.user_id || draft.userId,
        bundleId: draft.bundle_id || draft.bundleId,
        bundleName: draft.bundle_name || draft.bundleName,
        generatedHtml: draft.generated_html || draft.generatedHtml,
        editedHtml: draft.edited_html || draft.editedHtml,
        readinessScore: draft.readiness_score || draft.readinessScore,
        createdAt: draft.created_at ? new Date(draft.created_at) : (draft.createdAt ? new Date(draft.createdAt) : null),
        updatedAt: draft.updated_at ? new Date(draft.updated_at) : (draft.updatedAt ? new Date(draft.updatedAt) : null),
        sentAt: draft.sent_at ? new Date(draft.sent_at) : (draft.sentAt ? new Date(draft.sentAt) : null),
        scheduledFor: draft.scheduled_for ? new Date(draft.scheduled_for) : (draft.scheduledFor ? new Date(draft.scheduledFor) : null),
      }));
      
      setDrafts(transformedDrafts);
    }
    
    setLoading(false);
  }

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

        {/* Content based on active tab */}
        {activeTab === "bundles" ? (
          <BundlesSection />
        ) : (
          <>
            {/* Drafts List */}
            {error ? (
              <Card className="p-12 text-center border-destructive">
                <h3 className="text-lg font-semibold mb-2 text-destructive">Error Loading Drafts</h3>
                <p className="text-muted mb-6">{error}</p>
                <Button onClick={loadDrafts}>Retry</Button>
              </Card>
            ) : loading ? (
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
          </>
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
              {draft.topic || `${draft.bundleName || 'Newsletter'} Newsletter`}
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
            {draft.bundleName || 'Unknown Bundle'} • {draft.tone || 'default'} tone • {formatDateTime(draft.createdAt)}
          </p>

          <div
            className="text-sm text-foreground line-clamp-2 prose prose-sm max-w-none"
            dangerouslySetInnerHTML={{
              __html: (draft.generatedHtml || "").substring(0, 200) + "...",
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

function BundlesSection() {
  const [bundles, setBundles] = useState<Bundle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedBundle, setSelectedBundle] = useState<Bundle | null>(null);
  const [showSourceModal, setShowSourceModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    loadBundles();
  }, []);

  async function loadBundles() {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getBundles();
      if (response.error) {
        setError(response.error.detail || "Failed to load bundles");
        setBundles([]);
      } else {
        setBundles(Array.isArray(response.data) ? response.data : []);
      }
    } catch (err) {
      setError("Failed to load bundles");
      console.error("Error loading bundles:", err);
      setBundles([]);
    } finally {
      setLoading(false);
    }
  }

  const handleManageSources = (bundle: Bundle) => {
    setSelectedBundle(bundle);
    setShowSourceModal(true);
  };

  const handleCreateBundle = async (bundleData: { key: string; label: string; description: string }) => {
    // TODO: Implement API call to create bundle
    console.log("Creating bundle:", bundleData);
    // For now, just reload bundles
    await loadBundles();
  };

  const getSourceStats = (bundle: Bundle) => {
    const sources = bundle.sources || [];
    if (!Array.isArray(sources)) {
      return {};
    }
    
    const stats = sources.reduce((acc, source) => {
      if (typeof source === 'string') {
        acc.rss = (acc.rss || 0) + 1;
      } else {
        acc[source.type] = (acc[source.type] || 0) + 1;
      }
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
        return null;
    }
  };

  if (loading) {
    return (
      <div className="grid gap-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="p-6 animate-pulse">
            <div className="h-6 bg-border rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-border rounded w-full mb-2"></div>
            <div className="h-4 bg-border rounded w-2/3"></div>
          </Card>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <Card className="p-12 text-center border-destructive">
        <h3 className="text-lg font-semibold mb-2 text-destructive">Error Loading Bundles</h3>
        <p className="text-muted mb-6">{error}</p>
        <Button onClick={loadBundles}>Retry</Button>
      </Card>
    );
  }

  if (bundles.length === 0) {
    return (
      <Card className="p-12 text-center">
        <Settings className="h-12 w-12 text-muted mx-auto mb-4" />
        <h3 className="text-lg font-semibold mb-2">No bundles found</h3>
        <p className="text-muted mb-6">
          Create your first bundle to start organizing your content sources.
        </p>
        <Button onClick={() => setShowCreateModal(true)}>
          Create New Bundle
        </Button>
      </Card>
    );
  }

  return (
    <>
      <div className="grid gap-4">
        {bundles.map((bundle) => {
          const stats = getSourceStats(bundle);
          const totalSources = Object.values(stats).reduce((sum, count) => sum + count, 0);

          return (
            <Card key={bundle.id} className="p-6 hover:border-primary/50 transition-colors">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-lg">{bundle.label}</h3>
                    <Badge variant="secondary">
                      {totalSources} sources
                    </Badge>
                    {bundle.isPreset && (
                      <Badge variant="secondary">Preset</Badge>
                    )}
                  </div>
                  
                  <p className="text-sm text-muted mb-3">
                    {bundle.description}
                  </p>

                  {/* Source Type Indicators */}
                  <div className="flex items-center gap-4">
                    {Object.entries(stats).map(([type, count]) => (
                      <div key={type} className="flex items-center gap-1">
                        {getSourceIcon(type)}
                        <span className="text-sm text-muted">{count}</span>
                      </div>
                    ))}
                    {totalSources === 0 && (
                      <span className="text-sm text-muted">No sources configured</span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleManageSources(bundle)}
                    className="flex items-center gap-2"
                  >
                    <Settings className="h-4 w-4" />
                    Manage Sources
                  </Button>
                  <Link href={`/create?bundle=${bundle.id}`}>
                    <Button size="sm">
                      Create Draft
                    </Button>
                  </Link>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Source Management Modal */}
      {selectedBundle && (
        <BundleSourceModal
          bundleId={selectedBundle.id}
          bundleName={selectedBundle.label}
          isOpen={showSourceModal}
          onClose={() => {
            setShowSourceModal(false);
            setSelectedBundle(null);
          }}
        />
      )}

      {/* Create Bundle Modal */}
      <CreateBundleModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreateBundle={handleCreateBundle}
      />
    </>
  );
}

