import { useRef, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useCookies } from "../../services/queries";
import { api } from "../../services/api";
import type { CookieData } from "../../types";
import Badge from "../../components/Badge";

export default function CookiesManager() {
  const { data, isLoading } = useCookies();
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();

  const uploadMut = useMutation({
    mutationFn: (file: File) => api.cookies.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cookies"] });
    },
  });

  const testMut = useMutation({
    mutationFn: (id: string) => api.cookies.test(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["cookies"] }),
  });

  const deleteMut = useMutation({
    mutationFn: (id: string) => api.cookies.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["cookies"] }),
  });

  const handleFile = (file: File) => {
    if (file.name.endsWith(".txt") || file.name.endsWith(".json")) {
      uploadMut.mutate(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const statusBadge = (status: string) => {
    const map: Record<string, "success" | "warning" | "danger" | "default"> = {
      valid: "success",
      expired: "warning",
      invalid: "danger",
      unverified: "default",
    };
    return <Badge variant={map[status] || "default"}>{status}</Badge>;
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-1">Cookies Manager</h3>
      <p className="text-sm text-gray-500 mb-4">
        Export cookies from TikTok using the &quot;Get cookies.txt LOCALLY&quot; browser extension. Supports both TXT and JSON formats.
      </p>

      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors mb-4 ${
          dragOver ? "border-accent-500 bg-accent-500/5" : "border-gray-700 hover:border-gray-600"
        }`}
      >
        <input
          ref={fileRef}
          type="file"
          accept=".txt,.json"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
          }}
        />
        <p className="text-gray-400 text-sm">
          Drop <code className="text-accent-400">cookies.txt</code> or <code className="text-accent-400">cookies.json</code> here, or click to browse
        </p>
        {uploadMut.isPending && <p className="text-accent-400 text-sm mt-2">Uploading...</p>}
        {uploadMut.isError && <p className="text-red-400 text-sm mt-2">Error: {(uploadMut.error as Error).message}</p>}
      </div>

      {isLoading && <p className="text-gray-500 text-sm">Loading...</p>}

      <div className="space-y-2">
        {data?.cookies.map((cookie: CookieData) => (
          <div key={cookie.id} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3">
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-200">{cookie.name}</span>
              {statusBadge(cookie.status)}
              <span className="text-xs text-gray-600">{cookie.original_format.toUpperCase()}</span>
            </div>
            <div className="flex gap-1">
              <button
                onClick={() => testMut.mutate(cookie.id)}
                className="px-2 py-1 text-xs rounded bg-gray-700 text-gray-400 hover:text-gray-200"
              >
                Test
              </button>
              <button
                onClick={() => { if (confirm("Delete cookie?")) deleteMut.mutate(cookie.id); }}
                className="px-2 py-1 text-xs rounded bg-red-600/20 text-red-400 hover:bg-red-600/30"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
        {data?.cookies.length === 0 && (
          <p className="text-sm text-gray-600 text-center py-4">No cookies uploaded yet</p>
        )}
      </div>
    </div>
  );
}
