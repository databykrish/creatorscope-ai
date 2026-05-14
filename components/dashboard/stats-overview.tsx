"use client";

import { motion } from "framer-motion";
import { Users, TrendingUp, Zap, BarChart3 } from "lucide-react";
import { useStats } from "@/hooks/use-stats";
import { Skeleton } from "@/components/ui/skeleton";

export function StatsOverview() {
  const { stats, isLoading, error } = useStats();

  if (error) {
    return (
      <div className="glass-card rounded-xl bg-destructive/10 p-6 text-sm text-destructive">
        {error}
      </div>
    );
  }

  if (isLoading || !stats) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Skeleton key={i} className="h-32 rounded-xl" />
        ))}
      </div>
    );
  }

  const statCards = [
    {
      label: "Tracked Creators",
      value: stats.tracked_creators.toLocaleString(),
      change: "+324",
      trend: "up",
      icon: Users,
    },
    {
      label: "Avg. Engagement",
      value: `${stats.avg_engagement}%`,
      change: "+0.8%",
      trend: "up",
      icon: TrendingUp,
    },
    {
      label: "Active Campaigns",
      value: stats.active_campaigns,
      change: `+${stats.weekly_deltas.campaigns}`,
      trend: "up",
      icon: Zap,
    },
    {
      label: "AI Audits Run",
      value: stats.audits_run.toLocaleString(),
      change: `+${stats.weekly_deltas.audits}`,
      trend: "up",
      icon: BarChart3,
    },
  ];

  return (
    <div className="grid gap-4 p-6 sm:grid-cols-2 xl:grid-cols-4">
      {statCards.map((stat, i) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1, duration: 0.4 }}
          className="glass-card rounded-xl p-5"
        >
          <div className="flex items-center justify-between">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
              {stat.label}
            </p>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <stat.icon className="h-4 w-4 text-primary" />
            </div>
          </div>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground">
            {stat.value}
          </p>
          <p className="mt-1 text-xs font-medium text-primary">
            {stat.change} this week
          </p>
        </motion.div>
      ))}
    </div>
  );
}
