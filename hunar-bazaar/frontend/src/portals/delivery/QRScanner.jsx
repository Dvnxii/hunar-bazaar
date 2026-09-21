// "Scanner" here is a manual hex-paste stand-in for a camera-based QR
// reader (e.g. an html5-qrcode integration) - the decrypt/verify flow
// against the backend is the real logic this page demonstrates.
import { useState } from "react";
import { useParams } from "react-router-dom";
import { QRCodeSVG } from "qrcode.react";
import { api } from "../../api/client";

export function GenerateQR() {
  const { orderId } = useParams();
  const [ciphertext, setCiphertext] = useState(null);
  const [error, setError] = useState("");

  const generate = async () => {
    setError("");
    try {
      const { data } = await api.post(`/delivery/orders/${orderId}/generate-qr`);
      setCiphertext(data.ciphertext_hex);
    } catch (err) {
      setError(err.response?.data?.detail ?? "Could not generate QR");
    }
  };

  return (
    <div className="max-w-md mx-auto px-6 py-8 text-center">
      <h1 className="text-2xl mb-6">Handoff QR — order #{orderId.slice(-6)}</h1>
      {!ciphertext ? (
        <button onClick={generate} className="bg-indigo text-cream px-4 py-2 rounded">
          Generate encrypted QR
        </button>
      ) : (
        <div className="inline-block bg-white p-4 rounded-lg border border-ink/10">
          <QRCodeSVG value={ciphertext} size={220} />
          <p className="text-xs text-ink/40 mt-3 break-all">AES-128-CBC payload · {ciphertext.slice(0, 24)}…</p>
        </div>
      )}
      {error && <p className="text-red-600 text-sm mt-3">{error}</p>}
    </div>
  );
}

export function ScanQR() {
  const [hex, setHex] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const scan = async (e) => {
    e.preventDefault();
    setError(""); setResult(null);
    try {
      const { data } = await api.post("/delivery/orders/scan", { ciphertext_hex: hex });
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail ?? "Could not verify QR");
    }
  };

  return (
    <div className="max-w-md mx-auto px-6 py-8">
      <h1 className="text-2xl mb-6">Confirm delivery</h1>
      <form onSubmit={scan} className="space-y-4">
        <textarea
          required placeholder="Paste scanned QR payload (hex)"
          className="w-full border border-ink/20 rounded px-3 py-2 h-28 text-sm"
          value={hex} onChange={(e) => setHex(e.target.value)}
        />
        <button type="submit" className="w-full bg-indigo text-cream rounded py-2">Verify & mark delivered</button>
      </form>
      {result && <p className="text-green-700 text-sm mt-4">Order {result.order_id.slice(-6)} marked delivered ✓</p>}
      {error && <p className="text-red-600 text-sm mt-4">{error}</p>}
    </div>
  );
}
