import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function UserManagement() {
  const [users, setUsers] = useState([]);

  const load = () => api.get("/admin/users").then(({ data }) => setUsers(data));
  useEffect(() => { load(); }, []);

  const deactivate = async (id) => {
    await api.patch(`/admin/users/${id}/deactivate`);
    load();
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <h1 className="text-2xl mb-6">Users</h1>
      <div className="space-y-2">
        {users.map((u) => (
          <div key={u._id} className="border border-ink/10 rounded p-3 bg-white flex justify-between items-center text-sm">
            <span>{u.name} · {u.email} · {u.role}</span>
            {u.is_active ? (
              <button onClick={() => deactivate(u._id)} className="text-red-600 underline">Deactivate</button>
            ) : (
              <span className="text-ink/40">Deactivated</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
