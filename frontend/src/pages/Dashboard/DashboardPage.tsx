import DashboardCards from "./DashboardCards";
import MonitorPanel from "./MonitorPanel";
import ActivityFeed from "./ActivityFeed";

export default function DashboardPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <DashboardCards />
      <MonitorPanel />
      <ActivityFeed />
    </div>
  );
}
