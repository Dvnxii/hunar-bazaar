import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/admin/users").then(({ data }) => setUsers(data));
    api.get("/admin/orders").then(({ data }) => setOrders(data));
  }, []);

  const roleCounts = users.reduce((acc, u) => ({ ...acc, [u.role]: (acc[u.role] ?? 0) + 1 }), {});

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <h1 className="text-2xl mb-6">Admin overview</h1>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        {Object.entries(roleCounts).map(([role, count]) => (
          <div key={role} className="border border-ink/10 rounded-lg p-4 bg-white text-center">
            <p className="text-2xl font-display">{count}</p>
            <p className="text-sm text-ink/60 capitalize">{role.replace("_", " ")}s</p>
          </div>
        ))}
      </div>

      <h2 className="text-lg mb-3">All orders ({orders.length})</h2>
      <div className="space-y-2">
        {orders.map((o) => (
          <div key={o._id} className="border border-ink/10 rounded p-3 bg-white flex justify-between text-sm">
            <span>#{o._id.slice(-6)}</span>
            <span>₹{o.total_amount}</span>
            <span>{o.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
