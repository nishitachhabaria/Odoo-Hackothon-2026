import { AnimatePresence, motion } from "framer-motion";
import { Route, Routes, useLocation } from "react-router-dom";
import { DashboardPage } from "./pages/dashboard/DashboardPage";
import { LoginPage } from "./pages/auth/LoginPage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { Layout } from "./layouts/Layout";

function App() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="organization/*" element={<div className="p-6 text-slate-700">Organization pages coming soon</div>} />
          <Route path="assets/*" element={<div className="p-6 text-slate-700">Assets pages coming soon</div>} />
          <Route path="allocations/*" element={<div className="p-6 text-slate-700">Allocations pages coming soon</div>} />
          <Route path="transfers/*" element={<div className="p-6 text-slate-700">Transfers pages coming soon</div>} />
          <Route path="bookings/*" element={<div className="p-6 text-slate-700">Bookings pages coming soon</div>} />
          <Route path="maintenance/*" element={<div className="p-6 text-slate-700">Maintenance pages coming soon</div>} />
          <Route path="audits/*" element={<div className="p-6 text-slate-700">Audits pages coming soon</div>} />
          <Route path="reports/*" element={<div className="p-6 text-slate-700">Reports pages coming soon</div>} />
          <Route path="notifications" element={<div className="p-6 text-slate-700">Notifications center coming soon</div>} />
          <Route path="settings" element={<div className="p-6 text-slate-700">Settings coming soon</div>} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default App;
