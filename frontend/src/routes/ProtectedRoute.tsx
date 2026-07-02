import { useState } from "react";
import { Outlet } from "react-router-dom";
import { useAuthCheck } from "../services/queries";
import LoginPage from "../pages/LoginPage";
import Sidebar from "../components/Sidebar";
import { useAppStore } from "../hooks/useAppStore";

export default function ProtectedRoute() {
  const { data, isLoading } = useAuthCheck();
  const [authenticated, setAuthenticated] = useState(false);
  const theme = useAppStore((s) => s.theme);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  const needsSetup = data?.needs_setup === true;
  const isAuth = authenticated || data?.authenticated === true;

  if (needsSetup || !isAuth) {
    return <LoginPage onAuthenticated={() => setAuthenticated(true)} needsSetup={needsSetup} />;
  }

  return (
    <div className={theme}>
      <div className="dark:bg-gray-950 bg-white min-h-screen">
        <Sidebar />
        <main className="ml-16 lg:ml-56 p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
