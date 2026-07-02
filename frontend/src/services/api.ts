import type {
  AccountResponse,
  CookieResponse,
  MonitorStatus,
  VideoResponse,
} from "../types";

const BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const resp = await fetch(`${BASE}${url}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (resp.status === 204) return undefined as T;
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return resp.json();
}

export const api = {
  auth: {
    check: () => request<{ authenticated: boolean }>("/auth/check"),
    login: (password: string) =>
      request<{ authenticated: boolean }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ password }),
      }),
    setup: (password: string) =>
      request<{ authenticated: boolean }>("/auth/setup", {
        method: "POST",
        body: JSON.stringify({ password }),
      }),
    logout: () => request<void>("/auth/logout", { method: "POST" }),
  },

  accounts: {
    list: (search?: string, showDisabled?: boolean) => {
      const params = new URLSearchParams();
      if (search) params.set("search", search);
      if (showDisabled) params.set("show_disabled", "true");
      return request<AccountResponse>(`/accounts?${params}`);
    },
    create: (data: { tiktok_username: string; enabled?: boolean; cookie_id?: string }) =>
      request("/accounts", { method: "POST", body: JSON.stringify(data) }),
    get: (id: string) => request(`/accounts/${id}`),
    update: (id: string, data: Record<string, unknown>) =>
      request(`/accounts/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
    delete: (id: string) => request<void>(`/accounts/${id}`, { method: "DELETE" }),
  },

  videos: {
    list: (params?: { account_id?: string; status?: string; search?: string; page?: number }) => {
      const sp = new URLSearchParams();
      if (params?.account_id) sp.set("account_id", params.account_id);
      if (params?.status) sp.set("status", params.status);
      if (params?.search) sp.set("search", params.search);
      if (params?.page) sp.set("page", String(params.page));
      return request<VideoResponse>(`/videos?${sp}`);
    },
    get: (id: string) => request(`/videos/${id}`),
    getFileUrl: (id: string) => `${BASE}/videos/${id}/file`,
    retry: (id: string) => request(`/videos/${id}/retry`, { method: "POST" }),
    delete: (id: string) => request<void>(`/videos/${id}`, { method: "DELETE" }),
    bulk: (video_ids: string[], action: string) =>
      request(`/videos/bulk`, { method: "POST", body: JSON.stringify({ video_ids, action }) }),
  },

  cookies: {
    list: () => request<CookieResponse>("/cookies"),
    upload: (file: File, accountId?: string) => {
      const form = new FormData();
      form.append("file", file);
      if (accountId) form.append("account_id", accountId);
      return fetch(`${BASE}/cookies`, {
        method: "POST",
        credentials: "include",
        body: form,
      }).then((r) => {
        if (!r.ok) throw new Error("Upload failed");
        return r.json();
      });
    },
    test: (id: string) => request(`/cookies/${id}/test`, { method: "POST" }),
    delete: (id: string) => request<void>(`/cookies/${id}`, { method: "DELETE" }),
  },

  monitor: {
    status: () => request<MonitorStatus>("/monitor/status"),
    start: () => request("/monitor/start", { method: "POST" }),
    stop: () => request("/monitor/stop", { method: "POST" }),
    checkAll: () => request("/monitor/check-all", { method: "POST" }),
    checkAccount: (id: string) => request(`/monitor/accounts/${id}/check`, { method: "POST" }),
  },
};
