import { create } from "zustand";

interface AppState {
  theme: "light" | "dark";
  toggleTheme: () => void;
  setTheme: (t: "light" | "dark") => void;
}

export const useAppStore = create<AppState>((set) => ({
  theme: (localStorage.getItem("tikdown-theme") as "light" | "dark") || "dark",
  toggleTheme: () =>
    set((state) => {
      const next = state.theme === "dark" ? "light" : "dark";
      localStorage.setItem("tikdown-theme", next);
      return { theme: next };
    }),
  setTheme: (t) => {
    localStorage.setItem("tikdown-theme", t);
    set({ theme: t });
  },
}));
