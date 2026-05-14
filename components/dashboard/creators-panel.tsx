"use client";

import { motion, AnimatePresence } from "framer-motion";
import { CreatorCard, type Creator } from "./creator-card";
import { useCreators } from "@/hooks/use-creators";
import { Skeleton } from "@/components/ui/skeleton";

const mockCreators: Creator[] = [
  {
    id: "1",
    name: "Maya Rodriguez",
    handle: "@mayacreates",
    avatar: "",
    platform: "instagram",
    followers: "2.3M",
    engagement: 4.8,
    engagementTrend: "up",
    uploadConsistency: 92,
    campaignReady: "ready",
    niche: "Lifestyle",
    aiSummary:
      "High-performing lifestyle creator with consistent brand partnerships. Strong audience in 18-34 demo. Excellent story completion rates and saved-post ratios.",
    whyRecommended:
      "Top 3% engagement in lifestyle category. Previous brand collabs with similar products saw 2.4x ROAS.",
    recentPosts: 24,
    avgViews: "890K",
  },
  {
    id: "2",
    name: "Kai Nakamura",
    handle: "@kaitech",
    avatar: "",
    platform: "youtube",
    followers: "1.1M",
    engagement: 6.2,
    engagementTrend: "up",
    uploadConsistency: 88,
    campaignReady: "ready",
    niche: "Tech",
    aiSummary:
      "Trusted tech reviewer with deep audience trust signals. Comment sentiment analysis shows 94% positive. High watch-time retention at 68% avg.",
    whyRecommended:
      "Audience overlap with target demo is 78%. Previous sponsored content outperformed channel average by 1.8x.",
    recentPosts: 12,
    avgViews: "420K",
  },
  {
    id: "3",
    name: "Aria Chen",
    handle: "@ariastyle",
    avatar: "",
    platform: "tiktok",
    followers: "4.7M",
    engagement: 8.1,
    engagementTrend: "up",
    uploadConsistency: 95,
    campaignReady: "ready",
    niche: "Fashion",
    aiSummary:
      "Top-tier fashion content creator with viral potential. Audience skews 65% female, 18-28, high disposable income. Aesthetic alignment with premium brands.",
    whyRecommended:
      "Highest engagement rate in dataset. Recent fashion collab content achieved 12M views. Perfect fit for luxury campaigns.",
    recentPosts: 47,
    avgViews: "2.1M",
  },
];

export function CreatorsPanel() {
  const { creators, isLoading, error } = useCreators({
    tracked: true,
    limit: 12,
  });

  return (
    <div className="space-y-4 p-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Creator Analytics</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Top performing creators in your tracked network
        </p>
      </div>

      {error && (
        <div className="glass-card rounded-xl bg-destructive/10 p-4 text-sm text-destructive">
          {error}
        </div>
      )}

      {isLoading && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-80 rounded-xl" />
          ))}
        </div>
      )}

      {!isLoading && creators.length > 0 && (
        <motion.div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <AnimatePresence>
            {creators.map((creator, index) => (
              <CreatorCard key={creator.id} creator={creator} index={index} />
            ))}
          </AnimatePresence>
        </motion.div>
      )}

      {!isLoading && creators.length === 0 && (
        <div className="glass-card rounded-xl p-12 text-center">
          <p className="text-muted-foreground">No tracked creators yet</p>
        </div>
      )}
    </div>
  );
}
