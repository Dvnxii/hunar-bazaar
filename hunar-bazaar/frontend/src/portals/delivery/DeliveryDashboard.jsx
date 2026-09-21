import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";

export default function DeliveryDashboard() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/delivery/orders").then(({ data }) => setOrders(data));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <h1 className="text-2xl mb-6">Assigned deliveries</h1>
      {orders.length === 0 ? (
        <p className="text-ink/60">Nothing assigned to you right now.</p>
      ) : (
        <div className="space-y-3">
          {orders.map((o) => (
            <div key={o._id} className="border border-ink/10 rounded-lg p-4 bg-white flex justify-between items-center">
              <div>
                <p className="text-sm text-ink/50">Order #{o._id.slice(-6)}</p>
                <p>{o.status}</p>
              </div>
              <Link to={`/delivery/qr/${o._id}`} className="bg-indigo text-cream px-3 py-1.5 rounded text-sm">
                Generate handoff QR
              </Link>
            </div>
          ))}
        </div>
      )}
      <Link to="/delivery/scan" className="inline-block mt-8 text-brass underline">
        Scan a QR to confirm delivery →
      </Link>
    </div>
  );
}
