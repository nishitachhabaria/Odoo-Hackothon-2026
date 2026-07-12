const employees = [
  { name: "Derek Morris", role: "Asset Coordinator", team: "Operations" },
  { name: "Priya Nair", role: "Maintenance Lead", team: "Engineering" },
  { name: "Nina Walker", role: "IT Procurement", team: "Facilities" },
  { name: "Sam Chen", role: "Finance Analyst", team: "Finance" },
];

export function EmployeesPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Employees</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Team members and roles</h1>
        <p className="mt-2 text-sm text-slate-500">Track employee assignments across departments and workflows.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="grid gap-6 md:grid-cols-2">
          {employees.map((employee) => (
            <div key={employee.name} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <p className="text-base font-semibold text-slate-900">{employee.name}</p>
              <p className="mt-2 text-sm text-slate-500">{employee.role}</p>
              <p className="mt-2 text-sm font-medium text-slate-700">{employee.team}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
