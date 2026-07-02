import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../services/api";
import { useMonitorStatus } from "../../services/queries";

export default function MonitorPanel() {
  const { data: status } = useMonitorStatus();
  const queryClient = useQueryClient();

  const startMut = useMutation({ mutationFn: () => api.monitor.start(), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["monitor"] }) });
  const stopMut = useMutation({ mutationFn: () => api.monitor.stop(), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["monitor"] }) });
  const checkAllMut = useMutation({ mutationFn: () => api.monitor.checkAll() });

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
      <h2 className="text-lg font-semibold mb-4">Monitor</h2>
      <div className="flex flex-wrap gap-3 mb-4">
        <button
          onClick={() => status?.running ? stopMut.mutate() : startMut.mutate()}
          className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
            status?.running
              ? "bg-red-600/20 text-red-400 hover:bg-red-600/30"
              : "bg-accent-600/20 text-accent-400 hover:bg-accent-600/30"
          }`}
        >
          {status?.running ? "Stop" : "Start"}
        </button>
        <button
          onClick={() => checkAllMut.mutate()}
          className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 font-medium text-sm transition-colors"
        >
          Check Now
        </button>
      </div>
      {status && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div><span className="text-gray-500">Interval:</span> <span className="text-gray-300">{status.interval_minutes}min</span></div>
          <div><span className="text-gray-500">Accounts:</span> <span className="text-gray-300">{status.active_accounts}/{status.total_accounts}</span></div>
          <div><span className="text-gray-500">Concurrent:</span> <span className="text-gray-300">{status.concurrent_downloads}/{status.max_concurrent}</span></div>
          <div><span className="text-gray-500">Running:</span> <span className={status.running ? "text-emerald-400" : "text-red-400"}>{status.running ? "Yes" : "No"}</span></div>
        </div>
      )}
    </div>
  );
}
