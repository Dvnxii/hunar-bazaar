import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { api } from "../../api/client";
import { useAuth } from "../../context/AuthContext.jsx";

const PORTAL_HOME = { buyer: "/shop", seller: "/seller", delivery_agent: "/delivery", admin: "/admin" };

export default function VerifyOtp() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/otp/verify", { email: state?.email, code });
      await refreshUser();
      navigate(PORTAL_HOME[data.user.role] ?? "/");
    } catch {
      setError("Invalid or expired code");
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-16 px-6 text-center">
      <h1 className="text-2xl mb-2">Verify your email</h1>
      <p className="text-sm text-ink/70 mb-6">Enter the code sent to {state?.email ?? "your email"}.</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          required maxLength={6} placeholder="6-digit code"
          className="w-full border border-ink/20 rounded px-3 py-2 text-center tracking-[0.5em]"
          value={code} onChange={(e) => setCode(e.target.value)}
        />
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button type="submit" className="w-full bg-indigo text-cream rounded py-2 hover:bg-indigo-light">
          Verify
        </button>
      </form>
    </div>
  );
}
