const categories = [
  { name: "Laptops", items: 68, status: "Active" },
  { name: "Vehicles", items: 12, status: "Scheduled" },
  { name: "Furniture", items: 89, status: "Active" },
  { name: "Software", items: 34, status: "Review" },
];

export function AssetCategoriesPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Asset categories</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Organize assets by category</h1>
        <p className="mt-2 text-sm text-slate-500">Define asset categories and monitor inventory health at a glance.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="grid gap-6 lg:grid-cols-2">
          {categories.map((category) => (
            <div key={category.name} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <div className="flex items-center justify-between gap-4">
                <p className="text-lg font-semibold text-slate-900">{category.name}</p>
                <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">{category.status}</span>
              </div>
              <p className="mt-3 text-sm text-slate-500">{category.items} items in this category</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
