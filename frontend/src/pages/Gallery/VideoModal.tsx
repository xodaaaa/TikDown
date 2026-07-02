import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../services/api";
import type { Video } from "../../types";

interface Props {
  video: Video;
  onClose: () => void;
}

export default function VideoModal({ video, onClose }: Props) {
  const queryClient = useQueryClient();

  const retryMut = useMutation({
    mutationFn: () => api.videos.retry(video.id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["videos"] }),
  });
  const deleteMut = useMutation({
    mutationFn: () => api.videos.delete(video.id),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ["videos"] }); onClose(); },
  });

  const fileUrl = video.file_path ? api.videos.getFileUrl(video.id) : null;

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-900 border border-gray-800 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="p-6">
          {fileUrl && video.status === "downloaded" ? (
            <video controls className="w-full rounded-lg mb-4" src={fileUrl} />
          ) : (
            <div className="w-full aspect-video bg-gray-800 rounded-lg flex items-center justify-center mb-4">
              <span className="text-gray-600 text-4xl">🎬</span>
            </div>
          )}

          <h2 className="text-lg font-semibold mb-2">{video.title || "Untitled"}</h2>
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-400 mb-4">
            <div>Status: <span className="text-gray-200">{video.status}</span></div>
            <div>Likes: <span className="text-gray-200">{(video.likes || 0).toLocaleString()}</span></div>
            <div>Views: <span className="text-gray-200">{(video.views || 0).toLocaleString()}</span></div>
            <div>Retries: <span className="text-gray-200">{video.retry_count}</span></div>
          </div>
          {video.error_text && (
            <div className="bg-red-900/20 border border-red-900/50 rounded-lg p-3 text-sm text-red-400 mb-4">
              {video.error_text}
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => retryMut.mutate()}
              disabled={video.status === "downloaded" || retryMut.isPending}
              className="px-4 py-2 text-sm bg-accent-600/20 text-accent-400 hover:bg-accent-600/30 rounded-lg disabled:opacity-50"
            >
              Retry
            </button>
            {fileUrl && (
              <a
                href={fileUrl}
                download
                className="px-4 py-2 text-sm bg-gray-800 text-gray-300 hover:text-gray-100 rounded-lg inline-block"
              >
                Download
              </a>
            )}
            <button
              onClick={() => { if (confirm("Delete video?")) deleteMut.mutate(); }}
              className="px-4 py-2 text-sm bg-red-600/20 text-red-400 hover:bg-red-600/30 rounded-lg ml-auto"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
