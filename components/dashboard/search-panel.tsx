"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, SlidersHorizontal, X } from "lucide-react";
import { CreatorCard } from "./creator-card";
import { useCreators } from "@/hooks/use-creators";
import { Skeleton } from "@/components/ui/skeleton";

const nicheFilters = [
  "All Niches",
  "Lifestyle",
  "Tech",
  "Fashion",
  "Fitness",
  "Food",
  "Travel",
];

export function SearchPanel() {
  const [query, setQuery] = useState("");
  const [activePlatform, setActivePlatform] = useState("youtube");
  const [activeNiche, setActiveNiche] = useState("All Niches");
  const [showFilters, setShowFilters] = useState(false);

  // Use the custom hook to fetch creators from backend
  const { creators, isLoading, error, fallbackUsed } = useCreators({
    query,
    platform: activePlatform,
    niche: activeNiche === "All Niches" ? undefined : activeNiche,
    limit: 20,
  });

  const handleSearch = (val: string) => {
    setQuery(val);
  };

  return (
    <div className="space-y-6 p-6">
      {/* Search Bar */}
      <div className="glass-card flex items-center gap-3 rounded-xl p-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="Search creators on YouTube, Instagram, TikTok..."
            className="h-10 w-full rounded-lg border border-border bg-background pl-10 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
            disabled={isLoading}
          />
          {query && (
            <button
              onClick={() => handleSearch("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`flex h-10 items-center gap-2 rounded-lg border px-4 text-sm font-medium transition-colors ${
            showFilters
              ? "border-primary bg-primary/10 text-primary"
              : "border-border bg-secondary text-muted-foreground hover:text-foreground"
          }`}
        >
          <SlidersHorizontal className="h-4 w-4" />
          Filters
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="glass-card rounded-xl bg-destructive/10 p-4 text-sm text-destructive">
          ⚠️ {error}
        </div>
      )}

      {/* Data Source Info */}
      {fallbackUsed && (
        <div className="glass-card rounded-xl bg-blue-500/10 p-4 text-sm text-blue-600">
          ℹ️ Using yt-dlp scraper (YouTube API not configured). <a href="https://developers.google.com/youtube/v3" target="_blank" rel="noopener noreferrer" className="underline">Set up API key</a> for real-time data.
        </div>
      )}

      {/* Filters */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="glass-card space-y-4 rounded-xl p-4">
              <div>
                <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                  Platform
                </p>
                <div className="flex flex-wrap gap-2">
                  {[
                    { value: "youtube", label: "YouTube" },
                    { value: "instagram", label: "Instagram" },
                    { value: "tiktok", label: "TikTok" },
                  ].map((f) => (
                    <button
                      key={f.value}
                      onClick={() => setActivePlatform(f.value)}
                      className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                        activePlatform === f.value
                          ? "bg-primary text-primary-foreground"
                          : "bg-secondary text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {f.label}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                  Niche
                </p>
                <div className="flex flex-wrap gap-2">
                  {nicheFilters.map((f) => (
                    <button
                      key={f}
                      onClick={() => setActiveNiche(f)}
                      className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                        activeNiche === f
                          ? "bg-primary text-primary-foreground"
                          : "bg-secondary text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {f}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading State */}
      {isLoading && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-80 rounded-xl" />
          ))}
        </div>
      )}

      {/* Results */}
      {!isLoading && creators.length > 0 && (
        <>
          <p className="text-sm text-muted-foreground">Found {creators.length} creators</p>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <AnimatePresence mode="popLayout">
              {creators.map((creator, i) => (
                <CreatorCard key={creator.id} creator={creator} index={i} />
              ))}
            </AnimatePresence>
          </div>
        </>
      )}

      {/* Empty State */}
      {!isLoading && !error && creators.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20"
        >
          <Search className="h-12 w-12 text-muted-foreground/30" />
          <p className="mt-4 text-sm font-medium text-muted-foreground">
            {query ? "No creators found" : "Start searching for creators"}
          </p>
        </motion.div>
      )}
    </div>
  );
}
