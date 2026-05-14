"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Search,
  BarChart3,
  Users,
  Zap,
  Download,
  Terminal,
  Settings,
  ChevronLeft,
  ChevronRight,
  ScanLine,
} from "lucide-react";

const navItems = [
  { icon: Search, label: "Search", id: "search" },
  { icon: Users, label: "Creators", id: "creators" },
  { icon: BarChart3, label: "Analytics", id: "analytics" },
  { icon: Zap, label: "Campaigns", id: "campaigns" },
  { icon: Download, label: "Export", id: "export" },
  { icon: Terminal, label: "Console", id: "console" },
];

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <motion.aside
      animate={{ width: collapsed ? 72 : 240 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
      className="flex h-screen flex-col border-r border-border bg-card"
    >
      <div className="flex items-center gap-3 border-b border-border px-4 py-5">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary">
          <ScanLine className="h-4 w-4 text-primary-foreground" />
        </div>
        {!collapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <h1 className="text-sm font-semibold tracking-tight text-foreground">
              CreatorScope
            </h1>
            <p className="text-[10px] font-medium uppercase tracking-widest text-primary">
              AI
            </p>
          </motion.div>
        )}
      </div>

      <nav className="flex flex-1 flex-col gap-1 px-3 py-4">
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active"
                  className="absolute inset-0 rounded-lg bg-primary/10"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              <item.icon className="relative z-10 h-4 w-4 shrink-0" />
              {!collapsed && (
                <span className="relative z-10">{item.label}</span>
              )}
            </button>
          );
        })}
      </nav>

      <div className="border-t border-border px-3 py-3">
        <button
          onClick={() => onTabChange("settings")}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
        >
          <Settings className="h-4 w-4 shrink-0" />
          {!collapsed && <span>Settings</span>}
        </button>
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="mt-1 flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4 shrink-0" />
          ) : (
            <>
              <ChevronLeft className="h-4 w-4 shrink-0" />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>
    </motion.aside>
  );
}
