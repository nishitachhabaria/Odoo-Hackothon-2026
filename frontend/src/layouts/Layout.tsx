import { motion } from "framer-motion";
import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/layout/Sidebar";
import { Topbar } from "../components/layout/Topbar";
import { Footer } from "../components/layout/Footer";

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="flex-1 flex flex-col bg-slate-50">
          <Topbar />
          <motion.main
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex-1 px-4 py-6 sm:px-6 lg:px-8"
          >
            <Outlet />
          </motion.main>
          <Footer />
        </div>
      </div>
    </div>
  );
}
