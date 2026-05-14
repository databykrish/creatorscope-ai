"use client";

import { useState, useEffect, useCallback } from "react";
import { LogEntry } from "@/lib/types";
import { api } from "@/lib/api";

interface UseProcessingConsoleReturn {
  logs: LogEntry[];
  isConnected: boolean;
  error: string | null;
  clearLogs: () => void;
}

export function useProcessingConsole(): UseProcessingConsoleReturn {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  useEffect(() => {
    let ws: WebSocket | null = null;

    const connect = () => {
      try {
        ws = api.connectConsole(
          (entry: LogEntry) => {
            setLogs((prev) => [...prev, entry]);
            setIsConnected(true);
          },
          (errorMsg: string) => {
            setError(errorMsg);
            setIsConnected(false);
          }
        );

        setIsConnected(true);
      } catch (err) {
        const message = err instanceof Error ? err.message : "WebSocket connection failed";
        setError(message);
        setIsConnected(false);
      }
    };

    connect();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  return {
    logs,
    isConnected,
    error,
    clearLogs,
  };
}
