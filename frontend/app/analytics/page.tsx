"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Navigation } from "@/components/layout/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getMockAnalytics, getMockDrafts } from "@/lib/mock-data";
import { AnalyticsSummary, Draft } from "@/types";
import { formatDateTime } from "@/lib/utils";
import {
  TrendingUp,
  TrendingDown,
  Mail,
  MousePointerClick,
  Clock,
  CheckCircle,
  Eye,
} from "lucide-react";

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [timeframe, setTimeframe] = useState<"7d" | "30d">("7d");

  useEffect(() => {
    Promise.all([getMockAnalytics(), getMockDrafts()]).then(
      ([analyticsData, draftsData]) => {
        setAnalytics(analyticsData);
        setDrafts(draftsData.filter((d) => d.status === "sent"));
      }
    );
  }, []);

  if (!analytics) {
    return (
      <>
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-border rounded w-1/4"></div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-32 bg-border rounded"></div>
              ))}
            </div>
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
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-extrabold mb-2">Analytics</h1>
            <p className="text-muted">
              Track your newsletter performance and engagement metrics.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant={timeframe === "7d" ? "default" : "outline"}
              size="sm"
              onClick={() => setTimeframe("7d")}
            >
              7 Days
            </Button>
            <Button
              variant={timeframe === "30d" ? "default" : "outline"}
              size="sm"
              onClick={() => setTimeframe("30d")}
            >
              30 Days
            </Button>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard
            title="Open Rate"
            value={`${analytics.openRate.toFixed(1)}%`}
            change={+5.2}
            icon={<Mail className="h-5 w-5" />}
            description="Emails opened"
          />
          <MetricCard
            title="Click-Through Rate"
            value={`${analytics.clickThroughRate.toFixed(1)}%`}
            change={+2.1}
            icon={<MousePointerClick className="h-5 w-5" />}
            description="Links clicked"
          />
          <MetricCard
            title="Avg Review Time"
            value={`${analytics.avgReviewTime.toFixed(1)} min`}
            change={-3.5}
            icon={<Clock className="h-5 w-5" />}
            description="Time to send"
          />
          <MetricCard
            title="Acceptance Rate"
            value={`${analytics.draftAcceptanceRate.toFixed(1)}%`}
            change={+8.3}
            icon={<CheckCircle className="h-5 w-5" />}
            description="Drafts sent"
          />
        </div>

        {/* Summary Stats */}
        <div className="grid sm:grid-cols-3 gap-4 mb-8">
          <Card className="p-6">
            <div className="text-sm text-muted mb-1">Total Drafts</div>
            <div className="text-3xl font-bold">{analytics.totalDrafts}</div>
          </Card>
          <Card className="p-6">
            <div className="text-sm text-muted mb-1">Total Sent</div>
            <div className="text-3xl font-bold">{analytics.totalSent}</div>
          </Card>
          <Card className="p-6">
            <div className="text-sm text-muted mb-1">Time Saved</div>
            <div className="text-3xl font-bold">
              {(analytics.totalSent * 2.5).toFixed(0)} hrs
            </div>
          </Card>
        </div>

        {/* Performance Table */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted">
                      Newsletter
                    </th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-muted">
                      Sent Date
                    </th>
                    <th className="text-center py-3 px-4 text-sm font-medium text-muted">
                      Opens
                    </th>
                    <th className="text-center py-3 px-4 text-sm font-medium text-muted">
                      Clicks
                    </th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-muted">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {drafts.map((draft) => (
                    <tr key={draft.id} className="border-b border-border hover:bg-surface/50">
                      <td className="py-3 px-4">
                        <div className="font-medium">
                          {draft.topic || draft.bundleName}
                        </div>
                        <div className="text-xs text-muted">{draft.bundleName}</div>
                      </td>
                      <td className="py-3 px-4 text-sm text-muted">
                        {draft.sentAt ? formatDateTime(draft.sentAt) : "-"}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge variant="secondary">
                          {Math.floor(Math.random() * 50 + 30)}%
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge variant="secondary">
                          {Math.floor(Math.random() * 15 + 5)}%
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <Link href={`/create/${draft.id}`}>
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                            View
                          </Button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </main>
    </>
  );
}

function MetricCard({
  title,
  value,
  change,
  icon,
  description,
}: {
  title: string;
  value: string;
  change: number;
  icon: React.ReactNode;
  description: string;
}) {
  const isPositive = change > 0;
  const isNegative = change < 0;

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-sm font-medium text-muted">{title}</div>
        <div className="text-primary">{icon}</div>
      </div>
      <div className="text-3xl font-bold mb-1">{value}</div>
      <div className="flex items-center gap-2">
        <span className="text-xs text-muted">{description}</span>
        {change !== 0 && (
          <span
            className={`flex items-center gap-1 text-xs font-medium ${
              isPositive
                ? "text-green-600"
                : isNegative
                ? "text-red-600"
                : "text-muted"
            }`}
          >
            {isPositive ? (
              <TrendingUp className="h-3 w-3" />
            ) : (
              <TrendingDown className="h-3 w-3" />
            )}
            {Math.abs(change).toFixed(1)}%
          </span>
        )}
      </div>
    </Card>
  );
}

