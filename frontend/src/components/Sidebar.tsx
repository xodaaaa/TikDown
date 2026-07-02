import { NavLink } from "react-router-dom";
import { useAppStore } from "../hooks/useAppStore";

const navItems = [
  { icon: "▦", label: "Dashboard", route: "/" },
  { icon: "👤", label: "Users", route: "/users" },
  { icon: "🎬", label: "Gallery", route: "/gallery" },
  { icon: "⚙", label: "Settings", route: "/settings" },
];

export default function Sidebar() {
  const { theme, toggleTheme } = useAppStore();

  return (
    <aside className="w-16 lg:w-56 h-screen fixed left-0 top-0 bg-gray-900 dark:bg-gray-950 border-r border-gray-800 flex flex-col z-40">
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-lg font-bold text-accent-500 hidden lg:block">TikDown</h1>
        <span className="text-accent-500 font-bold lg:hidden text-center block">TD</span>
      </div>

      <nav className="flex-1 py-4" role="navigation">
        {navItems.map((item) => (
          <NavLink
            key={item.route}
            to={item.route}
            end={item.route === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                isActive
                  ? "text-accent-400 bg-accent-500/10 border-l-2 border-accent-500"
                  : "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50 border-l-2 border-transparent"
              }`
            }
            aria-current="page"
          >
            <span className="text-lg">{item.icon}</span>
            <span className="hidden lg:block">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <button
          onClick={toggleTheme}
          className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-400 hover:text-gray-200 transition-colors rounded"
          title="Toggle dark mode"
        >
          <span className="text-lg">{theme === "dark" ? "☀" : "🌙"}</span>
          <span className="hidden lg:block">{theme === "dark" ? "Light" : "Dark"}</span>
        </button>
      </div>
    </aside>
  );
}
