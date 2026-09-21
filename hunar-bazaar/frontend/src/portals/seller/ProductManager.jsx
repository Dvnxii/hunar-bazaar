import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../api/client";

export default function ProductManager() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ title: "", description: "", price: "", category: "", stock: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/seller/products", {
        ...form,
        price: parseFloat(form.price),
        stock: parseInt(form.stock, 10),
        images: [],
      });
      navigate("/seller");
    } catch (err) {
      setError(err.response?.data?.detail ?? "Could not create product");
    }
  };

  return (
    <div className="max-w-lg mx-auto px-6 py-8">
      <h1 className="text-2xl mb-6">List a new product</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {["title", "description", "category"].map((field) => (
          <input
            key={field} required placeholder={field} className="w-full border border-ink/20 rounded px-3 py-2"
            value={form[field]} onChange={(e) => setForm({ ...form, [field]: e.target.value })}
          />
        ))}
        <div className="flex gap-4">
          <input
            type="number" required placeholder="Price (₹)" className="w-full border border-ink/20 rounded px-3 py-2"
            value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })}
          />
          <input
            type="number" required placeholder="Stock" className="w-full border border-ink/20 rounded px-3 py-2"
            value={form.stock} onChange={(e) => setForm({ ...form, stock: e.target.value })}
          />
        </div>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button type="submit" className="w-full bg-indigo text-cream rounded py-2 hover:bg-indigo-light">
          Publish listing
        </button>
      </form>
    </div>
  );
}
