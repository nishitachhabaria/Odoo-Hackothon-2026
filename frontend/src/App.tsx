import { AnimatePresence } from "framer-motion";
import { Route, Routes, useLocation } from "react-router-dom";
import { DashboardPage } from "./pages/dashboard/DashboardPage";
import { LoginPage } from "./pages/auth/LoginPage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { OrganizationPage } from "./pages/organization/OrganizationPage";
import { DepartmentsPage } from "./pages/organization/DepartmentsPage";
import { EmployeesPage } from "./pages/organization/EmployeesPage";
import { AssetCategoriesPage } from "./pages/organization/AssetCategoriesPage";
import { AssetsPage } from "./pages/assets/AssetsPage";
import { AllocationsPage } from "./pages/allocation/AllocationsPage";
import { TransfersPage } from "./pages/transfers/TransfersPage";
import { BookingsPage } from "./pages/bookings/BookingsPage";
import { MaintenancePage } from "./pages/maintenance/MaintenancePage";
import { AuditsPage } from "./pages/audit/AuditsPage";
import { ReportsPage } from "./pages/reports/ReportsPage";
import { NotificationsPage } from "./pages/notifications/NotificationsPage";
import { SettingsPage } from "./pages/settings/SettingsPage";
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
          <Route path="organization" element={<OrganizationPage />} />
          <Route path="organization/departments" element={<DepartmentsPage />} />
          <Route path="organization/employees" element={<EmployeesPage />} />
          <Route path="organization/asset-categories" element={<AssetCategoriesPage />} />
          <Route path="assets" element={<AssetsPage />} />
          <Route path="allocations" element={<AllocationsPage />} />
          <Route path="transfers" element={<TransfersPage />} />
          <Route path="bookings" element={<BookingsPage />} />
          <Route path="maintenance" element={<MaintenancePage />} />
          <Route path="audits" element={<AuditsPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="notifications" element={<NotificationsPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default App;
