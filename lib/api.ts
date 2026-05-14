"use client";

import { Creator, CreatorSearchResponse, StatsResponse, ExportResponse, LogEntry, HealthResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = "APIError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  const data = await response.json();

  if (!response.ok) {
    throw new APIError(
      response.status,
      data.error || "UNKNOWN_ERROR",
      data.message || "An error occurred",
      data.details
    );
  }

  return data;
}

export const api = {
  // Health
  health: async (): Promise<HealthResponse> => {
    const response = await fetch(`${API_URL}/api/health`);
    return handleResponse(response);
  },

  // Creators
  searchCreators: async (
    query: string,
    platform = "youtube",
    niche?: string,
    sort = "relevance",
    limit = 20
  ): Promise<CreatorSearchResponse> => {
    const params = new URLSearchParams({
      q: query,
      platform,
      sort,
      limit: limit.toString(),
    });

    if (niche) params.append("niche", niche);

    const response = await fetch(`${API_URL}/api/creators/search?${params}`);
    return handleResponse(response);
  },

  getCreator: async (creatorId: string): Promise<Creator> => {
    const response = await fetch(`${API_URL}/api/creators/${creatorId}`);
    return handleResponse(response);
  },

  auditCreator: async (creatorId: string) => {
    const response = await fetch(`${API_URL}/api/creators/${creatorId}/audit`);
    return handleResponse(response);
  },

  // Analytics
  getStats: async (): Promise<StatsResponse> => {
    const response = await fetch(`${API_URL}/api/analytics/stats`);
    return handleResponse(response);
  },

  // Export
  createExport: async (
    format: "csv" | "json" | "pdf",
    creatorIds?: string[],
    searchQuery?: string,
    platform: string = "youtube"
  ): Promise<ExportResponse> => {
    const params = new URLSearchParams({
      format,
      platform,
    });

    // Add creator IDs if provided
    if (creatorIds && creatorIds.length > 0) {
      creatorIds.forEach((id) => params.append("creator_ids", id));
    }

    // Add search query if provided (triggers live data fetch)
    if (searchQuery && searchQuery.trim()) {
      params.append("query", searchQuery);
    }

    const response = await fetch(`${API_URL}/api/export/${format}?${params}`, {
      method: "POST",
    });
    return handleResponse(response);
  },

  downloadExport: async (exportId: string): Promise<Blob> => {
    const response = await fetch(`${API_URL}/api/export/${exportId}/download`);
    if (!response.ok) {
      throw new APIError(
        response.status,
        "DOWNLOAD_FAILED",
        "Failed to download export"
      );
    }
    return response.blob();
  },

  // WebSocket
  connectConsole: (
    onMessage: (entry: LogEntry) => void,
    onError: (error: string) => void
  ): WebSocket => {
    const wsUrl = `${API_URL.replace("http", "ws")}/ws/console`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("Console connected");
    };

    ws.onmessage = (event) => {
      try {
        const entry = JSON.parse(event.data);
        onMessage(entry);
      } catch (error) {
        onError("Failed to parse message");
      }
    };

    ws.onerror = () => {
      onError("WebSocket connection error");
    };

    return ws;
  },
};

export class APIErrorClass extends APIError {}
