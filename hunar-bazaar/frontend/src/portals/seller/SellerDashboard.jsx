import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";

export default function SellerDashboard() {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/seller/products").then(({ data }) => setProducts(data));
    api.get("/seller/orders").then(({ data }) => setOrders(data));
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl">Seller dashboard</h1>
        <Link to="/seller/products/new" className="bg-brass text-ink px-4 py-2 rounded hover:bg-brass-light">
          + New product
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section>
          <h2 className="text-lg mb-3">Your catalog ({products.length})</h2>
          <div className="space-y-2">
            {products.map((p) => (
              <div key={p.id} className="border border-ink/10 rounded p-3 bg-white flex justify-between">
                <span>{p.title}</span>
                <span>₹{p.price} · stock {p.stock}</span>
              </div>
            ))}
          </div>
        </section>
        <section>
          <h2 className="text-lg mb-3">Incoming orders ({orders.length})</h2>
          <div className="space-y-2">
            {orders.map((o) => (
              <div key={o._id} className="border border-ink/10 rounded p-3 bg-white">
                Order #{o._id.slice(-6)} · {o.status}
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
