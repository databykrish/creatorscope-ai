"use client";

import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  ExternalLink,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Clock,
} from "lucide-react";

export interface Creator {
  id: string;
  name: string;
  handle: string;
  avatar: string;
  platform: "instagram" | "youtube" | "tiktok";
  followers: string;
  engagement: number;
  engagementTrend: "up" | "down";
  uploadConsistency: number;
  campaignReady: "ready" | "review" | "pending";
  niche: string;
  aiSummary: string;
  whyRecommended: string;
  recentPosts: number;
  avgViews: string;
}

const platformColors: Record<string, string> = {
  instagram: "bg-pink-500/10 text-pink-400",
  youtube: "bg-red-500/10 text-red-400",
  tiktok: "bg-cyan-500/10 text-cyan-400",
};

const readinessConfig = {
  ready: {
    icon: CheckCircle2,
    label: "Campaign Ready",
    className: "bg-primary/10 text-primary",
  },
  review: {
    icon: AlertTriangle,
    label: "Needs Review",
    className: "bg-chart-3/10 text-chart-3",
  },
  pending: {
    icon: Clock,
    label: "Pending",
    className: "bg-muted text-muted-foreground",
  },
};

interface CreatorCardProps {
  creator: Creator;
  index: number;
}

export function CreatorCard({ creator, index }: CreatorCardProps) {
  const readiness = readinessConfig[creator.campaignReady];
  const ReadinessIcon = readiness.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08, duration: 0.4, ease: "easeOut" }}
      className="glass-card group relative overflow-hidden rounded-xl p-5 transition-all hover:border-primary/30"
    >
      {/* Scan line effect on hover */}
      <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity group-hover:opacity-100">
        <div className="animate-scan absolute left-0 right-0 h-px bg-primary/40" />
      </div>

      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="h-11 w-11 overflow-hidden rounded-full bg-secondary">
              <div className="flex h-full w-full items-center justify-center text-lg font-bold text-primary">
                {creator.name.charAt(0)}
              </div>
            </div>
            <div
              className={`absolute -bottom-0.5 -right-0.5 rounded-full px-1 py-0.5 text-[9px] font-bold uppercase ${platformColors[creator.platform]}`}
            >
              {creator.platform.slice(0, 2)}
            </div>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-foreground">
              {creator.name}
            </h3>
            <p className="text-xs text-muted-foreground">{creator.handle}</p>
          </div>
        </div>
        <button className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground">
          <ExternalLink className="h-3.5 w-3.5" />
        </button>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3">
        <div>
          <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
            Followers
          </p>
          <p className="mt-0.5 text-sm font-semibold text-foreground">
            {creator.followers}
          </p>
        </div>
        <div>
          <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
            Engagement
          </p>
          <div className="mt-0.5 flex items-center gap-1">
            <span className="text-sm font-semibold text-foreground">
              {creator.engagement}%
            </span>
            {creator.engagementTrend === "up" ? (
              <TrendingUp className="h-3 w-3 text-primary" />
            ) : (
              <TrendingDown className="h-3 w-3 text-destructive" />
            )}
          </div>
        </div>
        <div>
          <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
            Avg Views
          </p>
          <p className="mt-0.5 text-sm font-semibold text-foreground">
            {creator.avgViews}
          </p>
        </div>
      </div>

      {/* Upload Consistency Bar */}
      <div className="mt-4">
        <div className="flex items-center justify-between">
          <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
            Upload Consistency
          </p>
          <span className="text-[10px] font-semibold text-foreground">
            {creator.uploadConsistency}%
          </span>
        </div>
        <div className="mt-1.5 h-1 overflow-hidden rounded-full bg-secondary">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${creator.uploadConsistency}%` }}
            transition={{ delay: index * 0.08 + 0.3, duration: 0.8, ease: "easeOut" }}
            className="h-full rounded-full bg-primary"
          />
        </div>
      </div>

      {/* Campaign Readiness Badge */}
      <div className="mt-4 flex items-center justify-between">
        <span
          className={`inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-[11px] font-semibold ${readiness.className}`}
        >
          <ReadinessIcon className="h-3 w-3" />
          {readiness.label}
        </span>
        <span className="rounded-md bg-secondary px-2 py-1 text-[10px] font-medium text-muted-foreground">
          {creator.niche}
        </span>
      </div>

      {/* AI Summary */}
      <div className="mt-4 rounded-lg border border-border bg-secondary/50 p-3">
        <div className="flex items-center gap-1.5">
          <Sparkles className="h-3 w-3 text-primary" />
          <span className="text-[10px] font-semibold uppercase tracking-wider text-primary">
            AI Summary
          </span>
        </div>
        <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">
          {creator.aiSummary}
        </p>
      </div>

      {/* Why Recommended */}
      <div className="mt-3 rounded-lg border border-primary/10 bg-primary/5 p-3">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-primary">
          Why Recommended?
        </p>
        <p className="mt-1 text-xs leading-relaxed text-foreground/80">
          {creator.whyRecommended}
        </p>
      </div>
    </motion.div>
  );
}
