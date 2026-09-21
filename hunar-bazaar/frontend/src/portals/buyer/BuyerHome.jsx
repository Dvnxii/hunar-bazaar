import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "../../api/client";

export default function BuyerHome() {
  const { t } = useTranslation();
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState({}); // productId -> quantity

  useEffect(() => {
    api.get("/buyer/products").then(({ data }) => setProducts(data));
  }, []);

  const addToCart = (id) => setCart((c) => ({ ...c, [id]: (c[id] ?? 0) + 1 }));

  const placeOrder = async () => {
    const items = Object.entries(cart).map(([product_id, quantity]) => ({ product_id, quantity }));
    if (!items.length) return;
    await api.post("/buyer/orders", {
      items,
      shipping_address: { line1: "TODO: collect from a real address form" },
    });
    setCart({});
    alert("Order placed");
  };

  const cartCount = Object.values(cart).reduce((a, b) => a + b, 0);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl">Shop handcrafted pieces</h1>
        {cartCount > 0 && (
          <button onClick={placeOrder} className="bg-brass text-ink px-4 py-2 rounded hover:bg-brass-light">
            {t("buyer.placeOrder")} ({cartCount})
          </button>
        )}
      </div>

      {products.length === 0 ? (
        <p className="text-ink/60">
          No products yet — once a seller lists something on the Seller portal, it shows up here.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((p) => (
            <div key={p.id} className="border border-ink/10 rounded-lg p-4 bg-white">
              <div className="aspect-square bg-ink/5 rounded mb-3" />
              <h3 className="font-medium">{p.title}</h3>
              <p className="text-sm text-ink/60 line-clamp-2">{p.description}</p>
              <div className="flex items-center justify-between mt-3">
                <span className="font-display">₹{p.price}</span>
                <button
                  onClick={() => addToCart(p.id)}
                  className="text-sm bg-indigo text-cream px-3 py-1.5 rounded hover:bg-indigo-light"
                >
                  {t("buyer.addToCart")}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
