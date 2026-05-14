"use client";

import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Terminal, Circle } from "lucide-react";
import { useProcessingConsole } from "@/hooks/use-console";

const typeColors: Record<string, string> = {
  info: "text-chart-2",
  success: "text-primary",
  warning: "text-chart-3",
  process: "text-foreground",
};

const dotColors: Record<string, string> = {
  info: "text-chart-2",
  success: "text-primary",
  warning: "text-chart-3",
  process: "text-muted-foreground",
};

export function ProcessingConsole() {
  const { logs, isConnected, error, clearLogs } = useProcessingConsole();
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="glass-card overflow-hidden rounded-xl">
      <div className="flex items-center gap-2 border-b border-border px-4 py-3">
        <Terminal className="h-4 w-4 text-primary" />
        <span className="text-xs font-semibold uppercase tracking-wider text-foreground">
          Processing Console
        </span>
        <div className="ml-auto flex items-center gap-1.5">
          {isConnected ? (
            <>
              <span className="h-2 w-2 animate-pulse rounded-full bg-primary" />
              <span className="text-[10px] font-medium text-primary">LIVE</span>
            </>
          ) : (
            <>
              <span className="h-2 w-2 rounded-full bg-destructive" />
              <span className="text-[10px] font-medium text-destructive">OFFLINE</span>
            </>
          )}
        </div>
      </div>

      {error && (
        <div className="border-b border-border bg-destructive/10 px-4 py-2 text-xs text-destructive">
          Connection error: {error}
        </div>
      )}

      <div
        ref={scrollRef}
        className="h-96 overflow-y-auto bg-background/50 p-4 font-mono text-xs"
      >
        {logs.length === 0 ? (
          <div className="flex h-full items-center justify-center text-muted-foreground">
            Waiting for console output...
          </div>
        ) : (
          logs.map((log, i) => (
            <motion.div
              key={`${log.timestamp}-${i}`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className="flex items-start gap-2 py-0.5"
            >
              <span className="shrink-0 text-muted-foreground">
                [{log.timestamp}]
              </span>
              <Circle
                className={`mt-0.5 h-1.5 w-1.5 shrink-0 ${dotColors[log.type]}`}
                fill="currentColor"
              />
              <span className={`flex-1 ${typeColors[log.type]}`}>
                {log.message}
              </span>
            </motion.div>
          ))
        )}
      </div>

      <div className="border-t border-border bg-secondary/30 px-4 py-3">
        <button
          onClick={clearLogs}
          className="text-[10px] font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          Clear Console
        </button>
      </div>
    </div>
  );
}
