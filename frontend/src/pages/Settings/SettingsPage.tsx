import MonitorSettingsForm from "./MonitorSettingsForm";
import CookiesManager from "./CookiesManager";
import NotificationsSettings from "./NotificationsSettings";

export default function SettingsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <div className="space-y-6">
        <MonitorSettingsForm />
        <CookiesManager />
        <NotificationsSettings />
      </div>
    </div>
  );
}
