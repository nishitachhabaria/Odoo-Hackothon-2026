export function AllocationsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Asset allocation</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Allocation workflows</h1>
        <p className="mt-2 text-sm text-slate-500">View current allocations and manage resource delivery across departments.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
          <h2 className="text-xl font-semibold text-slate-900">Allocation summary</h2>
          <p className="mt-3 text-sm text-slate-500">Assets currently assigned to projects and teams.</p>
        </div>
        <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
          <h2 className="text-xl font-semibold text-slate-900">Pending approvals</h2>
          <p className="mt-3 text-sm text-slate-500">Track allocation requests awaiting review.</p>
        </div>
      </div>
    </div>
  );
}
