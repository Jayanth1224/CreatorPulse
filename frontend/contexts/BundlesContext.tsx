"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getBundles } from '@/lib/api-client';
import { Bundle } from '@/types';

interface BundlesContextType {
  bundles: Bundle[];
  loading: boolean;
  error: string | null;
  refreshBundles: () => Promise<void>;
  lastFetched: number | null;
}

const BundlesContext = createContext<BundlesContextType | undefined>(undefined);

export function BundlesProvider({ children }: { children: React.ReactNode }) {
  const [bundles, setBundles] = useState<Bundle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastFetched, setLastFetched] = useState<number | null>(null);

  const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  const loadBundles = useCallback(async (forceRefresh = false) => {
    // Check if we have cached data that's still valid
    if (!forceRefresh && lastFetched && Date.now() - lastFetched < CACHE_DURATION) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await getBundles();
      
      if (response.error) {
        setError(response.error.detail || "Failed to load bundles");
        setBundles([]);
      } else {
        const bundlesData = Array.isArray(response.data) ? response.data : [];
        setBundles(bundlesData);
        setLastFetched(Date.now());
      }
    } catch (err) {
      setError("Failed to load bundles");
      console.error("Error loading bundles:", err);
      setBundles([]);
    } finally {
      setLoading(false);
    }
  }, [lastFetched]);

  const refreshBundles = useCallback(async () => {
    await loadBundles(true);
  }, [loadBundles]);

  // Load bundles on mount
  useEffect(() => {
    loadBundles();
  }, [loadBundles]);

  const value: BundlesContextType = {
    bundles,
    loading,
    error,
    refreshBundles,
    lastFetched
  };

  return (
    <BundlesContext.Provider value={value}>
      {children}
    </BundlesContext.Provider>
  );
}

export function useBundles() {
  const context = useContext(BundlesContext);
  if (context === undefined) {
    throw new Error('useBundles must be used within a BundlesProvider');
  }
  return context;
}
