const transfers = [
  { name: "Equipment relocation", status: "Scheduled", date: "Tomorrow" },
  { name: "Warehouse transfer", status: "In transit", date: "Today" },
  { name: "Office move", status: "Pending", date: "Next week" },
];

export function TransfersPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Transfers</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Asset transfers</h1>
        <p className="mt-2 text-sm text-slate-500">Manage assets moving between locations and departments.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="space-y-4">
          {transfers.map((transfer) => (
            <div key={transfer.name} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-900">{transfer.name}</p>
                  <p className="mt-1 text-sm text-slate-500">{transfer.date}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">{transfer.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
