import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export const queryKeys = {
  accounts: ["accounts"] as const,
  account: (id: string) => ["accounts", id] as const,
  videos: ["videos"] as const,
  video: (id: string) => ["videos", id] as const,
  cookies: ["cookies"] as const,
  monitorStatus: ["monitor", "status"] as const,
  authCheck: ["auth", "check"] as const,
};

export function useAccounts(search?: string, showDisabled?: boolean) {
  return useQuery({
    queryKey: [...queryKeys.accounts, search, showDisabled],
    queryFn: () => api.accounts.list(search, showDisabled),
  });
}

export function useVideos(params?: { account_id?: string; status?: string; search?: string; page?: number }) {
  return useQuery({
    queryKey: [...queryKeys.videos, params],
    queryFn: () => api.videos.list(params),
  });
}

export function useCookies() {
  return useQuery({
    queryKey: queryKeys.cookies,
    queryFn: () => api.cookies.list(),
  });
}

export function useMonitorStatus() {
  return useQuery({
    queryKey: queryKeys.monitorStatus,
    queryFn: () => api.monitor.status(),
    refetchInterval: 10_000,
  });
}

export function useAuthCheck() {
  return useQuery({
    queryKey: queryKeys.authCheck,
    queryFn: () => api.auth.check(),
    retry: false,
  });
}
