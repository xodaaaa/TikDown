import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "./routes/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route element={<ProtectedRoute />}>
        <Route index lazy={() => import("./pages/Dashboard/DashboardPage").then((m) => ({ Component: m.default }))} />
        <Route path="users" lazy={() => import("./pages/Users/UsersPage").then((m) => ({ Component: m.default }))} />
        <Route path="gallery" lazy={() => import("./pages/Gallery/GalleryPage").then((m) => ({ Component: m.default }))} />
        <Route path="settings" lazy={() => import("./pages/Settings/SettingsPage").then((m) => ({ Component: m.default }))} />
      </Route>
    </Routes>
  );
}
