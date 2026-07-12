const notifications = [
  { message: "New booking request pending approval.", time: "5 minutes ago" },
  { message: "Asset category updated successfully.", time: "1 hour ago" },
  { message: "Maintenance task marked complete.", time: "Today" },
];

export function NotificationsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Notifications</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Activity center</h1>
        <p className="mt-2 text-sm text-slate-500">Stay on top of recent system updates and workflow alerts.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div key={notification.message} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <p className="text-sm text-slate-900">{notification.message}</p>
              <p className="mt-2 text-xs text-slate-500">{notification.time}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
