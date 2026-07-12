const auditSummaries = [
  { title: "Asset lifecycle review", status: "Complete", updated: "2 days ago" },
  { title: "Safety compliance audit", status: "In progress", updated: "Today" },
  { title: "Inventory reconciliation", status: "Pending", updated: "Yesterday" },
];

export function AuditsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Audits</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Audit management</h1>
        <p className="mt-2 text-sm text-slate-500">Review audit status, compliance results, and inspection trends.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="space-y-4">
          {auditSummaries.map((audit) => (
            <div key={audit.title} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-900">{audit.title}</p>
                  <p className="mt-1 text-sm text-slate-500">Updated: {audit.updated}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">{audit.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
