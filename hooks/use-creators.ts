"use client";

import { useState, useEffect, useCallback } from "react";
import { Creator, CreatorSearchResponse } from "@/lib/types";
import { api } from "@/lib/api";

interface UseCreatorsOptions {
  query?: string;
  platform?: string;
  tracked?: boolean;
  niche?: string;
  sort?: "relevance" | "engagement" | "followers";
  limit?: number;
}

interface UseCreatorsReturn {
  creators: Creator[];
  isLoading: boolean;
  error: string | null;
  total: number;
  source: string;
  fallbackUsed: boolean;
  refetch: () => Promise<void>;
}

export function useCreators(options: UseCreatorsOptions = {}): UseCreatorsReturn {
  const {
    query = "",
    platform = "youtube",
    tracked = false,
    niche,
    sort = "relevance",
    limit = 20,
  } = options;

  const [creators, setCreators] = useState<Creator[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [source, setSource] = useState("youtube_api");
  const [fallbackUsed, setFallbackUsed] = useState(false);

  const fetchCreators = useCallback(async () => {
    if (!query && !tracked) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      if (tracked) {
        // For tracked creators, use empty query
        const response = await api.searchCreators("", platform, niche, sort, limit);
        setCreators(response.creators);
        setTotal(response.total);
        setSource(response.source);
        setFallbackUsed(response.fallback_used);
      } else {
        const response = await api.searchCreators(query, platform, niche, sort, limit);
        setCreators(response.creators);
        setTotal(response.total);
        setSource(response.source);
        setFallbackUsed(response.fallback_used);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to fetch creators";
      setError(message);
      setCreators([]);
    } finally {
      setIsLoading(false);
    }
  }, [query, tracked, platform, niche, sort, limit]);

  useEffect(() => {
    fetchCreators();
  }, [fetchCreators]);

  return {
    creators,
    isLoading,
    error,
    total,
    source,
    fallbackUsed,
    refetch: fetchCreators,
  };
}
