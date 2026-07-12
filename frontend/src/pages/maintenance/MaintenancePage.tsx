const maintenanceTasks = [
  { task: "Server room inspection", due: "Today", status: "Scheduled" },
  { task: "Air conditioner filter replacement", due: "Tomorrow", status: "Pending" },
  { task: "Asset audit preparation", due: "Friday", status: "In progress" },
];

export function MaintenancePage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Maintenance</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Maintenance operations</h1>
        <p className="mt-2 text-sm text-slate-500">Manage upcoming maintenance tasks and asset service schedules.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="space-y-4">
          {maintenanceTasks.map((item) => (
            <div key={item.task} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-900">{item.task}</p>
                  <p className="mt-1 text-sm text-slate-500">Due: {item.due}</p>
                </div>
                <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">{item.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
