import { Bell, ChevronDown, Search } from "lucide-react";

export function Topbar() {
  return (
    <header className="border-b border-slate-200 bg-white px-4 py-4 shadow-sm sm:px-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-1 items-center gap-3">
          <button className="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-slate-600 transition-default hover:bg-slate-200">
            <Search className="h-5 w-5" />
          </button>
          <div className="min-w-0 flex-1 overflow-hidden rounded-2xl bg-slate-100 px-4 py-3 text-slate-500">
            Search for assets, departments or bookings...
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-slate-600 transition-default hover:bg-slate-200">
            <Bell className="h-5 w-5" />
          </button>
          <button className="inline-flex items-center gap-2 rounded-2xl bg-slate-100 px-4 py-3 text-sm text-slate-700 transition-default hover:bg-slate-200">
            <span className="h-8 w-8 rounded-full bg-blue-600 text-white grid place-items-center">D</span>
            <span>Dev User</span>
            <ChevronDown className="h-4 w-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
