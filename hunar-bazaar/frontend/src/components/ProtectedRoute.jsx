// Route guard: redirects unauthenticated users to /login, and users whose
// role doesn't match to their own portal home - keeps buyer/seller/
// delivery/admin routes from leaking into each other in the router table.
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProtectedRoute({ allowedRoles }) {
  const { user, loading } = useAuth();

  if (loading) return <div className="p-8 text-center text-indigo">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }
  return <Outlet />;
}
