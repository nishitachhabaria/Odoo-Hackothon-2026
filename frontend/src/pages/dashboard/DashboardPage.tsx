import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, CartesianGrid } from "recharts";

const summaryCards = [
  { label: "Total Assets", value: "124", change: "+12%", color: "bg-blue-500" },
  { label: "Available", value: "76", change: "+8%", color: "bg-emerald-500" },
  { label: "Allocated", value: "32", change: "-4%", color: "bg-orange-500" },
  { label: "Maintenance", value: "16", change: "+5%", color: "bg-rose-500" },
];

const chartData = [
  { name: "Jan", assets: 20, bookings: 14, maintenance: 8 },
  { name: "Feb", assets: 32, bookings: 18, maintenance: 11 },
  { name: "Mar", assets: 40, bookings: 24, maintenance: 13 },
  { name: "Apr", assets: 52, bookings: 30, maintenance: 18 },
  { name: "May", assets: 68, bookings: 34, maintenance: 20 },
  { name: "Jun", assets: 82, bookings: 42, maintenance: 24 },
];

const pieData = [
  { name: "Booked", value: 35 },
  { name: "Available", value: 52 },
  { name: "Maintenance", value: 13 },
];

const colors = ["#2563eb", "#14b8a6", "#f43f5e"];

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">ERP Dashboard</p>
            <h1 className="mt-2 text-3xl font-semibold text-slate-900">AssetFlow Overview</h1>
            <p className="mt-2 text-sm text-slate-500">Monitor assets, bookings, and maintenance in one modern workspace.</p>
          </div>
          <button className="inline-flex items-center justify-center rounded-2xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition-default hover:bg-blue-700">
            View reports
          </button>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-4">
        {summaryCards.map((card) => (
          <div key={card.label} className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-slate-500">{card.label}</p>
                <p className="mt-4 text-3xl font-semibold text-slate-900">{card.value}</p>
              </div>
              <div className={`rounded-3xl px-3 py-2 text-sm font-semibold text-white ${card.color}`}>{card.change}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.7fr]">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500">Booking Activity</p>
              <h2 className="text-xl font-semibold text-slate-900">Monthly trends</h2>
            </div>
            <div className="inline-flex items-center gap-2 rounded-3xl bg-slate-100 px-4 py-2 text-sm text-slate-600">
              <span className="h-2.5 w-2.5 rounded-full bg-blue-600"></span>
              Assets
            </div>
          </div>
          <div className="h-[320px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 20, left: -16, bottom: 0 }}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="4 4" />
                <XAxis dataKey="name" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} />
                <Tooltip />
                <Line type="monotone" dataKey="assets" stroke="#2563eb" strokeWidth={4} dot={false} />
                <Line type="monotone" dataKey="bookings" stroke="#14b8a6" strokeWidth={4} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500">Utilization</p>
              <h2 className="text-xl font-semibold text-slate-900">Status distribution</h2>
            </div>
          </div>
          <div className="h-[320px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={70} outerRadius={110} paddingAngle={4}>
                  {pieData.map((entry, index) => (
                    <Cell key={entry.name} fill={colors[index % colors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-6 grid gap-3">
            {pieData.map((item, index) => (
              <div key={item.name} className="flex items-center justify-between rounded-2xl bg-slate-50 px-4 py-3">
                <div className="flex items-center gap-3">
                  <span className={`h-3.5 w-3.5 rounded-full bg-[${colors[index]}]`} />
                  <span className="text-sm text-slate-700">{item.name}</span>
                </div>
                <span className="text-sm font-semibold text-slate-900">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500">Booking Status</p>
              <h2 className="text-lg font-semibold text-slate-900">Upcoming slot overview</h2>
            </div>
          </div>
          <div className="space-y-4">
            <div className="rounded-3xl border border-slate-100 bg-slate-50 p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-slate-600">Meeting Room A</p>
                <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">Upcoming</span>
              </div>
              <p className="mt-2 text-sm text-slate-500">Tomorrow • 09:00 - 10:00</p>
            </div>
            <div className="rounded-3xl border border-slate-100 bg-slate-50 p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-slate-600">Workshop Room</p>
                <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">Confirmed</span>
              </div>
              <p className="mt-2 text-sm text-slate-500">Today • 14:00 - 15:30</p>
            </div>
          </div>
        </div>

        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft xl:col-span-2">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500">Notifications</p>
              <h2 className="text-lg font-semibold text-slate-900">Recent activity</h2>
            </div>
          </div>
          <div className="space-y-4">
            <div className="rounded-3xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-700">New asset category created</p>
              <p className="mt-2 text-xs text-slate-500">2 mins ago</p>
            </div>
            <div className="rounded-3xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-700">Booking conflict resolved automatically</p>
              <p className="mt-2 text-xs text-slate-500">1 hour ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
