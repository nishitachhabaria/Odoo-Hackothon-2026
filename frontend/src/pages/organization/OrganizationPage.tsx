const overviewCards = [
  { label: "Departments", value: "12", detail: "Active business units" },
  { label: "Employees", value: "368", detail: "Team members onboarded" },
  { label: "Asset Categories", value: "24", detail: "Category definitions" },
];

export function OrganizationPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Organization</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Team structure and asset organization</h1>
        <p className="mt-2 text-sm text-slate-500">Manage departments, employees, and asset categories from a single place.</p>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        {overviewCards.map((card) => (
          <div key={card.label} className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
            <p className="text-sm font-medium text-slate-500">{card.label}</p>
            <p className="mt-4 text-4xl font-semibold text-slate-900">{card.value}</p>
            <p className="mt-3 text-sm text-slate-500">{card.detail}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
          <h2 className="text-lg font-semibold text-slate-900">Department performance</h2>
          <p className="mt-2 text-sm text-slate-500">Spotlight on active team units and their asset ownership.</p>
        </div>
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
          <h2 className="text-lg font-semibold text-slate-900">Employee engagement</h2>
          <p className="mt-2 text-sm text-slate-500">View employee capacity, roles, and current allocations.</p>
        </div>
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
          <h2 className="text-lg font-semibold text-slate-900">Category trends</h2>
          <p className="mt-2 text-sm text-slate-500">Analyze how asset categories are distributed across departments.</p>
        </div>
      </div>
    </div>
  );
}
