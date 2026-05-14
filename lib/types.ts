"use client";

// Creator
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

// Search Response
export interface CreatorSearchResponse {
  creators: Creator[];
  total: number;
  source: "youtube_api" | "ytdlp" | "cached";
  fallback_used: boolean;
}

// Audit
export interface AuditResult {
  creator_id: string;
  upload_history: Array<{ date: string; count: number }>;
  consistency_trend: string;
  engagement_trend: number[];
  risk_flags: string[];
  last_audit_date: string;
}

// Stats
export interface StatsResponse {
  tracked_creators: number;
  avg_engagement: number;
  active_campaigns: number;
  audits_run: number;
  weekly_deltas: {
    creators: number;
    engagement: number;
    campaigns: number;
    audits: number;
  };
}

// Export
export interface ExportResponse {
  export_id: string;
  download_url: string;
  expires_at: string;
  status: "pending" | "ready" | "expired";
}

// Log Entry
export interface LogEntry {
  timestamp: string;
  type: "info" | "success" | "warning" | "process";
  message: string;
}

// Health
export interface HealthResponse {
  status: string;
  version: string;
  youtube_api_ok: boolean;
  ytdlp_available: boolean;
  database_ok: boolean;
}
