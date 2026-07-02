import { useState } from "react";
import { useVideos } from "../../services/queries";
import type { Video } from "../../types";
import VideoCard from "./VideoCard";
import VideoModal from "./VideoModal";

export default function VideoGrid() {
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState("");
  const [selected, setSelected] = useState<Video | null>(null);
  const [bulkMode, setBulkMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  const { data, isLoading } = useVideos({ status: statusFilter || undefined, page });

  const toggleSelect = (video: Video) => {
    if (bulkMode) {
      setSelectedIds((prev) => {
        const next = new Set(prev);
        if (next.has(video.id)) next.delete(video.id);
        else next.add(video.id);
        return next;
      });
    } else {
      setSelected(video);
    }
  };

  const files: string[] = [];

  return (
    <div>
      <div className="flex flex-wrap gap-3 items-center mb-4">
        <select
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
          className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-accent-500"
        >
          <option value="">All status</option>
          <option value="downloaded">Downloaded</option>
          <option value="queued">Queued</option>
          <option value="failed">Failed</option>
        </select>
        <button
          onClick={() => { setBulkMode(!bulkMode); setSelectedIds(new Set()); }}
          className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
            bulkMode ? "bg-accent-600/20 text-accent-400" : "bg-gray-800 text-gray-400 hover:text-gray-200"
          }`}
        >
          {bulkMode ? "Cancel Bulk" : "Bulk Select"}
        </button>
      </div>

      {isLoading && <p className="text-center text-gray-500 py-12">Loading...</p>}

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {data?.videos.map((v) => (
          <VideoCard
            key={v.id}
            video={v}
            onSelect={toggleSelect}
            selected={bulkMode ? selectedIds.has(v.id) : false}
          />
        ))}
      </div>

      {data && data.total === 0 && (
        <p className="text-center text-gray-500 py-12">No videos found</p>
      )}

      {data && data.total > 0 && (
        <div className="flex items-center justify-center gap-4 mt-6">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-3 py-1.5 text-sm bg-gray-800 text-gray-400 hover:text-gray-200 rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-400">Page {page}</span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={page * 20 >= data.total}
            className="px-3 py-1.5 text-sm bg-gray-800 text-gray-400 hover:text-gray-200 rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}

      {selected && !bulkMode && (
        <VideoModal video={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
