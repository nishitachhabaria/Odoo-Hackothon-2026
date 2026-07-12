const reports = [
  { title: "Asset utilization", summary: "Track asset usage and availability." },
  { title: "Booking trends", summary: "See reservation volume and peak times." },
  { title: "Maintenance history", summary: "Analyze service records and compliance." },
];

export function ReportsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Reports</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Business reports</h1>
        <p className="mt-2 text-sm text-slate-500">View summary reports for assets, bookings, maintenance, and operations.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {reports.map((report) => (
          <div key={report.title} className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
            <h2 className="text-xl font-semibold text-slate-900">{report.title}</h2>
            <p className="mt-3 text-sm text-slate-500">{report.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
