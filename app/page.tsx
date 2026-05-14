"use client";

import { useState } from "react";
import { ThemeProvider } from "@/components/theme-provider";
import { Sidebar } from "@/components/dashboard/sidebar";
import { Header } from "@/components/dashboard/header";
import { SearchPanel } from "@/components/dashboard/search-panel";
import { CreatorsPanel } from "@/components/dashboard/creators-panel";
import { StatsOverview } from "@/components/dashboard/stats-overview";
import { ExportPanel } from "@/components/dashboard/export-panel";
import { ProcessingConsole } from "@/components/dashboard/processing-console";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("search");

  const renderContent = () => {
    switch (activeTab) {
      case "search":
        return <SearchPanel />;
      case "creators":
        return <CreatorsPanel />;
      case "analytics":
        return <StatsOverview />;
      case "campaigns":
        return <div className="p-6 text-foreground">Campaign Readiness Analysis</div>;
      case "export":
        return <ExportPanel />;
      case "console":
        return <ProcessingConsole />;
      case "settings":
        return <div className="p-6 text-foreground">Settings Panel</div>;
      default:
        return <SearchPanel />;
    }
  };

  return (
    <div className="flex h-screen w-screen bg-background">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <div className="flex flex-1 flex-col">
        <Header activeTab={activeTab} />
        <main className="flex-1 overflow-auto bg-background">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
