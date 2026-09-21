import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Layout/Navbar.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

import Login from "./portals/auth/Login.jsx";
import Register from "./portals/auth/Register.jsx";
import VerifyOtp from "./portals/auth/VerifyOtp.jsx";

import BuyerHome from "./portals/buyer/BuyerHome.jsx";
import Orders from "./portals/buyer/Orders.jsx";

import SellerDashboard from "./portals/seller/SellerDashboard.jsx";
import ProductManager from "./portals/seller/ProductManager.jsx";

import DeliveryDashboard from "./portals/delivery/DeliveryDashboard.jsx";
import { GenerateQR, ScanQR } from "./portals/delivery/QRScanner.jsx";

import AdminDashboard from "./portals/admin/AdminDashboard.jsx";
import UserManagement from "./portals/admin/UserManagement.jsx";

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/shop" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/verify-otp" element={<VerifyOtp />} />

        <Route element={<ProtectedRoute allowedRoles={["buyer"]} />}>
          <Route path="/shop" element={<BuyerHome />} />
          <Route path="/orders" element={<Orders />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["seller"]} />}>
          <Route path="/seller" element={<SellerDashboard />} />
          <Route path="/seller/products/new" element={<ProductManager />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["delivery_agent"]} />}>
          <Route path="/delivery" element={<DeliveryDashboard />} />
          <Route path="/delivery/qr/:orderId" element={<GenerateQR />} />
          <Route path="/delivery/scan" element={<ScanQR />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/users" element={<UserManagement />} />
        </Route>

        <Route path="*" element={<div className="p-8 text-center">Page not found</div>} />
      </Routes>
    </>
  );
}
