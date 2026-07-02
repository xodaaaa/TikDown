import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../services/api";

interface Props {
  onAuthenticated: () => void;
  needsSetup: boolean;
}

export default function LoginPage({ onAuthenticated, needsSetup }: Props) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const queryClient = useQueryClient();

  const loginMutation = useMutation({
    mutationFn: (pw: string) => api.auth.login(pw),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth"] });
      onAuthenticated();
    },
    onError: (e: Error) => setError(e.message),
  });

  const setupMutation = useMutation({
    mutationFn: (pw: string) => api.auth.setup(pw),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth"] });
      onAuthenticated();
    },
    onError: (e: Error) => setError(e.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (needsSetup) {
      setupMutation.mutate(password);
    } else {
      loginMutation.mutate(password);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950">
      <div className="w-full max-w-sm p-8 bg-gray-900 rounded-xl border border-gray-800">
        <h1 className="text-2xl font-bold text-center text-accent-500 mb-2">TikDown</h1>
        <p className="text-gray-400 text-center text-sm mb-6">
          {needsSetup ? "Set your admin password" : "Enter your password to continue"}
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-accent-500"
            autoFocus
          />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={!password || loginMutation.isPending || setupMutation.isPending}
            className="w-full py-2 bg-accent-600 hover:bg-accent-500 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
          >
            {needsSetup ? "Set Password" : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
