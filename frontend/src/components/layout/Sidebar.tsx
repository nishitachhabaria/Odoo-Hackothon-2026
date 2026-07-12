import { Link, useLocation } from "react-router-dom";
import { Bell, BookOpen, CheckSquare, ClipboardList, Home, Layers, MapPin, Shield, ShieldCheck, SlidersHorizontal, User, Users, Wallet } from "lucide-react";

const navItems = [
  { label: "Dashboard", path: "/dashboard", icon: Home },
  { label: "Organization", path: "/organization", icon: Users },
  { label: "Departments", path: "/organization/departments", icon: User, nested: true },
  { label: "Employees", path: "/organization/employees", icon: Users, nested: true },
  { label: "Asset Categories", path: "/organization/asset-categories", icon: Layers, nested: true },
  { label: "Assets", path: "/assets", icon: Wallet },
  { label: "Asset Allocation", path: "/allocations", icon: ClipboardList },
  { label: "Transfers", path: "/transfers", icon: MapPin },
  { label: "Bookings", path: "/bookings", icon: BookOpen },
  { label: "Maintenance", path: "/maintenance", icon: CheckSquare },
  { label: "Audits", path: "/audits", icon: ShieldCheck },
  { label: "Reports", path: "/reports", icon: BarChart },
  { label: "Notifications", path: "/notifications", icon: Bell },
  { label: "Settings", path: "/settings", icon: SlidersHorizontal },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="hidden w-72 shrink-0 overflow-y-auto border-r border-slate-200 bg-white px-4 py-6 lg:block">
      <div className="mb-8 px-4">
        <div className="mb-4 inline-flex items-center gap-2 text-2xl font-semibold text-slate-900">
          <div className="h-10 w-10 rounded-2xl bg-blue-600 text-white grid place-items-center">A</div>
          AssetFlow
        </div>
        <p className="text-sm text-slate-500">ERP workspace for asset and resource management.</p>
      </div>
      <nav className="space-y-1 px-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`group flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition-default ${
                isActive ? "bg-blue-600 text-white shadow-soft" : "text-slate-700 hover:bg-slate-100"
              } ${item.nested ? "ml-6" : ""}`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
