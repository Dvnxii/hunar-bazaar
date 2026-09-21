import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api } from "../../api/client";

export default function Register() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "buyer" });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/auth/register", form);
      navigate("/verify-otp", { state: { email: form.email } });
    } catch (err) {
      setError(err.response?.data?.detail ?? "Registration failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 px-6">
      <h1 className="text-2xl mb-6">{t("auth.register")}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          required placeholder="Full name" className="w-full border border-ink/20 rounded px-3 py-2"
          value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          type="email" required placeholder={t("auth.email")} className="w-full border border-ink/20 rounded px-3 py-2"
          value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password" required placeholder={t("auth.password")} className="w-full border border-ink/20 rounded px-3 py-2"
          value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <select
          className="w-full border border-ink/20 rounded px-3 py-2"
          value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}
        >
          <option value="buyer">Buyer</option>
          <option value="seller">Seller</option>
          <option value="delivery_agent">Delivery agent</option>
        </select>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button type="submit" className="w-full bg-indigo text-cream rounded py-2 hover:bg-indigo-light">
          {t("auth.register")}
        </button>
      </form>
      <p className="text-sm mt-6">
        Already have an account? <Link to="/login" className="text-brass underline">{t("auth.login")}</Link>
      </p>
    </div>
  );
}
