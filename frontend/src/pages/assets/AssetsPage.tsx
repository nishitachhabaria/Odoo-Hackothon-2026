const assets = [
  { name: "Desktop Workstation", category: "Computers", status: "Available" },
  { name: "Forklift", category: "Vehicles", status: "In Use" },
  { name: "Office Chair", category: "Furniture", status: "Available" },
  { name: "CRM License", category: "Software", status: "Renewal" },
];

export function AssetsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Assets</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Asset inventory</h1>
        <p className="mt-2 text-sm text-slate-500">Explore assigned assets and monitor availability across the organization.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="space-y-4">
          {assets.map((asset) => (
            <div key={asset.name} className="rounded-[1.5rem] border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-900">{asset.name}</p>
                  <p className="mt-1 text-sm text-slate-500">{asset.category}</p>
                </div>
                <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">{asset.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
