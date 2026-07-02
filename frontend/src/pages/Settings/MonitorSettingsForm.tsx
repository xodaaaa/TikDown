import { useState } from "react";

export default function MonitorSettingsForm() {
  const [interval, setInterval] = useState("60");
  const [maxDownloads, setMaxDownloads] = useState("2");
  const [minDelay, setMinDelay] = useState("5");
  const [maxDelay, setMaxDelay] = useState("30");

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-4">Monitor Preferences</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Check Interval (minutes)</label>
          <input
            type="number"
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-accent-500"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Max Concurrent Downloads</label>
          <input
            type="number"
            value={maxDownloads}
            onChange={(e) => setMaxDownloads(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-accent-500"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Min Delay (seconds)</label>
          <input
            type="number"
            value={minDelay}
            onChange={(e) => setMinDelay(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-accent-500"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Max Delay (seconds)</label>
          <input
            type="number"
            value={maxDelay}
            onChange={(e) => setMaxDelay(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-accent-500"
          />
        </div>
      </div>
      <button className="mt-4 px-4 py-2 bg-accent-600 hover:bg-accent-500 text-white text-sm rounded-lg transition-colors">
        Save Settings
      </button>
    </div>
  );
}
