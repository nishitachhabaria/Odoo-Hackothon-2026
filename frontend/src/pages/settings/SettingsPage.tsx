const settingsSections = [
  { title: "Profile settings", description: "Update personal and account settings." },
  { title: "Security", description: "Manage access controls and authentication." },
  { title: "System preferences", description: "Configure app behavior and notifications." },
];

export function SettingsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Settings</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Application settings</h1>
        <p className="mt-2 text-sm text-slate-500">Configure the AssetFlow workspace, permissions, and alerts.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {settingsSections.map((section) => (
          <div key={section.title} className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
            <h2 className="text-xl font-semibold text-slate-900">{section.title}</h2>
            <p className="mt-3 text-sm text-slate-500">{section.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
