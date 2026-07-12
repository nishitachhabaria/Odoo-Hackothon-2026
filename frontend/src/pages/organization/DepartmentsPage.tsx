const departments = [
  { name: "Operations", head: "Asha Patel", assets: 48 },
  { name: "Engineering", head: "Marcus Lee", assets: 64 },
  { name: "Facilities", head: "Irene Cole", assets: 17 },
  { name: "Finance", head: "Rafael Santos", assets: 9 },
];

export function DepartmentsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Departments</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Manage business units</h1>
        <p className="mt-2 text-sm text-slate-500">Review departments, leadership, and asset ownership assignments.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="grid gap-6 md:grid-cols-2">
          {departments.map((department) => (
            <div key={department.name} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <p className="text-sm font-medium text-slate-500">{department.name}</p>
              <p className="mt-3 text-2xl font-semibold text-slate-900">{department.head}</p>
              <p className="mt-2 text-sm text-slate-500">{department.assets} assigned assets</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
