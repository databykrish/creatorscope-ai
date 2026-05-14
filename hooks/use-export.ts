"use client";

import { useState, useCallback } from "react";
import { api } from "@/lib/api";

interface UseExportReturn {
  isExporting: boolean;
  error: string | null;
  exportFile: (
    format: "csv" | "json" | "pdf",
    creatorIds?: string[],
    searchQuery?: string,
    platform?: string
  ) => Promise<void>;
}

export function useExport(): UseExportReturn {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const exportFile = useCallback(
    async (
      format: "csv" | "json" | "pdf",
      creatorIds?: string[],
      searchQuery?: string,
      platform: string = "youtube"
    ) => {
      setIsExporting(true);
      setError(null);

      try {
        // Create export with search query and platform for live data
        const exportResponse = await api.createExport(
          format,
          creatorIds,
          searchQuery,
          platform
        );

        // Download file
        const blob = await api.downloadExport(exportResponse.export_id);

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;

        const filename = `creators_export_${Date.now()}.${format}`;
        link.setAttribute("download", filename);

        document.body.appendChild(link);
        link.click();

        // Clean up
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Export failed";
        setError(message);
      } finally {
        setIsExporting(false);
      }
    },
    []
  );

  return {
    isExporting,
    error,
    exportFile,
  };
}
