import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAccounts } from "../../services/queries";
import { api } from "../../services/api";
import Badge from "../../components/Badge";
import type { MonitoredAccount } from "../../types";

export default function UsersTable() {
  const [search, setSearch] = useState("");
  const [showDisabled, setShowDisabled] = useState(false);
  const { data, isLoading } = useAccounts(search, showDisabled);
  const queryClient = useQueryClient();

  const deleteMut = useMutation({
    mutationFn: (id: string) => api.accounts.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["accounts"] }),
  });
  const toggleMut = useMutation({
    mutationFn: ({ id, enabled }: { id: string; enabled: boolean }) => api.accounts.update(id, { enabled }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["accounts"] }),
  });
  const checkMut = useMutation({
    mutationFn: (id: string) => api.monitor.checkAccount(id),
  });

  const statusBadge = (status: string) => {
    const map: Record<string, "success" | "warning" | "danger"> = {
      ok: "success",
      needs_review: "warning",
      paused: "danger",
    };
    return <Badge variant={map[status] || "default"}>{status}</Badge>;
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div className="flex flex-wrap gap-3 items-center mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search accounts..."
          className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-accent-500 w-48"
        />
        <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
          <input type="checkbox" checked={showDisabled} onChange={(e) => setShowDisabled(e.target.checked)} />
          Show disabled
        </label>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-gray-800">
              <th className="py-2 pr-4">Username</th>
              <th className="py-2 pr-4">Status</th>
              <th className="py-2 pr-4">Followers</th>
              <th className="py-2 pr-4">Videos</th>
              <th className="py-2 pr-4">Last Check</th>
              <th className="py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr><td colSpan={6} className="py-8 text-center text-gray-500">Loading...</td></tr>
            )}
            {data?.accounts.map((account: MonitoredAccount) => (
              <tr key={account.id} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                <td className="py-3 pr-4">
                  <div className="flex items-center gap-2">
                    {account.avatar_url ? (
                      <img src={account.avatar_url} alt="" className="w-6 h-6 rounded-full" />
                    ) : (
                      <div className="w-6 h-6 rounded-full bg-gray-700" />
                    )}
                    <span className="text-gray-200">@{account.tiktok_username}</span>
                  </div>
                </td>
                <td className="py-3 pr-4">{statusBadge(account.status)}</td>
                <td className="py-3 pr-4 text-gray-400">{(account.follower_count || 0).toLocaleString()}</td>
                <td className="py-3 pr-4 text-gray-400">{account.video_count || 0}</td>
                <td className="py-3 pr-4 text-gray-400">
                  {account.last_check_at ? new Date(account.last_check_at).toLocaleDateString() : "Never"}
                </td>
                <td className="py-3">
                  <div className="flex gap-1">
                    <button
                      onClick={() => toggleMut.mutate({ id: account.id, enabled: !account.enabled })}
                      className="px-2 py-1 text-xs rounded bg-gray-800 text-gray-400 hover:text-gray-200"
                    >
                      {account.enabled ? "Disable" : "Enable"}
                    </button>
                    <button
                      onClick={() => checkMut.mutate(account.id)}
                      className="px-2 py-1 text-xs rounded bg-accent-600/20 text-accent-400 hover:bg-accent-600/30"
                    >
                      Check
                    </button>
                    <button
                      onClick={() => { if (confirm("Delete account?")) deleteMut.mutate(account.id); }}
                      className="px-2 py-1 text-xs rounded bg-red-600/20 text-red-400 hover:bg-red-600/30"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {data?.accounts.length === 0 && (
              <tr><td colSpan={6} className="py-8 text-center text-gray-500">No accounts monitored yet</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
