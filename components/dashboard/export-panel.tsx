"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Download,
  FileSpreadsheet,
  FileText,
  FileJson,
  Check,
  Loader2,
} from "lucide-react";
import { useExport } from "@/hooks/use-export";

const exportFormats = [
  {
    id: "csv",
    label: "CSV Spreadsheet",
    description: "Creator data with all metrics and AI scores",
    icon: FileSpreadsheet,
    size: "~2.4 MB",
  },
  {
    id: "pdf",
    label: "PDF Report",
    description: "Branded campaign readiness report with visuals",
    icon: FileText,
    size: "~8.1 MB",
  },
  {
    id: "json",
    label: "JSON API Format",
    description: "Raw structured data for integration pipelines",
    icon: FileJson,
    size: "~1.8 MB",
  },
];

export function ExportPanel() {
  const { isExporting, error, exportFile } = useExport();
  const [completed, setCompleted] = useState<string[]>([]);

  const handleExport = async (format: "csv" | "json" | "pdf") => {
    try {
      // For demo purposes, export all tracked creators (empty list means all)
      await exportFile(format, []);
      setCompleted((prev) => [...prev, format]);
      setTimeout(() => setCompleted((prev) => prev.filter((c) => c !== format)), 3000);
    } catch (err) {
      console.error("Export failed:", err);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {error && (
        <div className="glass-card rounded-xl bg-destructive/10 p-4 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="glass-card rounded-xl p-6">
        <h3 className="text-sm font-semibold text-foreground">
          Export Creator Data
        </h3>
        <p className="mt-1 text-xs text-muted-foreground">
          Download campaign reports and creator analytics in your preferred format.
        </p>

        <div className="mt-6 grid gap-3 md:grid-cols-3">
          {exportFormats.map((format, i) => (
            <motion.button
              key={format.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              onClick={() => handleExport(format.id as "csv" | "json" | "pdf")}
              disabled={isExporting}
              className="group relative overflow-hidden rounded-xl border border-border bg-secondary/50 p-5 text-left transition-all hover:border-primary/30 hover:bg-secondary disabled:cursor-wait disabled:opacity-60"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <format.icon className="h-5 w-5 text-primary" />
                </div>
                <AnimatePresence mode="wait">
                  {isExporting ? (
                    <motion.div
                      key="loading"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      exit={{ scale: 0 }}
                    >
                      <Loader2 className="h-5 w-5 animate-spin text-primary" />
                    </motion.div>
                  ) : completed.includes(format.id) ? (
                    <motion.div
                      key="done"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      exit={{ scale: 0 }}
                    >
                      <Check className="h-5 w-5 text-primary" />
                    </motion.div>
                  ) : (
                    <motion.div
                      key="download"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      exit={{ scale: 0 }}
                    >
                      <Download className="h-5 w-5 text-muted-foreground transition-colors group-hover:text-primary" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              <h4 className="mt-4 text-sm font-semibold text-foreground">
                {format.label}
              </h4>
              <p className="mt-1 text-xs text-muted-foreground">
                {format.description}
              </p>
              <p className="mt-3 text-[10px] font-medium text-muted-foreground">
                Est. size: {format.size}
              </p>
            </motion.button>
          ))}
        </div>
      </div>
    </div>
  );
}
