import { useState } from "react";
import { api } from "../../services/api";
import type { Video } from "../../types";
import Badge from "../../components/Badge";

interface Props {
  video: Video;
  onSelect: (video: Video) => void;
  selected: boolean;
}

export default function VideoCard({ video, onSelect, selected }: Props) {
  const statusMap: Record<string, "success" | "warning" | "danger" | "default"> = {
    downloaded: "success",
    downloading: "warning",
    queued: "default",
    failed: "danger",
  };

  return (
    <div
      onClick={() => onSelect(video)}
      className={`bg-gray-900 border rounded-xl overflow-hidden cursor-pointer transition-all ${
        selected ? "border-accent-500 ring-1 ring-accent-500" : "border-gray-800 hover:border-gray-700"
      }`}
    >
      <div className="aspect-[9/16] bg-gray-800 flex items-center justify-center relative">
        {video.thumbnail_path ? (
          <img src={video.thumbnail_path} alt={video.title} className="w-full h-full object-cover" />
        ) : (
          <span className="text-gray-600 text-4xl">🎬</span>
        )}
        <div className="absolute top-2 right-2">
          <Badge variant={statusMap[video.status] || "default"}>{video.status}</Badge>
        </div>
      </div>
      <div className="p-3">
        <div className="text-sm text-gray-200 truncate">{video.title || "Untitled"}</div>
        <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
          {video.likes !== undefined && <span>♥ {(video.likes || 0).toLocaleString()}</span>}
          {video.views !== undefined && <span>👁 {(video.views || 0).toLocaleString()}</span>}
        </div>
      </div>
    </div>
  );
}
