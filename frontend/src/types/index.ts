export interface AppConfig {
  theme: "light" | "dark";
  monitorInterval: number;
  maxConcurrentDownloads: number;
}

export interface MonitoredAccount {
  id: string;
  tiktok_username: string;
  enabled: boolean;
  last_check_at?: string;
  last_video_timestamp?: number;
  status: "ok" | "needs_review" | "paused";
  options?: Record<string, unknown>;
  avatar_url?: string;
  follower_count?: number;
  following_count?: number;
  total_likes?: number;
  video_count?: number;
  profile_last_refreshed?: string;
}

export interface Video {
  id: string;
  monitored_account_id: string;
  tiktok_id: string;
  title: string;
  description?: string;
  upload_date?: string;
  upload_timestamp?: number;
  duration?: number;
  thumbnail_path?: string;
  file_path?: string;
  file_size?: number;
  metadata?: Record<string, unknown>;
  likes?: number;
  views?: number;
  downloaded_at?: string;
  status: "queued" | "downloading" | "downloaded" | "failed";
  error_text?: string;
  retry_count?: number;
}

export type ActivityEvent =
  | { type: "monitor.cycle_started"; payload: { iteration: number; accounts: string[] } }
  | { type: "monitor.account_check_started"; payload: { username: string } }
  | { type: "monitor.new_videos_found"; payload: { count: number; accountId?: string } }
  | { type: "monitor.video_downloaded"; payload: { title: string; videoId: string } }
  | { type: "monitor.account_paused"; payload: { username: string; reason: string } }
  | { type: "monitor.cookie_expired"; payload: { accountId: string } }
  | { type: "monitor.yt_dlp_update_available"; payload: { currentVersion: string; latestVersion: string } }
  | { type: "monitor.error"; payload: { message: string } };

export interface CookieData {
  id: string;
  name: string;
  account_id?: string;
  original_format: string;
  status: string;
  last_validated_at?: string;
  created_at: string;
}

export interface AccountResponse {
  accounts: MonitoredAccount[];
  total: number;
}

export interface VideoResponse {
  videos: Video[];
  total: number;
  page: number;
  page_size: number;
}

export interface CookieResponse {
  cookies: CookieData[];
}

export interface MonitorStatus {
  running: boolean;
  interval_minutes: number;
  next_run?: string;
  last_run?: string;
  active_accounts: number;
  total_accounts: number;
  concurrent_downloads: number;
  max_concurrent: number;
}
