const bookingPlans = [
  { title: "Meeting Room A", schedule: "Today, 09:00 - 10:00", status: "Confirmed" },
  { title: "Workshop Lab", schedule: "Tomorrow, 14:00 - 16:00", status: "Pending" },
  { title: "Parking Bay 3", schedule: "Friday, 08:00 - 12:00", status: "Confirmed" },
];

export function BookingsPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-soft">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Bookings</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-900">Resource bookings</h1>
        <p className="mt-2 text-sm text-slate-500">Review scheduled bookings and manage reservation status.</p>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-6 shadow-soft">
        <div className="space-y-4">
          {bookingPlans.map((booking) => (
            <div key={booking.title} className="rounded-[1.5rem] border border-slate-200 bg-white p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-900">{booking.title}</p>
                  <p className="mt-1 text-sm text-slate-500">{booking.schedule}</p>
                </div>
                <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">{booking.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
