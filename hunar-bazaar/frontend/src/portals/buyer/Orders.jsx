import { useEffect, useState } from "react";
import { api } from "../../api/client";

const STATUS_LABEL = {
  placed: "Placed", confirmed: "Confirmed", assigned: "Assigned",
  out_for_delivery: "Out for delivery", delivered: "Delivered", cancelled: "Cancelled",
};

export default function Orders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/buyer/orders").then(({ data }) => setOrders(data));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <h1 className="text-2xl mb-6">Your orders</h1>
      {orders.length === 0 ? (
        <p className="text-ink/60">No orders yet.</p>
      ) : (
        <div className="space-y-3">
          {orders.map((o) => (
            <div key={o.id} className="border border-ink/10 rounded-lg p-4 bg-white flex justify-between">
              <div>
                <p className="text-sm text-ink/50">Order #{o.id.slice(-6)}</p>
                <p>{o.items.length} item(s) · ₹{o.total_amount}</p>
              </div>
              <span className="text-sm bg-indigo/10 text-indigo px-3 py-1 rounded-full h-fit">
                {STATUS_LABEL[o.status] ?? o.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
