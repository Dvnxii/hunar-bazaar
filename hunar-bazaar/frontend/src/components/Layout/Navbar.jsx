import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../../context/AuthContext.jsx";
import LanguageSwitcher from "../LanguageSwitcher.jsx";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();

  const portalHome = { buyer: "/shop", seller: "/seller", delivery_agent: "/delivery", admin: "/admin" };

  return (
    <header className="bg-indigo text-cream sticky top-0 z-10">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <Link to={user ? portalHome[user.role] : "/"} className="font-display text-xl tracking-wide">
          Hunar Bazaar
        </Link>
        <nav className="flex items-center gap-5 text-sm">
          {user?.role === "buyer" && (
            <>
              <Link to="/shop">{t("nav.shop")}</Link>
              <Link to="/orders">{t("nav.orders")}</Link>
            </>
          )}
          {user && user.role !== "buyer" && <Link to={portalHome[user.role]}>{t("nav.dashboard")}</Link>}
          <LanguageSwitcher />
          {user ? (
            <button
              onClick={async () => { await logout(); navigate("/login"); }}
              className="text-brass-light hover:text-brass"
            >
              {t("nav.logout")}
            </button>
          ) : (
            <Link to="/login" className="text-brass-light hover:text-brass">{t("auth.login")}</Link>
          )}
        </nav>
      </div>
    </header>
  );
}
