"use client";

import { Bell, Search } from "lucide-react";
import { motion } from "framer-motion";

interface HeaderProps {
  activeTab: string;
}

const tabTitles: Record<string, string> = {
  search: "Influencer Search",
  creators: "Creator Analytics",
  analytics: "Performance Insights",
  campaigns: "Campaign Readiness",
  export: "Export Center",
  console: "Processing Console",
  settings: "Settings",
};

export function Header({ activeTab }: HeaderProps) {
  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-card px-6">
      <div className="flex items-center gap-4">
        <motion.h2
          key={activeTab}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-lg font-semibold text-foreground"
        >
          {tabTitles[activeTab] || "Dashboard"}
        </motion.h2>
      </div>

      <div className="flex items-center gap-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search creators, campaigns..."
            className="h-9 w-64 rounded-lg border border-border bg-secondary pl-10 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        <button className="relative flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-secondary text-muted-foreground transition-colors hover:bg-accent hover:text-foreground">
          <Bell className="h-4 w-4" />
          <span className="absolute -right-0.5 -top-0.5 h-2 w-2 rounded-full bg-primary" />
        </button>

        <div className="flex items-center gap-2 rounded-lg border border-border bg-secondary px-3 py-1.5">
          <div className="h-6 w-6 rounded-full bg-primary/20 text-center text-xs font-semibold leading-6 text-primary">
            A
          </div>
          <span className="text-sm font-medium text-foreground">Agency</span>
        </div>
      </div>
    </header>
  );
}
