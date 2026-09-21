import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../../context/AuthContext.jsx";

const PORTAL_HOME = { buyer: "/shop", seller: "/seller", delivery_agent: "/delivery", admin: "/admin" };

export default function Login() {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const user = await login(form.email, form.password);
      navigate(PORTAL_HOME[user.role] ?? "/");
    } catch (err) {
      setError(err.response?.data?.detail ?? "Login failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 px-6">
      <h1 className="text-2xl mb-6">{t("auth.login")}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email" required placeholder={t("auth.email")}
          className="w-full border border-ink/20 rounded px-3 py-2"
          value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password" required placeholder={t("auth.password")}
          className="w-full border border-ink/20 rounded px-3 py-2"
          value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button type="submit" className="w-full bg-indigo text-cream rounded py-2 hover:bg-indigo-light">
          {t("auth.login")}
        </button>
      </form>
      <a href="/api/auth/oauth/google/login" className="block text-center mt-4 text-sm text-indigo underline">
        Continue with Google
      </a>
      <p className="text-sm mt-6">
        New here? <Link to="/register" className="text-brass underline">{t("auth.register")}</Link>
      </p>
    </div>
  );
}
