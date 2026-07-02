import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../../services/api";

interface Props {
  onClose: () => void;
}

export default function AddUserModal({ onClose }: Props) {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const queryClient = useQueryClient();

  const createMut = useMutation({
    mutationFn: () => api.accounts.create({ tiktok_username: username }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["accounts"] });
      onClose();
    },
    onError: (e: Error) => setError(e.message),
  });

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 w-full max-w-sm" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-lg font-semibold mb-4">Add TikTok Account</h2>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value.replace("@", ""))}
          placeholder="@username"
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:border-accent-500 mb-4"
          autoFocus
        />
        {error && <p className="text-red-400 text-sm mb-2">{error}</p>}
        <div className="flex gap-2 justify-end">
          <button onClick={onClose} className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200">Cancel</button>
          <button
            onClick={() => createMut.mutate()}
            disabled={!username || createMut.isPending}
            className="px-4 py-2 text-sm bg-accent-600 hover:bg-accent-500 disabled:opacity-50 text-white rounded-lg"
          >
            Add
          </button>
        </div>
      </div>
    </div>
  );
}
