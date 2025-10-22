"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, TrendingUp, Clock, AlertTriangle } from "lucide-react";

interface PerformanceMetrics {
  total_calls: number;
  avg_duration_ms: number;
  slow_calls: number;
  error_calls: number;
  endpoints: Record<string, {
    calls: number;
    avg_duration_ms: number;
    min_duration_ms: number;
    max_duration_ms: number;
    slow_calls: number;
    error_calls: number;
  }>;
}

export function PerformanceMonitor() {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/performance/metrics?hours=24');
      if (!response.ok) {
        throw new Error('Failed to fetch performance metrics');
      }
      
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch metrics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Loader2 className="h-5 w-5 animate-spin" />
            Performance Monitor
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">
            <p className="text-muted">Loading performance metrics...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            Performance Monitor
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">
            <p className="text-red-500 mb-4">{error}</p>
            <Button onClick={fetchMetrics} variant="outline">
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!metrics) {
    return null;
  }

  const slowEndpoints = Object.entries(metrics.endpoints)
    .filter(([_, data]) => data.avg_duration_ms > 1000)
    .sort(([_, a], [__, b]) => b.avg_duration_ms - a.avg_duration_ms);

  return (
    <div className="space-y-4">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted">Total API Calls</p>
                <p className="text-2xl font-bold">{metrics.total_calls}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted">Avg Response Time</p>
                <p className="text-2xl font-bold">{metrics.avg_duration_ms.toFixed(0)}ms</p>
              </div>
              <Clock className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted">Slow Calls</p>
                <p className="text-2xl font-bold text-orange-500">{metrics.slow_calls}</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted">Error Calls</p>
                <p className="text-2xl font-bold text-red-500">{metrics.error_calls}</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Endpoint Performance */}
      {Object.keys(metrics.endpoints).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Endpoint Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(metrics.endpoints).map(([endpoint, data]) => (
                <div key={endpoint} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium">{endpoint}</p>
                    <p className="text-sm text-muted">
                      {data.calls} calls • {data.avg_duration_ms.toFixed(0)}ms avg
                    </p>
                  </div>
                  <div className="flex gap-2">
                    {data.slow_calls > 0 && (
                      <Badge variant="secondary" className="text-orange-600">
                        {data.slow_calls} slow
                      </Badge>
                    )}
                    {data.error_calls > 0 && (
                      <Badge variant="destructive">
                        {data.error_calls} errors
                      </Badge>
                    )}
                    <Badge variant={data.avg_duration_ms > 1000 ? "destructive" : "secondary"}>
                      {data.avg_duration_ms.toFixed(0)}ms
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Slow Endpoints Alert */}
      {slowEndpoints.length > 0 && (
        <Card className="border-orange-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-600">
              <AlertTriangle className="h-5 w-5" />
              Slow Endpoints (>1s)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {slowEndpoints.map(([endpoint, data]) => (
                <div key={endpoint} className="flex items-center justify-between p-2 bg-orange-50 rounded">
                  <span className="font-medium">{endpoint}</span>
                  <Badge variant="destructive">
                    {data.avg_duration_ms.toFixed(0)}ms avg
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="flex justify-end">
        <Button onClick={fetchMetrics} variant="outline" size="sm">
          Refresh Metrics
        </Button>
      </div>
    </div>
  );
}
